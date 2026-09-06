# Safe Vertical Slice 0001 Evidence

Status: `PROPOSED` implementation evidence; this document records one bounded
smoke run and does not upgrade the general authority-binding guarantee.

## Scope

The slice implements the smallest Core-mediated path for:

```text
ExecutionRequest
→ Execution
→ Core Task
→ Attempt
→ immutable ExecutionManifest
→ bounded AuthorityRevision
→ RuntimeLane
→ Core-owned barrier
→ OpenCode Runtime Adapter
→ AttemptResult
→ Core verification
→ REPORT.md artifact
→ durable JSON execution evidence
```

The worker receives the authorized `README.md` content as controlled input.
OpenCode is launched with deny-all filesystem/tool permissions. Apex Core owns
the repository read, artifact write, path boundary, verification, semantic
state, and JSON ledger. This deliberately avoids claiming that OpenCode has
proven Apex-grade authority activation.

Implementation paths:

- `apex_code/core.py`
- `apex_code/runtime.py`
- `apex_code/cli.py`
- `tests/test_core.py`
- `tests/test_vertical_slice.py`

## Observed smoke run

The run used an isolated temporary copy of the repository `README.md` and the
installed OpenCode executable:

| Field | Observation |
| --- | --- |
| OpenCode executable | `/usr/local/bin/opencode` |
| OpenCode version | `1.18.25` |
| Model | `opencode/big-pickle` |
| Execution | `exec_6e5ab2c442a946df` |
| Core Task | `task_652c356939564c72` |
| Attempt | `att_a5b40d07127a4ce6` |
| ExecutionEpoch | `epoch_f74708930c944840` |
| ExecutionManifest | `manifest_f83663d7fd0c4b9b` |
| RuntimeLane | `lane_d3010144c67d4649` |
| Runtime session | `ses_f86e22feeffew54SV57lqgc3X3` |
| AuthorityRevision | `ar_slice_report_001` |
| Runtime fact | `EXITED` |
| Core verification | `PASS` |
| Semantic success | `true` |
| Artifact | `REPORT.md` |
| Artifact SHA-256 | `c26fba51a477d88a953e141099b755012a2b412deb15a5b3d8360a44dc834728` |

The durable ledger recorded request, execution, task, attempt, manifest,
authority, lane, barrier, result, artifact, and typed lifecycle events. The
event sequence was:

```text
attempt.created
manifest.created
authority.materialized
execution.barrier_released
runtime.fact
verification.completed
task.semantic_state
```

## Acceptance results

| Acceptance | Result | Evidence |
| --- | --- | --- |
| Open repository/workspace | PASS | Core read a bounded `README.md` from an isolated temporary workspace. |
| Create ExecutionRequest, Execution, Task, Attempt | PASS | Durable ledger records all four relationships. |
| One immutable manifest per Attempt | PASS | Frozen manifest object and ledger manifest record. |
| Bounded authority derived | PASS | Core `PermissionEnvelope` allows only `README.md` read and `REPORT.md` write. |
| Authority uncertainty fails closed | PASS | Unit tests reject unmaterialized or identity-mismatched evidence. |
| Runtime barrier before adapter start | PASS within Core-mediated mode | Core releases only after digest/identity checks; OpenCode substrate activation remains `NOT_PROVEN`. |
| OpenCode Runtime Adapter execution | PASS | OpenCode returned JSON events and an `EXITED` runtime fact. |
| Core verification before semantic success | PASS | Artifact markers, exact target, write, and readback were verified. |
| Authorized report creation | PASS | Core created and read back `REPORT.md`. |
| Unauthorized filesystem access | PASS at Core boundary | Path traversal and non-authorized read/write targets are denied by unit tests. OpenCode tool-level denial was not presented as independent proof. |
| Runtime completion alone means success | PASS negative test | An `EXITED` result without a verified report remains semantic failure/unknown and creates no artifact. |
| Sufficient evidence persisted | PASS | Atomic JSON ledger and artifact digest are written in the isolated workspace. |

## Security and proof boundary

The slice is safe because the OpenCode worker has no permitted file or shell
side-effect path. Core writes only the exact authorized artifact after
verification. A denied path is rejected before filesystem access, including
workspace escape and symlink targets.

This is not proof of the broader sequence:

```text
PermissionEnvelope
→ AuthorityRevision
→ materialization
→ activation verification
→ exact RuntimeLane binding
→ exact Attempt / ExecutionEpoch binding
→ ExecutionBarrier
→ START
```

The general OpenCode authority activation/binding guarantee remains
`NOT_PROVEN`, as does controller-loss reconciliation and duplicate-start
prevention. The slice's `CORE_MEDIATED_NO_RUNTIME_IO` mode is an explicit
bounded safety posture around those gaps, not a replacement Runtime Adapter
contract.

## Validation

Executed successfully:

```text
python3 -B -m unittest discover -s tests -v
python3 -B -m apex_code.cli <isolated-workspace> --opencode /usr/local/bin/opencode --model opencode/big-pickle
python3 scripts/validate_docs.py
git diff --check
```

The unit suite contains six tests covering manifest immutability, barrier
failure, path denial, verified artifact success, runtime-completion-vs-success,
and the Core-mediated slice contract.

## Remaining NOT_PROVEN items

- OpenCode active authority attestation.
- Exact AuthorityRevision → RuntimeLane → Attempt/ExecutionEpoch binding.
- General substrate-level forbidden-access proof after activation.
- Controller-loss reconciliation for OpenCode-owned execution.
- Duplicate-start fencing after controller loss.
- Orphan detection and safe stale resource reclaim.
- Independent semantic verification beyond this Core artifact verifier.
- Checkpoint side-effect safety.
