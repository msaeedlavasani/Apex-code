# Architecture Reconciliation 0001

**Status:** `PROPOSED` Owner decision proposal; no architecture contract is
changed by this document.

**Scope:** Reconcile the completed comparative harvest with the current Apex
Code architecture. This record does not authorize implementation, runtime
experiments, dependency selection, source reuse, or architecture freeze.

**Base:** Apex Code `main` at
`22f6be1eb8403f7b909b58c2e0d0ed34c9ac82e8`.

## 1. Purpose and authority

The comparative harvest is evidence, not architecture authority. The current
Apex contracts and status document remain authoritative unless an Owner accepts
a reconciliation proposal through the architecture-change process. This report
therefore records decisions as `KEEP`, `REFINE`, `ADD`, `EXPERIMENT`, `DEFER`,
or `REJECT`, while preserving the distinction between a useful external pattern
and a proven Apex guarantee.

Primary evidence is the [comparative harvest](AGENTIC-DEVELOPMENT-SYSTEMS-COMPARATIVE-HARVEST.md),
which pins all 13 systems to exact commits and records source paths. Apex
contract inputs are the [Execution Data Model](../architecture/02-EXECUTION-DATA-MODEL-v1.md),
[Execution Model](../architecture/03-EXECUTION-MODEL-v1.md),
[Execution API](../architecture/04-EXECUTION-API-v1.md),
[Architecture Status](../architecture/05-ARCHITECTURE-STATUS.md),
[System Design](../SYSTEM-DESIGN.md), and [Security Model](../SECURITY-MODEL.md).
The [OpenWork Feasibility](OPENWORK-FEASIBILITY.md) record is also used. The
requested `OPENWORK-RUNTIME-PROOF.md` file is not present on this base, so no
claim is based on that unavailable record; its absence is `UNKNOWN` evidence,
not a reason to invent or upgrade a runtime guarantee.

## 2. Reconciliation invariants

The following remain unchanged and are `KEEP` decisions:

- `Development Task != Core Task`.
- `Task != Session` and `Task != Attempt`; a session or process is not promoted
  to a Core domain Task merely because an external system uses it as its main
  work unit.
- Retry creates a new `Attempt`.
- Every Attempt has exactly one immutable `ExecutionManifest`; a Task may have
  multiple historical manifests through its Attempts.
- `Task Passport != Core Task != Attempt != ExecutionManifest != AttemptResult`.
- Runtime-specific session/process identifiers remain adapter-specific.
- Core owns runtime-neutral semantic state, authority, verification, and safety;
  adapters report substrate facts and substrates own native process/session
  behavior.
- Runtime completion, provider completion, tool completion, and transcript
  persistence do not equal semantic Task success or Development Task `DONE`.
- DPT is optional. Orchestration is optional and independent from DPT. Core
  does not depend on either.
- Product Shells and visual projections are replaceable consumers, not owners
  of canonical execution, authority, scheduler, or mission state.
- `AuthorityRevision` activation and binding to the exact RuntimeLane/Attempt
  context remains `NOT_PROVEN`.

## 3. Owner decision table

