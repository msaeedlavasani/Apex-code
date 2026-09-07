import json
import tempfile
import unittest
from pathlib import Path

from development_control import ControlPlaneStore, DevelopmentControlPlane, FailureClass, TaskStatus


def passport(task_id, dependencies=None, claims=None, human_gates=None):
    return {
        "schema_version": 1,
        "passport_id": f"passport_{task_id}_v1",
        "development_task_id": task_id,
        "revision": 1,
        "goal": f"Complete {task_id}",
        "scope": ["bounded implementation"],
        "out_of_scope": ["unrelated product work"],
        "dependencies": dependencies or [],
        "resource_claims": claims or [],
        "architecture_constraints": ["preserve Core ownership"],
        "acceptance_criteria": ["focused validation passes"],
        "validation": ["unit tests"],
        "risk": {"class": "LOW", "reversibility": "HIGH"},
        "executor_compatibility": {"executors": ["generic-executor", "*"]},
        "human_gates": human_gates or [],
        "evidence_refs": ["docs/evidence/DEVELOPMENT-CONTROL-PLANE-0015.md"],
    }


def task(task_id, *, status="BACKLOG", dependencies=None, claims=None, human_gates=None, priority="P1"):
    return {
        "task_id": task_id,
        "title": task_id,
        "status": status,
        "verification_status": "NOT_RUN",
        "evidence_status": "NOT_PROVEN",
        "priority": priority,
        "risk": "LOW",
        "decision_class": "ROUTINE",
        "autonomous_allowed": True,
        "executor_compatibility": {"executors": ["generic-executor", "*"]},
        "dependencies": dependencies or [],
        "resource_claims": claims or [],
        "human_gates": human_gates or [],
        "critical_path_weight": 1,
        "downstream_unlock_value": 1,
        "aging_days": 0,
    }


class DevelopmentControlPlaneTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        root = Path(self.tempdir.name)
        self.backlog_path = root / "backlog.json"
        self.passports_dir = root / "passports"
        self.state_path = root / "state.json"
        self.store = ControlPlaneStore(self.backlog_path, self.passports_dir, self.state_path)

    def tearDown(self):
        self.tempdir.cleanup()

    def make_plane(self, tasks):
        self.store.save_backlog({"schema_version": 1, "revision": 1, "tasks": tasks})
        for item in tasks:
            self.store.save_passport(item["task_id"], passport(item["task_id"], item.get("dependencies"), item.get("resource_claims"), item.get("human_gates")))
        return DevelopmentControlPlane(self.store)

    def test_readiness_requires_complete_passport_and_verified_dependency(self):
        prerequisite = task("AC-DEV-A", status="BACKLOG")
        dependent = task("AC-DEV-B", dependencies=["AC-DEV-A"])
        plane = self.make_plane([prerequisite, dependent])

        self.assertFalse(plane.readiness("AC-DEV-B")["eligible"])
        self.assertIn("DEPENDENCY_NOT_VERIFIED:AC-DEV-A", plane.readiness("AC-DEV-B")["reasons"])

        backlog = self.store.load_backlog()
        backlog["tasks"][0].update({"status": "DONE", "verification_status": "VERIFIED"})
        self.store.save_backlog(backlog)
        self.assertTrue(plane.readiness("AC-DEV-B")["eligible"])

    def test_batch_is_conflict_safe_and_eligibility_waits_for_next_batch(self):
        first = task("AC-DEV-A", claims=["workspace"])
        second = task("AC-DEV-B", claims=["workspace"])
        third = task("AC-DEV-C", claims=["other"])
        plane = self.make_plane([first, second, third])

        snapshot = plane.select_batch(concurrency=2)
        self.assertIsNotNone(snapshot)
        self.assertEqual(len(snapshot.task_ids), 2)
        self.assertEqual(set(snapshot.task_ids), {"AC-DEV-A", "AC-DEV-C"})
        persisted = self.store.load_state()["batches"][0]
        self.assertEqual(persisted["task_ids"], list(snapshot.task_ids))

        plane.complete_task("AC-DEV-A", snapshot.batch_id, {"evidence_status": "PROVEN"})
        plane.complete_task("AC-DEV-C", snapshot.batch_id, {"evidence_status": "PROVEN"})
        self.assertTrue(plane.verify_batch(snapshot.batch_id, "PASS")["closed"])

        next_snapshot = plane.select_batch(concurrency=2)
        self.assertIsNotNone(next_snapshot)
        self.assertEqual(next_snapshot.task_ids, ("AC-DEV-B",))

    def test_failure_isolated_from_batch_and_rework_gets_distinct_attempt(self):
        one = task("AC-DEV-A")
        two = task("AC-DEV-B")
        plane = self.make_plane([one, two])
        calls = {"AC-DEV-B": 0}

        def executor(item, _passport):
            if item["task_id"] == "AC-DEV-A":
                return {"status": "PASS", "evidence_status": "PROVEN"}
            calls[item["task_id"]] += 1
            if calls[item["task_id"]] == 1:
                return {"status": "FAIL", "failure_class": "TASK_FAILURE", "signature": "fixture"}
            return {"status": "PASS", "evidence_status": "PROVEN"}

        summary = plane.run(executor, concurrency=2)
        self.assertEqual(summary.batches, 2)
        self.assertEqual(summary.verified_tasks, 2)
        self.assertEqual(summary.executed_tasks, 3)
        self.assertEqual(summary.incidents, 1)
        self.assertEqual(summary.backlog_returns, 1)
        attempts = self.store.load_state()["attempts"]
        b_attempts = [attempt for attempt in attempts if attempt["task_id"] == "AC-DEV-B"]
        self.assertEqual(len(b_attempts), 2)
        self.assertNotEqual(b_attempts[0]["attempt_id"], b_attempts[1]["attempt_id"])
        self.assertEqual(self.store.load_backlog()["tasks"][1]["status"], TaskStatus.DONE.value)

    def test_systemic_failure_opens_circuit_breaker(self):
        plane = self.make_plane([task("AC-DEV-A"), task("AC-DEV-B")])

        def executor(_item, _passport):
            return {"status": "FAIL", "failure_class": "SYSTEM_FAILURE", "signature": "provider-down"}

        summary = plane.run(executor, concurrency=1)
        self.assertTrue(plane.systemic_circuit_breaker_open())
        self.assertEqual(summary.stop_reason, "SYSTEMIC_CIRCUIT_BREAKER")
        self.assertEqual(summary.batches, 1)
        self.assertEqual(len(self.store.load_state()["attempts"]), 1)

    def test_batch_does_not_close_with_unknown_or_dangling_member(self):
        plane = self.make_plane([task("AC-DEV-A")])
        snapshot = plane.select_batch()
        backlog = self.store.load_backlog()
        backlog["tasks"][0]["status"] = "UNKNOWN"
        self.store.save_backlog(backlog)
        result = plane.verify_batch(snapshot.batch_id, "PASS")
        self.assertFalse(result["closed"])
        self.assertIn("AC-DEV-A", result["unresolved"])

        backlog["tasks"] = []
        self.store.save_backlog(backlog)
        result = plane.verify_batch(snapshot.batch_id, "PASS")
        self.assertFalse(result["closed"])
        self.assertEqual(result["dangling"], ["AC-DEV-A"])

    def test_owner_gate_does_not_stop_unrelated_eligible_work(self):
        gated = task("AC-DEV-GATE", human_gates=["owner-review"])
        free = task("AC-DEV-FREE")
        plane = self.make_plane([gated, free])
        plane.queue_owner_decision("AC-DEV-GATE", "owner-review", ["evidence/ref.md"])
        snapshot = plane.select_batch()
        self.assertEqual(snapshot.task_ids, ("AC-DEV-FREE",))
        self.assertEqual([item["task_id"] for item in plane.open_human_gates()], ["AC-DEV-GATE"])

    def test_corrective_task_is_linked_to_incident(self):
        plane = self.make_plane([task("AC-DEV-A")])
        snapshot = plane.select_batch()
        result = plane.fail_task("AC-DEV-A", snapshot.batch_id, FailureClass.TASK_FAILURE, "lint", {"validation": "FAIL"})
        corrective = passport("AC-DEV-FIX", dependencies=["AC-DEV-A"])
        new_id = plane.generate_corrective_task(result["incident_id"], "AC-DEV-A", "Fix lint failure", corrective)
        backlog = self.store.load_backlog()
        self.assertIn(new_id, [item["task_id"] for item in backlog["tasks"]])
        incident = self.store.load_state()["incidents"][0]
        self.assertEqual(incident["corrective_task_ids"], [new_id])
        self.assertFalse(plane.readiness(new_id)["eligible"])

    def test_canonical_seed_preserves_not_proven_and_has_goose_probe(self):
        root = Path(__file__).resolve().parents[1]
        backlog = json.loads((root / "development_control/backlog.json").read_text())
        goose = next(item for item in backlog["tasks"] if item["task_id"] == "AC-DEV-007")
        self.assertEqual(goose["status"], "BACKLOG")
        self.assertEqual(goose["evidence_status"], "NOT_PROVEN")
        self.assertIn("goose", goose["title"].lower())

    def test_control_plane_rejects_secret_bearing_persistence_fields(self):
        with self.assertRaises(ValueError):
            self.store.save_state({"attempts": [{"token": "redacted-test-fixture"}]})


if __name__ == "__main__":
    unittest.main()
