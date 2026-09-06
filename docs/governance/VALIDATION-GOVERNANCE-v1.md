# Apex Code Validation Governance v1

Status: **PROPOSED**.

## Principle

Use the cheapest/narrowest reliable validation appropriate to affected scope and risk. Validation is evidence for acceptance, not completion by itself. Do not run full E2E indiscriminately.

## Tiers

`STATIC`, `LINT`, `TYPECHECK`, `UNIT`, `INTEGRATION`, `CONTRACT`, `ADAPTER_CONFORMANCE`, `SECURITY`, `TARGETED_SMOKE`, `E2E`.

Each validation check has one result: `PASS`, `FAIL`, `NOT_RUN`, or `BLOCKED`. These are validation results, not Apex evidence types and not claim states. `NOT_RUN` means no result was produced; `BLOCKED` means a prerequisite prevented the check. Neither is a pass.

## Proposed matrix

| Scope/risk | Minimum validation | Escalate when |
|---|---|---|
| DOCS_ONLY / low | current static/link/structure/status checks | frozen architecture or governance meaning changes |
| ordinary implementation | lint + typecheck + relevant unit | cross-module behavior or unclear contract |
| CORE_CHANGE | relevant unit + integration + contract | semantic invariant or recovery impact |
| RUNTIME_CHANGE | adapter contract + conformance + targeted integration | session/process or substrate uncertainty |
| AUTHORITY_CHANGE / SECURITY_SENSITIVE | targeted security + integration + negative tests | activation, revocation, or boundary is not proven |
| DATA_CHANGE | unit + migration/integrity/conflict checks | irreversible migration or data loss risk |
| critical execution/recovery | stronger integration + targeted smoke/E2E | production or contract blast radius |
| release/production | all applicable lower tiers plus targeted acceptance | owner gate, rollback, or environment uncertainty |

## Validation contract

Each development task records selected tiers, commands or check identifiers, expected evidence, failure routing, and whether independent review is required. A passed command may prove only the behavior it exercised. `UNKNOWN` and `NOT_PROVEN` remain visible.

Validation is layered with acceptance: implementation may be complete, machine validation may pass, and human acceptance may still be pending. Operational verification is a separate requirement for applicable runtime/production changes. The controlling contract for each check is identified explicitly; a convenient but non-authoritative test cannot override it.

The existing Apex CI currently supplies lean documentation/static validation. Future lint, typecheck, unit, integration, runtime-adapter conformance, and targeted smoke/E2E layers should be added independently when implementation scope justifies them.

## Failure routing

A failure report identifies the check, affected behavior, evidence, likely owner, smallest corrective state, and whether a rerun is meaningful. Re-run the narrowest relevant check after correction; do not hide a failure behind a broader green run.
