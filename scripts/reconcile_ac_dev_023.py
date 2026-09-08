#!/usr/bin/env python3
"""Reconcile AC-DEV-017 matching and AC-DEV-018 admission after AC-DEV-023."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from development_control import build_candidate_execution_plan, build_execution_admission_decision


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", required=True, type=Path)
    parser.add_argument("--passport", required=True, type=Path)
    parser.add_argument("--proof-receipt", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    passport = json.loads(args.passport.read_text(encoding="utf-8"))
    first_plan = build_candidate_execution_plan(passport, registry)
    second_plan = build_candidate_execution_plan(passport, registry)
    first_decision = build_execution_admission_decision(passport, first_plan)
    second_decision = build_execution_admission_decision(passport, second_plan)
    required_match = first_plan["required_capabilities"][0]
    policy = first_decision["policy"]
    receipt = {
        "schema_version": 1,
        "receipt_type": "CAPABILITY_MATCHING_AND_ADMISSION_RECONCILIATION",
        "receipt_id": "receipt_AC-DEV-023_reconciliation_0033",
        "development_task_id": "AC-DEV-023",
        "observed_at": now(),
        "evidence_refs": [args.proof_receipt],
        "registry": {
            "registry_id": registry["registry_id"],
            "revision": registry["revision"],
            "capability_id": "agent.definition_catalog",
            "mapping_changes": {},
            "unchanged_controls": {
                "agent_definition_catalog_claims": {
                    "goose-cli": "NOT_PROVEN",
                    "freebuff-cli": "NOT_PROVEN",
                    "ecc": "NOT_PROVEN",
                    "future-system": "UNKNOWN",
                },
                "ecc_installed": registry.get("ecc_installed"),
                "permanent_executor_selected": registry.get("permanent_executor_selected"),
            },
        },
        "ac_dev_017_matching": {
            "passport_id": passport["passport_id"],
            "plan_status": first_plan["status"],
            "required_match_status": required_match["match_status"],
            "observed_mappings": required_match["observed_mappings"],
            "plan_input_digest": first_plan["input_digest"],
            "repeated_output_equal": first_plan == second_plan,
            "dispatch_allowed": first_plan["dispatch_allowed"],
            "permanent_executor_selected": first_plan["permanent_executor_selected"],
        },
        "ac_dev_018_admission": {
            "passport_id": passport["passport_id"],
            "status": first_decision["status"],
            "blocked_reasons": first_decision["blocked_reasons"],
            "selection": first_decision["selection"],
            "selection_rationale": first_decision["selection_rationale"],
            "policy": {
                "allow_deterministic_tie_break": policy["allow_deterministic_tie_break"],
                "tie_break_strategy": policy["tie_break_strategy"],
                "source_id_asc_used": False,
            },
            "decision_input_digest": first_decision["input_digest"],
            "repeated_output_equal": first_decision == second_decision,
            "runtime_side_effects": first_decision["runtime_side_effects"],
            "dispatch_allowed": first_decision["dispatch_allowed"],
            "permanent_executor_selected": first_decision["permanent_executor_selected"],
        },
        "result": {
            "adapter_contract_proven": True,
            "native_agent_definition_catalog_proven": False,
            "admission_reconciled": False,
            "admission_reason": "REQUIRED_NATIVE_CAPABILITY_REMAINS_UNAVAILABLE",
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
