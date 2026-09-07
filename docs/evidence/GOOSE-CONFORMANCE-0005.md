# Goose Conformance and Architecture Freeze Readiness — 0005

Status: `PROPOSED` evidence report. No architecture status is changed by this
document.

## 1. Executive result

Goose was installed in a disposable, user-local scope and its control-plane
surfaces were inspected at a pinned release/source revision. The probe
established a usable CLI/help surface, isolated configuration/data/state roots,
session persistence surfaces, ACP server surface, and configurable permission
levels. The isolated environment had no configured local provider, so a real
bounded Goose execution and an Apex adapter run could not be safely completed.

Result: `CROSS_SUBSTRATE_NOT_PROVEN`.

This is an environment/provider limitation, not evidence that Goose cannot be
adapted. No Goose dependency was added to Apex, and no architecture status was
upgraded.

## 2. Snapshot and provenance

| Item | Observation | Evidence |
| --- | --- | --- |
| Source repository | `aaif-goose/goose` | `OBSERVED_REPOSITORY_STATE` |
| Source ref | tag `v1.49.0` | `OBSERVED_REPOSITORY_STATE` |
| Source commit | `71fc4be1ed729e26b1dc0a4466abdd03be548a53` | `OBSERVED_REPOSITORY_STATE` |
| Binary | `goose` 1.49.0, x86_64 macOS release asset | `OBSERVED_RUNTIME_EVIDENCE` |
| Installation | official release tarball, temporary `/tmp` executable; no PATH/profile change | `OBSERVED_REPOSITORY_STATE` |
| License | root `LICENSE` identifies Apache-2.0; source reuse remains separately governed | `DOCUMENTATION_EVIDENCE` |
| Inspection date | 2026-09-07 (Asia/Tehran) | `OBSERVED_REPOSITORY_STATE` |
| Apex dependency | none | `OBSERVED_REPOSITORY_STATE` |

The source checkout and binary were not treated as byte-identical artifacts;
binary-to-source reproducibility was not established (`NOT_PROVEN`). The
disposable installation is removed after the experiment.

## 3. Source-level observations

The following observations are tied to commit
`71fc4be1ed729e26b1dc0a4466abdd03be548a53`:

| Goose path | Direct observation | Apex classification |
| --- | --- | --- |
| `crates/goose/src/config/paths.rs` | `GOOSE_PATH_ROOT` can relocate config, data, state, and agent/plugin roots to an absolute isolated path. | `ADAPTABLE` |
| `crates/goose/src/config/permission.rs` | Permission manager reads `permission.yaml`; levels include `AlwaysAllow`, `AskBefore`, and `NeverAllow`. | `PARTIAL` |
| `crates/goose/src/session/session_manager.rs` (`Session`) | Session has a string id, working directory, provider/model metadata, timestamps, and persistent storage backed by SQLite. | `ADAPTABLE`; not an Apex Attempt |
| `crates/goose-cli/src/cli.rs` | `run` supports non-interactive text/instruction input, `--no-session`, JSON/stream output, provider/model selection, resume/session identifiers, and bounded turns. | `ADAPTABLE` |
| `crates/goose-cli/src/session/mod.rs` | Non-interactive permission behavior depends on mode; confirmation-required actions are not silently auto-approved in conservative modes. | `PARTIAL`; not Apex authority proof |
| `crates/goose/src/acp/server.rs` and `crates/goose/src/acp/common.rs` | ACP server and session/protocol surfaces exist; ACP authentication has an explicit unauthenticated-development option. | `ADAPTABLE`; security review required |
| `crates/goose/src/execution/manager.rs` | Goose owns an agent execution manager and runtime context internally. | `SUBSTRATE_SPECIFIC_BUT_ADAPTABLE` |
| `LICENSE` | Apache-2.0 license text is present at source root. | conceptual learning allowed; code reuse review required |

These are direct source observations (`SOURCE_CODE_EVIDENCE`) and do not prove
that an Apex RuntimeAdapter can correlate Goose authority, process identity,
session identity, and Attempt identity before side effects.

## 4. Capability matrix

