from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from apex_code.core import ExecutionCoordinator, SafetyError
from apex_code.contract import RuntimeExecution, RuntimeFact, RuntimeIdentity, RuntimePreparation


class FakeAdapter:
    model = "test-model"

    def materialize_authority(self, authority_digest: str) -> RuntimePreparation:
        return RuntimePreparation("prep_fake", authority_digest, tempfile.mkdtemp(prefix="apex-fake-authority-"), "CORE_MEDIATED_NO_RUNTIME_IO")

    def execute(
        self,
        prompt: str,
        workspace: Path,
        preparation: RuntimePreparation,
    ) -> RuntimeExecution:
        return RuntimeExecution(
            identity=RuntimeIdentity(session_id="ses_test"),
            fact=RuntimeFact.EXITED,
            exit_code=0,
            text="REPORT_CONTENT_BEGIN\n# Safe report\nGenerated from README.\nREPORT_CONTENT_END",
            event_count=1,
            authority_config_digest=preparation.authority_digest,
            preparation_id=preparation.preparation_id,
            command=("fake", "<prompt>"),
        )


class CompletionOnlyAdapter(FakeAdapter):
    def execute(
        self,
        prompt: str,
        workspace: Path,
        preparation: RuntimePreparation,
    ) -> RuntimeExecution:
        return RuntimeExecution(
            identity=RuntimeIdentity(session_id="ses_completion_only"),
            fact=RuntimeFact.EXITED,
            exit_code=0,
            text="The process completed, but no verified artifact was returned.",
            event_count=1,
            authority_config_digest=preparation.authority_digest,
            preparation_id=preparation.preparation_id,
            command=("fake", "<prompt>"),
        )


class MismatchedPreparationAdapter(FakeAdapter):
    def execute(
        self,
        prompt: str,
        workspace: Path,
        preparation: RuntimePreparation,
    ) -> RuntimeExecution:
        return RuntimeExecution(
            identity=RuntimeIdentity(session_id="ses_mismatch"),
            fact=RuntimeFact.EXITED,
            exit_code=0,
            text="REPORT_CONTENT_BEGIN\n# Unsafe correlation\nREPORT_CONTENT_END",
            event_count=1,
            authority_config_digest=preparation.authority_digest,
            preparation_id="prep_not_the_one_materialized",
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

    def test_runtime_preparation_mismatch_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            workspace = Path(root)
            (workspace / "README.md").write_text("# Example\n", encoding="utf-8")
            with self.assertRaisesRegex(SafetyError, "preparation identity mismatch"):
                ExecutionCoordinator(MismatchedPreparationAdapter()).run_report(workspace)  # type: ignore[arg-type]
            self.assertFalse((workspace / "REPORT.md").exists())


if __name__ == "__main__":
    unittest.main()
