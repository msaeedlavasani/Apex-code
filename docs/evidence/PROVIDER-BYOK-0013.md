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
