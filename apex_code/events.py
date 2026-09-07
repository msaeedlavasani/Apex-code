"""Typed durable event envelope for Core execution evidence."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class EventEnvelope:
    """Versioned fact envelope; it is not a source of semantic authority."""

    event_id: str
    event_type: str
    schema_version: int
    occurred_at: str
    sequence: int
    ordering_scope: str
    correlation_id: str | None
    causation_id: str | None
    references: dict[str, str]
    payload: dict[str, Any]

    @classmethod
    def create(
        cls,
        event_id: str,
        event_type: str,
        occurred_at: str,
        payload: dict[str, Any],
        sequence: int = 0,
        ordering_scope: str = "ledger",
    ) -> "EventEnvelope":
        reference_keys = (
            "execution_id",
            "task_id",
            "attempt_id",
            "execution_epoch_id",
            "authority_revision_id",
            "runtime_lane_id",
            "resource_claim_id",
            "fence_id",
        )
        references = {
            key: value
            for key in reference_keys
            if isinstance(value := payload.get(key), str)
        }
        correlation_id = payload.get("correlation_id")
        if not isinstance(correlation_id, str):
            correlation_id = next(
                (references[key] for key in ("attempt_id", "task_id", "execution_id") if key in references),
                None,
            )
        causation_id = payload.get("causation_id")
        if not isinstance(causation_id, str):
            causation_id = None
        return cls(
            event_id=event_id,
            event_type=event_type,
            schema_version=1,
            occurred_at=occurred_at,
            sequence=sequence,
            ordering_scope=ordering_scope,
            correlation_id=correlation_id,
            causation_id=causation_id,
            references=references,
            payload=dict(payload),
        )

    def to_record(self) -> dict[str, Any]:
        return asdict(self)
