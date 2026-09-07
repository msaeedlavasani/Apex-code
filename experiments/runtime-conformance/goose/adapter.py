"""Experiment-only Goose RuntimeAdapter mapping.

This module is deliberately outside Apex production composition. It maps
Goose process/session observations to the existing substrate-neutral contract;
it does not assign Apex semantic state or supply authority attestation.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

from apex_code.contract import RuntimeExecution, RuntimeFact, RuntimeIdentity, RuntimePreparation


class GooseRuntimeAdapter:
    """Minimal provider-backed adapter for the bounded artifact fixture."""

    def __init__(self, executable: str, provider: str = "claude-code", model: str = "default") -> None:
        self.executable = executable
        self.provider = provider
        self.model = model

    def materialize_authority(self, authority_digest: str) -> RuntimePreparation:
        root = Path(tempfile.mkdtemp(prefix="apex-goose-adapter-"))
        (root / "config").mkdir()
        (root / "home").mkdir()
        (root / "state").mkdir()
        permission = {
            "user": {
                "always_allow": [],
                "ask_before": [],
                "never_allow": ["developer__shell", "developer__computer"],
            }
        }
        (root / "config" / "permission.yaml").write_text(
            "user:\n  always_allow: []\n  ask_before: []\n  never_allow:\n    - developer__shell\n    - developer__computer\n",
            encoding="utf-8",
        )
        (root / "authority-digest").write_text(authority_digest + "\n", encoding="utf-8")
        return RuntimePreparation(
            preparation_id=f"prep_{root.name}",
            authority_digest=authority_digest,
            config_dir=str(root),
            mode="CORE_MEDIATED_NO_RUNTIME_IO",
            substrate_activation_confirmed=False,
        )

    @staticmethod
    def _safe_environment(root: Path) -> dict[str, str]:
        keep = {"PATH", "LANG", "LC_ALL", "LC_CTYPE", "TERM", "TMPDIR"}
        env = {key: value for key, value in os.environ.items() if key in keep}
        env["HOME"] = str(root / "home")
        env["GOOSE_PATH_ROOT"] = str(root)
        return env

    @staticmethod
    def _session_id(output: str) -> str | None:
        for pattern in (r'"sessionID"\s*:\s*"([^"]+)"', r'"session_id"\s*:\s*"([^"]+)"'):
            match = re.search(pattern, output)
            if match:
                return match.group(1)
        return None

    @staticmethod
    def _event_count(output: str) -> int:
        return sum(1 for line in output.splitlines() if line.lstrip().startswith("{"))

    def execute(self, prompt: str, workspace: Path, preparation: RuntimePreparation) -> RuntimeExecution:
        root = Path(preparation.config_dir)
        command = (
            self.executable,
            "run",
            "--provider",
            self.provider,
            "--no-profile",
            "--no-session",
            "--output-format",
            "json",
            "--max-turns",
            "1",
            "-t",
            prompt,
        )
        try:
            process = subprocess.Popen(
                command,
                cwd=workspace,
                env=self._safe_environment(root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            stdout, _stderr = process.communicate(timeout=90)
        except (OSError, subprocess.TimeoutExpired):
            if "process" in locals() and process.poll() is None:
                process.kill()
                process.communicate()
            return RuntimeExecution(
                identity=RuntimeIdentity(),
                fact=RuntimeFact.UNREACHABLE,
                exit_code=124,
                text="",
                event_count=0,
                preparation_id=preparation.preparation_id,
                authority_config_digest=preparation.authority_digest,
                command=command[:-1] + ("<prompt>",),
            )

        return RuntimeExecution(
            identity=RuntimeIdentity(
                session_id=self._session_id(stdout),
                process_id=process.pid,
                adapter_instance_id="goose-1.49.0-experimental",
            ),
            fact=RuntimeFact.EXITED if process.returncode == 0 else RuntimeFact.UNKNOWN,
            exit_code=process.returncode,
            text=stdout,
            event_count=self._event_count(stdout),
            preparation_id=preparation.preparation_id,
            authority_config_digest=preparation.authority_digest,
            command=command[:-1] + ("<prompt>",),
        )
