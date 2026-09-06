# Open Questions

The following remain open and are intentionally not resolved by this baseline.

1. What exact storage and event schema will preserve immutable manifests, authority revisions, receipts, and UNKNOWN states?
2. What is the precise state machine for Execution, Task, Attempt, barriers, verification, and cancellation?
3. How is authority materialized, bound, verified, and audited before every Attempt?
4. What adapter contract translates runtime facts without leaking runtime-specific semantics into Core?
5. How are RuntimeLane scheduling, session binding, resource claims, leases, and workspace snapshots coordinated?
6. What are the failure-isolation and degradation semantics when DPT, orchestration, or another optional capability fails?
7. Which capability discovery and entitlement checks are needed while keeping Capability, Entitlement, and Commercial Offering separate?
8. What evidence and conformance tests are required before each FREEZE_CANDIDATE becomes FROZEN?
9. Which OpenWork-derived shell components are retained, forked, or replaced, and under what license/compliance review?
10. What additional runtime substrates should be supported after OpenCode, and what is the minimum adapter conformance suite?

## Explicit non-claim

The authority materialization/binding chain is `NOT_PROVEN`. This document does not promote it to proven status by implication or by the PASS results for separate-runtime authority isolation.
