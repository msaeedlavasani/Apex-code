# Task Capability Requirements and Registry Matching Evidence 0022

Status: PROPOSED evidence report
Task: AC-DEV-017
Evidence date: 2026-09-08 (Asia/Tehran)

## Result

AC-DEV-017 adds an executor-neutral `capability_requirements` Passport field
and a pure `build_candidate_execution_plan` matcher. The matcher ranks
compatible registry source mappings without selecting or dispatching a source.
Its plan is machine-readable, deterministic, and explicitly sets
`dispatch_allowed` to false.

## Matching rules

- `required` and `optional` requirements are separate.
- Required `NOT_PROVEN`, `NOT_SUPPORTED`, `UNKNOWN`, unavailable, and
  ambiguous best matches produce `BLOCKED_REQUIRED_CAPABILITY`.
- Optional gaps remain in the plan with their observed claim state and do not
  block future routing.
- `PROVEN` outranks `PARTIAL`; equal-best candidates are retained in stable
  source-ID order and marked `AMBIGUOUS`.
- Match results preserve source identity, source status, claim state, evidence
  references, notes, compatibility, and rank.

## Ownership and scope

The Candidate Execution Plan is a routing input only. Apex Control Plane owns
requirements and candidate policy; Apex Core retains scheduling integration,
authority, verification, retry/rework, and semantic-success ownership. No task
dispatch or execution was added, ECC was not installed, and no permanent
executor was selected.

## Regression evidence

Tests cover proven support, accepted partial support, required NOT_PROVEN
failure, optional unsupported capability, ambiguous equal-best candidates,
duplicate requirement rejection, and repeated deterministic output.

AC-DEV-017 is recorded as DONE / VERIFIED / PROVEN. The registry evidence
states remain constrained by AC-DEV-011 through AC-DEV-016.
