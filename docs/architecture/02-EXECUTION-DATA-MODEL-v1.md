# Execution Data Model v1

Status: **FREEZE_CANDIDATE**. Names and ownership below are the baseline; storage representation remains open.

Reconciliation trace: [Architecture Reconciliation 0001](../evidence/ARCHITECTURE-RECONCILIATION-0001.md)
and the [comparative harvest](../evidence/AGENTIC-DEVELOPMENT-SYSTEMS-COMPARATIVE-HARVEST.md).

## Core primitives

| Primitive | Meaning | Status |
|---|---|---|
| Execution | Public aggregate for one execution lifecycle | FROZEN |
| ExecutionRequest | Requested work and constraints | FROZEN |
| Task | Unit of work within an execution | FROZEN |
| Attempt | One execution try for a Task | FROZEN |
| ExecutionManifest | Immutable execution contract | FROZEN |
| ExecutionEpoch | Distinct execution interval within an Attempt | FREEZE_CANDIDATE |
| AgentSelection | Selected agent identity/configuration | FREEZE_CANDIDATE |
| ModelSelection | Selected model identity/configuration | FREEZE_CANDIDATE |
| RuntimeRequirement | Runtime capabilities/constraints required | FREEZE_CANDIDATE |
| RuntimeLane | Runtime scheduling/isolation lane | PROPOSED |
| RuntimeSessionBinding | Binding between an Attempt context and an adapter session | FREEZE_CANDIDATE |
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
- Every Attempt has exactly one immutable ExecutionManifest, created for that Attempt.
- A Task may have multiple historical ExecutionManifests, one per Attempt over its lifetime.
- Runtime-specific session IDs remain adapter-specific.
- AuthorityRevision is immutable.
- No Attempt may enter actual execution/RUNNING before the exact AuthorityRevision for its ExecutionEpoch is verified active and bound to its RuntimeLane/Attempt context, followed by barrier release.
- Runtime completion is not Task success.
- UNKNOWN is a valid state and must be preserved.
- Task, Attempt, Authority, and Runtime belong to Apex Code Core, not DPT.
- Capabilities extend primitives; they do not replace them.

The model deliberately does not claim guarantees that are not yet proven by implementation evidence.

## Reconciled boundaries

`ExecutionEpoch` is a bounded continuation interval inside one Attempt. It may
be opened for an approved `AuthorityRevision` change, runtime/session
reconnect, bounded resume, checkpoint continuation, or recovery continuation.
It does not replace Attempt identity, and a provider checkpoint is not itself an
ExecutionEpoch. Its exact state machine and side-effect rules remain
`FREEZE_CANDIDATE` and require later evidence.

`ResourceClaim` expresses the Core semantic request for shared or exclusive use
of a workspace, RuntimeLane, or other resource. `ResourceLease` expresses the
granted bounded use. Core owns claim meaning, conflict semantics, and the
relationship to Attempt/Epoch; an adapter or control plane may materialize the
substrate reservation. Stale-lease reclamation and controller-loss behavior
remain `NOT_PROVEN` until tested.

The [Reconciliation Loop](03-EXECUTION-MODEL-v1.md#reconciliation-loop) uses
these primitives to compare durable Attempt state, adapter facts, authority
state, and resource ownership. It must not infer safe ownership from a local
lock, idle session, or missing runtime.
