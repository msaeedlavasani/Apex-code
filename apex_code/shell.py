"""Local web Product Shell for the bounded Apex MVP."""

from __future__ import annotations

import argparse
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .application import ApexApplication, ApplicationError, ProjectSelectionError, TaskBusyError


SHELL_ROOT = Path(__file__).resolve().parent.parent / "product_shell"


class _ShellHandler(BaseHTTPRequestHandler):
    application: ApexApplication

    def do_GET(self) -> None:  # noqa: N802 - stdlib handler API
        parsed = urlparse(self.path)
        try:
            if parsed.path == "/":
                self._file_response(SHELL_ROOT / "index.html", "text/html; charset=utf-8")
            elif parsed.path == "/assets/app.css":
                self._file_response(SHELL_ROOT / "app.css", "text/css; charset=utf-8")
            elif parsed.path == "/assets/app.js":
                self._file_response(SHELL_ROOT / "app.js", "text/javascript; charset=utf-8")
            elif parsed.path == "/api/health":
                self._json_response({"ok": True, "service": "apex-local-shell"})
            elif parsed.path == "/api/project":
                query = parse_qs(parsed.query)
                if query.get("path"):
                    self.application.open_project(query["path"][0])
                self._json_response(self.application.project_summary())
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

    def _file_response(self, path: Path, content_type: str) -> None:
        if not path.is_file():
            self._json_response({"error": "shell asset missing"}, HTTPStatus.INTERNAL_SERVER_ERROR)
            return
        content = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
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

    def __init__(self, address: tuple[str, int], application: ApexApplication) -> None:
        handler = type("ApexShellHandler", (_ShellHandler,), {"application": application})
        super().__init__(address, handler)
        self.application = application

    def server_close(self) -> None:
        self.application.close()
        super().server_close()


def serve(host: str = "127.0.0.1", port: int = 0, workspace: Path | None = None) -> ShellServer:
    application = ApexApplication()
    if workspace is not None:
        application.open_project(workspace)
    server = ShellServer((host, port), application)
    return server


def main() -> int:
    parser = argparse.ArgumentParser(description="Launch the local Apex Code Product Shell")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8787)
    parser.add_argument("--workspace", type=Path)
    args = parser.parse_args()
    try:
        server = serve(args.host, args.port, args.workspace)
    except ProjectSelectionError as exc:
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
