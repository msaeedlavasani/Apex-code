# Execution API v1

Status: **FREEZE_CANDIDATE**. This is a conceptual contract, not an implementation commitment.

Reconciliation trace: [Architecture Reconciliation 0001](../evidence/ARCHITECTURE-RECONCILIATION-0001.md)
and the [comparative harvest](../evidence/AGENTIC-DEVELOPMENT-SYSTEMS-COMPARATIVE-HARVEST.md).

## Public aggregate

`Execution` is the public aggregate. Its API exposes lifecycle commands and durable observations without exposing arbitrary internal state mutation.

## Conceptual public surface

- create/get execution
- pause/resume/cancel execution
- get task
- retry task
- get/cancel attempt
- transcript
- artifacts
- control input
- authority approve/reject
- events replay/stream
- command receipts
- capabilities

## API rules

- APIs express commands, not arbitrary state mutation.
- There is no public PATCH of Task or Attempt status.
- Every side-effecting command supports idempotency.
- Every accepted side-effecting command has a durable `CommandReceipt`.
- Adapters report facts; Core owns semantic state.
- The Product Shell consumes the Public API.
- DPT and orchestration use Capability SPI.
- OpenCode uses Runtime Adapter SPI.

Receipts and Events make command acceptance, replay, and outcome distinguishable. A command receipt is not itself proof that the requested work succeeded.

## Runtime facts and Events

Runtime Adapter facts are substrate observations, not semantic Apex outcomes.
The bounded Runtime Adapter Contract v1 exposes normalized facts such as `RUNNING`,
`EXITED`, `MISSING`, `UNREACHABLE`, `MISMATCH`, and `UNKNOWN`, together with
runtime-native identifiers and bounded command results. Its implementation is
[`apex_code/contract.py`](../../apex_code/contract.py); the stable
cross-substrate contract remains a `FREEZE_CANDIDATE`. Core interprets those
facts into Attempt, Epoch, verification, recovery, and Task state; an adapter
must not directly mark a Task successful or failed.

Apex Events are typed/versioned durable facts for replay and projection. The
event direction includes:

- event type, schema version, event identity, and timestamp;
- ordering scope, correlation ID, and causation ID;
- Execution/Task/Attempt references;
- an ExecutionEpoch reference when applicable;
- AuthorityRevision and resource references when applicable; and
- compatibility information needed by replaying consumers and projections.

Events do not grant permission, replace the Public API, or become semantic
authority. A projection consumes canonical Core state and Events but cannot
write visual or derived state back as canonical state without a Core command.

The exact Runtime Adapter and Event contracts remain `FREEZE_CANDIDATE` and
require later contract refinement. Their cross-substrate behavior is
`NOT_PROVEN`.
