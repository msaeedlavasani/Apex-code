# OpenWork Integration Boundary

Status: **CURRENT bounded integration**

This document records the first Apex Product Shell boundary against the pinned
OpenWork reference. It does not make OpenWork Apex identity, a permanent
dependency, or a runtime authority.

## Upstream pin

- Repository: [`different-ai/openwork`](https://github.com/different-ai/openwork)
- Ref inspected: `dev`
- Commit: `24b811cbe2afcb460051b686f04e5c12550a6b8c`
- Version: `0.0.0-dev` in the workspace packages at the inspected revision
- License boundary: root license describes MIT portions and an OpenWork
  Enterprise Edition boundary under `ee/`; the repository also contains
  `LICENSES/MIT.txt` and `LICENSES/LicenseRef-OpenWork-EE.txt`. No OpenWork
  source is copied into Apex by this slice.

## Surface map

| OpenWork surface | Apex treatment | Boundary |
| --- | --- | --- |
| `apps/app` React application shell | ADAPT conceptually | Workspace/session navigation and projection patterns inform the local shell; Apex Core remains the source of truth. |
| `apps/desktop` Electron lifecycle | DEFER | Desktop packaging is not needed for the first local web shell. |
| `apps/server` and `@openwork/sdk` | DO NOT USE in this slice | Their server, database, and generated SDK graph would introduce a separate application/control-plane contract. |
| `@openwork/types` workspace/session types | ADAPT conceptually | Apex uses its own frozen Task/Attempt/Manifest and RuntimeAdapter contracts. |
| `@openwork/headless-threads` | DO NOT USE in this slice | OpenCode session transport remains behind Apex RuntimeAdapter; no upstream runtime state is adopted as Apex truth. |
| OpenCode/MCP/provider UI surfaces | DEFER | Provider configuration is not expanded; the bounded default OpenCode composition remains in Core's existing adapter path. |
| File/workspace/session views | ADAPT | The Apex shell exposes project identity, safe entry names, bounded task submission, result, and history. |

## Apex-specific divergences

| ID | Upstream file/package | Apex change | Architectural owner | Removal/rebase condition |
| --- | --- | --- | --- | --- |
| OW-APEX-0008-01 | `apps/app` shell and workspace routes | Use a small local web projection instead of importing the current React/Electron package graph. | Product Shell / Apex Application Boundary | Rebase onto an accepted OpenWork shell only when it can call the bounded Apex Application/API Boundary without moving Core ownership. |
| OW-APEX-0008-02 | `apps/server`, `@openwork/sdk` | Keep the local transport as a narrow HTTP query/command boundary backed by `ExecutionCoordinator`; no OpenWork server, database, or SDK dependency enters Apex Core. | Apex Application Boundary | Replace with a pinned upstream transport adapter if the same Core-owned semantics and fail-closed behavior are preserved. |
| OW-APEX-0008-03 | OpenWork runtime/session surfaces | Do not let shell session state become Apex Task, Attempt, RuntimeLane, authority, or semantic-success state. | Apex Core / RuntimeAdapter | Permanent upstream integration requires a separate contract review and evidence. |

This is a clean integration seam, not a completed upstream fork. Future sync
work must compare the pin above and revalidate each divergence before changing
the shell. Product Shell remains replaceable; OpenWork remains replaceable.
