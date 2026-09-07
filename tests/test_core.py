from __future__ import annotations

import tempfile
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path

from apex_code.core import (
    AuthorityDenied,
    AuthorityEvidence,
    ExecutionBarrier,
    ExecutionCoordinator,
    ExecutionManifest,
    RuntimeLane,
)


class CoreSafetyTests(unittest.TestCase):
    def test_manifest_is_immutable(self) -> None:
        manifest = ExecutionManifest("m", "a", "t", "ar", "agent", "model", "req", "snap", "now")
        with self.assertRaises(FrozenInstanceError):
            manifest.attempt_id = "other"  # type: ignore[misc]

    def test_barrier_fails_closed_on_identity_mismatch(self) -> None:
        manifest = ExecutionManifest("m", "a", "t", "ar", "agent", "model", "req", "snap", "now")
        lane = RuntimeLane("lane", "a", "/tmp/workspace", "now")
        evidence = AuthorityEvidence("wrong", "digest", "lane", "a", "epoch", True, False, "CORE_MEDIATED_NO_RUNTIME_IO")
        with self.assertRaisesRegex(Exception, "authority revision mismatch"):
            ExecutionBarrier.release(manifest, lane, evidence)

    def test_barrier_fails_closed_when_authority_is_unmaterialized(self) -> None:
        manifest = ExecutionManifest("m", "a", "t", "ar", "agent", "model", "req", "snap", "now")
        lane = RuntimeLane("lane", "a", "/tmp/workspace", "now")
        evidence = AuthorityEvidence("ar", "digest", "lane", "a", "epoch", False, False, "CORE_MEDIATED_NO_RUNTIME_IO")
        with self.assertRaisesRegex(Exception, "not materialized"):
            ExecutionBarrier.release(manifest, lane, evidence)

    def test_path_boundary_denies_escape(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            workspace = Path(root)
            with self.assertRaises(AuthorityDenied):
                ExecutionCoordinator._safe_path(workspace, "../outside.txt", "write")
            with self.assertRaises(AuthorityDenied):
                ExecutionCoordinator._safe_path(workspace, "other.txt", "read")

    def test_default_adapter_is_lazy_and_available(self) -> None:
        coordinator = ExecutionCoordinator()
        self.assertEqual(coordinator.adapter.__class__.__name__, "OpenCodeRuntimeAdapter")


if __name__ == "__main__":
    unittest.main()
