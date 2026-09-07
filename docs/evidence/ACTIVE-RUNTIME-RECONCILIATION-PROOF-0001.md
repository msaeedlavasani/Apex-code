# Active Runtime Reconciliation Proof 0001

Status: `PROPOSED` evidence report; no architecture status change
Evidence date: 2026-09-07 Asia/Tehran
Scope: bounded controller-loss observation against an isolated OpenCode server

## 1. Executive result

`B = NOT_PROVEN`.

The follow-up experiment performed a real OpenCode controller restart while a
harmless prompt was observed in the server's active-session map. OpenCode
preserved the session record and rejected a duplicate durable message ID after
restart, but no separate runtime-native process identity or Apex Attempt
ownership was exposed, and active state was not re-established after restart.
This is useful substrate evidence, not proof of controller-independent
reconciliation or duplicate-start fencing for Apex.

## 2. Pinned environment and harness

| Field | Observation |
| --- | --- |
| Repository | `anomalyco/opencode` |
| Inspected source ref | `e207624c48159b03dbe17dbc8e51bbcf23e72df5` |
| Installed version | `1.18.25` |
| Executable | `/usr/local/Cellar/opencode/1.18.25/bin/opencode` |
| Workspace | disposable temporary workspace containing only a harmless sentinel |
| Controller | isolated `opencode serve --pure` process |
| Harness | [`active_runtime_reconciliation_probe.py`](../../experiments/runtime-proof/active_runtime_reconciliation_probe.py) |
| Secret content | not read or printed |

The source paths most relevant to the observation were inspected at the pinned
ref: `packages/core/src/session.ts`,
`packages/core/src/session/run-coordinator.ts`,
`packages/core/src/session/execution.ts`,
`packages/core/src/event.ts`, `packages/core/src/pty.ts`,
`packages/server/src/handlers/session.ts`, and
`packages/protocol/src/groups/session.ts`.

## 3. Experiment procedure

The harness:

1. wrote an isolated deny-all OpenCode configuration;
2. started a server and created one session;
3. admitted a harmless prompt with a fixed durable message ID;
4. sampled `/api/session/active`;
5. terminated the controller server without issuing a child-process kill;
6. restarted the controller using the same isolated state roots;
7. retrieved the session, active-session map, and message surface;
8. submitted the same message ID again with execution disabled;
9. queried an intentionally stale session ID;
10. terminated the disposable server.

The prompt was harmless and did not request tools or filesystem access. The
experiment did not claim that a model execution remained active after server
termination: no separate OpenCode runtime process was observable in the
tested path.

Because the active window is transient, a supplementary same-day direct probe
using the same `serve`/`session.prompt` route observed one `type: running`
session immediately after admission. The committed harness run did not
consistently capture that short window. This variance is itself a reason not
to promote OpenCode's active-session map into an Apex runtime identity or
recovery guarantee.

## 4. Raw observations

| Observation | Result | Evidence label |
| --- | --- | --- |
| Prompt admission | HTTP `200`; durable admitted sequence `1` and fixed message ID were returned | `OBSERVED_RUNTIME_EVIDENCE` |
| Active session before controller loss | A supplementary direct probe observed HTTP `200` with `type: running`; the committed harness did not consistently capture the transient window | `OBSERVED_RUNTIME_EVIDENCE` |
| Separate child runtime identity | No child process was observable under the server at the sampling point; active execution was process-owned in the tested path | `OBSERVED_RUNTIME_EVIDENCE` |
| Controller restart | Restart completed and health became reachable | `OBSERVED_RUNTIME_EVIDENCE` |
| Session after restart | HTTP `200`; same session ID was retrievable | `OBSERVED_RUNTIME_EVIDENCE` |
| Active session after restart | HTTP `200`, data `{}`; active state was not restored | `OBSERVED_RUNTIME_EVIDENCE` |
| Same message ID after restart | HTTP `409` conflict | `OBSERVED_RUNTIME_EVIDENCE` |
| Wrong/stale session ID | HTTP `404` | `OBSERVED_RUNTIME_EVIDENCE` |
| Apex Attempt ownership | No Apex Attempt/Lane/Epoch metadata was exposed by OpenCode | `NOT_PROVEN` |
| Semantic result after restart | Not inferred from session/message persistence | `NOT_PROVEN` |

