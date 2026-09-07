# Bounded Artifact Task 0001

Status: `PROPOSED` implementation evidence. This record documents a reusable
bounded Core path; it is not a new orchestration primitive or a general task
scheduler.

## Reusable path

`apex_code/core.py` now uses an internal `ArtifactTaskSpec` to parameterize the
safe slice's single-input/single-output shape. `run_report()` preserves the
original `README.md → REPORT.md` reference task, while `run_summary()` exercises
the same pipeline with `README.md → SUMMARY.md`.

Both shapes use the same:

- `ExecutionRequest → Execution → Core Task → Attempt` records;
- immutable per-Attempt `ExecutionManifest`;
- bounded `PermissionEnvelope` and Core-owned path checks;
- durable start fence and event ledger;
- typed Runtime Adapter preparation/execution contract;
- runtime-fact interpretation in Core; and
- exact artifact write/readback verification before semantic success.

The specification accepts only workspace-root file names, requires distinct
input and output files, and derives a distinct authority revision identity for
each bounded shape. It does not grant arbitrary file access or turn task
parameters into a public scheduler/API.

## Validation

The standard-library suite passed 18 tests. The added regression runs the
second `SUMMARY.md` shape through a fake adapter and confirms that the
original `REPORT.md` path is not created. Existing tests continue to cover
fencing, reconciliation, resource conflicts, identity checks, artifact
verification, and runtime completion versus semantic success.

The real OpenCode adapter also completed the second shape in an isolated
temporary workspace using `/usr/local/bin/opencode` version `1.18.25` and
model `opencode/big-pickle`:

| Field | Observation |
| --- | --- |
| Execution | `exec_7f3384c2bd024b02` |
| Core Task | `task_e4315642cdf144cd` |
| Attempt | `att_261ae35afa474e52` |
| ExecutionManifest | `manifest_47b09d051ff44c81` |
| Runtime session | `ses_f86c663d3ffev2eaUcSXAUdTmf` |
| Runtime fact | `EXITED` |
| Core verification | `PASS` |
| Semantic success | `true` |
| Artifact | `SUMMARY.md` |

`REPORT.md` was absent in that workspace, confirming the selected output
contract was applied.

The CLI now exposes the same bounded choices with `--task report|summary`;
`report` remains the default. A focused CLI test verifies selection without
coupling the entry point to a concrete adapter implementation.

Documentation validation and `git diff --check` passed. No Runtime Adapter,
authority, event, architecture status, dependency, DPT, or Orchestration
guarantee was upgraded by this task.
