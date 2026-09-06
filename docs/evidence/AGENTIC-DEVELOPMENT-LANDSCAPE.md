# Agentic Development / Creation Systems Competitive Landscape

Status: **PROPOSED**. This is a broad, shallow discovery report for Owner
shortlist selection. It is not a product decision, architecture change,
implementation plan, or permanent technology selection.

Research snapshot: 2026-09-07. Repository metadata and default-branch SHAs
were collected from official GitHub repository pages/API responses where
available. Documentation claims are labeled `DOCUMENTATION_EVIDENCE`;
repository metadata is `OBSERVED_REPOSITORY_STATE`; conclusions about Apex
fit are `INFERENCE`. Marketing or README claims are not treated as runtime
proof.

## 1. Purpose and scope

Apex Code is an independent, modular agentic development product moving
toward an Agentic Creation Ecosystem. This landscape identifies systems that
may teach Apex about execution, context, coordination, isolation, verification,
recovery, product shells, and visual supervision.

The report deliberately favors breadth over depth. A classification is a
recommendation for a later harvest, not an Owner-approved shortlist. No source
code is copied, vendored, or adopted by this report.

Existing Apex boundaries remain authoritative:

- Apex Core must work without DPT or Orchestration.
- DPT is optional; Orchestration is optional and independent from DPT.
- OpenWork-derived shell technology is replaceable, not Apex identity.
- OpenCode is the first runtime substrate candidate, not a permanent lock-in.
- Authority, execution, verification, recovery, and evidence remain Apex
  concerns.
- The complete authority materialization/activation/binding guarantee remains
  `NOT_PROVEN`.

## 2. Method and evidence vocabulary

The research method was: discover candidates across multiple categories;
prefer official repositories, documentation, release notes, and websites;
record exact default branches and observed revisions when available; inspect
license metadata; and characterize only the shallow path needed to recommend a
next harvest. Exact implementation ownership and runtime guarantees are left
for a later source-level audit.

Evidence labels used here are the established Apex vocabulary:

- `SOURCE_CODE_EVIDENCE`: a claim supported by inspected source code. This
  landscape did not perform a full source audit.
- `DOCUMENTATION_EVIDENCE`: an official README, documentation page, or product
  site states the behavior or product shape.
- `OBSERVED_REPOSITORY_STATE`: directly observed branch, SHA, license
  metadata, activity, archive state, or repository structure.
- `OBSERVED_RUNTIME_EVIDENCE`: direct runtime behavior. No new Apex runtime
  experiments were performed in this task.
- `INFERENCE`: a reasoned Apex relevance, novelty, or disposition judgment.
- `UNKNOWN`: insufficient evidence for a claim.
- `NOT_PROVEN`: a stronger guarantee was not established by the available
  evidence.

Feature cells use `YES`, `PARTIAL`, `NO`, `NOT_PROVEN`, or `N/A`. `YES` means
the primary source documents or visibly exposes the capability; it does not
mean the capability is correct, durable, safe, or equivalent to an Apex
contract.

## 3. Candidate universe

The following 30 candidates cover coding agents, runtimes, orchestration,
workforce systems, context/planning, sandboxes, product shells, and
visual/mission-control systems. Dates and SHAs are a point-in-time snapshot,
not a promise of continued activity.

