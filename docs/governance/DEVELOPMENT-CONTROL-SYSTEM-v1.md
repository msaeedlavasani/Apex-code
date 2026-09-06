# Apex Code Development Control System v1

Status: **PROPOSED**. This document governs development of Apex Code; it is not the Apex Code runtime execution engine and is not DPT.

## Purpose and boundary

The Development Control System (DCS) makes repository work inspectable, scoped, reviewable, and verifiable before product implementation begins. It owns development intent, planning, admission, change classification, validation selection, handoffs, completion reporting, and repository workflow.

It does not own `Execution`, `ExecutionRequest`, `Attempt`, `ExecutionManifest`, runtime sessions, Runtime Adapter behavior, orchestration, or DPT product semantics. It may produce inputs for Apex Core execution, but it cannot redefine Core primitives.

```text
Apex Code Development Control System
├── Repository Brain       durable guidance and ownership boundaries
├── Governance             source precedence, architecture, ADR, security
├── Work Management        development task, passport, backlog, lifecycle
├── Execution Governance   admission, authority inputs, validation, evidence
└── Repository Workflow    branch, PR, CI, review, merge, retirement
```

## Responsibility boundaries

| Area | DCS owns | DCS does not own |
|---|---|---|
| Repository Brain | development guidance and domain ownership | runtime semantic state or duplicated architecture law |
| Governance | rules for change, review, evidence, and source precedence | commercial packaging or DPT governance |
| Work Management | development intent, passport, backlog projection, workflow state | Core Task/Attempt identity |
| Execution Governance | admission, validation contract, handoff, completion evidence | runtime execution result or semantic Task success |
| Repository Workflow | branches, PRs, CI gates, merge/retirement | product release behavior not yet designed |

## Core relationships

```text
Development Intent
        ↓
Development Task
        ↓
Task Passport
        ↓
Planning / admission
        ↓
ExecutionRequest → one or more Apex Core Tasks
                         ↓
                    Attempt → ExecutionManifest
                         ↓
Completion Report ← Verification / AttemptResult / Artifacts
```

Owner decision D01 makes the boundary canonical for this proposal: a Development Task is separate from an Apex Core Execution Task. The Development Task owns objective, plan, scope, dependencies, branch/PR, review, acceptance, handoff, and learning. Its Task Passport is the bounded, revisioned contract for the package. It maps through `ExecutionRequest` to one or more Core `Task` instances; Core `Task`, `Attempt`, and `ExecutionManifest` retain their existing semantics.

## Context routing and bounded state

The proposed rehydration path is:

```text
AGENTS.md → Context Map → Current State → Task / Passport route → canonical sources
```

The accepted future canonical name is `docs/CONTEXT-MAP.md`, not `AI_CONTEXT_MAP.md`. It is substrate-neutral and routes to minimum sufficient context. A new agent should not load the whole repository, historical reports, chat history, or model memory as authority.

`Current State` is accepted as a P1 bounded, eventually machine-readable resume snapshot: active milestone, active/next task IDs, blockers, active gates, last meaningful validation, constraints, and canonical links. It must not duplicate the Work Registry, history, architecture, reports, or Task Passports.

The Work Registry is the sole active work-state owner; a full machine-readable implementation is P2. Reports are immutable evidence snapshots; Handoffs transfer context; Current State resumes work; the Task Passport defines bounded work/execution requirements. None may become a parallel backlog.

The accepted lightweight workflow is `DRAFT → PLANNING → READY → IN_PROGRESS → VALIDATING → REVIEW → DONE`, with side states `BLOCKED`, `NEEDS_DECISION`, `FAILED`, `CANCELLED`, and `SUPERSEDED`. Separate milestone facts are `IMPLEMENTED`, `MACHINE_VALIDATED`, `HUMAN_ACCEPTED`, `OPERATIONALLY_VERIFIED`, and `LEARNING_CAPTURED`; `IMPLEMENTED` and `MACHINE_VALIDATED` never imply `DONE`, and applicable Acceptance Contract gates determine closure.

## Proposed v1 decisions

