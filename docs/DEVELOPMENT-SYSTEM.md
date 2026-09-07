# Apex Code Development System

Status: **CURRENT** canonical overview. The bounded backlog-driven control
plane is materialized in
[`governance/DEVELOPMENT-CONTROL-PLANE-v1.md`](governance/DEVELOPMENT-CONTROL-PLANE-v1.md).
The earlier proposal and detailed contracts remain in
[`governance/DEVELOPMENT-CONTROL-SYSTEM-v1.md`](governance/DEVELOPMENT-CONTROL-SYSTEM-v1.md), especially the [Task System](governance/TASK-SYSTEM-v1.md),
[Task Passport](governance/TASK-PASSPORT-v1.md), [validation governance](governance/VALIDATION-GOVERNANCE-v1.md),
and [handoff contract](governance/HANDOFF-CONTRACT-v1.md).

## Controlled flow

```text
Owner Intent
    ↓
Development Task
    ↓
Task Passport
    ↓
PLAN / approval
    ↓
READY
    ↓
ExecutionRequest
    ↓
Core Task
    ↓
Attempt
    ↓
ExecutionManifest
    ↓
Runtime
    ↓
AttemptResult
    ↓
Validation
    ↓
Review / Acceptance
    ↓
DONE
    ↓
Completion / Evidence
    ↓
Learning
```

Development Task is a governance/work-management entity. Core Task remains an
Apex Execution Model primitive. A Development Task may map to one or more Core
Tasks and Attempts; it does not absorb runtime identity. A Task Passport is a
revisioned bounded contract for that Development Task. It is not a Core Task,
Attempt, ExecutionManifest, ExecutionEpoch, AttemptResult, or Completion Report.

## Admission and lifecycle

The lightweight workflow is:

`DRAFT → PLANNING → READY → IN_PROGRESS → VALIDATING → REVIEW → DONE`

Side states are `BLOCKED`, `NEEDS_DECISION`, `FAILED`, `CANCELLED`, and
`SUPERSEDED`. Passport admission fails closed as `PASSPORT_INCOMPLETE` when
information required for safe execution is missing, contradictory, or blocked.
Readiness is proportional to scope and risk; trivial work does not require
maximal ceremony, but an incomplete material/high-risk package cannot execute.

Milestone facts remain separate: `IMPLEMENTED`, `MACHINE_VALIDATED`,
`HUMAN_ACCEPTED`, `OPERATIONALLY_VERIFIED`, and `LEARNING_CAPTURED`.
`IMPLEMENTED != DONE` and `MACHINE_VALIDATED != DONE`; `DONE` requires the
applicable Acceptance Contract. Development lifecycle state is not Attempt
runtime state.

## Planning, permissions, and evidence

PLAN inspects, identifies affected contracts, scope, dependencies, acceptance,
validation, risk, resource cost, and stopping conditions. EXECUTE mutates only
the accepted package. Decision Class (`ROUTINE`/`MATERIAL`/`CRITICAL`), Risk
(`LOW`/`MEDIUM`/`HIGH`/`CRITICAL`), and Resource Class
(`STANDARD`/`ELEVATED`/`INTENSIVE`) are separate axes. Use the lowest responsible
resource cost; material resource expansion can require Owner escalation.

Acceptance is not an agent assertion. Validation results are `PASS`, `FAIL`,
`NOT_RUN`, or `BLOCKED`, separate from Claim State and Evidence Type. Use the
narrowest reliable validation first. System-First Correction asks whether a
recurring defect is enabled by a missing shared control; if so, fix and test
the control and retain the visible defect as an acceptance fixture.

Owner escalation is required for frozen architecture changes, authority or
security expansion, destructive/irreversible actions, production impact,
conflicting canonical sources, unclear acceptance, material product or
commercial decisions, and critical risk.

## Work and branch boundaries

The canonical development backlog and Passport collection now provide the
bounded active-work owner for this workflow. Runtime state is durable at the
caller-selected state path; it is not a second Core ledger. Current State is a
bounded resume snapshot, Handoff is transfer context, Completion Report is a
result, and Evidence Report is an immutable observation snapshot. Roadmap is
evolution, not backlog. A branch records purpose, base, Task/Passport, receiver,
and closure; the normal path is branch → PR → validation/review → merge → target
verification → retirement.

The control plane admits only complete Passports with verified dependencies,
closed Human Gates, compatible executors, permitted risk, and conflict-safe
resource claims. Its run loop continues across batches; failure returns a task
to backlog or quarantine and creates incident evidence. Human Gates accumulate
in an Owner Decision Queue while unrelated eligible work continues. See the
current bounded contract for the complete status vocabulary and non-claims.

Development Control System works without DPT and Orchestration. Either may
consume these generic contracts later, but Apex Core does not depend on them.
