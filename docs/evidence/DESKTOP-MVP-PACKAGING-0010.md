# Desktop MVP Packaging Evidence — AC-DESKTOP-MVP-PACKAGING-0010

Status: **CURRENT / bounded local desktop evidence**

This is product-container evidence. It does not change Apex architecture or
upgrade any unresolved runtime guarantee.

## Desktop audit and adoption

| Item | Result |
| --- | --- |
| OpenWork source | `different-ai/openwork`, ref `dev`, commit `24b811cbe2afcb460051b686f04e5c12550a6b8c` |
| OpenWork desktop source reused | None; audited only |
| Desktop framework | Electron `43.2.0` |
| Packaging | electron-builder `26.15.3` |
| Current target | macOS `x86_64` directory app |
| Enterprise source | None reused |
| Core frontend dependencies | None |
| Signing/notarization | Not performed; development artifact only |

The wrapper is intentionally smaller than OpenWork's `apps/desktop`: it does
not bring in OpenWork server, database, direct OpenCode transport, updater,
telemetry, sidecars, or Enterprise modules.

## Runtime lifecycle

Electron starts `python3 -m apex_code.shell --ui openwork --host 127.0.0.1
--port 0` with a deterministic environment allowlist. The announced loopback
URL is health-checked before the BrowserWindow loads the renderer. Electron's
single-instance lock prevents a second controller. On quit, the service gets a
bounded graceful shutdown followed by a forced process stop if necessary;
durable ledger state remains Core-owned.

The renderer receives only the loopback API base and two native commands:
directory selection and platform information. It never receives credentials or
raw runtime configuration.

## Evidence runs

Desktop unit checks:

- service command uses loopback and an ephemeral port;
- remote host URLs are rejected by the helper contract;
- ambient `API_KEY` and `SECRET_TOKEN` variables are excluded from the desktop
  service environment;
- packaged/development resource roots are deterministic.

Real development Electron smoke, driven through the actual renderer:

1. Electron launched and displayed `READY`.
2. A disposable project with `README.md` opened.
3. `Inspect README.md and create REPORT.md` was submitted.
4. Apex Core created the Task/Attempt/Manifest path.
5. OpenCode returned runtime fact `EXITED`.
6. Core verification returned `PASS` and semantic state `SUCCEEDED`.
7. The app was fully closed, not merely refreshed.
8. A new Electron process relaunched and reconstructed the same attempt,
   `REPORT.md`, and verification from the durable ledger.

Result: `DESKTOP_E2E = PASS`.

The same run against the packaged `Apex Code.app` directory artifact passed
the launch, bounded task, Core verification, and full close/relaunch history
checks. The packaged app is unsigned and uses host `python3`/OpenCode; this is
not distribution proof.

A desktop fail-closed fixture containing an uncertain persisted Attempt
displayed `RECOVERY_REQUIRED`, `NOT_OBSERVED`, and `NOT_RUN`; the submit button
was disabled. No runtime was adopted and no retry was issued.

The native picker IPC bridge was exercised with a disposable deterministic E2E
path. The actual macOS folder dialog opened, but automated keystrokes were
blocked by the environment's Accessibility permission; the normal production
path remains `dialog.showOpenDialog` and the validated text-path fallback is
also retained for web development.

## Validation

- Apex tests: 32 passed
- desktop typecheck: passed
- desktop unit tests: 3 passed
- OpenWork renderer typecheck/build: passed
- packaged macOS directory artifact: produced
- documentation validation: passed
- `git diff --check`: passed

Frozen Core contracts, default runtime, DPT/Orchestration boundaries, and all
current `NOT_PROVEN` authority/recovery limits remain unchanged.
