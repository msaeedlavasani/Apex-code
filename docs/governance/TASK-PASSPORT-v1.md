# Apex Code Task Passport v1

Status: **PROPOSED**.

A Task Passport is a revisioned development-control snapshot. It is not a Core `Task`, `Attempt`, `ExecutionManifest`, `AttemptResult`, or completion report. It informs admission and execution requirements without becoming runtime identity.

## Relationship

```text
Development Intent → Task Passport → planning/admission
                  → Development Task → Core Execution Task(s)
                  → Attempt → ExecutionManifest
```

The passport may influence capability requirements, agent/model/runtime requirements, authority-envelope inputs, validation, and risk gates. Core still creates the immutable manifest for each Attempt, and Core owns Task/Attempt/Authority semantics.

## Field classification

| Group | Mandatory | Optional | Derived | Capability-extended |
|---|---|---|---|---|
| Identity | `taskPassportId`, `developmentTaskId`, `revision`, `title` | `taskId` links | timestamps, revision lineage | capability/task aliases |
| Intent | objective, rationale, source, parent request | product narrative | normalized objective | DPT advisory references |
| Scope | allowed scope, forbidden scope, affected contracts/modules | file hints | scope digest | capability-specific scope |
| Dependencies | prerequisites, blockers | related tasks | readiness projection | orchestration dependency metadata |
| Classification | architecture/core/runtime/authority/security/data/UI/dependency/infra/production signals | notes | composable change flags | capability-specific flags |
| Requirements | required capabilities, agent/model/runtime requirements, authority requirements | preferred tools | admission requirements | DPT/Orchestration capabilities |
| Risk | risk class, reversibility, blast radius | risk narrative | risk score/bands | capability risk signals |
| Acceptance | acceptance criteria, completion contract | examples | validation obligations | capability-specific criteria |
| Validation | validation plan, required tests, evidence requirements | optional checks | selected tier matrix | adapter/conformance checks |
| Recovery | rollback expectations | recovery notes | rollback requirement | deployment-specific recovery |
| Control | executor, reviewer, owner decision needed, escalation conditions | notification hints | required approvers | capability routing |
| Audit | created/updated timestamps, PR/commit/result/artifact links | external references | current status | capability result links |
| Readiness | branch/base/worktree, passport completeness, dependency/evidence gates, stopping conditions, receiver, learning destination | retrieval manifest reference | derived admission state (`PASSPORT_INCOMPLETE`, `READY`, `BLOCKED`) | orchestration readiness projections |

`taskId` is a link to a Core Task when one exists; it does not copy runtime identity. `ExecutionManifest` fields such as session identifiers, attempt identity, and immutable execution birth data remain Core-owned.

## Capability requirements

The optional `capability_requirements` Passport field has this shape:

```json
{
  "required": [
    {"capability_id": "agent.parallel_delegation", "minimum_claim_state": "PROVEN"}
  ],
  "optional": [
    {"capability_id": "skill.registry", "minimum_claim_state": "PARTIAL"}
  ]
}
```

Capability IDs resolve only through the executor-neutral Agent/Skill Registry.
Required and optional requirements are distinct. A required capability with no
compatible source, a `NOT_PROVEN`/`NOT_SUPPORTED`/`UNKNOWN` claim, or an
ambiguous best match fails closed. Optional gaps remain visible in the
Candidate Execution Plan without making the plan dispatchable. Matching does
not dispatch work, select a permanent executor, or transfer scheduling,
authority, verification, retry, or semantic-success ownership.

## Execution admission

AC-DEV-018 may consume a Candidate Execution Plan and emit an
`EXECUTION_ADMISSION_DECISION`. The decision is a control-plane projection,
not a Core `ExecutionManifest` or dispatch request. Its status is one of
`ADMITTED`, `BLOCKED_CAPABILITY`, `BLOCKED_AMBIGUITY`, `BLOCKED_POLICY`, or
`HUMAN_GATE_REQUIRED`.

An `ADMITTED` decision selects one compatible source for the task only. It does
not permanently select an executor and it records `dispatch_allowed: false`.
Equal-quality candidates remain blocked as ambiguous unless the supplied
admission policy explicitly permits `SOURCE_ID_ASC` deterministic
tie-breaking. Decisions preserve the Candidate Execution Plan, claim states,
evidence references, selection rationale, and rejected candidates. Scheduling,
authority, verification, retry/rework, and semantic-success ownership remain
with Apex.

## Passport rules

- Every revision records why an authority-relevant field changed.
- A passport narrows, never expands, applicable architecture and authority constraints.
- Admission must fail closed when scope, acceptance, authority, or required evidence is unknown for the change class.
- Admission must fail closed as `PASSPORT_INCOMPLETE` when mandatory fields, dependency acceptance, branch/base/worktree context, or required evidence dependencies are missing.
- Resource class and owner approval requirements are recorded separately from risk and permission authority.
- A passport is a development input; a manifest is an immutable Attempt contract.
- DPT and Orchestration may consume the passport through an optional interface, but DCS works without them.
