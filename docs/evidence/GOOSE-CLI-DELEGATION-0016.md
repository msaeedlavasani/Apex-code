# Goose CLI Parallel Delegation Capability Probe 0016

Status: `PROPOSED` evidence report; no Apex architecture status change
Task: `AC-DEV-011`
Evidence date: 2026-09-08 Asia/Tehran

## 1. Executive result

Goose CLI `1.49.0` is a `PARTIAL` candidate executor for an Apex development
control plane. Its built-in `summon` surface operationally launched three
asynchronous delegated tasks with distinct session identities, returned their
individual outcomes, and allowed the parent to aggregate a mixed result. The
bounded probe also showed that unrelated delegated work can complete when one
worker reports a controlled failure.

The probe did not establish child-level cancellation, dependency scheduling, or
per-subtask provider/model assignment. Those concerns must remain owned by the
Apex Development Control Plane or be classified `NOT_PROVEN` until a separate
machine-level surface exists. Goose must remain a worker/executor, not backlog,
scheduler, authority, or verification owner.

## 2. Environment and safety

| Field | Observation |
| --- | --- |
| Executable | `/Users/msl/.local/bin/goose` |
| Version | `1.49.0` |
| Provider | `ChatGPT Codex` |
| Model | `gpt-5.6-luna` |
| Thinking effort | `High` |
| Authentication | OAuth was already configured; no credential value was read or printed |
| Workspace | disposable non-repository probe roots were created; the corrected run used Goose's `/private/tmp` process working directory |
| Repository mutation | none |
| Secret inspection | none |

The configured Goose file was not opened. No environment credential values,
tokens, private files, or provider responses containing secret material were
inspected or committed.

## 3. Executable probe

The bounded command used the installed CLI with `--no-profile`, built-in
`summon` and `developer` capabilities, `--no-session`, JSON output, and a
six-turn limit. The parent instruction required three independent subtasks:

1. Worker A writes a harmless marker file with UTC timestamps.
2. Worker B writes a separate harmless marker file with UTC timestamps.
3. Worker C reports a controlled failure without modifying files.

The first run launched the delegated tasks asynchronously but the workers had
no filesystem capability. It still directly observed three child identities
and a controlled failure, but A/B could not perform their requested writes.
That was classified as an environmental/tooling failure, not success.

The single bounded retry enabled the developer capability. The parent emitted
three asynchronous `delegate` requests before loading any result:

| Worker | Observed child session | Observed outcome |
| --- | --- | --- |
| A | `20260907_13` | completed; marker file reported created |
| B | `20260907_12` | completed; marker file reported created |
| C | `20260907_11` | controlled failure; no files modified |

The parent then loaded all three child results and returned a structured
aggregate with `concurrency_directly_evidenced: true`.

The run proves asynchronous delegated execution and aggregation. It does not
prove that the three workers were scheduled by an Apex-compatible dependency
planner, nor does it prove a production-safe workspace isolation boundary: the
parent process was launched from `/private/tmp`, so the delegated working
directory was observed as `/private/tmp` rather than the unique temporary
directory created by the harness wrapper. No repository files were touched.

## 4. Capability classification

| Capability | Classification | Direct evidence / boundary |
| --- | --- | --- |
| Parent delegates multiple independent subtasks | `PROVEN` | Three `delegate` calls were emitted in one parent turn; each returned a child session identity. |
| True concurrent/asynchronous execution | `PROVEN` | Each call used `async: true`; all three background tasks were started before parent `load` calls. |
| Distinct subagent/session identity | `PROVEN` | Child IDs `20260907_13`, `20260907_12`, and `20260907_11` were returned by Goose. |
| Result aggregation | `PROVEN` | Parent loaded each child and returned a combined JSON outcome. |
| One failure while unrelated work continues | `PROVEN` | Worker C failed by instruction while A and B completed independently. |
| Retry/rework | `PARTIAL` | A bounded parent-level retry corrected an environmental capability gap; child-task retry semantics and durable rework identity were not exposed. |
| Individual cancellation | `NOT_PROVEN` | The observed `load` schema included a `cancel` field, but no child was cancelled and no cancellation outcome was executed. |
| Dependency sequencing | `NOT_SUPPORTED` | The observed `delegate` arguments exposed no dependency/predecessor field; prompt ordering would be semantic instruction only. |
| Per-subtask provider assignment | `NOT_SUPPORTED` | The observed `delegate` arguments exposed no provider or model field; CLI provider/model options are parent-run options. |
| Per-subtask model assignment | `NOT_SUPPORTED` | No child-level model selector was present in the machine-readable delegation calls. |
| Isolated delegated workspace | `PARTIAL` | Workers were constrained by instruction and did not touch the repository, but the invocation used `/private/tmp` rather than the unique wrapper directory. |
| Apex semantic verification ownership | `NOT_PROVEN` | The probe only observed Goose outcomes; no Apex semantic result was assigned. |

## 5. Suitability for Apex

### Suitable with an Apex-owned boundary

The evidence supports this bounded composition:

```text
Apex Development Control Plane
        ↓
Goose CLI executor adapter
        ↓
Goose delegated workers
```

The Apex layer must retain canonical task decomposition, dependency order,
resource claims, attempt/rework identity, cancellation policy, authority,
verification, and semantic success. Goose may receive one immutable executor
projection, launch bounded workers, report opaque child identities and facts,
and return an aggregate observation. Goose's parent session, background task
IDs, prompts, and transcript remain adapter evidence rather than Apex
development truth.

### Not established by this probe

- general parallel scheduling safety;
- durable child-task recovery after parent/controller loss;
- child-level cancellation guarantee;
- dependency-aware execution;
- per-subtask provider/model assignment;
- Apex resource isolation or authority binding;
- independent verification of delegated work.

## 6. Reconciliation and status discipline

No architecture document or architecture status was changed. In particular,
the probe does not alter any Core `NOT_PROVEN` authority, recovery, fencing,
lease, checkpoint, event-ordering, or semantic-verification claim.

Task `AC-DEV-011` may be marked `DONE` with `verification_status: VERIFIED`
and `evidence_status: PARTIAL`: the development probe completed, while the
capability matrix retains its partial and unproven cells. `AC-DEV-010` remains
the deferred global event-ordering task and is not replaced by this probe.

## 7. Reproducibility boundary

The relevant executable surface can be rechecked without opening Goose
configuration:

```sh
/Users/msl/.local/bin/goose --version
/Users/msl/.local/bin/goose run --help
/Users/msl/.local/bin/goose run --no-profile --with-builtin summon,developer \
  --no-session --output-format json --max-turns 6 --text '<bounded probe prompt>'
```

Any future rerun must pass an explicitly unique working directory to the
delegated tool and verify the resulting marker paths before classifying
workspace isolation as `PROVEN`.
