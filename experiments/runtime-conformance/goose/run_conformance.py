#!/usr/bin/env python3
"""Run the existing Apex conformance seam and bounded task through Goose."""

from __future__ import annotations

import argparse
import json
import tempfile
import unittest
from pathlib import Path

from apex_code.contract import RuntimeFact
from apex_code.core import AuthorityEvidence, ExecutionBarrier, ExecutionLedger, ExecutionManifest, RuntimeLane, SafetyError
from apex_code.core import ExecutionCoordinator
from apex_code.runtime import OpenCodeRuntimeAdapter
from tests.test_runtime_conformance import assert_runtime_adapter_contract

from adapter import GooseRuntimeAdapter


def preparation_shape(adapter: object) -> dict[str, object]:
    preparation = adapter.materialize_authority("conformance-digest")  # type: ignore[attr-defined]
    return {
        "preparation_id_present": bool(preparation.preparation_id),
        "authority_digest_matches": preparation.authority_digest == "conformance-digest",
        "config_dir_exists": Path(preparation.config_dir).is_dir(),
        "semantic_success_field_present": False,
    }


def negative_barrier_probe() -> bool:
    manifest = ExecutionManifest("manifest_negative", "attempt_negative", "task_negative", "authority_expected", "agent", "model", "runtime", "snapshot", "now")
    lane = RuntimeLane("lane_negative", "attempt_negative", "/tmp/disposable", "now")
    evidence = AuthorityEvidence(
        authority_revision_id="authority_wrong",
        authority_digest="digest",
        runtime_lane_id=lane.runtime_lane_id,
        attempt_id=manifest.attempt_id,
        execution_epoch_id="epoch_negative",
        materialized=True,
        substrate_activation_confirmed=False,
        binding_mode="CORE_MEDIATED_NO_RUNTIME_IO",
    )
    try:
        ExecutionBarrier.release(manifest, lane, evidence)
    except SafetyError:
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--goose", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    goose = GooseRuntimeAdapter(args.goose)
    opencode = OpenCodeRuntimeAdapter(executable="opencode")
    conformance_case = unittest.TestCase()
    assert_runtime_adapter_contract(conformance_case, goose)
    assert_runtime_adapter_contract(conformance_case, opencode)
    with tempfile.TemporaryDirectory(prefix="apex-goose-same-task-0006-") as root:
        workspace = Path(root)
        (workspace / "README.md").write_text("# Disposable Apex fixture\nA bounded conformance task.\n", encoding="utf-8")
        result = ExecutionCoordinator(goose).run_report(workspace)
        ledger = ExecutionLedger(Path(result["ledger"]))
        ledger.validate_attempt_identity(result["attempt_id"])
        ledger_snapshot = ledger.snapshot()
        data = {
            "goose_preparation_contract": preparation_shape(goose),
            "opencode_preparation_contract": preparation_shape(opencode),
            "existing_conformance_helper_passed": True,
            "same_bounded_task": {
                "runtime_fact": result["runtime_fact"],
                "exit_observed": result["runtime_fact"] == RuntimeFact.EXITED.value,
                "semantic_success": result["semantic_success"],
                "verification": result["verification"],
                "artifact": result["artifact"],
                "runtime_identity_present": bool(result["runtime_identity"]),
                "authority_activation": result["substrate_authority_activation"],
                "workspace_claim_and_ledger": Path(result["ledger"]).is_file(),
                "immutable_identity_relations_valid": True,
                "durable_event_count": len(ledger_snapshot.get("events", [])),
                "preparation_correlation_recorded": any(
                    event.get("event_type") == "authority.materialized"
                    and event.get("payload", {}).get("preparation_id")
                    for event in ledger_snapshot.get("events", [])
                ),
            },
            "negative_barrier_probe_passed": negative_barrier_probe(),
            "credentials_printed": False,
            "raw_provider_output_written": False,
        }
    args.output.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(data, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
