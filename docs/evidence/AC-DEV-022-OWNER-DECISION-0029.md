# AC-DEV-022 — Owner Decision 0029

## Decision

`APPROVED`

The Owner approved the bounded architecture boundary: Apex may own canonical
`AgentDefinition` identity and capability metadata and project a bounded,
executor-specific invocation payload to a generic execution substrate that does
not expose a native agent catalog.

The executor remains an execution substrate only. Apex retains task semantics,
definition identity, capability requirements, scheduling, authority,
verification, retry/recovery, semantic success, and reconciliation.

## Conditions

Approval authorizes the boundary; it does not prove generic executor injection.
The projection must remain immutable and task-scoped, bind `definition_id`,
registry revision, and definition digest, and fail closed before invocation on
missing, malformed, stale, mismatched, or replayed identity material.

No executor is selected, no ECC is installed, and no unrestricted dispatch is
permitted. `agent.definition_catalog` remains `NOT_PROVEN`, and AC-DEV-018
remains `BLOCKED_CAPABILITY` with dispatch disabled until the follow-on proof is
accepted and admission is explicitly reconciled.

## Canonical follow-on

`AC-DEV-023 — Apex-Owned Definition Projection Adapter Proof` is canonicalized
as `READY / NOT_RUN / NOT_PROVEN`. Its bounded acceptance contract covers
projection integrity, identity preservation, fail-closed invocation, result
transport, and preservation of Apex authority.

The machine-readable decision receipt is
[`AC-DEV-022-OWNER-DECISION-0029.json`](AC-DEV-022-OWNER-DECISION-0029.json).
