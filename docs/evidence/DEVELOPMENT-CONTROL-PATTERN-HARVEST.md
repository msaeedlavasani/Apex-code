# DPT, Home Fit, and BaziGB Development-Control Pattern Harvest

Status: **PROPOSED**. This is an evidence-backed comparison and recommendation set, not a copy of either project’s governance.

## Evidence discipline

Reference-document claims below use `DOCUMENTATION_EVIDENCE`; observed repository/file presence uses `OBSERVED_REPOSITORY_STATE`. Recommendations are `INFERENCE`. No runtime guarantee is inferred from documentation.

## Source files inspected

### ApexAIPDT

`AGENTS.md`; `README.md`; `ROADMAP.md`; `brains/BRAIN_CONTRACT.md`; `brains/ARCHITECTURE.md`; `brains/DATA.md`; `brains/DESIGN.md`; `brains/ENGINEERING.md`; `brains/OPERATIONS.md`; `brains/PRODUCT.md`; `brains/QA.md`; `brains/SECURITY.md`; `core/HUMAN_AI_BOUNDARY.md`; `core/WORKFLOW_ENGINE.md`; `core/DECISION_SYSTEM.md`; `docs/APEX_AI_DPT_CONSTITUTION.md`; `docs/APEX_AI_DPT_TERMINOLOGY.md`; `docs/DPT_CANONICAL_STATE_PRECEDENCE_GOVERNANCE.md`; `docs/DPT_TASK_SYSTEM.md`; `docs/DPT_EXECUTION_CONTROL_MODEL.md`; `docs/DPT_REPORT_LIFECYCLE_GOVERNANCE.md`; `docs/FAILURE_INTELLIGENCE.md`; `docs/TASKS.md`; `workflows/VALIDATION_GATES.md`; `templates/DECISION_RECORD.md`; `templates/FEATURE_CONTRACT.md`.

### Apex-Home-Fitness

`AGENTS.md`; `docs/AI_DEVELOPMENT_SYSTEM.md`; `docs/BRANCHING_POLICY.md`; `docs/CI.md`; `docs/CURRENT_STATE.md`; `docs/HANDOFF.md`; `docs/INDEX.md`; `docs/TASKS.md`; `docs/GOVERNANCE_RUNTIME.md`; `docs/RELEASE_POLICY.md`; `docs/FEATURE_TO_PRODUCTION.md`; `docs/PRODUCTION_CHECKPOINTS.md`; `docs/PRODUCTION_INCIDENT_LEDGER.md`; `docs/TEST-DEBT.md`; `docs/governance/DOCUMENTATION-GOVERNANCE.md`; `docs/governance/DOCUMENTATION-SOURCE-OF-TRUTH-PROPOSAL.md`; `docs/governance/REPORT-DELIVERY-CONTRACT.md`; `docs/governance/UI-CONFORMANCE-GATE.md`; `docs/adr/README.md`; `docs/adr/ADR-TEMPLATE.md`; `docs/adr/0001-canonical-exercise-identity.md`; `docs/adr/0014-privacy-safety-architecture.md`; `docs/PITFALL_GUARDRAILS.md`; `docs/PITFALLS/PRODUCTION-OPERATIONS-SAFETY.md`; `docs/AI_CHANGE_TEMPLATE.md`.

### BaziGB Modular Architecture

`AGENTS.md`; `docs/HANDOFF.md`; `docs/ISSUES.md`; `docs/MODULARIZATION_TASKS.md`; `docs/ARCHITECTURE_AUDIT.md`; `docs/ARCHITECTURE_REFACTOR_REPORT.md`; `docs/CODE_AUDIT.md`; `docs/legacy-audit-and-tech-debt.md`.

The BaziGB checkout discrepancy is resolved. The local checkout inspected earlier is a dirty `feature/catan` worktree at `f8fbf05b2683f73dace69d7912c80a584c190a0a`; it lacks the requested control-plane paths. After fetch, authoritative `origin/main` is `3dabbb6c80b1ad2ce7e27da57bdcc25b8aa1e5e3`. The requested paths exist at that remote ref and were inspected read-only. The local feature checkout is therefore stale/divergent for this evidence; it was not modified.