| Apex requirement | Goose primitive | Evidence | Classification |
| --- | --- | --- | --- |
| preparation/materialization | `GOOSE_PATH_ROOT`, config paths, permission file | `paths.rs`, `permission.rs`, isolated `info` probe | `ADAPTABLE` |
| authority/config digest correlation | config/permission files can be hashed externally | probe produced a harmless permission-file digest | `PARTIAL` |
| active authority attestation | no direct pre-start activation/binding attestation found | source inspection and probe | `NOT_PROVEN` |
| runtime identity | session id; process may be observed by host | `Session`, CLI session commands | `PARTIAL` |
| session/process binding | session persistence exists; exact process-to-session proof absent | source inspection | `NOT_PROVEN` |
| non-interactive execute | `goose run -t/-i`, `--no-session`, structured output | CLI help probe | `DIRECT` for surface; execution unproven |
| runtime fact | CLI exit/output/process observation can be mapped by an adapter | inferred adapter seam | `ADAPTABLE` |
| result retrieval | text/JSON/stream output and persisted session data | CLI and session source | `PARTIAL` |
| cancellation | ACP cancel protocol surface; CLI behavior not fully tested | ACP source | `PARTIAL` |
| config isolation | `GOOSE_PATH_ROOT` | source + runtime `info` output | `DIRECT` |
| filesystem/tool permissions | permission manager and extension/tool confirmation | permission/session source | `PARTIAL` |
| provider/model selection | CLI flags and environment/config resolution | CLI source/help | `DIRECT` |
| reconnect/resume | session `--resume`/`--session-id` surfaces | CLI help/session source | `PARTIAL`; recovery semantics unproven |
| Apex semantic success | none should be delegated to Goose | RuntimeAdapter contract | `WRONG_ABSTRACTION` if delegated |

## 5. Experimental runtime result

The probe used a fresh `GOOSE_PATH_ROOT` and removed credential-bearing
environment variables from the child environment. It requested an Ollama
provider solely to avoid credential creation or reuse. No Ollama executable or
local provider endpoint was available; the command produced a startup session
banner and did not yield a bounded artifact result within the safe timeout.

The command was terminated after the timeout. No secret or file content was
printed. This establishes only that the installed CLI entered its session path;
it does not establish model execution, tool execution, permission enforcement,
result correlation, or semantic completion.

The reproducible probe is
`experiments/runtime-conformance/goose/capability_probe.py`. Its JSON output
intentionally records return/timeout/presence metadata rather than raw Goose
output, preventing accidental transcript or secret leakage.

Classification: `SUBSTRATE_CAPABILITY_GAP` for this environment;
`NOT_PROVEN` for Apex cross-substrate conformance.

## 6. Adapter and dual-substrate assessment

No experimental Goose adapter was added because the only available execution
path lacked a provider and could not produce a real result. Therefore:

- OpenCode remains the only substrate that has passed the existing Apex
  conformance tests and bounded vertical-slice smoke.
- Goose contract execution: `NOT_RUN`.
- Same bounded task on Goose: `NOT_RUN`.
- Same bounded task on OpenCode: existing main evidence remains valid; no new
  OpenCode runtime experiment was needed for this blocked Goose comparison.
- No OpenCode-specific contract correction was justified by this probe.

The current adapter contract appears conceptually portable for preparation,
opaque identity, runtime facts, result transport, and Core-owned semantic
completion. Cross-substrate proof remains incomplete because Goose execution,
identity correlation, cancellation, and result/artifact verification were not
observed end to end.

## 7. Freeze-readiness recommendation

This is a recommendation only. Architecture status files remain unchanged.

| Contract | Recommendation | Evidence and limitation |
| --- | --- | --- |
| Task / Attempt / Manifest | `READY_TO_FREEZE` for bounded semantics | Existing Apex implementation/tests preserve distinct Task, Attempt, and immutable Manifest identities; Goose session is not treated as an Apex Task or Attempt. |
| RuntimeAdapter boundary | `KEEP_FREEZE_CANDIDATE` | OpenCode passes the current bounded contract; Goose surfaces are adaptable but not executed through the contract. |
| RuntimeFact vocabulary | `READY_TO_FREEZE` for bounded vocabulary | Existing contract closes facts to `RUNNING`, `EXITED`, `MISSING`, `UNREACHABLE`, `MISMATCH`, `UNKNOWN`; semantic success remains Core-owned. |
| Runtime identity/correlation | `KEEP_FREEZE_CANDIDATE` | OpenCode bounded identity is tested; Goose session/process correlation is `NOT_PROVEN`. |
| Core semantic completion | `READY_TO_FREEZE` for bounded artifact tasks | Existing Core verifier gates semantic success; runtime exit alone is insufficient. General semantic verification remains out of scope. |
| Authority / barrier | `KEEP_FREEZE_CANDIDATE` | Core-mediated barrier exists and fails closed; exact substrate activation and binding remain `NOT_PROVEN`. |
| Event envelope | `READY_TO_FREEZE` for bounded ledger scope | Existing typed/versioned durable events and local ordering are tested; global ordering remains unproven. |
| Workspace ResourceClaim | `READY_TO_FREEZE` for bounded single-controller workspace | Existing conflict rejection is tested; general leases and stale reclamation remain unproven. |
| Bounded independent verification | `READY_TO_FREEZE` | Existing Core artifact verifier is independent of adapter self-report for bounded fixtures. |
| Startup reconciliation | `KEEP_FREEZE_CANDIDATE` | Bounded startup classification exists; active-runtime controller-loss recovery and orphan guarantees remain `NOT_PROVEN`. |

