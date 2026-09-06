# Apex Code Terminology

Status: **PROPOSED** glossary. Formal architecture documents and accepted ADRs
own contract meaning where this glossary links to them.

| Term | Canonical meaning |
|---|---|
| Apex Code | Standalone product for governed agent execution. |
| Product Shell | Replaceable client/presentation layer consuming the Public API. |
| Apex Core | Runtime-neutral execution, authority, safety, evidence, and semantic-state core. |
| Execution | Public aggregate for one execution lifecycle. |
| ExecutionRequest | Requested work and constraints that initiate an Execution. |
| Development Task | Governance/work-management entity for a desired development outcome; separate from Core Task. |
| Core Task | Runtime execution unit within an Execution; not a development backlog item. |
| Task Passport | Revisioned bounded Development Task contract for scope, requirements, gates, and acceptance; not runtime identity. |
| Attempt | One execution try for a Core Task; retry creates a new Attempt. |
| ExecutionEpoch | Distinct interval within an Attempt for future-safe authority/pause/resume/recovery boundaries; exact state semantics remain under refinement. |
| ExecutionManifest | Immutable birth certificate/contract for exactly one Attempt. |
| AttemptResult | Runtime facts and outcome reported for an Attempt; not a Completion Report. |
| Completion Report | Human-facing result record for a development change/work package. |
| Evidence Report | Immutable observation/proof snapshot with provenance. |
| Runtime Adapter | Translation boundary between Core semantics and a runtime substrate. |
| Runtime Lane | Core abstraction for runtime scheduling/isolation context. |
| Runtime Session | Native substrate session/process identity; not an Attempt. |
| RuntimeSessionBinding | Adapter/Core boundary binding an Attempt context to an adapter session. |
| WorkspaceSnapshot | Workspace state associated with an Attempt. |
| PermissionEnvelope | Allowed authority scope for an execution/change. |
| AuthorityRevision | Immutable revision of an authority decision. |
| ExecutionBarrier | Core gate that must release before actual execution. |
| ResourceClaim | Requested shared/exclusive resource use. |
| ResourceLease | Granted bounded resource use. |
| Capability | Optional or core-extending function exposed through a contract. |
| Capability Module | Implementation boundary for a capability; it does not replace Core primitives. |
| Entitlement | Whether a user/context may access a capability. |
| Commercial Offering | Product/package representation of value; separate from capability and entitlement. |
| Trial | Time/usage-limited access state; premium trials are labeled `Premium + Trial`. |
| Orchestration | Optional coordination capability that may consume Core/DCS contracts. |
| DPT | Optional Development/Product capability; not Apex Core identity or prerequisite. |
| Advanced Routing | Optional selection/routing capability above Core. |
| Verification | Evaluation of results, artifacts, or claims against a contract. |
| Recovery | Handling/resumption/rollback behavior after failure; details remain subject to future contracts. |
| Development Control System | Governance system for developing Apex Code, not the runtime engine. |
| Work Registry | Future canonical owner of active work state; implementation is P2. |
| Current State | Bounded resume snapshot, not a full backlog or history. |
| Handoff | Transfer context and pointers to a receiver. |
| ADR | Architecture Decision Record: WHY a durable/material decision was made. |
| Roadmap | Product/system evolution across past, present, and future; not execution authority. |
| Claim State | `CURRENT`, `TARGET`, `CONSTRAINT`, `DEBT`, or `UNKNOWN`. |
| Evidence Type | Apex evidence vocabulary: `SOURCE_CODE_EVIDENCE`, `DOCUMENTATION_EVIDENCE`, `OBSERVED_REPOSITORY_STATE`, `OBSERVED_RUNTIME_EVIDENCE`, `INFERENCE`, `UNKNOWN`, `NOT_PROVEN`. |
| Validation Result | `PASS`, `FAIL`, `NOT_RUN`, or `BLOCKED`. |
| Decision Class | `ROUTINE`, `MATERIAL`, or `CRITICAL` approval/governance level. |
| Risk | `LOW`, `MEDIUM`, `HIGH`, or `CRITICAL` consequence/blast-radius level. |
| Resource Class | `STANDARD`, `ELEVATED`, or `INTENSIVE` responsible investigation/execution cost. |
| NOT_PROVEN | Required guarantee lacks direct evidence; documentation cannot upgrade it. |

`Task`, `Attempt`, `Task Passport`, `ExecutionManifest`, `AttemptResult`, and
Completion Report are intentionally non-interchangeable.
