# Runtime Authority and Recovery Proof 0001

Status: `PROPOSED` evidence report for Owner review
Evidence date: 2026-09-06 UTC / 2026-09-07 Asia/Tehran
Scope: disposable runtime experiments only; no Apex product or architecture implementation

## 1. Executive result

| Experiment | Result | Meaning |
| --- | --- | --- |
| E1 — exact authority activation and binding | `NOT_PROVEN` | Materialization and OpenCode session identity were observed, but exact active-authority proof and binding to an Apex Attempt/ExecutionEpoch were not exposed. |
| E2 — controller loss and reconciliation | `NOT_PROVEN` | OpenCode session persistence and transport/identity facts were observable, but a durable controller-independent Attempt reconciliation contract was not. |
| E3 — resource ownership | `PARTIAL_PRIMITIVE` | Atomic local directory reservation was observed; stable owner identity, safe stale reclaim, and Apex ResourceLease semantics were not. |
| E4 — checkpoint side-effect safety | `DEFERRED_NOT_APPLICABLE_TO_CURRENT_SUBSTRATE` | No meaningful OpenCode checkpoint/resume contract for external side effects was exposed at the inspected boundary. |

The experiments support a conservative adapter boundary: a runtime can report
substrate facts, while Apex Core must retain semantic execution, authority,
resource, verification, and recovery decisions. No result upgrades the existing
`NOT_PROVEN` authority-binding or controller-loss status.

## 2. Environment and snapshot

### OpenCode source snapshot

- Repository: `anomalyco/opencode`
- Source URL: <https://github.com/anomalyco/opencode>
- Source checkout: `/tmp/apex-comparative-harvest.Wob1Ep/opencode`
- Ref state: detached checkout; exact inspected source SHA:
  `e207624c48159b03dbe17dbc8e51bbcf23e72df5`
- Relevant source paths inspected:
  - `packages/core/src/v1/config/permission.ts`
  - `packages/core/src/permission.ts`
  - `packages/core/src/global.ts`
  - `packages/server/src/handlers/session.ts`
  - `packages/server/src/handlers/permission.ts`
  - `packages/server/src/handlers/event.ts`
  - `packages/sdk/openapi.json`
- License/reuse boundary: not used as source code; this experiment only
  exercised the separately installed executable.

### Executable and run snapshot

- Executable: `/usr/local/bin/opencode`
- Reported version: `1.18.25`
- The installed executable was not treated as byte-for-byte identical to the
  pinned source checkout; that relationship is `NOT_PROVEN`.
- Workspace: disposable temporary directory, not the Apex repository.
- Configuration root: disposable temporary directory under the run's temp root.
- Run interval: `2026-09-06T23:31:31.211751+00:00` to
  `2026-09-06T23:31:47.691327+00:00`.
- No credentials, secret files, private keys, or secret contents were read or
  printed.

### Experimental identity ledger

The harness wrote a local disposable ledger before starting the server:

| Identity | Value |
| --- | --- |
| Attempt | `attempt-runtime-proof-001` |
| RuntimeLane | `lane-runtime-proof-001` |
| ExecutionEpoch | `epoch-runtime-proof-001` |
| AuthorityRevision | `ar-runtime-proof-001` |
| Authority state digest | `e092e0f1fbefff0e81e7494c55b4a7d48efb6c52aea133c424b6311561710186` |
| OpenCode session | `ses_f86efe162ffe4EZZvZ3qt30KyA` |
| First server process | `63486` |
| First observed server port | `59545` |

These identifiers were created by the experiment. Their existence does not
prove that OpenCode accepted or enforced Apex meanings for them.

## 3. Experiment architecture

The harness at
[`experiments/runtime-proof/authority_recovery_harness.py`](../../experiments/runtime-proof/authority_recovery_harness.py)
is disposable research tooling. It uses only the Python standard library,
starts OpenCode with `serve --pure` in an isolated temporary workspace, and
uses harmless subprocess fixtures for controller-loss/resource observations.
It is not a Runtime Adapter, authority engine, scheduler, reconciliation
implementation, or production package.

