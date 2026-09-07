"""Local web Product Shell for the bounded Apex MVP."""

from __future__ import annotations

import argparse
import hmac
import json
import mimetypes
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .application import ApexApplication, ApplicationError, ProjectSelectionError, TaskBusyError


SHELL_ROOT = Path(__file__).resolve().parent.parent / "product_shell"
OPENWORK_DIST = SHELL_ROOT / "openwork" / "dist"


class _ShellHandler(BaseHTTPRequestHandler):
    application: ApexApplication
    shell_root: Path = SHELL_ROOT

    def do_GET(self) -> None:  # noqa: N802 - stdlib handler API
        parsed = urlparse(self.path)
        try:
            if parsed.path == "/":
                self._static_response(self.shell_root / "index.html")
            elif parsed.path.startswith("/assets/"):
                relative = Path(parsed.path.lstrip("/"))
                candidate = (self.shell_root / relative).resolve()
                if self.shell_root.resolve() not in candidate.parents:
                    self._json_response({"error": "shell asset path denied"}, HTTPStatus.NOT_FOUND)
                else:
                    self._static_response(candidate)
            elif parsed.path == "/api/health":
                self._json_response({"ok": True, "service": "apex-local-shell"})
            elif parsed.path == "/api/project":
                query = parse_qs(parsed.query)
                if query.get("path"):
                    self.application.open_project(query["path"][0])
                self._json_response(self.application.project_summary())
            elif parsed.path == "/api/providers":
                self._json_response(self.application.provider_state())
            elif parsed.path == "/api/status":
                self._json_response(self.application.status())
            elif parsed.path == "/api/history":
                self._json_response(self.application.history())
            elif parsed.path == "/api/artifact":
                query = parse_qs(parsed.query)
                name = query.get("name", [""])[0]
                self._json_response(self.application.artifact(name))
            else:
                self._json_response({"error": "not found"}, HTTPStatus.NOT_FOUND)
        except ApplicationError as exc:
            self._json_response({"error": str(exc)}, HTTPStatus.CONFLICT if isinstance(exc, TaskBusyError) else HTTPStatus.BAD_REQUEST)

    def do_POST(self) -> None:  # noqa: N802 - stdlib handler API
        parsed = urlparse(self.path)
        try:
            if parsed.path.startswith("/api/internal/"):
                if not self._internal_authorized():
                    self._json_response({"error": "not found"}, HTTPStatus.NOT_FOUND)
                    return
                body = self._read_json()
                if parsed.path == "/api/internal/provider-runtime":
                    if not body.get("provider_id") or not body.get("model_id"):
                        self._json_response(self.application.clear_provider_runtime())
                        return
                    self._json_response(
                        self.application.configure_provider(
                            str(body.get("provider_id", "")),
                            str(body.get("model_id", "")),
                            body.get("credential") if isinstance(body.get("credential"), str) else None,
                        )
                    )
                    return
                if parsed.path == "/api/internal/provider-test":
                    self._json_response(
                        self.application.test_provider_configuration(
                            str(body.get("provider_id", "")),
                            str(body.get("model_id", "")),
                            body.get("credential") if isinstance(body.get("credential"), str) else None,
                        )
                    )
                    return
                self._json_response({"error": "not found"}, HTTPStatus.NOT_FOUND)
                return
            body = self._read_json()
            if parsed.path == "/api/project":
                self._json_response(self.application.open_project(body.get("path", "")))
            elif parsed.path == "/api/tasks":
                self._json_response(self.application.submit_task(body.get("task", "report")), HTTPStatus.ACCEPTED)
            else:
                self._json_response({"error": "not found"}, HTTPStatus.NOT_FOUND)
        except (ApplicationError, TypeError, ValueError, json.JSONDecodeError) as exc:
            self._json_response({"error": str(exc)}, HTTPStatus.BAD_REQUEST)

    def log_message(self, format: str, *args: object) -> None:
        # Keep the local shell quiet and avoid echoing request data into logs.
        return

    def _read_json(self) -> dict[str, object]:
        length = int(self.headers.get("Content-Length", "0"))
        if length > 16_384:
            raise ValueError("request body is too large")
        data = json.loads(self.rfile.read(length).decode("utf-8")) if length else {}
        if not isinstance(data, dict):
            raise ValueError("request body must be an object")
        return data

    def _internal_authorized(self) -> bool:
        expected = os.environ.get("APEX_INTERNAL_TOKEN", "")
        supplied = self.headers.get("X-Apex-Internal-Token", "")
        return bool(expected) and hmac.compare_digest(supplied, expected)

    def _static_response(self, path: Path) -> None:
        if not path.is_file():
            self._json_response({"error": "shell asset missing"}, HTTPStatus.INTERNAL_SERVER_ERROR)
            return
        content = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        self.send_header("Content-Type", f"{content_type}; charset=utf-8" if content_type.startswith(("text/", "application/javascript")) else content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)

    def _json_response(self, payload: dict[str, object], status: HTTPStatus = HTTPStatus.OK) -> None:
        content = json.dumps(payload, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)


class ShellServer(ThreadingHTTPServer):
    allow_reuse_address = True

    def __init__(self, address: tuple[str, int], application: ApexApplication, shell_root: Path = SHELL_ROOT) -> None:
        handler = type("ApexShellHandler", (_ShellHandler,), {"application": application, "shell_root": shell_root})
        super().__init__(address, handler)
        self.application = application
        self.shell_root = shell_root

    def server_close(self) -> None:
        self.application.close()
        super().server_close()


def serve(host: str = "127.0.0.1", port: int = 0, workspace: Path | None = None, ui: str = "bootstrap") -> ShellServer:
    application = ApexApplication()
    if workspace is not None:
        application.open_project(workspace)
    shell_root = OPENWORK_DIST if ui == "openwork" else SHELL_ROOT
    if ui == "openwork" and not (shell_root / "index.html").is_file():
        application.close()
        raise ApplicationError("OpenWork shell is not built; run npm install && npm run build in product_shell/openwork")
    server = ShellServer((host, port), application, shell_root)
    return server


def main() -> int:
    parser = argparse.ArgumentParser(description="Launch the local Apex Code Product Shell")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8787)
    parser.add_argument("--workspace", type=Path)
    parser.add_argument("--ui", choices=("openwork", "bootstrap"), default="openwork")
    args = parser.parse_args()
    try:
        server = serve(args.host, args.port, args.workspace, args.ui)
    except (ProjectSelectionError, ApplicationError) as exc:
        parser.error(str(exc))
    print(f"Apex Code shell listening at http://{server.server_address[0]}:{server.server_address[1]}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        return 0
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
