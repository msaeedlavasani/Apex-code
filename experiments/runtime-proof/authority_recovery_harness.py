#!/usr/bin/env python3
"""Disposable, dependency-free runtime-proof harness.

This is research tooling only. It does not implement an Apex runtime,
Runtime Adapter, authority engine, or ResourceLease. It starts the installed
OpenCode server in a temporary workspace and uses harmless subprocess fixtures
to probe controller-loss and local resource behavior.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


RUNTIME_FIXTURE = r"""
import pathlib, sys, time
root = pathlib.Path(sys.argv[1])
duration = float(sys.argv[2])
root.mkdir(parents=True, exist_ok=True)
(root / "started").write_text("started\n", encoding="utf-8")
time.sleep(duration)
(root / "completed").write_text("completed\n", encoding="utf-8")
"""

LOCK_FIXTURE = r"""
import pathlib, sys, time
lock = pathlib.Path(sys.argv[1])
result = pathlib.Path(sys.argv[2])
try:
    lock.mkdir()
except FileExistsError:
    result.write_text("LOST\n", encoding="utf-8")
else:
    result.write_text("WON\n", encoding="utf-8")
    time.sleep(0.4)
"""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def request(base: str, method: str, path: str, body: object | None = None) -> dict:
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        base + path,
        data=data,
        method=method,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=2) as response:
            raw = response.read().decode("utf-8", "replace")
            return {"http_status": response.status, "body": json.loads(raw) if raw else None}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", "replace")
        return {"http_status": exc.code, "body": raw[:200]}


def wait_health(base: str, process: subprocess.Popen[bytes], timeout: float = 8) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.poll() is not None:
            return False
        try:
            result = request(base, "GET", "/global/health")
            if result.get("http_status") == 200 and result.get("body", {}).get("healthy") is True:
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
    return process, base, wait_health(base, process)


def stop_process(process: subprocess.Popen[bytes] | None) -> None:
    if process is None or process.poll() is not None:
        return
    process.send_signal(signal.SIGTERM)
    try:
        process.wait(timeout=3)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=3)


def start_fixture(path: Path, duration: float) -> subprocess.Popen[bytes]:
    return subprocess.Popen(
        [sys.executable, "-c", RUNTIME_FIXTURE, str(path), str(duration)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--opencode", default="opencode")
    args = parser.parse_args()

    root = Path(tempfile.mkdtemp(prefix="apex-runtime-proof-"))
    workspace = root / "workspace"
    config = root / "config"
    data = root / "data"
    cache = root / "cache"
    state = root / "state"
    for directory in (workspace, config, data, cache, state):
        directory.mkdir(parents=True)
    (workspace / "allowed").mkdir()
    (workspace / "output").mkdir()
    (workspace / "forbidden").mkdir()
    (workspace / "allowed" / "read.txt").write_text("allowed-sentinel\n", encoding="utf-8")
    (workspace / "forbidden" / "read.txt").write_text("forbidden-sentinel\n", encoding="utf-8")

    authority = {
        "authorityRevisionId": "ar-runtime-proof-001",
        "permissionEnvelope": {
            "read": ["workspace/allowed/**"],
            "write": ["workspace/output/**"],
            "deny": ["workspace/forbidden/**", "outside-workspace/**"],
        },
    }
    authority_path = config / "authority-revision-001.json"
    authority_path.write_text(json.dumps(authority, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    authority_digest = sha256(authority_path)
    runtime_config = {
        "$schema": "https://opencode.ai/config.json",
        "permission": {"read": "deny", "edit": "deny", "bash": "deny", "external_directory": "deny"},
    }
    config_path = config / "opencode.json"
    config_path.write_text(json.dumps(runtime_config, sort_keys=True, indent=2) + "\n", encoding="utf-8")

    env = os.environ.copy()
    env.update(
        {
            "OPENCODE_CONFIG_DIR": str(config),
            "OPENCODE_CONFIG_CONTENT": json.dumps(runtime_config),
            "XDG_DATA_HOME": str(data),
            "XDG_CACHE_HOME": str(cache),
            "XDG_STATE_HOME": str(state),
        }
    )

    ledger = {
        "attemptId": "attempt-runtime-proof-001",
        "runtimeLaneId": "lane-runtime-proof-001",
        "runtimeSessionId": None,
        "authorityRevisionId": authority["authorityRevisionId"],
        "executionEpochId": "epoch-runtime-proof-001",
        "authorityDigest": authority_digest,
        "manifestImmutableAt": utc_now(),
    }
    (root / "ledger.json").write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")

    observations: dict[str, object] = {
        "experimentStartedAt": utc_now(),
        "workspace": str(workspace),
        "configurationRoot": str(config),
        "authorityPath": str(authority_path),
        "authorityDigest": authority_digest,
        "runtimeConfigPath": str(config_path),
        "opencodeExecutable": shutil.which(args.opencode) or args.opencode,
        "opencodeVersion": None,
        "ledgerPath": str(root / "ledger.json"),
    }
    version = subprocess.run([args.opencode, "--version"], capture_output=True, text=True, check=False)
    observations["opencodeVersion"] = version.stdout.strip() or version.stderr.strip()

    server = None
    base = None
    session_id = None
    try:
        server, base, healthy = start_server(args.opencode, workspace, env)
        observations["serverStart"] = {"healthy": healthy, "base": base, "pid": server.pid}
        if healthy:
            created = request(base, "POST", "/session?" + urllib.parse.urlencode({"directory": str(workspace)}), {})
            observations["sessionCreate"] = {"http_status": created.get("http_status")}
            if isinstance(created.get("body"), dict):
                session_id = created["body"].get("id")
            ledger["runtimeSessionId"] = session_id
            (root / "ledger.json").write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
            observations["sessionId"] = session_id
            observations["sessionStatusBeforeLoss"] = request(base, "GET", "/session/status")

        output_probe = workspace / "output" / "write.txt"
        output_probe.write_text("output-sentinel\n", encoding="utf-8")
        observations["e1"] = {
            "materialization": "CONFIG_WRITTEN",
            "authorityDigest": authority_digest,
            "activationConfirmed": False,
            "identityBindingConfirmed": False,
            "negativeFilesystemProbe": {
                "permittedRead": (workspace / "allowed" / "read.txt").read_text(encoding="utf-8").strip() == "allowed-sentinel",
                "permittedWrite": output_probe.exists(),
                "forbiddenRead": "NOT_RUN",
                "forbiddenWrite": "NOT_RUN",
            },
            "preStartBarrier": "BLOCKED_BY_HARNESS_BEFORE_RUNTIME_FIXTURE_START",
            "classification": "NOT_PROVEN",
            "reason": "OpenCode exposed server/session identity and permission configuration, but no direct active-authority proof or exact Attempt/Epoch binding.",
        }

        # E2-A: controller loss while an external harmless runtime fixture remains alive.
        live_path = root / "e2a-live"
        live = start_fixture(live_path, 4)
        time.sleep(0.25)
        stop_process(server)
        controller_down_fixture_alive = live.poll() is None
        server2, base2, healthy2 = start_server(args.opencode, workspace, env)
        session_after_restart = (
            request(base2, "GET", "/session/" + str(session_id)) if healthy2 and session_id else None
        )
        observations["e2a"] = {
            "controllerStopped": True,
            "fixtureStillAlive": controller_down_fixture_alive,
            "controllerRestartHealthy": healthy2,
            "sessionGetAfterRestart": (
                session_after_restart.get("http_status") if isinstance(session_after_restart, dict) else None
            ),
            "runtimeFact": "RUNNING" if controller_down_fixture_alive else "UNKNOWN",
            "semanticClassification": "RECOVERY_REQUIRED",
            "note": "The fixture was not OpenCode-owned; this tests controller-loss observation mechanics, not an Apex reconciliation guarantee.",
        }
        stop_process(live)
        server = server2
        base = base2

        # E2-B: runtime dies while controller is down.
        dead_path = root / "e2b-dead"
        dead = start_fixture(dead_path, 10)
        time.sleep(0.2)
        stop_process(server)
        controller_down = True
        dead.terminate()
        dead.wait(timeout=3)
        server3, base3, healthy3 = start_server(args.opencode, workspace, env)
        observations["e2b"] = {
            "controllerStopped": controller_down,
            "runtimeProcessTerminated": True,
            "controllerRestartHealthy": healthy3,
            "runtimeFact": "MISSING" if not dead_path.joinpath("completed").exists() else "EXITED",
            "semanticClassification": "RECOVERY_REQUIRED",
        }
        server = server3
        base = base3

        # E2-C: completion marker exists while controller is down; semantic success is withheld.
        completed_path = root / "e2c-completed"
        completed = start_fixture(completed_path, 0.4)
        time.sleep(0.1)
        stop_process(server)
        completed.wait(timeout=3)
        server4, base4, healthy4 = start_server(args.opencode, workspace, env)
        result_available = completed_path.joinpath("completed").exists()
        observations["e2c"] = {
            "controllerStopped": True,
            "runtimeFact": "EXITED",
            "resultMarkerAvailable": result_available,
            "controllerRestartHealthy": healthy4,
            "semanticSuccess": "NOT_INFERRED",
            "semanticClassification": "VERIFICATION_REQUIRED",
        }
        server = server4
        base = base4

        # E2-D/E: transport loss and intentionally wrong identity.
        stop_process(server)
        unreachable = False
        try:
            request(base, "GET", "/global/health")
        except (OSError, urllib.error.URLError):
            unreachable = True
        server5, base5, healthy5 = start_server(args.opencode, workspace, env)
        wrong_id = request(base5, "GET", "/session/ses-runtime-proof-wrong")
        observations["e2d_e"] = {
            "healthAfterControllerStop": "UNREACHABLE" if unreachable else "UNKNOWN",
            "wrongIdentityHttpStatus": wrong_id.get("http_status"),
            "wrongIdentityFact": "MISMATCH" if wrong_id.get("http_status") == 404 else "UNKNOWN",
            "controllerRestartHealthy": healthy5,
        }
        server = server5
        base = base5

        # E2-F: no durable Attempt identity is supplied to OpenCode; two fixtures can start.
        dup_a = start_fixture(root / "duplicate-a", 1.2)
        dup_b = start_fixture(root / "duplicate-b", 1.2)
        time.sleep(0.2)
        observations["e2f"] = {
            "sameAttemptId": ledger["attemptId"],
            "firstFixtureAlive": dup_a.poll() is None,
            "secondFixtureAlive": dup_b.poll() is None,
            "duplicatePrevented": False,
            "safeClassification": "UNKNOWN",
            "reason": "The substrate/session API did not provide durable Apex Attempt admission or duplicate-start prevention.",
        }
        stop_process(dup_a)
        stop_process(dup_b)

        # E2-G: an unledgered fixture is visible to this harness but not to OpenCode.
        orphan = start_fixture(root / "orphan", 1.0)
        time.sleep(0.15)
        observations["e2g"] = {
            "fixtureAliveWithoutLedgerEntry": orphan.poll() is None,
            "harnessCanFlagOrphan": True,
            "substrateOrphanDetection": "NOT_OBSERVED",
            "safeClassification": "UNKNOWN",
        }
        stop_process(orphan)

        observations["e2"] = {
            "classification": "NOT_PROVEN",
            "reason": "OpenCode server/session persistence and transport identity were observable, but no durable controller-independent Attempt reconciliation contract was exposed.",
        }

        # E3: atomic local directory creation is a substrate primitive, not an Apex lease.
        lock = root / "exclusive-resource.lock"
        lock_a_result = root / "lock-a.result"
        lock_b_result = root / "lock-b.result"
        p_a = subprocess.Popen([sys.executable, "-c", LOCK_FIXTURE, str(lock), str(lock_a_result)])
        p_b = subprocess.Popen([sys.executable, "-c", LOCK_FIXTURE, str(lock), str(lock_b_result)])
        p_a.wait(timeout=3)
        p_b.wait(timeout=3)
        results = {lock_a_result.read_text(encoding="utf-8").strip(), lock_b_result.read_text(encoding="utf-8").strip()}
        observations["e3"] = {
            "exclusiveAtomic": results == {"WON", "LOST"},
            "reservationAvailable": lock.exists(),
            "stableOwnerIdentity": False,
            "persistsAfterControllerRestart": lock.exists(),
            "staleOwnershipDetected": "PATH_EXISTS_ONLY",
            "staleReclaimSafe": "NOT_PROVEN",
            "localProcessOnly": True,
            "classification": "PARTIAL_PRIMITIVE" if results == {"WON", "LOST"} else "NOT_PROVEN",
        }
        observations["e4"] = {
            "classification": "DEFERRED_NOT_APPLICABLE_TO_CURRENT_SUBSTRATE",
            "reason": "No meaningful OpenCode checkpoint/resume contract for external side effects was exposed by the inspected API/source boundary.",
        }
    finally:
        stop_process(server)

    observations["experimentFinishedAt"] = utc_now()
    observations["temporaryRoot"] = str(root)
    print(json.dumps(observations, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
