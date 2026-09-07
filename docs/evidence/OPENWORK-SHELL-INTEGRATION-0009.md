# OpenWork Shell Integration Evidence — AC-OPENWORK-SHELL-RECONCILIATION-0009

Status: **CURRENT / bounded visual integration evidence**

This record covers the actual OpenWork-derived shell adoption. It does not
change Apex architecture or prove any of the unresolved runtime guarantees.

## Pinned source and audit

| Item | Evidence |
| --- | --- |
| Repository | `different-ai/openwork` |
| Ref | `dev` |
| Inspected commit | `24b811cbe2afcb460051b686f04e5c12550a6b8c` |
| Observed package version | `0.0.0-dev` |
| Selected source | `apps/app/src/react-app/shell/ui-state-store.ts`; `apps/app/src/react-app/shell/workspace-shell-layout.ts` |
| Apex destination | `product_shell/openwork/src/openwork/` |
| License | Selected files treated as MIT under the inspected repository boundary; `ee/` excluded |
| Build | `npm run typecheck` and `npm run build` passed |

The broader OpenWork application, server, SDK, headless-thread runtime, and
Enterprise tree were not imported. Direct OpenWork runtime/session paths are
bypassed and non-canonical for Apex execution.

## Bootstrap visual acceptance

Using isolated Chromium automation against a disposable project containing a
harmless `README.md`, the bootstrap shell visibly demonstrated:

- project/workspace identity and file surface;
- the bounded report task submitted through the shell;
- `SUCCEEDED`, runtime fact `EXITED`, Core verification `PASS`, and `REPORT.md`;
- history and artifact projection after browser reconnect;
- a seeded uncertain attempt displayed as `RECOVERY_REQUIRED`, with
  `NOT_OBSERVED` runtime and `NOT_RUN` verification rather than false success.

Result: `BOOTSTRAP_VISUAL_E2E = PASS`.

## OpenWork-derived visual acceptance

The built shell was served by `python3 -m apex_code.shell --ui openwork` and
driven through the rendered browser UI. The same disposable bounded report
task produced a Core-owned Task/Attempt path, an OpenCode `EXITED` fact, a
verified `REPORT.md`, and a visible semantic `SUCCEEDED` state. The process was
then stopped and relaunched; reopening the project showed the prior attempt,
artifact, and verification from the durable Core ledger.

The fail-closed visual case showed `RECOVERY_REQUIRED` for an uncertain
attempt, disabled task submission, no artifact, `NOT_OBSERVED`, and `NOT_RUN`.
No runtime was adopted and no retry was issued by the shell.

Result: `OPENWORK_DERIVED_VISUAL_E2E = PASS`.

The screenshots were captured in an isolated temporary browser workspace and
were not committed because they contain disposable local paths. The durable
claims above are backed by browser assertions and the existing Core tests.

## Core boundary confirmation

The shell uses the existing local HTTP Application Boundary for all commands
and queries. It does not create sessions, assign Task/Attempt state, bind
authority, override workspace claims, write the ledger, or assign semantic
success. The Apex Application Boundary delegates to Core, the existing
RuntimeAdapter, and OpenCode.

Frozen contracts were not changed. DPT and Orchestration remain optional and
independent. Native substrate authority activation/binding, active-runtime
reattachment, distributed fencing, stale lease reclamation, checkpoint safety,
global event ordering, and general semantic verification remain `NOT_PROVEN`.
