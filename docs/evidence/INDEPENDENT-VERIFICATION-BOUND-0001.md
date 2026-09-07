# Independent Verification Bound 0001

Status: `PROPOSED` evidence report; no architecture status change
Evidence date: 2026-09-07 Asia/Tehran
Scope: bounded artifact verification for the existing Core execution slice

## Result

`PARTIALLY_PROVEN`: Apex now has a small Core-owned verifier independent of
the Runtime Adapter for the existing bounded artifact task shapes. The full
semantic verification claim remains `NOT_PROVEN`.

The verifier in
[`apex_code/verification.py`](../../apex_code/verification.py) runs after the
adapter returns and checks:

- exact output filename in the resolved workspace;
- regular-file and non-symlink status;
- UTF-8 readback;
- exact equality with the bounded expected result;
- a digest of the verified content.

The runtime adapter cannot set `semantic_success`; Core calls the verifier and
uses its result as one input to the existing bounded semantic-success path.
The verifier does not inspect model quality, independently derive broad task
meaning, or replace human acceptance.

## Evidence

`tests/test_verification.py` directly covers:

1. exact artifact verification and digest production;
2. rejection of an output path outside the exact contract;
3. rejection of tampered content.

The full Python suite passed with 25 tests after this change. The existing
vertical-slice tests also continue to demonstrate that runtime completion
alone does not produce semantic success.

Evidence labels: `SOURCE_CODE_EVIDENCE` for the verifier implementation,
`OBSERVED_REPOSITORY_STATE` for its integration into Core, and
`OBSERVED_RUNTIME_EVIDENCE` is not claimed by this unit-only result.

## Boundary retained

This bounded result does not prove:

- general semantic correctness;
- independent model/output judgment;
- human acceptance or operational verification;
- authority activation/binding;
- controller-loss recovery;
- checkpoint side-effect safety.

Advanced Verification remains optional and no external dependency was added.
