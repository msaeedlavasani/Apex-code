# Execution API v1

Status: **FREEZE_CANDIDATE**. This is a conceptual contract, not an implementation commitment.

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
