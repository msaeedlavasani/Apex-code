#!/usr/bin/env python3
"""Disposable, non-secret Goose capability probe.

This is experiment-only tooling. It never imports Apex production modules,
uses a user profile, or prints command output from the probed runtime.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path


def safe_environment(root: Path) -> dict[str, str]:
    keep = {"PATH", "LANG", "LC_ALL", "LC_CTYPE", "TERM", "TMPDIR"}
    env = {key: value for key, value in os.environ.items() if key in keep}
    env["HOME"] = str(root / "home")
    env["GOOSE_PATH_ROOT"] = str(root)
    return env


def run_probe(goose: str, args: list[str], root: Path, timeout: int = 15) -> dict[str, object]:
    try:
        completed = subprocess.run(
            [goose, *args],
            env=safe_environment(root),
            cwd=root,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return {"returncode": None, "timed_out": True, "stdout_present": False, "stderr_present": False}
    return {
        "returncode": completed.returncode,
        "timed_out": False,
        "stdout_present": bool(completed.stdout),
        "stderr_present": bool(completed.stderr),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--goose", required=True, help="absolute path to the disposable Goose executable")
    parser.add_argument("--root", type=Path, help="isolated GOOSE_PATH_ROOT; created when omitted")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    goose = str(Path(args.goose).resolve())
    if not Path(goose).is_file():
        raise SystemExit(f"Goose executable not found: {goose}")

    owned_root = args.root is None
    root_context = tempfile.TemporaryDirectory(prefix="apex-goose-capability-") if owned_root else None
    root = Path(root_context.name) if root_context else args.root.resolve()
    root.mkdir(parents=True, exist_ok=True)
    (root / "config").mkdir(exist_ok=True)
    (root / "data").mkdir(exist_ok=True)
    (root / "state").mkdir(exist_ok=True)
    (root / "home").mkdir(exist_ok=True)

    permission = "user:\n  always_allow: []\n  ask_before: []\n  never_allow:\n    - developer__shell\n    - developer__computer\n"
    permission_path = root / "config" / "permission.yaml"
    permission_path.write_text(permission, encoding="utf-8")

    probes = {
        "info": run_probe(goose, ["info"], root),
        "run_help": run_probe(goose, ["run", "--help"], root),
        "acp_help": run_probe(goose, ["acp", "--help"], root),
        "session_help": run_probe(goose, ["session", "--help"], root),
        "isolated_no_credential_run": run_probe(
            goose,
            [
                "run",
                "--no-session",
                "--no-profile",
                "--output-format",
                "json",
                "--provider",
                "ollama",
                "--model",
                "llama3.2",
                "--max-turns",
                "1",
                "-t",
                "Respond with exactly READY and do not use tools.",
            ],
            root,
            timeout=10,
        ),
    }

    result = {
        "probe": "Goose capability probe (experiment-only)",
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "executable": goose,
        "goose_path_root": str(root),
        "isolated_environment": True,
        "credentials_supplied": False,
        "permission_config": {
            "path": str(permission_path),
            "sha256": hashlib.sha256(permission.encode()).hexdigest(),
            "content_printed": False,
        },
        "probes": probes,
        "interpretation": {
            "cli_and_help_surface": "observed from successful help/info probes",
            "noninteractive_execution": "not established without a configured provider",
            "session_persistence": "surface available; no semantic Apex identity inferred",
            "authority_binding": "not tested; config materialization is not activation attestation",
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if root_context:
        root_context.cleanup()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
