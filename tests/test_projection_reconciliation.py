import copy
import json
import unittest
from pathlib import Path

from development_control import build_candidate_execution_plan, build_execution_admission_decision


ROOT = Path(__file__).resolve().parents[1]


def load_json(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class ProjectionAwareCapabilityReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.registry = load_json("development_control/agent_skill_registry.json")
        self.passport = load_json("development_control/passports/AC-DEV-018.json")

    def test_native_catalog_not_proven_does_not_become_proven(self):
        catalog = next(item for item in self.registry["capabilities"] if item["capability_id"] == "agent.definition_catalog")
        claims = {item["source_id"]: item["claim_state"] for item in catalog["source_mappings"]}
        self.assertEqual(claims["goose-cli"], "NOT_PROVEN")
        self.assertEqual(claims["freebuff-cli"], "NOT_PROVEN")
        self.assertNotIn("agent.definition_catalog", {
            item["capability_id"] for item in self.passport["capability_requirements"]["required"]
        })

    def test_apex_projection_path_does_not_require_native_catalog(self):
        plan = build_candidate_execution_plan(self.passport, self.registry)
        decision = build_execution_admission_decision(self.passport, plan)
        self.assertEqual(plan["status"], "READY_FOR_FUTURE_ROUTING")
        self.assertEqual(decision["status"], "ADMITTED")
        self.assertEqual(decision["selection"]["source_id"], "apex-owned-projection")
        self.assertEqual(decision["selection"]["binding_scope"], "TASK_CANDIDATE_ONLY")
        self.assertFalse(decision["dispatch_allowed"])
        self.assertFalse(decision["permanent_executor_selected"])

    def test_missing_genuine_invocation_capability_blocks_admission(self):
        incomplete = copy.deepcopy(self.registry)
        incomplete["capabilities"] = [
            capability
            for capability in incomplete["capabilities"]
            if capability["capability_id"] != "execution.fail_closed_invocation"
        ]
        plan = build_candidate_execution_plan(self.passport, incomplete)
        decision = build_execution_admission_decision(self.passport, plan)
        self.assertEqual(plan["status"], "BLOCKED_REQUIRED_CAPABILITY")
        self.assertEqual(decision["status"], "BLOCKED_CAPABILITY")
        self.assertIn(
            "REQUIRED_CAPABILITY_UNAVAILABLE:execution.fail_closed_invocation",
            decision["blocked_reasons"],
        )
        self.assertFalse(decision["dispatch_allowed"])

    def test_identical_evidence_and_policy_are_deterministic(self):
        first_plan = build_candidate_execution_plan(self.passport, self.registry)
        second_plan = build_candidate_execution_plan(self.passport, self.registry)
        first_decision = build_execution_admission_decision(self.passport, first_plan)
        second_decision = build_execution_admission_decision(self.passport, second_plan)
        self.assertEqual(first_plan, second_plan)
        self.assertEqual(first_decision, second_decision)


if __name__ == "__main__":
    unittest.main()
