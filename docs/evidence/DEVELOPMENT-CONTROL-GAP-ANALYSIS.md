# Apex Code Development-Control Gap Analysis

Status: **PROPOSED**. Priorities are recommendations, not implementation authorization.

## Current versus target

| Area | Current Apex Code | Target DCS v1 | Gap / priority |
|---|---|---|---|
| Branch/PR/merge | Governance docs, protected main, lean CI, PR template | retained and extended by task-aware scope | sufficient baseline; future alignment P1 |
| Architecture law/status | architecture baseline with FROZEN/FREEZE_CANDIDATE and evidence labels | ADR linkage and owner review | P0 policy integration |
| Agent contract | no root `AGENTS.md` | Apex-native inspect/plan/execute/verify contract | P0 accepted documentation |
| Source precedence | implicit across architecture/governance docs | explicit current/target/constraint/debt/unknown model | P0 |
| Development task | no canonical registry/passport | Development Task + Task Passport mapped to Core Task(s) | P0 design, implementation later |
| Change/risk classification | not formalized | composable flags + four risk bands | P0 |
| Acceptance/completion | conceptual API and evidence docs | passport acceptance + verification + report contract | P0 |
| Validation | lean docs/static CI only | scope/risk matrix with independent future tiers | P0 policy, P1 implementation |
| Handoff/report | no Apex-native contract | structured handoff/completion fields | P0 |
| ADR mechanism | existing architecture status policy, now paired with accepted decision-only ADR direction | decision-only ADR process under `docs/adr/` | P0 accepted policy; materialization in this design delta |
| Canonical backlog | no task registry | exactly one active Work State owner; machine registry later | principle accepted; implementation P2 |
| Repository brain | no root contract | root `AGENTS.md`; full brain tree deferred | P0 accepted documentation; full tree P3 if justified |
| Context routing | no Context Map or bounded Current State | `docs/CONTEXT-MAP.md` + bounded resume snapshot | Context Map P0; Current State P1 |
| Active work authority | no task registry | one canonical Work Registry; reports/handoffs/current state/passports non-authoritative for active backlog | principle P0; implementation P2 |
| Passport readiness | proposed passport fields | `PASSPORT_INCOMPLETE` fail-closed admission with dependency/evidence gates | P0 |
| Validation results | lean CI outcomes only | PASS/FAIL/NOT_RUN/BLOCKED separate from evidence/claim state | P0 policy |
| Resource governance | no resource bands | Standard/Elevated/Intensive and lowest responsible cost; numeric approval mechanism deferred | principle P0; mechanism P3 |
| Learning destination | no Apex learning registry | one future findings/lessons destination | P2 |
| Incident/recovery | no runtime/production system | later runtime-aware recovery/incident controls | P3 |

## Priority interpretation

- **P0 — before substantive product/runtime implementation:** root `AGENTS.md`, `ROADMAP.md`, source precedence, Context Map design, Development Task/Task Passport and `PASSPORT_INCOMPLETE`, three classification axes, acceptance/evidence semantics, validation-result vocabulary, handoff/completion boundaries, ADR process, canonical documentation ownership, and System-First Correction.
- **P1 — before/with first Runtime Adapter:** bounded machine-readable Current State, adapter passport requirements, authority/runtime gates, adapter conformance, rollback/resource contracts, and security-specific validation.
- **P2 — before advanced Orchestration:** machine-readable Work Registry, readiness/dependency projection, orchestration interfaces, richer learning destination, and automated branch/task state integration.
- **P3 — later maturity:** Retrieval Manifest, full Repository Brain if justified, production incident/release machinery, numeric WIP/resource policy, automated learning promotion, and mature operational controls.

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
