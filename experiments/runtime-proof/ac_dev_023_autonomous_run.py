#!/usr/bin/env python3
"""Run the canonical control-plane loop for AC-DEV-023 in disposable state."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from definition_projection_adapter_probe import run_probe

from development_control import ControlPlaneStore, DevelopmentControlPlane


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--backlog", required=True, type=Path)
    parser.add_argument("--passports", required=True, type=Path)
    parser.add_argument("--proof-output", required=True, type=Path)
    parser.add_argument("--run-output", required=True, type=Path)
    args = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="apex-ac-dev-023-run-") as disposable:
        root = Path(disposable)
        backlog_path = root / "backlog.json"
        passports_path = root / "passports"
        state_path = root / "state.json"
        shutil.copy2(args.backlog, backlog_path)
        shutil.copytree(args.passports, passports_path)
        store = ControlPlaneStore(backlog_path, passports_path, state_path)
        plane = DevelopmentControlPlane(store, executor_id="generic-executor")

        proof_holder: dict[str, object] = {}

        def bounded_executor(task: dict, passport: dict) -> dict:
            if task.get("task_id") != "AC-DEV-023" or passport.get("development_task_id") != "AC-DEV-023":
                return {
                    "status": "FAIL",
                    "failure_class": "TASK_FAILURE",
                    "signature": "UNAUTHORIZED_TASK_SCOPE",
                    "validation": "executor received a task outside AC-DEV-023 scope",
                }
            proof = run_probe()
            proof_holder["receipt"] = proof
            all_proven = all(value == "PROVEN" for value in proof["acceptance"].values())
            return {
                "status": "PASS" if all_proven else "FAIL",
                "evidence_status": "PROVEN" if all_proven else "NOT_PROVEN",
                "verification": "VERIFIED" if all_proven else "NOT_VERIFIED",
                "bounded_operational_proof": proof["receipt_id"],
                "runtime_dispatch": False,
                "permanent_executor_selected": False,
            }

        summary = plane.run(bounded_executor, concurrency=1)
        state = store.load_state()
        proof = proof_holder.get("receipt")
        if not isinstance(proof, dict):
            raise RuntimeError("AC-DEV-023 proof did not execute")
        args.proof_output.parent.mkdir(parents=True, exist_ok=True)
        args.proof_output.write_text(json.dumps(proof, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        task = next(item for item in store.load_backlog()["tasks"] if item.get("task_id") == "AC-DEV-023")
        task_attempts = [item for item in state.get("attempts", []) if item.get("task_id") == "AC-DEV-023"]
        task_batches = [item for item in state.get("batches", []) if "AC-DEV-023" in item.get("task_ids", [])]
        batches = []
        for batch in task_batches:
            batches.append(
                {
                    "batch_id": batch["batch_id"],
                    "task_ids": batch["task_ids"],
                    "concurrency": batch["concurrency"],
                    "outcome": batch.get("task_outcomes", {}).get("AC-DEV-023", {}).get("status"),
                    "integration_verification": batch.get("integration_verification"),
                    "attempt_ids": [item["attempt_id"] for item in task_attempts if item.get("batch_id") == batch["batch_id"]],
                }
            )
        run_receipt = {
            "schema_version": 1,
            "receipt_type": "NIGHTLY_AUTONOMOUS_RUN",
            "receipt_id": "receipt_ac_dev_023_autonomous_run_0032",
            "development_task_id": "AC-DEV-023",
            "run_id": summary.run_id,
            "started_at": summary.started_at,
            "ended_at": summary.ended_at,
            "executor": "generic-executor",
            "batches": batches,
            "tasks_completed": [
                {
                    "task_id": "AC-DEV-023",
                    "status": task.get("status"),
                    "verification_status": task.get("verification_status"),
                    "evidence_status": task.get("evidence_status"),
                }
            ],
            "owner_decision_queue": [],
            "incidents": state.get("incidents", []),
            "rework": [],
            "registry_and_admission": {
                "registry_revision": 2,
                "agent_definition_catalog": {
                    "goose_cli": "NOT_PROVEN",
                    "freebuff_cli": "NOT_PROVEN",
                    "apex_owned_projection": "PROVEN_FOR_ADAPTER_CONTRACT_ONLY",
                },
                "ac_dev_018_status": "BLOCKED_CAPABILITY",
                "dispatch_allowed": False,
                "permanent_executor_selected": False,
                "ecc_installed": False,
            },
            "proof_evidence_refs": ["docs/evidence/AC-DEV-023-ADAPTER-PROOF-0031.json"],
            "stop_reason": summary.stop_reason,
            "run_summary": summary.as_dict(),
        }
        args.run_output.parent.mkdir(parents=True, exist_ok=True)
        args.run_output.write_text(json.dumps(run_receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
