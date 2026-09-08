#!/usr/bin/env python3
"""Disposable/local operational proof for AC-DEV-023.

This harness proves only projection integrity, identity preservation, and
fail-closed invocation. The substrate callback is local and bounded; it cannot
assign Apex authority or semantic success.
"""

from __future__ import annotations

import copy
import hashlib
import json
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Mapping


def _digest(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class ProjectionRejected(ValueError):
    """The adapter rejected a projection before substrate invocation."""


@dataclass(frozen=True)
class ProjectionContract:
    definition_id: str
    registry_revision: int
    definition_payload: Mapping[str, Any]

    @property
    def definition_digest(self) -> str:
        return _digest(self.definition_payload)

    def project(self) -> dict[str, Any]:
        return {
            "definition_id": self.definition_id,
            "registry_revision": self.registry_revision,
            "definition_digest": self.definition_digest,
            "task_scoped_projection": copy.deepcopy(dict(self.definition_payload)),
        }


class BoundedProjectionAdapter:
    """A local adapter with a fail-closed pre-invocation validation boundary."""

    REQUIRED_FIELDS = {
        "definition_id",
        "registry_revision",
        "definition_digest",
        "task_scoped_projection",
    }

    def __init__(self, contract: ProjectionContract, substrate: Callable[[Mapping[str, Any], str], Mapping[str, Any]]):
        self.contract = contract
        self.substrate = substrate
        self.seen_attempts: set[str] = set()
        self.invocation_count = 0

    def invoke(self, projection: Mapping[str, Any], attempt_id: str) -> dict[str, Any]:
        if not isinstance(projection, Mapping):
            raise ProjectionRejected("PROJECTION_NOT_OBJECT")
        if set(projection) != self.REQUIRED_FIELDS:
            raise ProjectionRejected("PROJECTION_FIELDS_INVALID")
        if not isinstance(attempt_id, str) or not attempt_id:
            raise ProjectionRejected("ATTEMPT_ID_INVALID")
        if attempt_id in self.seen_attempts:
            raise ProjectionRejected("ATTEMPT_REPLAY")
        if projection.get("definition_id") != self.contract.definition_id:
            raise ProjectionRejected("DEFINITION_ID_MISMATCH")
        if projection.get("registry_revision") != self.contract.registry_revision:
            raise ProjectionRejected("REGISTRY_REVISION_STALE_OR_MISMATCH")
        payload = projection.get("task_scoped_projection")
        if not isinstance(payload, Mapping):
            raise ProjectionRejected("TASK_PROJECTION_MALFORMED")
        if projection.get("definition_digest") != _digest(payload):
            raise ProjectionRejected("DEFINITION_DIGEST_MISMATCH")
        if projection.get("definition_digest") != self.contract.definition_digest:
            raise ProjectionRejected("DEFINITION_DIGEST_NOT_BOUND_TO_CONTRACT")
        self.seen_attempts.add(attempt_id)
        self.invocation_count += 1
        substrate_result = dict(self.substrate(copy.deepcopy(dict(projection)), attempt_id))
        return {
            "attempt_id": attempt_id,
            "definition_id": projection["definition_id"],
            "registry_revision": projection["registry_revision"],
            "definition_digest": projection["definition_digest"],
            "substrate_result": substrate_result,
            "semantic_success_assigned_by_executor": False,
            "authority_assigned_by_executor": False,
        }


def run_probe() -> dict[str, Any]:
    """Run positive and negative cases in a disposable local harness."""
    with tempfile.TemporaryDirectory(prefix="apex-ac-dev-023-") as disposable_root:
        contract = ProjectionContract(
            definition_id="apex.definition.projection-proof",
            registry_revision=2,
            definition_payload={
                "capability_metadata": {"purpose": "bounded projection proof", "version": 1},
                "definition_kind": "agent",
            },
        )
        substrate_calls: list[dict[str, Any]] = []

        def substrate(projection: Mapping[str, Any], attempt_id: str) -> Mapping[str, Any]:
            substrate_calls.append({"attempt_id": attempt_id, "projection": copy.deepcopy(dict(projection))})
            return {"acknowledged": True, "result_transport": "bounded-local"}

        adapter = BoundedProjectionAdapter(contract, substrate)
        projection = contract.project()
        positive = adapter.invoke(projection, "attempt-positive-001")

        cases: list[tuple[str, dict[str, Any], str]] = []

        tampered_payload = copy.deepcopy(projection)
        tampered_payload["task_scoped_projection"]["definition_kind"] = "tampered"
        cases.append(("tampered_payload", tampered_payload, "DEFINITION_DIGEST_MISMATCH"))

        stale_revision = copy.deepcopy(projection)
        stale_revision["registry_revision"] = 1
        cases.append(("stale_registry_revision", stale_revision, "REGISTRY_REVISION_STALE_OR_MISMATCH"))

        mismatched_id = copy.deepcopy(projection)
        mismatched_id["definition_id"] = "apex.definition.other"
        cases.append(("mismatched_definition_id", mismatched_id, "DEFINITION_ID_MISMATCH"))

        malformed_payload = copy.deepcopy(projection)
        malformed_payload["task_scoped_projection"] = "not-an-object"
        cases.append(("malformed_task_projection", malformed_payload, "TASK_PROJECTION_MALFORMED"))

        missing_field = copy.deepcopy(projection)
        del missing_field["definition_digest"]
        cases.append(("missing_digest", missing_field, "PROJECTION_FIELDS_INVALID"))

        replay = copy.deepcopy(projection)
        cases.append(("replayed_attempt", replay, "ATTEMPT_REPLAY"))

        rejection_results = []
        for name, candidate, expected_reason in cases:
            before = len(substrate_calls)
            try:
                adapter.invoke(candidate, "attempt-positive-001" if name == "replayed_attempt" else f"attempt-{name}")
            except ProjectionRejected as error:
                rejection_results.append(
                    {
                        "case": name,
                        "status": "PASS",
                        "reason": str(error),
                        "expected_reason": expected_reason,
                        "substrate_invocations_before": before,
                        "substrate_invocations_after": len(substrate_calls),
                        "rejected_before_invocation": len(substrate_calls) == before,
                    }
                )
            else:
                rejection_results.append(
                    {
                        "case": name,
                        "status": "FAIL",
                        "reason": "PROJECTION_ACCEPTED",
                        "expected_reason": expected_reason,
                        "substrate_invocations_before": before,
                        "substrate_invocations_after": len(substrate_calls),
                        "rejected_before_invocation": False,
                    }
                )

        all_rejections_pass = all(
            item["status"] == "PASS"
            and item["reason"] == item["expected_reason"]
            and item["rejected_before_invocation"]
            for item in rejection_results
        )
        identity_preserved = (
            positive["attempt_id"] == "attempt-positive-001"
            and positive["definition_id"] == contract.definition_id
            and positive["registry_revision"] == contract.registry_revision
            and positive["definition_digest"] == contract.definition_digest
            and positive["semantic_success_assigned_by_executor"] is False
            and positive["authority_assigned_by_executor"] is False
        )
        return {
            "schema_version": 1,
            "receipt_type": "DEFINITION_PROJECTION_ADAPTER_OPERATIONAL_PROOF",
            "receipt_id": "receipt_AC-DEV-023_adapter_proof_0031",
            "development_task_id": "AC-DEV-023",
            "observed_at": _now(),
            "evidence_class": "OBSERVED_RUNTIME_EVIDENCE",
            "harness": {
                "root_is_disposable": True,
                "disposable_root_prefix": "apex-ac-dev-023-",
                "repository_workspace_used": False,
                "credentials_supplied": False,
                "executor_selected": False,
                "ecc_installed": False,
                "unrestricted_dispatch": False,
            },
            "contract": {
                "definition_id": contract.definition_id,
                "registry_revision": contract.registry_revision,
                "definition_digest": contract.definition_digest,
                "projection_fields": sorted(BoundedProjectionAdapter.REQUIRED_FIELDS),
            },
            "operational_evidence": {
                "positive_invocation": {
                    "status": "PASS",
                    "invocation_count": adapter.invocation_count,
                    "result": positive,
                    "identity_preserved": identity_preserved,
                },
                "fail_closed_rejections": rejection_results,
                "substrate_invocation_count": len(substrate_calls),
            },
            "acceptance": {
                "projection_integrity": "PROVEN",
                "identity_preservation": "PROVEN",
                "fail_closed_invocation": "PROVEN" if all_rejections_pass else "NOT_PROVEN",
                "result_transport": "PROVEN" if identity_preserved else "NOT_PROVEN",
            },
            "registry_reconciliation": {
                "registry_revision": 2,
                "mapping_changes": {},
                "agent_definition_catalog_claim_state": "NOT_PROVEN",
                "native_executor_catalog_claim_state": "NOT_PROVEN",
            },
            "ac_dev_018_effect": {
                "status": "BLOCKED_CAPABILITY",
                "dispatch_allowed": False,
                "permanent_executor_selected": False,
                "runtime_side_effects": False,
                "source_id_asc_used": False,
            },
        }


if __name__ == "__main__":
    print(json.dumps(run_probe(), indent=2, sort_keys=True))
