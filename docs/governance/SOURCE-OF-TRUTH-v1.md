# Apex Code Source of Truth v1

Status: **PROPOSED**.

## Precedence

When sources conflict, use the highest applicable authority below, surface the contradiction, and do not silently guess. The ordering distinguishes current reality from intended design.

1. Directly observed repository state and implementation/configuration (`CURRENT` evidence).
2. Public API and formal contracts, including the existing frozen Apex architecture contracts.
3. `docs/architecture/05-ARCHITECTURE-STATUS.md` and the architecture documents it indexes.
4. Accepted ADRs, when they govern the decision and are not superseded.
5. `AGENTS.md` and repository brain documents for development behavior and domain guidance.
6. Governance documents for workflow, evidence, review, and validation.
7. Task Passport and canonical development-task registry for work-specific intent and scope.
8. Handoff/completion reports and evidence records for observations and results.
9. Historical documents and general assumptions.

The authority is topic-specific: implementation can prove `CURRENT` behavior, but it does not silently replace a required `TARGET` contract. An observed implementation that conflicts with a formal contract is recorded as `DEBT` or `UNKNOWN` and escalated according to risk.

Permission to act is a separate dimension from factual authority. A source may establish what exists without granting permission to change it; a reviewer or owner may grant permission without becoming evidence that the change succeeded. Commit, push, merge, and deploy are separate permissions.

## Two dimensions of truth

The Home Fit labels describe claim state, not evidence type. Apex should keep them separate:

| Claim state | Meaning |
|---|---|
| `CURRENT` | observed or contractually established present reality |
| `TARGET` | intended future contract or design |
| `CONSTRAINT` | boundary that limits valid choices |
| `DEBT` | known divergence between current and target/constraint |
| `UNKNOWN` | unresolved state or insufficient information |

Evidence remains the existing Apex vocabulary and must not be replaced:

`SOURCE_CODE_EVIDENCE`, `DOCUMENTATION_EVIDENCE`, `OBSERVED_REPOSITORY_STATE`, `OBSERVED_RUNTIME_EVIDENCE`, `INFERENCE`, `UNKNOWN`, `NOT_PROVEN`.

`NOT_PROVEN` is a proof state, not a claim-state synonym. In particular, documentation or an ADR cannot upgrade the authority materialization/binding chain from `NOT_PROVEN`.

## Ownership map

| Information | Canonical owner |
|---|---|
| Product identity/principles | existing architecture vision docs |
| Core contracts and invariants | existing architecture docs and Public API contracts |
| Architecture decision status | `docs/architecture/05-ARCHITECTURE-STATUS.md` plus ADRs |
| Development behavior | Root `AGENTS.md` |
| Context routing | `docs/CONTEXT-MAP.md` |
| Product definition and evolution | `docs/PRODUCT.md` and root `ROADMAP.md` |
| System-level composition | `docs/SYSTEM-DESIGN.md` |
| Canonical vocabulary | `docs/TERMINOLOGY.md` |
| Development-control overview | `docs/DEVELOPMENT-SYSTEM.md` and linked governance contracts |
| Testing strategy | `docs/TESTING-STRATEGY.md` and `docs/governance/VALIDATION-GOVERNANCE-v1.md` |
| Security model | `docs/SECURITY-MODEL.md` and relevant architecture contracts |
| Workflow/validation/review rules | existing `docs/governance/` files |
| One development task's scope | Task Passport |
| Candidate/active work | canonical task registry/backlog |
| Observation and proof | evidence records and validation outputs |
| Human-facing result | Completion Report / Handoff |

The active Work Registry is the only source for active work state. A bounded Current State is a resume projection, not a backlog. A Retrieval Manifest, if later introduced, records what context was loaded; it is evidence of retrieval, not authority over the retrieved sources.

## Contradiction handling

Record the conflicting sources, their labels, the highest-authority interpretation, affected scope, and required owner action. Do not treat document age, runtime confidence, or a generated projection as authority by itself. Historical documents remain useful evidence but do not become current instructions.
