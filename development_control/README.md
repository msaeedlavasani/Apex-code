# Development Control Plane

This package is the executor-neutral development workflow control plane for
Apex Code. It schedules Development Tasks and records development Attempts; it
does not implement Apex Core execution, runtime authority, verification, or
semantic success.

## Canonical inputs

- Backlog: `development_control/backlog.json`
- Passports: `development_control/passports/AC-DEV-*.json`
- Runtime state: caller-supplied durable JSON path
- Contract: `docs/governance/DEVELOPMENT-CONTROL-PLANE-v1.md`

## Minimal use

```python
from pathlib import Path

from development_control import ControlPlaneStore, DevelopmentControlPlane

store = ControlPlaneStore(
    Path("development_control/backlog.json"),
    Path("development_control/passports"),
    Path(".control-plane/state.json"),
)
plane = DevelopmentControlPlane(store, executor_id="generic-executor")
summary = plane.run(executor, concurrency=1)
```

An executor receives a task projection and its Passport and returns an outcome
projection. It cannot directly assign Apex Core semantic state. Every
development execution gets a distinct Attempt ID. Use `select_batch()` and
`verify_batch()` when a caller needs explicit phase control; use `run()` for
the bounded autonomous loop.

The seeded backlog is repository evidence, not permission to claim unresolved
guarantees. `NOT_PROVEN`, `UNKNOWN`, and `NOT_RUN` remain visible. The Goose
UI/Desktop parallel-delegation item (`AC-DEV-007`) was later evaluated in
`GOOSE-UI-DELEGATION-0015`; its task is verified with `PARTIAL` evidence, while
the unproven UI capabilities remain explicitly unproven.

Owner-authorized material tasks are admitted only when the canonical backlog
records `owner_authorized: true`; this is task-specific authorization and does
not lower task risk or change Passport constraints. The Goose CLI
parallel-delegation probe is tracked separately as `AC-DEV-011`; `AC-DEV-010`
retains its original global event-ordering identity. `AC-DEV-012` records the
bounded Freebuff CLI probe: the parent TUI and advertised agent surface are
observed, while child delegation and most operational capabilities remain
`NOT_PROVEN`. `AC-DEV-013` compares the two executor candidates without
selecting a permanent executor. ECC is not installed.
