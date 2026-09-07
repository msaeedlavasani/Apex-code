# OpenWork Thin-Fork Boundary v2

Status: **CURRENT bounded thin-fork integration**

This document records the actual OpenWork source adopted by the Apex Product
Shell. The shell is a replaceable projection and command surface; Apex Core,
not OpenWork, remains authoritative for execution, authority, verification,
artifacts, and durable history.

## Upstream pin and license boundary

- Repository: [`different-ai/openwork`](https://github.com/different-ai/openwork)
- Ref: `dev`
- Commit: `24b811cbe2afcb460051b686f04e5c12550a6b8c`
- Observed workspace version: `0.0.0-dev`
- Observed workspace package manager: `pnpm@11.4.0`
- License boundary: the selected shell files are MIT-covered. The upstream
  `ee/` tree is separately marked `LicenseRef-OpenWork-EE` and is excluded.
- Preserved notice: `product_shell/openwork/LICENSES-MIT.txt`

No Enterprise Edition source, credentials, provider configuration, or
OpenWork server database is included in Apex.

## Thin-fork method

`COPIED_PINNED_MIT_SHELL_SLICE` is the selected method. The source is present
under `product_shell/openwork/`, retains the relevant upstream package shape,
and is pinned to one inspectable revision. A small source slice keeps the
shell build reproducible without importing OpenWork's server, database,
cloud, telemetry, or direct runtime graph into Apex.

Alternatives rejected for this bounded slice:

- A full monorepo vendor would import unrelated runtime/server and Enterprise
  boundaries and would make the Apex/Core boundary opaque.
- A submodule would not provide a usable shell build without making the
  external checkout an implicit repository dependency.
- A remote-only relationship would not satisfy the requirement that the
  adopted source be present and reviewable in Apex.
- A dedicated fork lineage remains possible upstream, but is unnecessary
  until the selected MIT shell slice grows beyond this bounded integration.

## OpenWork thin-fork map

| Upstream surface | Treatment | Apex use and boundary | Sync / license basis |
| --- | --- | --- | --- |
| `apps/app/src/react-app/shell/ui-state-store.ts` | `FORK_THINLY` | Copied to `product_shell/openwork/src/openwork/ui-state-store.ts`; owns presentation layout only. | MIT; compare file-level changes at every pin update. |
| `apps/app/src/react-app/shell/workspace-shell-layout.ts` | `FORK_THINLY` | Copied to `product_shell/openwork/src/openwork/workspace-shell-layout.ts`; owns pane sizing/toggle behavior only. | MIT; rebase the narrow source slice when upstream changes. |
| `apps/app` routes and task/session surfaces | `ADAPT_BEHIND_APEX_SEAM` | The Apex shell uses the OpenWork workspace/sidebar/history shape but calls `/api/*` on the Apex Application Boundary. | MIT portions only; do not import direct runtime paths. |
| `apps/desktop` | `ADAPT` | Desktop lifecycle was audited but not imported; Apex uses a smaller Electron container in `product_shell/desktop/`. | OpenWork desktop source is MIT-adjacent in selected paths, but its server/runtime graph is excluded; preserve this bounded map. |
| `apps/server` | `REJECT` as canonical server | OpenWork server/session/database/runtime ownership is not Apex truth. | Do not copy into Core or use as the execution authority. |
| `@openwork/sdk` | `DEFER` | Not needed by the current local application seam. | Reconsider only with a bounded adapter review. |
| `@openwork/types` | `ADAPT_BEHIND_APEX_SEAM` | UI concepts may inform presentation types, but Apex frozen Task/Attempt/Manifest types remain canonical. | Do not leak OpenWork runtime/provider types into Core. |
| `@openwork/headless-threads` | `REJECT` for this slice | OpenCode/session transport remains behind Apex RuntimeAdapter. | No upstream session state becomes Apex execution truth. |
| OpenCode/MCP/provider surfaces | `DEFER` | Existing Apex default OpenCode composition remains the runtime path. | Provider UI is not expanded in this mission. |
| `ee/` and Enterprise-only packages | `REJECT` | Not imported or required. | `LicenseRef-OpenWork-EE`; excluded. |

## Apex integration boundary

```text
OpenWork-derived React shell
        ↓
Apex local HTTP Application Boundary
        ↓
Apex Core / ExecutionCoordinator
        ↓
Authority barrier → RuntimeAdapter → OpenCode
```

The shell may query project, status, history, and verified artifacts, and may
submit the bounded report/summary command. It must not create runtime sessions,
mutate Task or Attempt state, bind a RuntimeLane, override a ResourceClaim,
mark semantic success, or write the ledger as if it were Core.

OpenWork's direct OpenCode, session, MCP, and server paths are **BYPASSED** for
canonical Apex execution. They remain **NON_CANONICAL** reference surfaces;
they are not imported into the shell's execution path.

## Apex-specific divergence register

| Divergence ID | Upstream path | Apex path | Change / reason | Owner | Frozen contract protected | Removal or rebase condition |
| --- | --- | --- | --- | --- | --- | --- |
| OW-APEX-0009-01 | `apps/app/.../shell/ui-state-store.ts` | `product_shell/openwork/src/openwork/ui-state-store.ts` | Preserve OpenWork presentation persistence without adopting its session/runtime state. | Product Shell | Core Task/Attempt/Manifest and semantic completion | Rebase when upstream layout state changes; keep Core boundary. |
| OW-APEX-0009-02 | `apps/app/.../shell/workspace-shell-layout.ts` | `product_shell/openwork/src/openwork/workspace-shell-layout.ts` | Reuse workspace pane behavior in a dependency-light shell. | Product Shell | Product Shell non-authority | Rebase when upstream layout contract changes. |
| OW-APEX-0009-03 | OpenWork app/server runtime paths | `ApexOpenWorkShell.tsx` → Apex `/api/*` | Replace direct OpenWork runtime/session ownership with the Apex Application Boundary. | Apex Application Boundary | RuntimeAdapter, authority, ResourceClaim, EventEnvelope | Remove only when an equivalent bounded Apex seam is retained. |
| OW-APEX-0009-04 | OpenWork desktop lifecycle | `apex_code/shell.py --ui openwork` | Serve the built shell from the local Apex process; defer Electron packaging. | Product Shell | No Core frontend dependency | Revisit for an approved desktop distribution target. |

## Desktop adoption map — AC-DESKTOP-MVP-PACKAGING-0010

The pinned OpenWork `apps/desktop` source was audited at the same upstream
commit. It bundles OpenWork server/database/runtime/session ownership, direct
OpenCode sidecars, updater/telemetry, and Enterprise-adjacent package paths.
Those responsibilities are **REJECTED** for Apex's canonical desktop path.

| Upstream path / surface | Treatment | Apex destination | License / attribution | Sync handling |
| --- | --- | --- | --- | --- |
| `apps/desktop/electron/main.mjs` | `REIMPLEMENT_SMALL` | `product_shell/desktop/src/main.mjs` | No upstream source reused; no attribution required. | Re-audit lifecycle changes before any future reuse. |
| `apps/desktop/electron/preload.mjs` | `REJECT` | `product_shell/desktop/src/preload.cjs` | No upstream source reused. | Keep the bridge limited to desktop-native concerns. |
| `apps/desktop/electron-builder*.yml` | `REJECT` | `product_shell/desktop/electron-builder.yml` | No upstream source reused. | Maintain Apex-specific resource layout and unsigned target policy. |
| OpenWork desktop server/runtime startup | `REJECT` | Apex Python service launched on loopback | No source reused. | Never import OpenWork server/database/runtime authority. |
| Electron window/container concept | `ADAPT` | `product_shell/desktop/` | Conceptual learning only. | Compare lifecycle/security behavior at sync review. |
| OpenWork Enterprise desktop paths | `REJECT` | None | `LicenseRef-OpenWork-EE`; none reused. | Permanently excluded unless separately authorized. |

The current desktop wrapper is a small Apex implementation, not a copied
OpenWork desktop fork. The shared renderer remains the actual OpenWork-derived
surface. Electron-specific dependencies remain under Product Shell and do not
enter `apex_code` or frozen contracts.

## Desktop lifecycle and security boundary

| Process | Owner | Allowed responsibility |
| --- | --- | --- |
| Desktop main | Electron container | Window lifecycle, single-instance lock, native folder picker, loopback service process. |
| Renderer | OpenWork-derived Product Shell | Projection and bounded commands through the Application Boundary. |
| Apex Application process | Apex Core boundary | Project validation, startup reconciliation, task command, history/artifact queries. |
| Runtime/OpenCode process | RuntimeAdapter | Substrate execution facts and raw bounded result only. |

The service is started with `--host 127.0.0.1 --port 0`; the renderer receives
only the selected loopback base URL through an isolated preload bridge. The
desktop allowlist excludes ambient credential-shaped environment variables.
The existing RuntimeAdapter performs its own stricter child-environment
sanitization. A second launch is refused by Electron's single-instance lock.

Desktop failure does not fabricate semantic state: service loss or renderer
loss leaves durable Core state to reconciliation, and uncertain work remains
fail-closed.

## Bootstrap shell disposition

The original `product_shell/index.html`, `app.js`, and `app.css` implementation
is retained as `KEEP_AS_TEST_HARNESS`. It is useful for lightweight API and
fail-closed regression checks, but `product_shell/openwork/dist` is now the
default Product Shell served by `python3 -m apex_code.shell`. The two shells
are not competing production authorities.

## Development and upstream sync procedure

1. Fetch the desired OpenWork revision without following a moving ref in the
   Apex build.
2. Inspect the upstream diff and license boundary; exclude `ee/` and any new
   non-MIT path.
3. Compare only the selected shell paths with the pinned source.
4. Copy/rebase the selected MIT slice into the sync branch and preserve the
   Apex integration seam.
5. Run `npm install`, `npm run typecheck`, and `npm run build` in
   `product_shell/openwork`.
6. Run Apex unit/integration tests, documentation validation, and
   `git diff --check`.
7. Run the browser smoke for success, process restart/history, and one
   fail-closed state.
8. Review the divergence register, open a protected PR, and merge only after
   required CI passes.

The current local commands are:

```text
cd product_shell/openwork && npm install && npm run build
python3 -m apex_code.shell --ui openwork
```

The bootstrap harness remains available with `--ui bootstrap`.

## Explicit non-goals and unresolved boundaries

This adoption does not freeze or prove native runtime authority activation,
active-runtime reattachment, distributed fencing, stale lease reclamation,
checkpoint safety, global event ordering, or general semantic verification.
OpenWork replaceability and the DPT/Orchestration-optional boundary remain
unchanged.
