# Executor Capability Comparison 0018

Status: PROPOSED evidence report
Task: AC-DEV-013
Evidence date: 2026-09-08 (Asia/Tehran)

## Executive result

The verified evidence makes Goose CLI the stronger currently demonstrated
candidate for bounded parallel execution: AC-DEV-011 produced distinct child
IDs, asynchronous delegated work, JSON aggregation, and partial failure
containment. Freebuff CLI currently proves only an interactive parent surface,
an advertised agent-reference control, and a parent model picker; its child
execution capabilities remain mostly NOT_PROVEN.

Neither result authorizes permanent executor selection. Both remain replaceable
adapter candidates, and the Control Plane remains the owner of task identity,
dependencies, authority, resources, verification, and reconciliation. ECC was
not installed.

## Evidence basis

- Goose: `docs/evidence/GOOSE-CLI-DELEGATION-0016.md`, AC-DEV-011
- Freebuff: `docs/evidence/FREEBUFF-CLI-DELEGATION-0017.md`, AC-DEV-012
- Control Plane implementation and event-ordering evidence remains in
  `docs/evidence/DEVELOPMENT-CONTROL-PLANE-0015.md`
- Freebuff source-level comparison is bounded by the pinned harvest of
  CodebuffAI/freebuff commit `1310581654df57a5c6cff372dd38d34e7c44c0c5`;
  source evidence is not runtime proof

## Capability matrix

| Dimension | Goose CLI | Freebuff CLI | Apex / Control Plane implication |
|---|---|---|---|
| Parallelism | PROVEN for three asynchronous delegated workers | NOT_PROVEN; `@agents` is an advertised surface only | Schedule through an adapter until Freebuff child execution is proven |
| Isolation | PARTIAL; workers did not touch the repository, but unique child cwd isolation was not proven | PARTIAL; parent `--cwd` isolation observed, child isolation NOT_PROVEN | Keep resource claims and workspace policy above the executor |
| Failure / recovery | Failure containment PROVEN for unrelated workers; retry/rework PARTIAL; process recovery NOT_PROVEN | NOT_PROVEN | Core-owned failure state and rework remain authoritative |
| Controllability | PARTIAL; child cancellation, dependency sequencing, and per-child routing not proven | PARTIAL; parent `Ctrl+C`/`Esc` advertised, child controls NOT_PROVEN | Preserve explicit NOT_PROVEN controls in the adapter contract |
| Observability | PROVEN child IDs and JSON aggregate; semantic acceptance remains separate | PARTIAL TUI transcript, cwd, and parent model surface; no child IDs/results | Executor facts must not be confused with Apex verification |
| Agent extensibility | PARTIAL summon/extension operation pipeline; Apex agent contract not proven | PARTIAL source patterns plus TUI `@agents`; exact names, runtime use, and skills NOT_PROVEN | Curated catalog and compatibility contract must be Apex-owned |
| Provider / model flexibility | PARTIAL parent routing; per-subtask assignment unsupported | PARTIAL parent model picker; per-task assignment NOT_PROVEN | Treat provider/model routing as parent-level until proven otherwise |
| Control Plane integration | PARTIAL through a replaceable executor adapter; no direct integration proven | PARTIAL conceptually through the same adapter boundary; no direct integration proven | No executor-specific ownership may enter Apex Core |

## Viability: Freebuff native agents plus curated Apex/ECC agents/skills

The combination is viable only as a layered design: Freebuff-native agents may
serve as executor worker profiles, while curated Apex or ECC agents/skills are
versioned and selected by Apex policy, then projected into the executor through
an adapter. The executor must not become the authority for task identity,
dependencies, acceptance, or security.

Current viability is PARTIAL and operationally NOT_PROVEN because Freebuff has
not yet exposed enough child identity, result, isolation, or failure evidence to
support that composition. Exact native agent names, a dedicated skill registry,
and an install/override contract are also NOT_PROVEN. ECC compatibility cannot
be assessed by installation in this task because ECC was explicitly not
installed.

Agent self-report, source symbols, or a successful parent response are not
independent proof of delegated task completion or Apex semantic success.

## Decision and reconciliation

AC-DEV-013 is marked DONE / VERIFIED with PARTIAL evidence: the comparison is
complete, but unsupported capabilities remain visible as NOT_PROVEN. AC-DEV-011
and AC-DEV-012 are recorded as dependencies. AC-DEV-010 remains deferred, no
permanent executor is selected, no ECC installation is initiated, and no Apex
Core architecture change is introduced.