| Candidate | Main category / role | Official primary source | Default branch / observed SHA | License / status | Activity signal | Novelty | Recommendation |
|---|---|---|---|---|---|---|---|
| Freebuff | coding agent, product shell, hosted/local surfaces | [CodebuffAI/freebuff](https://github.com/CodebuffAI/freebuff) | `main` / `1310581654df57a5c6cff372dd38d34e7c44c0c5` | Apache-2.0 / active | pushed 2026-09-06 | MEDIUM | LANDSCAPE ONLY |
| OpenCode | coding agent, runtime substrate | [anomalyco/opencode](https://github.com/anomalyco/opencode) | `dev` / `ea2d59d7ca8028951a16d4ebc558104258440bf9 | MIT / active | pushed 2026-09-06 | MEDIUM | DEEP HARVEST |
| Goose | coding/general agent, runtime substrate | [aaif-goose/goose](https://github.com/aaif-goose/goose) | `main` / `5e90925962f05acf8e255032de44d16c4a7768a2` | Apache-2.0 / active | pushed 2026-09-06 | MEDIUM | TARGETED HARVEST |
| OpenWork | desktop/product shell over agent runtime | [ObunagaLabs/openwork](https://github.com/ObunagaLabs/openwork) | `add-admin-reverification-step-up` / `5e406445e811a00ba0d1103b9ab80ffba1c62bdb` | GitHub `NOASSERTION` / active but provenance-sensitive | pushed 2026-07-28 | MEDIUM | TARGETED HARVEST |
| OpenHands | autonomous coding agent/control center | [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) | `main` / `f7fb0c4b21f5ed726edbba8a6309634ef434b004` | MIT / active | pushed 2026-09-06 | HIGH | DEEP HARVEST |
| Aider | CLI coding agent, context/planning | [Aider-AI/aider](https://github.com/Aider-AI/aider) | `main` / `5dc9490bb35f9729ef2c95d00a19ccd30c26339c` | Apache-2.0 / active | pushed 2026-05-22 | MEDIUM | TARGETED HARVEST |
| Cline | IDE/terminal coding agent, parallel workspace | [cline/cline](https://github.com/cline/cline) | `main` / `dac3b35ba485dbab3b5a73aca239b0d07ce071cf` | Apache-2.0 / active | pushed 2026-09-05 | MEDIUM | TARGETED HARVEST |
| Continue | IDE/CLI coding agent platform | [continuedev/continue](https://github.com/continuedev/continue) | `main` / `5522c6f44ca0ac3528b37244818fbfa39b5af470` | Apache-2.0 / active | pushed 2026-09-06 | LOW | LANDSCAPE ONLY |
| SWE-agent | autonomous issue-solving agent | [SWE-agent/SWE-agent](https://github.com/SWE-agent/SWE-agent) | `main` / `3ea751c087f32b16e039a2233dd6eefecef325d5` | MIT / active, successor emphasized | pushed 2026-08-31 | MEDIUM | TARGETED HARVEST |
| Plandex | long-context planning/execution | [plandex-ai/plandex](https://github.com/plandex-ai/plandex) | `main` / `e2d772072efadbe41d2946d97d79be55532dbab5` | MIT / stale activity signal | pushed 2025-10-03 | MEDIUM | LANDSCAPE ONLY |
| Vibe Kanban | agent workspaces, kanban, diff/PR review | [BloopAI/vibe-kanban](https://github.com/BloopAI/vibe-kanban) | `main` / `4deb7eca8f381f7cbc1f9d15515a9ab8f8009053` | Apache-2.0 / active | pushed 2026-04-24 | HIGH | DEEP HARVEST |
| CrewAI | role-based multi-agent and event flows | [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) | `main` / `143e902178a07d0f13f9db2308f983aaacaaf0f8` | MIT / active | pushed 2026-09-04 | MEDIUM | TARGETED HARVEST |
| LangGraph | stateful orchestration, durable execution, HITL | [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | `main` / `81bf17b23123e4ef8b9d5f49fa09a0122fc2edd1` | MIT / active | pushed 2026-09-06 | HIGH | DEEP HARVEST |
| AutoGen | multi-agent framework | [microsoft/autogen](https://github.com/microsoft/autogen) | `main` / `027ecf0a379bcc1d09956d46d12d44a3ad9cee14` | CC-BY-4.0 metadata / maintenance mode | pushed 2026-04-15 | MEDIUM | LANDSCAPE ONLY |
| MetaGPT | software-company role simulation | [FoundationAgents/MetaGPT](https://github.com/FoundationAgents/MetaGPT) | `main` / `11cdf466d042ae04fc6cfd13b28e1a70341b1f` | MIT / active, older activity | pushed 2026-01-21 | HIGH | TARGETED HARVEST |
| E2B | secure code/runtime sandbox | [e2b-dev/E2B](https://github.com/e2b-dev/E2B) | `main` / `473d8bf3e62b68ee731cf18afb2e8258f9ca7a7c` | Apache-2.0 / active | pushed 2026-09-04 | HIGH | TARGETED HARVEST |
| Daytona | elastic AI-code computers/sandboxes | [daytonaio/daytona](https://github.com/daytonaio/daytona) | `main` / `ec4c21b2d597091ac09ecc278f3bcc172575a987` | GitHub license unrecognized / inspect before reuse | pushed 2026-07-24 | HIGH | TARGETED HARVEST |
| Browser Use | browser/computer-use agent | [browser-use/browser-use](https://github.com/browser-use/browser-use) | `main` / `e25ab65e699af3031a1f2d348526de2844be0e89` | MIT / active | pushed 2026-09-05 | MEDIUM | LANDSCAPE ONLY |
| ChatDev | multi-agent software lifecycle platform | [OpenBMB/ChatDev](https://github.com/OpenBMB/ChatDev) | `main` / `4fb2db0ea90375ce1059f44fe03ffbd191a7a169` | Apache-2.0 / active | pushed 2026-07-24 | HIGH | TARGETED HARVEST |
| Nimbalyst | visual local agent workspace | [nimbalyst/nimbalyst](https://github.com/nimbalyst/nimbalyst) | `main` / `34b14f33e48fd639d32c0f5eb7d77561bdccd2a4` | MIT / active | pushed 2026-09-05 | HIGH | TARGETED HARVEST |
| agtx | terminal blackboard/fleet orchestrator | [fynnfluegge/agtx](https://github.com/fynnfluegge/agtx) | `main` / `d307c4c182dff19a65370a50403185cb826f7f49` | Apache-2.0 / active | pushed 2026-09-06 | HIGH | TARGETED HARVEST |
| omux | tmux meta-agent and reviewer | [Happenmass/omux](https://github.com/Happenmass/omux) | `main` / `ecb127e39f28c0c461537b0f323a0b15e7f70fa7` | GitHub license unrecognized / early | pushed 2026-07-14 | HIGH | TARGETED HARVEST |
| Clave | local visual agentic IDE | [codika-io/clave](https://github.com/codika-io/clave) | `prod` / `e39c9a674fe8f9fa837c5f94bc5233a55384e51e` | MIT / early | pushed 2026-09-06 | HIGH | TARGETED HARVEST |
| BossConsole | governed operator console/workspace | [risa-labs-inc/BossConsole](https://github.com/risa-labs-inc/BossConsole) | `main` / `154c9c4bca5c38d06a723ad409b85a25cf54eb73` | Apache-2.0 / active | pushed 2026-09-06 | HIGH | TARGETED HARVEST |
| Vigla | mission control, typed events, isolated workers | [Kilbex/Vigla](https://github.com/Kilbex/Vigla) | `main` / `bbd19ae2d5a77401502756c550b5dcd4ae59bbc9` | Apache-2.0 / early | pushed 2026-09-01 | HIGH | DEEP HARVEST |
| Conductor | commercial multi-agent cloud workspace | [Conductor](https://www.conductor.build/) | N/A / proprietary service | commercial / closed | current site/changelog observed | HIGH | TARGETED HARVEST |
| Codeman | self-hosted agent mission control | [Ark0N/Codeman](https://github.com/Ark0N/Codeman) | `master` / `92af855ce4c0483569fd8cdde5069d1c56ec849a` | MIT / early | pushed 2026-09-06 | MEDIUM | LANDSCAPE ONLY |
| Astro Agent | DAG/worktree agent orchestrator | [astro-anywhere/astro-agent](https://github.com/astro-anywhere/astro-agent) | `dev` / `60b0fd138887600ee77d0f404b9e5e37ea479752` | GitHub `NOASSERTION` / early | pushed 2026-04-27 | HIGH | LANDSCAPE ONLY |
| Agent Mission Control | pixel-art visual operations dashboard | [glglak/agent-mission-control](https://github.com/glglak/agent-mission-control) | `main` / `39e2e3bd7ffa88e1296360e8833b099435f4c6a8` | GitHub license unrecognized / tiny | pushed 2026-03-28 | HIGH | LANDSCAPE ONLY |
| Mission-Control | cost-aware durable orchestration reference | [Mission-Control](https://github.com/ryfranklin/Mission-Control) | `main` / `bf228fc3296b594befc173ec7d199cea8b9b2a68` | GitHub license unrecognized / tiny | pushed 2026-08-23 | HIGH | TARGETED HARVEST |

The Freebuff/OpenWork rows are seed comparators rather than new Apex
dependencies. “OpenWork” is not a unique repository identity in the ecosystem;
the reviewed row names its exact repository and revision. Legal reuse must be
rechecked against the exact source tree and license at any later harvest.

## 4. Category map

| Category | Candidates with meaningful signal |
|---|---|
| Coding agents / agent runtimes | Freebuff, OpenCode, Goose, OpenHands, Aider, Cline, Continue, SWE-agent |
| Multi-agent coding systems | OpenHands, Cline, CrewAI, MetaGPT, ChatDev, omux, agtx |
| Orchestration harnesses | LangGraph, CrewAI, agtx, omux, Astro Agent, Mission-Control |
| Supervisor / worker systems | Vigla, LangGraph, CrewAI, MetaGPT, ChatDev, BossConsole, Mission-Control |
| Autonomous workforce systems | OpenHands, MetaGPT, ChatDev, Conductor, Vigla |
| Product shells / agent workspaces | Freebuff, OpenWork, OpenHands, Vibe Kanban, Nimbalyst, Clave, Conductor, BossConsole |
| Context / knowledge / planning | Aider, Plandex, OpenHands, LangGraph, Vibe Kanban, agtx, MetaGPT |
| Runtime / sandbox systems | OpenCode, Goose, E2B, Daytona, OpenHands, Conductor |
| Verification / recovery systems | OpenHands, SWE-agent, LangGraph, Vigla, Mission-Control, Plandex, Vibe Kanban |
| Visual / mission-control systems | Nimbalyst, Vibe Kanban, Clave, BossConsole, Vigla, Codeman, Astro Agent, Agent Mission Control, Mission-Control |
| Spatial / game-like ecosystems | Agent Mission Control; visual/spatial features in Nimbalyst, BossConsole, and Vigla are adjacent rather than equivalent |

## 5. Candidate profiles

The profiles below are intentionally shallow. “Likely ownership” is a route to
inspect in a later harvest, not a claim that the repository implements every
step as an Apex-equivalent contract.

### OpenCode — DEEP HARVEST

- Primary source: [official repository](https://github.com/anomalyco/opencode),
  `dev@ea2d59d7ca8028951a16d4ebc558104258440bf9`.
- Product shape: `DOCUMENTATION_EVIDENCE` describes an open-source coding agent
  with CLI/TUI and beta desktop surfaces, multi-provider support, sessions,
  tools, persistent storage, LSP, and file-change tracking.
- Execution/context: a strong first-runtime comparator for agent loop, tools,
  sessions, provider selection, and persistence. Full semantic authority,
  recovery, and acceptance guarantees are `NOT_PROVEN` here.
- Isolation/authority: runtime/process boundaries may be visible in a deep
  audit; Apex must not infer Core authority from substrate behavior.
- Likely trace: user input → CLI/TUI entry → session/context → agent loop/tool
  calls → provider/runtime process → file changes/events → session result.
- Apex relevance: strongest direct comparator for the existing first-substrate
  direction, while preserving adapter replaceability. Novelty: MEDIUM.

### OpenHands — DEEP HARVEST

- Primary source: [official repository](https://github.com/OpenHands/OpenHands),
  `main@f7fb0c4b21f5ed726edbba8a6309634ef434b004`, MIT.
- Product shape: `DOCUMENTATION_EVIDENCE` identifies Agent Canvas as a
  self-hosted developer control center and describes local/remote/cloud
  backends, multiple agent types, and automation/GitHub issue decomposition.
- Multi-agent/workflow: strong comparator for autonomous issue-to-workflow
  control, agent backends, automation, and result visibility. Exact join,
  retry, authority binding, and acceptance semantics are `NOT_PROVEN`.
- Likely trace: issue/user request → Canvas/automation entry → decomposition →
  selected agent/backend → container or remote runtime → tools/workspace →
  artifacts/PR/result → automation status.
- Apex relevance: broadest current comparator for a product shell above an
  execution substrate. Novelty: HIGH.

### Vibe Kanban — DEEP HARVEST

- Primary source: [official repository](https://github.com/BloopAI/vibe-kanban),
  `main@4deb7eca8f381f7cbc1f9d15515a9ab8f8009053`, Apache-2.0.
- Product shape: `DOCUMENTATION_EVIDENCE` describes a kanban workspace where
  each agent receives a workspace/branch/terminal/dev server, with inline diff
  comments, browser/device tools, and PR/merge flow.
- Multi-agent/UX: particularly useful for bounded parallel work, human review,
  workspace isolation, and result aggregation. It is not proof of Apex’s
  authority or recovery contract.
- Likely trace: board item → workspace/agent selection → branch/worktree and
  terminal → change/result → diff comments/review → PR/merge.
- Apex relevance: complementary product/work-management shell comparator.
  Novelty: HIGH.

### Vigla — DEEP HARVEST

- Primary source: [official repository](https://github.com/Kilbex/Vigla),
  `main@bbd19ae2d5a77401502756c550b5dcd4ae59bbc9`, Apache-2.0.
- Product shape: `DOCUMENTATION_EVIDENCE` describes local-first mission control
  with typed event streams, isolated worktrees, supervisor checks for scope,
  reversibility, risk and quality, and accept/extend/scrub/escalate decisions.
- Verification/recovery: the supervisor/review/revert vocabulary is unusually
  close to Apex’s verification and recovery interests. Exact production
  reliability and authority guarantees remain `NOT_PROVEN`.
- Likely trace: mission/envelope → supervisor plan → worker/worktree → typed
  events → supervisor review → accept/extend/scrub/escalate → merge or revert.
- Apex relevance: strongest small, source-available comparator for a governed
  supervisor/worker control surface. Novelty: HIGH.

### LangGraph — DEEP HARVEST

- Primary source: [official repository](https://github.com/langchain-ai/langgraph),
  `main@81bf17b23123e4ef8b9d5f49fa09a0122fc2edd1`, MIT.
- Product shape: `DOCUMENTATION_EVIDENCE` describes low-level stateful
  orchestration with durable execution/resume, human-in-the-loop, memory, and
  tracing/deployment integrations.
- Orchestration: a strong conceptual comparator for explicit state, pause/
  resume, branching, human gates, and durable workflow boundaries. It is a
  framework, not an Apex product shell or Core authority implementation.
- Likely trace: API/graph entry → stateful node/agent → tool/subgraph →
  checkpoint → human gate/restart → final state/trace.
- Apex relevance: useful for future orchestration interfaces without making
  Orchestration a Core dependency. Novelty: HIGH.

### E2B and Daytona — TARGETED HARVEST

- Primary sources: [E2B](https://github.com/e2b-dev/E2B),
  `main@473d8bf3e62b68ee731cf18afb2e8258f9ca7a7c`, Apache-2.0; and
  [Daytona](https://github.com/daytonaio/daytona),
  `main@ec4c21b2d597091ac09ecc278f3bcc172575a987`.
- Product shape: both document secure or elastic code-running environments;
  E2B emphasizes isolated cloud sandboxes and SDKs, while Daytona describes
  persistent composable computers/control and compute planes.
- Apex relevance: targeted source audit is justified for workspace snapshots,
  process/tool/network isolation, lifecycle, persistence, and recovery. Neither
  product-level acceptance nor Apex authority binding should be inferred.
- Licensing: E2B is Apache-2.0 in repository metadata. Daytona’s GitHub
  metadata did not resolve a standard SPDX license; reuse is `NOT_PROVEN`
  until the exact license is inspected.

### Nimbalyst, Clave, BossConsole — TARGETED HARVEST

- Primary sources: [Nimbalyst repository](https://github.com/nimbalyst/nimbalyst)
  at `main@34b14f33e48fd639d32c0f5eb7d77561bdccd2a4`, [Nimbalyst product
  site](https://nimbalyst.com/product/), [Clave repository](https://github.com/codika-io/clave)
  at `prod@e39c9a674fe8f9fa837c5f94bc5233a55384e51e`, and
  [BossConsole repository](https://github.com/risa-labs-inc/BossConsole) at
  `main@154c9c4bca5c38d06a723ad409b85a25cf54eb73`.
- Product shape: official pages describe local visual workspaces, parallel
  sessions, worktree/diff review, remote connections, session boards, or a
  governed multi-provider operator console with RBAC/MCP/plugin surfaces.
- Apex relevance: these are targeted UX/control-plane references for making
  persistent state legible. The visual surface must remain a projection of
  canonical Apex state, never its owner. Novelty: HIGH.
- License: Nimbalyst and Clave report MIT metadata; BossConsole reports
  Apache-2.0.

### agtx and omux — TARGETED HARVEST

- Primary sources: [agtx](https://github.com/fynnfluegge/agtx),
  `main@d307c4c182dff19a65370a50403185cb826f7f49`, Apache-2.0; and
  [omux](https://github.com/Happenmass/omux),
  `main@ecb127e39f28c0c461537b0f323a0b15e7f70fa7`.
- Product shape: agtx documents a terminal blackboard with parallel agents,
  context handover, dependency graph, backlog, review/done phases, and virtual
  merge checking. omux documents a tmux meta-agent with parallel subagents,
  auto-continue, execute-then-review, cross-session memory, adapter routing,
  and explicitly no git worktree isolation.
- Apex relevance: useful contrast between a blackboard/worktree model and a
  lightweight pane/session supervisor. Their limitations are also useful:
  workspace isolation, semantic state, and merge/recovery guarantees require
  direct inspection. omux’s license was not recognized in GitHub metadata.

### CrewAI, MetaGPT, ChatDev — TARGETED HARVEST

- Primary sources: [CrewAI](https://github.com/crewAIInc/crewAI),
  `main@143e902178a07d0f13f9db2308f983aaacaaf0f8`, MIT; [MetaGPT](https://github.com/FoundationAgents/MetaGPT),
  `main@11cdf466d042ae04fc6cfd13b28e1a70341b1f`, MIT; and
  [ChatDev](https://github.com/OpenBMB/ChatDev),
  `main@4fb2db0ea90375ce1059f44fe03ffbd191a7a169`, Apache-2.0.
- Product shape: official documentation describes role-based crews/flows,
  software-company role simulation, or a multi-agent software lifecycle
  platform.
- Apex relevance: these systems offer complementary workflow/decomposition and
  result-aggregation patterns. DPT role semantics, “virtual company” language,
  and team topology must not be imported into Apex Core. Novelty: HIGH for
  workforce concepts, MEDIUM for Core execution.

### Mission-Control and related small visual systems — TARGETED or LANDSCAPE

- [Mission-Control](https://github.com/ryfranklin/Mission-Control) documents a
  cost-aware durable orchestration reference with isolated worktrees,
  per-step telemetry, human go/no-go, crash resume, and an evaluation harness.
  Its license is `NOT_PROVEN` from repository metadata; targeted harvest is
  justified because the recovery/cost/approval combination is unusually close
  to Apex concerns.
- [Codeman](https://github.com/Ark0N/Codeman),
  [Astro Agent](https://github.com/astro-anywhere/astro-agent), and
  [Agent Mission Control](https://github.com/glglak/agent-mission-control) are
  useful visual or multi-repository comparators, but are small or early. They
  remain landscape only until source depth, health, and reusable contracts
  justify a harvest.

### Other seed and context comparators — LANDSCAPE or TARGETED

- Goose is a strong provider/MCP/runtime comparator, but not the first deep
  target while OpenCode is already Apex’s initial substrate direction.
- Aider is valuable for repository mapping, model/provider flexibility, and
  human-controlled git flow; it is less valuable for multi-agent supervision.
- Cline is useful for per-run workspace isolation and parallel agent UX.
- Continue and Browser Use broaden the IDE and computer-use landscape, but
  mostly duplicate known dimensions for the next deep harvest.
- SWE-agent remains a useful issue-solving/evaluation comparator, while its
  own README emphasizes current development moving to mini-SWE-agent; this
  reduces the value of treating the repository as a primary current target.
- Plandex remains relevant to long-context planning and cumulative diff review,
  but its activity signal is stale relative to the current shortlist.
- AutoGen is historically important but its official repository says it is in
  maintenance mode and directs new users to Microsoft Agent Framework; its
  CC-BY-4.0 metadata also warrants legal review before reuse.

## 6. Comparative matrix

This matrix is a discovery aid, not a benchmark. Cells summarize primary-source
documentation and repository shape; `NOT_PROVEN` means the stronger semantic
claim needs a source-level or runtime audit.

| Candidate | Core execution | Context / planning | Multi-agent / orchestration | Routing / providers | Isolation / authority | Recovery / durable state | Verification / acceptance | Visual / supervisor UX | Apex novelty |
|---|---|---|---|---|---|---|---|---|---|
| OpenCode | YES | PARTIAL | PARTIAL | YES | NOT_PROVEN | PARTIAL | PARTIAL | PARTIAL | MEDIUM |
| Goose | YES | PARTIAL | PARTIAL | YES | NOT_PROVEN | PARTIAL | PARTIAL | PARTIAL | MEDIUM |
| OpenHands | YES | YES | YES | PARTIAL | PARTIAL / NOT_PROVEN | PARTIAL | PARTIAL | YES | HIGH |
| Cline | YES | PARTIAL | YES | YES | PARTIAL / NOT_PROVEN | PARTIAL | PARTIAL | PARTIAL | MEDIUM |
| Vibe Kanban | N/A shell | PARTIAL | YES | PARTIAL | YES workspace / NOT_PROVEN authority | PARTIAL | YES diff/review | YES | HIGH |
| Nimbalyst | N/A shell | PARTIAL | YES | PARTIAL | YES worktree / NOT_PROVEN authority | NOT_PROVEN | YES diff/review | YES | HIGH |
| agtx | PARTIAL | YES | YES | PARTIAL | PARTIAL / NOT_PROVEN | PARTIAL | PARTIAL | YES | HIGH |
| omux | YES via adapters | PARTIAL | YES | YES | NO worktree isolation documented | PARTIAL | YES independent review | PARTIAL | HIGH |
| Vigla | PARTIAL worker harness | PARTIAL | YES | PARTIAL | YES worktree / NOT_PROVEN authority | YES revert direction / NOT_PROVEN durability | YES supervisor gates | YES | HIGH |
| LangGraph | N/A framework | YES | YES | PARTIAL | NOT_PROVEN | YES documented durable execution | PARTIAL | PARTIAL via tracing | HIGH |
| CrewAI | N/A framework | PARTIAL | YES | PARTIAL | NOT_PROVEN | PARTIAL | PARTIAL | NO | MEDIUM |
| MetaGPT | YES via roles | YES | YES | PARTIAL | NOT_PROVEN | PARTIAL | PARTIAL | NO | HIGH |
| ChatDev | YES via roles | YES | YES | PARTIAL | NOT_PROVEN | PARTIAL | PARTIAL | PARTIAL | HIGH |
| E2B | N/A runtime | N/A | N/A | N/A | YES sandbox / NOT_PROVEN Apex authority | PARTIAL | NOT_PROVEN | NO | HIGH |
| Daytona | N/A runtime | N/A | N/A | N/A | YES documented isolation / NOT_PROVEN Apex authority | YES persistence direction | NOT_PROVEN | PARTIAL | HIGH |
| Mission-Control | PARTIAL | PARTIAL | YES | PARTIAL | YES worktree / NOT_PROVEN authority | YES documented crash-resume direction | YES human go/no-go | YES | HIGH |

## 7. Visual and mission-control landscape

The most relevant visual systems are not all competitors for the same product
layer:

- Nimbalyst and Clave emphasize a local visual workspace around live sessions,
  files, and diffs.
- Vibe Kanban emphasizes work-item routing, isolated agent workspaces, and
  review/merge.
- BossConsole emphasizes an operator console with governed tools, plugins, and
  multi-provider threads.
- Vigla emphasizes mission supervision, typed events, risk/reversibility
  checks, and action after review.
- Codeman and Astro Agent emphasize fleets, repositories, dashboards, or
  worktree-backed supervision at an early stage.
- Agent Mission Control is a novel pixel-art operational projection, but its
  small repository size and limited activity make it a visual reference rather
  than a near-term architecture source.
- Conductor is a commercial reference for cloud team-of-agents UX,
  multiplayer workspace, isolated compute, and broad client surfaces. It is
  useful for product-shape comparison but cannot provide reusable source
  implementation.

The Apex question is not “which visual metaphor should Apex copy?” It is which
canonical state, events, dependencies, gates, and human interventions should a
projection make legible. The visual layer must remain downstream of Apex state.

## 8. Multi-agent and workforce landscape

OpenHands, CrewAI, MetaGPT, ChatDev, LangGraph, agtx, omux, Vigla, and
Conductor expose different answers to delegation:

- role simulation (MetaGPT/ChatDev);
- explicit crews and event flows (CrewAI);
- stateful graphs and resumable nodes (LangGraph);
- workspace/board-oriented agents (Vibe Kanban/agtx);
- lightweight session supervision (omux);
- governed supervisor/worker review (Vigla);
- productized cloud team workspaces (Conductor);
- autonomous developer control-center workflows (OpenHands).

The transferable Apex concern is capability and responsibility boundaries, not
simulated job titles. DPT-specific roles remain optional capability territory.
No candidate in this shallow pass proves a complete Apex-grade semantic model
for delegation, join, retry, reassignment, authority, acceptance, and learning
as one coherent contract.

## 9. Runtime, authority, and isolation landscape

OpenCode and Goose are the strongest substrate comparisons. E2B and Daytona
are the strongest runtime-isolation comparisons. OpenHands and Conductor show
how product surfaces can select local, remote, or cloud execution backends.
Vibe Kanban, Nimbalyst, agtx, and Vigla provide worktree/session isolation
patterns.

These are different layers. A sandbox or worktree is not an Apex
`PermissionEnvelope`; a runtime session is not an Apex `Attempt`; a provider
selector is not an Apex `ModelSelection` contract; and a documented approval
button is not proof of immutable authority binding. The complete
AuthorityRevision → RuntimeLane/Attempt activation chain remains
`NOT_PROVEN` for Apex.

## 10. Verification and recovery landscape

- OpenHands and SWE-agent are useful autonomous issue-solving comparators, but
  result quality and durable semantic acceptance require a deeper audit.
- Vibe Kanban makes diff review and PR/merge a visible product boundary.
- Vigla exposes supervisor checks and accept/extend/scrub/escalate/revert
  concepts that are unusually relevant to Apex verification/recovery.
- LangGraph documents durable execution and resume, useful for orchestration
  state but not a complete runtime authority model.
- Mission-Control documents crash resume, cost telemetry, human go/no-go, and
  evaluation-harness ideas, but its small size and license uncertainty limit
  confidence.
- Plandex offers cumulative diff review and controlled command execution, with
  a stale current-activity signal.
- omux’s execute-then-review flow is useful as a narrow review pattern, while
  its lack of worktree isolation is an important limitation.

No landscape source establishes that runtime completion equals semantic task
success. Apex should preserve the distinction among result collection,
verification, acceptance, and completion.

## 11. Context and planning landscape

Aider’s repository map, Plandex’s long-context plan/execute model, OpenHands’
automation/decomposition, LangGraph’s explicit state graph, agtx’s dependency
blackboard, and Vibe Kanban’s task/workspace board are complementary references.

The reusable Apex question is how to retain bounded intent and context while
avoiding hidden state. A candidate’s “memory,” “context,” or “plan” label is
not by itself evidence of Apex `ExecutionManifest`, `Task Passport`, or
`Current State` semantics.

## 12. Licensing and reuse notes

The classifications separate conceptual learning from code reuse. A useful
concept can remain relevant even when its code is legally unsuitable.

- MIT: OpenCode, OpenHands, Aider, CrewAI, LangGraph, MetaGPT, Nimbalyst,
  Clave, and Codeman report MIT metadata.
- Apache-2.0: Freebuff, Goose, Cline, Continue, Vibe Kanban, E2B, agtx,
  BossConsole, Vigla, and ChatDev report Apache-2.0 metadata.
- CC-BY-4.0 / maintenance: AutoGen’s repository metadata is not a default
  assumption for source incorporation; inspect the exact license and content
  boundaries before reuse.
- `NOASSERTION` or unrecognized: OpenWork, Daytona, omux, Astro Agent, Agent
  Mission Control, and Mission-Control need exact license inspection before any
  source reuse. The report makes no legal conclusion.
- Proprietary: Conductor is a product/service reference, not a source-reuse
  candidate.
- Archived/stale health is separate from license: Plandex and MetaGPT have
  weaker recent-activity signals than the active systems; SWE-agent’s own
  README points toward its successor.

No external source code or dependency was added to Apex Code.

## 13. Apex novelty analysis

### High novelty

Vigla’s supervisor review/revert/event model; LangGraph’s stateful durable
orchestration; OpenHands’ control-center/automation shape; Vibe Kanban’s
work-item-to-isolated-workspace review path; Nimbalyst/Clave/BossConsole’s
visual persistent workspace patterns; agtx’s blackboard/dependency model;
Mission-Control’s cost-aware crash-resume reference; and E2B/Daytona’s
composable sandbox/control-plane boundaries.

### Medium novelty

OpenCode and Goose runtime/provider boundaries; Cline’s parallel workspace UX;
Aider’s repository mapping; Plandex’s large-task planning and diff review;
CrewAI/ChatDev/MetaGPT workflow decomposition; and Freebuff’s multi-surface
product positioning.

### Low novelty

Continue, Browser Use, and generic coding-agent surfaces in this phase. They
remain useful context and may become relevant to a focused provider, IDE, or
computer-use question.

## 14. Recommended classification

### DEEP HARVEST

1. OpenCode — first-runtime and adapter boundary.
2. OpenHands — autonomous developer control center and automation.
3. Vibe Kanban — work-item, workspace, review, and merge product flow.
4. Vigla — supervisor, typed events, verification, and recovery direction.
5. LangGraph — durable stateful orchestration and human-gate semantics.

This is a complementary shortlist. It intentionally does not mean Apex should
adopt any implementation or depend on any project.

### TARGETED HARVEST

OpenWork; Goose; Cline; Aider; SWE-agent; CrewAI; MetaGPT; ChatDev; E2B; Daytona;
Nimbalyst; Clave; BossConsole; agtx; omux; Mission-Control; and Conductor.

The target should be narrowed by the Owner to a specific subsystem or question
per candidate, such as “worktree isolation,” “durable resume,” “visual human
gate,” or “provider/runtime adapter.”

### LANDSCAPE ONLY

Freebuff; Continue; Plandex; Browser Use; AutoGen; Codeman; Astro Agent; and
Agent Mission Control.

These candidates are useful context, but their next-harvest value is lower due
to overlap, maintenance status, small/early evidence, or layer mismatch.

### REJECT

No candidate was rejected solely for being small or unfamiliar: a narrow
system can still teach Apex something. No additional candidate met the
high-confidence threshold for a hard `REJECT` in this discovery pass. The
Owner may reject candidates later for legal, health, or architectural reasons
after the shortlist is chosen.

## 15. Source-level trace for likely top candidates

These traces identify likely ownership boundaries to inspect later. They are
not full audits and do not assert that every arrow exists exactly as drawn.

| Candidate | Likely path for later inspection |
|---|---|
| OpenCode | User input → CLI/TUI → context/session → planner/agent loop → model/provider → tool calls → workspace/files → events/result → persistence |
| OpenHands | User/issue → Canvas/automation → decomposition → agent/backend selection → container/remote runtime → tools/workspace → artifacts/PR → result/automation state |
| Vibe Kanban | Work item → agent/workspace selection → branch/worktree + terminal/dev server → diff/result → comments/review → PR/merge |
| Vigla | Mission → supervisor plan → worker/worktree → typed events → supervisor checks → accept/extend/scrub/escalate → merge/revert |
| LangGraph | API/graph entry → stateful node/subgraph → tool/agent work → checkpoint → human gate/restart → final state/trace |
| E2B / Daytona | SDK/API → control plane → sandbox/composable computer → process/code/tool execution → snapshot/result → lifecycle cleanup/recovery |

## 16. Open questions and `NOT_PROVEN` items

- Which exact OpenWork repository, license, and revision should remain the
  relevant shell comparator? Multiple repositories use the name.
- Does any candidate provide an immutable, versioned authority revision bound
  to an exact attempt/lane before execution? `NOT_PROVEN`.
- Which systems provide durable join/retry/reassignment semantics rather than
  merely parallel processes? `NOT_PROVEN` for this landscape.
- Which candidate’s visual state is a projection of a durable canonical model,
  rather than the UI’s own state? `NOT_PROVEN`.
- What recovery evidence survives process loss, machine loss, or provider
  failure? `NOT_PROVEN` across the landscape.
- Which licenses permit conceptual-only versus source-level reuse, and under
  what attribution or copyleft obligations? `NOT_PROVEN` until legal review of
  the exact files.
- Do commercial systems expose enough documentation for targeted comparative
  learning without implying source access? `UNKNOWN`.
- Does Freebuff’s current hosted/local product structure provide transferable
  product-shell patterns beyond existing Apex evidence? `UNKNOWN` until a
  focused harvest.

## 17. Owner decisions required

1. Select the final deep-harvest shortlist; the five recommendations above are
   intentionally a starting point.
2. Decide whether the next harvest prioritizes Core execution, runtime
   isolation, development workflow, supervisor/workforce control, or visual
   mission control.
3. Decide whether commercial references such as Conductor belong in targeted
   product/UX research despite having no reusable source.
4. Decide whether exact-license review should precede all targeted source
   inspection for `NOASSERTION` candidates.
5. Decide whether the OpenWork comparison should follow the current
   `ObunagaLabs/openwork` repository, another named OpenWork repository, or the
   already-recorded Apex OpenWork feasibility evidence only.

## 18. Non-effects on Apex architecture

This report does not change the Apex architecture, execution data model,
execution API, authority model, Runtime Adapter design, Capability SPI, DPT,
Orchestration, product roadmap commitments, commercial packaging, CI, or
runtime code. It does not establish any candidate as an Apex dependency or
prove any candidate’s runtime guarantee.
