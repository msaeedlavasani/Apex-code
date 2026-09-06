# Agentic Development Systems Comparative Harvest

**Status:** Research evidence; no architecture decision.
**Inspection date:** 2026-09-07
**Scope:** 13 Owner-selected systems; four deep source traces and nine bounded targeted traces.
**Repository snapshot:** `ec48b06901ca70932ff1d5bed714f07ece236675` was verified as the Apex Code `main` base before this branch was created.

## 1. Purpose and scope

This report compares concrete implementation patterns relevant to Apex Code's execution, development-control, runtime-adapter, verification, recovery, product-shell, and future projection concerns. It is not a feature-count ranking and does not authorize adoption, dependency addition, source reuse, implementation, or architecture change.

The selected systems are research inputs only. Apex Code remains standalone; DPT and Orchestration remain optional and independent; OpenWork is a replaceable Product Shell/Foundation candidate; OpenCode is a first runtime substrate candidate rather than Apex identity. Apex authority remains Core-owned, and the complete authority materialization/binding guarantee remains `NOT_PROVEN`.

## 2. Method and evidence vocabulary

Each reference was inspected in a read-only local checkout pinned to one exact commit. Evidence was not silently mixed across revisions. The common trace was:

`User Input → Entry → Context → Planning → Task/Delegation → Selection → Workspace/Session → Permission → Execution → Results → Review/Validation → Retry/Recovery → Completion/Persistence`.

The report uses Apex's evidence vocabulary:

- `SOURCE_CODE_EVIDENCE` — behavior visible in implementation.
- `DOCUMENTATION_EVIDENCE` — claim made by repository documentation or type comments.
- `OBSERVED_REPOSITORY_STATE` — directly observed tree, ref, license, or configuration state.
- `OBSERVED_RUNTIME_EVIDENCE` — not collected in this source-only task unless explicitly stated.
- `INFERENCE` — reasoned interpretation from evidence, not direct proof.
- `UNKNOWN` — not established by the inspected sources.
- `NOT_PROVEN` — a required guarantee lacks direct evidence.

Comparison values use `YES`, `PARTIAL`, `NO`, `NOT_PROVEN`, and `N/A`. `YES` means the inspected source supports the narrow property; it does not mean Apex-grade semantics are established.

## 3. Source snapshots and license boundary

