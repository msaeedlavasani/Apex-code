import unittest

from development_control import (
    build_candidate_execution_plan,
    build_execution_admission_decision,
)


def registry_for(*mappings):
    source_ids = sorted({source_id for source_id, _claim_state in mappings})
    return {
        "schema_version": 1,
        "registry_id": "test-registry",
        "revision": 1,
        "sources": [
            {
                "source_id": source_id,
                "source_type": "EXECUTOR",
                "display_name": source_id.title(),
                "status": "PARTIAL",
                "evidence_refs": [f"evidence/{source_id}.md"],
            }
            for source_id in source_ids
        ],
        "capabilities": [
            {
                "capability_id": "agent.test",
                "kind": "agent",
                "title": "Test capability",
                "source_mappings": [
                    {"source_id": source_id, "claim_state": claim_state}
                    for source_id, claim_state in mappings
                ],
            }
        ],
    }


def passport_with(required=None, human_gates=None):
    return {
        "passport_id": "passport_test_v1",
        "development_task_id": "AC-DEV-TEST",
        "human_gates": human_gates or [],
        "capability_requirements": {
            "required": required or [{"capability_id": "agent.test", "minimum_claim_state": "PARTIAL"}],
            "optional": [],
        },
    }


def plan_for(passport, *mappings):
    return build_candidate_execution_plan(passport, registry_for(*mappings))


class ExecutionAdmissionTests(unittest.TestCase):
    def test_unique_compatible_source_is_admitted_without_dispatch(self):
        passport = passport_with()
        decision = build_execution_admission_decision(
            passport,
            plan_for(passport, ("goose-cli", "PROVEN"), ("freebuff-cli", "PARTIAL")),
        )
        self.assertEqual(decision["status"], "ADMITTED")
        self.assertTrue(decision["admitted"])
        self.assertEqual(decision["selection"]["source_id"], "goose-cli")
        self.assertFalse(decision["dispatch_allowed"])
        self.assertFalse(decision["permanent_executor_selected"])
        self.assertEqual(decision["selection"]["required_capabilities"][0]["claim_state"], "PROVEN")
        self.assertEqual(decision["rejected_candidates"][0]["source_id"], "freebuff-cli")
        self.assertIn("NOT_SELECTED", decision["rejected_candidates"][0]["rejection_reasons"])

    def test_blocked_candidate_plan_fails_as_capability_block(self):
        passport = passport_with(required=[{"capability_id": "agent.test", "minimum_claim_state": "PROVEN"}])
        plan = plan_for(passport, ("goose-cli", "NOT_PROVEN"))
        decision = build_execution_admission_decision(passport, plan)
        self.assertEqual(decision["status"], "BLOCKED_CAPABILITY")
        self.assertIn("REQUIRED_CAPABILITY_UNAVAILABLE:agent.test", decision["blocked_reasons"])
        self.assertEqual(decision["candidate_execution_plan"]["required_capabilities"][0]["observed_mappings"][0]["claim_state"], "NOT_PROVEN")

    def test_ambiguous_required_candidate_blocks_without_policy_tie_break(self):
        passport = passport_with()
        plan = plan_for(passport, ("alpha", "PARTIAL"), ("beta", "PARTIAL"))
        decision = build_execution_admission_decision(passport, plan)
        self.assertEqual(decision["status"], "BLOCKED_AMBIGUITY")
        self.assertIn("AMBIGUOUS_REQUIRED_CAPABILITY:agent.test", decision["blocked_reasons"])

    def test_policy_explicitly_permits_deterministic_tie_break(self):
        passport = passport_with()
        plan = plan_for(passport, ("beta", "PARTIAL"), ("alpha", "PARTIAL"))
        policy = {
            "policy_id": "test-policy",
            "revision": 1,
            "allow_deterministic_tie_break": True,
            "tie_break_strategy": "SOURCE_ID_ASC",
        }
        first = build_execution_admission_decision(passport, plan, policy)
        second = build_execution_admission_decision(passport, plan, policy)
        self.assertEqual(first, second)
        self.assertEqual(first["status"], "ADMITTED")
        self.assertEqual(first["selection"]["source_id"], "alpha")
        self.assertEqual(first["selection_rationale"], "POLICY_PERMITTED_SOURCE_ID_ASC_TIE_BREAK")
        self.assertEqual(first["rejected_candidates"][0]["source_id"], "beta")

    def test_policy_denial_blocks_before_candidate_selection(self):
        passport = passport_with()
        decision = build_execution_admission_decision(
            passport,
            plan_for(passport, ("goose-cli", "PROVEN")),
            {"admission_allowed": False},
        )
        self.assertEqual(decision["status"], "BLOCKED_POLICY")
        self.assertEqual(decision["blocked_reasons"], ["ADMISSION_POLICY_DENIED"])
        self.assertIsNone(decision["selection"])

    def test_human_gate_blocks_before_policy_and_selection(self):
        passport = passport_with(human_gates=["OWNER_APPROVAL"])
        decision = build_execution_admission_decision(
            passport,
            plan_for(passport, ("goose-cli", "PROVEN")),
        )
        self.assertEqual(decision["status"], "HUMAN_GATE_REQUIRED")
        self.assertEqual(decision["human_gates"], ["OWNER_APPROVAL"])
        self.assertFalse(decision["admitted"])


if __name__ == "__main__":
    unittest.main()
