# Execution Data Model v1

Status: **FREEZE_CANDIDATE**. Names and ownership below are the baseline; storage representation remains open.

## Core primitives

| Primitive | Meaning | Status |
|---|---|---|
| Execution | Public aggregate for one execution lifecycle | FROZEN |
| ExecutionRequest | Requested work and constraints | FROZEN |
| Task | Unit of work within an execution | FROZEN |
| Attempt | One execution try for a Task | FROZEN |
| ExecutionManifest | Immutable execution contract | FROZEN |
| ExecutionEpoch | Versioned execution coordination boundary | FREEZE_CANDIDATE |
| AgentSelection | Selected agent identity/configuration | FREEZE_CANDIDATE |
| ModelSelection | Selected model identity/configuration | FREEZE_CANDIDATE |
| RuntimeRequirement | Runtime capabilities/constraints required | FREEZE_CANDIDATE |
| RuntimeLane | Runtime scheduling/isolation lane | PROPOSED |
| RuntimeSessionBinding | Core-to-adapter session binding | FREEZE_CANDIDATE |
| PermissionEnvelope | Allowed authority scope | FROZEN |
| AuthorityRevision | Immutable authority decision revision | FROZEN |
| ExecutionBarrier | Gate that must release before execution | FROZEN |
| ResourceClaim | Requested exclusive/shared resource | FREEZE_CANDIDATE |
| ResourceLease | Granted time/version-bounded resource use | FREEZE_CANDIDATE |
| WorkspaceSnapshot | Workspace state associated with an attempt | FREEZE_CANDIDATE |
| AttemptResult | Facts and outcome reported for an attempt | FROZEN |
| Artifact | Durable output or evidence reference | FROZEN |
| Verification | Validation of result/artifact/claim | FROZEN |
| Event | Durable lifecycle fact for replay/streaming | FROZEN |

## Invariants

- Attempt is the unit of execution.
- Retry creates a new Attempt; it does not mutate the old Attempt into a retry.
- ExecutionManifest is immutable.
- Runtime-specific session IDs remain adapter-specific.
- AuthorityRevision is immutable.
- No execution occurs before authority verification and barrier release.
- Runtime completion is not Task success.
- UNKNOWN is a valid state and must be preserved.
- Task, Attempt, Authority, and Runtime belong to Apex Code Core, not DPT.
- Capabilities extend primitives; they do not replace them.

The model deliberately does not claim guarantees that are not yet proven by implementation evidence.