Remote provenance used for the added BaziGB claims: `origin/main@3dabbb6c80b1ad2ce7e27da57bdcc25b8aa1e5e3` (fetched 2026-09-07). Newly inspected files: `AGENTS.md`, `AI_CONTEXT_MAP.md`, `ai/COLLABORATION_CONTRACT.md`, `ai/CONTROL_PLANE.md`, `ai/NEXT_TASK_HANDOFF.md`, `ai/SYSTEM_INTEGRATION.md`, `ai/VALIDATION_GATE.md`, `ai/WORK_MANAGEMENT.md`, `ai/current-state.json`, `ai/retrieval-manifest-v1.json`, `ai/system-integration-v1.json`, `ai/work-registry-v1.json`, and `docs/aipde/system-governance.md`. The earlier BaziGB audit files remain evidence from the local checkout and are not silently reattributed to the remote ref.

### BaziGB evidence map

All newly relied-on BaziGB control-plane claims use `DOCUMENTATION_EVIDENCE` from the same fetched ref: `AGENTS.md` and `AI_CONTEXT_MAP.md` support entry routing, source precedence, minimum sufficient context, and claim-state distinctions; `ai/WORK_MANAGEMENT.md` and `ai/CONTROL_PLANE.md` support active-work ownership, task hierarchy, readiness, capability boundaries, and learning; `ai/COLLABORATION_CONTRACT.md` and `ai/NEXT_TASK_HANDOFF.md` support approval boundaries, branch/receiver/closure, and handoff semantics; `ai/VALIDATION_GATE.md` and `ai/SYSTEM_INTEGRATION.md` support validation/evidence gates and controlling-contract checks; `ai/current-state.json`, `ai/work-registry-v1.json`, and `ai/retrieval-manifest-v1.json` support the bounded Current State, canonical Work Registry, and future retrieval-manifest observations; `docs/aipde/system-governance.md` supports lifecycle, capability, resource, system-first, learning, and report-vs-state boundaries. JSON contents were inspected only as control-plane metadata; no secret-bearing material was read or exposed.

## Pattern inventory