The test workspace contained only harmless sentinels:

- `allowed/read.txt`
- `output/`
- `forbidden/read.txt`

The authority profile allowed the first two categories and denied the
forbidden/outside-workspace categories. Configuration was materialized before
the OpenCode session was created. No model-backed agent prompt or tool action
was run, so permission behavior in an actual OpenCode tool call was not
claimed.

## 4. E1 — Exact authority activation and binding

### E1-A — Materialization before execution

Observed (`OBSERVED_RUNTIME_EVIDENCE`):

1. The disposable `authority-revision-001.json` was written and hashed.
2. OpenCode configuration was written under the disposable configuration root.
3. The OpenCode server became healthy.
4. A session was created only after those writes.

The harness intentionally did not start a runtime fixture before its local
pre-start check. This proves ordering in the harness, not an atomic OpenCode
authority barrier.

Result: `CONFIG_WRITTEN`; `AUTHORITY_ACTIVE_CONFIRMED` was not established.

### E1-B — Activation verification

Source inspection (`SOURCE_CODE_EVIDENCE`) and runtime observation found:

- `/global/health` returned `{"healthy":true,"version":"1.18.25"}`.
- The session API returned a machine-readable OpenCode session identifier.
- The inspected permission configuration/API exposed permission rules and
  permission request/reply surfaces.
- No inspected endpoint or response directly attested that the exact
  `ar-runtime-proof-001` revision was the active authority for a particular
  runtime lane and Attempt.

Result: `AUTHORITY_ACTIVE_CONFIRMED = NOT_OBSERVED`.

### E1-C — Identity binding

The experiment recorded an Apex-shaped ledger containing Attempt, Lane, Epoch,
AuthorityRevision, and manifest digest before session creation. OpenCode
returned `ses_f86efe162ffe4EZZvZ3qt30KyA`, and its session could be retrieved
after server restart. No OpenCode response or event correlated that session to
the ledger's Attempt, Epoch, or AuthorityRevision.

Result: exact immutable binding is `NOT_PROVEN`.

### E1-D — Negative access

The harmless workspace was prepared for permitted-read, permitted-write,
forbidden-read, and forbidden-write checks. Permitted read and write were
confirmed as ordinary filesystem fixture operations. Forbidden operations were
not attempted because activation was not verified; doing so would not have
converted a filesystem result into exact authority-binding proof.

Result: substrate-enforced negative access after verified activation is
`NOT_PROVEN`.

### E1-E — Authority drift

No verified active-authority signal was available against which a subsequent
revision could be compared. An old-versus-new active authority test was
therefore not promoted to a result.

Result: `NOT_PROVEN`.

### E1-F — Pre-start barrier

The harness blocked its own runtime fixture before activation confirmation. No
OpenCode API was found that atomically enforced the complete Apex sequence:

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

Result: the Apex required barrier remains a design invariant, but substrate
enforcement/proof is `NOT_PROVEN`.

### E1 classification

`NOT_PROVEN`

## 5. E2 — Controller loss and reconciliation

The controller in these scenarios was the disposable OpenCode server. The
long-running processes were explicitly harmless external fixtures, not
OpenCode-managed agent executions. This distinction prevents fixture behavior
from being misreported as OpenCode recovery behavior.

### E2-A — Controller dies while runtime remains

Observed (`OBSERVED_RUNTIME_EVIDENCE`):

- OpenCode server was stopped while the fixture process remained alive.
- The fixture was still alive after controller loss: normalized fact `RUNNING`.
- OpenCode restarted healthy on a new local port.
- The prior OpenCode session was retrievable after restart: HTTP `200`.

Safe Apex interpretation: controller restart plus session persistence is not
enough to declare the Attempt running or safe to resume. The conservative
semantic classification is `RECOVERY_REQUIRED`.

