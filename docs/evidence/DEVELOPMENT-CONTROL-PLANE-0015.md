# Development Control Plane Materialization Evidence

Delta: `AC-DEVELOPMENT-CONTROL-PLANE-0015`

Status: **IMPLEMENTED / MACHINE-VALIDATED / RECONCILED**

## Scope

This Delta materialized the smallest durable, executor-neutral backlog control
plane. The canonical reconciliation preserves `AC-DEV-010` as the deferred
global event-ordering task and allocates `AC-DEV-011` to the Goose CLI probe,
`AC-DEV-012` to the Freebuff CLI probe, and `AC-DEV-013` to their comparison.
The UI/Desktop probe is recorded separately in
`docs/evidence/GOOSE-UI-DELEGATION-0015.md`, while the CLI probe is recorded in
`docs/evidence/GOOSE-CLI-DELEGATION-0016.md`. The Freebuff and comparison
reports are recorded in `docs/evidence/FREEBUFF-CLI-DELEGATION-0017.md` and
`docs/evidence/EXECUTOR-CAPABILITY-COMPARISON-0018.md`. This reconciliation
does not change Apex Core, RuntimeAdapter, authority, verification, DPT, or
Orchestration semantics, does not select a permanent executor, and does not
install ECC.

## Canonical artifacts

| Artifact | Role |
|---|---|
| `development_control/backlog.json` | stable Development Task backlog and metadata |
| `development_control/passports/` | Task Passport v1 documents |
| `development_control/control_plane.py` | readiness, batching, attempts, incidents, run loop |
| `docs/governance/DEVELOPMENT-CONTROL-PLANE-v1.md` | current bounded contract |
| `development_control/README.md` | usage and boundary summary |

## Implemented behavior

- deterministic dependency/passport/policy/executor/resource eligibility;
- immutable persisted batch snapshots with conflict-safe resource claims;
- distinct development Attempts for execution, rework, and bounded recovery;
- task failure isolation from batch failure;
- stable incident fingerprints, corrective-task links, and quarantine;
- batch terminal-outcome and integration verification;
- autonomous multi-batch run loop with owner decision accumulation;
- systemic failure circuit breaker and concise durable run summaries;
- atomic JSON persistence without a database or permanent dependency;
- task-specific `owner_authorized` admission for explicitly authorized
  material tasks without lowering their risk or changing Passport constraints;
- per-member canonical backlog reload during a batch run, preventing stale
  snapshots from overwriting an earlier member's successful outcome.

## Seed reconciliation

The backlog was seeded from accepted Apex evidence. It included the current
implementation task (`AC-DEV-001`), unresolved authority/recovery and future
capability items, and `AC-DEV-007 — Goose UI/Desktop Parallel Delegation
Capability Probe`. The later probe completed with `VERIFIED` workflow status
and `PARTIAL` evidence; individual unsupported UI capabilities remain
`NOT_PROVEN` in its dedicated report.

Owner-authorized AC-DEV-002, AC-DEV-003, and AC-DEV-009 proofs completed with
`VERIFIED` workflow status while preserving `NOT_PROVEN` evidence claims.
AC-DEV-011 completed with `VERIFIED` workflow status and `PARTIAL` evidence.
Its CLI report directly observed asynchronous delegation, distinct child
identities, aggregation, and mixed success/failure; child cancellation,
dependency scheduling, and per-subtask provider/model assignment remain
unproven or unsupported at the observed surface.

AC-DEV-012 completed with `VERIFIED` workflow status and `PARTIAL` evidence.
The installed Freebuff CLI reached an isolated disposable TUI and exposed
parent agent/model surfaces, but child worker identity, concurrency, isolation,
aggregation, failure containment, retry/rework, dependency sequencing, and
per-task routing remain `NOT_PROVEN`. AC-DEV-013 completed with `VERIFIED`
workflow status and `PARTIAL` evidence, depends on AC-DEV-011 and AC-DEV-012,
and keeps executor choice open.

AC-DEV-014 completed with `VERIFIED` workflow status and `PARTIAL` evidence.
Its extension audit confirms only the bounded parent/source surfaces and keeps
exact native catalogs, dedicated skills, overrides, packaging, and child
routing `NOT_PROVEN`. It depends on AC-DEV-012 and AC-DEV-013; no ECC was
installed and no executor was selected.

AC-DEV-015 defines the executor-neutral Agent/Skill Registry v1 with stable
capability IDs and source mappings constrained by AC-DEV-011 through AC-DEV-014.
It is recorded as `VERIFIED` with `PARTIAL` evidence because future routing and
unsupported mappings remain unproven. No ECC installation or executor-specific
integration was introduced.

AC-DEV-016 adds deterministic canonical backlog persistence. Repeated
readiness/reconciliation cycles now preserve bytes and revision after semantic
convergence, while actual writes remain atomic and preserve task semantics and
history.

AC-DEV-017 adds executor-neutral required/optional capability requirements and
deterministic registry matching. Its Candidate Execution Plan preserves source
claim/evidence state, fails closed for required gaps or ambiguity, and never
dispatches or selects an executor.

AC-DEV-018 consumes the Candidate Execution Plan for a pure Execution Admission
Decision. It distinguishes capability, ambiguity, policy, and Human Gate
blocks from admission, preserves claim/evidence state and rejected-candidate
rationale, and selects only a task-scoped source. Equal-quality tie-breaking is
disabled by default and requires explicit `SOURCE_ID_ASC` policy. Dispatch,
runtime side effects, permanent executor selection, ECC installation, and Apex
Core ownership changes remain out of scope.

## Boundary checks

The implementation is separate from `apex_code/` and does not import Core
execution modules. It has no external dependencies. DPT and Orchestration
remain optional and independent. Backlog workflow status is separate from
evidence status, so existing `NOT_PROVEN` claims are preserved.

## Validation evidence

The focused control-plane tests cover Passport admission, verified
dependencies, resource-conflict batching, next-batch eligibility, distinct
Attempts, failure/rework and incidents, quarantine/circuit-breaker behavior,
batch dangling/unknown protection, owner decision accumulation, corrective
tasks, multi-batch continuation, owner-authorized material admission, and
stale-snapshot protection. Repository-wide Python tests and the
documentation validator are required before merge.
