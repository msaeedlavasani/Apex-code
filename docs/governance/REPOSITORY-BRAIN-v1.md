# Apex Code Repository Brain v1

Status: **PROPOSED**.

## Recommendation

Owner decision D14 defers the full Repository Brain tree. Before product implementation, materialize an Apex-native `AGENTS.md` as the behavior contract and `docs/CONTEXT-MAP.md` as the routing contract; bounded Current State is P1. Do not mechanically create domain brain files until canonical documentation demonstrates a durable, owned, non-duplicative need.

The brain is guidance and routing. Existing architecture documents remain authoritative for Core contracts; ADRs remain authoritative for decisions; governance documents remain authoritative for workflow. A brain must not copy those sources.

## Proposed minimum

| Brain/interface | Mandatory now? | Responsibility |
|---|---|---|
| `AGENTS.md` | P0 accepted documentation | how agents behave: entry, scope, plan/execute, validation, evidence, escalation, completion |
| `docs/CONTEXT-MAP.md` | P0 accepted design | minimum-sufficient context routing and canonical read paths |
| Current State | P1 accepted design | bounded resume snapshot; never backlog or history |
| Full domain brain tree | Deferred | reconsider only if retrieval/decision quality improves without duplication |
| Product | defer until product requirements emerge | intent, outcomes, priorities, acceptance |
| Data | defer | data contracts, metrics, privacy-sensitive instrumentation |
| UX | defer unless a UI surface exists | interaction/accessibility/UI conformance |
| Operations | defer until deployable runtime exists | environments, reliability, rollback, observability |

## Contract

If introduced, each brain declares identity/version, responsibilities, non-responsibilities, authority, inputs, outputs, dependencies, validation, memory, and failure modes. This is adapted from DPT’s Brain Contract; role/team topology is not imported.

## Ownership and contradiction resolution

The repository owner assigns each brain’s maintainer. Updates link the canonical contract they affect. Contradictions follow `SOURCE-OF-TRUTH-v1.md`; a brain cannot override FROZEN architecture or convert `NOT_PROVEN` into proof. Brains are not ADRs, task passports, backlog records, or runtime manifests.

The BaziGB local checkout lacked the requested files, but fetched `origin/main@3dabbb6c80b1ad2ce7e27da57bdcc25b8aa1e5e3` contains `AI_CONTEXT_MAP.md`, `ai/`, and `docs/aipde/`; those remote files provide direct evidence for routing and bounded-state patterns. Apex adopts the concept with a substrate-neutral name and defers the full brain tree.
