# Provider / BYOK Productization Evidence — AC-PROVIDER-BYOK-PRODUCTIZATION-0013

Status: **CURRENT bounded desktop implementation evidence**

This record covers the first provider/model settings and secure local BYOK
seam. It does not change the frozen Apex execution contracts or establish
native substrate authority attestation.

## Source snapshots

| Surface | Revision / source | Observation |
| --- | --- | --- |
| OpenCode | `e207624c48159b03dbe17dbc8e51bbcf23e72df5` | Pinned source audit for OpenCode 1.18.25. |
| OpenWork | `different-ai/openwork`, ref `dev`, `24b811cbe2afcb460051b686f04e5c12550a6b8c` | Existing MIT shell pin; provider backend/session ownership remains outside Apex. |

The OpenCode audit inspected `packages/opencode/src/cli/cmd/run.ts`,
`models.ts`, `providers.ts`, `provider/provider.ts`, `provider/auth.ts`, and
`config/config.ts`, plus the JavaScript SDK server surfaces. The observed
control surface accepts provider/model references in `provider/model` form,
supports `--model`, and uses provider-specific environment metadata. The
implementation therefore uses an Apex curated catalog and adapter-side
materialization rather than exposing OpenCode config syntax in the UI.

## Implemented ownership path

```text
Desktop settings
  → non-secret Provider/Model selection
  → Electron safeStorage credential vault
  → private internal application-boundary sync
  → selected OpenCode RuntimeAdapter environment
  → Apex Core Task / Attempt / Manifest
  → Core verification and semantic result
```

The provider credential is not accepted by the public task endpoint and is not
part of the Core execution request. The Core manifest records only the
non-secret provider/model reference for Attempt provenance.

## Evidence matrix

| Requirement | Evidence | Classification |
| --- | --- | --- |
| Static provider registry | `apex_code/providers.py`, 38 Core tests | `PROVEN_BOUNDED` |
| Model selection validation | `validate_selection` and invalid-model unit test | `PROVEN_BOUNDED` |
| Selected credential only | `_safe_environment` implementation and unit test with ambient credential sentinel | `PROVEN_BOUNDED` |
| No renderer credential readback | preload bridge has save/delete/status/test only; desktop vault test | `PROVEN_BOUNDED` |
| Encrypted persistence | Electron `safeStorage` vault and persistence test | `PROVEN_BOUNDED` when OS-backed storage is available |
| Credential replacement/deletion | `ProviderVault` lifecycle test and bounded desktop bridge | `PROVEN_BOUNDED` |
| Bounded provider test | `OpenCodeRuntimeAdapter.test_connection`, redacted statuses, mocked deterministic test | `PROVEN_BOUNDED`; real provider result is environment-dependent |
| Provider in Attempt provenance | existing immutable `ExecutionManifest.model_selection`, application history projection | `PROVEN_BOUNDED` |
| No ambient fallback | explicit credential requirement plus sanitized desktop/runtime environments | `PROVEN_BOUNDED` |
| Exact provider activation inside OpenCode | no direct active-authority attestation observed | `NOT_PROVEN` |
| Real provider execution in this environment | no credential-bearing acceptance was run during implementation | `NOT_RUN` |

## Security checks

The implementation and tests preserve these outcomes:

- plaintext secret in repository: **NO**;
- plaintext secret in ledger, events, or artifact metadata: **NO**;
- plaintext secret in renderer storage: **NO**;
- plaintext readback API: **NO**;
- ambient provider fallback: **NO**;
- unselected provider credential in the OpenCode child environment: **NO**.

The test suite uses disposable sentinel values only and does not print them.
No real credential, provider response, or secret file was inspected or
recorded.

## UI and restart boundary

The OpenWork-derived renderer exposes provider, model, configured status, test,
save, replace, and remove controls only in the desktop container. The browser
bootstrap shell does not persist credentials. Desktop restart reloads the
encrypted vault state and re-synchronizes only the selected credential to the
new local service process; the renderer sees configured status and selection,
not plaintext.

## Remaining limits

This evidence does not prove exact `AuthorityRevision` activation/binding,
active-runtime reattachment, distributed fencing, stale lease reclamation,
checkpoint side-effect safety, global event ordering, or general semantic
verification. Provider selection remains product intent and is not advanced
routing.

## Authorized real-provider acceptance — 2026-09-07

