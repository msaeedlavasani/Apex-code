"""OpenCode Runtime Adapter for the bounded Core-mediated slice.

The adapter reports substrate facts and raw output. It does not assign Apex
semantic success, write repository artifacts, or decide authority.
"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path

from .contract import RuntimeExecution, RuntimeFact, RuntimeIdentity, RuntimePreparation


class OpenCodeRuntimeAdapter:
    """Run OpenCode as a text-producing worker with Core-mediated I/O.

    The worker receives the authorized README content in its prompt. Its
    OpenCode permission configuration denies filesystem/tool access so that
    REPORT.md is created only by Apex Core after verification.
    """

    def __init__(self, executable: str = "opencode", model: str = "opencode/big-pickle") -> None:
        self.executable = executable
        self.model = model

    @staticmethod
    def _permission_config() -> dict[str, object]:
        return {
            "$schema": "https://opencode.ai/config.json",
            "permission": {
                "read": "deny",
                "edit": "deny",
                "bash": "deny",
                "external_directory": "deny",
            },
        }

    def materialize_authority(self, authority_digest: str) -> RuntimePreparation:
        """Materialize a deny-all worker config in an isolated temp root."""
        root = Path(tempfile.mkdtemp(prefix="apex-opencode-slice-"))
        config_path = root / "opencode.json"
        config = self._permission_config()
        config_path.write_text(json.dumps(config, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        # The digest is carried in a separate file so Core can attest exactly
        # which authority revision the launch preparation referenced.
        (root / "authority-digest").write_text(authority_digest + "\n", encoding="utf-8")
        return RuntimePreparation(
            preparation_id=f"prep_{root.name}",
            authority_digest=authority_digest,
            config_dir=str(root),
            mode="CORE_MEDIATED_NO_RUNTIME_IO",
            substrate_activation_confirmed=False,
        )

    def execute(
        self,
        prompt: str,
        workspace: Path,
        preparation: RuntimePreparation,
    ) -> RuntimeExecution:
        config_dir = preparation.config_dir
        materialized_digest = preparation.authority_digest
        env = os.environ.copy()
        config = self._permission_config()
        env.update(
            {
                "OPENCODE_CONFIG_DIR": config_dir,
                "OPENCODE_CONFIG_CONTENT": json.dumps(config, sort_keys=True),
                "XDG_DATA_HOME": os.path.join(config_dir, "data"),
                "XDG_CACHE_HOME": os.path.join(config_dir, "cache"),
                "XDG_STATE_HOME": os.path.join(config_dir, "state"),
            }
        )
        command = (
            self.executable,
            "run",
            "--pure",
            "--model",
            self.model,
            "--format",
            "json",
            prompt,
        )
        try:
            completed = subprocess.run(
                command,
                cwd=workspace,
                env=env,
                capture_output=True,
                text=True,
                check=False,
                timeout=120,
            )
        except (OSError, subprocess.TimeoutExpired):
            return RuntimeExecution(
                identity=RuntimeIdentity(),
                fact=RuntimeFact.UNREACHABLE,
                exit_code=124,
                text="",
                event_count=0,
                authority_config_digest=materialized_digest,
                preparation_id=preparation.preparation_id,
                command=command[:-1] + ("<prompt>",),
            )

        text_parts: list[str] = []
        session_id: str | None = None
        event_count = 0
        for line in completed.stdout.splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            event_count += 1
            session_id = session_id or event.get("sessionID")
            part = event.get("part")
            if isinstance(part, dict) and part.get("type") == "text" and isinstance(part.get("text"), str):
                text_parts.append(part["text"])
        fact = RuntimeFact.EXITED if completed.returncode == 0 else RuntimeFact.UNKNOWN
        return RuntimeExecution(
            identity=RuntimeIdentity(session_id=session_id),
            fact=fact,
            exit_code=completed.returncode,
            text="".join(text_parts),
            event_count=event_count,
            authority_config_digest=materialized_digest,
            preparation_id=preparation.preparation_id,
            command=command[:-1] + ("<prompt>",),
        )
