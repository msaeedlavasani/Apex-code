# Apex Agent/Skill Registry v1

Status: **PROPOSED**.

The Apex Agent/Skill Registry is an executor-neutral capability catalog. It
gives Task Passports and future routing a stable capability vocabulary without
making Goose, Freebuff, ECC, or any future system an Apex dependency.

## Ownership

- The Apex Control Plane owns capability IDs, claim interpretation, task
  requirements, scheduling, resource claims, and routing policy.
- Apex Core owns runtime authority, Core Task/Attempt state, verification, and
  semantic success.
- Goose, Freebuff, ECC, and future systems are capability or executor sources
  only. A source mapping is evidence, not authority or a permanent selection.
- A capability source cannot elevate its own `PARTIAL`, `NOT_PROVEN`, or
  `UNKNOWN` claim, assign Apex semantic state, or bypass Core verification.

## Canonical artifact

The machine-readable registry is
`development_control/agent_skill_registry.json`. Its stable top-level fields
are:

| Field | Meaning |
|---|---|
| `registry_id` / `revision` | Registry identity and revision lineage |
| `claim_states` | Closed vocabulary for evidence strength |
| `sources` | Executor, curated, or future capability sources |
| `capabilities` | Stable capability IDs and source mappings |
| `permanent_executor_selected` | Must remain `false` until a separate approved decision |
| `ecc_installed` | Must remain `false` for the current bounded registry |

Each capability has a stable `capability_id`, a `kind`, a human-readable title,
and `source_mappings`. Each mapping contains a `source_id` and `claim_state`,
with notes only where the evidence boundary needs explanation.

## Passport and routing consumption

Task Passports may reference registry `capability_id` values as requirements;
they must not copy source-specific identity into Core Task or ExecutionManifest
fields. A future router may match a Passport requirement to a source mapping
only when the required claim state is satisfied and all Passport authority,
dependency, resource, and verification gates are independently satisfied.

`NOT_PROVEN` and `UNKNOWN` never satisfy a proven capability requirement.
`PARTIAL` satisfies only a Passport that explicitly accepts partial evidence.
Registry claims do not replace runtime conformance, independent verification,
or acceptance evidence.

## Current evidence boundary

AC-DEV-011 through AC-DEV-014 provide bounded Goose and Freebuff evidence. The
registry records Goose's observed bounded strengths, Freebuff's parent/source
surfaces, and unsupported mappings explicitly. ECC is listed as not installed;
its mappings remain `NOT_PROVEN`. No executor is selected and no executor-
specific integration is introduced by this registry.