| Topic | Current Apex Position | Harvest Evidence | Decision | Required Change | Confidence | Evidence Needed |
|---|---|---|---|---|---|---|
| Task versus session | Core Task is a domain primitive; sessions are adapter/runtime details | OpenCode and Goose center sessions; Vibe Kanban and Vigla separate task/process or task/worker | KEEP | Keep the distinction explicit in future Runtime Adapter and API contracts | SOURCE_CODE_EVIDENCE + FROZEN architecture | None for the invariant; adapter mapping remains to be designed |
| Development Task versus Core Task | Separate DCS and Core entities | Vibe/agtx/Vigla show useful work records but do not define Apex semantics | KEEP | Preserve explicit Development Task → ExecutionRequest → Core Task mapping | DOCUMENTATION_EVIDENCE + accepted DCS boundary | Detailed mapping contract later |
| Retry identity | Retry creates a new Attempt | Vigla continuation can reuse worker identity; Goose resumes sessions | KEEP | Reject identity reuse as Apex Attempt semantics | SOURCE_CODE_EVIDENCE | Runtime implementation tests later |
| Immutable ExecutionManifest | One immutable manifest per Attempt | No selected system proves this Apex contract; Vigla has partial worker/event identity | KEEP | Do not substitute session, worker, or checkpoint metadata for the Manifest | NOT_PROVEN external evidence; FROZEN Apex rule | Implementation evidence when Core exists |
| ExecutionEpoch | FREEZE_CANDIDATE interval within an Attempt | LangGraph checkpoint/interrupt ancestry and E2B snapshots are useful bounded patterns | REFINE | Keep Epoch as the Apex boundary for authority changes, reconnect, and continuation; do not equate it with a provider checkpoint | SOURCE_CODE_EVIDENCE + existing status | Exact Attempt/Epoch state machine and side-effect rules |
| Checkpoint lineage | Not yet assigned to a canonical owner | LangGraph persists checkpoint IDs, parent links, versions, writes, and metadata | REFINE | Treat checkpoint lineage as adapter/recovery evidence associated with an Epoch; Attempt identity remains Core-owned | SOURCE_CODE_EVIDENCE | Cross-substrate resume and idempotency experiment |
| Checkpoint side-effect safety | Not established | LangGraph resumes node logic from checkpoint boundaries; the harvest does not prove external side-effect idempotency | EXPERIMENT | Do not define resume as safe re-execution until side-effect behavior is measured | NOT_PROVEN | E4 checkpoint/resume side-effects experiment |
| Runtime Adapter boundary | Accepted direction; exact v1 contract is FREEZE_CANDIDATE | OpenCode/Goose provider seams; E2B sandbox API; Daytona documentation-only control planes; OpenWork proxy seam | REFINE | Define typed adapter facts/commands and identity correlation without letting adapters assign semantic Task state | SOURCE_CODE_EVIDENCE + existing status | Cross-substrate contract experiment and contract design |
| Runtime facts | Core already requires adapters to report facts | External patterns expose process/session/sandbox states but use product-specific terms | REFINE | Normalize facts such as `RUNNING`, `EXITED`, `MISSING`, `UNREACHABLE`, `MISMATCH`, `UNKNOWN`; facts are not semantic outcomes | SOURCE_CODE_EVIDENCE + INFERENCE | Adapter contract and failure-injection tests |
| Controller-loss reconciliation | Recovery direction exists; complete guarantee is not proven | No selected system proves controller-loss reconciliation; Vigla explicitly leaves this gap | ADD | Add a proposed Core Reconciliation Loop concept: durable Attempt + adapter facts + authority + resource ownership → semantic state | NOT_PROVEN across harvest; strong risk inference | Restart/loss/reconnect experiment |
| Startup recovery | Not yet implemented | LangGraph checkpoint resume and E2B reconnect are bounded patterns | REFINE | Define startup scan and classification of stale Attempts, missing lanes, orphaned lanes, and unknown facts | SOURCE_CODE_EVIDENCE + INFERENCE | Recovery experiment |
| Duplicate execution prevention | Required safety goal; implementation absent | Vigla reserves slots; OpenCode coordinator is process-local; Vibe monitors processes | REFINE | Make duplicate-start detection a Core/reconciliation acceptance condition, not a shell or adapter assumption | SOURCE_CODE_EVIDENCE + NOT_PROVEN | Controller-loss and duplicate-start test |
| ResourceClaim / ResourceLease | Both are `FREEZE_CANDIDATE` Core primitives | Vibe/Vigla/Nimbalyst provide worktree/workspace isolation but no Apex-grade lease proof | REFINE | Core owns claim meaning/conflict semantics; adapter/control plane performs substrate reservation; define expiry/reclaim only after contract work | SOURCE_CODE_EVIDENCE + existing status | Concurrent claim, stale lease, and reclaim experiment |
| Authority binding | Immutable AuthorityRevision, PermissionEnvelope, barrier sequence; binding is `NOT_PROVEN` | OpenCode, OpenWork, Vibe, Goose, and Nimbalyst show approval/permission patterns, not Apex binding | REFINE | Preserve and sharpen `Envelope → Revision → materialize → verify active → bind exact Lane/Attempt/Epoch → Barrier → START` | NOT_PROVEN; source evidence is partial | Direct activation/binding proof experiment |
| Authority-binding proof | Required by the existing invariant but absent from implementation | No selected comparator proves the exact binding chain | EXPERIMENT | Keep the requirement unchanged and test it before claiming runtime support | NOT_PROVEN | E1 authority activation and binding experiment |
| Independent verification | Verification is Core-owned; runtime completion is not success | Vibe review, Vigla review/witness events, and Freebuff outputs are not independent semantic verification | REFINE | Define verification as contract-based evaluation; executor/provider self-report cannot alone close a Task | SOURCE_CODE_EVIDENCE + FROZEN invariant | Negative and independent-verifier tests |
| Verification ownership | Core Verification derives semantic state; Advanced Verification is optional | External systems expose review/validation surfaces with no Apex authority proof | KEEP | Keep basic safety/integrity verification in Core; advanced methods remain optional capability extensions | Existing architecture + harvest | Detailed verification contract later |
| Completion semantics | AttemptResult, Verification, Acceptance, and DONE are distinct | Vibe process/review split and Vigla Completion/Review partially support the separation | KEEP | Document the state chain; never mark Task success from process exit alone | SOURCE_CODE_EVIDENCE + FROZEN invariant | Core implementation and acceptance tests |
| Retry / resume / reconnect / recovery | Concepts are not yet fully separated in the contract | Provider retries, session resume, checkpoint resume, sandbox reconnect, rollback, and requeue appear as different mechanisms | REFINE | Reserve distinct terms and state transitions; retry is a new Attempt, resume may continue an Epoch, reconnect restores adapter observation, recovery reconciles state | SOURCE_CODE_EVIDENCE | Failure matrix and recovery experiment |
| Orchestration boundary | Optional capability above Core | Vigla/LangGraph/agtx show DAG, worker slots, joins, and command-mediated workflow | KEEP | Keep DAG/readiness/assignment/join/reassignment in optional Orchestration; Core owns Tasks, Attempts, resources, and semantic state | SOURCE_CODE_EVIDENCE + FROZEN boundary | Orchestration contract later |
| Dependency readiness | Not a Core replacement for Task semantics | Vigla and LangGraph provide direct dependency/barrier patterns; agtx is partial | REFINE | Allow Orchestration to project prerequisites and readiness into Core commands without owning Core Task identity | SOURCE_CODE_EVIDENCE | Join/failure mapping experiment |
| Fallback and reassignment | Advanced Routing is optional; no guarantee is frozen | Freebuff/Goose provider fallback exists; dynamic semantic reassignment is not proven | DEFER | Do not add dynamic reassignment to Core; define only after Orchestration/Routing contracts exist | NOT_PROVEN | Routing/reassignment experiment later |
| Product Shell boundary | Shell consumes Public API and is replaceable | OpenWork/OpenHands/Vibe/Nimbalyst show shell, workspace, review, and control-center seams | KEEP | Shell may own navigation, presentation, workspace/session UX, review UX, configuration UI, and approval surfaces; it must not own semantic state | SOURCE_CODE_EVIDENCE + FROZEN boundary | Shell contract when implementation begins |
| Projection boundary | Visual state must not be canonical | Agent Mission Control demonstrates event → reducer → replay projection; Nimbalyst provides persistent workspace views | ADD | Add a proposed Projection Protocol/Layer concept for consuming canonical events/state; do not design spatial UI now | SOURCE_CODE_EVIDENCE + INFERENCE | Projection corruption/staleness experiment |
| Events | Durable lifecycle facts are `FROZEN` | Vigla typed versioned events; OpenCode typed event persistence; Mission Control event replay | REFINE | Define envelope/version/order/correlation/causation and references to Task/Attempt/Authority/Resource; events remain facts, not permission or semantic authority | SOURCE_CODE_EVIDENCE + existing status | Event replay/versioning contract |
| Agent/model/provider routing | Selection primitives exist; Advanced Routing is optional | OpenCode/Goose provider seams and Freebuff agent definitions | REFINE | Keep AgentSelection/ModelSelection/Provider abstraction in Core-neutral contracts; dynamic policy remains optional | SOURCE_CODE_EVIDENCE + FROZEN/Freeze Candidate primitives | Adapter/provider comparison |
| Runtime and sandbox ownership | Core owns runtime-neutral semantics and RuntimeLane abstractions | E2B exposes sandbox/process/network boundary; OpenCode/Goose own substrate-specific session behavior | KEEP | Use precise wording: Core owns semantics; adapters translate; substrates own native sessions/processes | SOURCE_CODE_EVIDENCE + existing architecture | Runtime Adapter Contract v1 |
| Source reuse and licenses | External learning is separate from implementation reuse | OpenWork MIT/EE split; Daytona and Agent Mission Control lack a license file at pinned refs | KEEP | Borrow concepts only; legal/source review gates any code reuse; preserve OpenWork/OpenCode replaceability | OBSERVED_REPOSITORY_STATE | License review for any future reuse |
| Harmful semantic collapse | Apex explicitly separates task, session, attempt, transcript, UI, runtime completion, and authority | External anti-pattern signals include session-as-task, transcript-as-ledger, UI-as-state, retry-as-recovery, and self-report as verification | REJECT | Do not import these shortcuts into Core, Product Shell, Orchestration, or DPT | SOURCE_CODE_EVIDENCE + FROZEN Apex boundaries | None; enforce through future contract review |
| DPT / Orchestration dependency | Both optional and independent; Core depends on neither | Harvest patterns are useful as capability inputs, not Core requirements | KEEP | No architecture or package dependency change | FROZEN architecture | None |

