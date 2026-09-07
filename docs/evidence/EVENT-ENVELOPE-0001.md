# Event Envelope 0001

Status: `PROPOSED` implementation evidence. This is a bounded durable ledger
contract; it does not freeze the full public event API or make Events a source
of semantic authority.

## Implemented contract

`apex_code/events.py` defines a frozen `EventEnvelope` with:

- `event_id` and `event_type`;
- `schema_version` (currently `1`);
- `occurred_at`;
- a monotonic `sequence` within an `ordering_scope` (currently one ledger);
- optional `correlation_id` and `causation_id`;
- explicit references for Execution, Task, Attempt, ExecutionEpoch,
  AuthorityRevision, RuntimeLane, resource claim, and fence identities when
  present in the event payload; and
- the original event payload for bounded compatibility.

`ExecutionLedger.event`, durable attempt-fence acquisition, and resource-claim
acquisition all write this same envelope shape. Correlation defaults to the
nearest available Attempt, Task, or Execution identity, while explicit
correlation and causation values remain available to callers.

Atomic ledger mutations assign the next sequence number while holding the
ledger lock. This gives one ledger a deterministic local order for replay;
there is no claim of ordering across separate ledgers, machines, or future
distributed controllers.

The envelope records facts for audit, replay, and future projections. It does
not grant permission, choose semantic Task state, or replace Core commands.
Runtime facts remain adapter observations and Core remains the interpreter of
semantic success, failure, and recovery.

## Validation

The standard-library suite passed 17 tests, including envelope versioning,
reference extraction, correlation/causation preservation, and the existing
fencing, identity, reconciliation, resource-conflict, artifact-verification,
and runtime-completion tests. Documentation validation and whitespace checks
also passed.

This task does not claim to prove event ordering across processes, durable
replay compatibility across schema migrations, controller-loss reconciliation,
or any authority activation/binding guarantee. Those remain subject to the
existing `NOT_PROVEN` boundaries and future contract/experiment work.
