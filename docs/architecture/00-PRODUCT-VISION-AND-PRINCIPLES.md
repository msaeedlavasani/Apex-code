# Product Vision and Principles

Status: **FROZEN** for this baseline.

## Product identity

Apex Code is a standalone competitive product: a durable execution system for agent work, with explicit authority, runtime, evidence, and artifact boundaries. OpenWork-derived shell technology is replaceable. OpenCode is the first runtime substrate, not the product identity.

The Base/Core product continues evolving. Premium capabilities also continue evolving. Commercial packaging must not be confused with the architecture:

- Capability != Entitlement != Commercial Offering.
- Architectural Core != Commercial Free.
- Commercial transparency is mandatory.
- Premium trials must be labeled **Premium + Trial** from the start.

## Modular principles

- DPT is optional.
- Orchestration is optional and independent from DPT.
- DPT, orchestration, and advanced capabilities depend downward on Apex Core; they do not merge into it.
- Core safety primitives are not paywalled.
- Failure of an optional capability must not break Base Apex Code.
- Capabilities extend primitives; they do not replace them.
- Runtime adapters report facts; Apex Core owns semantic state.

## Dependency direction

```text
DPT / Orchestration / Advanced capabilities
                    -> Apex Core
                    -> Runtime Adapter API
                    -> OpenCode / Goose / future runtimes
```

The direction is strictly downward. Product shells consume the Public API; they are replaceable clients rather than sources of core semantics.
