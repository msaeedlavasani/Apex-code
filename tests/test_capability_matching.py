import unittest

from development_control import CapabilityMatchError, build_candidate_execution_plan


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


def passport_with(required=None, optional=None):
    return {
        "passport_id": "passport_test_v1",
        "development_task_id": "AC-DEV-TEST",
        "capability_requirements": {
            "required": required or [],
            "optional": optional or [],
        },
    }


class CapabilityMatchingTests(unittest.TestCase):
    def test_proven_required_capability_is_ranked_without_selection(self):
        plan = build_candidate_execution_plan(
            passport_with(required=[{"capability_id": "agent.test", "minimum_claim_state": "PROVEN"}]),
            registry_for(("alpha", "PROVEN"), ("beta", "PARTIAL")),
        )
        match = plan["required_capabilities"][0]
        self.assertEqual(plan["status"], "READY_FOR_FUTURE_ROUTING")
        self.assertEqual(match["match_status"], "MATCHED")
        self.assertEqual([item["source_id"] for item in match["compatible_candidates"]], ["alpha"])
        self.assertFalse(plan["dispatch_allowed"])
        self.assertIsNone(plan["selection"])

    def test_partial_required_capability_is_supported_when_passport_allows_partial(self):
        plan = build_candidate_execution_plan(
            passport_with(required=[{"capability_id": "agent.test", "minimum_claim_state": "PARTIAL"}]),
            registry_for(("alpha", "PARTIAL")),
        )
        self.assertEqual(plan["status"], "READY_FOR_FUTURE_ROUTING")
        self.assertEqual(plan["required_capabilities"][0]["match_status"], "MATCHED")
        self.assertEqual(plan["required_capabilities"][0]["compatible_candidates"][0]["claim_state"], "PARTIAL")

    def test_required_not_proven_fails_closed_and_preserves_observation(self):
        plan = build_candidate_execution_plan(
            passport_with(required=[{"capability_id": "agent.test", "minimum_claim_state": "PROVEN"}]),
            registry_for(("alpha", "NOT_PROVEN")),
        )
        match = plan["required_capabilities"][0]
        self.assertEqual(plan["status"], "BLOCKED_REQUIRED_CAPABILITY")
        self.assertEqual(plan["blocked_required_capabilities"], ["agent.test"])
        self.assertEqual(match["match_status"], "UNAVAILABLE")
        self.assertEqual(match["observed_mappings"][0]["claim_state"], "NOT_PROVEN")
        self.assertFalse(match["observed_mappings"][0]["compatible"])

    def test_optional_unsupported_capability_does_not_block_plan(self):
        plan = build_candidate_execution_plan(
            passport_with(optional=[{"capability_id": "agent.test", "minimum_claim_state": "PARTIAL"}]),
            registry_for(("alpha", "NOT_SUPPORTED")),
        )
        match = plan["optional_capabilities"][0]
        self.assertEqual(plan["status"], "READY_FOR_FUTURE_ROUTING")
        self.assertEqual(match["match_status"], "UNAVAILABLE")
        self.assertEqual(match["observed_mappings"][0]["claim_state"], "NOT_SUPPORTED")

    def test_equal_best_sources_are_ambiguous_but_deterministically_ranked(self):
        passport = passport_with(required=[{"capability_id": "agent.test", "minimum_claim_state": "PARTIAL"}])
        registry = registry_for(("beta", "PARTIAL"), ("alpha", "PARTIAL"))
        first = build_candidate_execution_plan(passport, registry)
        second = build_candidate_execution_plan(passport, registry)
        match = first["required_capabilities"][0]
        self.assertEqual(first, second)
        self.assertEqual(first["status"], "BLOCKED_REQUIRED_CAPABILITY")
        self.assertEqual(match["match_status"], "AMBIGUOUS")
        self.assertEqual([item["source_id"] for item in match["compatible_candidates"]], ["alpha", "beta"])
        self.assertEqual(match["compatible_candidates"][0]["rank"], 1)

    def test_duplicate_requirements_fail_closed_as_invalid_input(self):
        with self.assertRaises(CapabilityMatchError):
            build_candidate_execution_plan(
                passport_with(
                    required=["agent.test"],
                    optional=[{"capability_id": "agent.test", "minimum_claim_state": "PARTIAL"}],
                ),
                registry_for(("alpha", "PROVEN")),
            )


if __name__ == "__main__":
    unittest.main()
