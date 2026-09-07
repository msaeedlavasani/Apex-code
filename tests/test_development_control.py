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

    def test_run_preserves_each_successful_member_in_a_multi_task_batch(self):
        first = task("AC-DEV-A")
        second = task("AC-DEV-B")
        plane = self.make_plane([first, second])

        summary = plane.run(lambda _item, _passport: {"status": "PASS", "evidence_status": "PROVEN"}, concurrency=2)

        self.assertEqual(summary.verified_tasks, 2)
        statuses = {item["task_id"]: item["status"] for item in self.store.load_backlog()["tasks"]}
        self.assertEqual(statuses, {"AC-DEV-A": TaskStatus.DONE.value, "AC-DEV-B": TaskStatus.DONE.value})

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

    def test_owner_authorized_material_task_is_admissible_without_changing_risk_class(self):
        authorized = task("AC-DEV-A")
        authorized.update({"decision_class": "MATERIAL", "risk": "HIGH", "owner_authorized": True})
        plane = self.make_plane([authorized])

        readiness = plane.readiness("AC-DEV-A")
        self.assertTrue(readiness["eligible"])
        self.assertNotIn("NON_ROUTINE_DECISION_CLASS", readiness["reasons"])

    def test_material_task_without_owner_authorization_remains_ineligible(self):
        gated = task("AC-DEV-A")
        gated.update({"decision_class": "MATERIAL", "risk": "HIGH"})
        plane = self.make_plane([gated])

        readiness = plane.readiness("AC-DEV-A")
        self.assertFalse(readiness["eligible"])
        self.assertIn("NON_ROUTINE_DECISION_CLASS", readiness["reasons"])

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

    def test_canonical_seed_preserves_partial_goose_ui_probe_evidence(self):
        root = Path(__file__).resolve().parents[1]
        backlog = json.loads((root / "development_control/backlog.json").read_text())
        goose = next(item for item in backlog["tasks"] if item["task_id"] == "AC-DEV-007")
        self.assertEqual(goose["status"], "DONE")
        self.assertEqual(goose["verification_status"], "VERIFIED")
        self.assertEqual(goose["evidence_status"], "PARTIAL")
        self.assertIn("goose", goose["title"].lower())

    def test_canonical_seed_preserves_event_ordering_task_and_adds_cli_probe(self):
        root = Path(__file__).resolve().parents[1]
        backlog = json.loads((root / "development_control/backlog.json").read_text())
        event_ordering = next(item for item in backlog["tasks"] if item["task_id"] == "AC-DEV-010")
        cli_probe = next(item for item in backlog["tasks"] if item["task_id"] == "AC-DEV-011")
        self.assertEqual(event_ordering["title"], "Global event ordering beyond ledger-local ordering")
        self.assertEqual(event_ordering["status"], "DEFERRED")
        self.assertEqual(event_ordering["evidence_status"], "NOT_PROVEN")
        self.assertEqual(cli_probe["title"], "Goose CLI Parallel Delegation Capability Probe")
        self.assertEqual(cli_probe["status"], "DONE")

        freebuff_probe = next(item for item in backlog["tasks"] if item["task_id"] == "AC-DEV-012")
        self.assertEqual(freebuff_probe["title"], "Freebuff CLI Operational Parallel Delegation Probe")
        self.assertEqual(freebuff_probe["status"], "DONE")
        self.assertEqual(freebuff_probe["verification_status"], "VERIFIED")
        self.assertEqual(freebuff_probe["evidence_status"], "PARTIAL")

        comparison = next(item for item in backlog["tasks"] if item["task_id"] == "AC-DEV-013")
        self.assertEqual(comparison["title"], "Executor Capability Comparison — Goose CLI vs Freebuff CLI")
        self.assertEqual(comparison["status"], "DONE")
        self.assertEqual(comparison["verification_status"], "VERIFIED")
        self.assertEqual(comparison["evidence_status"], "PARTIAL")
        self.assertEqual(comparison["dependencies"], ["AC-DEV-011", "AC-DEV-012"])

        extension_audit = next(item for item in backlog["tasks"] if item["task_id"] == "AC-DEV-014")
        self.assertEqual(extension_audit["title"], "Freebuff Agent/Skill Extension Surface Audit")
        self.assertEqual(extension_audit["status"], "DONE")
        self.assertEqual(extension_audit["verification_status"], "VERIFIED")
        self.assertEqual(extension_audit["evidence_status"], "PARTIAL")
        self.assertEqual(extension_audit["dependencies"], ["AC-DEV-012", "AC-DEV-013"])

        registry_task = next(item for item in backlog["tasks"] if item["task_id"] == "AC-DEV-015")
        self.assertEqual(registry_task["title"], "Apex Agent/Skill Registry v1")
        self.assertEqual(registry_task["status"], "DONE")
        self.assertEqual(registry_task["verification_status"], "VERIFIED")
        self.assertEqual(registry_task["evidence_status"], "PARTIAL")
        self.assertEqual(registry_task["dependencies"], ["AC-DEV-011", "AC-DEV-012", "AC-DEV-013", "AC-DEV-014"])

    def test_agent_skill_registry_is_executor_neutral_and_preserves_claim_states(self):
        root = Path(__file__).resolve().parents[1]
        registry = json.loads((root / "development_control/agent_skill_registry.json").read_text())
        self.assertEqual(registry["registry_id"], "apex-agent-skill-registry-v1")
        self.assertTrue(registry["executor_neutral"])
        self.assertFalse(registry["permanent_executor_selected"])
        self.assertFalse(registry["ecc_installed"])
        source_ids = {source["source_id"] for source in registry["sources"]}
        self.assertEqual(source_ids, {"goose-cli", "freebuff-cli", "ecc", "future-system"})
        claim_states = set(registry["claim_states"])
        for capability in registry["capabilities"]:
            self.assertRegex(capability["capability_id"], r"^[a-z]+\.[a-z0-9_.]+$")
            for mapping in capability["source_mappings"]:
                self.assertIn(mapping["source_id"], source_ids)
                self.assertIn(mapping["claim_state"], claim_states)

    def test_canonical_owner_authorizations_are_task_specific(self):
        root = Path(__file__).resolve().parents[1]
        backlog = json.loads((root / "development_control/backlog.json").read_text())
        tasks = {item["task_id"]: item for item in backlog["tasks"]}
        for task_id in ("AC-DEV-002", "AC-DEV-003", "AC-DEV-009"):
            self.assertTrue(tasks[task_id]["owner_authorized"])
            self.assertTrue(tasks[task_id]["autonomous_allowed"])
            self.assertEqual(tasks[task_id]["decision_class"], "MATERIAL")
            self.assertEqual(tasks[task_id]["evidence_status"], "NOT_PROVEN")
        self.assertNotIn("owner_authorized", tasks["AC-DEV-010"])

    def test_control_plane_rejects_secret_bearing_persistence_fields(self):
        with self.assertRaises(ValueError):
            self.store.save_state({"attempts": [{"token": "redacted-test-fixture"}]})


if __name__ == "__main__":
    unittest.main()
