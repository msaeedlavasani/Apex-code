"""Minimal Apex Code execution slice.

The package is intentionally small and standard-library-only while the first
Runtime Adapter contract is being validated.
"""

from .core import (
    AuthorityDenied,
    AuthorityRevision,
    ExecutionCoordinator,
    ExecutionManifest,
    RuntimeFact,
    SafetyError,
)
from .runtime import OpenCodeRuntimeAdapter

__all__ = [
    "AuthorityDenied",
    "AuthorityRevision",
    "ExecutionCoordinator",
    "ExecutionManifest",
    "OpenCodeRuntimeAdapter",
    "RuntimeFact",
    "SafetyError",
]
