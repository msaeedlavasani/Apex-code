# AC-DEV-020 — Persistence/Reconciliation Regression Closure

Status: `VERIFIED` / `PROVEN`

Task: `AC-DEV-020`

## Result

The AC-DEV-019 failure mode is closed at the shared persistence boundary.
Canonical backlog task records no longer retain derived
`readiness_reasons`, `batch_id`, or `last_attempt_id` projections. Readiness is
returned as an in-memory projection; batch, Attempt, incident, and Owner
Decision Queue records remain in caller-supplied operational state.

The machine-readable reconciliation receipt is
[`AC-DEV-020-PERSISTENCE-RECONCILIATION-0025.json`](AC-DEV-020-PERSISTENCE-RECONCILIATION-0025.json).

## Control correction

- `ControlPlaneStore.save_backlog()` canonicalizes known transient task fields
  before comparing or writing JSON.
- `refresh_readiness()` repairs stale projections, persists only canonical
  workflow state, and returns readiness reasons without persisting them.
- batch selection no longer writes a batch ID into a task;
- completion, failure, and recovery keep attempt identity in operational state;
- task Human Gates are idempotently projected into the Owner Decision Queue;
- the run-loop stop reason is `OWNER_DECISIONS_ONLY` when that queue is the only
  remaining work.

## Regression evidence

Focused tests cover stale transient fields, cleanup, repeated byte identity,
batch/attempt projection absence, and idempotent Owner Decision Queue
reconciliation. The full suite and documentation validation are required before
the task is marked complete.

No authority, admission, executor, ECC, or Core runtime boundary changed.