The Owner confirmed that the credential was entered directly into the actual
Apex Code Desktop UI and saved successfully. The credential value was not
shared with Freebuff, ChatGPT, GitHub, the repository, or the evidence record.

```text
OWNER_LOCAL_UI_ENTRY: PASS
PROVIDER: OpenRouter
MODEL: OpenAI GPT-4o mini
CREDENTIAL_SAVED: YES
CREDENTIAL_STATUS: CONFIGURED
SECURE_STORAGE: OS_BACKED
CONNECTION_TEST: VALID (Owner-confirmed)
AUTOMATED_NATIVE_VISUAL_E2E: NOT_AVAILABLE_IN_CURRENT_ENVIRONMENT
```

### First real execution

Using the already running packaged desktop service and a disposable project
containing only a harmless `README.md`, the production Application Boundary
was used to select the project and submit the bounded report task. No provider
mock or direct runtime invocation was used.

| Field | Observed result |
| --- | --- |
| Task | `task_b59e6f1056374b4b` — Inspect README and create REPORT.md |
| Attempt | `att_da6a9adfaead461b` |
| Provider/model provenance | `openrouter/openai/gpt-4o-mini` |
| Runtime fact | `EXITED` |
| Artifact | `REPORT.md` |
| Core verification | `PASS` |
| Semantic result | `SUCCEEDED` |

The artifact was retrieved through the Application Boundary and its recorded
Attempt correlation and Core verification were present. No credential field,
header, prefix, suffix, or secret-derived value was returned.

### Full application restart and second execution

The packaged desktop process and its Apex service were terminated, then the
packaged application was relaunched. The desktop broker restored the selected
provider/model and reported `CONFIGURED`; the first Attempt, artifact, and
verification were recovered from the durable workspace ledger. A second
bounded summary task then completed without re-entering the credential:

| Field | Observed result |
| --- | --- |
| Task | `task_350699b385374a00` — Inspect README and create SUMMARY.md |
| Attempt | `att_07af7c8a82464a0c` |
| Provider/model provenance | `openrouter/openai/gpt-4o-mini` |
| Runtime fact | `EXITED` |
| Artifact | `SUMMARY.md` |
| Core verification | `PASS` |
| Semantic result | `SUCCEEDED` |

### Credential deletion and fail-closed behavior

Because native visual automation was unavailable in this environment, deletion
was exercised through the same production `ProviderVault` deletion seam after
the desktop was closed; the vault value was never read or emitted. After
relaunch:

```text
CREDENTIAL_STATUS: NOT_CONFIGURED
POST_DELETE_TASK: REJECTED
POST_DELETE_ERROR: provider credential is not configured
AMBIENT_FALLBACK: NO
```

The post-delete task was rejected before useful provider execution and did not
create a new artifact or semantic success. The selected non-secret provider /
model preference remained visible, but no credential was available to the
RuntimeAdapter.

### Secret-forensics result

The audit used structural checks only. It did not read, hash, print, or compare
the credential value.

| Surface | Result |
| --- | --- |
| Repository | `NO` — no credential was entered into source or evidence. |
| Ledger/events | `NO` — durable records contain provider/model provenance only; no credential fields. |
| Logs | `NO OBSERVED` — the service uses quiet request logging and no credential-bearing log was produced. |
| Renderer storage | `NO` — renderer has no credential readback and no credential persistence path. |
| Screenshots | `NOT_AVAILABLE` — native visual automation was unavailable; no screenshot containing a credential was captured. |
| GitHub | `NO` — the credential was not entered into GitHub or CI. |

### Final acceptance classification

```text
REAL_PROVIDER_CREDENTIAL: AUTHORIZED
REAL_CONNECTION_TEST: PASS (Owner-confirmed)
REAL_PROVIDER_EXECUTION: PASS
REAL_OPENCODE_EXECUTION: PASS
CORE_VERIFICATION: PASS
SEMANTIC_SUCCESS: PASS
REAL_PROVIDER_PROVENANCE: PASS
DESKTOP_RESTART_CREDENTIAL_PERSISTENCE: PASS
POST_RESTART_PROVIDER_EXECUTION: PASS
CREDENTIAL_DELETE: PASS
AMBIENT_FALLBACK_AFTER_DELETE: NO
PLAINTEXT_SECRET_LEAK: NO OBSERVED
SECOND_PROVIDER_CONFORMANCE: PASS (deterministic; no second live credential used)
```
