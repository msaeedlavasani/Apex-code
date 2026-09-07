"""Core-owned bounded artifact verification.

The verifier is intentionally independent of the Runtime Adapter.  It checks
the artifact on disk after the adapter returns and never assigns runtime or
Task semantic state itself.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path


@dataclass(frozen=True)
class ArtifactVerification:
    passed: bool
    reason: str
    artifact_path: str | None = None
    artifact_digest: str | None = None


class BoundedArtifactVerifier:
    """Verify one exact regular file in one exact workspace directory."""

    @staticmethod
    def verify(workspace: Path, output_name: str, artifact_path: Path, expected_content: str) -> ArtifactVerification:
        root = workspace.resolve()
        expected_path = root / output_name
        if Path(output_name).name != output_name or artifact_path.resolve() != expected_path:
            return ArtifactVerification(False, "artifact path is outside the bounded output contract")
        if not artifact_path.exists() or artifact_path.is_symlink() or not artifact_path.is_file():
            return ArtifactVerification(False, "expected artifact is not a regular file")
        try:
            actual = artifact_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            return ArtifactVerification(False, "artifact could not be read for verification")
        if actual != expected_content:
            return ArtifactVerification(False, "artifact readback differs from the expected bounded result")
        artifact_digest = hashlib.sha256(actual.encode("utf-8")).hexdigest()
        return ArtifactVerification(
            True,
            "Core independently verified exact bounded artifact path and content",
            output_name,
            artifact_digest,
        )