### E2-B — Runtime dies while controller is absent

- Controller was stopped.
- The fixture process was terminated while the controller was absent.
- On controller restart, no completion marker existed.

Normalized runtime fact: `MISSING`. Safe semantic classification:
`RECOVERY_REQUIRED`. No durable Apex reconciliation decision was inferred.

### E2-C — Runtime completes while controller is absent

- Controller was stopped.
- The fixture exited and wrote a harmless completion marker.
- Controller restart was healthy.
- Result-marker availability was observed.

Normalized runtime fact: `EXITED`. The harness deliberately reported
`semanticSuccess = NOT_INFERRED`; process completion and result availability do
not replace result collection, independent verification, acceptance, or Core
Task semantics.

### E2-D — Runtime unreachable

An HTTP health request while the OpenCode controller was stopped failed at the
transport layer and was normalized as `UNREACHABLE`. This is a transport fact,
not a Task failure.

### E2-E — Identity mismatch

A request using the intentionally wrong session identity returned HTTP `404`.
This was normalized as `MISMATCH` / safe failure rather than silently attaching
the Attempt to another session.

This demonstrates an API identity error response, not exact Apex
Attempt/Lane/Epoch binding.

### E2-F — Duplicate-start prevention

Two harmless fixtures were intentionally started with the same experimental
Attempt identifier while the controller lifecycle was being exercised. Both
were alive concurrently. The OpenCode session API did not provide a durable
Apex Attempt admission or duplicate-start mechanism for this scenario.

Normalized safe classification: `UNKNOWN`. Duplicate-start prevention is
`NOT_PROVEN`.

### E2-G — Orphan detection

A fixture was started without a corresponding ledger entry. The harness could
flag that local discrepancy, but no OpenCode substrate orphan-detection signal
was observed.

Normalized safe classification: `UNKNOWN`. Substrate orphan detection is
`NOT_OBSERVED`.

### E2 classification

`NOT_PROVEN`

## 6. E3 — Minimal resource ownership probe

This probe did not implement `ResourceClaim` or `ResourceLease`. Two local
processes raced to create one shared directory using the operating system's
atomic directory-creation operation.

| Question | Observation |
| --- | --- |
| Is substrate reservation available? | Yes, a local directory reservation was available. |
| Is reservation durable across controller restart? | The reservation path persisted. |
| Does it have stable identity? | No stable owner identity was observed; the path alone is insufficient. |
| Can stale ownership be detected? | Only `PATH_EXISTS_ONLY`; no owner/liveness proof. |
| Can stale ownership be reclaimed safely? | `NOT_PROVEN`. |
| Is exclusive ownership atomic? | Yes for this local directory-creation race: one `WON`, one `LOST`. |
| Is this local-process only? | Yes. |

Classification: `PARTIAL_PRIMITIVE`.

The result supports retaining/refining the Apex `ResourceClaim` /
`ResourceLease` concept as a Core semantic boundary, but does not promote this
filesystem primitive into an Apex lease.

## 7. Optional E4 — Checkpoint side-effect safety

Classification: `DEFERRED_NOT_APPLICABLE_TO_CURRENT_SUBSTRATE`.

At the inspected OpenCode source/API boundary, no meaningful checkpoint/resume
contract for external side effects was identified. LangGraph or another
framework was not introduced merely to run this experiment. A later experiment
may be designed if the selected Runtime Adapter exposes a concrete checkpoint
mechanism.

## 8. Raw observation summary

