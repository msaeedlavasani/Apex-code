# Goose UI/Desktop Parallel Delegation Capability Probe

Delta: `AC-DEVELOPMENT-CONTROL-PLANE-0015`, task `AC-DEV-007`

Status: **PARTIALLY_PROVEN**

## Executive result

Goose Desktop provides a prompt-driven subagent experience: an operator can
ask Goose to delegate work, request parallel work in natural language, and see
subagent tool activity inline with a link to the subagent session. This is
direct UI evidence from the installed Electron bundle plus official Desktop
documentation, not a CLI-only inference.

The full acceptance target — “Can an Apex operator use Goose UI/Desktop as a
practical parallel delegated-task executor?” — is **NOT_PROVEN**. The current
evidence does not establish native UI controls for independently cancelling a
delegated task, editing/visualizing a dependency graph, or assigning a
different provider/model to each delegated task. No native visual run was
performed because the current CUA environment exposes no native app surface.

This report does not add a Goose dependency, change Apex architecture, or
upgrade any runtime/authority guarantee.

## Scope and provenance

The probe intentionally evaluates Goose UI/Desktop, not Goose CLI behavior.
CLI/runtime observations are included only where they explain a UI surface.

| Item | Observation |
|---|---|
| Installed application | `/Applications/Goose.app` |
| Bundle identifier | `com.electron.goose` |
| Application version | `1.49.0` |
| Prior source pin | `aaif-goose/goose`, tag `v1.49.0`, SHA `71fc4be1ed729e26b1dc0a4466abdd03be548a53` |
| Bundle/source identity | `NOT_PROVEN`; the installed bundle was not rebuilt from the source checkout |
| UI automation state | `apps: []`, `browsers: []`; native app methods were unavailable |
| Credentials/provider execution | Not used |
| Workspace mutation | None |

Official references used for UI claims:

- [Goose Subagents guide](https://goose-docs.ai/docs/guides/context-engineering/subagents/)
- [Goose Subagents tutorial](https://goose-docs.ai/docs/tutorials/subagents/)
- [Goose Summon extension](https://goose-docs.ai/docs/mcp/summon-mcp/)
- [Goose source repository](https://github.com/aaif-goose/goose)

## UI evidence

The installed Electron renderer bundle contains UI handling for:

- `subagent_tool_request` notifications and `subagent_id` values;
- `_meta.subagent_session_id` extraction;
- a visible `View subagent session` action;
- expandable tool details and inline subagent activity presentation.

The official Subagents guide explicitly lists Goose Desktop alongside CLI for
monitoring subagent activity, says that delegation can be requested in natural
language, and documents parallel prompts such as creating multiple artifacts
simultaneously. The tutorial describes parallel frontend/backend subagents and
result aggregation back into the parent interaction.

These observations establish a UI presentation and prompt surface. They do
not establish an Apex-grade task controller or a successful UI-driven run in
this environment.

## Capability matrix

| Apex-required UI capability | UI/Desktop evidence | Classification |
|---|---|---|
| Create/delegate sub-agents | Natural-language delegation is documented for Desktop; bundle renders subagent activity/session links | `PARTIAL_PROVEN` |
| Run delegated work concurrently | Desktop documentation gives parallel prompt semantics; no native run was observed | `PARTIAL_PROVEN` |
| Show/manage multiple active delegated tasks | Inline tool-call activity and “View subagent session” exist; no task board or independent task manager was found | `PARTIAL_PROVEN` |
| Isolate delegated execution state | Documentation describes independent instances; UI carries subagent/session identifiers | `PARTIAL_PROVEN` |
| Aggregate delegated results to parent | Documentation describes successful subagent results returning to the parent interaction; no UI run was observed | `PARTIAL_PROVEN` |
| One sub-task failure leaves unrelated work | Documentation says parallel results include successful work when a subagent fails; UI failure handling was not exercised | `DOCUMENTED_ONLY` |
| Cancel an individual delegated task | Generic conversation cancellation strings exist, but no child-specific cancel control or observed behavior was established | `NOT_PROVEN` |
| Represent delegated-task dependencies | Bundle formatting exposes `depends_on` in a tool-graph display for one tool shape; no general delegated-task dependency UI was established | `NOT_PROVEN` |
| Assign provider/model per delegated task | Current-session model/provider surfaces exist, but no per-delegated-task assignment control or binding evidence was established | `NOT_PROVEN` |

## Acceptance classification

```text
GOOSE_UI_PROMPT_DELEGATION: PARTIAL_PROVEN
GOOSE_UI_PARALLEL_MONITORING: PARTIAL_PROVEN
GOOSE_UI_PRACTICAL_APEX_DELEGATED_EXECUTOR: NOT_PROVEN
AC-DEV-007: VERIFIED_WITH_PARTIAL_EVIDENCE
```

Goose Desktop is a plausible operator surface for conversational delegation
and monitoring. It is not yet proven as a practical Apex parallel delegated-
task executor because the required independent control semantics are not
visible or exercised at the UI boundary.

## Explicit non-claims

This probe does not prove:

- Apex Task/Attempt mapping for Goose subagents;
- durable parent/child task identity or dependency state;
- independent child cancellation;
- failure isolation beyond the documented result behavior;
- per-child model/provider assignment;
- authority isolation or resource ownership;
- controller-loss recovery;
- Goose CLI capability as equivalent to Goose Desktop capability.

## Next evidence required

With a native desktop automation surface or a human-operated disposable run,
repeat the probe in Goose Desktop using harmless independent read-only tasks.
Capture only UI-visible state and structural task identifiers. The run should
demonstrate two concurrent delegated tasks, one failure, one individual
cancellation, a dependency relationship, and any per-task model/provider
selection. Until then, Apex must treat Goose UI parallel delegation as an
experimental capability, not a scheduler or canonical development executor.
