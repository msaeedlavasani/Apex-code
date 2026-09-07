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

    PROVIDER_ENV = {
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "openrouter": "OPENROUTER_API_KEY",
        "opencode": None,
    }

    def __init__(
        self,
        executable: str = "opencode",
        model: str = "opencode/big-pickle",
        provider_id: str | None = None,
        credential: str | None = None,
    ) -> None:
        self.executable = executable
        if provider_id is None:
            provider_id, _, model_id = model.partition("/")
            model_id = model_id or model
        else:
            model_id = model
        self.provider_id = provider_id
        self.model_id = model_id
        self.model = f"{provider_id}/{model_id}"
        self.credential = credential

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
        config["model"] = self.model
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
        config = self._permission_config()
        config["model"] = self.model
        env = self._safe_environment(config_dir, config, self.provider_id, self.credential)
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

    def test_connection(self) -> dict[str, str]:
        """Run a bounded provider probe without creating Apex execution state."""
        if not self.credential:
            return {"status": "NO_CREDENTIAL", "message": "Configure a credential before testing this provider."}
        root = Path(tempfile.mkdtemp(prefix="apex-provider-test-"))
        preparation = self.materialize_authority("provider-test")
        command = (
            self.executable,
            "run",
            "--pure",
            "--model",
            self.model,
            "--format",
            "json",
            "Return the word VALID and nothing else.",
        )
        try:
            completed = subprocess.run(
                command,
                cwd=root,
                env=self._safe_environment(preparation.config_dir, self._permission_config(), self.provider_id, self.credential),
                capture_output=True,
                text=True,
                check=False,
                timeout=30,
            )
        except subprocess.TimeoutExpired:
            return {"status": "PROVIDER_UNAVAILABLE", "message": "The provider test timed out."}
        except OSError:
            return {"status": "PROVIDER_UNAVAILABLE", "message": "The OpenCode runtime is unavailable."}
        if completed.returncode == 0:
            return {"status": "VALID", "message": "Provider configuration accepted."}
        detail = self._redacted_failure(completed.stderr, completed.stdout)
        return {"status": self._classify_failure(detail), "message": detail}

    @staticmethod
    def _redacted_failure(stderr: str, stdout: str) -> str:
        text = " ".join((stderr or "").split() + (stdout or "").split()).lower()
        if any(token in text for token in ("401", "403", "unauthorized", "invalid api", "authentication", "api key")):
            return "Provider rejected the credential."
        if "429" in text or "rate limit" in text:
            return "Provider rate limit reached."
        if any(token in text for token in ("timeout", "timed out", "econn", "network", "unreachable")):
            return "Provider network request failed."
        if "model" in text and any(token in text for token in ("not found", "unavailable", "invalid")):
            return "Selected model is unavailable."
        return "Provider test failed without a safe diagnostic."

    @staticmethod
    def _classify_failure(message: str) -> str:
        if "credential" in message.lower():
            return "INVALID_CREDENTIAL"
        if "rate limit" in message.lower():
            return "RATE_LIMITED"
        if "model" in message.lower():
            return "MODEL_UNAVAILABLE"
        if "network" in message.lower():
            return "NETWORK_ERROR"
        return "UNKNOWN"

    @staticmethod
    def _safe_environment(
        config_dir: str,
        config: dict[str, object],
        provider_id: str | None = None,
        credential: str | None = None,
    ) -> dict[str, str]:
        """Build a minimal child environment for Core-mediated execution.

        Ambient user variables, credentials, and repository-specific
        configuration are intentionally not inherited by the worker.
        """
        path_entries = [
            os.defpath,
            "/usr/local/bin",
            "/opt/homebrew/bin",
            "/usr/bin",
            "/bin",
            "/usr/sbin",
            "/sbin",
        ]
        path = os.pathsep.join(
            dict.fromkeys(
                item
                for entry in path_entries
                for item in entry.split(os.pathsep)
                if item
            )
        )
        environment = {
            "PATH": path,
            "HOME": config_dir,
            "TERM": "dumb",
            "NO_COLOR": "1",
            "OPENCODE_CONFIG_DIR": config_dir,
            "OPENCODE_CONFIG_CONTENT": json.dumps(config, sort_keys=True),
            "XDG_DATA_HOME": os.path.join(config_dir, "data"),
            "XDG_CACHE_HOME": os.path.join(config_dir, "cache"),
            "XDG_STATE_HOME": os.path.join(config_dir, "state"),
        }
        credential_env = OpenCodeRuntimeAdapter.PROVIDER_ENV.get(provider_id or "")
        if credential_env and credential:
            environment[credential_env] = credential
        return environment
