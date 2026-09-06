# OpenWork Feasibility Evidence

This document records evidence without treating upstream projects as Apex Code identity.

`OBSERVED_REPOSITORY_STATE`: this repository is currently architecture-first and pre-implementation; the baseline introduces documentation only.

## Labels

- `SOURCE_CODE_EVIDENCE`: supported by inspected source code.
- `DOCUMENTATION_EVIDENCE`: supported by project documentation.
- `OBSERVED_REPOSITORY_STATE`: directly observed repository condition.
- `OBSERVED_RUNTIME_EVIDENCE`: directly observed runtime behavior.
- `INFERENCE`: reasoned conclusion, not direct proof.
- `UNKNOWN`: insufficient information.
- `NOT_PROVEN`: the required guarantee was not established.

## Findings

| Question | Result | Evidence label | Boundary |
|---|---|---|---|
| Can an OpenWork-derived shell be used as a replaceable product shell? | FORK_RECOMMENDED | INFERENCE | Feasibility does not make OpenWork Apex Code identity. |
| Can independent OpenCode sessions run concurrently? | PASS | OBSERVED_RUNTIME_EVIDENCE | Runtime observation only; not a Core semantic guarantee. |
| Can authority be isolated across separate runtimes? | PASS | OBSERVED_RUNTIME_EVIDENCE | Applies to the observed setup, not all future adapters. |
| Is the full pre-execution authority materialization/binding chain proven? | NOT_PROVEN | NOT_PROVEN | Do not upgrade without direct evidence. |

These findings constrain confidence in integration choices; they do not authorize product implementation or introduce runtime guarantees.
