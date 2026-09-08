# AC-DEV-018 — Execution Admission & Candidate Selection v1

Status: **PROPOSED evidence report**.

## Scope

AC-DEV-018 consumes the non-dispatching Candidate Execution Plan produced by
AC-DEV-017. It emits a deterministic, machine-readable Execution Admission
Decision and may select one task-scoped candidate source for future execution.
It does not dispatch, execute, install ECC, or permanently bind Apex to Goose,
Freebuff, or another executor.

## Decision contract

The admission projection emits one of:

- `ADMITTED` — one compatible source is selected for this task only;
- `BLOCKED_CAPABILITY` — a required capability is unavailable or no single
  source satisfies all required capabilities;
- `BLOCKED_AMBIGUITY` — required capability or overall source quality is tied
  without an explicit tie-break policy;
- `BLOCKED_POLICY` — admission or source eligibility is denied by policy;
- `HUMAN_GATE_REQUIRED` — a Passport or policy Human Gate is open.

Required capability claim and evidence records are carried into the decision.
Rejected candidates include their source identity, required-capability records,
quality, and rejection rationale. Optional capability gaps remain visible in
the embedded Candidate Execution Plan and do not silently become required.

The default policy does not break equal-quality ties. A caller must explicitly
provide `allow_deterministic_tie_break: true` and
`tie_break_strategy: SOURCE_ID_ASC` to permit that deterministic policy.

## Ownership and safety

Admission and task-scoped candidate selection remain Apex Control Plane
responsibilities. Scheduling remains Apex Control Plane-owned. Runtime
authority, verification, retry/rework, and semantic success remain Apex
Core-owned. The output always records `runtime_side_effects: false`,
`dispatch_allowed: false`, and `permanent_executor_selected: false`.

## Verification

Regression coverage exercises admitted unique candidates, required
`NOT_PROVEN`/unsupported capability blocking, ambiguity blocking, explicit
tie-break admission, policy denial, Human Gate blocking, evidence/claim-state
preservation, and identical-input determinism. Canonical tests, JSON/document
validation, whitespace validation, and the protected CI gate are required
before merge.

AC-DEV-018 is recorded as `DONE` / `VERIFIED` / `PROVEN` for the control-plane
implementation. Runtime dispatch and execution remain outside this task and
are not claimed as proven.
