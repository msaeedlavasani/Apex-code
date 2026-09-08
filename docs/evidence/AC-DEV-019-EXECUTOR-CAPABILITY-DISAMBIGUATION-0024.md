# AC-DEV-019 — Executor Capability Disambiguation Proof

Status: `VERIFIED` control-plane task; capability evidence remains `NOT_PROVEN`
for both Goose and Freebuff

Task: `AC-DEV-019`

Evidence date: 2026-09-08 (Asia/Tehran)

## Result

The current AC-DEV-018 ambiguity is resolved by bounded operational evidence,
not by policy tie-breaking. The required capability is
`agent.definition_catalog`: discoverable native agent definitions with stable
runtime identity. Neither candidate produced an operational catalog or stable
named native definition in an isolated local probe. Both registry mappings are
therefore reconciled from `PARTIAL` to `NOT_PROVEN`.

AC-DEV-017 now returns `BLOCKED_REQUIRED_CAPABILITY`, and AC-DEV-018 now
returns `BLOCKED_CAPABILITY` with reason
`REQUIRED_CAPABILITY_UNAVAILABLE:agent.definition_catalog`. This is not
`BLOCKED_AMBIGUITY`: there are no compatible candidates. The default admission
policy remains unchanged; `SOURCE_ID_ASC` was not used.

## Canonical acceptance boundary

Acceptance requires direct runtime evidence of at least one stable named native
agent definition through an executor catalog/list operation or an equivalent
stable runtime enumeration. The following are deliberately insufficient:

- a UI label such as `@agents` or a parent model picker;
- source symbols such as `AgentDefinition`, `spawn_agents`, or `summon`;
- documentation or a source harvest;
- a skill catalog, which is a different capability;
- an agent self-report without a runtime identity-bearing catalog observation.

## Independent operational evidence

| Executor | Disposable probe | Direct observation | Claim |
|---|---|---|---|
| Goose CLI 1.49.0 | Isolated profile; `goose recipe list` and `goose skills list` | `recipe list` completed with an empty catalog. `skills list` returned `goose-doc-guide` and `web-search`, explicitly classified as a non-target skill catalog. | `NOT_PROVEN` |
| Freebuff CLI 0.0.170 | Isolated `--cwd`; bounded parent session with `@agents` input and harness termination | Public CLI exposed no catalog/list command. The parent session produced no stable named native agent entry. | `NOT_PROVEN` |

The machine-readable probe receipt is
[`AC-DEV-019-OPERATIONAL-PROBE-0024.json`](AC-DEV-019-OPERATIONAL-PROBE-0024.json).
Prior source and advertised-surface observations remain source evidence only;
they were not upgraded or reused as operational proof.

## Matching and admission reconciliation

The registry is revision 2. The only changed mappings are:

| Source | Previous | Reconciled | Reason |
|---|---:|---:|---|
| `goose-cli` | `PARTIAL` | `NOT_PROVEN` | No isolated runtime agent-definition catalog; recipe absence and separate skills catalog do not satisfy the definition. |
| `freebuff-cli` | `PARTIAL` | `NOT_PROVEN` | No catalog/list command or stable named native agent entry in the bounded isolated session. |

The full machine-readable reconciliation receipt is
[`AC-DEV-019-RECONCILIATION-0024.json`](AC-DEV-019-RECONCILIATION-0024.json).

The rerun preserved these controls:

- candidate plan status: `BLOCKED_REQUIRED_CAPABILITY`;
- admission status: `BLOCKED_CAPABILITY`;
- `selection: null` and no selection rationale;
- `runtime_side_effects: false` and `dispatch_allowed: false`;
- `permanent_executor_selected: false`;
- default tie-break policy disabled and `SOURCE_ID_ASC` unused;
- repeated plan and decision outputs identical.

## Eligibility and autonomous run loop

AC-DEV-019 was eligible after its AC-DEV-018 dependency was verified. The
bounded control-plane run executed one generic-executor development attempt,
verified the evidence package, recorded `PARTIAL` task evidence (because the
capability itself remains unproven), and refreshed readiness. No incident,
owner gate, or eligible task remained; the run stopped with
`NO_ELIGIBLE_WORK`. The canonical backlog records AC-DEV-019 as
`DONE` / `VERIFIED` / `PARTIAL`.

No ECC installation, permanent executor selection, production dispatch, or
Apex Core architecture change occurred.
