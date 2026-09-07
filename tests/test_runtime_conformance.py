from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from apex_code.contract import RuntimeAdapter, RuntimeExecution, RuntimeFact, RuntimeIdentity
from apex_code.runtime import OpenCodeRuntimeAdapter


def assert_runtime_adapter_contract(test: unittest.TestCase, adapter: RuntimeAdapter) -> None:
    """Exercise the substrate-neutral portion of the adapter contract.

    This deliberately stops before provider execution.  Runtime execution is
    covered by the bounded vertical-slice tests; this helper checks that an
    adapter's preparation and returned fact/result shape cannot assign Apex
    semantic success directly.
    """
    test.assertIsInstance(adapter, RuntimeAdapter)
    with tempfile.TemporaryDirectory(prefix="apex-runtime-contract-") as root:
        preparation = adapter.materialize_authority("authority-digest-test")
        test.assertEqual(preparation.authority_digest, "authority-digest-test")
        test.assertTrue(preparation.preparation_id)
        test.assertTrue(Path(preparation.config_dir).is_dir())

        result = RuntimeExecution(
            identity=RuntimeIdentity(session_id="opaque-session", process_id=7, adapter_instance_id="test-adapter"),
            fact=RuntimeFact.UNKNOWN,
            exit_code=None,
            text="",
            event_count=0,
            preparation_id=preparation.preparation_id,
            authority_config_digest=preparation.authority_digest,
            command=("adapter", "<prompt>"),
        )
        test.assertIn(result.fact, set(RuntimeFact))
        test.assertEqual(result.preparation_id, preparation.preparation_id)
        test.assertEqual(result.authority_config_digest, preparation.authority_digest)
        test.assertFalse(hasattr(result, "semantic_success"))
        shutil.rmtree(preparation.config_dir, ignore_errors=True)


class RuntimeAdapterConformanceTests(unittest.TestCase):
    def test_opencode_adapter_satisfies_portable_contract(self) -> None:
        assert_runtime_adapter_contract(self, OpenCodeRuntimeAdapter(executable="opencode"))

    def test_runtime_fact_vocabulary_is_closed_and_semantic_state_is_core_owned(self) -> None:
        self.assertEqual(
            {fact.value for fact in RuntimeFact},
            {"RUNNING", "EXITED", "MISSING", "UNREACHABLE", "MISMATCH", "UNKNOWN"},
        )
        self.assertNotIn("SUCCEEDED", {fact.value for fact in RuntimeFact})


if __name__ == "__main__":
    unittest.main()
