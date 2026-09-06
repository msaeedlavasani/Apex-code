# Architecture Status

Status vocabulary: **FROZEN**, **FREEZE_CANDIDATE**, **PROPOSED**, **INFERENCE**, **UNKNOWN**, **NOT_PROVEN**.

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
| Execution primitive set and invariants | FROZEN | See data model and execution model. |
| Public command API and receipts | FREEZE_CANDIDATE | Conceptual contract pending implementation. |
| Runtime lanes/session binding details | PROPOSED | Requires implementation evidence. |

## Evidence discipline

Evidence labels are defined and preserved in the evidence documents. `NOT_PROVEN` is an explicit outcome, not a temporary synonym for PASS. In particular, the pre-execution authority materialization/binding chain remains `NOT_PROVEN` and must not be upgraded without direct evidence.
