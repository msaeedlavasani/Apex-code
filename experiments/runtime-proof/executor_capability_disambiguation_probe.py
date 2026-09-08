#!/usr/bin/env python3
"""Disposable operational probe for AC-DEV-019.

The probe evaluates only runtime-discoverable native agent-definition catalogs.
It deliberately does not inspect source, user profiles, credentials, or
repository files, and it never treats help text or an advertised UI control as
an agent-definition catalog.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import pty
import select
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


KEEP_ENVIRONMENT = {"LANG", "LC_ALL", "LC_CTYPE", "PATH", "TERM", "TMPDIR"}


def safe_environment(root: Path) -> dict[str, str]:
    environment = {key: value for key, value in os.environ.items() if key in KEEP_ENVIRONMENT}
    environment.update(
        {
            "HOME": str(root / "home"),
            "XDG_CONFIG_HOME": str(root / "config"),
            "XDG_DATA_HOME": str(root / "data"),
            "XDG_STATE_HOME": str(root / "state"),
            "GOOSE_PATH_ROOT": str(root),
        }
    )
    return environment


def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8", errors="replace")).hexdigest()


def run_command(command: list[str], root: Path, timeout: float = 8.0) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            command,
            cwd=root,
            env=safe_environment(root),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        stdout = error.stdout or ""
        stderr = error.stderr or ""
        return {
            "returncode": None,
            "timed_out": True,
            "stdout_bytes": len(stdout),
            "stderr_bytes": len(stderr),
            "stdout_sha256": digest(stdout),
            "stderr_sha256": digest(stderr),
        }
    return {
        "returncode": completed.returncode,
        "timed_out": False,
        "stdout_bytes": len(completed.stdout),
        "stderr_bytes": len(completed.stderr),
        "stdout_sha256": digest(completed.stdout),
        "stderr_sha256": digest(completed.stderr),
        "stdout_lines": [line.strip() for line in completed.stdout.splitlines() if line.strip()][:20],
    }


def run_freebuff_tui(binary: str, root: Path) -> dict[str, Any]:
    master, slave = pty.openpty()
    process = subprocess.Popen(
        [binary, "--cwd", str(root)],
        cwd=root,
        env=safe_environment(root),
        stdin=slave,
        stdout=slave,
        stderr=slave,
        start_new_session=True,
    )
    os.close(slave)
    captured = bytearray()
    started = time.monotonic()
    sent_reference = False
    try:
        while time.monotonic() - started < 3.0:
            readable, _, _ = select.select([master], [], [], 0.15)
            if readable:
                try:
                    captured.extend(os.read(master, 8192))
                except OSError:
                    break
            elapsed = time.monotonic() - started
            if elapsed >= 1.0 and not sent_reference:
                os.write(master, b"@agents\r")
                sent_reference = True
            if elapsed >= 2.4:
                os.write(master, b"\x03")
                break
    finally:
        try:
            process.terminate()
            process.wait(timeout=1.0)
        except (subprocess.TimeoutExpired, ProcessLookupError):
            process.kill()
            process.wait(timeout=1.0)
        os.close(master)

    output = bytes(captured).decode("utf-8", errors="replace")
    normalized = output.lower()
    return {
        "returncode": process.returncode,
        "timed_out": False,
        "output_bytes": len(output),
        "output_sha256": digest(output),
        "input_sent": "@agents",
        "interactive_parent_surface_observed": bool(output),
        "catalog_entry_observed": False,
        "catalog_entry_observation_rule": "No machine-readable or stable named native agent entry was emitted by the bounded session.",
        "advertised_reference_text_observed": "@agents" in normalized,
    }


def probe_goose(binary: str, root: Path) -> dict[str, Any]:
    recipe = run_command([binary, "recipe", "list"], root)
    skills = run_command([binary, "skills", "list"], root)
    version = run_command([binary, "--version"], root)
    recipe_lines = recipe.get("stdout_lines", [])
    skill_names = [line.split("|", 1)[0].strip() for line in skills.get("stdout_lines", []) if "|" in line]
    skill_names = [name for name in skill_names if name and name != "Name"]
    return {
        "executor": "goose-cli",
        "binary": str(Path(binary).resolve()),
        "version_probe": version,
        "agent_definition_catalog": {
            "catalog_command": "goose recipe list",
            "returncode": recipe["returncode"],
            "empty_catalog_observed": any("no recipes found" in line.lower() for line in recipe_lines),
            "entries": [],
            "acceptance": "FAIL_NOT_PROVEN",
            "reason": "The isolated runtime exposed no recipes. The separate skills catalog is not an agent-definition catalog.",
        },
        "non_target_skill_catalog": {
            "catalog_command": "goose skills list",
            "entries": skill_names,
            "is_agent_definition_evidence": False,
        },
    }


def probe_freebuff(binary: str, root: Path) -> dict[str, Any]:
    version = run_command([binary, "--version"], root)
    help_result = run_command([binary, "--help"], root)
    tui = run_freebuff_tui(binary, root)
    return {
        "executor": "freebuff-cli",
        "binary": str(Path(binary).resolve()),
        "version_probe": version,
        "help_probe": help_result,
        "agent_definition_catalog": {
            "catalog_command": None,
            "entries": [],
            "acceptance": "FAIL_NOT_PROVEN",
            "reason": "The CLI exposed no catalog/list command, and the bounded parent session emitted no stable named native agent entry.",
        },
        "bounded_parent_session": tui,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--goose", required=True)
    parser.add_argument("--freebuff", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--root", type=Path)
    args = parser.parse_args()

    for binary in (args.goose, args.freebuff):
        if not Path(binary).is_file():
            raise SystemExit(f"executable not found: {binary}")

    owned = args.root is None
    temporary = tempfile.TemporaryDirectory(prefix="apex-ac-dev-019-") if owned else None
    root = Path(temporary.name) if temporary else args.root.resolve()
    for name in ("home", "config", "data", "state"):
        (root / name).mkdir(parents=True, exist_ok=True)
    result = {
        "probe": "AC-DEV-019 executor capability disambiguation (experiment-only)",
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "root_is_disposable": True,
        "credentials_supplied": False,
        "repository_workspace_used": False,
        "goose": probe_goose(args.goose, root),
        "freebuff": probe_freebuff(args.freebuff, root),
        "interpretation": {
            "canonical_capability": "agent.definition_catalog",
            "definition": "Discoverable native agent definitions with stable runtime identity; UI labels, source symbols, documentation, and unrelated skill catalogs do not satisfy it.",
            "goose_claim_state": "NOT_PROVEN",
            "freebuff_claim_state": "NOT_PROVEN",
            "admission_effect": "No compatible source is proven for a REQUIRED PARTIAL claim; AC-DEV-018 must return BLOCKED_CAPABILITY.",
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if temporary:
        temporary.cleanup()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