| Pattern | Source / observed mechanics | Strengths | Assumptions/weaknesses | Apex disposition / owner | Evidence |
|---|---|---|---|---|---|
| Repository Brain | DPT `brains/*` + `BRAIN_CONTRACT.md`; bounded purpose, authority, inputs/outputs, validation, failure modes | clear ownership and routing | DPT role topology is project-specific | ADAPT; `REPOSITORY-BRAIN-v1.md` / future `AGENTS.md` | DOCUMENTATION_EVIDENCE |
| Constitution / architectural law | DPT Constitution; numbered articles and invariants | makes non-negotiables visible | component-first/DPT scope cannot become Apex law wholesale | ADAPT; existing architecture docs | DOCUMENTATION_EVIDENCE |
| Source-of-truth hierarchy | DPT canonical precedence; Home Fit `AGENTS.md`, documentation governance, INDEX | conflict handling and durable ownership | Home Fit ordering assumes mature implementation | ADAPT; `SOURCE-OF-TRUTH-v1.md` | DOCUMENTATION_EVIDENCE |
| Agent behavior contract | DPT `AGENTS.md`; Home Fit `AGENTS.md`; inspect, reuse, plan, authority, verify | prevents silent drift and unsafe action | language/UI/deployment rules are project-specific | ADAPT; future root `AGENTS.md` | DOCUMENTATION_EVIDENCE |
| PLAN vs EXECUTE | Home Fit `AGENTS.md`, `AI_DEVELOPMENT_SYSTEM.md`; plan for non-trivial work, execute only authorized | separates reasoning from mutation | requiring plan for every trivial edit adds friction | ADAPT; DCS policy | DOCUMENTATION_EVIDENCE |
| Task system | DPT `DPT_TASK_SYSTEM.md`, `docs/TASKS.md`; durable records, deltas, readiness, authority, closure | reconstructable state, machine projection | DPT lifecycle/authority fields need Apex mapping | ADAPT; `TASK-SYSTEM-v1.md` | DOCUMENTATION_EVIDENCE |
| Task Passport | DPT task-system and schemas; revisioned scope/capability/authority snapshot | separates task intent from dispatch | must not become Apex runtime manifest | ADAPT; `TASK-PASSPORT-v1.md` | DOCUMENTATION_EVIDENCE |
| Task lifecycle/state | DPT task system; Home Fit executable backlog and release policy | explicit transitions and closure guards | production states are Home Fit-specific | ADAPT; `TASK-SYSTEM-v1.md` | DOCUMENTATION_EVIDENCE |
| Work order / execution request mapping | DPT execution model: Intent → Plan → Task → Work Order → Attempt; Apex Core has ExecutionRequest | clear bounded assignment | DPT Work Order is not automatically Core API | ADAPT; DCS mapping to Core contracts | DOCUMENTATION_EVIDENCE |
| Handoff system | Home Fit `HANDOFF.md`, AI change template; DPT Result/Handoff | preserves next action, limits, evidence | Owner report destination is Home Fit-specific | ADAPT; `HANDOFF-CONTRACT-v1.md` | DOCUMENTATION_EVIDENCE |
| Completion report | DPT Result != Completion; Home Fit report delivery contract | prevents “agent says done” completion | external inbox/export mechanics do not apply | ADAPT; `HANDOFF-CONTRACT-v1.md` | DOCUMENTATION_EVIDENCE |
| Acceptance criteria | DPT Feature Contract and Task System; Home Fit task acceptance fields | makes success explicit | criteria must not be duplicated across artifacts | ADAPT; Task Passport completion contract | DOCUMENTATION_EVIDENCE |
| Validation contract | DPT `VALIDATION_GATES.md`; Home Fit `CI.md` tiering and failure classification | risk-based, narrowest reliable gate | mature app commands cannot be copied | ADAPT; `VALIDATION-GOVERNANCE-v1.md` | DOCUMENTATION_EVIDENCE |
| Evidence discipline | DPT Constitution/Task System and report lifecycle; Home Fit reports/guardrails | facts, verification, provenance, fail-closed | evidence labels differ and must remain Apex-native | ADOPT conceptually; existing Apex evidence vocabulary | DOCUMENTATION_EVIDENCE |
| ADRs | DPT Decision Record; Home Fit `docs/adr/` README/template and accepted ADRs | durable alternatives/rationale/owner | ADR is not generic documentation or authority | ADAPT; `ADR-POLICY-v1.md` | DOCUMENTATION_EVIDENCE |
| Documentation governance | Home Fit governance, index, canonical homes, conflict surfacing | avoids duplicate truth and stale docs | more bureaucracy than current Apex needs | ADAPT; source-of-truth proposal | DOCUMENTATION_EVIDENCE |
| Branch/PR/merge governance | Home Fit branching/release docs; current Apex governance baseline | ephemeral branches, ancestry proof, review gates | production checkpoint rules are project-specific | ADOPT/ADAPT; preserve existing Apex docs | DOCUMENTATION_EVIDENCE |
| CI/validation gates | current Apex `.github/workflows/ci.yml`; DPT/Home Fit tier policies | lean baseline with extensible tiers | do not add heavy jobs now | ADOPT existing; propose future matrix | OBSERVED_REPOSITORY_STATE + DOCUMENTATION_EVIDENCE |
| Security-sensitive change handling | DPT Security brain/authority; Home Fit AGENTS/release/pitfall rules | secrets never exposed, explicit rollback/gates | Home Fit OTP/deploy details are not generic | ADAPT; change classification and future `AGENTS.md` | DOCUMENTATION_EVIDENCE |
| Recovery/rollback | Home Fit release policy/pitfalls; DPT failure routing | rollback before mutation and small correction | production image/deploy mechanics do not apply now | DEFER generic implementation; retain principle | DOCUMENTATION_EVIDENCE |
| Findings/lessons/pitfalls | DPT Failure Intelligence/Pitfall Pool; Home Fit `PITFALLS/` and guardrails | turns repeated failures into controls | DPT Pools and Home Fit taxonomy are heavyweight | ADAPT one findings/lessons registry later | DOCUMENTATION_EVIDENCE |
| Incident handling | Home Fit incident ledger and production reports | explicit termination evidence and follow-up | production incident machinery premature | DEFER until runtime/deployment exists | DOCUMENTATION_EVIDENCE |
| Technical debt tracking | Home Fit `TEST-DEBT.md`, tasks/debt fields | visible known divergence and follow-up | avoid a second backlog | ADAPT as `DEBT` claim state in canonical task registry | DOCUMENTATION_EVIDENCE |
| Change classification | Home Fit AI system categories; DPT small/standard/cross-domain gates | drives scope-aware gates | UI/domain categories are app-specific | ADAPT composable flags | DOCUMENTATION_EVIDENCE |
| Risk classification | DPT risk envelope/authority; Home Fit production sensitivity gates | risk drives review and validation | no need for detailed DPT authority modes now | ADAPT LOW/MEDIUM/HIGH/CRITICAL | DOCUMENTATION_EVIDENCE |
| Owner escalation/approval | DPT Human/AI boundary, Decision System, Escalation; Home Fit owner gates | bounded autonomy and clear stop conditions | DPT role/HG classes are not Apex primitives | ADAPT generic escalation model | DOCUMENTATION_EVIDENCE |
| Canonical backlog/work queue | DPT `docs/TASKS.md` machine projection; Home Fit `docs/TASKS.md` only executable backlog | one durable queue, explicit readiness | task engine and GitHub sync are premature | ADAPT document-backed future registry | DOCUMENTATION_EVIDENCE |
| Terminology governance | DPT Terminology; Home Fit canonical vocabulary/read order | prevents semantic drift | DPT terms like Scout/Analyst are product-specific | ADAPT glossary/contract ownership later | DOCUMENTATION_EVIDENCE |
| Architecture freeze/change handling | existing Apex policy; DPT Constitution/ADRs; Home Fit ADR/governance | explicit review for protected decisions | must retain Apex statuses | ADOPT existing, ADAPT ADR proposal | DOCUMENTATION_EVIDENCE |
| Result delivery | DPT report lifecycle; Home Fit report delivery contract | persistence vs delivery distinction | external Owner inbox does not apply | ADAPT repository handoff/artifact links | DOCUMENTATION_EVIDENCE |
| Development project state | DPT workflow state; Home Fit current/release state | useful for orchestration dashboards | duplicate task lifecycle risk | DEFER project-level state; task state is enough v1 | DOCUMENTATION_EVIDENCE |
| Specialized DPT team/roles | DPT Scout, Analyst, Architect, Developer, QA, pools, capability engine | powerful for DPT ecosystem | product-specific and would couple Core to DPT | REJECT from Apex Core; DEFER to optional DPT | DOCUMENTATION_EVIDENCE |
| Home Fit UI conformance gate | Home Fit UI governance/AGENTS; reuse kit, locale, visual evidence | strong for UI changes | no Apex UI exists and rules are product-specific | DEFER; later adapt generic UI flag | DOCUMENTATION_EVIDENCE |
| Home Fit production gateway | release/deploy gateway, OTP, Docker, browser acceptance | production-safe in its project | unsafe/irrelevant generic import | REJECT generic DCS; future operations design | DOCUMENTATION_EVIDENCE |
| AI Context Map / task routing | BaziGB `origin/main@3dabbb6` provides `AI_CONTEXT_MAP.md`, route tables, minimum-sufficient-context rules, and links from `AGENTS.md` | strong direct evidence for routed retrieval without loading the whole repository | the name and AI-specific wording are not Apex ownership boundaries | ADAPT as `docs/CONTEXT-MAP.md`; do not copy the name mechanically | DOCUMENTATION_EVIDENCE + OBSERVED_REPOSITORY_STATE |
| Bounded Current State | BaziGB `AGENTS.md` separates current implementation from target/debt/unknown; audit/handoff snapshots are bounded | fast resume without treating history as truth | BaziGB handoff includes project-specific deployment facts | ADAPT; bounded current-state artifact | DOCUMENTATION_EVIDENCE |
| Retrieval manifest | BaziGB `origin/main@3dabbb6` contains `ai/retrieval-manifest-v1.json`, route-to-source entries, and retrieval constraints | demonstrates a machine-readable future interface | premature for Apex before the Context Map and canonical docs exist | DEFER implementation; preserve future compatibility | DOCUMENTATION_EVIDENCE + OBSERVED_REPOSITORY_STATE |
| One canonical active Work Registry | BaziGB `docs/MODULARIZATION_TASKS.md` and audit identify task/backlog drift and propose a canonical backlog | exposes active-state ownership problem | the source itself records unresolved documentation drift | ADAPT; one Apex work registry | DOCUMENTATION_EVIDENCE |
| Historical reports != active state | BaziGB audit distinguishes historical reports from current branch/code truth; Home Fit makes this explicit | prevents stale handoffs becoming backlog authority | requires declared document status | ADOPT conceptually; source-of-truth and handoff contracts | DOCUMENTATION_EVIDENCE |
| Passport readiness / fail closed | BaziGB `ai/exchange/schemas/task-passport.schema.json` and `ai/WORK_MANAGEMENT.md` define bounded execution packages, dependency/evidence gates, and incomplete readiness handling | strengthens the case for explicit fail-closed admission | schema is BaziGB-specific and cannot become Core Task or ExecutionManifest | ADAPT as Apex `PASSPORT_INCOMPLETE` | DOCUMENTATION_EVIDENCE + OBSERVED_REPOSITORY_STATE |
| Evidence dependency gates | BaziGB audits record evidence, affected files, validation plan, and pending approval; Home Fit gates are stronger | ties work readiness to evidence | audit evidence is not an executable gate | ADAPT; validation/acceptance contract | DOCUMENTATION_EVIDENCE |
| Branch lifecycle / explicit closure | BaziGB historical task says branch was integrated and deleted; `MODULARIZATION_TASKS.md` defines small commits/tests | reinforces ephemeral branches and closure proof | current BaziGB also documents a single-main model, not Apex PR flow | ADAPT existing Apex branch governance | DOCUMENTATION_EVIDENCE |
| WIP limits | No explicit numeric WIP limit observed in BaziGB control docs; Home Fit has production-bound WIP rules | absence is useful caution against inventing a limit | no direct BaziGB adoption evidence | DEFER numeric limit; use risk/resource admission first | OBSERVED_REPOSITORY_STATE |
| Implementation != validation | BaziGB audits distinguish code architecture from validation plan/status; `AGENTS.md` requires actual validation | protects completion semantics | audit status can become stale | ADOPT and strengthen in validation contract | DOCUMENTATION_EVIDENCE |
| Validation != human acceptance | BaziGB `AGENTS.md` requires approval for architectural/risky changes; audits list pending owner approval separately | separates technical proof from decision | no universal BaziGB state machine observed | ADAPT; acceptance/review boundary | DOCUMENTATION_EVIDENCE |
| Acceptance != operational verification | BaziGB handoff lists deploy/health checks separately from code/tests | preserves operational distinction | deployment details are project-specific | ADAPT later; defer production mechanics | DOCUMENTATION_EVIDENCE |
| Routine / Material / Critical | No exact BaziGB triad observed; audit priorities and approval sensitivity provide analogous signals | useful decision class axis | do not misattribute triad to BaziGB | ADAPT as Apex decision class | INFERENCE + DOCUMENTATION_EVIDENCE |
| Standard / Elevated / Intensive resources | No exact BaziGB resource bands observed | gives explicit cost/effort governance option | no source evidence for token percentage bands | ADAPT without numeric bands; resource governance proposal | INFERENCE + OBSERVED_REPOSITORY_STATE |
| Resource Approval Request | BaziGB audit marks owner approval for material changes but no named request artifact | makes exceptional resource use visible | no reusable BaziGB request contract observed | DEFER/adapt later for broad or paid work | OBSERVED_REPOSITORY_STATE + DOCUMENTATION_EVIDENCE |
| System-first correction | BaziGB modularization audit turns repeated coupling into boundary/gate tasks; DPT failure intelligence supplies reusable pattern | fixes missing controls instead of symptoms | must avoid automatic refactoring | ADAPT; agent/governance principle | DOCUMENTATION_EVIDENCE |
| Controlling-contract validation | BaziGB audit identifies canonical architecture and public API boundaries; Home Fit names canonical contract owners | validation checks the authoritative contract | current Apex has no implementation contract yet | ADAPT; validation governance | DOCUMENTATION_EVIDENCE |
| Validation result vocabulary | No explicit BaziGB `PASS/FAIL/NOT_RUN/BLOCKED` contract observed; audit uses status prose/check marks | explicit result states improve honesty | do not claim source implementation | ADAPT as proposed Apex vocabulary | OBSERVED_REPOSITORY_STATE + INFERENCE |
| Documentation retrieval/supersession | BaziGB audit identifies stale branch/docs references and recommends update/merge/deprecate; Home Fit governance formalizes canonical homes | makes stale knowledge visible | no BaziGB retrieval manifest | ADAPT; source-of-truth policy | DOCUMENTATION_EVIDENCE |
| Immutable evidence vs mutable contracts | BaziGB audit/refactor report preserves historical evidence while proposing updates to current docs | separates observation from current policy | requires status metadata | ADAPT; handoff/evidence boundaries | DOCUMENTATION_EVIDENCE |
| Current State vs historical handoff | BaziGB `HANDOFF.md` is a snapshot with version/branch/operations; audits are historical | clear resume/history split | BaziGB snapshot contains stale facts by design | ADAPT with explicit bounded snapshot status | DOCUMENTATION_EVIDENCE |
| Permission authority vs factual source | BaziGB `AGENTS.md` separates approval/authority from repository facts; DPT makes this explicit | prevents facts from granting permission | no BaziGB runtime authority model observed | ADAPT; source-of-truth + escalation | DOCUMENTATION_EVIDENCE |
| Bundled approval | BaziGB handoff says deployment requires explicit approval, but no bundled approval object observed | identifies a useful approval-package concept | avoid claiming implementation | DEFER; owner decision package later | OBSERVED_REPOSITORY_STATE + DOCUMENTATION_EVIDENCE |
| Separate commit/push/merge/deploy permissions | BaziGB separates deployment approval from branch work; `AGENTS.md` forbids unapproved risky action | least privilege and clear gates | single-main workflow is not Apex workflow | ADAPT; Apex permission actions | DOCUMENTATION_EVIDENCE |
| Learning destination | BaziGB audits and legacy debt docs record findings/tasks; DPT has Pitfall Pool | converts lessons into durable controls | no single BaziGB learning registry observed | ADAPT one future findings/lessons destination | DOCUMENTATION_EVIDENCE |
| Capability responsibilities vs job titles | BaziGB modular architecture uses package/module responsibilities rather than DPT role graph | keeps responsibilities generic | app roles still exist outside control plane | ADOPT boundary; reject DPT title import | DOCUMENTATION_EVIDENCE |
| Portfolio/workstream/task hierarchy | BaziGB modularization tasks use a dependency graph and phases | supports sequencing | not a formal portfolio registry | ADAPT only if work volume requires it | DOCUMENTATION_EVIDENCE |
| Branch drift/release authority checks | BaziGB audits compare documented branch state with actual Git state and identify stale refs | directly useful to Apex branch governance | current branch policy was single-main and project-specific | ADAPT; pre-task and closure checks | DOCUMENTATION_EVIDENCE |

