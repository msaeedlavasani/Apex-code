# Apex Code Development Control Plane v1

Status: **CURRENT bounded implementation**. This document describes the
machine-readable, backlog-driven development workflow materialized for
`AC-DEVELOPMENT-CONTROL-PLANE-0015`. It is a development workflow control
plane, not Apex Core execution authority, DPT, or product Orchestration.

## Canonical ownership

The canonical backlog is `development_control/backlog.json`. Task Passports
are the files in `development_control/passports/`. Operational state is
runtime data supplied to `ControlPlaneStore.state_path`; it must not be
committed as canonical product truth unless a later governance decision adds a
durable state publication policy.

The control plane owns Development Task admission, batching, development
Attempts, incidents, owner decisions, and run summaries. Apex Core remains the
authority for Core `Task`, `Attempt`, `ExecutionManifest`, runtime facts,
verification, semantic success, and execution evidence.

```text
Canonical backlog + Task Passport
              ↓
      readiness / eligibility
              ↓
    immutable BatchSnapshot
              ↓
 executor-neutral development Attempt
              ↓
       verify / rework / incident
              ↓
     next batch or owner queue
```

## Status vocabulary

The backlog uses these workflow statuses:

`DONE`, `BACKLOG`, `BLOCKED`, `READY`, `ELIGIBLE`, `BATCHED`, `IN_PROGRESS`,
`VERIFYING`, `HUMAN_GATE`, `QUARANTINED`, and `DEFERRED`.

Workflow status is separate from evidence/claim status. `NOT_PROVEN` remains
an evidence state and is never converted to proof by readiness, successful
execution, or lack of observed failure.

## Passport admission

Every runnable task requires a complete Passport v1 containing goal, scope,
out-of-scope boundaries, dependencies, resource claims, architecture
constraints, acceptance criteria, validation, risk, executor compatibility,
and Human Gates. Admission is fail-closed when any required field is missing,
a dependency is not verified/done, a Human Gate is open, autonomous policy
does not allow the task, or the selected executor is incompatible.
An explicitly recorded `owner_authorized` task may pass the material-decision
policy check only for the named task; its risk, decision class, Passport
constraints, and evidence status remain unchanged. Deterministic and
reversible control-plane inconsistencies may be repaired when intent is
unambiguous and canonical history is preserved. Ambiguous or material
architecture, authority, security, or destructive decisions still require an
Owner gate.

## Deterministic batching

`DevelopmentControlPlane.select_batch()` refreshes readiness and selects a
conflict-safe subset using priority, critical-path weight, downstream unlock
value, aging, risk, and task ID as a deterministic tie-breaker. The persisted
`BatchSnapshot` is immutable in meaning: tasks that become eligible after the
snapshot wait for the next batch, and resource-claim conflicts are not placed
in the same batch.

## Attempts, failures, and incidents

Every execution and rework is recorded as a distinct development Attempt. A
task failure does not fail its batch. The failure is classified as
`TASK_FAILURE` or `SYSTEM_FAILURE`, linked to a stable incident fingerprint,
and returned to `BACKLOG` only within the bounded rework policy. Repeated or
systemic failures are `QUARANTINED`. Dependent tasks remain blocked until the
prerequisite is verified/done.

Incidents retain affected tasks, evidence references, occurrence count,
resolution, and corrective-task links. Repeated correlated failures can open
the systemic circuit breaker; the run loop then stops further wasteful
execution while preserving the owner decision queue and evidence.

## Batch verification and autonomous run loop

A batch closes only when every member has a terminal outcome and no task is
missing, `UNKNOWN`, or otherwise dangling. A batch may complete with mixed
success and failure. Tasks retain task-level verification, and an integration
verification result is required when the batch declares one.

The run loop is:

```text
BACKLOG → prioritize → READY/ELIGIBLE → immutable batch
        → execute → bounded recovery → verify/reconcile
        → update backlog → reprioritize → next batch
```

Batch completion never ends the run by itself. Human-Gated tasks accumulate in
the Owner Decision Queue while unrelated eligible work continues. The run
stops only at no safe batch, human-gates-only, a systemic circuit breaker, or
an explicit configured run bound.

