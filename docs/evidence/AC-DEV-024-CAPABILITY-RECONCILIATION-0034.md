# AC-DEV-024 — Projection-Aware Capability Requirement Reconciliation

Status: **PROVEN**

Evidence class: **OBSERVED_RUNTIME_EVIDENCE + RECONCILIATION_EVIDENCE**

AC-DEV-024 reconciles the AC-DEV-017/018 capability contract with the
Owner-approved AC-DEV-022 architecture boundary and the bounded operational
proof in AC-DEV-023. The native executor capability
`agent.definition_catalog` remains optional and is still `NOT_PROVEN` for
Goose and Freebuff. No source evidence, UI label, or Apex-owned projection
proof promotes that native claim.

## Reconciled minimum contract

The AC-DEV-018 Passport now requires these four `PROVEN` guarantees:

- `execution.definition_projection`
- `execution.attempt_identity_binding`
- `execution.fail_closed_invocation`
- `execution.result_transport`

They are provided by the task-scoped Apex-owned projection contract evidenced
by AC-DEV-023. The generic execution substrate consumes a bounded payload; it
does not own AgentDefinition identity, the native catalog, Apex authority,
verification, retry/recovery, or semantic success. The native catalog remains
an explicit optional requirement for environments that independently prove it.

## Matching and admission

AC-DEV-017 was rerun twice against registry revision 3 and the AC-DEV-018
Passport revision 2. Every required bounded-invocation capability matched the
single `apex-owned-projection` capability source. AC-DEV-018 was safely
`ADMITTED` with a task-scoped candidate selection; this is not a permanent
executor selection and did not dispatch runtime work.

The admission decision retained:

- `dispatch_allowed: false`
- `runtime_side_effects: false`
- `permanent_executor_selected: false`
- no `SOURCE_ID_ASC` tie-break
- Apex ownership of scheduling, authority, verification, retry/recovery, and
  semantic success

## Regression coverage

The focused tests prove that:

1. Goose and Freebuff native catalog claims remain `NOT_PROVEN`.
2. The approved projection path admits without executor-native catalog
   ownership.
3. Removing a genuine bounded-invocation capability blocks admission.
4. Identical Passport, registry, and policy inputs produce identical matching
   and admission output.

The receipt validator also checks the schema, claim vocabulary, secret safety,
current registry consistency, native-claim preservation, and admission policy.
Historical receipts at older registry revisions remain immutable and valid
when their claims still agree with the current registry; future revisions are
rejected.

## Durable artifacts

- [`AC-DEV-024-RECONCILIATION-0034.json`](AC-DEV-024-RECONCILIATION-0034.json)
- [`AC-DEV-023-ADAPTER-PROOF-0031.json`](AC-DEV-023-ADAPTER-PROOF-0031.json)
- [`AC-DEV-023-RECONCILIATION-0033.json`](AC-DEV-023-RECONCILIATION-0033.json)

No executor was permanently selected, ECC was not installed, and no runtime
work was dispatched.