## 4. Execution and ownership decisions

### 4.1 Attempt, manifest, epoch, and checkpoint

The canonical relationship remains:

```text
Development Task
    ↓
Task Passport
    ↓
ExecutionRequest
    ↓
one or more Core Tasks
    ↓
Attempt
    ↓
one immutable ExecutionManifest
    ↓
ExecutionEpoch(s) within that Attempt
    ↓
Runtime Adapter / Runtime Session
```

`ExecutionManifest` is the birth certificate and immutable contract of one
Attempt. A provider session, worker row, graph task, sandbox, or checkpoint
cannot replace it. A retry creates a new Attempt and a new Manifest; a resume
or reconnect may remain within the same Attempt only if the future Core
contract says the Attempt identity and semantic execution interval remain
valid.

`ExecutionEpoch` remains `FREEZE_CANDIDATE`, not `FROZEN`. It is retained
because the existing model needs a bounded place for an approved authority
revision change, pause/resume, reconnect, or recovery continuation without
mutating prior authority history. LangGraph checkpoint ancestry is useful
evidence for lineage, but it is an adapter/recovery mechanism until Apex
defines how checkpoint side effects, idempotency, and semantic ownership work.

### 4.2 Runtime Adapter Contract direction

The adapter must expose typed observations and bounded commands. It must not
decide Apex semantic success or manufacture authority. A future contract should
separate:

