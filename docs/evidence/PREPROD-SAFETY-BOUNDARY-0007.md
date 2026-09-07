# Bounded Production Safety Boundary — 0007

Status: `PROPOSED` release-boundary evidence. This report documents the
current bounded profile; it does not change frozen contract meaning or claim
unproven substrate guarantees.

## Executive result

`BOUNDED_CORE_MEDIATED_MVP` is safe to describe as a bounded release profile
for the current single-controller artifact path, with explicit refusals around
uncertain runtime ownership and direct runtime I/O.

The decisive boundary is that Core performs the only repository fixture read
and artifact write. The runtime receives bounded prompt content, runs with a
minimal child environment and deny-all OpenCode I/O configuration, and returns
substrate facts/raw output. Core owns the barrier, durable identity, workspace
claim, artifact verification, and semantic result.

Therefore:

1. Exact substrate-native `AuthorityRevision` activation/binding can remain
   `NOT_PROVEN` without blocking this profile because the profile does not rely
   on runtime-native repository authority.
2. Active-runtime reattachment can remain `NOT_PROVEN` while controller loss
   is production-safe for this profile by refusing uncertain adoption and
   retaining durable fences/claims.
3. Stale lease reclamation can remain `NOT_PROVEN` while uncertain claims are
   never silently reused.

Release boundary: `YES_WITH_BOUNDED_RELEASE_PROFILE`.

## 1. Authority dependency trace

| Side effect | Owner | Authority source | Runtime repository I/O? | Exact substrate attestation required? | Fail-closed boundary |
| --- | --- | --- | --- | --- | --- |
| Read `README.md` fixture | Core `ExecutionCoordinator._safe_path` | immutable bounded `PermissionEnvelope` / `AuthorityRevision` | No | No | exact input name, workspace root, symlink/path checks |
| Invoke provider/runtime process | Runtime Adapter after Core barrier | Core `ExecutionBarrier` and durable fence | Process runs, but no repository tool authority is relied upon | No for this profile | materialization/digest/identity mismatch rejects before/after execution |
| Runtime filesystem/tool access | No permitted owner in bounded mode | deny-all OpenCode config; Core-mediated mode | Forbidden | Native activation proof not relied upon | runtime is not used for repository mutation; native/direct mode is excluded |
| Write `REPORT.md`/`SUMMARY.md` | Core after result extraction | bounded output contract and workspace claim | No | No | exact output path, regular-file/symlink check, Core verifier |
| Workspace reservation | Core ledger `ResourceClaim` | Attempt/Manifest relation | No | No | conflicting or uncertain held claim blocks reuse |
| Provider request | adapter/provider | configured provider credential outside Apex authority model | External inference only | No repository-authority proof | no credentials inherited by OpenCode child; result still untrusted until Core verification |
| Result collection | Runtime Adapter | preparation ID and authority digest correlation | No | No | wrong preparation/digest or unknown fact fails closed |

The bounded path is not a general permission sandbox. It is a Core-mediated
mode that avoids making substrate-native authority enforcement a safety
dependency.

## 2. Authority mode hardening

The OpenCode adapter now constructs a minimal child environment rather than
copying the controller environment. It supplies only stable process basics,
isolated `HOME`, isolated XDG roots, and the explicit OpenCode configuration.
Ambient provider keys, user configuration, and unrelated repository
environment are not inherited by the worker.

Focused tests and a clean-environment OpenCode smoke establish:

