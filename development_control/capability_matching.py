"""Deterministic, non-dispatching capability matching for Task Passports."""

from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping


CLAIM_RANK = {
    "NOT_SUPPORTED": -1,
    "UNKNOWN": 0,
    "NOT_PROVEN": 0,
    "PARTIAL": 1,
    "PROVEN": 2,
}
MATCHABLE_MINIMUMS = {"PARTIAL", "PROVEN"}
SOURCE_STATUS_RANK = CLAIM_RANK


class CapabilityMatchError(ValueError):
    """Raised when a Passport or registry cannot be matched safely."""


def _canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _normalize_requirements(passport: Mapping[str, Any]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    raw = passport.get("capability_requirements", {})
    if raw is None:
        raw = {}
    if not isinstance(raw, Mapping):
        raise CapabilityMatchError("capability_requirements must be an object")

    normalized: dict[str, list[dict[str, str]]] = {}
    seen: set[str] = set()
    for bucket, default_minimum in (("required", "PROVEN"), ("optional", "PARTIAL")):
        values = raw.get(bucket, [])
        if not isinstance(values, list):
            raise CapabilityMatchError(f"capability_requirements.{bucket} must be a list")
        normalized[bucket] = []
        for item in values:
            if isinstance(item, str):
                capability_id = item
                minimum = default_minimum
            elif isinstance(item, Mapping):
                capability_id = item.get("capability_id")
                minimum = item.get("minimum_claim_state", default_minimum)
            else:
                raise CapabilityMatchError(f"{bucket} capability requirement must be an object or string")
            if not isinstance(capability_id, str) or not capability_id.strip():
                raise CapabilityMatchError(f"{bucket} capability_id must be a non-empty string")
            if minimum not in MATCHABLE_MINIMUMS:
                raise CapabilityMatchError(
                    f"{bucket} capability {capability_id} minimum_claim_state must be PARTIAL or PROVEN"
                )
            if capability_id in seen:
                raise CapabilityMatchError(f"capability requirement appears more than once: {capability_id}")
            seen.add(capability_id)
            normalized[bucket].append(
                {"capability_id": capability_id, "minimum_claim_state": str(minimum)}
            )
        normalized[bucket].sort(key=lambda requirement: (requirement["capability_id"], requirement["minimum_claim_state"]))
    return normalized["required"], normalized["optional"]


def _index_registry(registry: Mapping[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    sources = registry.get("sources", [])
    capabilities = registry.get("capabilities", [])
    if not isinstance(sources, list) or not isinstance(capabilities, list):
        raise CapabilityMatchError("registry sources and capabilities must be lists")

    source_index: dict[str, dict[str, Any]] = {}
    for source in sources:
        if not isinstance(source, Mapping) or not isinstance(source.get("source_id"), str):
            raise CapabilityMatchError("registry source is missing source_id")
        source_id = str(source["source_id"])
        if source_id in source_index:
            raise CapabilityMatchError(f"duplicate registry source: {source_id}")
        source_index[source_id] = dict(source)

    capability_index: dict[str, dict[str, Any]] = {}
    for capability in capabilities:
        if not isinstance(capability, Mapping) or not isinstance(capability.get("capability_id"), str):
            raise CapabilityMatchError("registry capability is missing capability_id")
        capability_id = str(capability["capability_id"])
        if capability_id in capability_index:
            raise CapabilityMatchError(f"duplicate registry capability: {capability_id}")
        mappings = capability.get("source_mappings", [])
        if not isinstance(mappings, list):
            raise CapabilityMatchError(f"source_mappings must be a list: {capability_id}")
        for mapping in mappings:
            if not isinstance(mapping, Mapping) or mapping.get("source_id") not in source_index:
                raise CapabilityMatchError(f"unknown source mapping for capability: {capability_id}")
            if mapping.get("claim_state") not in CLAIM_RANK:
                raise CapabilityMatchError(f"unknown claim state for capability: {capability_id}")
        capability_index[capability_id] = dict(capability)
    return capability_index, source_index


def _candidate(mapping: Mapping[str, Any], source: Mapping[str, Any], minimum: str) -> dict[str, Any]:
    claim_state = str(mapping["claim_state"])
    claim_rank = CLAIM_RANK[claim_state]
    minimum_rank = CLAIM_RANK[minimum]
    compatible = claim_rank >= minimum_rank and claim_state in {"PARTIAL", "PROVEN"}
    if compatible:
        reason = "CLAIM_STATE_MEETS_MINIMUM"
    elif claim_state in {"NOT_SUPPORTED", "UNKNOWN", "NOT_PROVEN"}:
        reason = "CLAIM_STATE_NOT_PROVEN"
    else:
        reason = "CLAIM_STATE_BELOW_MINIMUM"
    result = {
        "source_id": mapping["source_id"],
        "display_name": source.get("display_name"),
        "source_type": source.get("source_type"),
        "source_status": source.get("status", "UNKNOWN"),
        "claim_state": claim_state,
        "claim_rank": claim_rank,
        "minimum_claim_state": minimum,
        "compatible": compatible,
        "reason": reason,
        "evidence_refs": list(source.get("evidence_refs", [])),
    }
    if "notes" in mapping:
        result["notes"] = mapping["notes"]
    return result


def _match_requirement(
    requirement: Mapping[str, str],
    capability_index: Mapping[str, Mapping[str, Any]],
    source_index: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    capability_id = requirement["capability_id"]
    minimum = requirement["minimum_claim_state"]
    capability = capability_index.get(capability_id)
    if capability is None:
        return {
            "capability_id": capability_id,
            "minimum_claim_state": minimum,
            "match_status": "UNAVAILABLE",
            "compatible_candidates": [],
            "observed_mappings": [],
        }

    observed = [
        _candidate(mapping, source_index[str(mapping["source_id"])], minimum)
        for mapping in sorted(capability.get("source_mappings", []), key=lambda item: str(item["source_id"]))
    ]
    compatible = [candidate for candidate in observed if candidate["compatible"]]
    compatible.sort(
        key=lambda candidate: (
            -candidate["claim_rank"],
            -SOURCE_STATUS_RANK.get(str(candidate["source_status"]), 0),
            str(candidate["source_id"]),
        )
    )
    for rank, candidate in enumerate(compatible, start=1):
        candidate["rank"] = rank
    best_key = None
    if compatible:
        best = compatible[0]
        best_key = (best["claim_rank"], SOURCE_STATUS_RANK.get(str(best["source_status"]), 0))
    top = [
        candidate
        for candidate in compatible
        if best_key is not None
        and (candidate["claim_rank"], SOURCE_STATUS_RANK.get(str(candidate["source_status"]), 0)) == best_key
    ]
    if not compatible:
        match_status = "UNAVAILABLE"
    elif len(top) > 1:
        match_status = "AMBIGUOUS"
    else:
        match_status = "MATCHED"
    return {
        "capability_id": capability_id,
        "minimum_claim_state": minimum,
        "match_status": match_status,
        "compatible_candidates": compatible,
        "observed_mappings": observed,
    }


def build_candidate_execution_plan(
    passport: Mapping[str, Any], registry: Mapping[str, Any]
) -> dict[str, Any]:
    """Build a deterministic candidate plan without dispatching or selecting a source."""
    required, optional = _normalize_requirements(passport)
    capability_index, source_index = _index_registry(registry)
    required_matches = [_match_requirement(item, capability_index, source_index) for item in required]
    optional_matches = [_match_requirement(item, capability_index, source_index) for item in optional]
    blocked_required = [
        item["capability_id"]
        for item in required_matches
        if item["match_status"] in {"UNAVAILABLE", "AMBIGUOUS"}
    ]
    status = "BLOCKED_REQUIRED_CAPABILITY" if blocked_required else "READY_FOR_FUTURE_ROUTING"
    return {
        "plan_schema_version": 1,
        "plan_type": "CANDIDATE_EXECUTION_PLAN",
        "input_digest": _canonical_digest({"passport": passport, "registry": registry}),
        "passport_id": passport.get("passport_id"),
        "development_task_id": passport.get("development_task_id"),
        "registry_id": registry.get("registry_id"),
        "registry_revision": registry.get("revision"),
        "status": status,
        "dispatch_allowed": False,
        "permanent_executor_selected": False,
        "selection": None,
        "required_capabilities": required_matches,
        "optional_capabilities": optional_matches,
        "blocked_required_capabilities": blocked_required,
        "ownership": {
            "task_semantics": "apex-control-plane",
            "scheduling": "apex-control-plane",
            "authority": "apex-core",
            "verification": "apex-core",
            "semantic_success": "apex-core",
        },
    }
