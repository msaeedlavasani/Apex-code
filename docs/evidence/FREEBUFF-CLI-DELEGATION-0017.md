# Freebuff CLI Operational Parallel Delegation Probe 0017

Status: PROPOSED evidence report
Task: AC-DEV-012
Evidence date: 2026-09-08 (Asia/Tehran)

## Executive result

The installed Freebuff CLI 0.0.170 reached its interactive TUI in an isolated,
disposable working directory and exposed a parent model picker plus advertised
agent-reference and agent-pane controls. A bounded attempt did not produce a
child worker identity, child session identity, or machine-readable delegated
result. Native operational delegation, true concurrency, child isolation,
failure containment, aggregation, retry/rework, dependency sequencing, and
per-task provider/model assignment therefore remain NOT_PROVEN unless stated
otherwise below.

This probe did not install ECC, modify Apex architecture, select an executor,
or mutate repository state.

## Environment and safety boundary

- Command wrapper: `freebuff`
- Cached runtime observed: `/Users/msl/.config/manicode/freebuff`
- Runtime version: `0.0.170`
- Workspace: disposable non-repository directory supplied through `--cwd`
- Authentication: the existing local application session was used; no
  credential values were opened or printed
- Source comparator: CodebuffAI/freebuff source harvest pinned at commit
  `1310581654df57a5c6cff372dd38d34e7c44c0c5`; source evidence is not runtime
  proof
- No repository files were changed by the probe; the repository `.freebuff/`
  directory was not used as the probe workspace

## Direct runtime observations

1. `freebuff --help` and the cached binary help exposed `login`,
   `--continue`, `--cwd`, `--version`, and help controls, but no batch,
   parallel-task, or delegation subcommand.
2. `freebuff --cwd <disposable-directory>` successfully opened the authenticated
   interactive TUI and displayed the disposable working directory.
3. The parent model picker displayed `DeepSeek V4 Flash 07/31` and `Solar Pro
   4`. This proves only a parent-level model selection surface; it does not
   prove child-level routing.
4. The TUI help displayed `Ctrl+T` for collapsing/expanding agents, `@agents`
   for using an agent, and a tip that `@` can reference agents to spawn or
   files to read. It also displayed parent controls such as `Ctrl+C`/`Esc`,
   `!bash`, and conversation affordances.
5. Entering `@agents` produced a normal assistant response. No child panel,
   worker/session identifier, delegated result, or aggregate result was
   observed. This is evidence of an advertised interaction surface, not
   evidence of successful delegation.

## Agent and skill extensibility inventory

| Surface | Evidence | Classification |
|---|---|---|
| Agent definition/source patterns | Pinned source harvest identifies `AgentDefinition` and an `agents` source area | PARTIAL; source-level only |
| Agent spawning/source patterns | Pinned source harvest identifies `spawn_agents` and `spawnableAgents` | PARTIAL; runtime execution not proven |
| Native TUI agent reference | Runtime help exposes `@agents` and `Ctrl+T` | PROVEN as an advertised surface |
| Exact native agent names in the installed runtime | Not exposed by public help; no reliable local listing | NOT_PROVEN |
| Dedicated Freebuff skill registry or skill invocation | Not observed in help; source harvest does not establish a dedicated registry | NOT_PROVEN |
| Local agent override or curated-agent installation contract | Not established by this probe | NOT_PROVEN |

## Capability classification

| Capability | Classification | Boundary |
|---|---|---|
| Native agent-reference control | PROVEN | TUI advertises `@agents`; child execution was not observed |
| Delegation of multiple independent subtasks | NOT_PROVEN | No child worker/result evidence |
| True concurrency | NOT_PROVEN | No concurrent child executions observed |
| Distinct worker/session identity | NOT_PROVEN | No child identity surfaced |
| Workspace/state isolation | PARTIAL | Parent `--cwd` isolation was observed; child isolation was not |
| Failure containment | NOT_PROVEN | No delegated failure/continuation experiment completed |
| Result aggregation | NOT_PROVEN | No machine-readable aggregate was observed |
| Retry/rework | NOT_PROVEN | Parent continuation affordance is not child rework proof |
| Cancellation | PARTIAL | Parent `Ctrl+C`/`Esc` control is advertised; child cancellation is NOT_PROVEN |
| Dependency sequencing | NOT_PROVEN | No dependency/DAG control was exposed or exercised |
| Per-task model/provider assignment | NOT_PROVEN | Parent model picker only |
| Apex semantic verification ownership | NOT_PROVEN | No independent verifier or Apex acceptance evidence |

## Suitability and reconciliation

Freebuff can remain an exploratory adapter candidate if a future bounded probe
establishes stable child identities, result transport, isolation, and failure
controls. The Control Plane and Apex Core must continue to own task identity,
dependency policy, authority, resource claims, and semantic verification.

AC-DEV-012 is marked DONE / VERIFIED with PARTIAL evidence because the bounded
probe and inventory are complete while most requested operational capabilities
remain NOT_PROVEN. ECC was not installed, and no permanent executor was
selected.

## Reproducibility boundary

The bounded commands were:

```text
freebuff --version
freebuff --help
/Users/msl/.config/manicode/freebuff --help
/Users/msl/.config/manicode/freebuff --cwd <disposable-directory>
```
