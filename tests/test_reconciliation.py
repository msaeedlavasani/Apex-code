from __future__ import annotations

import tempfile
import unittest
import json
from dataclasses import asdict
from pathlib import Path

from apex_code.core import (
    AuthorityRevision,
    DuplicateStart,
    Execution,
    ExecutionLedger,
    ExecutionManifest,
    IdentityMismatch,
    PermissionEnvelope,
    ResourceConflict,
    RuntimeLane,
    Task,
    sha256_file,
)
from apex_code.reconciliation import ReconciliationLoop, RuntimeObservation
from apex_code.contract import RuntimeIdentity
from apex_code.core import RuntimeFact


def seed_attempt(root: Path, attempt_id: str = "attempt-a", session_id: str | None = "session-x", status: str = "RUNNING") -> ExecutionLedger:
    ledger = ExecutionLedger(root / "execution-ledger.json")
    request_id = "request-a"
    execution = Execution("execution-a", request_id)
    task = Task("task-a", execution.execution_id, "test task")
    authority = AuthorityRevision(
        "authority-a",
        PermissionEnvelope(("README.md",), ("REPORT.md",), ("../**",)),
        "now",
    )
    lane = RuntimeLane("lane-a", attempt_id, str(root), "now")
    manifest = ExecutionManifest("manifest-a", attempt_id, task.task_id, authority.authority_revision_id, "agent", "model", "req", "snap", "now")
    ledger.put("executions", execution.execution_id, asdict(execution))
    ledger.put("tasks", task.task_id, asdict(task))
    ledger.put("authorities", authority.authority_revision_id, asdict(authority))
    ledger.put("lanes", lane.runtime_lane_id, asdict(lane))
    ledger.put("manifests", manifest.manifest_id, asdict(manifest))
    ledger.put(
        "attempts",
        attempt_id,
        {
            "attempt_id": attempt_id,
            "task_id": task.task_id,
            "execution_epoch_id": "epoch-a",
            "status": status,
            "barrier": "RELEASED",
            "manifest_id": manifest.manifest_id,
            "authority_revision_id": authority.authority_revision_id,
            "runtime_lane_id": lane.runtime_lane_id,
            "runtime_session_id": session_id,
        },
    )
    ledger.claim_attempt_start(attempt_id, manifest.manifest_id, lane.runtime_lane_id)
    return ledger


