from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from apex_code.verification import BoundedArtifactVerifier


class BoundedArtifactVerifierTests(unittest.TestCase):
    def test_verifies_exact_artifact_without_runtime_claims(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            workspace = Path(root)
            artifact = workspace / "REPORT.md"
            artifact.write_text("# verified\n", encoding="utf-8")
            result = BoundedArtifactVerifier.verify(workspace, "REPORT.md", artifact, "# verified\n")
            self.assertTrue(result.passed)
            self.assertEqual(result.artifact_path, "REPORT.md")
            self.assertTrue(result.artifact_digest)

    def test_rejects_path_outside_exact_output_contract(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            workspace = Path(root)
            artifact = workspace / "OTHER.md"
            artifact.write_text("unexpected\n", encoding="utf-8")
            result = BoundedArtifactVerifier.verify(workspace, "REPORT.md", artifact, "unexpected\n")
            self.assertFalse(result.passed)

    def test_rejects_tampered_content(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            workspace = Path(root)
            artifact = workspace / "REPORT.md"
            artifact.write_text("# changed\n", encoding="utf-8")
            result = BoundedArtifactVerifier.verify(workspace, "REPORT.md", artifact, "# expected\n")
            self.assertFalse(result.passed)
            self.assertIn("differs", result.reason)


if __name__ == "__main__":
    unittest.main()
