# Architecture Status

Status vocabulary: **FROZEN**, **FREEZE_CANDIDATE**, **PROPOSED**, **INFERENCE**, **UNKNOWN**, **NOT_PROVEN**.

Reconciliation trace: [Architecture Reconciliation 0001](../evidence/ARCHITECTURE-RECONCILIATION-0001.md)
and the [comparative harvest](../evidence/AGENTIC-DEVELOPMENT-SYSTEMS-COMPARATIVE-HARVEST.md).

- **FROZEN**: intentionally fixed as current architecture law.
- **FREEZE_CANDIDATE**: accepted direction that remains subject to contract refinement.
- **PROPOSED**: not yet sufficiently designed or validated.
- **NOT_PROVEN**: required guarantee lacks direct evidence.

## Major decisions

| Item | Status | Note |
|---|---|---|
| Apex Code is a standalone competitive product | FROZEN | Product identity is independent of source projects. |
| DPT is optional | FROZEN | DPT is a capability, not Core. |
| Orchestration is optional and independent from DPT | FROZEN | Neither is a Core prerequisite. |
| Base/Core continues evolving | FROZEN | Core is not a completed/static tier. |
| Premium capabilities continue evolving | FROZEN | Capability evolution is independent of packaging. |
| Capability != Entitlement != Commercial Offering | FROZEN | Keep these concepts separate. |
| Architectural Core != Commercial Free | FROZEN | Architecture does not define pricing. |
| Commercial transparency | FROZEN | Premium and trial labels must be explicit. |
| Core safety primitives are not paywalled | FROZEN | Safety is foundational. |
| Optional capability failure isolation | FREEZE_CANDIDATE | Base Apex Code must remain usable. |
| OpenWork-derived shell is replaceable | FROZEN | Shell is a replaceable client boundary. |
| OpenCode is first runtime substrate | FROZEN | It is not product identity. |
| Strict downward dependency direction | FROZEN | Capability -> Core -> Adapter -> runtimes. |
| Full execution primitive set and invariant semantics | FREEZE_CANDIDATE | ExecutionEpoch, RuntimeLane, resource claims/leases, and exact state semantics remain under refinement. |
| Attempt is the unit of execution | FROZEN | A retry is a new Attempt. |
| ExecutionManifest is immutable once created | FROZEN | Exactly one immutable manifest belongs to each Attempt. |
| Runtime-specific session identifiers remain adapter-specific | FROZEN | Native session/process behavior stays in substrates. |
| AuthorityRevision is immutable | FROZEN | Prior authority history is not mutated. |
| Runtime completion != Task success | FROZEN | Core verification derives semantic Task state. |
| UNKNOWN is a valid semantic state | FROZEN | Unknown information must be preserved. |
| Task/Attempt/Authority execution primitives belong to Apex Core, not DPT | FROZEN | Capabilities extend but do not replace Core primitives. |
| Public command API and receipts | FREEZE_CANDIDATE | Conceptual contract pending implementation. |
| Full Execution Model v1 | FREEZE_CANDIDATE | Lifecycle and authority sequencing are design requirements; implementation guarantee remains NOT_PROVEN. |
| Execution API v1 | FREEZE_CANDIDATE | Conceptual surface pending contract refinement. |
| Runtime Adapter API / SPI | FREEZE_CANDIDATE | Bounded Runtime Adapter Contract v1 exists and is tested; stable cross-substrate API/SPI and guarantees remain under refinement. |
| Runtime lanes/session binding details | PROPOSED | Requires implementation evidence. |
| Core Reconciliation Loop | FREEZE_CANDIDATE | Core concept for comparing durable Attempt state, adapter facts, authority, and resource ownership; controller-loss behavior is not proven. |
| Projection Protocol / Layer | FREEZE_CANDIDATE | Non-authoritative consumer of canonical Core state and Events; visual/spatial implementation is not implied. |
| Authority activation and RuntimeLane/Attempt binding guarantee | NOT_PROVEN | Required sequencing is canonical; complete materialization, activation verification, and exact binding lack direct implementation evidence. |
| Controller-loss reconciliation guarantee | NOT_PROVEN | Startup recovery, stale/orphaned lane handling, and duplicate-start prevention remain unproven. |
| Independent semantic verification implementation | NOT_PROVEN | Core Verification is required conceptually, but implementation evidence for independent semantic verification does not exist. |

## Evidence discipline

Evidence labels are defined and preserved in the evidence documents. `NOT_PROVEN` is an explicit outcome, not a temporary synonym for PASS. In particular, the pre-execution authority materialization/binding chain remains `NOT_PROVEN` and must not be upgraded without direct evidence.
