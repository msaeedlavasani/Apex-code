# Runtime Adapter Cross-Substrate Conformance 0001

Status: `PROPOSED` evidence report; no architecture status change
Evidence date: 2026-09-07 Asia/Tehran
Scope: Goose availability check and reusable conformance checks for the existing adapter seam

## 1. Track C result

`SUBSTRATE_UNAVAILABLE` for Goose.

The requested executable check was performed:

```text
command -v goose → not found
goose --version   → command not found
```

No Goose checkout was present in the local reference-repository area or the
disposable `/tmp` source area. No installation was attempted: there was no
existing executable to reuse, and installing a new runtime would add an
unnecessary external variable and could require credentials or persistent
machine changes. The lack of a second substrate does not block the independent
OpenCode authority/recovery evidence in Tracks A/B.

## 2. Contract evidence

The current Apex contract was inspected in:

- `apex_code/contract.py`
- `apex_code/runtime.py`
- `apex_code/reconciliation.py`
- `tests/test_vertical_slice.py`
- `tests/test_reconciliation.py`

The reusable helper at
[`tests/test_runtime_conformance.py`](../../tests/test_runtime_conformance.py)
checks the substrate-neutral contract without calling a provider:

- adapter structural conformance;
- authority preparation digest preservation;
- stable preparation identity;
- opaque runtime identity fields;
- closed runtime-fact vocabulary;
- result correlation to preparation;
- absence of direct semantic-success state on `RuntimeExecution`.

The OpenCode adapter passes these checks. This is `SOURCE_CODE_EVIDENCE` and
unit-test evidence for the bounded contract, not proof of a second-substrate
implementation or of exact authority binding.

## 3. Field portability assessment

| Contract area | Assessment | Evidence / limitation |
| --- | --- | --- |
| preparation identity | `PORTABLE` | `RuntimePreparation.preparation_id` is opaque to Core and is exercised by the suite |
| authority digest correlation | `SUBSTRATE_SPECIFIC_BUT_ADAPTABLE` | OpenCode carries a digest, but active-substrate attestation remains `NOT_PROVEN` |
| runtime identity | `PORTABLE` | `RuntimeIdentity` separates opaque session/process/adapter fields from Apex Attempt identity |
| execute entry point | `PORTABLE` | Protocol accepts prompt/workspace/preparation; provider execution itself was not cross-tested |
| runtime facts | `PORTABLE` | `RuntimeFact` is substrate-neutral and excludes semantic success |
| result collection | `SUBSTRATE_SPECIFIC_BUT_ADAPTABLE` | `RuntimeExecution.text`/event count fit the bounded adapter; durable result parity is not proven |
| identity mismatch detection | `NOT_PROVEN` cross-substrate | Core tests cover mismatch inputs; no second substrate supplied observations |
| missing/unreachable fail-closed behavior | `PORTABLE` conceptually | Core reconciliation maps facts conservatively; second-substrate runtime proof is unavailable |
| direct semantic Task success | `PORTABLE` prohibition | Contract has no semantic-success field; Core owns verification and semantic state |
| exact authority activation/binding | `MISSING_ON_SUBSTRATE` for observed OpenCode surface | No direct attestation was exposed; Goose was unavailable |

No `WRONG_ABSTRACTION` was established. The remaining `NOT_PROVEN` entries
must not be filled with assumptions from OpenCode or from the contract tests.

## 4. Track D status

`PARTIALLY_COMPLETE`.

The reusable architecture-level checks pass for the existing OpenCode adapter.
They intentionally do not claim:

- a second-substrate conformance result;
- provider/model portability in execution;
- active authority attestation;
- controller-loss recovery;
- global event ordering;
- independent semantic verification.

The suite tests contract behavior rather than OpenCode internals and does not
alter the default adapter composition.

## 5. Recommended next step

When an already-authorized second substrate is safely available, run the same
helper against an experimental adapter and classify unsupported fields
explicitly. Do not add Goose or another runtime as a permanent dependency
without a separate Owner decision.
