# Apex Code Change Classification v1

Status: **PROPOSED**.

## Composable signals

Change classes are composable flags, not mutually exclusive labels. `DOCS_ONLY` and `TEST_ONLY` describe dominant scope but may combine with `GOVERNANCE_CHANGE` or evidence updates. The highest-risk applicable signal controls required gates.

`DOCS_ONLY`, `ARCHITECTURE_CHANGE`, `CORE_CHANGE`, `RUNTIME_CHANGE`, `AUTHORITY_CHANGE`, `SECURITY_SENSITIVE`, `DATA_CHANGE`, `UI_CHANGE`, `DEPENDENCY_CHANGE`, `INFRA_CHANGE`, `PRODUCTION_CHANGE`, `TEST_ONLY`, `GOVERNANCE_CHANGE`.

## Gate matrix

| Signal | Plan | Review | Validation | Recovery/evidence |
|---|---|---|---|---|
| DOCS_ONLY | lightweight plan unless frozen rule | normal docs review | static/link/status checks | source/evidence links |
| TEST_ONLY | targeted plan | code review | affected test layers | failure interpretation |
| GOVERNANCE_CHANGE | explicit scope | governance review | docs/static + CI | policy impact |
| ARCHITECTURE_CHANGE | mandatory PLAN | architecture review; frozen rule requires explicit review | contract + relevant integration | ADR/evidence/rollback |
| CORE_CHANGE | mandatory PLAN | Core owner/architecture | lint/type/unit/integration/contract | semantic invariants |
| RUNTIME_CHANGE | mandatory PLAN | runtime/architecture | adapter contract/conformance/integration | substrate rollback |
| AUTHORITY_CHANGE | mandatory PLAN | explicit owner/architecture/security review | negative/security/integration | fail-closed recovery |
| SECURITY_SENSITIVE | mandatory PLAN | security review | targeted security + relevant tests | containment/rollback |
| DATA_CHANGE | mandatory PLAN | data/architecture review | migration/conflict/integrity tests | reversible migration |
| UI_CHANGE | scoped PLAN | design review when system boundary changes | UI conformance and affected tests | before/after evidence |
| DEPENDENCY_CHANGE | mandatory PLAN | architecture/security as applicable | compatibility/security/build | version rollback |
| INFRA_CHANGE | mandatory PLAN | operations/owner if material | config/build/smoke | executable rollback |
| PRODUCTION_CHANGE | mandatory PLAN | explicit owner gate | production-specific checks | rollback before mutation |

## Classification rules

Classify from the intended and affected contract, not only changed filenames. If classification is uncertain, use the stricter plausible class and record `UNKNOWN`/`NOT_PROVEN` evidence rather than silently narrowing scope. A change can be docs-only in files but architecture-impacting in meaning.

The current CI remains unchanged. This matrix is a future control-plane proposal, not a request to add jobs in this delta.
