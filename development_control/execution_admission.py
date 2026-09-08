"""Deterministic, non-dispatching execution admission and candidate selection."""

from __future__ import annotations

import copy
import hashlib
import json
from typing import Any, Mapping


class ExecutionAdmissionError(ValueError):
    """Raised when an admission input is structurally unsafe to evaluate."""


ADMISSION_STATUSES = {
    "ADMITTED",
    "BLOCKED_CAPABILITY",
    "BLOCKED_AMBIGUITY",
    "BLOCKED_POLICY",
    "HUMAN_GATE_REQUIRED",
}
CLAIM_RANK = {
    "NOT_SUPPORTED": -1,
    "UNKNOWN": 0,
    "NOT_PROVEN": 0,
    "PARTIAL": 1,
    "PROVEN": 2,
}
SOURCE_STATUS_RANK = CLAIM_RANK
DEFAULT_POLICY = {
    "policy_id": "apex-execution-admission-v1",
    "revision": 1,
    "admission_allowed": True,
    "allow_deterministic_tie_break": False,
    "tie_break_strategy": None,
    "allowed_source_ids": [],
    "human_gate_required": False,
}


def _canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _copy_mapping(value: Mapping[str, Any]) -> dict[str, Any]:
    return copy.deepcopy(dict(value))


def _normalize_policy(policy: Mapping[str, Any] | None) -> dict[str, Any]:
    if policy is None:
        return copy.deepcopy(DEFAULT_POLICY)
    if not isinstance(policy, Mapping):
        raise ExecutionAdmissionError("admission policy must be an object")
    normalized = copy.deepcopy(DEFAULT_POLICY)
    normalized.update(_copy_mapping(policy))
    if not isinstance(normalized["admission_allowed"], bool):
        raise ExecutionAdmissionError("policy admission_allowed must be boolean")
    if not isinstance(normalized["allow_deterministic_tie_break"], bool):
        raise ExecutionAdmissionError("policy allow_deterministic_tie_break must be boolean")
    allowed = normalized.get("allowed_source_ids", [])
    if not isinstance(allowed, list) or any(not isinstance(item, str) or not item for item in allowed):
        raise ExecutionAdmissionError("policy allowed_source_ids must be a list of non-empty strings")
    normalized["allowed_source_ids"] = sorted(set(allowed))
    if normalized["allow_deterministic_tie_break"] and normalized.get("tie_break_strategy") != "SOURCE_ID_ASC":
        raise ExecutionAdmissionError(
            "explicit deterministic tie-breaking requires tie_break_strategy SOURCE_ID_ASC"
        )
    return normalized


def _validate_plan(candidate_plan: Mapping[str, Any]) -> None:
    if not isinstance(candidate_plan, Mapping):
        raise ExecutionAdmissionError("candidate execution plan must be an object")
    if candidate_plan.get("plan_type") != "CANDIDATE_EXECUTION_PLAN":
        raise ExecutionAdmissionError("unsupported candidate execution plan type")
    if candidate_plan.get("plan_schema_version") != 1:
        raise ExecutionAdmissionError("unsupported candidate execution plan schema")
    for bucket in ("required_capabilities", "optional_capabilities"):
        if not isinstance(candidate_plan.get(bucket), list):
            raise ExecutionAdmissionError(f"candidate plan {bucket} must be a list")
    if candidate_plan.get("permanent_executor_selected") is not False:
        raise ExecutionAdmissionError("candidate plan cannot permanently select an executor")


def _human_gates(passport: Mapping[str, Any], policy: Mapping[str, Any]) -> list[Any]:
    gates: list[Any] = []
    passport_gates = passport.get("human_gates", [])
    if passport_gates:
        gates.extend(copy.deepcopy(passport_gates if isinstance(passport_gates, list) else [passport_gates]))
    policy_gates = policy.get("human_gate_ids", [])
    if policy_gates:
        gates.extend(copy.deepcopy(policy_gates if isinstance(policy_gates, list) else [policy_gates]))
    if policy.get("human_gate_required") and not gates:
        gates.append("POLICY_HUMAN_GATE")
    return gates


