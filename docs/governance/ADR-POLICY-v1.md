# Apex Code ADR Policy v1

Status: **PROPOSED**.

## When an ADR is required

Use `docs/adr/` for a durable decision with meaningful alternatives, cross-boundary consequences, contract impact, difficult reversibility, or an architecture-status change. Routine implementation choices and explanatory documentation do not need an ADR.

An ADR is mandatory for changing a `FROZEN` decision, introducing a new Core boundary, changing Public API semantics, changing authority/safety guarantees, selecting a Runtime Adapter Contract, or superseding an accepted architectural decision.

## Format

Use sequential `ADR-####-kebab-case-title.md` records with: status, date, decision owner, context, alternatives, decision, rationale, consequences, reversibility, affected contracts/modules, evidence, and supersedes/superseded-by links. Proposed records are not authority to implement.

Suggested statuses: `PROPOSED`, `ACCEPTED`, `SUPERSEDED`, `REJECTED`.

## Relationship to architecture status

Architecture documents describe the contract and `05-ARCHITECTURE-STATUS.md` records whether a major item is `FROZEN`, `FREEZE_CANDIDATE`, `PROPOSED`, `INFERENCE`, `UNKNOWN`, or `NOT_PROVEN`. An ADR records the decision process; it does not silently change the status table. The status owner and ADR decision owner must be named when a major item changes.

Frozen changes require the existing Architecture Change Policy: explicit frozen decision, rationale, affected contracts/modules, status update, evidence discipline, and explicit architecture review. `FREEZE_CANDIDATE` refinement requires rationale but is not automatically frozen. `NOT_PROVEN` cannot become proven through an ADR or documentation alone.