## Disposition matrices

### ADOPT

| Pattern | Why |
|---|---|
| Evidence before claiming | Directly supports Apex’s `NOT_PROVEN` discipline. |
| Result/verification distinct from completion | Aligns with Apex `AttemptResult`, `Verification`, and Task semantics. |
| Narrowest reliable validation | Already present in Apex CI policy and supported by both references. |
| Branch → PR → validation → review → merge | Existing Apex governance already establishes it. |
| Explicit source ownership and contradiction surfacing | Prevents duplicate architecture/control truth. |
| Historical evidence separated from active state | BaziGB audit findings and Home Fit governance support this distinction. |
| Separate permission actions | BaziGB approval/deployment separation strengthens least-privilege control. |

### ADAPT

| Pattern | Apex adaptation |
|---|---|
| Brain contract | Development guidance only; no duplicate architecture law or DPT role graph. |
| Task Passport | Development contract mapped to Core Tasks; never an ExecutionManifest. |
| Durable task ledger | Proposed one canonical registry, no database/task engine. |
| PLAN/EXECUTE | Required by non-trivial scope/risk; lightweight for safe docs edits. |
| Change/risk classes | Composable generic signals, not Home Fit’s product categories. |
| Handoff/report | Repository-native fields; no external report inbox assumption. |
| ADR/documentation governance | Retain Apex statuses and evidence labels. |
| Owner escalation | Generic protected-boundary triggers, independent of DPT authority modes. |
| Context routing and bounded Current State | Use a substrate-neutral map and small resume snapshot; do not claim absent BaziGB files. |
| Validation result states | Add PASS/FAIL/NOT_RUN/BLOCKED as a result dimension, separate from Apex evidence. |
| Decision/resource classes | Add routine/material/critical and standard/elevated/intensive as separate proposed axes. |
| Branch drift/closure checks | Adapt BaziGB audit discipline to existing Apex PR branch lifecycle. |

