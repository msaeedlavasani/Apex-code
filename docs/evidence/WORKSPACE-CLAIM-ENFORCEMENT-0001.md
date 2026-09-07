# Workspace Claim Enforcement 0001

Status: `PROPOSED` implementation evidence. This is bounded single-workspace
ownership for the current slice, not a general `ResourceLease` guarantee.

## Implemented behavior

`ExecutionCoordinator.run_artifact_task()` now acquires the existing Core
exclusive resource primitive for `workspace:<resolved-workspace>` after the
Attempt start fence and before authority release or runtime execution. A
second owner is rejected by the atomic ledger claim operation.

For a known terminal runtime fact (`EXITED`), Core releases the owning claim
only after result processing. Release is owner-checked and idempotent. If the
adapter returns an uncertain/non-terminal fact or the pipeline fails before a
known terminal observation, the claim is retained rather than guessed safe;
this preserves fail-closed behavior for future reconciliation.

The claim record carries a stable claim identity, Attempt identity, immutable
Manifest identity, resource name, exclusivity, and lifecycle timestamps. Claim
and release are represented by the common versioned event envelope.

## Validation

The 18-test standard-library suite passed. The bounded vertical-slice tests
now assert that a successful artifact run leaves exactly one workspace claim in
`RELEASED` state, while the reconciliation suite continues to prove conflict
rejection and stale-claim fail-closed behavior.

Documentation validation and `git diff --check` passed.

## Limits

This change does not prove distributed or multi-controller ownership, lease
renewal, wall-clock expiry, stale reclaim, controller-loss resource recovery,
or arbitrary external-resource locking. Those remain `NOT_PROVEN` and are not
implemented here.
