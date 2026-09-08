"""Pure validation for durable development evidence and reconciliation receipts."""

from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Mapping


CLAIM_STATES = {"PROVEN", "PARTIAL", "NOT_PROVEN", "NOT_SUPPORTED", "UNKNOWN"}
ADMISSION_STATUSES = {
    "ADMITTED",
    "BLOCKED_CAPABILITY",
    "BLOCKED_AMBIGUITY",
    "BLOCKED_POLICY",
    "HUMAN_GATE_REQUIRED",
}
SUPPORTED_RECEIPT_TYPES = {
    "EXECUTOR_CAPABILITY_OPERATIONAL_PROBE",
    "CAPABILITY_MATCHING_AND_ADMISSION_RECONCILIATION",
    "CONTROL_PLANE_PERSISTENCE_RECONCILIATION",
    "EVIDENCE_RECEIPT_VALIDATION_RUN",
    "ARCHITECTURE_STRATEGY_OWNER_DECISION",
    "NIGHTLY_AUTONOMOUS_RUN",
}
FORBIDDEN_SECRET_KEYS = {
    "secret",
    "secrets",
    "api_key",
    "apikey",
    "token",
    "password",
    "private_key",
    "authorization",
    "cookie",
    "access_key",
}
OBVIOUS_SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
)
CLAIM_FIELD_NAMES = {
    "claim_state",
    "before",
    "after",
    "goose_claim_state",
    "freebuff_claim_state",
}
CLAIM_RANK = {
    "NOT_SUPPORTED": -1,
    "UNKNOWN": 0,
    "NOT_PROVEN": 0,
    "PARTIAL": 1,
    "PROVEN": 2,
}


def _canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _normalized_key(key: Any) -> str:
    return str(key).lower().replace("-", "_")


def _path_join(path: str, key: Any) -> str:
    return f"{path}.{key}" if path else str(key)


def _walk(value: Any, path: str = "root"):
    yield path, value
    if isinstance(value, Mapping):
        for key, nested in value.items():
            yield from _walk(nested, _path_join(path, key))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            yield from _walk(nested, f"{path}[{index}]")


