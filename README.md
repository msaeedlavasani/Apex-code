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

The OpenWork-derived Product Shell can be built and launched locally:

```text
cd product_shell/openwork && npm install && npm run build
python3 -m apex_code.shell --ui openwork
```

It connects project selection and bounded task commands to canonical Apex Core
through a local application boundary. The shell is a projection: durable
execution state, authority, verification, and artifacts remain Core-owned. The
original lightweight shell remains available as a test harness with
`python3 -m apex_code.shell --ui bootstrap`. The pinned OpenWork source slice,
license boundary, and upstream-sync procedure are recorded in
[docs/apex/FORK_BOUNDARY.md](docs/apex/FORK_BOUNDARY.md).

The first local desktop container can be run and packaged with:

```text
cd product_shell/desktop && npm ci
npm run dev
npm run package:dir
```

The desktop process starts the bounded Apex service on loopback, reuses the
same OpenWork renderer, and does not become an execution or authority owner.
Packaging is currently an unsigned, development-quality macOS directory app;
signing, notarization, and distribution automation are intentionally out of
scope.

Provider/model settings are available in the desktop shell for the bounded
OpenCode MVP. The desktop main process stores credentials with OS-backed
Electron `safeStorage` when available and exposes only configured status to the
renderer. Provider/model selection is non-secret product intent; Core records
the selected provider/model provenance while the RuntimeAdapter injects only
the selected credential into a sanitized child environment. There is no
ambient credential fallback. See
[Provider Architecture](docs/apex/PROVIDER-ARCHITECTURE.md) and
[BYOK evidence](docs/evidence/PROVIDER-BYOK-0013.md).
