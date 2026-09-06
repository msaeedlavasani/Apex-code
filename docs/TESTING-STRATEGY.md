# Apex Code Testing Strategy

Status: **PROPOSED** testing and validation strategy.

## Principle and progression

Choose the cheapest/narrowest reliable validation for the affected scope,
contract, Decision Class, Risk, and Resource Class. Escalate when evidence,
blast radius, or uncertainty requires it; do not run full E2E indiscriminately.

```text
STATIC → LINT → TYPECHECK → UNIT → INTEGRATION → CONTRACT
       → ADAPTER_CONFORMANCE → SECURITY → TARGETED_SMOKE → E2E
       → HUMAN_ACCEPTANCE → OPERATIONAL_VERIFICATION
```

Not every task requires every layer. Existing lean CI currently covers static
documentation/repository checks; future layers remain independently addable.
The [Validation Governance](governance/VALIDATION-GOVERNANCE-v1.md) document
owns the validation contract and result semantics.

## Scope examples

| Scope | Starting validation | Escalate when |
|---|---|---|
| Docs/governance | static/link/structure/status checks | architecture meaning or evidence claim changes |
| Core semantics | relevant unit + integration + contract | invariant, recovery, or cross-boundary impact |
| Runtime Adapter | adapter contract + conformance + targeted integration | substrate/session uncertainty |
| Authority/security | security checks, negative tests, integration | activation/revocation or isolation is uncertain |
| Critical execution/recovery | stronger integration + targeted smoke/E2E | production or irreversible blast radius |

## What checks do not prove

- Build PASS does not prove UI correctness.
- Static inspection does not prove runtime correctness.
- A screenshot does not prove responsive behavior.
- HTTP 200 does not prove successful execution.
- An idle session does not prove Task completion.
- Documentation does not prove runtime authority binding.

Future targeted validation must cover authority and isolation, recovery,
preservation of `UNKNOWN`, duplicate-execution prevention, adapter conformance,
event replay, idempotency, and negative permission tests. A validation result
must be one of `PASS`, `FAIL`, `NOT_RUN`, or `BLOCKED`; `NOT_RUN` and `BLOCKED`
are never implicit passes.
