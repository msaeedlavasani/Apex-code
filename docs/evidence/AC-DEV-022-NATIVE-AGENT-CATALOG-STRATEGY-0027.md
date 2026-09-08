# AC-DEV-022 — Native Agent Catalog Capability Strategy

Status: `HUMAN_GATE` / `NOT_PROVEN`; Owner Decision Queue required

Task: `AC-DEV-022`

## Decision boundary

AC-DEV-019 established that Goose and Freebuff do not currently provide
operational proof of the required native `agent.definition_catalog`. Apex now
owns an executor-neutral Agent/Skill Registry, but registry ownership does not
by itself prove that a generic executor can consume Apex-owned definitions.

The current AC-DEV-017/018 requirement remains unchanged:
`agent.definition_catalog` is REQUIRED at minimum `PARTIAL`, and admission
remains `BLOCKED_CAPABILITY` until an accepted capability contract is proven.

The machine-readable Owner Decision receipt is
[`AC-DEV-022-OWNER-DECISION-0027.json`](AC-DEV-022-OWNER-DECISION-0027.json).

## Exact contracts

Native catalog contract: an executor operationally enumerates stable named
native agent definitions and exposes enough identity to select one without
confusing UI labels, source symbols, documentation, or self-report with proof.

Apex-owned definition projection target: Apex selects a registry definition and
passes an immutable task-scoped projection containing `definition_id`, the
registry revision, a definition digest, and the bounded definition payload
through a future adapter. The adapter must acknowledge the projection and keep
the identity/digest bound to the development Attempt. Apex retains task
identity, scheduling, resource claims, authority, verification, semantic
success, and reconciliation. The executor cannot elevate claims or assign
semantic success.

## Strategy result

Generic executor consumption is a plausible future adapter target, but it is
not operationally proven in this repository. Implementing it would change the
capability/authority boundary and requires Owner approval plus a separate
adapter proof for identity binding, projection integrity, rejection behavior,
and result transport. Therefore this task does not remove the REQUIRED
capability, does not weaken admission, and does not dispatch runtime work.

The Owner Decision Queue item is
`OWNER_APPROVAL:AC-DEV-022-APEX-OWNED-DEFINITION-PROJECTION`. Until it is
resolved, AC-DEV-022 remains `HUMAN_GATE`, the registry is unchanged, and the
autonomous run may continue only with unrelated eligible work.
