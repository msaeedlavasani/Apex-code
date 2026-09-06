# Apex Code Product

Status: **PROPOSED** product definition grounded in the accepted architecture.

## Definition and users

Apex Code is a standalone competitive product for controlled agent execution.
It serves people and teams who need agent work to be bounded by explicit
authority, observable through events/transcripts/artifacts, verifiable beyond a
runtime completion signal, and portable across runtime substrates.

## Problems and Jobs To Be Done

Users need to:

- request agent work with an explicit scope and permission envelope;
- choose or supply provider/model credentials without being locked to one
  substrate or vendor;
- pause, resume, cancel, inspect, verify, retry, and audit execution;
- distinguish runtime facts, artifacts, verification, and semantic success;
- recover safely when a runtime or optional capability fails.

The core job is: “Run useful agent work under authority I can understand,
observe, and control.”

## Base experience and capability extensions

The Base Apex Code experience centers on the Public API and Apex Core:
Execution, Tasks, Attempts, immutable manifests, authority, barriers, runtime
adapter boundaries, events, artifacts, verification, and safe failure. Core
safety and integrity primitives are foundational and are not paywalled.

Runtime substrate flexibility begins with OpenCode and must preserve a future
path for Goose and other adapters. The Product Shell is a replaceable client
of the Public API.

Optional capabilities may include Orchestration, DPT, Advanced Routing,
Advanced Verification, and Advanced Recovery. Orchestration is independent of
DPT; both may evolve and consume Core/DCS contracts without becoming Core
dependencies. Optional capability failure must not unnecessarily disable Base
Apex Code.

## Differentiation and non-goals

Differentiation is the combination of controlled execution, explicit authority,
runtime neutrality, durable evidence, semantic verification, and transparent
extension boundaries. Apex Code is not OpenWork, OpenCode, Goose, or DPT. It is
not a mandatory DPT host, a provider-specific wrapper, or a promise that
documentation already proves runtime guarantees.

## Commercial transparency

Capability, entitlement, and commercial offering are separate dimensions.
Architectural Core does not mean a Commercial Free tier, and pricing plans do
not belong in architecture documents. Premium capabilities must be labeled
`Premium + Trial` from the start when trial access is offered. The Base/Core and
premium capability sets may both continue evolving.

## Success criteria

Product success requires useful agent work, explicit and enforceable authority,
observable execution, trustworthy verification, recoverable failure, substrate
flexibility, optional-capability isolation, clear commercial communication,
and evidence that distinguishes `CURRENT`, `TARGET`, `UNKNOWN`, and
`NOT_PROVEN`.
