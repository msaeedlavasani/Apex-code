from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from apex_code.core import ExecutionCoordinator
from apex_code.runtime import RuntimeExecution


class FakeAdapter:
    model = "test-model"

    def materialize_authority(self, authority_digest: str) -> tuple[str, str]:
        return tempfile.mkdtemp(prefix="apex-fake-authority-"), authority_digest

    def execute(
        self,
        prompt: str,
        authority_digest: str,
        workspace: Path,
        config_dir: str | None = None,
    ) -> RuntimeExecution:
        return RuntimeExecution(
            session_id="ses_test",
            fact="EXITED",
            exit_code=0,
            text="REPORT_CONTENT_BEGIN\n# Safe report\nGenerated from README.\nREPORT_CONTENT_END",
            event_count=1,
            authority_config_dir="/tmp/fake",
            authority_config_digest=authority_digest,
            command=("fake", "<prompt>"),
        )


class CompletionOnlyAdapter(FakeAdapter):
    def execute(
        self,
        prompt: str,
        authority_digest: str,
        workspace: Path,
        config_dir: str | None = None,
    ) -> RuntimeExecution:
        return RuntimeExecution(
            session_id="ses_completion_only",
            fact="EXITED",
            exit_code=0,
            text="The process completed, but no verified artifact was returned.",
            event_count=1,
            authority_config_dir="/tmp/fake",
            authority_config_digest=authority_digest,
            command=("fake", "<prompt>"),
        )


class VerticalSliceTests(unittest.TestCase):
    def test_core_verifies_before_marking_success(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            workspace = Path(root)
            (workspace / "README.md").write_text("# Example\nA safe test repository.\n", encoding="utf-8")
            result = ExecutionCoordinator(FakeAdapter()).run_report(workspace)  # type: ignore[arg-type]
            self.assertTrue(result["semantic_success"])
            self.assertEqual(result["verification"], "PASS")
            self.assertEqual((workspace / "REPORT.md").read_text(encoding="utf-8"), "# Safe report\nGenerated from README.\n")
            ledger = (workspace / "execution-ledger.json").read_text(encoding="utf-8")
            self.assertIn('"semantic_success": true', ledger)
            self.assertIn('"event_type": "verification.completed"', ledger)

    def test_runtime_completion_alone_is_not_success(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            workspace = Path(root)
            (workspace / "README.md").write_text("# Example\n", encoding="utf-8")
            result = ExecutionCoordinator(CompletionOnlyAdapter()).run_report(workspace)  # type: ignore[arg-type]
            self.assertFalse(result["semantic_success"])
            self.assertEqual(result["verification"], "FAIL")
            self.assertFalse((workspace / "REPORT.md").exists())


if __name__ == "__main__":
    unittest.main()
