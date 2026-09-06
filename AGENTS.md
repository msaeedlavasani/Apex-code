# Apex Code Agent Contract

This is the mandatory operating contract for agents working in Apex Code.
`AGENTS.md` defines how to work; it does not replace architecture, product,
governance, or evidence documents.

## Entry protocol

1. Verify repository identity, branch, worktree, and remote state.
2. Read this file and route through [`docs/CONTEXT-MAP.md`](docs/CONTEXT-MAP.md).
3. Read the bounded Current State when one exists and identify the active
   Development Task and Task Passport; do not treat chat memory as state.
4. Read only the minimum canonical sources required by the route.
5. Classify scope, change/decision class, risk, resource class, and whether
   Owner approval is required.
6. Distinguish `CURRENT`, `TARGET`, `CONSTRAINT`, `DEBT`, and `UNKNOWN`.
7. Plan before non-trivial mutation; execute only within accepted scope.
8. Validate with the narrowest responsible checks, record evidence, and report
   what was actually verified.
9. Apply System-First Correction when a recurring defect indicates a missing
   shared control.
10. Complete the handoff/report and close the branch or work state correctly.

## Operating rules

- Inspect before editing. Preserve unrelated user work and `.freebuff/`.
- Prefer `reuse → compose → extend → create`; make the smallest coherent change.
- Do not silently redesign architecture, change a `FROZEN` rule, or invent facts.
- `NOT_PROVEN`, `UNKNOWN`, `NOT_RUN`, and `BLOCKED` must remain visible.
- Never claim validation that was not executed. Documentation is not runtime
  proof, and an agent’s assertion is not acceptance.
- Never read, print, commit, or expose secrets, credentials, private keys, or
  real environment values.
- DPT and Orchestration are optional. Apex Core must not depend on either.
- Preserve `Task != Attempt`, Development Task != Core Task, Task Passport !=
  ExecutionManifest, and development lifecycle != runtime lifecycle.
- A change to a `FROZEN` architectural rule requires explicit rationale,
  affected contracts, status/evidence updates, and architecture review under
  [`ARCHITECTURE-CHANGE-POLICY.md`](docs/governance/ARCHITECTURE-CHANGE-POLICY.md).
- Escalate ambiguous destructive actions, authority/security expansion,
  production impact, irreversible migrations, conflicting canonical sources,
  unclear acceptance, material product/commercial decisions, and critical risk.

## PLAN / EXECUTE and branch closure

PLAN inspects, identifies contracts and risks, defines scope, acceptance, and
validation. EXECUTE mutates only the approved package, then validates and
reports. Trivial, safe, reversible work may use a lightweight plan; material,
architecture, runtime, authority, security, data, infrastructure, or production
work requires planning and the approvals defined by the governing documents.

Development branches record purpose, base, Task/Passport, receiver, and closure
condition. The normal path is branch → PR → validation → review → merge →
verify target → retire branch. Commit, push, merge, and deploy are separate
permissions. A completion report records changed files, validation results,
evidence, acceptance, risks, rollback, unknowns, artifacts, and follow-up.
