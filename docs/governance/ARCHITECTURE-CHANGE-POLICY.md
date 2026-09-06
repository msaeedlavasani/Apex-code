# Architecture Change Policy

This policy governs Apex Code architecture. It applies to the Core and its boundaries, and does not make DPT or orchestration part of Core; both remain optional capabilities.

## Status meanings

- **FROZEN**: a decision intentionally fixed as current architecture law.
- **FREEZE_CANDIDATE**: an accepted direction that remains subject to contract refinement.
- **PROPOSED**: not yet sufficiently designed or validated.
- **INFERENCE**: a reasoned conclusion rather than direct evidence.
- **UNKNOWN**: insufficient information.
- **NOT_PROVEN**: a required guarantee lacks direct evidence.

## Changing frozen decisions

A pull request changing a `FROZEN` architectural decision is not an ordinary documentation edit. It must:

1. Identify the frozen decision explicitly.
2. Explain the rationale for changing it.
3. Identify affected contracts and modules.
4. Update `docs/architecture/05-ARCHITECTURE-STATUS.md`.
5. Preserve the evidence labels and distinguish observation, inference, and lack of proof.
6. Receive explicit architecture review before merge.

`FREEZE_CANDIDATE` decisions require rationale and may evolve through contract refinement. That evolution must still preserve the documented invariants unless the pull request follows the frozen-decision process.

`NOT_PROVEN` must never be upgraded to proven solely by documentation edits. Direct evidence is required, and the evidence label must remain visible until the guarantee is established.
