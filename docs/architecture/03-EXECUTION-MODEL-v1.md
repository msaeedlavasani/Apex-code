# Execution Model v1

Status: **FREEZE_CANDIDATE**.

## Lifecycle

An `ExecutionRequest` creates an `Execution` and an immutable `ExecutionManifest`. The Core materializes Tasks, selects an agent/model/runtime lane, binds the runtime session through the adapter, verifies authority, and releases the `ExecutionBarrier`. Only then may a new `Attempt` execute.

An Attempt reports runtime facts into an `AttemptResult`. Core interprets those facts, performs verification, records artifacts and Events, and derives semantic Task state. Runtime completion alone never implies Task success. A retry creates a new Attempt and retains the history of the prior Attempt.

```text
Request -> Manifest -> Task -> authority revision -> barrier release
                                      -> Attempt -> adapter facts
                                      -> verification -> result/artifacts/events
```

## State and safety rules

Authority is represented by an immutable `AuthorityRevision` and bounded by a `PermissionEnvelope`. Execution is blocked until authority is verified and the barrier is released. Unknown or incomplete information remains `UNKNOWN`; it is never silently converted to success, failure, or approval.

Runtime session identifiers and runtime-specific lifecycle details remain behind the Runtime Adapter SPI. Core owns the meaning of Task, Attempt, Authority, and Runtime states.

## Ownership

Task, Attempt, Authority, and Runtime are Apex Code Core concepts. DPT and orchestration may consume and extend these primitives through their capability boundary, but cannot redefine or replace them.