Recommended boundary: freeze the bounded Core semantics and explicit
fail-closed interfaces when Owner governance accepts them, while retaining
substrate-specific authority attestation, active-runtime recovery, and
multi-controller guarantees as explicit extensions/experiments. Do not treat
this evidence report as a status upgrade.

## 8. NOT_PROVEN triage

| Item | Triage | Reason |
| --- | --- | --- |
| exact AuthorityRevision activation/binding | `PRE_PRODUCTION_BLOCKER` | Current bounded barrier is useful, but exact active/bound attestation is not proven. |
| active-runtime controller-loss reconciliation | `PRE_PRODUCTION_BLOCKER` | Restart with durable state is not proof of reconnecting to a still-running runtime safely. |
| distributed/multi-controller fencing | `DISTRIBUTED_FUTURE` | Explicitly outside the single-controller bounded slice. |
| stale ResourceLease reclamation | `NON_BLOCKING_WITH_FAIL_CLOSED_BOUNDARY` for bounded mode; production concern later | Current conflict behavior can fail closed; safe stale reclaim is unproven. |
| checkpoint side-effect safety | `ADVANCED_CAPABILITY_BLOCKER` | No meaningful Goose/OpenCode checkpoint semantics were exercised. |
| cross-substrate conformance | `MVP_BLOCKER` for a freeze claim covering multiple real substrates; otherwise `NON_BLOCKING_WITH_FAIL_CLOSED_BOUNDARY` | Goose was installed but provider-backed execution was unavailable. |
| global event ordering | `DISTRIBUTED_FUTURE` | Ledger-local ordering is bounded and does not establish a global event log. |
| general independent semantic verification | `ADVANCED_CAPABILITY_BLOCKER` | Bounded artifact verification exists; broad semantic verification does not. |

## 9. Owner decisions / next safe phase

No architecture decision is made here. Owner review is required for any status
freeze. The next evidence-efficient choices are:

1. authorize a provider-backed, cost-bounded Goose execution environment (or
   select another already-approved substrate) to complete cross-substrate
   conformance;
2. decide whether the bounded Core/RuntimeFact/Event/verification interfaces
   are ready to freeze despite unresolved substrate extensions;
3. separately prioritize exact authority attestation and active-runtime
   controller-loss recovery before production-grade execution.

No permanent dependency, architecture status change, security weakening, or
   production runtime selection is authorized by this report.

## 10. Reproducibility

From the repository root, with the disposable Goose release executable:

```sh
python3 experiments/runtime-conformance/goose/capability_probe.py \
  --goose /path/to/disposable/goose \
  --root /tmp/apex-goose-probe-reproduction \
  --output /tmp/apex-goose-probe-reproduction.json
```

The probe uses only an isolated `GOOSE_PATH_ROOT`, a harmless permission
fixture, and safe metadata output. It does not read or print secrets and is not
part of Apex production composition.

## 11. Related evidence

- [Runtime Adapter contract](RUNTIME-ADAPTER-CONTRACT-0001.md)
- [Cross-substrate evidence](RUNTIME-ADAPTER-CROSS-SUBSTRATE-CONFORMANCE-0001.md)
- [OpenCode authority evidence](OPENCODE-AUTHORITY-ATTESTATION-PROOF-0001.md)
- [Active-runtime reconciliation evidence](ACTIVE-RUNTIME-RECONCILIATION-PROOF-0001.md)
- [Architecture reconciliation](ARCHITECTURE-RECONCILIATION-0001.md)
