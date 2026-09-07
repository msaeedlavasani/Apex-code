# Apex Code Context Map

Status: **PROPOSED** routing contract. Its purpose is **MINIMUM SUFFICIENT CONTEXT**:
start with the route, read the bounded sources needed for the task,
and expand only when risk, dependency, uncertainty, or failed evidence requires
it. No Retrieval Manifest is materialized; that mechanism remains deferred.

```text
AGENTS.md
    ↓
CONTEXT-MAP
    ↓
Current State, when available
    ↓
Development Task / Task Passport
    ↓
minimum required canonical sources
```

AI/chat memory is not repository state. Historical reports are not active work
authority.

## Routes

| Route | Required starting documents | Optional secondary sources | Normally not required |
|---|---|---|---|
| Product / commercial | [`PRODUCT.md`](PRODUCT.md), [`ROADMAP.md`](../ROADMAP.md), architecture vision | terminology, evidence | runtime model, task passport |
| Architecture | [`SYSTEM-DESIGN.md`](SYSTEM-DESIGN.md), relevant `architecture/` contract, architecture status | related ADR, open questions | product reports unrelated to the contract |
| Execution Core | execution data model, execution model, execution API | system design, open questions | DPT and UI documents |
| Runtime Adapter | modular architecture, execution model/API, relevant status | testing strategy, security model, runtime evidence | DPT-specific governance |
| Authority / security | execution data model/model, [`SECURITY-MODEL.md`](SECURITY-MODEL.md), open questions | validation governance, evidence | commercial or UI docs |
| Capability platform | modular architecture, product, DCS proposal | capability-specific evidence | substrate implementation details |
| Orchestration | modular architecture, DCS/development system, task/passport proposals | API, validation, ADRs | unless directly affected, runtime substrate internals |
| DPT | product, modular architecture, DCS boundaries | DPT-related evidence and capability contracts | treating DPT as Core |
| Public API | execution API, system design, terminology | execution model, architecture status | internal runtime details unless exposed |
| Governance / ADR | AGENTS, relevant governance policy, source of truth | ADR policy, architecture status | unrelated runtime evidence |
| Task / Passport | [`DEVELOPMENT-SYSTEM.md`](DEVELOPMENT-SYSTEM.md), [`governance/DEVELOPMENT-CONTROL-PLANE-v1.md`](governance/DEVELOPMENT-CONTROL-PLANE-v1.md), canonical backlog/passports, active state when available | classification, validation, handoff | full architecture unless affected |
| Testing | [`TESTING-STRATEGY.md`](TESTING-STRATEGY.md), validation governance | affected contract, security | unrelated product history |
| Documentation | INDEX, source-of-truth, documentation ownership in governance | target owner document, evidence | full repository scan |
| Repository / CI | AGENTS, development workflow, CI validation policy | validator, PR template | runtime/product docs unless scope says so |

## Source selection rules

Read the canonical owner document before a secondary report. If sources
conflict, record the contradiction and apply the two-dimensional model in
[`SOURCE-OF-TRUTH-v1.md`](governance/SOURCE-OF-TRUTH-v1.md); permission to act
does not make a source factual proof. When a required fact is absent, preserve
`UNKNOWN` or `NOT_PROVEN` rather than filling the gap from memory.
