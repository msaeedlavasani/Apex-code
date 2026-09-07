#!/usr/bin/env python3
"""Bounded controller-loss probe against an isolated OpenCode server.

The server is the only OpenCode control process under test.  The harness does
not kill child processes, read response content, or use a real repository.
It records observable metadata and intentionally avoids treating a durable
session as proof of an Apex Attempt/runtime binding.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import socket
import subprocess
import tempfile
import threading
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def request(base: str, method: str, path: str, payload: dict | None = None, timeout: float = 8.0) -> dict:
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Accept": "application/json"}
    if payload is not None:
        headers["Content-Type"] = "application/json"
    try:
        with urlopen(Request(base + path, data=body, headers=headers, method=method), timeout=timeout) as response:
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
    if isinstance(value, dict):
        result: dict[str, object] = {}
        for key, item in value.items():
            if key in {"data", "info"} and isinstance(item, dict):
                result[key] = summarize(item)
            elif key in {"id", "sessionID", "status", "healthy", "type", "admittedSeq", "promotedSeq"}:
                result[key] = summarize(item)
            elif key in {"messages", "parts", "events"} and isinstance(item, list):
                result[key] = {
                    "count": len(item),
                    "types": sorted({str(x.get("info", {}).get("role")) for x in item if isinstance(x, dict)}),
                }
        return result
    if isinstance(value, list):
        return {"count": len(value)}
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return type(value).__name__


def children_of(pid: int) -> list[int]:
    result: list[int] = []
    try:
        lines = subprocess.check_output(["ps", "-axo", "pid=,ppid="], text=True).splitlines()
    except (OSError, subprocess.SubprocessError):
        return result
    for line in lines:
        fields = line.split()
        if len(fields) == 2 and fields[1] == str(pid):
            try:
                result.append(int(fields[0]))
            except ValueError:
                pass
    return sorted(result)


def start_server(config_root: Path, workspace: Path, port: int) -> tuple[subprocess.Popen[str], str]:
    config = {
        "$schema": "https://opencode.ai/config.json",
        "permission": {"read": "deny", "edit": "deny", "bash": "deny", "external_directory": "deny"},
    }
    (config_root / "opencode.json").write_text(json.dumps(config, sort_keys=True, indent=2) + "\n", encoding="utf-8")
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
    command = ["opencode", "serve", "--pure", "--hostname", "127.0.0.1", "--port", str(port)]
    process = subprocess.Popen(command, cwd=workspace, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    base = f"http://127.0.0.1:{port}"
    for _ in range(40):
        if request(base, "GET", "/api/health").get("http") == 200:
            return process, base
        time.sleep(0.25)
    return process, base


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="apex-opencode-reconciliation-probe-") as raw:
        root = Path(raw)
        workspace = root / "workspace"
        workspace.mkdir()
        (workspace / "sentinel.txt").write_text("harmless sentinel\n", encoding="utf-8")
        config_root = root / "config"
        config_root.mkdir()
        port = free_port()
        process, base = start_server(config_root, workspace, port)
        session_response = request(base, "POST", "/api/session", {"location": {"directory": str(workspace)}})
        session_id = None
        if isinstance(session_response.get("json"), dict):
            data = session_response["json"].get("data")
            if isinstance(data, dict):
                session_id = data.get("id")

        prompt_id = "msg_apex_reconciliation_probe_001"
        prompt_result: dict[str, object] = {"state": "NOT_STARTED"}

        def send_prompt() -> None:
            nonlocal prompt_result
            if not isinstance(session_id, str):
                prompt_result = {"state": "NO_SESSION"}
                return
            prompt_result = request(
                base,
                "POST",
                f"/api/session/{session_id}/prompt",
                {
                    "id": prompt_id,
                    "prompt": {"text": "Reply with a concise harmless status sentence. Do not use tools."},
                },
                timeout=30,
            )

        prompt_thread = threading.Thread(target=send_prompt, daemon=True)
        prompt_thread.start()
        active_samples: list[dict] = []
        for _ in range(20):
            active_samples.append(request(base, "GET", "/api/session/active"))
            if prompt_result.get("http") is not None or prompt_result.get("state") not in {"NOT_STARTED"}:
                break
            time.sleep(0.25)
        children_before = children_of(process.pid)
        process.kill()
        process.wait(timeout=10)
        prompt_thread.join(timeout=2)
        children_after = children_of(process.pid)

        restart_port = free_port()
        restarted, restarted_base = start_server(config_root, workspace, restart_port)
        session_after_restart = request(restarted_base, "GET", f"/api/session/{session_id}") if isinstance(session_id, str) else {"error": "no_session_id"}
        active_after_restart = request(restarted_base, "GET", "/api/session/active")
        messages_after_restart = request(restarted_base, "GET", f"/api/session/{session_id}/message") if isinstance(session_id, str) else {"error": "no_session_id"}
        duplicate_start = (
            request(
                restarted_base,
                "POST",
                f"/api/session/{session_id}/prompt",
                {
                    "id": prompt_id,
                    "prompt": {"text": "Duplicate bounded probe request; do not use tools."},
                    "resume": False,
                },
            )
            if isinstance(session_id, str)
            else {"error": "no_session_id"}
        )
        wrong_session = request(restarted_base, "GET", "/api/session/ses_stale_probe_identity")
        restarted.kill()
        restarted.wait(timeout=10)

        print(
            json.dumps(
                {
                    "repository": "anomalyco/opencode",
                    "source_sha": "e207624c48159b03dbe17dbc8e51bbcf23e72df5",
                    "installed_version": "1.18.25",
                    "workspace": str(workspace),
                    "authority_config_digest": hashlib.sha256((config_root / "opencode.json").read_bytes()).hexdigest(),
                    "session_id": session_id,
                    "controller_pid": process.pid,
                    "runtime_native_process_identity": "NOT_EXPOSED_AS_SEPARATE_IDENTITY",
                    "children_before_controller_loss": children_before,
                    "children_after_controller_loss": children_after,
                    "prompt_admission": prompt_result,
                    "active_samples_before_loss": active_samples,
                    "session_after_restart": session_after_restart,
                    "active_after_restart": active_after_restart,
                    "messages_after_restart": messages_after_restart,
                    "duplicate_same_message_id": duplicate_start,
                    "wrong_or_stale_session": wrong_session,
                    "controller_restart_performed": True,
                    "secret_content_read_or_printed": False,
                },
                indent=2,
                sort_keys=True,
            )
        )


if __name__ == "__main__":
    main()