class ReconciliationTests(unittest.TestCase):
    def test_fence_survives_reload_and_rejects_duplicate_start(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            path = Path(root)
            ledger = seed_attempt(path, status="CREATED")
            reloaded = ExecutionLedger(path / "execution-ledger.json")
            self.assertIn("attempt-a", reloaded.snapshot()["fences"])
            with self.assertRaises(DuplicateStart):
                reloaded.claim_attempt_start("attempt-a", "manifest-a", "lane-a")

    def test_identity_mismatch_fails_closed_without_reassociation(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            path = Path(root)
            seed_attempt(path)
            outcome = ReconciliationLoop(path / "execution-ledger.json").reconcile(
                [RuntimeObservation(RuntimeFact.RUNNING, "attempt-a", "session-y")]
            )[0]
            self.assertEqual(outcome.runtime_fact, RuntimeFact.MISMATCH)
            self.assertEqual(outcome.semantic_state, "RECOVERY_REQUIRED")
            data = ExecutionLedger(path / "execution-ledger.json").snapshot()
            self.assertEqual(data["attempts"]["attempt-a"]["runtime_session_id"], "session-x")

    def test_native_runtime_identity_mismatch_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            path = Path(root)
            ledger = seed_attempt(path)
            ledger.put(
                "attempts",
                "attempt-a",
                {**ledger.snapshot()["attempts"]["attempt-a"], "runtime_identity": {"session_id": "session-x", "process_id": 7, "adapter_instance_id": "adapter-a"}},
            )
            outcome = ReconciliationLoop(path / "execution-ledger.json").reconcile(
                [RuntimeObservation(RuntimeFact.RUNNING, "attempt-a", "session-x", identity=RuntimeIdentity("session-x", 8, "adapter-a"))]
            )[0]
            self.assertEqual((outcome.runtime_fact, outcome.semantic_state), (RuntimeFact.MISMATCH, "RECOVERY_REQUIRED"))

    def test_missing_and_unreachable_remain_recovery_states(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            path = Path(root)
            seed_attempt(path)
            loop = ReconciliationLoop(path / "execution-ledger.json")
            missing = loop.reconcile([RuntimeObservation(RuntimeFact.MISSING, "attempt-a", "session-x")])[0]
            self.assertEqual((missing.runtime_fact, missing.semantic_state), (RuntimeFact.MISSING, "LOST"))
            unreachable = loop.reconcile([RuntimeObservation(RuntimeFact.UNREACHABLE, "attempt-a", "session-x")])[0]
            self.assertEqual((unreachable.runtime_fact, unreachable.semantic_state), (RuntimeFact.UNREACHABLE, "RECOVERY_REQUIRED"))

    def test_completed_runtime_requires_verified_artifact_after_restart(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            path = Path(root)
            seed_attempt(path)
            (path / "REPORT.md").write_text("verified\n", encoding="utf-8")
            loop = ReconciliationLoop(path / "execution-ledger.json")
            unverified = loop.reconcile([RuntimeObservation(RuntimeFact.EXITED, "attempt-a", "session-x")])[0]
            self.assertEqual(unverified.semantic_state, "VERIFYING")
            ledger = ExecutionLedger(path / "execution-ledger.json")
            ledger.put("results", "attempt-a", {"verification": "PASS", "semantic_success": True})
            ledger.put("artifacts", "REPORT.md", {"path": "REPORT.md", "sha256": sha256_file(path / "REPORT.md"), "attempt_id": "attempt-a"})
            verified = loop.reconcile([RuntimeObservation(RuntimeFact.EXITED, "attempt-a", "session-x", verified_artifact=True)])[0]
            self.assertEqual((verified.semantic_state, verified.disposition), ("SUCCEEDED", "VERIFIED_RESULT"))

    def test_orphan_is_quarantined_and_not_adopted(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            path = Path(root)
            seed_attempt(path)
            outcome = ReconciliationLoop(path / "execution-ledger.json").reconcile(
                [RuntimeObservation(RuntimeFact.RUNNING, "unknown-attempt", "session-orphan")]
            )[0]
            self.assertTrue(outcome.orphan)
            self.assertEqual(outcome.disposition, "ORPHAN_QUARANTINED")
            self.assertNotIn("unknown-attempt", ExecutionLedger(path / "execution-ledger.json").snapshot()["attempts"])

    def test_controller_restart_without_observation_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            path = Path(root)
            seed_attempt(path)
            first = ReconciliationLoop(path / "execution-ledger.json").reconcile([])[0]
            second = ReconciliationLoop(path / "execution-ledger.json").reconcile([])[0]
            self.assertEqual(first.runtime_fact, RuntimeFact.UNKNOWN)
            self.assertEqual(first.semantic_state, "RECOVERY_REQUIRED")
            self.assertEqual(second.disposition, "NO_OBSERVATION_FAIL_CLOSED")

    def test_exclusive_workspace_claim_conflict_and_stale_reclaim_denial(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            ledger = ExecutionLedger(Path(root) / "execution-ledger.json")
            first = ledger.claim_resource("attempt-a", "manifest-a", "workspace:/safe")
            self.assertTrue(first["exclusive"])
            reloaded = ExecutionLedger(Path(root) / "execution-ledger.json")
            with self.assertRaises(ResourceConflict):
                reloaded.claim_resource("attempt-b", "manifest-b", "workspace:/safe")
            self.assertEqual(reloaded.snapshot()["claims"][first["claim_id"]]["state"], "HELD")

    def test_corrupt_immutable_relation_is_not_repaired(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            path = Path(root)
            seed_attempt(path)
            ledger = ExecutionLedger(path / "execution-ledger.json")
            data = ledger.snapshot()
            data["manifests"]["manifest-a"]["attempt_id"] = "other-attempt"
            (path / "execution-ledger.json").write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(IdentityMismatch):
                ExecutionLedger(path / "execution-ledger.json").validate_attempt_identity("attempt-a")


if __name__ == "__main__":
    unittest.main()