def _candidate_evaluations(required_matches: list[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_source: dict[str, dict[str, dict[str, Any]]] = {}
    for match in required_matches:
        capability_id = str(match.get("capability_id"))
        for candidate in match.get("compatible_candidates", []):
            source_id = str(candidate.get("source_id"))
            by_source.setdefault(source_id, {})[capability_id] = copy.deepcopy(dict(candidate))

    evaluations: list[dict[str, Any]] = []
    required_ids = [str(match.get("capability_id")) for match in required_matches]
    for source_id in sorted(by_source):
        records = by_source[source_id]
        missing = [capability_id for capability_id in required_ids if capability_id not in records]
        complete = not missing and bool(required_ids)
        quality = None
        if complete:
            values = list(records.values())
            claim_ranks = [int(item["claim_rank"]) for item in values]
            source_status_ranks = [SOURCE_STATUS_RANK.get(str(item["source_status"]), 0) for item in values]
            quality = {
                "minimum_claim_rank": min(claim_ranks),
                "total_claim_rank": sum(claim_ranks),
                "minimum_source_status_rank": min(source_status_ranks),
                "total_source_status_rank": sum(source_status_ranks),
            }
        evaluations.append(
            {
                "source_id": source_id,
                "compatible_for_all_required": complete,
                "missing_required_capabilities": missing,
                "quality": quality,
                "required_capabilities": [records[key] for key in sorted(records)],
                "rejection_reasons": [],
            }
        )
    return evaluations


def _quality_key(evaluation: Mapping[str, Any]) -> tuple[int, int, int, int]:
    quality = evaluation["quality"]
    return (
        int(quality["minimum_claim_rank"]),
        int(quality["total_claim_rank"]),
        int(quality["minimum_source_status_rank"]),
        int(quality["total_source_status_rank"]),
    )


def _rejected(evaluation: Mapping[str, Any], reason: str) -> dict[str, Any]:
    result = copy.deepcopy(dict(evaluation))
    result["rejection_reasons"] = sorted(set(result.get("rejection_reasons", []) + [reason]))
    return result


def _base_decision(
    passport: Mapping[str, Any], candidate_plan: Mapping[str, Any], policy: Mapping[str, Any]
) -> dict[str, Any]:
    return {
        "decision_schema_version": 1,
        "decision_type": "EXECUTION_ADMISSION_DECISION",
        "input_digest": _canonical_digest(
            {"passport": passport, "candidate_execution_plan": candidate_plan, "policy": policy}
        ),
        "passport_id": passport.get("passport_id"),
        "development_task_id": passport.get("development_task_id"),
        "candidate_plan_digest": candidate_plan.get("input_digest"),
        "policy": copy.deepcopy(dict(policy)),
        "status": None,
        "admitted": False,
        "runtime_side_effects": False,
        "dispatch_allowed": False,
        "permanent_executor_selected": False,
        "selection": None,
        "selection_rationale": None,
        "rejected_candidates": [],
        "candidate_evaluations": [],
        "blocked_reasons": [],
        "human_gates": [],
        "candidate_execution_plan": copy.deepcopy(dict(candidate_plan)),
        "ownership": {
            "admission": "apex-control-plane",
            "candidate_selection": "apex-control-plane",
            "scheduling": "apex-control-plane",
            "authority": "apex-core",
            "verification": "apex-core",
            "retry_rework": "apex-core",
            "semantic_success": "apex-core",
        },
    }


def build_execution_admission_decision(
    passport: Mapping[str, Any],
    candidate_plan: Mapping[str, Any],
    policy: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Evaluate a Candidate Execution Plan without dispatching or side effects."""
    if not isinstance(passport, Mapping):
        raise ExecutionAdmissionError("passport must be an object")
    _validate_plan(candidate_plan)
    normalized_policy = _normalize_policy(policy)
    decision = _base_decision(passport, candidate_plan, normalized_policy)
    gates = _human_gates(passport, normalized_policy)
    decision["human_gates"] = gates
    if gates:
        decision["status"] = "HUMAN_GATE_REQUIRED"
        decision["blocked_reasons"] = ["HUMAN_GATE_REQUIRED"]
        return decision
    if not normalized_policy["admission_allowed"]:
        decision["status"] = "BLOCKED_POLICY"
        decision["blocked_reasons"] = ["ADMISSION_POLICY_DENIED"]
        return decision

    required_matches = [copy.deepcopy(dict(item)) for item in candidate_plan["required_capabilities"]]
    unavailable_matches = [
        item
        for item in required_matches
        if item.get("match_status") == "UNAVAILABLE"
    ]
    ambiguous_matches = [item for item in required_matches if item.get("match_status") == "AMBIGUOUS"]
    decision["candidate_evaluations"] = _candidate_evaluations(required_matches)
    if unavailable_matches:
        decision["status"] = "BLOCKED_CAPABILITY"
        decision["blocked_reasons"] = [
            f"REQUIRED_CAPABILITY_UNAVAILABLE:{item.get('capability_id')}" for item in unavailable_matches
        ]
        decision["rejected_candidates"] = [
            _rejected(item, "REQUIRED_CAPABILITY_UNAVAILABLE") for item in decision["candidate_evaluations"]
        ]
        return decision
    if ambiguous_matches and not normalized_policy["allow_deterministic_tie_break"]:
        decision["status"] = "BLOCKED_AMBIGUITY"
        decision["blocked_reasons"] = [
            f"AMBIGUOUS_REQUIRED_CAPABILITY:{item.get('capability_id')}"
            for item in ambiguous_matches
        ]
        decision["rejected_candidates"] = [
            _rejected(item, "REQUIRED_CAPABILITY_AMBIGUOUS") for item in decision["candidate_evaluations"]
        ]
        return decision

    evaluations = decision["candidate_evaluations"]
    allowed_source_ids = set(normalized_policy["allowed_source_ids"])
    for evaluation in evaluations:
        if not evaluation["compatible_for_all_required"]:
            evaluation["rejection_reasons"].append("DOES_NOT_SATISFY_ALL_REQUIRED_CAPABILITIES")
        elif allowed_source_ids and evaluation["source_id"] not in allowed_source_ids:
            evaluation["rejection_reasons"].append("SOURCE_NOT_ALLOWED_BY_POLICY")
    eligible = [item for item in evaluations if not item["rejection_reasons"]]
    if not eligible:
        decision["status"] = "BLOCKED_POLICY" if allowed_source_ids else "BLOCKED_CAPABILITY"
        decision["blocked_reasons"] = [
            "POLICY_ALLOWED_SOURCES_HAVE_NO_COMPATIBLE_CANDIDATE"
            if allowed_source_ids
            else "NO_SINGLE_SOURCE_SATISFIES_ALL_REQUIRED_CAPABILITIES"
        ]
        decision["rejected_candidates"] = [
            _rejected(item, item["rejection_reasons"][0] if item["rejection_reasons"] else "NO_COMPATIBLE_CANDIDATE")
            for item in evaluations
        ]
        return decision

    best_quality = max(_quality_key(item) for item in eligible)
    best = [item for item in eligible if _quality_key(item) == best_quality]
    chosen: dict[str, Any] | None = None
    if len(best) == 1:
        chosen = best[0]
        rationale = "UNIQUE_HIGHEST_QUALITY_COMPATIBLE_SOURCE"
    elif normalized_policy["allow_deterministic_tie_break"]:
        chosen = sorted(best, key=lambda item: str(item["source_id"]))[0]
        rationale = "POLICY_PERMITTED_SOURCE_ID_ASC_TIE_BREAK"
    else:
        decision["status"] = "BLOCKED_AMBIGUITY"
        decision["blocked_reasons"] = ["EQUAL_QUALITY_COMPATIBLE_SOURCES"]
        decision["rejected_candidates"] = [
            _rejected(item, "UNRESOLVED_EQUAL_QUALITY") if item in best else _rejected(item, "NOT_SELECTED")
            for item in evaluations
        ]
        return decision

    decision["status"] = "ADMITTED"
    decision["admitted"] = True
    decision["selection"] = {
        "source_id": chosen["source_id"],
        "binding_scope": "TASK_CANDIDATE_ONLY",
        "permanent": False,
        "required_capabilities": copy.deepcopy(chosen["required_capabilities"]),
        "quality": copy.deepcopy(chosen["quality"]),
    }
    decision["selection_rationale"] = rationale
    decision["rejected_candidates"] = [
        _rejected(item, "SELECTED") if item["source_id"] == chosen["source_id"] else _rejected(item, "NOT_SELECTED")
        for item in evaluations
        if item["source_id"] != chosen["source_id"]
    ]
    return decision


__all__ = ["ExecutionAdmissionError", "build_execution_admission_decision"]