| Observation | Direct result | Evidence label |
| --- | --- | --- |
| OpenCode health | HTTP `200`, healthy, version `1.18.25` | `OBSERVED_RUNTIME_EVIDENCE` |
| Session creation | HTTP `200`, session `ses_f86efe162ffe4EZZvZ3qt30KyA` | `OBSERVED_RUNTIME_EVIDENCE` |
| Session after controller restart | HTTP `200` | `OBSERVED_RUNTIME_EVIDENCE` |
| Controller transport loss | health request failed | `OBSERVED_RUNTIME_EVIDENCE` |
| Wrong session identity | HTTP `404` | `OBSERVED_RUNTIME_EVIDENCE` |
| Authority file | written before server/session start; digest recorded | `OBSERVED_RUNTIME_EVIDENCE` |
| Active authority attestation | not exposed/observed | `NOT_PROVEN` |
| Exact Attempt/Epoch binding | not exposed/observed | `NOT_PROVEN` |
| Runtime alive through controller loss | fixture remained alive | `OBSERVED_RUNTIME_EVIDENCE` |
| Runtime completion through controller loss | marker available, success withheld | `OBSERVED_RUNTIME_EVIDENCE` |
| Atomic local reservation | one winner, one loser | `OBSERVED_RUNTIME_EVIDENCE` |
| Safe stale reclaim | no evidence | `NOT_PROVEN` |

## 9. Proven and partially proven facts

### Proven within the experiment boundary

- The installed OpenCode executable can serve a disposable workspace and expose
  a machine-readable health endpoint.
- OpenCode can create a session with a machine-readable session ID.
- The session record remained retrievable after restarting the disposable
  OpenCode controller.
- A stopped controller is distinguishable from a reachable controller at the
  HTTP transport boundary (`UNREACHABLE`).
- An intentionally wrong session identifier received an explicit not-found
  response, normalized as `MISMATCH`.
- Atomic local directory creation can provide a single winner in a local race.
- A runtime/process completion marker can remain available while the controller
  is absent, without justifying semantic success.

### Partially proven / bounded facts

- Session persistence is useful substrate behavior, but it is not a durable
  Apex execution ledger or reconciliation guarantee.
- Local filesystem reservation is a useful substrate primitive, but it is not a
  durable identity-bearing Apex ResourceLease.
- The harness can enforce a pre-start check in itself, but this does not prove
  an OpenCode atomic authority barrier.

## 10. NOT_PROVEN facts

- Exact `AuthorityRevision` active for the exact RuntimeLane.
- Exact `AuthorityRevision` bound to the exact Attempt and ExecutionEpoch.
- Atomic activation verification before substrate execution.
- Authority drift detection without trusting agent self-report.
- Substrate-enforced forbidden access after verified authority activation.
- Duplicate-start prevention surviving controller loss.
- Safe reconciliation of stale `RUNNING` Attempts.
- Controller-independent detection of orphaned RuntimeLanes.
- Distinguishing all of `RUNNING`, `EXITED`, `MISSING`, `UNREACHABLE`,
  `MISMATCH`, and `UNKNOWN` for OpenCode-owned execution contexts.
- Process-loss reconciliation and safe resume/reconnect semantics.
- Safe stale resource reclaim or renewable lease semantics.
- Independent semantic verification implementation.
- Checkpoint side-effect safety.
- Equivalence of the installed executable and the pinned source checkout.

## 11. Failed assumptions and unsafe inferences avoided

- `CONFIG_WRITTEN` was not treated as `AUTHORITY_ACTIVE_CONFIRMED`.
- A session ID was not treated as an Apex Attempt identity.
- Session persistence was not treated as an execution ledger.
- A process exit or completion marker was not treated as semantic Task success.
- A transport error was not treated as a semantic Task failure.
- A local lock directory was not treated as `ResourceLease`.
- The harness's barrier was not treated as OpenCode's atomic enforcement.
- No forbidden content was read or printed.

## 12. Runtime Adapter implications

The adapter boundary should report typed substrate facts and identifiers, not
assign Apex semantic Task success/failure. Candidate normalized facts remain:

```text
RUNNING
EXITED
MISSING
UNREACHABLE
MISMATCH
UNKNOWN
```

