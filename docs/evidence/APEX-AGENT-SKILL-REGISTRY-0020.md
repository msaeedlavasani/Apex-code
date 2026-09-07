# Apex Agent/Skill Registry v1 Evidence 0020

Status: PROPOSED evidence report
Task: AC-DEV-015
Evidence date: 2026-09-08 (Asia/Tehran)

## Result

AC-DEV-015 defines and reconciles the executor-neutral machine-readable
registry at `development_control/agent_skill_registry.json` and its contract
at `docs/governance/APEX-AGENT-SKILL-REGISTRY-v1.md`.

The registry provides stable capability IDs for agent execution, skill
surfaces, and independent verification. It maps Goose CLI, Freebuff CLI, ECC,
and future systems as capability sources only. It does not select an executor,
install ECC, add an adapter, or transfer task semantics, scheduling, authority,
or verification out of Apex.

## Constraint reconciliation

| Constraint | Registry treatment |
|---|---|
| AC-DEV-011 Goose CLI evidence | Bounded strengths are mapped as PROVEN or PARTIAL only where directly observed |
| AC-DEV-012 Freebuff CLI evidence | Parent TUI/model/agent surfaces remain separate from unproven child execution |
| AC-DEV-013 comparison | Executor neutrality and no premature selection remain explicit |
| AC-DEV-014 extension audit | Exact native catalogs, skills, overrides, packaging, and child routing remain NOT_PROVEN |
| ECC boundary | `ecc_installed` is false and all ECC mappings remain NOT_PROVEN |
| Apex ownership | Registry owner is `apex-control-plane`; Core verification and semantic success remain separate |

## Reconciliation

AC-DEV-015 is DONE / VERIFIED with PARTIAL evidence: the registry contract is
defined, while future runtime routing and unsupported source mappings remain
NOT_PROVEN. It depends on AC-DEV-011 through AC-DEV-014. No executor-specific
integration or ECC installation was performed.
