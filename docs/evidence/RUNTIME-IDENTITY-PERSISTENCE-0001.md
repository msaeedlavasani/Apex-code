# Runtime Identity Persistence 0001

Status: `PROPOSED` implementation evidence. This records adapter-native
identity correlation in the bounded ledger; it does not make substrate
reassociation or controller-loss recovery proven.

## Implemented behavior

The typed `RuntimeIdentity` (`session_id`, optional `process_id`, and optional
`adapter_instance_id`) is now persisted on the Attempt record after adapter
execution, included in the runtime-fact event and AttemptResult, and returned
as evidence by the bounded coordinator. It remains distinct from Apex
`attempt_id`; runtime-native identifiers never create or replace Attempt
identity.

`ReconciliationLoop` continues to support the existing session-only
observation form and, when a full native identity is supplied, compares every
identity component available on both sides. A mismatch becomes
`MISMATCH → RECOVERY_REQUIRED`; no reassociation or semantic success is
performed.

## Validation

The standard-library suite passed 19 tests, including persistence of a fake
adapter's session/process/adapter identity and a process-identity mismatch
reconciliation test. Documentation validation and `git diff --check` passed.

## Limits

The OpenCode process identity is not always exposed by its JSON output, so
missing optional components remain unknown rather than fabricated. This task
does not prove exact AuthorityRevision binding, controller-loss recovery,
distributed fencing, stale lease reclamation, checkpoint safety, or
independent semantic verification.
