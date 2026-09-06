# Apex Code Development Task System v1

Status: **PROPOSED**.

## Development Task versus Execution Task

Two alternatives were evaluated:

| Option | Consequence |
|---|---|
| A. One shared Task primitive with context metadata | Simple mapping, but planning/review/acceptance can leak into Core Task semantics and confuse retries, runtime identity, and external API users. |
| B. Development Task mapped explicitly to Core Execution Task(s) | Adds a boundary and mapping record, but preserves Core semantics, supports multi-step work and review, and lets DPT/Orchestration consume generic work metadata without owning Core. |

Recommendation: **Option B, PROPOSED**. A Development Task owns development intent, scope, dependencies, acceptance, review, and change/risk metadata. It may map one-to-one or one-to-many to Core `Task` instances. A Core Task remains executor-independent runtime work; an `Attempt` remains one execution try; retries do not create new Development Tasks automatically.

## Admission and readiness

`PASSPORT_INCOMPLETE` is a fail-closed development readiness state, not a Core runtime state. It applies when mandatory passport fields or dependency evidence are missing or contradictory. A task cannot enter `READY` or authorize execution while it is `PASSPORT_INCOMPLETE`.

Mandatory before admission: identity/revision, objective, allowed and forbidden scope, affected contracts, dependencies, change/risk/resource classification, acceptance criteria, validation plan, evidence requirements, branch/base/worktree context, required capabilities, authority-envelope requirements, stopping conditions, owner/reviewer, and receiver/learning destination. Broader evidence, resource, and operational fields become mandatory in proportion to risk; they are not all required for a trivial docs task.

Passport readiness also requires accepted dependencies, a known worktree/base, a valid permission envelope input, and no unresolved stopping condition. It does not prove runtime authority materialization.

This recommendation is compatible with DPT because DPT can consume the mapping and passport, while Apex Code remains independent of DPT. It also supports future external users who need Core execution without Apex-specific development workflow.

## Canonical backlog

V1 should use one human-readable, machine-projectable `docs/TASKS.md`-style registry only after a separate owner-approved implementation delta. Until then, the DCS design is the canonical proposal and does not create a task engine, database, or second backlog. GitHub Issues may mirror or discuss work, but must not silently become a competing source of execution eligibility.

## Proposed development lifecycle

```text
DRAFT → READY_FOR_PLAN → PLANNING → PLANNED → READY
      → IN_PROGRESS → VALIDATING → REVIEW → DONE
```

Side states: `BLOCKED`, `NEEDS_DECISION`, `FAILED`, `CANCELLED`, `SUPERSEDED`.

| State | Owner and meaning |
|---|---|
| DRAFT | author; incomplete intent |
| READY_FOR_PLAN | owner/agent; scope is sufficient to plan |
| PLANNING | planner; dependencies, acceptance, risk, and validation are being defined |
| PLANNED | reviewer/owner; plan is coherent, not yet admitted |
| READY | admission check passed; authority and required review gates are available |
| IN_PROGRESS | bounded mutation is authorized on a task branch |
| VALIDATING | implementation is stable enough for declared checks |
| REVIEW | PR and architecture/security/owner review as required |
| DONE | acceptance evidence, validation, and decision are recorded |
| BLOCKED | proven prerequisite prevents progress |
| NEEDS_DECISION | owner judgment or protected decision is required |
| FAILED | an Attempt or validation failed; non-terminal until disposition is recorded |
| CANCELLED | explicitly stopped; no new work may start |
| SUPERSEDED | replaced by a linked task/decision; history retained |

Human authority owns product, commercial, protected architecture, destructive, security-widening, and production decisions. Agents may advance deterministic states within scope. `DONE` requires accepted evidence; an executor or CI result alone is not completion.

The lifecycle keeps implementation and acceptance distinct. `IMPLEMENTED`, `MACHINE_VALIDATED`, `HUMAN_ACCEPTED`, `OPERATIONALLY_VERIFIED`, and `LEARNING_CAPTURED` are proposed milestone facts attached to the task/report, not automatically additional workflow states. `IMPLEMENTED` never equals `DONE`; operational verification is required only when the change class requires it.

Decision class, risk, and resource class are separate dimensions. Proposed decision classes are `ROUTINE`, `MATERIAL`, and `CRITICAL`; risk remains `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`; resource class is `STANDARD`, `ELEVATED`, or `INTENSIVE`. A separate Resource Approval Request is deferred until expensive work exists.

## Core mapping

Development lifecycle state is not runtime state. Planning can create or map Core `ExecutionRequest`/Task inputs; execution creates Attempts and immutable manifests; verification consumes AttemptResult/Artifacts; the development task closes only after its acceptance contract is satisfied.
