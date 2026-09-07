# Freebuff Agent/Skill Extension Surface Audit 0019

Status: PROPOSED evidence report
Task: AC-DEV-014
Evidence date: 2026-09-08 (Asia/Tehran)

## Executive result

The approved Freebuff evidence supports a layered extension boundary, but not a
verified Freebuff-native agent or skill installation contract. The installed
CLI exposes an interactive `@agents` surface, while the pinned source harvest
shows agent-definition and spawning patterns. Exact native agent names, a
dedicated skill registry, skill invocation semantics, local override behavior,
and per-task provider/model injection remain NOT_PROVEN.

AC-DEV-014 is therefore DONE / VERIFIED with PARTIAL evidence. No ECC was
installed, no source was imported, no adapter was implemented, and no permanent
executor was selected.

## Evidence boundary

- Runtime evidence: `docs/evidence/FREEBUFF-CLI-DELEGATION-0017.md`
- Executor comparison: `docs/evidence/EXECUTOR-CAPABILITY-COMPARISON-0018.md`
- Source-level comparator: pinned CodebuffAI/freebuff harvest at commit
  `1310581654df57a5c6cff372dd38d34e7c44c0c5` in
  `docs/evidence/AGENTIC-DEVELOPMENT-SYSTEMS-COMPARATIVE-HARVEST.md`
- This audit reuses those bounded observations; source symbols and parent UI
  responses are not treated as delegated-task or Apex semantic proof.

## Extension surface inventory

| Surface | Evidence | Classification |
|---|---|---|
| Native agent reference | TUI help exposes `@agents` and `Ctrl+T`; bounded use did not produce a child worker | PARTIAL |
| Agent definition model | Source harvest identifies `AgentDefinition` and an `agents` source area | PARTIAL; source-level only |
| Agent spawning | Source harvest identifies `spawn_agents` and `spawnableAgents` | PARTIAL; runtime execution NOT_PROVEN |
| Exact native agent catalog | Public help and bounded runtime did not expose a reliable list | NOT_PROVEN |
| Dedicated skill registry | No dedicated Freebuff registry established by runtime help or the pinned harvest | NOT_PROVEN |
| Skill invocation semantics | No bounded runtime skill invocation observed | NOT_PROVEN |
| Local agent/skill override | No documented or runtime-proven override contract | NOT_PROVEN |
| Curated agent/skill packaging | No install/import contract established | NOT_PROVEN |
| Provider/model injection | Parent model picker observed; per-agent or per-task assignment not proven | PARTIAL at parent level; child routing NOT_PROVEN |
| Independent verification hook | No Freebuff-native Apex semantic verifier observed | NOT_PROVEN |

## Safe Apex composition boundary

Freebuff-native agents may be treated as replaceable worker profiles only after
an adapter proves stable identity, result transport, isolation, and failure
controls. Curated Apex agents and skills should remain versioned Apex policy
inputs, with the Control Plane owning task identity, dependencies, resource
claims, authority, acceptance, and reconciliation. A future ECC composition
must use the same projection boundary; ECC compatibility is NOT_PROVEN until a
separate approved task establishes it.

The extension surface must not grant an executor authority to assign Apex
semantic state, bypass Core verification, or persist credentials.

## Reconciliation

AC-DEV-014 depends on AC-DEV-012 and AC-DEV-013 and is recorded as DONE /
VERIFIED / PARTIAL. Unsupported claims remain visible as NOT_PROVEN. The
Control Plane backlog and Passport are the canonical task record; this report
does not change Apex Core or select an executor.
