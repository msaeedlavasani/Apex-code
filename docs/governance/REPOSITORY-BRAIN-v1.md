# Apex Code Repository Brain v1

Status: **PROPOSED**.

## Recommendation

Adopt a lightweight repository-brain interface, but do not mechanically create seven duplicated brain files now. Before product implementation, create an Apex-native `AGENTS.md` as the behavior contract and add a substrate-neutral Context Map plus bounded Current State. Add domain brain documents only when a domain has durable rules, clear ownership, and a validation surface.

The brain is guidance and routing. Existing architecture documents remain authoritative for Core contracts; ADRs remain authoritative for decisions; governance documents remain authoritative for workflow. A brain must not copy those sources.

## Proposed minimum

| Brain/interface | Mandatory now? | Responsibility |
|---|---|---|
| `AGENTS.md` | P0 candidate | inspect/plan/execute/verify, scope, source precedence, secret safety, escalation |
| Context Map | P0 candidate | minimum-sufficient context routing and canonical read paths; prefer this substrate-neutral name over `AI_CONTEXT_MAP.md` |
| Current State | P1 candidate | bounded resume snapshot; never the backlog or history |
| Architecture | P0 candidate | route to existing architecture laws; identify contracts and freeze status |
| Engineering | P0 candidate | implementation/reuse/refactor/test behavior once code exists |
| Security | P0 candidate | secret, authority, dependency, and security-sensitive routing |
| QA | P0 candidate | validation tier selection and evidence interpretation |
| Product | defer until product requirements emerge | intent, outcomes, priorities, acceptance |
| Data | defer | data contracts, metrics, privacy-sensitive instrumentation |
| UX | defer unless a UI surface exists | interaction/accessibility/UI conformance |
| Operations | defer until deployable runtime exists | environments, reliability, rollback, observability |

## Contract

If introduced, each brain declares identity/version, responsibilities, non-responsibilities, authority, inputs, outputs, dependencies, validation, memory, and failure modes. This is adapted from DPT’s Brain Contract; role/team topology is not imported.

## Ownership and contradiction resolution

The repository owner assigns each brain’s maintainer. Updates link the canonical contract they affect. Contradictions follow `SOURCE-OF-TRUTH-v1.md`; a brain cannot override FROZEN architecture or convert `NOT_PROVEN` into proof. Brains are not ADRs, task passports, backlog records, or runtime manifests.

The BaziGB checkout did not contain the requested brain/context-map control-plane files, so this recommendation is based on its observed `AGENTS.md` discipline and audit evidence, not on a claimed BaziGB implementation of those artifacts.