| Adapter-facing fact/operation | Apex Core responsibility |
|---|---|
| runtime/session identity, availability, process state, exit facts, tool/process facts, reconnect result, substrate errors | map facts to Attempt/Epoch semantic state |
| lane/session start, interrupt, stop, reconnect request, fact query | authorize command, enforce idempotency, record receipt/event, release barrier, derive outcome |
| `RUNNING`, `EXITED`, `MISSING`, `UNREACHABLE`, `MISMATCH`, `UNKNOWN` | decide whether state is running, failed, lost, recovery-required, or otherwise semantic |
| substrate-native permissions, sandbox/network/process controls | materialize and verify `PermissionEnvelope`/`AuthorityRevision` and bind them to the exact context |

This is a `REFINE` direction for the existing `FREEZE_CANDIDATE` adapter
boundary. It is not a Runtime Adapter Contract v1 and does not select OpenCode,
Goose, E2B, or Daytona as a permanent dependency.

### 4.3 Proposed Reconciliation Loop

`ADD` is proposed for an explicit Core reconciliation concept, not an
implementation. Its responsibility is to compare:

```text
Core durable Attempt state
    + Runtime Adapter observed facts
    + AuthorityRevision / barrier state
    + RuntimeLane and ResourceClaim ownership
    ↓
reconciled Apex semantic execution state
```

