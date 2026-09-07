# OpenCode Authority Attestation Proof 0001

Status: `PROPOSED` evidence report; no architecture status change
Evidence date: 2026-09-07 Asia/Tehran
Scope: bounded source inspection and disposable OpenCode server probes

## 1. Executive result

`E1 = NOT_PROVEN`.

The experiment directly observed configuration materialization before server
and session creation, and it observed stable OpenCode session identifiers.
It did not find a machine-readable OpenCode attestation that the exact Apex
`AuthorityRevision` was active, bound to a RuntimeLane, or bound to an Apex
Attempt/ExecutionEpoch before side effects. Configuration materialization is
therefore not treated as activation or binding proof.

## 2. Pinned environment

| Field | Observation |
| --- | --- |
| Repository | `anomalyco/opencode` |
| Source URL | <https://github.com/anomalyco/opencode> |
| Inspected source ref | `e207624c48159b03dbe17dbc8e51bbcf23e72df5` |
| Installed executable | `/usr/local/Cellar/opencode/1.18.25/bin/opencode` |
| Installed version | `1.18.25` |
| Source/binary identity | `NOT_PROVEN`; the installed binary was not assumed byte-identical to the source checkout |
| Workspace | disposable temporary workspace with harmless sentinels |
| Dependencies added | none |

Relevant source paths inspected at the pinned source ref:

- `packages/core/src/config.ts`
- `packages/core/src/global.ts`
- `packages/core/src/permission.ts`
- `packages/core/src/v1/config/permission.ts`
- `packages/server/src/handlers/health.ts`
- `packages/server/src/handlers/permission.ts`
- `packages/server/src/handlers/session.ts`
- `packages/server/src/handlers/event.ts`
- `packages/protocol/src/groups/health.ts`
- `packages/protocol/src/groups/permission.ts`
- `packages/protocol/src/groups/session.ts`
- `packages/sdk/openapi.json`

## 3. Experiment architecture

[`opencode_authority_attestation_probe.py`](../../experiments/runtime-proof/opencode_authority_attestation_probe.py)
used only the Python standard library. For two disposable labels, the harness:

1. wrote an OpenCode deny-all configuration and a separate Apex-shaped
   AuthorityRevision identifier/digest;
2. started `opencode serve --pure` with isolated configuration and XDG roots;
3. waited for `/api/health`;
4. created and retrieved one harmless session;
5. queried active-session and session-permission surfaces;
6. terminated the disposable server and deleted the temporary root through the
   harness context manager.

No agent prompt, tool call, credential, secret file, or secret content was
used. The experiment did not attempt to turn a permission-denial result into
identity-binding proof.

## 4. Observed results

| Probe | Direct observation | Evidence label |
| --- | --- | --- |
| Config materialization | `opencode.json` and the authority digest were written before server start | `OBSERVED_RUNTIME_EVIDENCE` |
| Server health | `/api/health` returned HTTP `200` and `{"healthy":true}` | `OBSERVED_RUNTIME_EVIDENCE` |
| Session identity | `/api/session` returned HTTP `200` with a machine-readable `ses_...` identifier | `OBSERVED_RUNTIME_EVIDENCE` |
| Session retrieval | The created session was retrievable by ID | `OBSERVED_RUNTIME_EVIDENCE` |
| Permission API | The session permission list endpoint was reachable, but did not return an Apex authority digest/binding record | `OBSERVED_RUNTIME_EVIDENCE` |
| Active-session API | `/api/session/active` returned an empty data map immediately after session creation | `OBSERVED_RUNTIME_EVIDENCE` |
| Authority revision A vs B | Two different Apex-shaped revision identifiers produced the same OpenCode config digest because the identifier was external to OpenCode configuration | `OBSERVED_RUNTIME_EVIDENCE` |
| Exact active authority | No direct OpenCode attestation was observed | `NOT_PROVEN` |
| Exact session/config binding | No direct digest-to-session binding was observed | `NOT_PROVEN` |
| Exact execution binding | No execution was started; no binding surface was observed | `NOT_PROVEN` |

The OpenCode source supports these boundaries: configuration is loaded from
configured roots (`packages/core/src/config.ts`, `packages/core/src/global.ts`),
permission evaluation is an action/resource decision surface
(`packages/core/src/permission.ts`), and health/session/permission endpoints
return service/session/request data rather than an Apex authority attestation
(`packages/server/src/handlers/health.ts`, `permission.ts`, `session.ts`).
This is `SOURCE_CODE_EVIDENCE` about available surfaces, not proof that every
runtime behavior is absent beyond the inspected paths.

## 5. Required authority sequence

The Apex sequence remains unchanged:

```text
PermissionEnvelope
→ AuthorityRevision
→ materialization
→ activation verification
→ exact RuntimeLane binding
→ exact Attempt / ExecutionEpoch binding
→ Execution Barrier
→ START
```

The harness only established the first, local materialization ordering. It did
not establish `CONFIG_LOADED`, `CONFIG_ACTIVE`,
`CONFIG_BOUND_TO_SESSION`, or `CONFIG_BOUND_TO_EXECUTION` as independently
attested Apex facts. The pre-start barrier must therefore continue to fail
closed when activation/binding evidence is unavailable.

## 6. Results by required test

| Test | Result | Interpretation |
| --- | --- | --- |
| E1-A materialization before execution | `CONFIG_WRITTEN` observed | Harness ordering only; no atomic substrate barrier proven |
| E1-B activation verification | `NOT_PROVEN` | Health and permission surfaces do not attest exact active revision |
| E1-C identity binding | `NOT_PROVEN` | Session ID was not correlated to Apex Attempt/Epoch/revision |
| E1-D negative access after verified activation | `NOT_PROVEN` | Activation was not verified, so no denial result is overclaimed |
| E1-E authority drift | `NOT_PROVEN` | No active-authority signal existed for old/new comparison |
| E1-F pre-start barrier | `NOT_PROVEN` at substrate boundary | Apex may enforce its own gate, but OpenCode atomic enforcement was not proven |

## 7. Implications

The adapter may report runtime-native identity and substrate facts, but Core
must own the authority evidence chain and decide whether the execution barrier
can release. A config path, digest, session ID, health response, or permission
denial is not by itself an `AuthorityRevision` activation/binding guarantee.

No architecture status was changed. In particular, exact authority binding
remains `NOT_PROVEN`, and no Runtime Adapter, authority engine, or product
dependency was added.

## 8. Follow-up experiment candidates

These are not executed by this report:

- a harmless tool permission request with a substrate-observable request ID;
- a disposable adapter-owned identity registry correlated to session/process
  events;
- a second substrate probe using the same Core authority evidence schema.
