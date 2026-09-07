"""Substrate-neutral Runtime Adapter Contract v1 for the bounded slice.

The contract deliberately carries facts and opaque runtime identity. It does
not contain Apex semantic Task states or authority decisions.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Protocol, runtime_checkable


class RuntimeFact(str, Enum):
    RUNNING = "RUNNING"
    EXITED = "EXITED"
    MISSING = "MISSING"
    UNREACHABLE = "UNREACHABLE"
    MISMATCH = "MISMATCH"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class RuntimeIdentity:
    """Native identity observed by an adapter; never an Apex Attempt ID."""

    session_id: str | None = None
    process_id: int | None = None
    adapter_instance_id: str | None = None


@dataclass(frozen=True)
class RuntimePreparation:
    """Opaque preparation evidence shared by materialization and execution."""

    preparation_id: str
    authority_digest: str
    config_dir: str
    mode: str
    substrate_activation_confirmed: bool = False


@dataclass(frozen=True)
class RuntimeExecution:
    """Substrate facts returned by an adapter; Core interprets their meaning."""

    identity: RuntimeIdentity
    fact: RuntimeFact
    exit_code: int | None
    text: str
    event_count: int
    preparation_id: str
    authority_config_digest: str
    command: tuple[str, ...]

    @property
    def session_id(self) -> str | None:
        return self.identity.session_id


@runtime_checkable
class RuntimeAdapter(Protocol):
    """Minimum adapter seam used by Core; no substrate type leaks into Core."""

    model: str

    def materialize_authority(self, authority_digest: str) -> RuntimePreparation:
        """Prepare a substrate context without assigning semantic state."""

    def execute(self, prompt: str, workspace: Path, preparation: RuntimePreparation) -> RuntimeExecution:
        """Execute after Core releases its barrier and report substrate facts."""
