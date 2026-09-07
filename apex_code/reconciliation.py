"""Bounded Core reconciliation for restart and uncertain runtime facts."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
from pathlib import Path
from typing import Iterable

from .core import ExecutionLedger, IdentityMismatch, RuntimeFact, now
from .contract import RuntimeIdentity


@dataclass(frozen=True)
class RuntimeObservation:
    fact: RuntimeFact
    attempt_id: str | None = None
    session_id: str | None = None
    verified_artifact: bool = False
    detail: str = ""
    identity: RuntimeIdentity | None = None


@dataclass(frozen=True)
class ReconciliationOutcome:
    attempt_id: str | None
    runtime_fact: RuntimeFact
    semantic_state: str
    disposition: str
    orphan: bool = False
    identity_valid: bool = True


class ReconciliationLoop:
    """Reconcile durable Core records with external adapter observations.

    The loop never adopts a runtime identity, starts work, or converts an
    external fact directly into Task success. Non-terminal uncertainty remains
    fenced and requires recovery/verification.
    """

    def __init__(self, ledger_path: Path) -> None:
        self.ledger_path = ledger_path

    def reconcile(self, observations: Iterable[RuntimeObservation]) -> list[ReconciliationOutcome]:
        ledger = ExecutionLedger(self.ledger_path)
        data = ledger.snapshot()
        attempts = data.get("attempts", {})
        outcomes: list[ReconciliationOutcome] = []
        seen_attempts: set[str] = set()

        for observation in observations:
            attempt_id = observation.attempt_id
            if not attempt_id or attempt_id not in attempts:
                ledger.event(
                    "runtime.orphan_observed",
                    {
                        "attempt_id": attempt_id,
                        "runtime_session_id": observation.session_id,
                        "runtime_fact": observation.fact.value,
                        "disposition": "QUARANTINED",
                    },
                )
                outcomes.append(
                    ReconciliationOutcome(
                        attempt_id=attempt_id,
                        runtime_fact=observation.fact,
                        semantic_state="UNKNOWN",
                        disposition="ORPHAN_QUARANTINED",
                        orphan=True,
                        identity_valid=False,
                    )
                )
                continue

            seen_attempts.add(attempt_id)
            try:
                attempt = ledger.validate_attempt_identity(attempt_id)
            except IdentityMismatch as exc:
                ledger.event(
                    "reconciliation.identity_mismatch",
                    {"attempt_id": attempt_id, "runtime_fact": observation.fact.value, "detail": str(exc)},
                )
                outcomes.append(
                    ReconciliationOutcome(
                        attempt_id=attempt_id,
                        runtime_fact=RuntimeFact.MISMATCH,
                        semantic_state="RECOVERY_REQUIRED",
                        disposition="MISMATCH_FAIL_CLOSED",
                        identity_valid=False,
                    )
                )
                continue

            expected_session = attempt.get("runtime_session_id")
            if expected_session is None or (
                observation.session_id is not None and observation.session_id != expected_session
            ):
                ledger.event(
                    "reconciliation.identity_mismatch",
                    {
                        "attempt_id": attempt_id,
                        "expected_runtime_session_id": expected_session,
                        "observed_runtime_session_id": observation.session_id,
                        "runtime_fact": observation.fact.value,
                    },
                )
                outcomes.append(
                    ReconciliationOutcome(
                        attempt_id=attempt_id,
                        runtime_fact=RuntimeFact.MISMATCH,
                        semantic_state="RECOVERY_REQUIRED",
                        disposition="MISMATCH_FAIL_CLOSED",
                        identity_valid=False,
                    )
                )
                continue

            expected_identity = attempt.get("runtime_identity")
            if observation.identity is not None and isinstance(expected_identity, dict):
                observed_identity = asdict(observation.identity)
                identity_mismatch = any(
                    expected_identity.get(key) is not None
                    and observed_identity.get(key) is not None
                    and expected_identity.get(key) != observed_identity.get(key)
                    for key in ("session_id", "process_id", "adapter_instance_id")
                )
                if identity_mismatch:
                    ledger.event(
                        "reconciliation.identity_mismatch",
                        {
                            "attempt_id": attempt_id,
                            "expected_runtime_identity": expected_identity,
                            "observed_runtime_identity": observed_identity,
                            "runtime_fact": observation.fact.value,
                        },
                    )
                    outcomes.append(
                        ReconciliationOutcome(
                            attempt_id=attempt_id,
                            runtime_fact=RuntimeFact.MISMATCH,
                            semantic_state="RECOVERY_REQUIRED",
                            disposition="MISMATCH_FAIL_CLOSED",
                            identity_valid=False,
                        )
                    )
                    continue

            semantic_state, disposition = self._classify(observation, data, attempt_id)
            ledger.put(
                "attempts",
                attempt_id,
                {
                    **attempt,
                    "last_runtime_fact": observation.fact.value,
                    "reconciliation_state": semantic_state,
                    "last_reconciled_at": now(),
                },
            )
            if semantic_state == "SUCCEEDED":
                task_id = attempt.get("task_id")
                task = data.get("tasks", {}).get(task_id, {})
                ledger.put("tasks", task_id, {**task, "semantic_state": "SUCCEEDED"})
                ledger.put("attempts", attempt_id, {**attempt, "status": "SUCCEEDED", "reconciliation_state": semantic_state})
                ledger.update_fence(attempt_id, "RELEASED")
            ledger.event(
                "reconciliation.completed",
                {
                    "attempt_id": attempt_id,
                    "runtime_fact": observation.fact.value,
                    "semantic_state": semantic_state,
                    "disposition": disposition,
                    "detail": observation.detail,
                },
            )
            outcomes.append(
                ReconciliationOutcome(
                    attempt_id=attempt_id,
                    runtime_fact=observation.fact,
                    semantic_state=semantic_state,
                    disposition=disposition,
                )
            )

        # Startup recovery loads all non-terminal attempts. A missing
        # observation is itself UNKNOWN; the durable fence remains in place.
        for attempt_id, attempt in attempts.items():
            if attempt.get("status") in {"SUCCEEDED", "FAILED", "CANCELLED"} or attempt_id in seen_attempts:
                continue
            ledger.event(
                "reconciliation.unknown",
                {"attempt_id": attempt_id, "semantic_state": "RECOVERY_REQUIRED", "reason": "no runtime observation"},
            )
            outcomes.append(
                ReconciliationOutcome(
                    attempt_id=attempt_id,
                    runtime_fact=RuntimeFact.UNKNOWN,
                    semantic_state="RECOVERY_REQUIRED",
                    disposition="NO_OBSERVATION_FAIL_CLOSED",
                )
            )
        return outcomes

    @staticmethod
    def _classify(observation: RuntimeObservation, data: dict[str, object], attempt_id: str) -> tuple[str, str]:
        if observation.fact is RuntimeFact.RUNNING:
            return "RECOVERY_REQUIRED", "ACTIVE_RUNTIME_REQUIRES_RECONCILIATION"
        if observation.fact is RuntimeFact.EXITED:
            if ReconciliationLoop._persisted_artifact_is_verified(data, attempt_id):
                return "SUCCEEDED", "VERIFIED_RESULT"
            return "VERIFYING", "RESULT_REQUIRES_VERIFICATION"
        if observation.fact is RuntimeFact.MISSING:
            return "LOST", "RUNTIME_MISSING"
        if observation.fact is RuntimeFact.UNREACHABLE:
            return "RECOVERY_REQUIRED", "RUNTIME_UNREACHABLE"
        if observation.fact is RuntimeFact.MISMATCH:
            return "RECOVERY_REQUIRED", "IDENTITY_MISMATCH"
        return "RECOVERY_REQUIRED", "UNKNOWN_FAIL_CLOSED"

    @staticmethod
    def _persisted_artifact_is_verified(data: dict[str, object], attempt_id: str) -> bool:
        """Verify persisted Core evidence; never trust an adapter success flag."""
        results = data.get("results", {})
        artifacts = data.get("artifacts", {})
        result = results.get(attempt_id) if isinstance(results, dict) else None
        if not isinstance(result, dict) or result.get("verification") != "PASS":
            return False
        if result.get("semantic_success") is not True:
            return False
        if not isinstance(artifacts, dict):
            return False
        for artifact in artifacts.values():
            if not isinstance(artifact, dict) or artifact.get("attempt_id") != attempt_id:
                continue
            relative = artifact.get("path")
            expected = artifact.get("sha256")
            if not isinstance(relative, str) or not isinstance(expected, str):
                continue
            ledger_path = data.get("_ledger_path")
            if not isinstance(ledger_path, str):
                continue
            candidate = Path(ledger_path).parent / relative
            if candidate.is_file() and hashlib.sha256(candidate.read_bytes()).hexdigest() == expected:
                return True
        return False
