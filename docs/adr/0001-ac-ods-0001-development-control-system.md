# ADR-0001 — AC-ODS-0001 Development Control System

Status: **ACCEPTED**
Decision owner: Apex Code Owner
Decision record: AC-ODS-0001
Date: 2026-09-07

## Context

Apex Code requires a development-control design before substantive product and
runtime implementation. The DCS harvest compared ApexAIPDT, Apex Home Fitness,
and BaziGB Modular Architecture. The BaziGB evidence discrepancy was resolved
before this record: the local dirty `feature/catan` checkout at
`f8fbf05b2683f73dace69d7912c80a584c190a0a` lacks the control-plane paths, while
fetched `origin/main@3dabbb6c80b1ad2ce7e27da57bdcc25b8aa1e5e3` contains and was
used to inspect them read-only.

## Decision

The Owner accepts AC-ODS-0001 D01–D20 as the direction for canonicalization:

| IDs | Accepted direction |
|---|---|
| D01–D03 | Development Task is separate from Core Task; Task Passport is its bounded revisioned contract; incomplete safe-execution information fails closed as `PASSPORT_INCOMPLETE`. |
| D04–D07 | Materialize root `AGENTS.md` as agent-behavior contract (P0), accept `docs/CONTEXT-MAP.md`, accept bounded Current State (P1), and keep one authoritative active Work State owner; full Work Registry implementation is P2. |
| D08–D12 | Use lightweight workflow with separate milestone facts; keep Decision Class, Risk, and Resource Class as separate axes; use lowest responsible resource cost; use `PASS`/`FAIL`/`NOT_RUN`/`BLOCKED`; adopt System-First Correction. |
| D13–D15 | Use decision-only ADRs under `docs/adr/`; defer the full Repository Brain tree and machine Retrieval Manifest. |
| D16–D18 | Keep Work Registry, Passport, Current State, Handoff, Completion Report, and Evidence Report semantically distinct; require explicit branch retirement; keep DCS independent from optional DPT and Orchestration. |
| D19 | Resolve and preserve BaziGB source provenance before relying on its evidence. |
| D20 | Materialize `ROADMAP.md` as P0 Product/System Evolution documentation, distinct from active work and execution authority. |

The detailed field schemas and future machine artifacts remain **PROPOSED** or
the explicitly assigned priority/status in the DCS documents. Accepted
direction does not make runtime implementation exist.

## Consequences

Development governance can plan and review work without changing Apex Core
`Task`, `Attempt`, `ExecutionManifest`, `ExecutionEpoch`, or `AttemptResult`.
DPT and Orchestration may consume generic DCS contracts later, but neither is a
dependency of Apex Code Core or of the DCS itself. The next materialization
delta creates the accepted canonical documents; a later enforcement delta may
add deterministic checks only after those contracts exist.

## Evidence and limits

Harvest claims are recorded in
[`DEVELOPMENT-CONTROL-PATTERN-HARVEST.md`](../evidence/DEVELOPMENT-CONTROL-PATTERN-HARVEST.md)
with source/ref provenance. Existing Apex architecture status and evidence
vocabulary remain authoritative. In particular, authority materialization and
binding remains `NOT_PROVEN`; this ADR cannot upgrade it.

## Related records

- [`DEVELOPMENT-CONTROL-SYSTEM-v1.md`](../governance/DEVELOPMENT-CONTROL-SYSTEM-v1.md)
- [`DEVELOPMENT-CONTROL-GAP-ANALYSIS.md`](../evidence/DEVELOPMENT-CONTROL-GAP-ANALYSIS.md)
- [`ADR-POLICY-v1.md`](../governance/ADR-POLICY-v1.md)
- Next planned delta: AC-MASTER-DOCS (not started)
- Follow-up enforcement delta: AC-GOV-CI (not started)
