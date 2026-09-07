from __future__ import annotations

import tempfile
import unittest
import json
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
            identity=RuntimeIdentity(session_id="ses_test", process_id=101, adapter_instance_id="fake-v1"),
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


class SummaryAdapter(FakeAdapter):
    def execute(
        self,
        prompt: str,
        workspace: Path,
        preparation: RuntimePreparation,
    ) -> RuntimeExecution:
        return RuntimeExecution(
            identity=RuntimeIdentity(session_id="ses_summary"),
            fact=RuntimeFact.EXITED,
            exit_code=0,
            text="SUMMARY_CONTENT_BEGIN\n# Safe summary\nGenerated from README.\nSUMMARY_CONTENT_END",
            event_count=1,
            authority_config_digest=preparation.authority_digest,
            preparation_id=preparation.preparation_id,
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
            claims = json.loads(ledger)["claims"]
            self.assertEqual(len(claims), 1)
            self.assertEqual(next(iter(claims.values()))["state"], "RELEASED")
            attempt = next(iter(json.loads(ledger)["attempts"].values()))
            self.assertEqual(attempt["runtime_identity"], {"session_id": "ses_test", "process_id": 101, "adapter_instance_id": "fake-v1"})

    def test_runtime_completion_alone_is_not_success(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            workspace = Path(root)
            (workspace / "README.md").write_text("# Example\n", encoding="utf-8")
            result = ExecutionCoordinator(CompletionOnlyAdapter()).run_report(workspace)  # type: ignore[arg-type]
            self.assertFalse(result["semantic_success"])
            self.assertEqual(result["verification"], "FAIL")
            self.assertFalse((workspace / "REPORT.md").exists())
            claims = json.loads((workspace / "execution-ledger.json").read_text(encoding="utf-8"))["claims"]
            self.assertEqual(next(iter(claims.values()))["state"], "HELD")

    def test_runtime_preparation_mismatch_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            workspace = Path(root)
            (workspace / "README.md").write_text("# Example\n", encoding="utf-8")
            with self.assertRaisesRegex(SafetyError, "preparation identity mismatch"):
                ExecutionCoordinator(MismatchedPreparationAdapter()).run_report(workspace)  # type: ignore[arg-type]
            self.assertFalse((workspace / "REPORT.md").exists())

    def test_second_bounded_artifact_shape_uses_same_core_pipeline(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            workspace = Path(root)
            (workspace / "README.md").write_text("# Example\n", encoding="utf-8")
            result = ExecutionCoordinator(SummaryAdapter()).run_summary(workspace)  # type: ignore[arg-type]
            self.assertTrue(result["semantic_success"])
            self.assertEqual(result["artifact"], "SUMMARY.md")
            self.assertEqual((workspace / "SUMMARY.md").read_text(encoding="utf-8"), "# Safe summary\nGenerated from README.\n")
            self.assertFalse((workspace / "REPORT.md").exists())


if __name__ == "__main__":
    unittest.main()
