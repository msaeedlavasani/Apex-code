#!/usr/bin/env python3
"""Bounded OpenCode authority-attestation probe.

This is experiment-only code.  It starts isolated OpenCode servers, creates
harmless sessions, and records metadata/status shapes without running an
agent tool or printing response content.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import socket
import subprocess
import tempfile
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


OPENCODE_SOURCE_SHA = "e207624c48159b03dbe17dbc8e51bbcf23e72df5"
OPENCODE_VERSION = "1.18.25"


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def request(base: str, method: str, path: str, payload: dict | None = None) -> dict:
    body = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    try:
        with urlopen(Request(base + path, data=body, headers=headers, method=method), timeout=8) as response:
            raw = response.read()
            value = json.loads(raw.decode("utf-8")) if raw else None
            return {"http": response.status, "json": summarize(value)}
    except HTTPError as error:
        raw = error.read()
        try:
            value = json.loads(raw.decode("utf-8")) if raw else None
        except json.JSONDecodeError:
            value = None
        return {"http": error.code, "json": summarize(value)}
    except (URLError, TimeoutError, OSError) as error:
        return {"error": type(error).__name__}


def summarize(value: object) -> object:
    """Keep only non-sensitive shape and identity metadata."""
    if isinstance(value, dict):
        result: dict[str, object] = {}
        for key, item in value.items():
            if key in {"data", "info"} and isinstance(item, dict):
                result[key] = summarize(item)
            elif key in {"id", "sessionID", "status", "healthy", "type", "cursor", "admittedSeq"}:
                result[key] = summarize(item)
            elif key in {"message", "error"}:
                result[key] = type(item).__name__
        return result
    if isinstance(value, list):
        return {"count": len(value), "item_keys": sorted(value[0].keys()) if value and isinstance(value[0], dict) else []}
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return type(value).__name__


def authority_config() -> dict[str, object]:
    return {
        "$schema": "https://opencode.ai/config.json",
        "permission": {
            "read": "deny",
            "edit": "deny",
            "bash": "deny",
            "external_directory": "deny",
        },
    }


def run_server(config_root: Path, workspace: Path, label: str) -> dict[str, object]:
    port = free_port()
    config = authority_config()
    config_path = config_root / "opencode.json"
    config_path.write_text(json.dumps(config, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    config_bytes = config_path.read_bytes()
    config_digest = hashlib.sha256(config_bytes).hexdigest()
    revision_id = f"authority-{label}"
    (config_root / "authority-revision-id").write_text(revision_id + "\n", encoding="utf-8")
    (config_root / "authority-config-digest").write_text(config_digest + "\n", encoding="utf-8")

    env = os.environ.copy()
    env.update(
        {
            "OPENCODE_CONFIG_DIR": str(config_root),
            "OPENCODE_CONFIG_CONTENT": json.dumps(config, sort_keys=True),
            "XDG_DATA_HOME": str(config_root / "data"),
            "XDG_CACHE_HOME": str(config_root / "cache"),
            "XDG_STATE_HOME": str(config_root / "state"),
        }
    )
    command = [
        "opencode",
        "serve",
        "--pure",
        "--hostname",
        "127.0.0.1",
        "--port",
        str(port),
    ]
    process = subprocess.Popen(command, cwd=workspace, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    base = f"http://127.0.0.1:{port}"
    health: dict[str, object] = {"error": "not_observed"}
    for _ in range(40):
        health = request(base, "GET", "/api/health")
        if health.get("http") == 200:
            break
        time.sleep(0.25)
    session = request(base, "POST", "/api/session", {"location": {"directory": str(workspace)}})
    session_id = None
    if isinstance(session.get("json"), dict):
        data = session["json"].get("data")
        if isinstance(data, dict):
            session_id = data.get("id")
    session_get = request(base, "GET", f"/api/session/{session_id}") if isinstance(session_id, str) else {"error": "no_session_id"}
    active = request(base, "GET", "/api/session/active")
    permissions = request(base, "GET", f"/api/session/{session_id}/permission") if isinstance(session_id, str) else {"error": "no_session_id"}
    process.terminate()
    try:
        process.wait(timeout=8)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=8)
    return {
        "label": label,
        "command": command,
        "server_pid": process.pid,
        "workspace": str(workspace),
        "config_path": str(config_path),
        "authority_revision_id": revision_id,
        "authority_config_digest": config_digest,
        "config_written_before_server_start": True,
        "health": health,
        "session_create": session,
        "session_id": session_id,
        "session_get": session_get,
        "active_sessions": active,
        "permission_surface": permissions,
    }


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="apex-opencode-authority-probe-") as raw:
        root = Path(raw)
        workspace = root / "workspace"
        workspace.mkdir()
        (workspace / "allowed").mkdir()
        (workspace / "output").mkdir()
        (workspace / "allowed" / "sentinel.txt").write_text("harmless sentinel\n", encoding="utf-8")
        results = []
        for label in ("revision-a", "revision-b"):
            config_root = root / label
            config_root.mkdir()
            results.append(run_server(config_root, workspace, label))
        print(
            json.dumps(
                {
                    "repository": "anomalyco/opencode",
                    "source_sha": OPENCODE_SOURCE_SHA,
                    "installed_version": OPENCODE_VERSION,
                    "executable": os.path.realpath("/usr/local/bin/opencode"),
                    "installed_binary_source_identity": "NOT_PROVEN",
                    "observations": results,
                    "side_effecting_agent_prompt_sent": False,
                    "secret_content_read_or_printed": False,
                },
                indent=2,
                sort_keys=True,
            )
        )


if __name__ == "__main__":
    main()