def _source_index(registry: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {
        str(source.get("source_id")): source
        for source in registry.get("sources", [])
        if isinstance(source, Mapping) and isinstance(source.get("source_id"), str)
    }


def _capability_index(registry: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {
        str(capability.get("capability_id")): capability
        for capability in registry.get("capabilities", [])
        if isinstance(capability, Mapping) and isinstance(capability.get("capability_id"), str)
    }


def _mapping_index(registry: Mapping[str, Any], capability_id: str) -> dict[str, str]:
    capability = _capability_index(registry).get(capability_id, {})
    return {
        str(mapping.get("source_id")): str(mapping.get("claim_state"))
        for mapping in capability.get("source_mappings", [])
        if isinstance(mapping, Mapping) and isinstance(mapping.get("source_id"), str)
    }


def _add_error(errors: list[dict[str, str]], code: str, path: str, message: str) -> None:
    errors.append({"code": code, "path": path, "message": message})


def _check_secret_safety(receipt: Mapping[str, Any], errors: list[dict[str, str]]) -> None:
    for path, value in _walk(receipt):
        if isinstance(value, Mapping):
            for key in value:
                if _normalized_key(key) in FORBIDDEN_SECRET_KEYS:
                    _add_error(errors, "SECRET_KEY_FORBIDDEN", _path_join(path, key), "secret-shaped fields are not allowed")
        elif isinstance(value, str) and any(pattern.search(value) for pattern in OBVIOUS_SECRET_PATTERNS):
            _add_error(errors, "SECRET_PATTERN_FOUND", path, "obvious secret material is not allowed")


def _check_schema_and_claims(
    receipt: Mapping[str, Any], errors: list[dict[str, str]], claims_observed: list[dict[str, str]]
) -> None:
    if receipt.get("schema_version") != 1:
        _add_error(errors, "SCHEMA_VERSION_UNSUPPORTED", "schema_version", "receipt schema_version must be 1")
    for field in ("receipt_id", "receipt_type", "development_task_id"):
        if not isinstance(receipt.get(field), str) or not receipt[field].strip():
            _add_error(errors, "SCHEMA_FIELD_REQUIRED", field, "receipt field must be a non-empty string")
    receipt_type = receipt.get("receipt_type")
    if receipt_type not in SUPPORTED_RECEIPT_TYPES:
        _add_error(errors, "RECEIPT_TYPE_UNSUPPORTED", "receipt_type", "receipt type is outside validator v1")

    for path, value in _walk(receipt):
        if not isinstance(value, Mapping):
            continue
        for key, nested in value.items():
            normalized = _normalized_key(key)
            if normalized in CLAIM_FIELD_NAMES:
                if nested not in CLAIM_STATES:
                    _add_error(errors, "CLAIM_STATE_INVALID", _path_join(path, key), "claim state is not in the closed registry vocabulary")
                else:
                    claims_observed.append({"path": _path_join(path, key), "claim_state": str(nested)})


def _check_evidence_refs(
    receipt: Mapping[str, Any], repository_root: Path | None, errors: list[dict[str, str]]
) -> None:
    refs: list[tuple[str, str]] = []
    for path, value in _walk(receipt):
        if isinstance(value, Mapping):
            for key, nested in value.items():
                if str(key).lower().endswith("evidence_refs") and isinstance(nested, list):
                    refs.extend((f"{path}.{key}[{index}]", str(item)) for index, item in enumerate(nested) if isinstance(item, str))
    if repository_root is None:
        return
    root = repository_root.resolve()
    for path, reference in refs:
        candidate = Path(reference)
        if candidate.is_absolute() or ".." in candidate.parts:
            _add_error(errors, "EVIDENCE_REF_UNSAFE", path, "evidence references must be relative and repository-contained")
            continue
        if not (root / candidate).resolve().is_file():
            _add_error(errors, "EVIDENCE_REF_MISSING", path, f"evidence reference does not exist: {reference}")


def _check_registry_consistency(
    receipt: Mapping[str, Any], registry: Mapping[str, Any], errors: list[dict[str, str]]
) -> None:
    receipt_type = receipt.get("receipt_type")
    source_ids = _source_index(registry)
    capability_ids = _capability_index(registry)

    if receipt_type == "EXECUTOR_CAPABILITY_OPERATIONAL_PROBE":
        capability_id = receipt.get("canonical_capability", {}).get("capability_id")
        if capability_id not in capability_ids:
            _add_error(errors, "REGISTRY_CAPABILITY_MISSING", "canonical_capability.capability_id", "capability is absent from the registry")
            return
        mappings = _mapping_index(registry, str(capability_id))
        operational = receipt.get("operational_evidence", {})
        if not isinstance(operational, Mapping):
            _add_error(errors, "EVIDENCE_SECTION_INVALID", "operational_evidence", "operational_evidence must be an object")
            return
        for label, source_id in (("goose", "goose-cli"), ("freebuff", "freebuff-cli")):
            observation = operational.get(label)
            if source_id not in source_ids or source_id not in mappings:
                _add_error(errors, "REGISTRY_SOURCE_MISSING", f"operational_evidence.{label}", "operational source is absent from the registry mapping")
                continue
            if observation is None:
                _add_error(errors, "EVIDENCE_SECTION_INVALID", f"operational_evidence.{label}", "operational source observation is missing")
                continue
            if not isinstance(observation, Mapping):
                _add_error(errors, "EVIDENCE_SECTION_INVALID", f"operational_evidence.{label}", "source observation must be an object")
                continue
            claim_state = observation.get("claim_state")
            if claim_state != mappings[source_id]:
                _add_error(errors, "REGISTRY_CLAIM_MISMATCH", f"operational_evidence.{label}.claim_state", "operational claim differs from current registry mapping")
        result = receipt.get("result", {})
        if isinstance(result, Mapping):
            for label, source_id in (("goose", "goose-cli"), ("freebuff", "freebuff-cli")):
                state_key = f"{label}_claim_state"
                if state_key in result and result[state_key] != mappings.get(source_id):
                    _add_error(errors, "REGISTRY_CLAIM_MISMATCH", f"result.{state_key}", "result claim differs from current registry mapping")

    elif receipt_type == "CAPABILITY_MATCHING_AND_ADMISSION_RECONCILIATION":
        registry_section = receipt.get("registry")
        if not isinstance(registry_section, Mapping):
            _add_error(errors, "REGISTRY_SECTION_REQUIRED", "registry", "reconciliation receipts require a registry section")
            return
        if registry_section.get("registry_id") != registry.get("registry_id"):
            _add_error(errors, "REGISTRY_ID_MISMATCH", "registry.registry_id", "receipt registry id differs from current registry")
        if registry_section.get("revision") != registry.get("revision"):
            _add_error(errors, "REGISTRY_REVISION_MISMATCH", "registry.revision", "receipt registry revision differs from current registry")
        capability_id = registry_section.get("capability_id")
        if capability_id not in capability_ids:
            _add_error(errors, "REGISTRY_CAPABILITY_MISSING", "registry.capability_id", "capability is absent from the registry")
            return
        mapping_changes = registry_section.get("mapping_changes", {})
        if not isinstance(mapping_changes, Mapping):
            _add_error(errors, "MAPPING_CHANGES_INVALID", "registry.mapping_changes", "mapping_changes must be an object")
            return
        mappings = _mapping_index(registry, str(capability_id))
        for source_id, change in mapping_changes.items():
            if source_id not in source_ids or source_id not in mappings:
                _add_error(errors, "REGISTRY_SOURCE_MISSING", f"registry.mapping_changes.{source_id}", "mapping source is absent from the registry")
                continue
            if not isinstance(change, Mapping) or change.get("after") != mappings[source_id]:
                _add_error(errors, "REGISTRY_CLAIM_MISMATCH", f"registry.mapping_changes.{source_id}.after", "receipt mapping does not match current registry")


def _check_no_unsupported_promotion(receipt: Mapping[str, Any], errors: list[dict[str, str]]) -> None:
    changes = receipt.get("registry", {}).get("mapping_changes", {})
    if not isinstance(changes, Mapping):
        return
    for source_id, change in changes.items():
        if not isinstance(change, Mapping):
            continue
        before = change.get("before")
        after = change.get("after")
        if before in CLAIM_RANK and after in CLAIM_RANK and CLAIM_RANK[after] > CLAIM_RANK[before]:
            proof = receipt.get("promotion_evidence")
            if not isinstance(proof, Mapping) or proof.get("evidence_class") != "OBSERVED_RUNTIME_EVIDENCE" or proof.get("acceptance_demonstrated") is not True:
                _add_error(errors, "UNSUPPORTED_CLAIM_PROMOTION", f"registry.mapping_changes.{source_id}", "claim promotion requires explicit demonstrated runtime evidence")


def _check_admission_policy(receipt: Mapping[str, Any], errors: list[dict[str, str]]) -> None:
    admission = receipt.get("ac_dev_018_admission")
    if admission is None:
        return
    if not isinstance(admission, Mapping):
        _add_error(errors, "ADMISSION_SECTION_INVALID", "ac_dev_018_admission", "admission section must be an object")
        return
    status = admission.get("status")
    if status not in ADMISSION_STATUSES:
        _add_error(errors, "ADMISSION_STATUS_INVALID", "ac_dev_018_admission.status", "admission status is outside the AC-DEV-018 vocabulary")
    policy = admission.get("policy", {})
    if not isinstance(policy, Mapping):
        _add_error(errors, "ADMISSION_POLICY_INVALID", "ac_dev_018_admission.policy", "admission policy must be an object")
        return
    allow_tie_break = policy.get("allow_deterministic_tie_break")
    strategy = policy.get("tie_break_strategy")
    used = policy.get("source_id_asc_used")
    if not isinstance(allow_tie_break, bool) or not isinstance(used, bool):
        _add_error(errors, "ADMISSION_POLICY_INVALID", "ac_dev_018_admission.policy", "tie-break policy fields must be boolean")
    if used and not (allow_tie_break is True and strategy == "SOURCE_ID_ASC"):
        _add_error(errors, "ADMISSION_TIE_BREAK_UNAUTHORIZED", "ac_dev_018_admission.policy", "SOURCE_ID_ASC use requires explicit matching policy")
    if status == "ADMITTED" and admission.get("selection") is None:
        _add_error(errors, "ADMISSION_SELECTION_MISSING", "ac_dev_018_admission.selection", "ADMITTED receipts require a task-scoped selection")
    if status != "ADMITTED" and admission.get("selection") is not None:
        _add_error(errors, "ADMISSION_SELECTION_ON_BLOCK", "ac_dev_018_admission.selection", "blocked receipts cannot contain a selection")
    for field in ("runtime_side_effects", "dispatch_allowed", "permanent_executor_selected"):
        if admission.get(field) is not False:
            _add_error(errors, "ADMISSION_BOUNDARY_VIOLATION", f"ac_dev_018_admission.{field}", f"{field} must remain false")


def validate_receipt(
    receipt: Mapping[str, Any],
    registry: Mapping[str, Any],
    *,
    repository_root: Path | None = None,
) -> dict[str, Any]:
    """Validate one receipt without mutating it or promoting any claim."""
    original = copy.deepcopy(dict(receipt)) if isinstance(receipt, Mapping) else receipt
    errors: list[dict[str, str]] = []
    claims_observed: list[dict[str, str]] = []
    if not isinstance(receipt, Mapping):
        _add_error(errors, "RECEIPT_NOT_OBJECT", "root", "receipt must be an object")
        return {"validator_schema_version": 1, "valid": False, "errors": errors, "claims_observed": [], "mutated_input": False}
    if not isinstance(registry, Mapping):
        _add_error(errors, "REGISTRY_NOT_OBJECT", "registry", "registry must be an object")
    _check_secret_safety(receipt, errors)
    _check_schema_and_claims(receipt, errors, claims_observed)
    _check_evidence_refs(receipt, repository_root, errors)
    if isinstance(registry, Mapping):
        _check_registry_consistency(receipt, registry, errors)
    _check_no_unsupported_promotion(receipt, errors)
    _check_admission_policy(receipt, errors)
    return {
        "validator_schema_version": 1,
        "validator": "apex-control-plane-evidence-receipts-v1",
        "receipt_id": receipt.get("receipt_id"),
        "receipt_type": receipt.get("receipt_type"),
        "valid": not errors,
        "errors": errors,
        "claims_observed": claims_observed,
        "input_digest": _canonical_digest(receipt),
        "mutated_input": original != receipt,
        "claim_promotion": False,
    }


def validate_receipt_file(
    receipt_path: Path,
    registry_path: Path,
    *,
    repository_root: Path | None = None,
) -> dict[str, Any]:
    """Load and validate a receipt file using the current registry."""
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    return validate_receipt(receipt, registry, repository_root=repository_root)


__all__ = ["validate_receipt", "validate_receipt_file"]
