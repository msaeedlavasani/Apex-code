# Modular Product Architecture v1

Status: **FREEZE_CANDIDATE**.

## Layers

| Layer | Responsibility | Status |
|---|---|---|
| Product Shell | UI, workflows, presentation, and Public API consumption | FREEZE_CANDIDATE |
| Apex Core | Execution, Task, Attempt, authority, runtime-neutral semantics, evidence, and safety primitives | FROZEN |
| Capability Layer | DPT, orchestration, and advanced capabilities through Capability SPI | FREEZE_CANDIDATE |
| Runtime Adapter API | Stable facts/commands boundary to runtime substrates | FROZEN |
| Runtime Substrates | OpenCode first; Goose and future runtimes possible | PROPOSED |

## Rules

DPT is optional and is not part of the Core. Orchestration is optional, independently deployable conceptually, and is not a prerequisite for Core execution. Optional capability failure is isolated from Base Apex Code.

OpenWork-derived shell components may be replaced without changing the Core contract. OpenCode is the first runtime substrate only. Neither repository is Apex Code identity.

The Core owns semantic state and safety decisions. Adapters expose runtime facts and adapter-specific identifiers. Commercial offerings may package capabilities differently, but pricing plans are not encoded in this architecture.

## Extension boundaries

- Public Shell -> Public API
- DPT/Orchestration -> Capability SPI
- OpenCode/Goose/future runtimes -> Runtime Adapter SPI

No extension may bypass authority verification, barrier release, or Core-owned state transitions.
