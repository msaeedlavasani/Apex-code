# Apex Code

Apex Code is a standalone product for safe, observable, governed agent
execution. Its value is a runtime-neutral execution core with explicit
authority, artifacts, verification, recovery direction, and replaceable
runtime and shell boundaries.

The Base/Core product continues evolving. DPT, Orchestration, Advanced Routing,
and other premium capabilities are optional consumers or extensions; they do
not define Apex Code or become prerequisites for its base experience. OpenCode
is the first runtime substrate, not product identity. Commercial packaging is
separate from architecture: capability, entitlement, and commercial offering
are different concepts.

This repository is architecture-first with a first bounded executable slice;
the broader product and runtime contracts remain under implementation. Start
with the [canonical documentation index](docs/INDEX.md), or choose a route:

- Human/product orientation: [Product](docs/PRODUCT.md) and [Roadmap](ROADMAP.md)
- Development agent: [AGENTS.md](AGENTS.md) and [Context Map](docs/CONTEXT-MAP.md)
- System orientation: [System Design](docs/SYSTEM-DESIGN.md)
- Formal architecture: [architecture status](docs/architecture/05-ARCHITECTURE-STATUS.md)
- Development control: [Development System](docs/DEVELOPMENT-SYSTEM.md)
- Evidence and proof limits: [OpenWork feasibility](docs/evidence/OPENWORK-FEASIBILITY.md) and [open questions](docs/evidence/OPEN-QUESTIONS.md)

The formal baseline preserves `NOT_PROVEN` where implementation evidence is
missing. In particular, the complete authority materialization, activation,
and binding chain is not proven by documentation alone. The bounded slice uses
Core-mediated artifact I/O and does not establish the full product/runtime
implementation.

The first local Product Shell can be launched with `python3 -m apex_code.shell`.
It connects project selection and bounded task commands to canonical Apex Core
through a local application boundary. The shell is a projection: durable
execution state, authority, verification, and artifacts remain Core-owned. The
OpenWork source pin and divergence boundary are recorded in
[docs/apex/FORK_BOUNDARY.md](docs/apex/FORK_BOUNDARY.md).