| Decision | Status | Disposition |
|---|---|---|
| Keep DCS independent from DPT and Orchestration | ACCEPTED BOUNDARY | Owner decision D18; DPT and Orchestration may consume contracts but are not dependencies |
| Separate Development Task from Core Task | ACCEPTED BOUNDARY | Owner decision D01 |
| Use a revisioned Task Passport with fail-closed readiness | ACCEPTED BOUNDARY | Owner decisions D02/D03; incomplete material/high-risk packages are `PASSPORT_INCOMPLETE` |
| Establish root `AGENTS.md` and `ROADMAP.md` | ACCEPTED P0 DOCUMENTATION | Owner decisions D04/D20; materialization is a later delta |
| Use `docs/CONTEXT-MAP.md` | ACCEPTED DESIGN | Owner decision D05; retrieval manifest remains deferred |
| Use one canonical active Work State owner | ACCEPTED PRINCIPLE | Work Registry implementation is P2 |
| Use lightweight workflow plus separate milestone facts | ACCEPTED MODIFIED | Owner decision D08 |
| Use composable change-classification flags | PROPOSED | Adapt Home Fit categories for generic Apex changes |
| Use PLAN/EXECUTE selectively by scope and risk | PROPOSED | Adapt, with no ceremony for trivial safe edits |
| Require evidence-backed completion | PROPOSED | Adopt Result != Completion discipline |
| Keep current Apex evidence vocabulary | PROPOSED | Preserve; add separate claim-state labels only if useful |
| Use one canonical active Work State owner | ACCEPTED PRINCIPLE | Historical reports, handoffs, Current State, and Passports cannot become competing backlogs; machine registry is P2 |
| Add explicit validation result states | ACCEPTED DESIGN | `PASS`/`FAIL`/`NOT_RUN`/`BLOCKED`, separate from Claim State and Apex Evidence Type |
| Separate decision class, risk, and resource class | ACCEPTED DESIGN | ROUTINE/MATERIAL/CRITICAL; LOW/MEDIUM/HIGH/CRITICAL; STANDARD/ELEVATED/INTENSIVE |
| Treat system-first correction as a development rule | ACCEPTED DESIGN | Correct the missing shared control, add regression/evaluation, retain the visible issue as fixture |
| Use an ADR system | ACCEPTED DESIGN | `docs/adr/`; ADR records WHY, architecture docs WHAT, AGENTS HOW |
| Defer full Repository Brain tree and Retrieval Manifest | ACCEPTED DEFERRED | Avoid duplicate sources before canonical documentation exists |
| Use lowest responsible resource cost | ACCEPTED PRINCIPLE | Numeric bands and mandatory Resource Approval Request remain deferred |

All detailed schemas and machine enforcement remain PROPOSED unless separately accepted. The Apex authority materialization/binding guarantee remains `NOT_PROVEN`.

## Relationship to optional capabilities

Orchestration may later read passports, dependencies, requirements, validation contracts, and handoffs to schedule work. DPT may consume the same interfaces as an optional capability. Neither is required for DCS operation, and no dependency from Apex Core to either capability is created:

```text
DPT / Orchestration (optional consumers)
                 ↓
Apex Code Development Control System
                 ↓
Apex Core Public API / Core contracts
```

Branch governance remains explicit: every development branch records purpose, base, Task/Passport owner, receiver, and closure condition. Completion selects `MERGE`, `RETAIN WITH REASON`, `ARCHIVE`, or `DELETE`; merged short-lived branches are normally deleted only after remote-main verification. Commit, push, merge, and deploy are separate permission decisions.

## Product Evolution Roadmap boundary

Owner decision D20 accepts `ROADMAP.md` as P0 canonical documentation. The Roadmap describes evidence-backed past evolution, the present maturity frontier, and directional future phases. It is not the active backlog, Work Registry, Task Passport collection, implementation checklist, or execution authority; a future item never authorizes work without an active Development Task and accepted scope.

The proposed horizons are: past repository/architecture/governance/DCS foundations; present canonical development foundation (`AGENTS.md`, `CONTEXT-MAP`, Product, System Design, Terminology, Security, Testing, and Roadmap documentation); and future Runtime Adapter Contract, safe execution, OpenCode adapter, vertical slice, shell integration, recovery hardening, Orchestration, routing, DPT capability, and commercial maturity. The exact phase ordering remains directional. Roadmap statuses should stay distinct from task lifecycle, using the smallest later-approved vocabulary for historical, current, planned, future, and deferred direction.

## Non-claims

This is a proposed development-control design. It does not freeze new architecture, prove authority materialization, implement a task registry, or authorize runtime/product changes.
