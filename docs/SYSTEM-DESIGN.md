# Apex Code System Design

Status: **PROPOSED** system-level composition map. Formal contracts remain in
the [architecture status](architecture/05-ARCHITECTURE-STATUS.md) and linked
architecture documents.

Reconciliation trace: [Architecture Reconciliation 0001](evidence/ARCHITECTURE-RECONCILIATION-0001.md)
and the [comparative harvest](evidence/AGENTIC-DEVELOPMENT-SYSTEMS-COMPARATIVE-HARVEST.md).

## Composition and dependency direction

```text
Product Shell
      ↓ Public API
Apex Execution Core
  ├── Authority and safety primitives
  ├── Events, artifacts, and verification
  ├── Reconciliation Loop
  ├── Recovery semantics
  └── Capability interfaces
      ↓ Runtime Adapter Contract
OpenCode / Goose / future runtime substrates

Projection Layer (non-authoritative)
      ↑ Public API / Events / canonical Core state

Optional consumers/extensions above Core:
Orchestration · DPT · Advanced Routing · Advanced Verification · Advanced Recovery
```

The strict dependency direction is optional capabilities → Apex Core → Runtime
Adapter API → runtime substrates. OpenWork-derived shell technology and
OpenCode are replaceable boundaries, not Apex identity. Core owns
runtime-neutral semantics and RuntimeLane abstractions; adapters translate
substrate facts; substrates own native sessions/processes.

## Flows

- Control: a Public API command targets the `Execution` aggregate; Core owns
  command semantics, idempotency, receipts, state transitions, authority, and
  barrier release.
- Data: `ExecutionRequest` becomes an `Execution`, Core Tasks, Attempts, and one
  immutable `ExecutionManifest` per Attempt. Results, artifacts, verification,
  and Events remain distinct records.
- Authority: a `PermissionEnvelope` and immutable `AuthorityRevision` are
  materialized and checked for the relevant epoch/lane/Attempt before actual
  execution. The complete implementation guarantee remains `NOT_PROVEN`.
- Reconciliation: Core compares durable Attempt state, Runtime Adapter facts,
  authority/barrier state, and RuntimeLane/resource ownership. Startup and
  controller-loss cases are classified rather than inferred as success; stale
  `RUNNING`, missing/orphaned lanes, duplicate-start risk, and
  `UNREACHABLE`/`UNKNOWN`/`LOST` conditions may require recovery.
- Extension: capabilities consume Public API/Core/DCS contracts through
  explicit interfaces; they do not replace Core primitives.
- Failure: optional capability failure is isolated from Base Apex Code where
  the applicable contract permits; substrate failure is reported as adapter
  facts and interpreted by Core rather than silently becoming Task success.

## Projection boundary

The Projection Layer is a proposed non-authoritative boundary for task, attempt,
agent, dependency, failure, resource, verification, human-gate, and Event
views. It may support future visual or spatial experiences, but it never owns
canonical Apex state, authority truth, scheduler state, or semantic success.
Projection data may be stale, incomplete, duplicated, or rebuilt from Events;
commands that change state must go through the Public API/Core boundary.

See the [modular architecture](architecture/01-MODULAR-PRODUCT-ARCHITECTURE-v1.md),
[execution model](architecture/03-EXECUTION-MODEL-v1.md), and [execution API](architecture/04-EXECUTION-API-v1.md)
for authoritative detail.