| System | Official source | Default branch | Inspected commit | License observed at snapshot | Relevant paths |
|---|---|---:|---|---|---|
| OpenCode | [anomalyco/opencode](https://github.com/anomalyco/opencode) | `dev` | `e207624c48159b03dbe17dbc8e51bbcf23e72df5` | MIT (`LICENSE`) | `packages/core/src/session`, `packages/core/src/event.ts`, `packages/core/src/permission.ts`, `packages/server/src` |
| OpenHands | [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) | `main` | `f7fb0c4b21f5ed726edbba8a6309634ef434b004` | MIT (`LICENSE`) | `AGENTS.md`, `src/routes`, `src/contexts`, `src/services`, `src/stores`, `src/types`, tests |
| Vibe Kanban | [BloopAI/vibe-kanban](https://github.com/BloopAI/vibe-kanban) | `main` | `4deb7eca8f381f7cbc1f9d15515a9ab8f8009053` | Apache-2.0 (`LICENSE`) | `crates/db`, `crates/executors`, `crates/local-deployment`, `crates/workspace-manager`, `crates/git`, `crates/review` |
| Vigla | [Kilbex/Vigla](https://github.com/Kilbex/Vigla) | `main` | `bbd19ae2d5a77401502756c550b5dcd4ae59bbc9` | Apache-2.0 (`LICENSE`) | `crates/event-schema`, `crates/orchestrator/src/supervisor`, `crates/orchestrator/src/mission_workspace`, `app/src` |
| OpenWork | [different-ai/openwork](https://github.com/different-ai/openwork) | `dev` | `9a64fe1087aff7f5c552a446595d1325e1d1a91b` | MIT outside `ee/`; OpenWork EE License under `ee/`; see `LICENSE`, `LICENSES/LicenseRef-OpenWork-EE.txt`, `ee/LICENSE` | `apps/server`, `apps/desktop/electron`, `packages/runtime`, `packages/opencode-plugin`, `integrations/agent-plugins` |
| Freebuff | [CodebuffAI/freebuff](https://github.com/CodebuffAI/freebuff) | `main` | `1310581654df57a5c6cff372dd38d34e7c44c0c5` | Apache-2.0 (`LICENSE`) | `AGENTS.md`, `agents`, `packages/agent-runtime`, `sdk`, `common`, `cli` |
| Goose | [aaif-goose/goose](https://github.com/aaif-goose/goose) | `main` | `5e90925962f05acf8e255032de44d16c4a7768a2` | Apache-2.0 (`LICENSE`) | `crates/goose-agent`, `crates/goose-provider-types`, `crates/goose-providers`, `crates/goose/src/session`, `crates/goose/src/permission` |
| LangGraph | [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | `main` | `81bf17b23123e4ef8b9d5f49fa09a0122fc2edd1` | MIT (`LICENSE`) | `libs/langgraph/langgraph/graph`, `libs/langgraph/langgraph/pregel`, `libs/langgraph/langgraph/types.py`, `libs/checkpoint` |
| agtx | [fynnfluegge/agtx](https://github.com/fynnfluegge/agtx) | `main` | `d307c4c182dff19a65370a50403185cb826f7f49` | Apache-2.0 (`LICENSE`) | `src/db`, `src/core`, `src/agent`, `src/tmux`, `src/git`, `src/tui`, `src/web`, `plugins/agtx/skills` |
| E2B | [e2b-dev/E2B](https://github.com/e2b-dev/E2B) | `main` | `473d8bf3e62b68ee731cf18afb2e8258f9ca7a7c` | Apache-2.0 (`LICENSE`) | `packages/js-sdk/src/sandbox`, `packages/code-interpreter-js`, `packages/desktop-js`, API/schema/tests |
| Daytona | [daytonaio/daytona](https://github.com/daytonaio/daytona) | `main` | `ec4c21b2d597091ac09ecc278f3bcc172575a987` | No license file present in the inspected tree; README links historical `v0.190.0` license | `README.md` only at this snapshot |
| Nimbalyst | [nimbalyst/nimbalyst](https://github.com/nimbalyst/nimbalyst) | `main` | `34b14f33e48fd639d32c0f5eb7d77561bdccd2a4` | MIT (`LICENSE`) | `docs/SESSION_HIERARCHY.md`, `docs/WORKTREES.md`, `docs/STATE_PERSISTENCE.md`, `docs/AGENT_PERMISSIONS.md`, `docs/EXTENSION_ARCHITECTURE.md`, `packages/extension-sdk` |
| Agent Mission Control | [glglak/agent-mission-control](https://github.com/glglak/agent-mission-control) | `main` | `39e2e3bd7ffa88e1296360e8833b099435f4c6a8` | No license file present in the inspected tree | `packages/shared/src/events`, `packages/telemetry-bridge`, `packages/simulation-engine`, `apps/web` |

**License caution:** license presence or permissiveness does not by itself make code reusable in Apex. OpenWork's split license is material: conceptual learning is available, but the `ee/` source has subscription terms. Daytona and Agent Mission Control require an explicit legal review before any code reuse because no license file was present at the pinned snapshot. No external source code is copied by this report.

## 4. Comparative matrix: execution, task, and attempt

| System | Domain task | Separate attempt/retry identity | Immutable execution birth metadata | Durable state | Semantic success beyond process/runtime completion |
|---|---|---|---|---|---|
| OpenCode | NO; `Session` is primary work unit | PARTIAL; provider turns/tools, no Apex Attempt entity | NO / `NOT_PROVEN` | YES, SQLite session/message/event tables | NOT_PROVEN |
| OpenHands | PARTIAL; conversation/automation surfaces | NOT_PROVEN; backend external to checkout | NOT_PROVEN | PARTIAL; client/API state and automation history are exposed | PARTIAL; UI distinguishes task/error but acceptance is not proven |
| Vibe Kanban | YES; `Task` row | PARTIAL; `ExecutionProcess` rows and follow-up sessions, no immutable Attempt contract | NO / `NOT_PROVEN` | YES, SQLite task/workspace/process records | PARTIAL; review/PR flow is separate from process status |
| Vigla | YES; `TaskInfo` | PARTIAL; retry creates new `WorkerInfo` while retaining task id | PARTIAL; worker/task/event identity is persisted, not Apex Manifest | YES, repository/event store | PARTIAL; `Completion` is worker-reported and review/arbiter semantics are separate |
| OpenWork | PARTIAL; workspace/session/capability request | NOT_PROVEN | NOT_PROVEN | PARTIAL; filesystem-backed workspace/server/audit state | NOT_PROVEN |
| Freebuff | NO; agent run/session shape | PARTIAL; SDK retries and snapshots, no stable Attempt contract | NO / `NOT_PROVEN` | PARTIAL; host-provided snapshots and run persistence hooks | NOT_PROVEN |
| Goose | NO; conversation/session shape | PARTIAL; provider retry and session resume/fork | NO / `NOT_PROVEN` | YES for sessions/messages | NOT_PROVEN |
| LangGraph | PARTIAL; graph node/Pregel task | YES at task execution level, but not Apex Attempt semantics | PARTIAL; checkpoint metadata/run ids | YES when checkpointer configured | PARTIAL; graph result is not domain acceptance |
| agtx | YES; SQLite kanban `Task` | PARTIAL; task cycle and running agent, no immutable Attempt | NO / `NOT_PROVEN` | YES, SQLite | PARTIAL; Review column and PR linkage are separate |
| E2B | NO; sandbox/process/code execution | NO for agent attempts | NO | YES for sandbox lifecycle/snapshots, not task ledger | NO / `NOT_PROVEN` |
| Daytona | NOT_PROVEN; source absent | NOT_PROVEN | NOT_PROVEN | DOCUMENTED only | NOT_PROVEN |
| Nimbalyst | PARTIAL; session/worktree grouping | NOT_PROVEN | NOT_PROVEN | YES, SQLite/electron stores documented | NOT_PROVEN |
| Agent Mission Control | PARTIAL; telemetry task events | NO / `NOT_PROVEN` | NO | YES for event telemetry database | NO; simulation projection consumes event facts |

No selected external system proves Apex's required invariant that every retry is a new Apex `Attempt` with exactly one immutable `ExecutionManifest`, nor the full AuthorityRevision-to-RuntimeLane binding guarantee.

## 5. Comparative matrix: delegation, scheduling, routing, and recovery

| System | Delegation / multi-agent | True parallelism | Dependency-aware readiness | Fallback / reassignment | Retry / recovery / reconciliation |
|---|---|---|---|---|---|
| OpenCode | NO domain delegation; plugin/tool extension | YES across different sessions; per-session serialized | NO | NOT_PROVEN | Provider retry and snapshot/revert slices; durable recovery TODO in `packages/core/src/session/runner/llm.ts` |
| OpenHands | PARTIAL child conversations and automation | PARTIAL / backend not locally inspected | NOT_PROVEN | NOT_PROVEN | Cloud sandbox resume and client recovery paths; backend recovery NOT_PROVEN |
| Vibe Kanban | PARTIAL executor actions and follow-ups | YES across workspace/process handles | PARTIAL; task row and workspace lifecycle, not DAG | PARTIAL executor-profile validation; reassignment NOT_PROVEN | Process status, cancellation, queued follow-up; crash reconciliation NOT_PROVEN |
| Vigla | YES supervisor/worker | YES, worker slots and concurrent child processes | YES, `DispatchRequest.depends_on` and pending queue | PARTIAL; vendor-aware resume support, no general next-best selection | YES for bounded retry/backoff, stop, resume where adapter supports it; controller-loss reconciliation NOT_PROVEN |
| OpenWork | PARTIAL capability execution and renderer mailbox | NOT_PROVEN | NO | NOT_PROVEN | Provider title recovery and renderer crash recovery; product-workflow recovery NOT_PROVEN |
| Freebuff | YES `spawn_agents` | YES, `Promise.allSettled` in `spawn-agents.ts` | NO durable DAG | NO general reassignment | Provider/API retry and state snapshots; clean run completion is not independent verification |
| Goose | PARTIAL operation pipeline/extensions | NOT_PROVEN | NO | Provider fallback/refresh varies | Provider exponential retry; session resume/fork; process-loss recovery NOT_PROVEN |
| LangGraph | YES graph nodes/subgraphs/`Send` | YES Pregel task execution | YES graph edges, barriers/join channels, checkpointed tasks | NOT_PROVEN | RetryPolicy, interrupt/resume, checkpoint replay; exact process-loss reconciliation depends on runtime/checkpointer |
| agtx | PARTIAL orchestrator skills and board | PARTIAL via separate tmux sessions | PARTIAL referenced tasks/dependency checks | NOT_PROVEN | Transition requests, agent status, no demonstrated durable requeue/reconciliation |
| E2B | N/A | YES sandbox/process concurrency possible | N/A | N/A | Sandbox reconnect, pause/resume/snapshot and killed-process handling; no agent workflow recovery |
| Daytona | DOCUMENTED platform/control plane | DOCUMENTED parallelization | NOT_PROVEN | NOT_PROVEN | DOCUMENTED persistence/snapshots; implementation unavailable at ref |
| Nimbalyst | PARTIAL session/worktree collaboration | PARTIAL; one worktree can have multiple sessions | NO | NOT_PROVEN | Persistence migration defaults and worktree reliability docs; task recovery NOT_PROVEN |
| Agent Mission Control | NO execution orchestrator observed | N/A; event/UI processing | NO | NO | Event replay/time seek, not execution recovery |

## 6. Comparative matrix: workspace, runtime, authority, result, and UX

| System | Workspace / isolation | Authority / permission | Runtime / session boundary | Result / verification | Product / visual model |
|---|---|---|---|---|---|
| OpenCode | Project directories, snapshots/revert; lane isolation NOT_PROVEN | Tool permission rules and server auth; per-attempt authority NOT_PROVEN | Provider/tool runtime behind Core registry; session IDs are product/session IDs | Typed tool settlement and events; semantic acceptance NOT_PROVEN | CLI/TUI/web server surfaces, transcript/event projection |
| OpenHands | Workspace/sandbox lifecycle through client/backend contracts | Backend/server permissions and cloud sandbox state; exact binding NOT_PROVEN | Conversation and automation services, external SDK/Agent Server | Task/error UI and event stores; independent verification NOT_PROVEN | Agent Canvas/control-center and automation UX |
| Vibe Kanban | Git worktrees per workspace; process cwd bound to workspace | Executor approval service for tool calls; no Apex PermissionEnvelope | Executor profiles spawn child processes; follow-up session ids | Review action and PR/branch workflows; process status not task success | Kanban task/workspace/review UI |
| Vigla | Worker `cwd` is own worktree; mission workspaces; revert anchors | Adapter/operator events include review witnesses; Apex authority binding NOT_PROVEN | Vendor CLI adapter + supervisor + worker identity | Typed Completion/Failure, Review state, arbiter-oriented event schema | Station canvas, event feed, result/diff/replay views |
| OpenWork | Dedicated/local/remote workspace and filesystem server | Manual/auto host approvals, owner/collaborator/viewer tokens, scoped capabilities | Desktop, server, OpenCode proxy, MCP/plugin integrations | Audit/events/artifacts endpoints; success contract NOT_PROVEN | Replaceable desktop/web shell, Den control plane |
| Freebuff | File context and host terminal broker; sandbox/host boundary varies | Agent tool list/spawnableAgents, API identity, tool execution host; per-attempt authority NOT_PROVEN | SDK runtime + CLI + framework agent definitions | `set_output`, aggregated subagent reports, snapshots; no independent verifier |
| Goose | Working directory per session; extension/tool boundary | Tool permissions persisted by context hash and expiry; global/session semantics, no Apex binding | Provider abstraction + MCP extensions + session manager | Conversation messages and tool results; acceptance NOT_PROVEN | CLI, gateway/SDK, persistent chat sessions |
| LangGraph | Abstract graph state, not workspace isolation | No domain permission model in core | Graph/checkpointer/runtime abstraction | Task/debug streams and checkpoints; result is graph state |
| agtx | Git worktree path and tmux session per task | Caller-specific action validation plus command broker; no per-attempt authority | TUI/web/MCP request queue → tmux agent | Review board, PR linkage, notifications; no independent verifier |
| E2B | Strong sandbox boundary: filesystem, process, PTY, network/egress, optional IAM | Sandbox credentials/network rules; not Apex semantic authority | `Sandbox` id + envd/control-plane API + process handles | Command/code execution results and error classes |
| Daytona | README documents full isolated computer/sandbox/control/compute planes | Documented platform/API/network controls; source not available | Sandbox + SDK/API/CLI; implementation NOT_PROVEN | Logs/code/process APIs; semantic acceptance NOT_PROVEN |
| Nimbalyst | Git worktrees, workspace/session hierarchy, renderer/main IPC | Project-scoped trust, remembered patterns, path/URL/command controls | Electron main/runtime/provider and persisted session/worktree ids | Diffs/editor lifecycle; independent verification NOT_PROVEN |
| Agent Mission Control | No execution sandbox; telemetry session/agent projection | No authority model observed | Telemetry events and simulation engine | Event payloads, analytics, replay; no semantic completion authority |

### 6.1 Cross-system matrix across the required comparison dimensions

The matrix below provides a compact normalized index across all 15 requested
areas. `YES` and `PARTIAL` refer only to the bounded evidence in this report;
they do not establish Apex-grade guarantees. The per-system profiles contain
the supporting paths and qualifications.

| System | Execution / Task / Attempt | Delegation / Multi-agent / Parallelism | Scheduling / DAG / Dependencies | Routing / Reassignment / Fallback | Workspace / Isolation / Authority | Runtime / Session / Sandbox | Result / Verification / Completion | Retry / Recovery / Reconciliation | Persistence / Durable State | Human Gates / Intervention | Events / Artifacts / Provenance | Product Shell / UX | Visual / Mission Control | License / Reuse | Apex learning value |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| OpenCode | PARTIAL | PARTIAL | NO | PARTIAL | PARTIAL | YES | PARTIAL | PARTIAL | YES | YES | YES | YES | N/A | MIT | HIGH |
| OpenHands | PARTIAL | PARTIAL | NOT_PROVEN | NOT_PROVEN | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | YES | YES | PARTIAL | MIT | HIGH |
| Vibe Kanban | YES | PARTIAL | PARTIAL | PARTIAL | YES | YES | YES | PARTIAL | YES | YES | PARTIAL | YES | N/A | Apache-2.0 | HIGH |
| Vigla | YES | YES | YES | PARTIAL | YES | YES | PARTIAL | YES | YES | YES | YES | YES | PARTIAL | Apache-2.0 | HIGH |
| OpenWork | PARTIAL | PARTIAL | NOT_PROVEN | NOT_PROVEN | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | YES | YES | YES | PARTIAL | MIT/EE | HIGH |
| Freebuff | PARTIAL | YES | NO | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | NO | PARTIAL | YES | N/A | Apache-2.0 | MEDIUM |
| Goose | PARTIAL | PARTIAL | NO | PARTIAL | PARTIAL | YES | PARTIAL | PARTIAL | YES | PARTIAL | PARTIAL | YES | N/A | Apache-2.0 | MEDIUM |
| LangGraph | PARTIAL | YES | YES | PARTIAL | N/A | PARTIAL | PARTIAL | YES | YES | YES | YES | PARTIAL | N/A | MIT | HIGH |
| agtx | YES | PARTIAL | PARTIAL | PARTIAL | YES | PARTIAL | PARTIAL | PARTIAL | YES | PARTIAL | PARTIAL | YES | N/A | Apache-2.0 | MEDIUM |
| E2B | NO | N/A | N/A | N/A | YES | YES | PARTIAL | YES | YES | N/A | PARTIAL | PARTIAL | N/A | Apache-2.0 | HIGH |
| Daytona | NOT_PROVEN | NOT_PROVEN | NOT_PROVEN | NOT_PROVEN | PARTIAL | PARTIAL | NOT_PROVEN | PARTIAL | PARTIAL | NOT_PROVEN | PARTIAL | PARTIAL | N/A | source gap | MEDIUM |
| Nimbalyst | PARTIAL | PARTIAL | NO | NOT_PROVEN | YES | PARTIAL | PARTIAL | PARTIAL | YES | YES | PARTIAL | YES | PARTIAL | MIT | MEDIUM |
| Agent Mission Control | PARTIAL | NO | NO | NO | NO | NO | NO | NO | YES | NO | YES | YES | YES | no license observed | MEDIUM |

The `License / Reuse` column records the observed boundary, not a legal
conclusion. `Apex learning value` is a research prioritization signal, not an
adoption decision.

## 7. Deep harvest profiles

### 7.1 OpenCode — `e207624c...`

**A. Identity.** Open-source TypeScript/Effect runtime and product server; official source is [anomalyco/opencode](https://github.com/anomalyco/opencode), `dev`, `e207624c48159b03dbe17dbc8e51bbcf23e72df5` (`SOURCE_CODE_EVIDENCE`, `OBSERVED_REPOSITORY_STATE`).

**B. Product / system shape.** `packages/core` owns sessions, events, tools, providers, projects, and permissions; `packages/server` exposes product/server handlers. The split supports a runtime-neutral Core/server seam, but it is not Apex's Core contract (`SOURCE_CODE_EVIDENCE`).

**C. Entry points.** `packages/core/src/session.ts` exposes create/get/list/prompt/resume/interrupt-style session operations; `packages/server/src/handlers/session.ts` is a server entry surface (`SOURCE_CODE_EVIDENCE`).

**D. Context model.** `packages/core/src/session/sql.ts`, `history.ts`, and `context-epoch.ts` persist message/event context; `SessionContextEpoch` is a context compaction baseline, not Apex `ExecutionEpoch` (`SOURCE_CODE_EVIDENCE`, `INFERENCE`).

**E. Planning model.** `packages/core/src/session/runner/llm.ts` builds a provider request, streams the turn, executes tools, compacts on overflow, and continues. A durable product planning/task contract is `NOT_PROVEN`.

**F. Task / work unit.** The durable unit is `SessionTable`; `SessionMessageTable` and `PartTable` hold transcript parts. No domain Task/Attempt aggregate was found (`SOURCE_CODE_EVIDENCE`).

**G. Delegation model.** Tool/plugin registry is visible; a durable multi-agent delegation model was not found (`SOURCE_CODE_EVIDENCE`, `NOT_PROVEN`).

**H. Multi-agent model.** No Apex-like supervisor/worker model was established (`NOT_PROVEN`).

**I. Parallelism.** `packages/core/src/session/run-coordinator.ts` maintains a `Map<Key,Entry>`, serializes each key, and allows different keys to run concurrently; `packages/core/src/session/execution.ts` describes ownership as “this process” (`SOURCE_CODE_EVIDENCE`).

**J. Scheduling / dependency.** No dependency-aware durable scheduler was found. The coordinator is per-session concurrency control, not a DAG (`SOURCE_CODE_EVIDENCE`, `NOT_PROVEN`).

**K. Agent / runtime selection.** `runTurnAttempt` loads agent/model/tools and passes them into `LLM.request`; provider selection is concrete, but Apex-style `AgentSelection`/`ModelSelection` birth metadata is absent (`SOURCE_CODE_EVIDENCE`).

**L. Model / provider.** `packages/core/src/provider.ts` and the LLM runner abstract provider requests. Runtime/provider substitution is a useful seam; the exact contract is not Apex's Runtime Adapter SPI (`SOURCE_CODE_EVIDENCE`).

**M. Workspace / isolation.** Project directory types and snapshot/revert paths exist in `packages/core/src/project/sql.ts` and `packages/core/src/session/revert.ts`; per-attempt workspace isolation is `NOT_PROVEN`.

**N. Permission / authority.** `packages/core/src/permission.ts` evaluates ordered rules, defaults missing agent permissions to deny-all, emits permission questions, waits for replies, and can raise `BlockedError`. `packages/server/src/middleware/authorization.ts` authenticates server access; neither proves Apex AuthorityRevision binding (`SOURCE_CODE_EVIDENCE`, `NOT_PROVEN`).

**O. Runtime / session.** `SessionExecution` and `SessionRunCoordinator` own local process execution; runtime-specific IDs are embedded in session/provider context. Cluster ownership, durable attempt status, and stale-runtime rejection are explicit TODOs in `packages/core/src/session/runner/llm.ts` (`SOURCE_CODE_EVIDENCE`).

**P. Execution lifecycle.** `runTurnAttempt` records/streams provider and tool work, persists tool facts before side effects, waits for tool settlements, and handles interruption (`SOURCE_CODE_EVIDENCE`). It is turn execution, not Apex Attempt lifecycle.

**Q. Result collection.** Messages, parts, typed tool success/failure, and public events are stored/projected through `packages/core/src/session/sql.ts`, `event.ts`, and `session/projector.ts` (`SOURCE_CODE_EVIDENCE`).

**R. Verification / review.** Tool settlement and event projection are present. Independent verification or acceptance of task results is `NOT_PROVEN`.

**S. Retry / failure.** Provider error handling and context-overflow compaction exist; the runner's own checklist marks durable retry/final status/recovery as unfinished (`SOURCE_CODE_EVIDENCE`).

**T. Recovery / resume / reconciliation.** Session resume and snapshot/revert are available. Controller-loss reconciliation and durable runtime ownership are explicitly not complete (`SOURCE_CODE_EVIDENCE`, `NOT_PROVEN`).

**U. Persistence.** SQLite tables include session, message, part, input admission/promotion, context epoch, and event data. This is stronger than an in-memory transcript but not an Apex execution ledger (`SOURCE_CODE_EVIDENCE`).

**V. Human gates.** Permission questions pause tool execution awaiting a reply; exact authority revision and barrier semantics are absent (`SOURCE_CODE_EVIDENCE`, `NOT_PROVEN`).

**W. Events / observability.** `packages/core/src/event.ts` decodes and persists typed durable events; it contains a TODO about binding projectors to exact type/version before incompatible historical payloads (`SOURCE_CODE_EVIDENCE`).

**X. Artifacts / provenance.** Snapshots/revert and tool/event records provide partial provenance. Immutable per-attempt manifest/artifact provenance is `NOT_PROVEN`.

**Y. Extensibility.** Tool registry, plugins, providers, and server handlers are strong extension seams (`SOURCE_CODE_EVIDENCE`).

**Z. Product UX.** Session UI/server surfaces center transcript, tools, and project context. This is a useful substrate comparison, not Apex identity.

**AA. License / reuse.** MIT at the inspected root. License does not grant permission to copy without preserving notices or resolving dependency licenses.

**AB. Apex-relevant patterns.** `ADOPT PATTERN` for durable typed event/version discipline and per-key local concurrency as concepts; `ADAPT PATTERN` for provider/tool boundaries and snapshot/revert; `DEFER` clustered ownership until Runtime Adapter/Execution contracts are designed.

**AC. Apex risks / anti-patterns.** Session-as-work-unit; local ownership mistaken for durable ownership; provider/runtime completion mistaken for semantic task success; snapshot/revert mistaken for full recovery.

**AD. NOT_PROVEN / open questions.** Distributed ownership, immutable attempt birth contract, authority binding to runtime lane, independent verification, and semantic completion are not proven.

**AE. Recommended Apex action.** `ADAPT PATTERN`; retain OpenCode as the first substrate candidate only, behind the future Runtime Adapter Contract. **Likely next inspection path:** API/session entry → `SessionRunner.runTurn` → tool registry/permissions → process/provider → SQLite event/session projection.

### 7.2 OpenHands — `f7fb0c4b...`

**A. Identity.** OpenHands frontend/control-center repository, MIT, `main`, `f7fb0c4b21f5ed726edbba8a6309634ef434b004` (`OBSERVED_REPOSITORY_STATE`).

**B. Product / system shape.** Root `AGENTS.md` documents separate `software-agent-sdk`/Agent Server, `automation`, `extensions`, and Agent Canvas responsibilities. This is direct documentation evidence of a split control plane; the backend source is not in this checkout.

**C. Entry points.** `src/routes/conversation.tsx` is the conversation route; `src/routes/automation-detail.tsx` is the automation/control route (`SOURCE_CODE_EVIDENCE`).

**D. Context model.** `src/contexts/conversation-websocket-context.tsx` loads main conversation history via REST, then WebSocket deltas; planning conversations use a separate WebSocket path. This shows explicit replay/context hydration (`SOURCE_CODE_EVIDENCE`).

**E. Planning model.** Conversation and planning channels are distinct in the client; durable planner semantics are backend-owned and `NOT_PROVEN` locally.

**F. Task / work unit.** Conversations, child conversations, automations, and runs are the visible units. `src/services/child-conversation-launch.ts` handles child launch/race concerns; a Core Task/Attempt model is not locally visible.

**G. Delegation model.** Child-conversation launch is directly observed; automation scheduling/dispatch is described by `AGENTS.md` as external `automation` responsibility.

**H. Multi-agent model.** PARTIAL: child/planning conversation surfaces exist; true multi-agent execution is `NOT_PROVEN` in this checkout.

**I. Parallelism.** Client state and WebSocket channels support concurrent conversation views; backend worker parallelism is `NOT_PROVEN`.

**J. Scheduling / dependency.** Automation detail exposes scheduling/run-now/health and activity data, but dependency-aware execution is `NOT_PROVEN` locally.

**K. Agent / runtime selection.** `src/api/backend-registry` and conversation route code distinguish backend IDs/configuration; selection semantics are product/backend-specific.

**L. Model / provider.** Backend/provider configuration is exposed through API types and route state; provider execution is external to this checkout.

**M. Workspace / isolation.** `conversation.tsx` resumes a cloud sandbox when it observes `sandbox_status === "PAUSED"`; sandbox ownership/backend details are outside this repository.

**N. Permission / authority.** Automation detail has owner/manage permissions; cloud sandbox and backend permissions are documented. Binding an authority revision to an execution identity is `NOT_PROVEN`.

**O. Runtime / session.** Conversation IDs, backend IDs, organization IDs, and WebSocket streams are explicit client identities. They are not Apex RuntimeSessionBinding proof.

**P. Execution lifecycle.** Client flow is load → connect → stream → update/reset/error navigation. Runtime lifecycle is backend-owned.

**Q. Result collection.** Event store and conversation state stores accumulate streaming messages and task data; result aggregation at the execution domain is `NOT_PROVEN`.

**R. Verification / review.** Task error states and automation activity/run displays are present. Independent verification/acceptance is `NOT_PROVEN`.

**S. Retry / failure.** Client handles errors and cloud-sandbox resume; child launch tests explicitly cover REST/WebSocket race/duplicate-start concerns. This is failure containment, not a complete recovery model.

**T. Recovery / resume / reconciliation.** REST-first plus WebSocket replay and cloud sandbox resume are useful recovery patterns. Process-loss reconciliation and semantic retry are `NOT_PROVEN`.

**U. Persistence.** Client/API history and automation run history are exposed; source of backend durability is external.

**V. Human gates.** Automation owner/manage permissions and conversation interaction provide human control surfaces; explicit Apex-style barriers are `NOT_PROVEN`.

**W. Events / observability.** WebSocket streams and event stores provide incremental observability, with separate planning/main channels.

**X. Artifacts / provenance.** Conversation and automation activity can be displayed/exported; immutable attempt provenance is `NOT_PROVEN`.

**Y. Extensibility.** `AGENTS.md` documents extensions/automations/integrations; the frontend has backend registry/API seams.

**Z. Product UX.** Strong control-center/Agent Canvas, conversation, automation, and sandbox-resume UX. This is high product-shell learning value.

**AA. License / reuse.** MIT at root. The repository documents external components and their own boundaries; those must be reviewed separately.

**AB. Apex-relevant patterns.** `ADAPT PATTERN` REST-first history plus WebSocket delta replay; `ADAPT PATTERN` control-center/automation separation; `DEFER` backend automation assumptions until source-level access exists.

**AC. Apex risks / anti-patterns.** Treating UI task status as runtime semantic truth; conflating conversation continuity with durable execution recovery; assuming external SDK behavior from frontend state.

**AD. NOT_PROVEN / open questions.** Agent-server task ledger, attempt identity, backend scheduler/dependencies, permission binding, acceptance, and crash reconciliation.

**AE. Recommended Apex action.** `ADAPT PATTERN`; deep harvest remains justified for the architecture/control-center boundary, but later work must inspect the external SDK/Agent Server and automation repositories at pinned revisions. **Likely next path:** conversation route → backend API/WS → SDK conversation runner → automation dispatch → workspace/runtime.

### 7.3 Vibe Kanban — `4deb7eca...`

**A. Identity.** Rust task/workspace/product shell, Apache-2.0, `main`, `4deb7eca8f381f7cbc1f9d15515a9ab8f8009053` (`OBSERVED_REPOSITORY_STATE`).

**B. Product / system shape.** `crates/db`, `executors`, `local-deployment`, `workspace-manager`, `git`, `review`, and UI-facing API types make the task–workspace–executor–review chain visible (`SOURCE_CODE_EVIDENCE`).

**C. Entry points.** Executor actions such as `crates/executors/src/actions/coding_agent_initial.rs` and `review.rs`; local control is concentrated in `LocalContainerService` (`SOURCE_CODE_EVIDENCE`).

**D. Context model.** `Workspace` loads repos/session context; review can discover Claude projects/sessions by branch in `crates/review/src/session_selector.rs`.

**E. Planning model.** Task status includes Todo/InProgress/InReview/Done/Cancelled; planning beyond this workflow is `NOT_PROVEN`.

**F. Task / work unit.** `crates/db/src/models/task.rs` has a durable `Task` with project, title, status, parent workspace, timestamps. This is a genuine domain task, but the status set is product-specific.

**G. Delegation model.** Coding agent executor actions are selected through executor profiles; no general supervisor graph was found.

**H. Multi-agent model.** Multiple executor profiles and sessions are possible; a durable dependency-aware multi-agent controller is `NOT_PROVEN`.

**I. Parallelism.** `LocalContainerService` tracks child processes, cancellation tokens, message stores, DB stream handles, and exit monitors; separate workspace/process execution can overlap (`SOURCE_CODE_EVIDENCE`).

**J. Scheduling / dependency.** Task/workspace relations exist; no full DAG scheduler or join semantics were established.

**K. Agent / runtime selection.** `CodingAgentInitialRequest` resolves an `ExecutorConfig`, profile, overrides, approvals, and working directory; `container.rs` validates executor profile continuity for queued follow-ups (`SOURCE_CODE_EVIDENCE`).

**L. Model / provider.** Executor profile/configuration is the provider/agent selection boundary.

**M. Workspace / isolation.** `WorkspaceManager::create_workspace` creates one Git worktree per repository and rolls back partial creation. The process runs in the effective worktree/working directory (`SOURCE_CODE_EVIDENCE`).

**N. Permission / authority.** `ExecutorApprovalService` is threaded into coding/review agent spawning; `crates/utils/src/approvals.rs` models pending/approved/denied/timed-out outcomes. This is useful approval flow, not Apex authority binding proof.

**O. Runtime / session.** `ExecutionProcess` stores session ID, action, status, exit code, times, and dropped flag. This is a runtime-process record, not an immutable Apex Attempt.

**P. Execution lifecycle.** Container spawn → stream/monitor → map exit to Completed/Failed/Killed → update process/session summary → optionally consume queued follow-up (`SOURCE_CODE_EVIDENCE`, `crates/local-deployment/src/container.rs`).

**Q. Result collection.** Process logs/stream stores and session summaries persist execution output; branch/worktree state is separately observable.

**R. Verification / review.** `crates/executors/src/actions/review.rs` and review session selection create a distinct review phase; PR/branch review is not equal to process success.

**S. Retry / failure.** Killed/failed process statuses and queued follow-ups exist. The source does not establish a general retry policy or attempt-preserving recovery.

**T. Recovery / resume / reconciliation.** Worktree creation rolls back on partial failure; process exit monitoring and follow-up session resume exist. Cold restart/runtime reconciliation is `NOT_PROVEN`.

**U. Persistence.** SQLite-backed Task, Workspace, Session, ExecutionProcess, and process-repo-state records are durable.

**V. Human gates.** Tool approval service and review selection are explicit human intervention surfaces.

**W. Events / observability.** DB stream/process logs and status records provide process observability; no canonical typed event contract equivalent to Vigla was found.

**X. Artifacts / provenance.** Before/after commit state and workspace Git metadata provide strong code-change provenance; immutable per-attempt manifest is absent.

**Y. Extensibility.** Executor profiles and action traits are the primary extension seams.

**Z. Product UX.** Kanban task/workspace/review UX closely matches Apex development-control and Product Shell interests.

**AA. License / reuse.** Apache-2.0 at repository root; inspect third-party and generated assets before any code reuse.

**AB. Apex-relevant patterns.** `ADOPT PATTERN` durable Task separate from process; `ADAPT PATTERN` worktree-per-workspace, approval service, branch-aware review; `ADAPT PATTERN` process status as facts only.

**AC. Apex risks / anti-patterns.** Process status can be read as task success; follow-up session may resemble retry without a new immutable attempt; approval service lacks Apex revision/barrier semantics.

**AD. NOT_PROVEN / open questions.** Crash recovery, duplicate spawn prevention across restart, per-attempt authority, independent verification, and task/attempt mapping.

**AE. Recommended Apex action.** `ADOPT PATTERN` for the domain-task/workspace/review separation, then adapt it behind Apex Core/Runtime Adapter boundaries. **Likely next path:** Task API → workspace manager → `LocalContainerService` → executor profile/action → process logs/exit → review/PR.

### 7.4 Vigla — `bbd19ae2...`

**A. Identity.** Rust/Tauri supervisor/worker station, Apache-2.0, `main`, `bbd19ae2d5a77401502756c550b5dcd4ae59bbc9` (`OBSERVED_REPOSITORY_STATE`).

**B. Product / system shape.** `event-schema` is explicitly runtime-free and the canonical event contract; `orchestrator` supervises child vendor processes; adapters translate vendor streams; app renders the station (`SOURCE_CODE_EVIDENCE`).

**C. Entry points.** `Supervisor::dispatch` in `crates/orchestrator/src/supervisor/dispatch.rs` is the main scheduling entry; adapter supervision parses process output into events.

**D. Context model.** Worker/task identity and event streams carry the execution context; context restoration is adapter/vendor-specific (`resume.rs`, `adapter_supervision.rs`).

**E. Planning model.** Worker states include `Planning`, `Executing`, `Blocked`, `Reviewing`; planning is represented as a worker state, not a separate development-plan contract.

**F. Task / work unit.** `TaskInfo` has stable id, parent, title, `depends_on`, and creation timestamp. It is a real orchestration task identity.

**G. Delegation model.** Supervisor dispatches `DispatchRequest` to workers and releases dependent tasks on terminal coordination events.

**H. Multi-agent model.** `Supervisor` maintains running worker slots, task completion/failure sets, pending dispatches, and coordination sinks (`SOURCE_CODE_EVIDENCE`).

**I. Parallelism.** Worker slots and separate child processes support concurrent workers; coordination uses bounded chatty-event and unbounded terminal-event lanes to protect dependency/retry bookkeeping.

**J. Scheduling / dependency.** `DispatchRequest.depends_on` is evaluated under locks; unsatisfied work is queued, failed dependencies block downstream work, and completion drains pending dispatches (`dispatch.rs`). This is direct dependency-aware readiness evidence.

**K. Agent / runtime selection.** `vendor_for_script`, `WorkerInfo.vendor`, `cli_binary`, `cli_version`, `model`, and adapter profiles select the worker substrate. General next-best dynamic routing is `NOT_PROVEN`.

**L. Model / provider.** Vendor profiles and command rendering are explicit; adapter selection is separate from supervisor logic.

**M. Workspace / isolation.** `WorkerInfo.cwd` is documented as the worker's own Git worktree; `mission_workspace` and `mission_worker_dispatch` create/operate on worktrees. This is strong workspace isolation evidence.

**N. Permission / authority.** Event memory has witness kinds such as review/user acceptance and adapter/operator control paths. An Apex PermissionEnvelope/AuthorityRevision bound before execution is `NOT_PROVEN`.

**O. Runtime / session.** Worker ID is stable for a spawned process; retry creates a fresh WorkerInfo while retaining TaskInfo task id. Vendor session IDs are saved only when adapter supports resume (`resume.rs`).

**P. Execution lifecycle.** Reserve slot → persist worker/task → spawn process → parse stdout/stderr → persist/emit events → terminal completion/failure → drain dependants or schedule retry (`dispatch.rs`, `parser.rs`, `coordination.rs`).

**Q. Result collection.** Canonical typed `Completion`, `Failure`, `Artifact`, `TestResult`, `FileActivity`, and log events are persisted and forwarded to UI.

**R. Verification / review.** `WorkerState::Reviewing`, event witness memory, result/diff/replay surfaces, and mission review concepts provide a separate review/arbiter path. Independent semantic verifier guarantees remain `NOT_PROVEN`.

**S. Retry / failure.** `FailureCategory` and `retryable` classify failure; `RetryPolicy::OnFailure` bounds retries with exponential backoff. This is stronger than a generic “retry” button but remains supervisor-specific.

**T. Recovery / resume / reconciliation.** Claude resume/retry uses persisted session metadata and increments event sequence to avoid key collisions. Other vendors explicitly return `ResumeUnsupported`; controller-loss reconciliation is `NOT_PROVEN`.

**U. Persistence.** Repository/event persistence stores worker/task/events and resume metadata. Exact cross-process ownership after supervisor loss is `NOT_PROVEN`.

**V. Human gates.** Failure suggestions/escalation, review, and memory witnesses expose operator gates; explicit barrier release before running is not the Apex contract.

**W. Events / observability.** Versioned, typed, monotonic per-worker event envelope is one of the strongest observed patterns. Events are persisted before/alongside forwarding and UI replay consumes them.

**X. Artifacts / provenance.** Worker/task ids, cwd, vendor, model, timestamps, sequence, file activity, test results, and artifact references form useful provenance. It is not an immutable Apex ExecutionManifest.

**Y. Extensibility.** Adapter crates and conformance fixtures create a clear runtime adapter seam; event-schema is deliberately runtime-free.

**Z. Product UX.** Station canvas, event feed, result/diff, replay, and worker portraits provide a strong supervisor/operator projection.

**AA. License / reuse.** Apache-2.0 at root; inspect vendored/third-party notices before any reuse.

**AB. Apex-relevant patterns.** `ADOPT PATTERN` typed versioned events and dependency-aware dispatch as concepts; `ADAPT PATTERN` supervisor/worker and retry classification; `EXPERIMENT REQUIRED` for controller-loss recovery and authority binding.

**AC. Apex risks / anti-patterns.** Reusing a worker identity for continuation can obscure attempt boundaries; worker-reported completion is not semantic success; bounded in-process supervisor state is not automatically a durable active owner.

**AD. NOT_PROVEN / open questions.** Exact durable reconciliation after supervisor loss, authority activation/binding, independent verification, and immutable birth metadata.

**AE. Recommended Apex action.** `ADAPT PATTERN`; Vigla is the closest source-level comparator for future Foreman/Mission Control interests, but its names and implementation must not be imported into Apex Core. **Likely next path:** control input → `Supervisor::dispatch` → dependency queue/slot → adapter process → typed event repository → review/recovery/replay.

## 8. Targeted harvest profiles

The following profiles answer only the Owner-bounded questions. Uninspected internals are explicitly marked `UNKNOWN` or `NOT_PROVEN`.

### 8.1 OpenWork — `9a64fe108...`

**A. Identity / product shape.** [different-ai/openwork](https://github.com/different-ai/openwork), `dev`, `9a64fe1087aff7f5c552a446595d1325e1d1a91b`; desktop/web/server shell around shared skills, MCP, OpenCode, workspaces, and optional Den control plane (`README.md`, `apps/server/README.md`).

**B–E. Entry, context, planning, task.** `apps/server` exposes workspace/config/events/plugins/skills/MCP/commands/audit/artifacts; filesystem-backed workspace state is distinct from the OpenCode proxy. A durable Apex Task/Attempt model is `NOT_PROVEN` (`apps/server/README.md`, `apps/desktop/electron/workspace-store.mjs`).

**F–J. Delegation, parallelism, scheduling.** Capability execution and UI-control mailbox are present; polling claims are per-request and not broadcast. Durable dependency orchestration is `NOT_PROVEN`.

**K–O. Selection, workspace, authority, runtime.** Workspace state is written atomically; server supports client/host/owner/collaborator/viewer tokens and host approvals; `OPENWORK_OPENCODE_*` config and OpenCode proxy define a replaceable integration seam. This is shell/control-plane evidence, not Apex authority binding (`apps/server/README.md`, `apps/desktop/electron/workspace-store.mjs`).

**P–T. Lifecycle/result/recovery.** Server events/audit/artifacts and desktop crash/recovery helpers exist. Renderer crash recovery and title retry are bounded recovery features, not execution reconciliation (`apps/desktop/electron/process-resilience.mjs`, `recovery.mjs`, `apps/server/README.md`).

**U–Z. Persistence/UX/extensibility.** Electron workspace state and server filesystem state are persisted; MCP, plugins, skills, and package split are strong shell seams. The visual desktop is not canonical Apex state.

**AA. License.** MIT outside `ee/`; `ee/` is OpenWork EE License/source-available with subscription conditions documented in root `LICENSE`/`ee/LICENSE`.

**AB–AE. Apex mapping/action.** `ADAPT PATTERN` shell/server/package split, MCP/capability surface, explicit approval/token scopes, and OpenCode integration. `DEFER` any upstream fork implementation until reconciliation with prior `OPENWORK-FEASIBILITY.md` and `OPENWORK-RUNTIME-PROOF.md`. OpenWork remains replaceable and not Apex identity. Unproven: durable admission/orchestration, authority binding, task semantic success. **Likely path:** desktop/app → server workspace API → OpenCode proxy/MCP → runtime session/audit/artifact.

### 8.2 Freebuff — `131058165...`

**A. Identity / product shape.** Freebuff is a public/free coding agent built from the Codebuff framework (`AGENTS.md`), Apache-2.0, `main`, `1310581654df57a5c6cff372dd38d34e7c44c0c5`.

**B–F. Entry/context/planning/task.** CLI/SDK/runtime are separate from public agent definitions; `AgentDefinition` supports prompt/params schemas, model/provider options, tools, spawnable agents, output mode, context compaction, and windowed file reads (`agents/types/agent-definition.ts`). No durable domain Task/Attempt was observed.

**G–J. Delegation/multi-agent/parallelism/scheduling.** `packages/agent-runtime/src/tools/handlers/tool/spawn-agents.ts` validates allowed child agents, creates child state, executes all entries with `Promise.allSettled`, streams child chunks, and aggregates reports/cost. This is real parallel subagent execution; no durable DAG/dependency scheduler.

**K–O. Selection/workspace/authority/runtime.** Agent definitions choose model/provider/fallback options and tool/spawn permissions; context is passed through `SubagentContextParams`; terminal execution is brokered by CLI/SDK paths (`AGENTS.md`, `docs/agents-and-tools.md`, `spawn-agent-utils.ts`). Per-attempt authority/workspace isolation is `NOT_PROVEN`.

**P–T. Lifecycle/results/recovery.** `sdk/src/run.ts` supports periodic `onStateSnapshot` snapshots, cancellation state, and provider/API retries; `set_output` and aggregated child reports are outputs. Snapshots preserve progress but are not immutable manifests or independent verification.

**U–Z. Persistence/UX/extensibility.** Framework/product boundary is unusually explicit: `agents/`, `packages/agent-runtime`, `sdk`, `cli`, and `common`; specialized agents include file/context tools and thinker/basher patterns. Desktop/Cloud separation is not proven in this public checkout.

**AA. License.** Apache-2.0 at root; framework dependencies and provider terms remain separate concerns.

**AB–AE. Apex mapping/action.** `ADAPT PATTERN` constrained spawnable-agent graph, specialized context discovery, structured outputs, and parallel aggregation. `DEFER` framework/product assumptions and `REJECT` treating agent self-report or SDK output as Apex completion/verification. Retry/fallback/reassignment and isolated parallel workspaces remain `NOT_PROVEN`. **Likely path:** CLI/SDK run → agent definition → spawn handler → child runtime/tools → aggregated output/state snapshot.

### 8.3 Goose — `5e909259...`

**A. Identity / product shape.** Rust agent/runtime with provider and MCP extension crates, Apache-2.0, `main`, `5e90925962f05acf8e255032de44d16c4a7768a2`.

**B–F. Entry/context/planning/task.** `crates/goose/src/session/session_manager.rs` persists `Session` with working directory, conversation, provider/model, usage, recipe, project, parent session, and type. `crates/goose-agent/src/machine.rs` runs a sequence of operations/inference over persisted conversations. No domain Task/Attempt.

**G–J. Delegation/multi-agent/parallelism/scheduling.** Operations/extensions and session types include `SubAgent`/`Scheduled`; general dependency scheduling is `NOT_PROVEN`.

**K–O. Selection/workspace/authority/runtime.** Provider abstraction and declarative provider definitions are in `crates/goose-providers`/`goose-provider-types`; `session_context.rs` carries provider-facing session id headers; `permission_store.rs` persists tool permission decisions keyed by tool/context hash with expiry. This is a useful adapter/provider boundary, not Apex authority.

**P–T. Lifecycle/results/recovery.** `StateMachine::run` repeatedly loads a session, applies one operation/inference, persists effects, and reloads; provider retry uses exponential backoff/jitter in `goose-provider-types/src/retry.rs`; CLI supports resume/fork. Process-loss/reconciliation is `NOT_PROVEN`.

**U–Z. Persistence/UX/extensibility.** Session/message SQLite storage, MCP extensions, provider adapters, CLI/gateway/SDK surfaces are strong; conversation remains the primary durable unit; no independent verification contract.

**AA. License.** Apache-2.0 root.

**AB–AE. Apex mapping/action.** `ADAPT PATTERN` provider abstraction, operation/state-machine pipeline, persisted effect notes, and permission-context hashing. `TARGETED HARVEST` only; do not equate session resume with Attempt recovery or provider retry with Apex retry. **Likely path:** CLI session builder → SessionManager → StateMachine → provider/MCP operation → persisted conversation/effects.

### 8.4 LangGraph — `81bf17b23...`

**A. Identity / product shape.** MIT graph/orchestration libraries, `main`, `81bf17b23123e4ef8b9d5f49fa09a0122fc2edd1`.

**B–F. Entry/context/planning/task.** `StateGraph` builds graph nodes/edges; Pregel tasks carry node work and writes; `types.py` documents task/interrupt/checkpoint stream shapes. The graph task is not Apex Core Task.

**G–J. Delegation/multi-agent/parallelism/scheduling.** `Send` enables push-style task fan-out; graph edges and named barrier/join channels in `graph/state.py`/Pregel provide dependency/join semantics. This is the strongest selected reference for durable graph control, but not an Apex product workflow.

**K–O. Selection/workspace/authority/runtime.** Node/runtime configuration and user-provided tools are flexible; no Apex agent/model/runtime lane or authority envelope.

**P–T. Lifecycle/results/recovery.** `RetryPolicy` supports max attempts, exponential backoff, cap, jitter, and exception predicates (`types.py`). `interrupt()` raises a resumable graph interrupt; `Command(resume=...)` resumes from node start and requires a checkpointer. `BaseCheckpointSaver` uses `thread_id`, checkpoint id/namespace, parent links, versions, writes, and metadata; `AsyncSqliteSaver` is an implementation. Exact process-loss reconciliation depends on deployment/checkpointer and is not universal proof.

**U–Z. Persistence/UX/extensibility.** Checkpoint backends, streams (`values`, `updates`, `checkpoints`, `tasks`, `debug`), graph composition, and SDK surfaces are strong reusable control primitives. Graph state is not an authority ledger or semantic acceptance record.

**AA. License.** MIT root.

**AB–AE. Apex mapping/action.** `ADAPT PATTERN` checkpoint identity/ancestry, resumable human interrupts, explicit retry policy, fan-out/join, and task debug streams. `DEFER` full framework adoption; `EXPERIMENT REQUIRED` for process-loss/reconciliation and side-effect idempotency. **Likely path:** StateGraph compile → Pregel loop → node/task scheduling → checkpointer → interrupt/Command/retry → stream/result.

### 8.5 agtx — `d307c4c18...`

**A. Identity / product shape.** Rust kanban/TUI/web/MCP board for agent task coordination, Apache-2.0, `main`, `d307c4c182dff19a65370a50403185cb826f7f49`.

**B–F. Entry/context/planning/task.** `src/db/models.rs` defines SQLite `Task` with status, agent, session, worktree, branch, PR, cycle, referenced tasks, escalation note, and base branch. `TaskStatus` is Backlog/Planning/Running/Review/Done.

**G–J. Delegation/multi-agent/parallelism/scheduling.** `src/core/actions.rs` centralizes allowed actions by caller and task state; dependency satisfaction gates transitions. Tmux sessions and agent/worktree records provide parallel coordination; a full fleet scheduler is `NOT_PROVEN`.

**K–O. Selection/workspace/authority/runtime.** `src/agent` stores agent operations/spec/trust; `src/tmux` delivers input with bounded confirmation; `src/git/worktree.rs` owns worktrees; action validation separates human from orchestrator permissions. This is workflow governance, not Apex authority binding.

**P–T. Lifecycle/results/recovery.** SQLite transition requests are queued for the TUI to apply with side effects; notifications are typed; tmux delivery has bounded retries/confirmation; no demonstrated process-loss reconciliation or durable requeue.

**U–Z. Persistence/UX/extensibility.** Central/global SQLite, web/MCP/TUI projections, dependency graph, branch/PR fields, and plugin skills are useful; review semantics remain product-specific.

**AA. License.** Apache-2.0 root.

**AB–AE. Apex mapping/action.** `ADAPT PATTERN` command-mediated state transitions, explicit caller permissions, worktree/session/branch linkage, and canonical DB records. `DEFER` board-as-registry until Apex Work Registry design is materialized. **Likely path:** MCP/web request → transition request → DB/task validation → TUI side effect → tmux agent/worktree → review/PR fields.

### 8.6 E2B — `473d8bf3...`

**A. Identity / product shape.** Apache-2.0 sandbox/control-plane SDK repository, `main`, `473d8bf3e62b68ee731cf18afb2e8258f9ca7a7c`.

**B–F. Entry/context/planning/task.** `packages/js-sdk/src/sandbox/index.ts` exposes `Sandbox`, `files`, `commands`, `pty`, `git`; `SandboxApi` defines sandbox lifecycle and states. It is a runtime/sandbox primitive, not a task planner.

**G–J. Delegation/multi-agent/parallelism/scheduling.** Independent sandbox/process concurrency is possible; no orchestration DAG.

**K–O. Selection/workspace/authority/runtime.** Sandbox identity is `sandboxId`; envd/control-plane RPC and access headers are explicit. Commands have cwd/user/env/stdin/timeout; filesystem and network modules are separate. Network allow/deny, egress proxy, IAM token placeholders, secure mode, and sandbox access controls are strong isolation primitives (`packages/js-sdk/src/sandbox/sandboxApi.ts`).

**P–T. Lifecycle/results/recovery.** Create/connect/kill/pause/snapshot/fork are implemented API concepts; tests cover reconnect, sandbox kill during execution, client timeout interruption, snapshots, and subsequent execution. These prove sandbox lifecycle behavior in tests, not Apex semantic recovery.

**U–Z. Persistence/UX/extensibility.** Snapshots can persist sandbox state; process/file/PTY/MCP interfaces are composable. No task/artifact acceptance ledger.

**AA. License.** Apache-2.0 root.

**AB–AE. Apex mapping/action.** `ADAPT PATTERN` sandbox identity/control-plane API, reconnect/pause/snapshot, network/iam boundary, and explicit process API. `TARGETED HARVEST` remains bounded to Runtime Adapter beneath Apex; do not import E2B semantics as Apex PermissionEnvelope. **Likely path:** SDK `Sandbox.create/connect` → envd RPC → commands/files/PTY → sandbox lifecycle.

### 8.7 Daytona — `ec4c21b2...`

**A. Identity / product shape.** README-only tree at the inspected `main` commit `ec4c21b2d597091ac09ecc278f3bcc172575a987`; README states the repository is no longer maintained and core development moved private as of June 2026 (`OBSERVED_REPOSITORY_STATE`, `DOCUMENTATION_EVIDENCE`).

**B–J. Execution/control.** README documents sandboxes, full composable computers, interface/control/compute planes, snapshots, process/code/file/network tools, parallelization, and persistence. Because no source tree was present, ownership and exact lifecycle are `NOT_PROVEN`.

**K–O. Runtime/authority.** Documented SDK/API/CLI and sandbox/control-plane boundary are relevant; implementation, isolation enforcement, reconnect, and authority details are `NOT_PROVEN` at this ref.

**P–T. Recovery.** README documents persistent snapshots and stateful environments; no source-level recovery path was available.

**U–Z. UX/extensibility.** Dashboard, web terminal, VNC, SDKs, API, CLI, MCP, OTEL, and audit are documented, not source-verified.

**AA. License.** No license file in the inspected tree; README links the historical `v0.190.0` license. Treat code reuse as blocked pending legal/source review.

**AB–AE. Apex mapping/action.** `EXPERIMENT REQUIRED`/`DEFER` for targeted comparison with E2B only. **Likely path from docs:** SDK/API → control plane → sandbox → process/files/network; no source claims should be promoted.

### 8.8 Nimbalyst — `34b14f33...`

**A. Identity / product shape.** MIT desktop/editor/agent workspace, `main`, `34b14f33e48fd639d32c0f5eb7d77561bdccd2a4`.

**B–F. Entry/context/planning/task.** `docs/SESSION_HIERARCHY.md` defines standalone/workstream/worktree/blitz session shapes and explicitly prevents invalid nesting; task semantics are session-oriented, not Apex domain Task.

**G–J. Delegation/parallelism.** Worktrees can contain multiple sessions; multi-agent scheduling/dependency semantics are `NOT_PROVEN`.

**K–O. Workspace/permission/runtime.** `docs/WORKTREES.md` and `GitWorktreeService`/`WorktreeStore` describe worktree branches/base branches/status and session association. `docs/AGENT_PERMISSIONS.md` defines project trust, read-only defaults, path/URL/bash patterns, approval scopes, and provider modes. This is useful Product Shell permission UX, not Apex authority binding.

**P–T. Lifecycle/recovery.** `docs/STATE_PERSISTENCE.md` requires defaults plus merge-on-load for persisted state; worktree reliability and file-change tracking docs address recovery/consistency. Agent task completion/reconciliation is `NOT_PROVEN`.

**U–Z. Persistence/UX/extensibility.** SQLite/electron persistence, visual session hierarchy, file watching, EditorHost contract, custom editors, and extension SDK are strong persistent-workspace/projection patterns.

**AA. License.** MIT root.

**AB–AE. Apex mapping/action.** `ADAPT PATTERN` worktree/session association, persisted-state migrations, project-scoped permissions, EditorHost/extension contract, and visible intervention UX. `TARGETED HARVEST` only; visual state must remain projection. **Likely path:** Electron session/worktree service → provider runtime → editor/file watcher → persisted session/diff.

### 8.9 Agent Mission Control — `39e2e3bd...`

**A. Identity / product shape.** Small telemetry/simulation/web visualization repository, `main`, `39e2e3bd7ffa88e1296360e8833b099435f4c6a8`; no license file observed.

**B–F. Entry/context/planning/task.** `packages/shared/src/events/schema.ts` defines session/agent/task/tool/file/cost events; task is an event payload rather than an execution domain aggregate.

**G–J. Delegation/parallelism.** Agent messages and telemetry show relationships; no execution scheduler was found.

**K–O. Runtime/authority.** `telemetry-bridge` ingests events into SQLite; `simulation-engine` reduces them into world state. No runtime or authority owner is observed.

**P–T. Lifecycle/results/recovery.** `ReplayController` and `EventCursor` rebuild world state from event history, support play/pause/seek, and are useful visual replay patterns. They do not recover a failed worker.

**U–Z. Persistence/UX/extensibility.** Typed Zod events, `INSERT OR IGNORE` event storage, world reducers, agent/file nodes, timeline, analytics, and web streaming provide a compact projection architecture.

**AA. License.** No license file observed at pinned ref; no code-reuse recommendation.

**AB–AE. Apex mapping/action.** `ADAPT PATTERN` event-sourced projection/replay and explicit telemetry-to-world-state reduction. `DEFER` spatial/game-like UX implementation until canonical Apex state is available; `REJECT` any visual state as source of truth. **Likely path:** event producer → telemetry bridge/SQLite → web stream → simulation reducer → visual projection.

## 9. Cross-system answers to Owner questions

| Question | Evidence-based answer |
|---|---|
| Real domain-level Task? | Yes: Vibe Kanban, Vigla, agtx. LangGraph has graph tasks; others are mainly sessions/conversations/sandboxes/events. |
| Session/prompt/job treated as task? | OpenCode, Goose, Freebuff, OpenHands client surfaces, and often OpenWork primarily use session/conversation/run shapes. |
| Task distinct from Attempt/retry? | Vigla partially separates TaskInfo and WorkerInfo; Vibe separates Task and ExecutionProcess; LangGraph has task attempts internally. No selected system proves Apex's exact immutable Attempt contract. |
| Immutable execution birth metadata? | No selected system proves an Apex ExecutionManifest. Vigla's persisted WorkerInfo/event identity is the closest partial pattern. |
| Durable state? | OpenCode, Vibe, Vigla, Goose, LangGraph with checkpointer, agtx, E2B sandbox lifecycle, Nimbalyst, and Agent Mission Control have durable or persisted slices. Freebuff/OpenHands are partial at the inspected boundary. |
| Recovery after process restart? | LangGraph checkpoint resume and E2B sandbox reconnect are concrete bounded patterns; Vigla vendor resume is selective. Full controller-loss reconciliation is generally `NOT_PROVEN`. |
| Runtime-state reconciliation after controller loss? | `NOT_PROVEN` across the selected systems. |
| True parallel execution? | Vigla, Vibe, Freebuff, OpenCode across distinct session keys, and LangGraph graph tasks show direct evidence. |
| Dependency-aware readiness? | Vigla direct; LangGraph graph/barrier semantics; agtx partial; Vibe only partial task/workspace relation. |
| Resource/workspace conflict prevention? | Vibe, Vigla, Nimbalyst, and agtx use worktrees/workspace paths; Apex-grade ResourceClaim/Lease semantics are not proven. |
| Next-best agent fallback? | Provider fallback exists in Freebuff/Goose/provider layers; dynamic semantic reassignment is `NOT_PROVEN`. |
| Dynamic reassignment? | No strong source proof in the selected set. |
| Runtime completion distinct from semantic success? | Vibe review/process split and Vigla Completion/Review are partial; no system proves Apex acceptance semantics. |
| Independent verification? | Review surfaces are common; independent verifier authority is `NOT_PROVEN` in all selected systems. |
| Explicit human gates? | OpenCode permission wait, Vibe approvals, OpenWork approvals, Goose permissions, LangGraph interrupt, and Vigla review/escalation provide concrete patterns. |
| Authority bound to execution identity? | No selected system proves the required Apex AuthorityRevision → RuntimeLane/Attempt binding. |
| Material agent-authority isolation? | E2B and worktree/sandbox systems provide substrate isolation; semantic per-attempt authority is `NOT_PROVEN`. |
| Per-attempt provenance? | Vigla worker/event sequence, Vibe process/commit state, and LangGraph checkpoint ancestry are partial; immutable Apex birth provenance is absent. |
| Visual UI as projection? | Agent Mission Control directly implements event→reducer→world projection; Nimbalyst and Vigla provide related views. Projection/source separation must be preserved by Apex. |
| Reusable runtime/sandbox abstraction? | E2B is strongest; Daytona is documentation-only at this ref; OpenCode/Goose provide runtime/provider seams. |
| Product-shell boundary worth borrowing? | OpenWork, OpenHands, Vibe Kanban, Nimbalyst, and Vigla each expose complementary shell/control-center/workspace patterns. |
| Anti-patterns? | Session-as-task, transcript-as-ledger, UI-as-state, retry-as-recovery, worker self-report as acceptance, hidden orchestration, and provider lock-in recur as risks. |

## 10. Source-level ownership traces for likely top comparators

| System | Entry | Context/planner | Delegation/selection | Workspace/session/permissions | Execution/results | Review/retry/persistence |
|---|---|---|---|---|---|---|
| OpenCode | `packages/core/src/session.ts`, server handlers | `session/runner/llm.ts`, `context-epoch.ts` | agent/model/tool registry | `session/sql.ts`, `permission.ts` | provider stream + tool registry + projector | `revert.ts`, events, runner TODOs |
| OpenHands | `src/routes/conversation.tsx` | client planning/main channels; backend external | child conversation service; automation external | cloud sandbox/backend registry | REST/WS conversation events | client recovery/replay; backend NOT_PROVEN |
| Vibe Kanban | executor action requests | Task/Workspace DB | ExecutorConfig/profile | WorkspaceManager + approval service | LocalContainerService + ExecutionProcess | review session selector, GitService, queued follow-up |
| Vigla | Supervisor dispatch | TaskInfo/dependency queue | vendor/adapter profile | worker cwd/worktree + slot reservation | child process + parser + typed event repository | retry/resume/coordination/replay/revert |
| OpenWork | desktop/app/server APIs | workspace state/OpenCode proxy | MCP/plugin/capability calls | server approval/token/workspace files | OpenCode proxy and server audit/events | renderer crash/title recovery |
| Freebuff | CLI/SDK `run` | agent definitions/context params | `spawn-agents.ts` + `spawn-agent-utils.ts` | tool lists/context; host broker | agent runtime/tools + `set_output` | snapshots/provider retry; no verifier |
| Goose | CLI session builder | StateMachine over Conversation | operations/extensions/provider | SessionManager + permission store | provider inference/tool operations | retry/resume/fork/persisted messages |
| LangGraph | graph compile/invoke | StateGraph/Pregel | `Send`, edges, subgraphs | checkpointer/thread_id | node tasks/checkpoints/streams | RetryPolicy + interrupt/Command/checkpoint |
| agtx | MCP/web/TUI | board task status/deps | actions + tmux agents | Git worktree + tmux + DB | agent pane/process | transition queue/review/notifications |
| E2B | SDK `Sandbox.create/connect` | N/A | N/A | sandbox/envd/files/commands/network | process/PTY/code | pause/snapshot/reconnect/kill |
| Daytona | documented SDK/API | NOT_PROVEN | NOT_PROVEN | documented sandbox/control plane | NOT_PROVEN | documented snapshots; no source |
| Nimbalyst | Electron session/worktree UI | session hierarchy | provider/session service | GitWorktreeService + PermissionService | provider/editor/file host | persisted state/worktree docs |
| Agent Mission Control | telemetry API/WS | event stream | no scheduler | telemetry DB/session | event ingestion/reducer | replay cursor/timeline |

## 11. Patterns and anti-patterns for Apex

### 11.1 Recommended pattern dispositions

| Pattern | Source evidence | Apex mapping | Disposition | Boundary |
|---|---|---|---|---|
| Durable typed/versioned event envelope | Vigla `crates/event-schema/src/lib.rs`; OpenCode `packages/core/src/event.ts` | Apex Events | ADOPT PATTERN | Versioned facts still do not define semantic success. |
| Dependency-aware dispatch under a serialized coordination boundary | Vigla `supervisor/dispatch.rs`, `coordination.rs` | Orchestration → Core Task/Execution | ADAPT PATTERN | Must not move Orchestration into Core. |
| Domain Task separate from process/session | Vibe `db/models/task.rs`, `execution_process.rs`; Vigla `TaskInfo`/`WorkerInfo` | Apex Core Task vs Attempt | ADAPT PATTERN | Preserve Apex Task != Attempt and immutable Manifest. |
| Worktree-per-workspace isolation | Vibe `workspace_manager.rs`; Vigla mission worker dispatch; Nimbalyst `WORKTREES.md` | Runtime/WorkspaceSnapshot/ResourceClaim | ADAPT PATTERN | Does not prove PermissionEnvelope. |
| Tool approval as explicit pending/approved/denied outcome | OpenCode `permission.ts`; Vibe `approvals.rs`; OpenWork server | Apex Authority/Barrier | ADAPT PATTERN | Bind to AuthorityRevision and exact Attempt/Lane later. |
| Checkpoint ancestry and resumable interrupt | LangGraph `checkpoint/base`, `types.py` | ExecutionEpoch/Recovery | ADAPT PATTERN | Side effects and process-loss reconciliation need experiments. |
| Sandbox lifecycle with reconnect/pause/snapshot | E2B `sandboxApi.ts`, reconnect/kill tests | Runtime Adapter / Runtime Lane | ADAPT PATTERN | E2B is a substrate, not Apex authority. |
| REST-first history then event-stream delta replay | OpenHands `conversation-websocket-context.tsx`; OpenCode event/history | Public API / Events | ADAPT PATTERN | API state remains separate from Core semantic state. |
| Constrained child-agent definitions and structured outputs | Freebuff `AgentDefinition`, `spawn-agents.ts` | Capability Platform | ADAPT PATTERN | Agent self-report is not verification. |
| Operation/state-machine pipeline with persisted effect notes | Goose `goose-agent/src/machine.rs`, `operation.rs` | Execution/Capability | ADAPT PATTERN | Must not collapse Development Task into runtime Session. |
| Command-mediated state transitions and caller-aware permissions | agtx `src/core/actions.rs`, `src/db/models.rs` | Development System / Work Registry | ADAPT PATTERN | Do not materialize Work Registry in this task. |
| Product shell/server/MCP/package split | OpenWork README and `apps/server/README.md` | Product Shell / Capability Modules | ADAPT PATTERN | Keep shell replaceable and EE license boundary explicit. |
| Event-to-world projection with replay cursor | Agent Mission Control `telemetry-bridge`, `simulation-engine/replay` | Projection Layer | ADOPT PATTERN | Projection cannot own canonical state. |
| Provider/runtime abstraction | Goose providers; OpenCode provider/runtime; E2B SDK | Runtime Adapter API | EXPERIMENT REQUIRED | Exact Apex contract remains to be designed. |

### 11.2 Anti-patterns Apex should avoid

| Anti-pattern | Evidence signal | Apex rule |
|---|---|---|
| Session = Task | OpenCode/Goose/Freebuff primarily center sessions/conversations | Keep Core Task, Attempt, Manifest, and Development Task distinct. |
| Transcript = execution ledger | OpenCode/Goose message persistence | Transcript is evidence/artifact context, not semantic execution state. |
| Mutable/reused worker/session identity across retries | Vigla `continue_worker` reuses worker id for MVP continuation; Goose session resume | Retry creates a new Apex Attempt and new immutable Manifest. |
| UI state = canonical state | OpenHands/Nimbalyst/Agent Mission Control projections | UI is a Product Shell/Projection Layer consumer of Public/Core state. |
| Global permission config = per-attempt authority | Goose permission store; OpenWork server tokens | Permission facts must not be upgraded to Apex AuthorityRevision binding. |
| In-memory queue = durable scheduler | OpenCode local coordinator; Vigla supervisor maps | Durable active ownership and reconciliation require direct evidence. |
| Retry = recovery | provider retries, follow-up/resume paths | Classify retry, resume, rollback, reconciliation, and acceptance separately. |
| Runtime/process completion = task success | Vibe process statuses; Vigla Completion; E2B result | Core owns semantic state; verification/acceptance is separate. |
| Agent self-report = verification | Vigla Completion summary; Freebuff output; AMC payload success | Require independent evidence/verification where contract says so. |
| Hidden orchestration inside shell | OpenWork/desktop and OpenHands control surfaces | Optional Orchestration remains above Core and independently replaceable. |
| Provider/runtime lock-in | vendor/provider-specific resume and profiles | Runtime Adapter boundary remains substrate-neutral. |
| Uncontrolled shared workspace | session/worktree and sandbox variations | Require explicit WorkspaceSnapshot/ResourceClaim/Lease semantics before execution. |
| Implicit authority escalation | token/config/approval surfaces | No widening without authority and human/Owner gate. |

## 12. Adopt / adapt / defer / reject summary by system

These are pattern dispositions, not product adoption decisions.

| System | ADOPT PATTERN | ADAPT PATTERN | DEFER | REJECT / EXPERIMENT REQUIRED |
|---|---|---|---|---|
| OpenCode | typed event facts; per-key local coordination | provider/tool/permission/snapshot seams | clustered ownership until contract | session-as-task; authority proof not established |
| OpenHands | REST-first/event-stream replay as concept | control-center/automation/backend boundary | backend harvest outside current checkout | UI status as semantic truth |
| Vibe Kanban | explicit domain Task and workspace/review separation | approval, process facts, worktree lifecycle | full scheduler/recovery | process status as task success |
| Vigla | typed event schema; dependency-aware coordination | supervisor/worker, retry categories, adapter seam | product-specific station semantics | worker identity reuse as Apex Attempt; experiment controller loss |
| OpenWork | replaceable shell/capability seam as concept | server/app/MCP/OpenCode/approval split | prior feasibility repeat and EE-dependent reuse | OpenWork as Apex identity; EE code reuse pending license review |
| Freebuff | constrained agent definitions and parallel aggregation as concepts | context discovery/structured output/snapshots | framework/product integration | output/self-report as verification |
| Goose | provider/operation abstraction; persisted effect notes | permission store/session resume semantics | full framework adoption | session resume as Apex recovery |
| LangGraph | checkpoint ancestry and explicit interrupt/retry concepts | graph fan-out/join/checkpointer mapping | full framework adoption | graph result as Apex acceptance; experiment side-effect recovery |
| agtx | command validation and task/branch linkage concepts | DB-backed board projection and caller permissions | Work Registry implementation | board as sole Apex canonical state without contract |
| E2B | sandbox lifecycle/control-plane abstraction | network/files/process/IAM mapping to Runtime Adapter | provider-specific integration | sandbox = PermissionEnvelope |
| Daytona | conceptual control/compute/interface planes only | compare with E2B if source becomes available | source reuse and independent deep audit | legal/source gap; experiment required |
| Nimbalyst | explicit hierarchy constraints and state migration discipline | worktree/session/EditorHost/permission UX | broader visual workspace adoption | visual state as authority |
| Agent Mission Control | event projection/replay separation | future spatial/mission-control views | implementation until canonical state exists | UI/world state as source of truth; no-code license gap |

## 13. License and reuse notes

- OpenCode, OpenHands, LangGraph, and Nimbalyst expose MIT root licenses; preserve notices and inspect dependency licenses before any reuse.
- Vibe Kanban, Vigla, Freebuff, Goose, agtx, E2B, and Daytona's historical reference are Apache-family contexts where applicable, but each repository may contain third-party or generated assets with separate notices.
- OpenWork is materially split: MIT outside `ee/`, OpenWork EE License under `ee/`, with subscription/source-available conditions. Apex should borrow concepts without assuming code reuse is permitted.
- Daytona's inspected tree has no license file and states the public repository is no longer maintained; no code-reuse recommendation is made.
- Agent Mission Control's inspected tree has no license file; conceptual learning only.
- No legal conclusion is made beyond observed repository license text and file presence.

## 14. Apex learning map

| Learning area | Highest-value sources | Apex layer | Current action |
|---|---|---|---|
| Runtime/session/tool/provider boundary | OpenCode, Goose | Runtime Adapter, Apex Runtime, Capability Platform | ADAPT; preserve substrate neutrality |
| Domain Task/workspace/review | Vibe Kanban, Vigla, agtx | Core Task, Product Shell, Development System | ADAPT after contract reconciliation |
| Durable dependency dispatch | Vigla, LangGraph | Optional Orchestration over Core | ADAPT; not Core-owned |
| Checkpoint/resume/interrupt | LangGraph, E2B, OpenCode | ExecutionEpoch, Recovery, Runtime Adapter | EXPERIMENT REQUIRED |
| Permission/authority UX | OpenCode, OpenWork, Vibe, Goose, Nimbalyst | Apex Authority, PermissionEnvelope, Product Shell | ADAPT; no binding claim yet |
| Typed events/provenance | Vigla, OpenCode, Agent Mission Control | Apex Events, Artifacts, Projection Layer | ADOPT/ADAPT |
| Workspace isolation | E2B, Vibe, Vigla, Nimbalyst | Runtime Lane, WorkspaceSnapshot, ResourceClaim/Lease | ADAPT; exact semantics open |
| Product shell/control center | OpenWork, OpenHands, Vibe, Nimbalyst | Product Shell, Public API | ADAPT; keep replaceable |
| Future visual projection | Agent Mission Control, Vigla, Nimbalyst | Projection Layer | DEFER implementation; preserve projection rule |

## 15. Owner Reconciliation Candidates

These are not decisions made by this harvest.

1. Should Apex's future Runtime Adapter Contract require a durable adapter event envelope with version, runtime/session identity, attempt identity, and fact/claim classification?
2. What exact Core-owned reconciliation contract is required after a runtime process or controller is lost?
3. Should `ExecutionEpoch` absorb checkpoint ancestry, or should checkpoint lineage remain an adapter/recovery detail?
4. What minimum independent verification contract separates worker/provider completion from Apex Task success?
5. Which resource-conflict semantics are mandatory for `ResourceClaim`/`ResourceLease` before parallel execution?
6. What exact authority evidence is sufficient to prove `AuthorityRevision` activation and binding to an Attempt/RuntimeLane?
7. Should a future Product Shell expose a projection protocol that is intentionally independent of any visual/spatial implementation?
8. Does OpenHands backend/automation source add enough value to justify a separately pinned follow-up checkout, given that the current frontend repository documents the split but does not include those internals?
9. Does Daytona's current private successor justify any future source-level comparison, or should E2B remain the only immediate sandbox track?

## 16. Proposed runtime experiments

No experiments were run in this delta. These are candidate designs for later Owner authorization:

1. Kill/restart an adapter/controller during an active Attempt and verify whether Core can discover, classify, and reconcile the runtime without duplicate side effects.
2. Exercise two concurrent Attempts against one workspace and test ResourceClaim/Lease conflict behavior.
3. Change authority during a paused execution interval and verify immutable prior AuthorityRevision history plus new ExecutionEpoch semantics.
4. Deny/approve a tool after a runtime reconnect and verify no stale approval crosses RuntimeLane or Attempt identity.
5. Compare OpenCode, Goose, and E2B adapters under the same minimal Core contract for session identity, process facts, cancellation, reconnect, and artifact collection.
6. Run a LangGraph-style fan-out/join with one child retrying and one child failing, then test whether the resulting semantic state can map cleanly to Apex Task/Attempt/Verification without treating graph completion as success.
7. Validate visual projections from an append-only event feed while deliberately withholding or corrupting a projection; the projection must never become the state owner.

## 17. Final recommendations and stop condition

### Highest-value patterns

1. Vigla's runtime-free, versioned typed event contract.
2. Vigla's dependency-aware dispatch with separate terminal coordination lane.
3. Vibe Kanban's durable Task → Workspace → ExecutionProcess → Review/PR separation.
4. LangGraph's checkpoint ancestry, resumable interrupt, retry policy, and fan-out/join semantics.
5. E2B's explicit sandbox identity, process/files/PTY/network APIs, and reconnect/snapshot lifecycle.
6. OpenCode's durable session/event persistence plus explicit TODO boundary around cluster ownership and durable terminal state.
7. OpenWork's shell/server/MCP/capability split and explicit approval/token surfaces.
8. Freebuff's constrained spawnable-agent definitions, context-specialist composition, parallel `Promise.allSettled`, and structured child outputs.
9. Goose's operation/state-machine pipeline and provider abstraction with persisted effect notes.
10. Agent Mission Control's event → reducer → world projection and replay cursor.

### Important conclusions

- No selected system establishes Apex's full authority materialization and binding invariant; keep it `NOT_PROVEN`.
- No selected system provides a reason to collapse Development Task, Core Task, Attempt, ExecutionManifest, Runtime Session, or Completion Report.
- Durable state is usually narrower than the product's apparent control surface. A transcript, task row, worker row, checkpoint, sandbox, or UI projection should not be promoted to an Apex semantic ledger without explicit evidence.
- Recovery is layered: provider retry, process restart, session resume, checkpoint replay, workspace rollback, and controller reconciliation are different behaviors.
- The most complementary future research tracks are OpenCode (runtime), OpenHands (control center), Vibe Kanban (work/review shell), Vigla (supervisor/events/recovery), LangGraph (durable orchestration primitives), and E2B (sandbox boundary).

### Status

`AC_COMP_HARVEST_COMPLETE` is appropriate only for this source/documentation harvest. This report does not authorize architecture reconciliation, Runtime Adapter Contract changes, implementation, code reuse, experiments, OpenWork fork work, Orchestration, DPT, Mission Control, or Spatial UI.
