# Apex Code Handoff and Completion Contract v1

Status: **PROPOSED**.

## Handoff

Handoffs are durable, concise, and machine-readable later. A human→agent, agent→agent, agent→reviewer, task→next task, implementation→verification, or future runtime→orchestration handoff should expose:

```text
TASK / TASK_PASSPORT
OBJECTIVE
SCOPE
CHANGED
VALIDATION_PLAN
VALIDATION_EXECUTED
EVIDENCE
ACCEPTANCE_STATUS
RISKS
LIMITATIONS
ARCHITECTURE_IMPACT
ROLLBACK
OPEN_QUESTIONS
FOLLOW_UP
ARTIFACTS
COMMIT
PR
RESULT_STATUS
UNKNOWNS
```

Empty fields must say `NONE` or `NOT_APPLICABLE`; they must not be omitted when the field is part of the applicable contract. Secret values and credential contents never belong in a handoff.

## Completion report

A Completion Report separates:

- Objective: intended outcome.
- Acceptance Criteria: explicit conditions from the passport.
- Validation: checks actually executed and their outputs.
- Evidence: source/observation references with Apex evidence labels.
- Verification Result: independent assessment of the acceptance contract.
- Result Status: `SUCCESS`, `PARTIAL`, `FAIL`, `BLOCKED`, or `UNKNOWN` as applicable.
- Architecture Impact, risk/limitations, rollback, open questions, artifacts, commit, PR, and passport links.

`AttemptResult` is runtime evidence; a Completion Report is a development-control artifact. Neither alone is semantic Task success. Completion requires explicit acceptance and verification. “Agent says done” is never sufficient.

## Delivery rule

Never report validation as passed unless it was actually executed. If a check was unavailable or not run, record `UNKNOWN` or `NOT_PROVEN` with the reason and scope impact.
