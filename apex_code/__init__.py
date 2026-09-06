"""Minimal Apex Code execution slice.

The package is intentionally small and standard-library-only while the first
Runtime Adapter contract is being validated.
"""

from .core import (
    AuthorityDenied,
    AuthorityRevision,
    DuplicateStart,
    ExecutionCoordinator,
    ExecutionManifest,
    IdentityMismatch,
    ResourceConflict,
    RuntimeFact,
    SafetyError,
)
from .reconciliation import ReconciliationLoop, ReconciliationOutcome, RuntimeObservation
from .runtime import OpenCodeRuntimeAdapter

__all__ = [
    "AuthorityDenied",
    "AuthorityRevision",
    "DuplicateStart",
    "ExecutionCoordinator",
    "ExecutionManifest",
    "IdentityMismatch",
    "OpenCodeRuntimeAdapter",
    "ReconciliationLoop",
    "ReconciliationOutcome",
    "RuntimeFact",
    "RuntimeObservation",
    "ResourceConflict",
    "SafetyError",
]