The loop should eventually classify startup and controller-loss conditions,
including stale `RUNNING` Attempts, missing RuntimeLanes, orphaned lanes,
unreachable or mismatched runtimes, duplicate-start risk, and
`UNKNOWN`/`LOST`/`RECOVERY_REQUIRED` outcomes. No state name is frozen here.
The loop must fail closed where authority or resource ownership cannot be
verified and must not infer success from an idle or missing session.

### 4.4 Resource claims and leases

The harvest justifies `REFINE`, not a new primitive. `ResourceClaim` expresses
the Core semantic request for shared or exclusive use; `ResourceLease` expresses
the granted bounded ownership. Core should own the meaning, conflict result,
and relationship to Attempt/Epoch. A Runtime Adapter or control plane may
perform substrate-specific reservation, renewal, and release, but cannot turn a
local filesystem lock into a universal Apex guarantee.

Before parallel execution is implemented, the contract must answer:

- which resources are claimable (workspace, worktree, runtime lane, network,
  provider quota, or other resources);
- whether claims are durable and how they are correlated to Attempt/Epoch;
- renewal, expiry, stale-lease reclamation, and controller-loss behavior;
- how conflicting claims become `BLOCKED`, `UNKNOWN`, or
  `RECOVERY_REQUIRED`; and
- how duplicate execution is prevented when ownership is uncertain.

## 5. Authority and verification

The harvest does not weaken the existing authority invariant. The required
sequence remains:

```text
PermissionEnvelope
    ↓
AuthorityRevision materialized
    ↓
activation verified
    ↓
bound to exact RuntimeLane / Attempt / ExecutionEpoch context
    ↓
ExecutionBarrier released
    ↓
actual execution / RUNNING
```

OpenCode permission questions, OpenWork host approvals, Vibe approvals, Goose
permission records, and Nimbalyst project trust are useful UX or substrate
patterns. None proves the Apex binding guarantee. The complete
materialization/activation/binding chain remains `NOT_PROVEN`; this document
does not promote it through design prose.

Core Verification evaluates AttemptResult, Artifacts, Events, and the
applicable acceptance/verification contract. A runtime exit or worker summary
can be an input fact, but cannot directly mark a Core Task successful. The
semantic sequence remains distinct:

```text
Execution Complete
    → Result Collected
    → Verification Performed
    → Verification Passed (when required)
    → Acceptance Satisfied
    → Core Task semantic success
    → Development Task DONE
```

The exact verifier topology is `REFINE`: independent verification is required
where the contract/risk calls for it, but a mandatory separate verifier for
every task is not added by this reconciliation. Advanced Verification remains
an optional capability.

## 6. Recovery vocabulary

These terms must not be collapsed into a generic “retry”:

| Term | Proposed Apex meaning | Decision |
|---|---|---|
| Retry | Start a new Attempt for the same Core Task, with a new Manifest | KEEP |
| Resume | Continue an existing Attempt/Epoch from valid persisted context | REFINE |
| Reconnect | Re-establish observation/control of an existing runtime/session | REFINE |
| Rollback / Revert | Restore or undo workspace/resource changes according to a recovery contract | REFINE |
| Re-execution | Perform execution again; normally creates a new Attempt | KEEP |
| Reassignment | Change executor/agent/runtime ownership under an orchestration/routing decision | DEFER |
| Recovery | Bounded handling after failure, loss, interruption, or unsafe uncertainty | REFINE |
| Reconciliation | Compare durable Core state with observed external facts and repair semantic divergence | ADD |

No external source proves the complete recovery model. Runtime experiments are
required before any implementation claim is made.

## 7. Orchestration and Product Shell

### Orchestration

The harvest supports `KEEP` for the existing boundary and `REFINE` for the
interfaces. Orchestration may own DAG construction, dependency readiness,
fan-out, join, worker-slot policy, assignment, fallback, and reassignment. It
may issue Core commands and consume Core facts, but it does not own Core Task or
Attempt identity, authority truth, RuntimeLane semantics, or semantic success.

