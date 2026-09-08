import copy
import json
import unittest
from pathlib import Path

from development_control import validate_receipt


ROOT = Path(__file__).resolve().parents[1]


def load_json(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class EvidenceReceiptValidationTests(unittest.TestCase):
    def setUp(self):
        self.registry = load_json("development_control/agent_skill_registry.json")

    def test_canonical_ac_dev_019_receipts_validate_without_mutation(self):
        for relative in (
            "docs/evidence/AC-DEV-019-OPERATIONAL-PROBE-0024.json",
            "docs/evidence/AC-DEV-019-RECONCILIATION-0024.json",
        ):
            receipt = load_json(relative)
            original = copy.deepcopy(receipt)
            report = validate_receipt(receipt, self.registry, repository_root=ROOT)
            self.assertTrue(report["valid"], report)
            self.assertFalse(report["mutated_input"])
            self.assertEqual(receipt, original)
            self.assertFalse(report["claim_promotion"])

    def test_secret_shaped_fields_fail_closed(self):
        receipt = load_json("docs/evidence/AC-DEV-019-OPERATIONAL-PROBE-0024.json")
        receipt["operational_evidence"]["goose"]["token"] = "redacted"
        report = validate_receipt(receipt, self.registry)
        self.assertFalse(report["valid"])
        self.assertIn("SECRET_KEY_FORBIDDEN", {error["code"] for error in report["errors"]})

    def test_invalid_claim_state_and_registry_mismatch_fail_closed(self):
        receipt = load_json("docs/evidence/AC-DEV-019-OPERATIONAL-PROBE-0024.json")
        receipt["operational_evidence"]["goose"]["claim_state"] = "PROVEN_BUT_TRUST_ME"
        report = validate_receipt(receipt, self.registry)
        codes = {error["code"] for error in report["errors"]}
        self.assertIn("CLAIM_STATE_INVALID", codes)
        self.assertIn("REGISTRY_CLAIM_MISMATCH", codes)

    def test_unauthorized_source_id_tie_break_is_rejected(self):
        receipt = load_json("docs/evidence/AC-DEV-019-RECONCILIATION-0024.json")
        receipt["ac_dev_018_admission"]["policy"]["source_id_asc_used"] = True
        report = validate_receipt(receipt, self.registry)
        self.assertFalse(report["valid"])
        self.assertIn("ADMISSION_TIE_BREAK_UNAUTHORIZED", {error["code"] for error in report["errors"]})

    def test_not_proven_promotion_requires_demonstrated_runtime_evidence(self):
        receipt = load_json("docs/evidence/AC-DEV-019-RECONCILIATION-0024.json")
        receipt["registry"]["mapping_changes"]["goose-cli"] = {"before": "NOT_PROVEN", "after": "PROVEN"}
        report = validate_receipt(receipt, self.registry)
        self.assertFalse(report["valid"])
        self.assertIn("UNSUPPORTED_CLAIM_PROMOTION", {error["code"] for error in report["errors"]})


if __name__ == "__main__":
    unittest.main()
