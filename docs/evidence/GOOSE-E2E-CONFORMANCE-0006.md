# Provider-Backed Goose Conformance and Bounded Freeze — 0006

Status: `PROPOSED` evidence and freeze-readiness report. This report does not
change architecture status. It records one bounded provider-backed experiment
and one bounded dual-substrate comparison.

## 1. Executive result

Goose 1.49.0 completed the same bounded `REPORT.md` artifact task through an
experiment-only adapter, using the existing `claude-code` provider path. The
OpenCode and Goose runs both passed the existing Core-owned verification path.
The existing RuntimeAdapter conformance helper also passed for both adapters.

Conclusion: the bounded RuntimeAdapter/Core contract did not reveal a hidden
OpenCode-specific assumption in this experiment. The contract is portable with
adapter-side mapping for process/session details and substrate facts. This is
not proof of all-substrate conformance, authority attestation, controller-loss
recovery, or production-grade runtime identity.

## 2. Environment and provenance

| Item | Observation | Evidence |
| --- | --- | --- |
| Apex main before experiment | `a330881554efa7e51144c8348104d73f804ccb42` | `OBSERVED_REPOSITORY_STATE` |
| Goose source | `aaif-goose/goose` | `OBSERVED_REPOSITORY_STATE` |
| Goose source ref | tag `v1.49.0` | `OBSERVED_REPOSITORY_STATE` |
| Goose source SHA | `71fc4be1ed729e26b1dc0a4466abdd03be548a53` | `OBSERVED_REPOSITORY_STATE` |
| Goose executable | `/Applications/Goose.app/Contents/Resources/bin/goose` | `OBSERVED_RUNTIME_EVIDENCE` |
| Goose version | `1.49.0` | `OBSERVED_RUNTIME_EVIDENCE` |
| Provider | `claude-code` | `OBSERVED_RUNTIME_EVIDENCE` |
| Model | provider-selected default; no explicit model value supplied | `OBSERVED_RUNTIME_EVIDENCE` |
| Credentials | existing environment/provider access used; values were never read, printed, copied, or persisted | `OBSERVED_REPOSITORY_STATE` |
| Workspaces | disposable temporary directories | `OBSERVED_RUNTIME_EVIDENCE` |
| Apex dependency | none | `OBSERVED_REPOSITORY_STATE` |

The Goose binary was used through its existing application installation; no
PATH/profile edit or project dependency was made. The experiment-only adapter
and runner are under `experiments/runtime-conformance/goose/` and are not part
of default Apex composition.

## 3. Experiment implementation

The experiment adapter maps only the existing contract:

- `materialize_authority` creates an isolated temporary Goose root and carries
  the Core authority digest.
- `execute` invokes Goose non-interactively with a bounded turn count and
  structured-output request.
- the adapter maps process completion to `RuntimeFact.EXITED` or
  `RuntimeFact.UNKNOWN` and returns opaque runtime identity.
- it never assigns Apex semantic success.
- Core writes and verifies `REPORT.md`; Goose is instructed not to use tools or
  write files.

The adapter does not provide substrate activation attestation. Its preparation
therefore remains `substrate_activation_confirmed = false`, consistent with
the existing fail-closed boundary.

## 4. Capability and portability findings

| Contract area | OpenCode | Goose | Classification |
| --- | --- | --- | --- |
| Preparation identity | passed | passed | `PASS_BOTH` |
| Preparation/result correlation | passed | passed | `PASS_WITH_SUBSTRATE_MAPPING` |
| Authority/config digest transport | Core digest carried and checked | Core digest carried and checked | `PASS_WITH_SUBSTRATE_MAPPING`; activation remains `NOT_PROVEN` |
| Opaque runtime identity | session identity may be present | process identity and adapter instance were available; no stable session id in `--no-session` output | `PASS_WITH_SUBSTRATE_MAPPING` |
| RuntimeFact normalization | `EXITED`/unknown mapping | `EXITED`/unknown mapping | `PASS_WITH_SUBSTRATE_MAPPING` |
| Core-owned semantic success | passed | passed | `PASS_BOTH` |
| Result/artifact correlation | passed | passed | `PASS_WITH_SUBSTRATE_MAPPING` |
| Unknown/mismatch fail-closed behavior | existing tests pass | Core barrier negative probe passed | `PASS_BOTH` for bounded Core behavior |
| Workspace ownership | Core claim and release | Core claim and release | `PASS_BOTH` for bounded workspace |
| Cancellation | not newly exercised | not exercised | `NOT_PROVEN` |
| Reconnect/resume | outside bounded run | Goose exposes session surfaces, but adapter recovery not exercised | `NOT_PROVEN` |
| Substrate authority attestation | not proven | not proven | `NOT_PROVEN` |

The only concrete portability difference was the absence of a stable Goose
session identifier when `--no-session` was used. The existing
`RuntimeIdentity` already permits optional `session_id`, `process_id`, and
`adapter_instance_id`, so no canonical contract change was required. This
experiment does not prove that process identity alone survives controller loss
or is sufficient for safe reassociation.

## 5. Same bounded task on two substrates

The task was `Inspect README and create REPORT.md`, with separate disposable
workspaces and the same Apex Core coordinator.