Parallel execution is not itself proof of safe coordination. Resource claims,
idempotent commands, join behavior, failure classification, and reconciliation
must be explicit before parallel execution is treated as a reliable capability.
DPT may consume these contracts later but remains optional and independent.

### Product Shell

Product Shells may own navigation, workspace presentation, session and task
views, review UX, model/provider configuration, and approval presentation. They
must consume the Public API and event/projection contracts. They must not own
canonical Attempt state, authority truth, semantic success, durable scheduler
state, or mission state.

OpenWork, OpenHands, Vibe Kanban, and Nimbalyst provide complementary shell
patterns. Their UX does not make their local state an Apex source of truth, and
OpenWork remains replaceable rather than Apex identity.

### Projection Protocol

`ADD` is proposed for a future Projection Protocol/Layer contract, kept separate
from spatial or visual UI design. A projection may consume Tasks, Attempts,
Agents, Events, failures, dependencies, claims, verification, and human gates.
It must declare its source revision/cursor, tolerate stale or missing data, and
never write visual state back as canonical truth without a Core command.

Agent Mission Control's event/reducer/replay model is direct evidence for the
projection separation; it is not evidence for a Mission Control product or
runtime scheduler.

## 8. Events, routing, and licenses

### Events

The existing `Event` primitive remains `FROZEN`; its detailed contract should be
`REFINED` later using the harvest. A candidate envelope is:

```text
eventType
schemaVersion
eventId
occurredAt
sequence / ordering scope
causationId
correlationId
executionId / taskId / attemptId / epochId
runtimeLaneId / runtimeSessionId when applicable
authorityRevisionId / resourceLeaseId when applicable
fact-or-interpretation classification
payload
```

Events are durable facts for replay and projection. An event does not grant
permission, replace the source-of-truth hierarchy, or by itself establish
semantic success. Ordering and replay scope must be defined per aggregate or
stream, not assumed from an external event bus.

### Routing

Keep `AgentSelection`, `ModelSelection`, and provider abstraction as
runtime-neutral Core inputs/contract references. Dynamic next-best routing,
fallback policy, and reassignment are `DEFER` until Runtime Adapter and
Orchestration contracts exist. Freebuff and Goose show provider/fallback seams;
that is useful evidence, not a reason to introduce DPT or Advanced Routing into
Core.

### License and source reuse

The reconciliation `KEEP`s the existing rule that conceptual learning and code
reuse are separate decisions. OpenWork's MIT/EE split remains a material reuse
boundary. Daytona and Agent Mission Control had no license file at their pinned
harvest snapshots, so code reuse is unresolved and not recommended. No
architecture should depend on copying OpenCode, OpenWork, Goose, or any other
external implementation.

## 9. Proposed architecture deltas and status handling

No existing architecture file is modified in this proposal. If the Owner
accepts the `ADD`/`REFINE` decisions, a later architecture delta should make
only traceable edits:

| Proposed delta | Current owner/status | Intended next owner | Status now |
|---|---|---|---|
| Runtime fact/event contract | `04-EXECUTION-API`, `03-EXECUTION-MODEL`; Adapter API `FREEZE_CANDIDATE` | Runtime Adapter Contract v1 | PROPOSED |
| Reconciliation Loop | Recovery direction in System Design; no explicit contract | Execution Model / Runtime Adapter Contract | PROPOSED |
| Resource claim/lease lifecycle | Execution Data Model `FREEZE_CANDIDATE` | Execution Data Model / Runtime contract | PROPOSED |
| Checkpoint-to-Epoch relationship | Execution Data Model `FREEZE_CANDIDATE` | Execution Model / Recovery contract | PROPOSED |
| Projection Protocol | Not yet a formal Core primitive | System Design / Public API projection contract | PROPOSED |
| Event envelope detail | `Event` is FROZEN; detail remains open | Execution API / Events contract | PROPOSED |
| Verification and recovery distinctions | Verification is FROZEN; detailed semantics open | Execution Model / Validation contract | PROPOSED |

These are not silently promoted to `FROZEN`. Existing FROZEN principles remain
unchanged, and `NOT_PROVEN` remains visible.

## 10. Bounded runtime experiment backlog

