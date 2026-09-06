# Attempt Identity and Reconciliation Hardening 0002

Status: `PROPOSED` implementation evidence. This record documents bounded
single-controller behavior; it does not upgrade general runtime authority or
distributed lease guarantees.

## Implemented boundary

The Core ledger now persists and reloads:

- Execution/Task/Attempt identity relations;
- one immutable ExecutionManifest relation per Attempt;
- ExecutionEpoch, AuthorityRevision, and RuntimeLane references;
- runtime-native session identity;
- barrier state;
- a durable per-Attempt start fence;
- exclusive workspace/resource claims;
- results, artifacts, and typed lifecycle/reconciliation events.

The fence is acquired before barrier release. A second claim for the same
Attempt is rejected after reload; retry remains a new Attempt concern. A stale
fence or claim is not reclaimed automatically.

The Core Reconciliation Loop consumes runtime facts and durable identity. It
does not adopt runtime identities, start work, or assign semantic success from
adapter facts. It emits safe classifications including `RECOVERY_REQUIRED`,
`LOST`, `VERIFYING`, and `UNKNOWN`, while orphan observations are quarantined.

## Reconciliation rules

| Runtime observation | Identity/result condition | Core disposition |
| --- | --- | --- |
| `RUNNING` | expected identity | `RECOVERY_REQUIRED`; no restart |
| `EXITED` | persisted artifact/result integrity verifies | `SUCCEEDED` |
| `EXITED` | verification evidence absent or invalid | `VERIFYING` |
| `MISSING` | expected identity | `LOST` |
| `UNREACHABLE` | controller/runtime transport unavailable | `RECOVERY_REQUIRED` |
| `MISMATCH` | observed identity differs or relations are corrupt | `RECOVERY_REQUIRED`; no reassociation |
| `UNKNOWN` | insufficient evidence | `RECOVERY_REQUIRED`; fence retained |
| unknown Attempt/session observation | no durable owner | `ORPHAN_QUARANTINED` |

Persisted success after restart is accepted only when Core independently finds
the expected artifact, matches its digest, and finds a persisted verification
pass for the same Attempt. An adapter-provided success flag is not sufficient.

## Test evidence

The standard-library test suite passed 14 tests covering:

- Attempt identity persistence/reload;
- immutable Manifest mutation rejection;
- durable duplicate-start fence rejection;
- runtime identity mismatch without reassociation;
- `MISSING` and `UNREACHABLE` recovery classification;
- completed runtime without verified artifact;
- verified artifact after ledger reload;
- orphan runtime quarantine;
- controller restart with no observation;
- exclusive workspace claim conflict;
- stale claim fail-closed behavior;
- corrupt immutable relation rejection;
- Core artifact verification;
- runtime completion versus semantic success.

## Real OpenCode restart smoke

Command:

```sh
PYTHONPATH=. python3 -B experiments/runtime-proof/reconciliation_restart_smoke.py
```

Environment: `/usr/local/bin/opencode`, version `1.18.25`, disposable
workspace/config/data/cache/state directories, no credentials or secret
contents. OpenCode created session
`ses_f86d717abffec7o77z0QmKVD2z`.

Observed:

- first controller health: true;
- controller transport during stop: `UNREACHABLE`;
- second controller health: true;
- session retrieval after restart: HTTP `200`;
- Core runtime fact: `UNKNOWN`;
- Core semantic state: `RECOVERY_REQUIRED`;
- disposition: `UNKNOWN_FAIL_CLOSED`;
- duplicate start allowed: false.

The session record surviving restart is not treated as proof that an active
runtime exists. This is the intended fail-closed behavior for the current
OpenCode boundary.

## Safety and proof limits

The implementation preserves:

- `Task != Attempt`;
- retry creates a new Attempt;
- runtime-native session IDs remain adapter-specific;
- Runtime Adapter facts remain external observations;
- runtime completion `!=` semantic success;
- Core owns semantic state and authority meaning;
- DPT and Orchestration remain optional;
- exact AuthorityRevision activation/binding remains `NOT_PROVEN`;
- controller-loss reconciliation remains bounded and not generally proven;
- stale ResourceLease reclamation remains `NOT_PROVEN`;
- independent semantic verification remains limited to the bounded artifact
  verifier.

The single-controller JSON lock/fence is not a distributed scheduler or a
general ResourceLease implementation. Recovery remains fail-closed whenever
authority, identity, runtime, artifact, or resource evidence is incomplete.
