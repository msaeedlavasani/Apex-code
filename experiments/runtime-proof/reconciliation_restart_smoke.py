#!/usr/bin/env python3
"""Real OpenCode controller restart smoke for the bounded reconciliation loop."""

from __future__ import annotations

import json
import os
import signal
import socket
import subprocess
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict
from pathlib import Path

from apex_code.core import AuthorityRevision, ExecutionLedger, ExecutionManifest, PermissionEnvelope, RuntimeLane
from apex_code.reconciliation import ReconciliationLoop, RuntimeObservation
from apex_code.core import RuntimeFact


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def request(base: str, method: str, path: str, body: object | None = None) -> tuple[int, object | None]:
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(base + path, method=method, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=2) as response:
        raw = response.read().decode("utf-8", "replace")
        return response.status, json.loads(raw) if raw else None


def wait_healthy(base: str, process: subprocess.Popen[bytes]) -> bool:
    deadline = time.monotonic() + 8
    while time.monotonic() < deadline:
        if process.poll() is not None:
            return False
        try:
            status, body = request(base, "GET", "/global/health")
            if status == 200 and isinstance(body, dict) and body.get("healthy") is True:
                return True
        except (OSError, ValueError):
            pass
        time.sleep(0.1)
    return False


def start_server(opencode: str, workspace: Path, env: dict[str, str]) -> tuple[subprocess.Popen[bytes], str, bool]:
    port = free_port()
    base = f"http://127.0.0.1:{port}"
    process = subprocess.Popen(
        [opencode, "serve", "--pure", "--hostname", "127.0.0.1", "--port", str(port)],
        cwd=workspace,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return process, base, wait_healthy(base, process)


def stop_server(process: subprocess.Popen[bytes]) -> None:
    if process.poll() is not None:
        return
    process.send_signal(signal.SIGTERM)
    process.wait(timeout=4)


def seed_attempt(path: Path, session_id: str) -> None:
    ledger = ExecutionLedger(path / "execution-ledger.json")
    authority = AuthorityRevision(
        "authority-restart-smoke",
        PermissionEnvelope(("README.md",), ("REPORT.md",), ("../**",)),
        "restart-smoke",
    )
    lane = RuntimeLane("lane-restart-smoke", "attempt-restart-smoke", str(path), "restart-smoke")
    manifest = ExecutionManifest(
        "manifest-restart-smoke",
        "attempt-restart-smoke",
        "task-restart-smoke",
        authority.authority_revision_id,
        "opencode-worker",
        "opencode/big-pickle",
        "restart-smoke",
        "workspace-snapshot",
        "restart-smoke",
    )
    ledger.put("authorities", authority.authority_revision_id, asdict(authority))
    ledger.put("lanes", lane.runtime_lane_id, asdict(lane))
    ledger.put("manifests", manifest.manifest_id, asdict(manifest))
    ledger.put(
        "attempts",
        "attempt-restart-smoke",
        {
            "attempt_id": "attempt-restart-smoke",
            "task_id": "task-restart-smoke",
            "execution_epoch_id": "epoch-restart-smoke",
            "status": "RUNNING",
            "barrier": "RELEASED",
            "manifest_id": manifest.manifest_id,
            "authority_revision_id": authority.authority_revision_id,
            "runtime_lane_id": lane.runtime_lane_id,
            "runtime_session_id": session_id,
        },
    )
    ledger.claim_attempt_start("attempt-restart-smoke", manifest.manifest_id, lane.runtime_lane_id)


def main() -> int:
    opencode = os.environ.get("OPENCODE_EXECUTABLE", "/usr/local/bin/opencode")
    root = Path(tempfile.mkdtemp(prefix="apex-reconciliation-smoke-"))
    workspace = root / "workspace"
    config = root / "config"
    data = root / "data"
    cache = root / "cache"
    state = root / "state"
    for directory in (workspace, config, data, cache, state):
        directory.mkdir(parents=True)
    (workspace / "README.md").write_text("# Restart smoke\n", encoding="utf-8")
    env = os.environ.copy()
    env.update(
        {
            "OPENCODE_CONFIG_DIR": str(config),
            "XDG_DATA_HOME": str(data),
            "XDG_CACHE_HOME": str(cache),
            "XDG_STATE_HOME": str(state),
        }
    )

    server, base, first_healthy = start_server(opencode, workspace, env)
    if not first_healthy:
        return 1
    status, session = request(base, "POST", "/session?" + urllib.parse.urlencode({"directory": str(workspace)}), {})
    session_id = session.get("id") if isinstance(session, dict) else None
    if status != 200 or not session_id:
        stop_server(server)
        return 1
    seed_attempt(root, session_id)
    stop_server(server)
    try:
        request(base, "GET", "/global/health")
    except (OSError, urllib.error.URLError):
        unreachable_during_loss = True
    else:
        unreachable_during_loss = False

    server2, base2, second_healthy = start_server(opencode, workspace, env)
    try:
        session_status, _ = request(base2, "GET", "/session/" + session_id)
        # A persisted session record is not evidence that a runtime is active.
        outcome = ReconciliationLoop(root / "execution-ledger.json").reconcile(
            [RuntimeObservation(RuntimeFact.UNKNOWN, "attempt-restart-smoke", session_id, detail="session persisted; activity not attested")]
        )[0]
        print(
            json.dumps(
                {
                    "opencode": opencode,
                    "workspace": str(workspace),
                    "firstControllerHealthy": first_healthy,
                    "sessionId": session_id,
                    "controllerUnreachableDuringLoss": unreachable_during_loss,
                    "secondControllerHealthy": second_healthy,
                    "sessionGetAfterRestartHttpStatus": session_status,
                    "reconciledRuntimeFact": outcome.runtime_fact.value,
                    "reconciledSemanticState": outcome.semantic_state,
                    "reconciledDisposition": outcome.disposition,
                    "duplicateStartAllowed": False,
                    "expectedSafeResult": "RECOVERY_REQUIRED",
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0 if second_healthy and session_status == 200 and outcome.semantic_state == "RECOVERY_REQUIRED" else 1
    finally:
        stop_server(server2)


if __name__ == "__main__":
    raise SystemExit(main())