These experiments are required before the relevant implementation or contract
can be treated as proven. None was executed in this delta.

### E1 — Authority activation and binding

- **Question:** Can an exact `AuthorityRevision` be materialized, verified
  active, and bound to the exact RuntimeLane/Attempt/Epoch before the barrier
  releases?
- **Invariant:** No actual execution/RUNNING before the verified exact binding.
- **Substrate/system:** First Runtime Adapter candidate, with a controlled
  test runtime; OpenCode may be a substrate fixture, not the contract owner.
- **Setup:** Create an Attempt, revisioned envelope, lane, and intentionally
  stale/mismatched approval; test allow, deny, unknown, reconnect, and revision
  change cases.
- **Expected evidence:** Durable command/event/receipt records plus adapter
  facts showing identity correlation and barrier ordering.
- **Pass:** Only the exact active revision permits start; mismatches fail closed
  and remain observable.
- **Fail:** Start occurs before binding, stale authority is accepted, or
  identity correlation is ambiguous.
- **Decision unlocked:** Runtime Adapter authority fact contract and final
  barrier/binding semantics.

### E2 — Controller loss and reconciliation

- **Question:** Can Core classify and safely recover from controller/process loss
  during an active Attempt?
- **Invariant:** No duplicate execution; uncertain ownership remains
  `UNKNOWN`, `LOST`, or `RECOVERY_REQUIRED`, not success.
- **Substrate/system:** Controlled adapter process with kill/restart and
  reconnect support.
- **Setup:** Kill controller, runtime process, and network independently at
  pre-start, running, tool-side-effect, and completion boundaries.
- **Expected evidence:** Durable Attempt/Epoch state, adapter fact timeline,
  resource ownership, and reconciliation decisions.
- **Pass:** Recovery is idempotent, ownership is classified, and no duplicate
  side effect is started.
- **Fail:** Stale RUNNING is trusted, two owners start, or state silently marks
  success.
- **Decision unlocked:** Reconciliation Loop states, startup scan, and recovery
  contract.

### E3 — Resource claim/lease conflict

- **Question:** Can two Attempts be prevented from unsafe concurrent use of the
  same workspace or runtime resource?
- **Invariant:** Conflicting claims cannot both become valid leases.
- **Substrate/system:** Two adapter instances against one workspace plus
  controller restart.
- **Setup:** Compete for exclusive/shared claims, expire a lease, lose its
  owner, and attempt stale release/reclaim.
- **Expected evidence:** Claim/lease records, conflict result, expiry/reclaim
  event, and Attempt correlation.
- **Pass:** Conflicts are deterministic, stale ownership is safe, and no
  unverified reclaim causes overlap.
- **Fail:** Both Attempts write, lease ownership is ambiguous, or reclaim
  silently bypasses Core semantics.
- **Decision unlocked:** ResourceClaim/Lease lifecycle and adapter ownership.

### E4 — Checkpoint/resume side effects

- **Question:** Can checkpoint or session resume continue safely without
  duplicating non-idempotent effects?
- **Invariant:** Checkpoint lineage never replaces Attempt identity and resumed
  work cannot replay an unsafe side effect without a Core decision.
- **Substrate/system:** LangGraph-style checkpoint fixture and one runtime
  adapter; compare provider/session resume where available.
- **Setup:** Interrupt before, during, and after an external side effect; resume
  from parent and child checkpoints with duplicate delivery.
- **Expected evidence:** Epoch/checkpoint lineage, effect receipts, and
  duplicate suppression or explicit recovery classification.
- **Pass:** Resume boundaries and side effects are deterministic and auditable.
- **Fail:** Resume replays an unsafe effect or creates ambiguous Attempt state.
- **Decision unlocked:** Checkpoint-to-Epoch ownership and Resume contract.

### E5 — Independent semantic verification

- **Question:** What minimum verification separates runtime/provider completion
  from Core Task success?
- **Invariant:** Executor self-report and process exit cannot alone satisfy a
  required acceptance contract.
- **Substrate/system:** Controlled executor plus an independent verifier path.
- **Setup:** Produce correct, incorrect, incomplete, and unknown artifacts with
  successful, failed, and interrupted process exits.