| Invariant | OpenCode | Goose |
| --- | --- | --- |
| Runtime fact | `EXITED` | `EXITED` |
| Process/runtime identity observed | yes | yes; session component was not required |
| Preparation identity | valid | valid |
| Authority digest correlation | valid | valid |
| Authority activation attestation | `NOT_PROVEN` | `NOT_PROVEN` |
| Workspace claim and ledger | valid | valid |
| Immutable identity relations | valid | valid |
| Durable events | existing bounded run | 10 ledger events |
| Core artifact verification | `PASS` | `PASS` |
| Semantic success | true only after verification | true only after verification |

The report contents need not be byte-identical. The relevant result is that
both substrates traversed the same Core contract and neither adapter assigned
semantic success directly.

## 6. Negative probe

The experiment supplied an authority evidence record whose
`authority_revision_id` did not match the immutable manifest. Core
`ExecutionBarrier.release` rejected it with `SafetyError`.

Result: `PASS` for the bounded Core fail-closed barrier. This does not prove
that a substrate itself activated or bound the authority revision.

## 7. Freeze-readiness recommendation

No status is changed by this report. The recommendation is:

| Contract | Recommendation | Bounded guarantee supported | Excluded/unproven guarantee |
| --- | --- | --- | --- |
| Task / Attempt / immutable ExecutionManifest | `READY_TO_FREEZE` | distinct identity and immutable manifest relation | future epoch/checkpoint lineage |
| RuntimeFact vocabulary and semantic separation | `READY_TO_FREEZE` | substrate facts do not include Apex semantic success | complete fact mapping for every substrate |
| Core semantic completion | `READY_TO_FREEZE` | Core artifact verification gates bounded success | general semantic verification |
| EventEnvelope | `READY_TO_FREEZE` | typed/versioned durable events in ledger-local scope | global ordering/consensus |
| Workspace ResourceClaim | `READY_TO_FREEZE` | bounded single-controller exclusive workspace conflict prevention | distributed leases and stale reclaim |
| Independent Core artifact verification | `READY_TO_FREEZE` | executor output is checked by Core after execution | advanced or general semantic judging |
| RuntimeAdapter boundary | `READY_TO_FREEZE` for bounded contract | OpenCode and Goose both map preparation, identity, facts, result, and Core verification | universal runtime conformance, recovery, cancellation |
| RuntimeIdentity/correlation | `READY_TO_FREEZE` for bounded opaque/optional fields | adapter-specific identity may be optional and is not Attempt identity | stable cross-restart identity binding |
| Authority/ExecutionBarrier | `KEEP_FREEZE_CANDIDATE` | Core checks materialization, revision, lane, Attempt, and barrier sequence | exact substrate activation/binding attestation |
| Startup/controller-loss reconciliation | `KEEP_FREEZE_CANDIDATE` | bounded fail-closed classifications | active-runtime recovery and orphan reassociation |

The evidence supports freezing the bounded contract boundary, not the
unproven substrate/runtime guarantees surrounding it. Any actual `FROZEN`
status update requires a separate governed architecture-status change.

## 8. Remaining NOT_PROVEN triage

| Item | Triage |
| --- | --- |
| Exact AuthorityRevision activation/binding | `PRE_PRODUCTION_BLOCKER` |
| Active-runtime controller-loss reconciliation | `PRE_PRODUCTION_BLOCKER` |
| Distributed/multi-controller fencing | `DISTRIBUTED_FUTURE` |
| Stale ResourceLease reclamation | `NON_BLOCKING_WITH_FAIL_CLOSED_BOUNDARY` for bounded mode; production concern later |
| Checkpoint side-effect safety | `ADVANCED_CAPABILITY_BLOCKER` |
| Universal cross-substrate conformance | `NON_BLOCKING_WITH_FAIL_CLOSED_BOUNDARY` for OpenCode-only MVP; blocker for multi-substrate claim |
| Global event ordering | `DISTRIBUTED_FUTURE` |
| General independent semantic verification | `ADVANCED_CAPABILITY_BLOCKER` |
| Goose cancellation/reconnect/recovery semantics | `NOT_PROVEN`; future adapter qualification work |

## 9. MVP release-boundary answer

`YES_WITH_BOUNDED_GUARANTEES`.

Apex may proceed toward an OpenCode-backed MVP while Goose remains optional and
experimental, exact authority activation remains `NOT_PROVEN`, and
active-runtime recovery remains `NOT_PROVEN`, provided the MVP retains the
current Core-mediated barrier, durable identity/fence behavior, fail-closed
unknown handling, bounded workspace claims, and Core verification. This is not
a claim of production-grade authority attestation or controller-loss recovery.

## 10. Reproducibility and related evidence

The experiment-only commands were:

```sh
PYTHONPATH=. python3 -B \
  experiments/runtime-conformance/goose/run_conformance.py \
  --goose /Applications/Goose.app/Contents/Resources/bin/goose \
  --output /tmp/apex-goose-conformance-0006.json

python3 -B -m unittest tests.test_runtime_conformance -v
```

The runner records only structural metadata and never writes raw provider
output to the repository. It uses disposable workspaces and does not import
Goose into production composition.

- [Prior Goose capability evidence](GOOSE-CONFORMANCE-0005.md)
- [Runtime Adapter contract evidence](RUNTIME-ADAPTER-CONTRACT-0001.md)
- [Cross-substrate baseline evidence](RUNTIME-ADAPTER-CROSS-SUBSTRATE-CONFORMANCE-0001.md)
- [OpenCode authority evidence](OPENCODE-AUTHORITY-ATTESTATION-PROOF-0001.md)
- [Architecture reconciliation](ARCHITECTURE-RECONCILIATION-0001.md)