## Executor neutrality and boundaries

Executors are workers selected by compatibility metadata. They are not
backlog, scheduler, authority, or semantic-success owners. The control plane
does not depend on Freebuff, Goose, OpenCode, DPT, or product Orchestration.

The seeded `AC-DEV-007` Goose UI/Desktop capability probe is now a verified
development outcome with partial evidence. Its required questions included
delegation, isolation, aggregation, failure, cancellation, dependency
awareness, and model/provider assignment. The evidence report preserves the
capabilities that remain `NOT_PROVEN`; the task result does not turn Goose into
a product dependency or scheduler authority.

The Goose CLI probe (`AC-DEV-011`) is supplemented by the Freebuff CLI probe
(`AC-DEV-012`). Freebuff reached an interactive parent surface and exposed
source-level extensibility signals, but child delegation, isolation,
aggregation, recovery, dependency sequencing, and per-task routing remain
`NOT_PROVEN`. The executor comparison (`AC-DEV-013`) keeps Goose and Freebuff
as replaceable candidates and does not select a permanent executor. ECC is not
installed. These probes do not transfer task authority to Goose or Freebuff or
change the Apex Core boundary.

The follow-on extension audit (`AC-DEV-014`) records the Freebuff agent/skill
surface as partial and preserves exact catalogs, dedicated skills, overrides,
packaging, and child routing as `NOT_PROVEN`. It reuses the bounded evidence
without installing ECC or changing executor neutrality.

The Agent/Skill Registry v1 (`AC-DEV-015`) provides stable executor-neutral
capability IDs for Task Passports and future routing. Its source mappings are
evidence claims only; Apex retains task semantics, scheduling, authority, and
verification, and unsupported mappings remain `NOT_PROVEN`.

Canonical backlog persistence (`AC-DEV-016`) is semantic and idempotent. A
no-op write preserves existing bytes, actual writes retain insertion order
instead of sorted-key churn, and readiness refresh advances revision only when
canonical state changes.

Capability matching (`AC-DEV-017`) is a pure candidate-plan projection. It does
not dispatch work or select an executor. Required unproven, unsupported, or
ambiguous matches fail closed; optional gaps remain visible. Scheduling,
authority, verification, retry/rework, and semantic success remain Apex-owned.

Execution admission (`AC-DEV-018`) consumes that Candidate Execution Plan as a
pure decision projection. It distinguishes capability blocks, unresolved
ambiguity, policy denial, and Human Gates from `ADMITTED`. A unique compatible
source may be selected for the task only; equal-quality sources require an
explicit policy before deterministic `SOURCE_ID_ASC` tie-breaking is allowed.
The decision preserves claim/evidence records, rationale, and rejected
candidates while keeping dispatch disabled and permanent executor selection
false. No runtime side effects occur, and Apex Core retains authority,
verification, retry/rework, and semantic-success ownership.

No secrets may appear in backlog, Passports, incidents, attempts, events,
evidence, or run summaries. Protected-main and CI governance remain mandatory
for repository changes.

## Durable operational use

```python
from development_control import ControlPlaneStore, DevelopmentControlPlane

store = ControlPlaneStore(backlog, passports, state)
plane = DevelopmentControlPlane(store, executor_id="generic-executor")
summary = plane.run(executor, concurrency=1)
```

The state path is supplied by the caller so deployments can choose an
appropriate durable location. Atomic file replacement prevents partial JSON
writes; this bounded implementation is not a distributed or multi-controller
registry.

## Evidence boundary

Implementation and seed decisions are recorded in
[`docs/evidence/DEVELOPMENT-CONTROL-PLANE-0015.md`](../evidence/DEVELOPMENT-CONTROL-PLANE-0015.md).
The accepted architecture and evidence sources remain authoritative for Core
semantics. In particular, authority activation, active-runtime recovery,
distributed fencing, stale lease reclamation, checkpoint safety, and other
`NOT_PROVEN` claims remain unchanged.
