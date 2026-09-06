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
Task Passport
        ↓
Planning / admission
        ↓
Development Task → one or more Apex Execution Tasks
        ↓                         ↓
review / validation          Attempt → ExecutionManifest
        ↓                         ↓
Completion Report ← Verification / AttemptResult / Artifacts
```

The recommended mapping is explicit: a Development Task is a governance entity that can map to one or more Core Execution Tasks. This preserves external users' Core `Task` semantics while allowing planning, review, and acceptance to span multiple runtime executions.

## Context routing and bounded state

The proposed rehydration path is:

```text
AGENTS.md → Context Map → Current State → Task / Passport route → canonical sources
```

`Context Map` is preferred over `AI_CONTEXT_MAP.md` as the future Apex name because it is substrate-neutral; the word AI describes a consumer, not the ownership of the routing contract. A new agent should receive minimum sufficient context, not the whole repository, chat history, or model memory.

`Current State` is a small machine-readable resume snapshot: active milestone, active/next task IDs, blockers, active gates, last meaningful validation, constraints, and links to canonical sources. It must not duplicate the Work Registry, history, architecture, reports, or Task Passports. It is a P1 candidate: useful before the first Runtime Adapter, but not required to begin a docs-only design review.

The Work Registry is the sole active work-state owner. Reports are immutable evidence snapshots; Handoffs transfer context; Current State resumes work; the Task Passport defines bounded work/execution requirements. None of these may become a parallel backlog.

## Proposed v1 decisions

| Decision | Status | Disposition |
|---|---|---|
| Keep DCS independent from DPT and Orchestration | PROPOSED | Adopt as a boundary requirement |
| Use a Task Passport as a revisioned development-control contract | PROPOSED | Adapt DPT passport concept; do not make it a runtime manifest |
| Use composable change-classification flags | PROPOSED | Adapt Home Fit categories for generic Apex changes |
| Use PLAN/EXECUTE selectively by scope and risk | PROPOSED | Adapt, with no ceremony for trivial safe edits |
| Require evidence-backed completion | PROPOSED | Adopt Result != Completion discipline |
| Keep current Apex evidence vocabulary | PROPOSED | Preserve; add separate claim-state labels only if useful |
| Use one canonical backlog projection | PROPOSED | Start with a document-backed registry; defer a task engine |
| Add explicit validation result states | PROPOSED | `PASS`/`FAIL`/`NOT_RUN`/`BLOCKED`, separate from evidence type |
| Separate decision class, risk, and resource class | PROPOSED | Avoid redundant gates while governing expensive work |
| Treat system-first correction as a development rule | PROPOSED | Repeated symptoms trigger control-gap analysis |

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

## Non-claims

This is a proposed development-control design. It does not freeze new architecture, prove authority materialization, implement a task registry, or authorize runtime/product changes.
