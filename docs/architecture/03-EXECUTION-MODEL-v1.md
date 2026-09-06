# Execution Model v1

Status: **FREEZE_CANDIDATE**.

Reconciliation trace: [Architecture Reconciliation 0001](../evidence/ARCHITECTURE-RECONCILIATION-0001.md)
and the [comparative harvest](../evidence/AGENTIC-DEVELOPMENT-SYSTEMS-COMPARATIVE-HARVEST.md).

## Lifecycle

An `ExecutionRequest` creates an `Execution`, which materializes one or more Tasks. When a Task is attempted, the Core creates an `Attempt` and exactly one immutable `ExecutionManifest` for that Attempt. The manifest records the `AgentSelection`, `ModelSelection`, `RuntimeRequirement`, `WorkspaceSnapshot`, and an `AuthorityRevision` reference. A retry creates a new Attempt and therefore a new immutable ExecutionManifest; prior manifests remain historical records.

The Core then reserves or prepares a `RuntimeLane`, materializes and verifies authority, binds the exact active `AuthorityRevision` to the RuntimeLane/Attempt context, and releases the `ExecutionBarrier`. Only after that sequence may the Attempt enter actual execution/RUNNING.

An Attempt reports runtime facts into an `AttemptResult`. Core interprets those facts, performs verification, records artifacts and Events, and derives semantic Task state. Runtime completion alone never implies Task success. A retry creates a new Attempt and retains the history of the prior Attempt.

```text
ExecutionRequest -> Execution -> Task -> Attempt created
                                      -> ExecutionManifest created
                                      -> RuntimeLane reserved/prepared
                                      -> authority materialized + verified
                                      -> ExecutionBarrier released
                                      -> Attempt starts
                                      -> result collection
                                      -> verification
                                      -> AttemptResult / Artifacts / Events
                                      -> Task semantic state
```

## State and safety rules

Authority is represented by an immutable `AuthorityRevision` and bounded by a `PermissionEnvelope`. No Attempt may enter actual execution/RUNNING before the exact AuthorityRevision for the relevant ExecutionEpoch is verified active and bound to the exact RuntimeLane/Attempt context. The complete implementation guarantee for this materialization and binding chain remains `NOT_PROVEN`. Unknown or incomplete information remains `UNKNOWN`; it is never silently converted to success, failure, or approval.

Core owns runtime-neutral execution semantics and RuntimeLane abstractions. Runtime adapters own substrate translation/integration, runtime substrates own native session/process behavior, and Core interprets adapter facts into Apex semantic state. Runtime session identifiers and runtime-specific lifecycle details remain behind the Runtime Adapter SPI.

## Runtime facts and reconciliation

Runtime Adapters report substrate facts and accept bounded Core commands. They
do not directly assign Apex semantic Task success or failure. A future adapter
contract may normalize facts such as `RUNNING`, `EXITED`, `MISSING`,
`UNREACHABLE`, `MISMATCH`, and `UNKNOWN`, while retaining native identifiers
behind the adapter boundary.

### Reconciliation Loop

The Core-owned Reconciliation Loop is a `FREEZE_CANDIDATE` concept. It compares:

```text
durable Attempt state
    + Runtime Adapter observed facts
    + AuthorityRevision / barrier state
    + RuntimeLane and ResourceClaim / ResourceLease ownership
    ↓
reconciled Apex semantic execution state
```

At startup or after controller/process loss, it must classify stale
`RUNNING` Attempts, missing or orphaned RuntimeLanes, duplicate-start risk,
`UNREACHABLE`/`UNKNOWN`/`LOST` facts, and `RECOVERY_REQUIRED` conditions. It
must fail closed when authority or resource ownership cannot be verified. The
complete controller-loss and duplicate-prevention guarantee remains
`NOT_PROVEN`.

## Recovery vocabulary

The following terms are distinct: `Retry` starts a new Attempt; `Resume`
continues an existing valid Attempt/Epoch; `Reconnect` restores observation or
control of an existing runtime; `Rollback/Revert` restores or undoes changes;
`Re-execution` performs execution again and normally creates a new Attempt;
`Reassignment` changes executor ownership under optional orchestration/routing;
`Recovery` handles failure, loss, interruption, or unsafe uncertainty; and
`Reconciliation` compares durable Core state with external facts. `Retry` is
not an umbrella term for these behaviors.

## Verification and semantic completion

Runtime or provider completion is not semantic Task success. The Core
progression is:

```text
Execution Complete → Result Collected → Verification → Acceptance
                  → Task semantic terminal state
```

Basic integrity and safety verification remain Core-owned. Advanced
Verification remains an optional capability. The implementation of independent
semantic verification is `NOT_PROVEN`; executor or provider self-report alone
cannot satisfy a required acceptance contract.

## Authority binding status

The required sequence remains:

```text
PermissionEnvelope → AuthorityRevision → materialization
→ activation verification → exact RuntimeLane binding
→ exact Attempt/ExecutionEpoch binding → ExecutionBarrier → START
```

The sequence is a required design invariant, but its complete implementation
guarantee remains `NOT_PROVEN`.

## Ownership

Task, Attempt, Authority, and Runtime are Apex Code Core concepts. DPT and orchestration may consume and extend these primitives through their capability boundary, but cannot redefine or replace them.
