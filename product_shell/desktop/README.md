# Apex Code Desktop MVP

This package is the local desktop container for the OpenWork-derived Apex
renderer. Electron owns the window, native folder picker, single-instance
policy, and bounded local-service lifecycle. It does not own Apex execution
state, authority, verification, artifacts, or semantic success.

## Requirements

- macOS for the current packaged target (the observed machine is Intel
  `x86_64`)
- Python 3.14+ with the Apex checkout available
- Node.js 24.x and npm 11.x
- Electron 43.2.0 and electron-builder 26.15.3, installed by `npm ci`
- OpenCode available to the bounded Apex RuntimeAdapter

The package is development-quality and unsigned. It is not notarized or
distribution-ready. The packaged app expects `python3` and the bounded
OpenCode executable to be available on the host; neither is made a desktop
authority or hidden renderer dependency.

## Commands

From this directory:

```text
npm ci
npm run typecheck
npm test
npm run dev
npm run package:dir
```

`npm run dev` builds the shared OpenWork renderer, starts the local Apex
Application Boundary on `127.0.0.1` with an ephemeral port, and opens Electron.
`npm run package:dir` produces an unsigned macOS directory app under
`dist-electron/mac/Apex Code.app`.

The renderer can still be developed independently with:

```text
cd ../openwork
npm ci
npm run dev
```

## Lifecycle boundary

```text
Electron main process
  ├─ native folder picker / window lifecycle
  ├─ single desktop instance
  └─ bounded Python Apex service on 127.0.0.1
       ↓
OpenWork-derived renderer
       ↓
Apex Application Boundary → Apex Core → RuntimeAdapter → OpenCode
```

Closing the desktop stops only the local Apex application service. Durable
Core state remains on disk; uncertain Attempts are reconciled by Core on the
next project open. Renderer disappearance is not a Task or Attempt result.

For deterministic local UI smoke only, `APEX_DESKTOP_E2E=1` with
`APEX_DESKTOP_TEST_PROJECT=/absolute/path` makes the picker IPC return the
specified disposable fixture instead of opening the OS dialog. This hook is
not used in normal launches.
