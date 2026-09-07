# Runtime Adapter Contract 0001

Status: `PROPOSED` implementation evidence. This record documents a small,
substrate-neutral contract used by the bounded slice; it does not freeze a
permanent Runtime Adapter API or upgrade any authority guarantee.

## Contract boundary

`apex_code/contract.py` defines the minimum adapter-facing types:

- `RuntimeFact`: `RUNNING`, `EXITED`, `MISSING`, `UNREACHABLE`, `MISMATCH`,
  and `UNKNOWN`;
- `RuntimeIdentity`: opaque runtime-native session/process/adapter identity;
- `RuntimePreparation`: immutable preparation identity, authority digest,
  configuration location, and preparation mode;
- `RuntimeExecution`: immutable runtime identity, substrate fact, exit/result
  data, event count, preparation identity, authority digest, and redacted
  command shape;
- `RuntimeAdapter`: a structural protocol for authority preparation and
  execution.

Core consumes this contract and interprets its facts. The contract contains no
Apex semantic Task success/failure assignment and no authority decision. A
preparation object is passed from materialization to execution so Core can
reject a result correlated with a different preparation or authority digest.

`apex_code/core.py` no longer imports or constructs the OpenCode adapter. The
CLI composes `OpenCodeRuntimeAdapter` at the application boundary. This keeps
the bounded Core path substrate-neutral while retaining OpenCode as the first
runtime implementation.

## Verification

The standard-library suite passed 15 tests, including a focused regression
where an adapter returns a different preparation identity. Core raises a
`SafetyError` before accepting or writing an artifact. Existing tests continue
to cover immutable manifests, fencing, reconciliation, resource conflicts,
identity mismatch, artifact verification, and runtime completion versus
semantic success.

The real bounded slice was run against one isolated temporary workspace:

| Field | Observation |
| --- | --- |
| Executable | `/usr/local/bin/opencode` |
| Version | `1.18.25` |
| Model | `opencode/big-pickle` |
| Execution | `exec_4aaf00abb0864e7a` |
| Core Task | `task_863697ec2d964b82` |
| Attempt | `att_6ea1b09fe01041fe` |
| ExecutionManifest | `manifest_35f06c043b6d438c` |
| Runtime session | `ses_f86ce299bffedbcGUtEu76uZDp` |
| Runtime fact | `EXITED` |
| Core verification | `PASS` |
| Semantic success | `true` |
| Artifacts | `REPORT.md`, `execution-ledger.json` |

The command was:

```text
PYTHONPATH=. python3 -B -m apex_code.cli <isolated-workspace> --opencode /usr/local/bin/opencode --model opencode/big-pickle
```

## Limits preserved

This contract does not prove:

- exact OpenCode authority activation or AuthorityRevision-to-runtime binding;
- controller-loss reconciliation beyond the existing bounded Core behavior;
- distributed or multi-controller fencing;
- stale ResourceLease reclamation;
- independent semantic verification beyond the bounded Core artifact verifier;
- checkpoint side-effect safety.

The adapter reports `EXITED` as a substrate fact. Core still requires a
verified artifact before semantic success, so runtime completion remains
distinct from semantic Task success. DPT and Orchestration remain optional,
and no external runtime dependency was added.

## Validation

Executed successfully:

```text
python3 -B -m unittest discover -s tests -v
python3 scripts/validate_docs.py
git diff --check
```