- **Expected evidence:** AttemptResult, artifacts, verification record, and
  semantic Task state with explicit acceptance outcome.
- **Pass:** Required verification and acceptance gates are enforced and
  `UNKNOWN` is preserved.
- **Fail:** A successful process or agent summary closes a task without the
  required verification.
- **Decision unlocked:** Core Verification contract and Advanced Verification
  extension boundary.

### E6 — Cross-substrate adapter facts

- **Question:** Can OpenCode, Goose, and a sandbox substrate report a common
  minimal fact/command contract without leaking substrate semantics into Core?
- **Invariant:** Core receives normalized facts while runtime-native IDs and
  behavior remain adapter-specific.
- **Substrate/system:** OpenCode, Goose, and E2B-style fixtures; Daytona remains
  documentation/source-gap context only.
- **Setup:** Exercise start, interrupt, stop, exit, missing, unreachable,
  reconnect, artifact, and session identity cases.
- **Expected evidence:** Same contract-level event/fact set with explicit
  unsupported/unknown results.
- **Pass:** Core semantics remain stable across substrates.
- **Fail:** Core requires provider-specific behavior or treats unsupported
  behavior as success.
- **Decision unlocked:** Runtime Adapter Contract v1 and substrate fit.

### E7 — Event replay and projection integrity

- **Question:** Can a projection rebuild from canonical events while remaining
  non-authoritative and safe under stale, missing, or duplicated events?
- **Invariant:** Visual/projection state cannot become canonical execution or
  authority state.
- **Substrate/system:** Append-only event fixture with replay cursor and a
  deliberately corrupted projection.
- **Setup:** Drop, duplicate, reorder, and replay events; issue a command only
  through the Core boundary.
- **Expected evidence:** Projection cursor/version, rebuild result, and proof
  that visual state cannot authorize or close an Attempt.
- **Pass:** Projection converges or reports uncertainty without mutating Core
  truth.
- **Fail:** Projection data is accepted as authority or semantic success.
- **Decision unlocked:** Projection Protocol and event replay contract.

## 11. Unresolved `NOT_PROVEN` and `UNKNOWN` items

- Full `AuthorityRevision` materialization, activation verification, and exact
  RuntimeLane/Attempt/Epoch binding.
- Controller-loss reconciliation and startup recovery.
- Duplicate execution prevention across process/controller restart.
- ResourceClaim/ResourceLease persistence, renewal, expiry, and safe reclaim.
- Checkpoint side-effect idempotency and its relationship to ExecutionEpoch.
- Independent semantic verification guarantees and verifier authority.
- Cross-substrate Runtime Adapter Contract conformance.
- Dynamic reassignment and next-best fallback semantics.
- Whether the unavailable `OPENWORK-RUNTIME-PROOF.md` record exists in another
  historical ref; no claim is made until provenance is established.
- License/source boundary for code reuse from Daytona or Agent Mission Control.

## 12. Result and next gate

The comparative harvest materially strengthens several existing directions but
does not justify rewriting Apex architecture or selecting a permanent
substrate. The recommended reconciliation is:

- **KEEP:** Core boundaries, Task/Attempt/Manifest identity, authority
  ownership, semantic completion, optional DPT/Orchestration, and replaceable
  shells/projections.
- **REFINE:** Runtime facts, event envelope, recovery vocabulary, verification
  stages, checkpoint/Epoch relationship, and resource ownership.
- **ADD:** A proposed Core Reconciliation Loop and a proposed non-authoritative
  Projection Protocol/Layer.
- **EXPERIMENT:** Authority binding, controller loss, resource claims,
  checkpoint side effects, independent verification, cross-substrate facts, and
  projection integrity.
- **DEFER:** Dynamic reassignment, full orchestration scheduling semantics,
  numeric resource policy, and substrate/framework adoption.
- **REJECT:** Session-as-Task, transcript-as-ledger, UI-as-source-of-truth,
  retry-as-recovery, worker self-report as verification, implicit authority
  escalation, and external product/team semantics embedded in Core.

This report is ready for Owner review. It does not modify architecture files,
create implementation scope, or upgrade any `NOT_PROVEN` claim.
