from __future__ import annotations

import os
import subprocess
import tempfile
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import json
from pathlib import Path
from unittest.mock import patch

from apex_code.application import ApexApplication
from apex_code.providers import ProviderConfigurationError, catalog_records, validate_selection
from apex_code.runtime import OpenCodeRuntimeAdapter
from apex_code.shell import ShellServer


class ProviderTests(unittest.TestCase):
    def test_catalog_and_selection_are_non_secret(self) -> None:
        records = catalog_records()
        self.assertEqual({record["provider_id"] for record in records}, {"openai", "anthropic", "openrouter"})
        serialized = repr(records)
        self.assertNotIn("credential_env", serialized)
        self.assertNotIn("secret", serialized.lower())
        self.assertEqual(validate_selection("openai", "gpt-4o-mini").model_reference, "openai/gpt-4o-mini")
        with self.assertRaises(ProviderConfigurationError):
            validate_selection("openai", "unsupported-model")

    def test_runtime_environment_injects_only_selected_provider(self) -> None:
        original = os.environ.get("OPENAI_API_KEY")
        os.environ["OPENAI_API_KEY"] = "ambient-value-must-not-pass"
        try:
            environment = OpenCodeRuntimeAdapter._safe_environment(
                "/tmp/apex-provider-test",
                {"permission": {"read": "deny"}},
                "anthropic",
                "selected-value",
            )
        finally:
            if original is None:
                os.environ.pop("OPENAI_API_KEY", None)
            else:
                os.environ["OPENAI_API_KEY"] = original
        self.assertNotIn("OPENAI_API_KEY", environment)
        self.assertEqual(environment["ANTHROPIC_API_KEY"], "selected-value")
        self.assertNotIn("APEX_INTERNAL_TOKEN", environment)

    def test_connection_probe_is_bounded_and_redacts_failure(self) -> None:
        adapter = OpenCodeRuntimeAdapter(provider_id="openai", model="gpt-4o-mini", credential="selected-value")
        observed: dict[str, object] = {}

        def fake_run(command, **kwargs):
            observed["command"] = command
            observed["env"] = kwargs["env"]
            return subprocess.CompletedProcess(command, 0, '{"part":{"type":"text","text":"VALID"}}\n', "")

        with patch("apex_code.runtime.subprocess.run", side_effect=fake_run):
            result = adapter.test_connection()
        self.assertEqual(result["status"], "VALID")
        self.assertIn("--model", observed["command"])
        self.assertEqual(observed["env"]["OPENAI_API_KEY"], "selected-value")
        self.assertNotIn("ANTHROPIC_API_KEY", observed["env"])

    def test_second_provider_mapping_is_adapter_local(self) -> None:
        adapter = OpenCodeRuntimeAdapter(provider_id="openrouter", model="openai/gpt-4o-mini", credential="selected-value")
        environment = adapter._safe_environment(
            "/tmp/apex-provider-test",
            {"permission": {"read": "deny"}},
            adapter.provider_id,
            adapter.credential,
        )
        self.assertEqual(adapter.model, "openrouter/openai/gpt-4o-mini")
        self.assertEqual(environment["OPENROUTER_API_KEY"], "selected-value")
        self.assertNotIn("OPENAI_API_KEY", environment)

    def test_provider_state_keeps_secret_out_of_application_projection(self) -> None:
        application = ApexApplication()
        try:
            state = application.configure_provider("openrouter", "openai/gpt-4o-mini", "selected-value")
            serialized = repr(state)
            self.assertEqual(state["credential_status"], "CONFIGURED")
            self.assertEqual(state["selection"]["provider_id"], "openrouter")
            self.assertNotIn("selected-value", serialized)
            self.assertNotIn("credential_env", serialized)
            self.assertEqual(application.clear_provider_runtime()["credential_status"], "NOT_CONFIGURED")
        finally:
            application.close()

    def test_provider_runtime_sync_requires_internal_token_and_redacts_secret(self) -> None:
        application = ApexApplication()
        server = ShellServer(("127.0.0.1", 0), application)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{server.server_address[1]}"
        payload = json.dumps({"provider_id": "openai", "model_id": "gpt-4o-mini", "credential": "selected-value"}).encode()
        try:
            request = Request(
                base + "/api/internal/provider-runtime",
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with patch.dict(os.environ, {"APEX_INTERNAL_TOKEN": "unit-token"}, clear=False):
                with self.assertRaises(HTTPError) as error:
                    urlopen(request)
                self.assertEqual(error.exception.code, 404)
                error.exception.close()
                request.add_header("X-Apex-Internal-Token", "unit-token")
                with urlopen(request) as response:
                    body = response.read().decode()
            self.assertNotIn("selected-value", body)
            self.assertIn('"CONFIGURED"', body)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)


if __name__ == "__main__":
    unittest.main()
