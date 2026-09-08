# AC-DEV-023 — Apex-Owned Definition Projection Adapter Proof

Status: `READY` / `NOT_RUN` / `NOT_PROVEN`

## Contract

Apex owns canonical `AgentDefinition` identity and capability metadata. A
bounded adapter may project a task-scoped immutable payload to a generic
execution substrate. The projection must bind `definition_id`, registry
revision, definition digest, and the bounded definition payload to the
Development Attempt.

The executor cannot define Apex claims, elevate authority, assign semantic
success, or replace Apex scheduling, verification, retry/recovery, or
reconciliation. The proof must reject missing, malformed, stale, mismatched,
or replayed projection identity before invocation.

## Acceptance boundary

The proof is limited to disposable/local bounded execution and must produce
durable operational evidence for projection integrity, identity preservation,
fail-closed invocation, and result transport. It must not select Goose or
Freebuff permanently, install ECC, or perform unrestricted runtime dispatch.

Until the proof is accepted and AC-DEV-017 matching plus AC-DEV-018 admission
are explicitly reconciled, `agent.definition_catalog` remains `NOT_PROVEN`,
AC-DEV-018 remains `BLOCKED_CAPABILITY`, and dispatch remains disabled.