- isolated child `HOME` and config roots;
- no `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or AWS secret variable in the
  constructed environment;
- deny-all runtime configuration remains in force;
- traversal and symlink escapes are denied;
- authority digest, preparation, Attempt, and RuntimeLane mismatches fail
  closed;
- unexpected/unverified output cannot become semantic success;
- failed/unverified exit retains the workspace claim.

This is `BOUNDED_CORE_MEDIATED_AUTHORITY = PROVEN` for the stated artifact
profile, based on `SOURCE_CODE_EVIDENCE`, `DOCUMENTATION_EVIDENCE`, and
`OBSERVED_RUNTIME_EVIDENCE`. It is not proof of native runtime authority
activation.

## 3. Native runtime I/O boundary

The bounded profile excludes any mode in which an agent/runtime directly:

- edits repository files;
- runs arbitrary project commands;
- accesses a broader filesystem;
- performs unrestricted network/tool actions; or
- expands authority through plugins or inherited configuration.

For such a future direct-I/O mode, the complete sequence remains:

```text
PermissionEnvelope
→ AuthorityRevision
→ materialization
→ activation verification
→ exact RuntimeLane binding
→ exact Attempt / ExecutionEpoch binding
→ Execution Barrier
→ START
```

Native runtime authority activation and exact binding remain `NOT_PROVEN` and
must not inherit approval from this bounded profile.

## 4. Controller-loss policy

The current `ReconciliationLoop` consumes durable ledger state and adapter
facts. It never adopts a runtime, starts work, or assigns semantic success from
an external fact.

| Scenario | Observed fact | Core classification | Task state | Attempt state | Claim state | Reattach? | Retry? | Human/recovery action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| D1 runtime disappears with controller | `MISSING` or no observation → `UNKNOWN` | `LOST` or `RECOVERY_REQUIRED` | not successful | non-terminal uncertainty retained | `HELD` | No | No same Attempt | required |
| D2 durable session remains, process unproven | `UNKNOWN` | `RECOVERY_REQUIRED` | not successful | fence remains | `HELD` | No | No same Attempt | required |
| D3 identity cannot be correlated | `MISMATCH` | `RECOVERY_REQUIRED` | not successful | immutable identity unchanged | `HELD` | No | No same Attempt | required |
| D4 terminal result and exact artifact evidence correlate | `EXITED` | `VERIFYING` then `SUCCEEDED` only after Core verification | `SUCCEEDED` | terminal only after verification | released after success | Not a reattach | New retry unnecessary | no, if all checks pass |
| D5 duplicate start after restart | durable fence exists | `DuplicateStart` rejection | unchanged | original Attempt preserved | held/quarantined | No | New Attempt only after explicit resolution | required if uncertain |
| D6 wrong/stale runtime identity | `MISMATCH` | `RECOVERY_REQUIRED` | not successful | no reassociation | held | No | No same Attempt | required |
| D7 uncertain workspace claim | held claim | conflict/fail closed | no new success | prior Attempt remains unresolved | `HELD` | No | No reuse | explicit recovery/admin action |

`RUNNING` observations also remain `RECOVERY_REQUIRED`; a visible live runtime
does not prove complete Apex identity correlation. The real OpenCode restart
smoke below observed this policy.

## 5. Terminal-result reconciliation

An `EXITED` runtime may reach semantic success only when Core can correlate:

- the original Attempt and immutable Manifest;
- the expected preparation and authority digest;
- the expected artifact path;
- artifact integrity and exact content;
- persisted Core verification for the same Attempt; and
- no identity mismatch or duplicate semantic completion.

An exit code, session record, transcript, or provider self-report alone is not
sufficient.

## 6. Duplicate, retry, and claim safety

- A durable per-Attempt fence rejects a second start after ledger reload.
- A retry is a new Attempt; an old Attempt is never mutated into a retry.
- Old result/artifact evidence is keyed to its original Attempt and cannot
  complete a different Attempt.
- An exclusive workspace claim rejects overlap.
- Unknown, missing, unreachable, mismatched, or unverified work does not
  release its claim automatically.
- Only verified semantic success releases the bounded claim automatically.
- General stale lease reclamation is not implemented; uncertain claims require
  explicit recovery/admin resolution.

## 7. Real OpenCode controller-loss smoke

Command, run with a sanitized environment and disposable workspace:

```sh
PYTHONPATH=. python3 -B experiments/runtime-proof/reconciliation_restart_smoke.py
```

Observed result:

| Observation | Result |
| --- | --- |
| OpenCode executable/version | `/usr/local/bin/opencode`, `1.18.25` |
| first controller | healthy |
| controller loss | transport became unreachable |
| restarted controller | healthy |
| session retrieval after restart | HTTP `200` |
| Apex runtime fact | `UNKNOWN` |
| Apex semantic state | `RECOVERY_REQUIRED` |
| disposition | `UNKNOWN_FAIL_CLOSED` |
| duplicate start | rejected/not allowed |
| secrets read or printed | no |

The persisted OpenCode session was deliberately not treated as proof of an
active runtime or safe reassociation.

Classification: `CONTROLLER_LOSS_FAIL_CLOSED_RECOVERY = PROVEN` for the
bounded policy of refusing uncertain adoption. `ACTIVE_RUNTIME_REATTACHMENT =
NOT_PROVEN`.

## 8. Bounded MVP release contract

### Guarantees

- single-controller execution only;
- one bounded Attempt at a time per claimed workspace;
- durable Attempt/Manifest/Lane identity and start fencing;
- Core-mediated fixture read and artifact write;
- minimal runtime child environment and no ambient credential/config
  inheritance in the OpenCode adapter;
- Core-owned semantic completion;
- exact bounded artifact verification before success;
- typed runtime facts and durable ledger evidence;
- mismatch, unknown, missing, unreachable, and uncertain claims fail closed;
- retry requires a new Attempt;
- optional runtime failure cannot silently become Task success.

### Does not guarantee

- substrate-native AuthorityRevision activation or binding;
- direct runtime-I/O authority safety;
- active-runtime controller-loss reattachment;
- distributed or multi-controller fencing;
- automatic stale lease reclamation;
- checkpoint/resume side-effect safety;
- general semantic verification;
- global event ordering.

### Must refuse

- direct runtime-I/O execution under this profile;
- reattachment when exact identity correlation is absent or mismatched;
- duplicate start of an unresolved Attempt;
- workspace reuse while an uncertain exclusive claim remains held;
- semantic success from runtime exit, transcript, session presence, or agent
  self-report alone;
- authority expansion or credential/config inheritance that is not explicitly
  bounded and verified.

## 9. Mission success questions

1. Exact substrate authority activation can remain `NOT_PROVEN`: **YES**.
2. Active-runtime reattachment can remain `NOT_PROVEN` with fail-closed
   controller-loss handling: **YES**.
3. Stale lease reclamation can remain `NOT_PROVEN` when uncertain claims are
   never silently reused: **YES**.
4. Apex can proceed into MVP product development under this profile:
   **YES_WITH_BOUNDED_RELEASE_PROFILE**.

## 10. NOT_PROVEN re-triage

| Item | Classification |
| --- | --- |
| Exact substrate AuthorityRevision activation/binding | `NON_BLOCKING_WITH_FAIL_CLOSED_BOUNDARY` for this Core-mediated MVP; `PRE_PRODUCTION_BLOCKER` for direct runtime-I/O mode |
| Active-runtime reattachment | `NON_BLOCKING_WITH_FAIL_CLOSED_BOUNDARY` for this MVP; `PRE_PRODUCTION_BLOCKER` for production reattachment |
| Stale ResourceLease reclamation | `NON_BLOCKING_WITH_FAIL_CLOSED_BOUNDARY` |
| Checkpoint side-effect safety | `ADVANCED_CAPABILITY_BLOCKER` |
| Distributed fencing | `DISTRIBUTED_FUTURE` |
| Global event ordering | `DISTRIBUTED_FUTURE` |
| General semantic verification | `ADVANCED_CAPABILITY_BLOCKER` |

## 11. Related evidence

- [Attempt reconciliation hardening](ATTEMPT-RECONCILIATION-HARDENING-0002.md)
- [OpenCode authority proof](OPENCODE-AUTHORITY-ATTESTATION-PROOF-0001.md)
- [Architecture status](../architecture/05-ARCHITECTURE-STATUS.md)
- [Runtime Adapter contract](RUNTIME-ADAPTER-CONTRACT-0001.md)
