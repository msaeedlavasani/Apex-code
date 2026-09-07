# Apex Provider and Credential Architecture

Status: **CURRENT bounded desktop MVP**

This document defines provider/model selection as product intent. It does not
make a provider, OpenCode, or a credential store part of Apex Core identity.

## Ownership

| Concern | Owner | Boundary |
| --- | --- | --- |
| Supported provider and model catalog | Apex Application/Product Shell | Non-secret curated metadata; extensible without changing Task semantics. |
| Current provider/model preference | Desktop provider broker and Application Boundary | Non-secret selection only. |
| Credential persistence | Electron desktop main process | macOS Electron `safeStorage`; renderer receives status, never plaintext. |
| Credential resolution | Desktop main process | Resolves only the selected provider credential for a bounded internal call. |
| Execution provenance | Apex Core | The selected `provider/model` reference is recorded in the immutable Attempt manifest; no credential is recorded. |
| Runtime materialization | Runtime Adapter | Translates typed provider/model intent into isolated OpenCode configuration and a selected environment variable. |
| Semantic completion | Apex Core | Provider/runtime completion remains distinct from verification and semantic success. |

The renderer is a projection and command surface. It cannot read a stored
credential, mutate the ledger, start a runtime, or assign semantic success.

## Bounded provider model

The MVP uses these non-secret concepts:

- `ProviderDefinition`: stable provider id, display name, and supported model
  metadata.
- `ProviderConfiguration`: configured/not-configured state and non-secret
  selection metadata.
- `ModelDefinition`: provider-scoped model id and display label.
- `ModelSelection`: provider id plus model id, represented for execution as a
  provider/model reference.
- `CredentialReference`: an internal desktop-vault association; its secret
  value never enters an `ExecutionRequest`, `Task`, `Attempt`, manifest,
  event, ledger, artifact, renderer state, or log.

The current catalog is intentionally curated for OpenCode's provider/model
reference surface: OpenAI, Anthropic, and OpenRouter. Model discovery is not
performed through a provider call in the bounded MVP. A future catalog update
may add models without changing Core contracts.

## Secure credential lifecycle

The desktop broker supports `CREATE/SAVE`, `REPLACE`, `DELETE`, and
`CONFIGURED` status. It persists an encrypted blob in the Electron application
data directory using OS-backed `safeStorage` when available. The file contains
only the selection and encrypted credential blobs. The plaintext is held in
memory only while the desktop main process synchronizes or tests the selected
runtime configuration.

The preload bridge exposes only:

- `getProviderState`
- `setProviderSelection`
- `saveProviderCredential`
- `deleteProviderCredential`
- `testProvider`

There is deliberately no `readCredential` operation. Provider test failures
are reduced to bounded statuses such as `INVALID_CREDENTIAL`,
`PROVIDER_UNAVAILABLE`, `MODEL_UNAVAILABLE`, `RATE_LIMITED`, and
`NETWORK_ERROR`; raw provider responses are not returned.

## Runtime materialization

The desktop main process starts the loopback Apex service with a private,
per-launch internal token. It resolves the selected credential and sends it
once to an authenticated internal application-boundary operation. The Python
service retains it only in the selected adapter instance. The OpenCode adapter
constructs a fresh allowlisted child environment and adds only the selected
provider variable (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or
`OPENROUTER_API_KEY`). Ambient credential variables and unrelated user
configuration are excluded.

The runtime receives the selected non-secret model reference and a deny-all
Core-mediated tool configuration. It is not granted repository mutation
authority by this feature. Exact substrate-native authority activation and
binding remains `NOT_PROVEN` as recorded by the authority evidence.

## Application boundary

Public queries expose only catalog, selection, and configured status through
`GET /api/providers`. Credential-bearing operations are desktop-to-local-
service calls under `POST /api/internal/*`, authenticated by the private
per-launch token and not exposed as renderer commands. The browser/bootstrap
harness can display provider availability but does not persist or inject
credentials; product execution requiring OpenCode configuration is desktop
only.

## Defaults and provider addition

There is no silent ambient-key fallback. A desktop task requires an explicit
configured product credential. If none is configured, submission fails before
runtime start with a configuration error.

To add a provider:

1. verify the pinned OpenCode provider/model and credential surface;
2. add non-secret catalog metadata and the adapter environment mapping;
3. add redaction, selected-only environment, and bounded failure tests;
4. add the desktop settings projection without exposing the secret;
5. validate the provider through an explicitly authorized acceptance workflow;
6. preserve the RuntimeAdapter and Core ownership boundaries.

This is provider selection, not advanced routing. No fallback, cost policy,
or multi-provider scheduler is introduced.