An adapter should expose enough correlation data for Core to decide whether a
fact belongs to the expected RuntimeLane/session, but this experiment did not
establish the exact v1 contract. Runtime Adapter v1 remains
`FREEZE_CANDIDATE`; exact fact mapping requires further design and
experimentation.

## 13. Core Reconciliation implications

The results support the existing Core-owned Reconciliation Loop concept:

```text
durable Attempt state
+ Runtime Adapter observed facts
+ Authority state
+ Resource ownership
→ semantic execution state
```

After controller restart, Core should prefer safe classifications such as
`RECOVERY_REQUIRED` or `UNKNOWN` when identity, authority, resource, or result
facts cannot be established. It must not automatically resume or start a
duplicate Attempt merely because a session exists or a controller is healthy.

The implementation guarantee for controller-loss reconciliation remains
`NOT_PROVEN`.

## 14. Authority implications

The required Apex sequence remains unchanged:

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

The experiment strengthens the reason for separating configuration
materialization from activation proof. It does not prove any missing link in
that sequence, and it does not change the current `NOT_PROVEN` status.

## 15. ResourceClaim / ResourceLease implications

The local atomic reservation is useful evidence for an adapter/control-plane
primitive, but it lacks owner identity, lease renewal, controller-loss
reconciliation, and safe stale reclamation. Core should continue to own the
semantic conflict meaning while substrate/control-plane components may
materialize reservations. The complete Apex semantics remain
`FREEZE_CANDIDATE` / `NOT_PROVEN` as applicable.

## 16. Architecture changes unlocked

None by this evidence-only delta. The following existing directions are
supported for later Owner reconciliation, not silently frozen here:

- typed Runtime Adapter facts;
- Core-owned Reconciliation Loop;
- explicit ResourceClaim / ResourceLease boundary;
- authority activation and binding as a pre-start barrier;
- separate runtime completion, verification, acceptance, and semantic success.

## 17. Architecture changes still blocked

No Runtime Adapter v1 freeze should rely on this run alone. In particular,
exact authority binding, controller-loss reconciliation, duplicate-start
prevention, stale lease reclamation, checkpoint side-effect safety, and
independent semantic verification remain blocked by missing direct evidence.

## 18. Recommended next experiments

These are proposals only; they were not executed here:

1. Add a controlled OpenCode tool action with a substrate-observable,
   non-secret permission request and determine whether the resulting event or
   response can be correlated to a pre-materialized authority digest.
2. Introduce an explicit adapter-side durable identity registry in a disposable
   harness and test crash/restart fencing against duplicate starts.
3. Test a concrete runtime/session reconnect path with a stable runtime identity
   and intentionally stale identity.
4. Compare two independent adapter substrates using the same typed-fact
   contract.
5. Test checkpoint continuation only when the selected substrate exposes a
   concrete checkpoint and side-effect model.

## 19. Reproducibility instructions

From the Apex Code repository, with OpenCode `1.18.25` available:

```sh
python3 -B experiments/runtime-proof/authority_recovery_harness.py \
  --opencode /usr/local/bin/opencode
```

The harness creates and removes no files in the Apex workspace; its workspace,
configuration, ledger, runtime fixtures, and machine-readable observations are
under a disposable system temporary directory. Server output is discarded so
that no environment or provider material can be printed. The report above
records the non-secret identifiers and normalized results needed to interpret
the run.

## 20. Evidence boundary and final status

This report is an evidence snapshot, not an architecture amendment. Existing
Apex architecture remains authoritative, including:

- `Task != Attempt`;
- one immutable `ExecutionManifest` per Attempt;
- Core-owned authority and semantic state;
- runtime completion `!=` semantic success;
- optional DPT and optional, independent Orchestration;
- replaceable runtime substrates;
- authority materialization/binding `NOT_PROVEN`;
- controller-loss reconciliation `NOT_PROVEN`.

No architecture document, CI workflow, product/runtime code, dependency, or
reference repository was modified by this experiment.
