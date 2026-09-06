# Execution Model v1

Status: **FREEZE_CANDIDATE**.

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

## Ownership

Task, Attempt, Authority, and Runtime are Apex Code Core concepts. DPT and orchestration may consume and extend these primitives through their capability boundary, but cannot redefine or replace them.
