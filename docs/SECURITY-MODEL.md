# Apex Code Security Model

Status: **PROPOSED** security boundary model. It describes required boundaries,
not a claim that all controls are implemented.

Reconciliation trace: [Architecture Reconciliation 0001](evidence/ARCHITECTURE-RECONCILIATION-0001.md)
and the [comparative harvest](evidence/AGENTIC-DEVELOPMENT-SYSTEMS-COMPARATIVE-HARVEST.md).

## Trust and authority boundaries

The Owner/user establishes intent and approval. Apex Core owns semantic
authority and safety decisions. `PermissionEnvelope` bounds allowed actions;
immutable `AuthorityRevision` records a specific decision; `ExecutionBarrier`
prevents actual execution until required checks release. Runtime adapters and
substrates translate and perform native operations within the Core-approved
context; they do not redefine authority semantics.

Relevant boundaries include:

- workspace and `WorkspaceSnapshot` isolation;
- RuntimeLane and runtime-session/process isolation;
- filesystem, process/tool, and network permissions;
- external services, provider credentials, and secret stores;
- capability boundaries for DPT, Orchestration, and advanced modules;
- Public API commands, idempotency, receipts, Events, artifacts, and audit
  evidence.

## Safety rules

Authority expansion requires explicit approval and appropriate security review.
Optional capability failure must not unnecessarily disable Base Apex Code.
Secrets must never be printed or committed. Security-sensitive changes require
negative tests, targeted validation, fail-closed behavior, and a recovery or
containment plan proportional to risk.

The architecture requires that the exact `AuthorityRevision` for the relevant
ExecutionEpoch be verified active and bound to the exact RuntimeLane/Attempt
context before barrier release and actual execution. OpenWork/OpenCode
experiments provide useful isolation/runtime evidence, but the complete
authority materialization → activation → immutable revision → Attempt binding
guarantee remains `NOT_PROVEN`. Documentation, an ADR, or a successful adjacent
test cannot upgrade that evidence state.

## Loss, resource, and projection safety

The Core Reconciliation Loop must compare durable Attempt state, Runtime Adapter
facts, authority/barrier state, and `RuntimeLane`/`ResourceClaim`/
`ResourceLease` ownership after startup or controller/process loss. Stale
`RUNNING` Attempts, missing or orphaned lanes, duplicate-start risk, and
`UNREACHABLE`/`UNKNOWN`/`LOST` facts must not be interpreted as permission or
success. Controller-loss recovery, stale-lease reclamation, and duplicate-start
prevention remain `NOT_PROVEN` until direct tests establish them.

Runtime or sandbox isolation is a substrate safety boundary, not by itself an
Apex `PermissionEnvelope`. Adapter controls may enforce filesystem, process,
network, or provider restrictions, while Core owns authority meaning and
semantic state.

Any visual or spatial projection consumes canonical Core state and Events. It
cannot own authority, approve execution, close a Task, or become a source of
truth when its state is stale or incomplete.

## Evidence vocabulary

Security claims must identify Claim State (`CURRENT`, `TARGET`, `CONSTRAINT`,
`DEBT`, `UNKNOWN`), Evidence Type (including `OBSERVED_RUNTIME_EVIDENCE` and
`NOT_PROVEN`), and Validation Result (`PASS`, `FAIL`, `NOT_RUN`, `BLOCKED`)
separately. Unknown or unavailable facts remain visible and safe failure is
preferred to an inferred permission grant.
