# Apex Code Development-Control Gap Analysis

Status: **PROPOSED**. Priorities are recommendations, not implementation authorization.

## Current versus target

| Area | Current Apex Code | Target DCS v1 | Gap / priority |
|---|---|---|---|
| Branch/PR/merge | Governance docs, protected main, lean CI, PR template | retained and extended by task-aware scope | sufficient baseline; future alignment P1 |
| Architecture law/status | architecture baseline with FROZEN/FREEZE_CANDIDATE and evidence labels | ADR linkage and owner review | P0 policy integration |
| Agent contract | no root `AGENTS.md` | Apex-native inspect/plan/execute/verify contract | P0 candidate |
| Source precedence | implicit across architecture/governance docs | explicit current/target/constraint/debt/unknown model | P0 |
| Development task | no canonical registry/passport | Development Task + Task Passport mapped to Core Task(s) | P0 design, implementation later |
| Change/risk classification | not formalized | composable flags + four risk bands | P0 |
| Acceptance/completion | conceptual API and evidence docs | passport acceptance + verification + report contract | P0 |
| Validation | lean docs/static CI only | scope/risk matrix with independent future tiers | P0 policy, P1 implementation |
| Handoff/report | no Apex-native contract | structured handoff/completion fields | P0 |
| ADR mechanism | existing architecture status policy, no `docs/adr/` | decision-only ADR process | P0 candidate for architecture changes |
| Canonical backlog | no task registry | one document-backed projection | P1, after owner design |
| Repository brain | no root contract | lightweight `AGENTS.md`, selective brains | P0 candidate |
| Incident/recovery | no runtime/production system | later runtime-aware recovery/incident controls | P3 |

## Priority interpretation

- **P0 — before any product implementation:** source precedence, agent contract, Development Task/Passport contract, change/risk classification, acceptance/validation/evidence, handoff/completion, ADR decision process, and minimum repository brain.
- **P1 — before first Runtime Adapter implementation:** adapter-specific passport requirements, runtime/authority change gates, conformance validation, resource/rollback contract, and exact mapping to Core `ExecutionRequest`.
- **P2 — before Orchestration capability:** machine-readable task registry, dependency/readiness projection, handoff scheduling interface, verifier routing, and capability-consumption SPI.
- **P3 — later maturity:** incident ledger, production release control, learning/failure pools, metrics/data brain, UX brain, and automated debt/lessons promotion.

## Existing Apex governance review

| Existing file | Sufficient now | Missing / future delta | Must remain unchanged here |
|---|---|---|---|
| `docs/governance/DEVELOPMENT-WORKFLOW.md` | branch prefixes, PR path, squash recommendation | link task/passport and scope gates | current branch/PR semantics |
| `docs/governance/CI-VALIDATION-POLICY.md` | lean checks, future independent layers, narrowest principle | reference classification matrix | current CI behavior |
| `docs/governance/ARCHITECTURE-CHANGE-POLICY.md` | frozen-change review, evidence discipline, NOT_PROVEN rule | ADR linkage and passport triggers | existing frozen rules |
| `.github/workflows/ci.yml` | static docs/structure/secret/whitespace validation | future jobs only in later scoped deltas | workflow behavior |
| `.github/pull_request_template.md` | validation, architecture, secret, `.freebuff/` checks | passport/classification fields later | template baseline |
| `scripts/validate_docs.py` | structural/status/link/secret checks | task/passport validation later | validator behavior |

No existing governance file was modified by this harvest. DPT/Home Fit production, UI, role, credit, and deployment semantics are not imported into Apex Core.