The `409` is a durable OpenCode message-admission conflict. It is not Apex
single-controller fencing, because no Apex Attempt fence was supplied to or
returned by OpenCode.

## 5. Scenario classification

The requested scenarios are classified conservatively:

| Scenario | Classification | Safe Apex interpretation |
| --- | --- | --- |
| B1 running attempt, controller exits, runtime remains | `NOT_PROVEN` | An active session was observed before loss, but no separate runtime survived/was observable after controller termination |
| B2 completes while controller absent | `NOT_PROVEN` | No controller-independent OpenCode completion/result correlation was established |
| B3 runtime disappears while controller absent | `NOT_PROVEN` | OpenCode did not expose enough identity/state to distinguish runtime loss from controller loss |
| B4 wrong/stale session reconnect | `PARTIALLY_PROVEN` | Unknown session is rejected with `404`; exact Apex identity mismatch remains unproven |
| B5 duplicate request after restart | `PARTIALLY_PROVEN` | Same message ID is rejected with `409`; Apex Attempt duplicate-start fencing remains a Core responsibility and was not proven by OpenCode |
| B6 orphan runtime/session | `NOT_PROVEN` | OpenCode exposed no Apex ownership relation and no orphan-adoption/quarantine signal |

Overall B classification: `NOT_PROVEN`.

## 6. Reconciliation interpretation

For each controller-loss observation, the safe Apex record is:

| Fact dimension | Safe result |
| --- | --- |
| Durable Apex-side Attempt fact | Not present in OpenCode; must come from the Core ledger |
| Runtime observed fact | `UNKNOWN` where no separate runtime identity/status is observable; transport loss may separately be `UNREACHABLE` |
| Authority fact | `NOT_PROVEN` for active/bound AuthorityRevision |
| Resource/workspace fact | No Apex ownership relation exposed |
| Semantic classification | `RECOVERY_REQUIRED` / fail closed; never inferred success |
| Unsafe assumption avoided | session persistence, message conflict, or HTTP health is not execution recovery proof |

OpenCode source inspection supports this boundary: its session coordinator
tracks active sessions in process-owned execution state
(`packages/core/src/session/execution.ts`,
`packages/core/src/session/run-coordinator.ts`), while session/events are
durable data surfaces (`packages/core/src/session.ts`,
`packages/core/src/event.ts`). The distinction is `SOURCE_CODE_EVIDENCE`; it
does not prove an Apex-grade controller-loss contract.

## 7. Facts and non-facts

### Proven within this bounded run

- An isolated OpenCode server can admit a harmless message with a fixed ID and
  expose a process-owned active-session window.
- The session record remained retrievable after restarting the server with the
  same isolated state roots.
- The same durable message ID received an explicit conflict response after
  restart.
- An intentionally unknown session ID received an explicit not-found response.
- No secret content was read or printed.

### Remains NOT_PROVEN

- active OpenCode runtime survival after controller loss;
- controller-independent result/artifact correlation;
- exact runtime-native process/session identity binding;
- distinction of all six runtime facts for an OpenCode-owned execution;
- Apex duplicate-start prevention surviving controller loss;
- stale Attempt or RuntimeLane reconciliation;
- orphan runtime detection or quarantine by substrate;
- automatic safe resume, reconnect, reassignment, or re-execution;
- semantic success after runtime completion without Core verification.

## 8. Required Apex behavior

The Core Reconciliation Loop must continue to combine:

```text
durable Attempt state
+ Runtime Adapter observed facts
+ authority/barrier evidence
+ resource ownership
→ reconciled semantic state
```

On restart, an existing session must not be adopted or restarted merely
because it is retrievable. Missing identity, authority, result, or resource
evidence must remain `UNKNOWN`/`RECOVERY_REQUIRED`; a retry must create a new
Attempt rather than mutate the original Attempt identity.

No architecture status was changed. Controller-loss reconciliation, general
active-runtime recovery, distributed fencing, stale lease reclamation, and
checkpoint side-effect safety remain `NOT_PROVEN`.

## 9. Reproducibility

From the Apex Code repository with OpenCode `1.18.25` available:

```sh
python3 -B experiments/runtime-proof/active_runtime_reconciliation_probe.py
```
