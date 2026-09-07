# Apex Code Documentation Index

This is the canonical navigation and ownership map. Read the smallest route
that answers the task; use links to the owning document instead of creating a
second source of truth.

## Entry documents

| Document | Purpose / owner | Status | Read when | Must not duplicate |
|---|---|---|---|---|
| [`README.md`](../README.md) | Human repository/product orientation | Current entry | First human visit | Full contracts or policy |
| [`AGENTS.md`](../AGENTS.md) | Agent behavior and safe operating rules | Canonical governance contract | Every agent task | Architecture and task schema |
| [`ROADMAP.md`](../ROADMAP.md) | Product/system evolution: past, present, future | Directional / PROPOSED | Product or maturity questions | Backlog or execution authority |

## Canonical `docs/` documents

| Document | Domain owner | Status | Read when | Must not duplicate |
|---|---|---|---|---|
| [`PRODUCT.md`](PRODUCT.md) | Product definition | Canonical product document | Product/use-case questions | Architecture status or pricing plans |
| [`SYSTEM-DESIGN.md`](SYSTEM-DESIGN.md) | System composition | System map | Cross-layer design | Formal contract details |
| [`TERMINOLOGY.md`](TERMINOLOGY.md) | Vocabulary | Canonical glossary | Any semantic ambiguity | Full rationale/history |
| [`CONTEXT-MAP.md`](CONTEXT-MAP.md) | Context routing | Canonical routing design | Task entry and source selection | Current State or backlog |
| [`DEVELOPMENT-SYSTEM.md`](DEVELOPMENT-SYSTEM.md) | Development-control flow | Canonical development overview | Planning, execution, acceptance | Full passport schema |
| [`TESTING-STRATEGY.md`](TESTING-STRATEGY.md) | Validation philosophy | Canonical testing strategy | Selecting validation | Individual test output |
| [`SECURITY-MODEL.md`](SECURITY-MODEL.md) | Trust and security boundaries | Canonical security model | Authority/security work | Runtime implementation proof |
| [`SOURCE-OF-TRUTH-v1.md`](governance/SOURCE-OF-TRUTH-v1.md) | Factual precedence and permission/intent separation | Canonical governance model | Any source conflict | Replacing domain contracts |
| [`apex/FORK_BOUNDARY.md`](apex/FORK_BOUNDARY.md) | OpenWork pin and Product Shell divergence boundary | Current integration record | Shell/upstream synchronization work | Replacing the architecture or runtime contract |

## Formal directories

| Directory | Authority/domain | Contents |
|---|---|---|
| [`architecture/`](architecture/05-ARCHITECTURE-STATUS.md) | Architecture contracts, boundaries, invariants, and status | formal WHAT of Apex architecture |
| [`governance/`](governance/DEVELOPMENT-WORKFLOW.md) | Repository/development behavior, review, validation, source precedence | rules controlling HOW work is governed |
| [`adr/`](adr/0001-ac-ods-0001-development-control-system.md) | Durable/material decision rationale | WHY decisions were made; not generic docs |
| [`evidence/`](evidence/OPENWORK-FEASIBILITY.md) | Observations, audits, measurements, proof limits | what was observed or verified; not active policy |

## Read-order guidance

For product orientation read README → PRODUCT → ROADMAP. For architecture read
README → SYSTEM-DESIGN → relevant `architecture/` document → architecture
status/evidence. For development read AGENTS → CONTEXT-MAP → relevant Current
State/Task Passport when materialized → DEVELOPMENT-SYSTEM and the selected
governance documents. For a security or authority question read the security
model, relevant architecture contract, and evidence; never infer proof from a
design document alone.

Existing governance and architecture documents remain owners of their topics;
this index does not promote a lower-status proposal or evidence record to
architecture law.