### DEFER

| Pattern | Reason |
|---|---|
| Full domain brain tree | No implementation/product domains yet; duplication risk. |
| Project-level development state | Task lifecycle is sufficient until orchestration needs dashboards. |
| Incident ledger and production rollback machinery | No deployable Apex runtime exists. |
| Machine task database/queue and GitHub synchronization | Premature implementation and source duplication. |
| UI conformance gate | No Apex UI surface exists. |
| DPT Pools/failure-intelligence machinery | Optional capability and heavier than current phase. |
| Retrieval Manifest | Useful after a context map and machine registry exist; present in BaziGB remote evidence but premature for Apex now. |
| Numeric WIP/resource/token bands | No direct BaziGB evidence and unnecessary policy precision at this phase. |

### REJECT

| Pattern | Reason |
|---|---|
| DPT Scout/Analyst/Architect/Developer/QA topology in Core | Couples Apex identity and architecture to DPT. |
| DPT credit/economy/project subscription semantics | Commercial/product-specific and outside DCS. |
| Home Fit OTP, Docker, deployment gateway, and production paths | Project-specific operational assumptions. |
| Copying reference files verbatim | Violates Apex-native boundaries and creates duplicate truth. |

## Confidence limits

The source repositories directly support the documented mechanics where labeled. The BaziGB local/remote discrepancy is recorded as `OBSERVED_REPOSITORY_STATE` with exact refs; remote control-plane mechanics are labeled `DOCUMENTATION_EVIDENCE` and are not inferred from the stale local checkout. This harvest does not prove that any proposed Apex DCS pattern works in an Apex runtime. Runtime authority binding remains `NOT_PROVEN` in Apex architecture evidence.
