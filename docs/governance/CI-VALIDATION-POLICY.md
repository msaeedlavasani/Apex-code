# CI Validation Policy

CI uses the cheapest reliable validation appropriate to the affected scope. It must not run heavy end-to-end infrastructure indiscriminately after every change.

## Validation tiers

The repository now has a layered product-validation pipeline. The required PR
workflow is intentionally credential-free and uses the same commands developers
can run locally.

### Tier 1 — required PR validation

The `Apex Code CI Gate` aggregates these always-present required jobs:

- repository/documentation validation and change-range `git diff --check`;
- `python3 -B -m unittest discover -s tests -v` for Core;
- `npm ci`, `npm run typecheck`, and `npm run build` in `product_shell/openwork`;
- `npm ci`, `npm run typecheck`, and `npm test` in `product_shell/desktop`.

The legacy `Lean documentation validation` context remains as a temporary
compatibility job because it is currently required by `main` branch protection.
It is not the canonical aggregate gate and should be removed after branch
protection requires `Apex Code CI Gate` instead.

### Tier 2 — targeted integration validation

The PR workflow always creates explicit targeted jobs. They report
`NOT_APPLICABLE` and succeed for unrelated changes; executable-surface changes
run the relevant Application Boundary, renderer, desktop, and macOS packaging
checks. This keeps required-check names stable while avoiding unnecessary
platform work for documentation-only changes.

### Tier 3 — acceptance and release validation

`Apex Code Acceptance` is manually dispatched. It runs canonical static checks
and a macOS unsigned directory-package smoke. Real OpenCode/provider execution,
full desktop restart/recovery acceptance, visual browser acceptance, and future
signing/notarization remain higher-cost or credential-bearing validation and
are not required for ordinary pull requests.

## CI validation map

| Source area | Required PR validation | Targeted validation | Acceptance/release validation |
|---|---|---|---|
| Repository, docs, governance | `validate_docs.py`; change-range `git diff --check` | — | same static checks |
| `apex_code/`, `tests/` | full Core test suite | Application Boundary tests when the executable seam is affected | full Core suite in manual acceptance |
| `product_shell/openwork/` | locked install, typecheck, production build | Application Boundary and renderer seam checks | renderer build as part of packaged smoke |
| `product_shell/desktop/` | locked install, Node syntax/typecheck, deterministic tests | desktop lifecycle/security and package-sensitive checks | unsigned macOS directory-package smoke |
| cross-layer changes | all Tier 1 jobs | targeted integration job; macOS job when shell/packaging paths change | full manual acceptance workflow |
| provider/runtime credentials | never required | never required | separately authorized real-provider validation only |

## Current validation coverage

The static repository checks include:

- Markdown structure checks: balanced fenced blocks, headings, and practical internal relative-link validation.
- Required architecture directory/file checks.
- Constrained architecture status vocabulary: `FROZEN`, `FREEZE_CANDIDATE`, `PROPOSED`, `INFERENCE`, `UNKNOWN`, `NOT_PROVEN`.
- `git diff --check` for whitespace errors.
- Obvious secret/key/private-credential filename and content-pattern checks. Failures report paths and never secret values.

The validator is intentionally static and uses only the Python standard library. It does not execute product code or inspect `.freebuff/`.

## Scope-aware validation

```text
docs-only
  -> Tier 1 required checks; targeted jobs explicitly report NOT_APPLICABLE

core code
  -> lint + typecheck + unit + relevant integration

runtime adapter
  -> adapter tests + conformance + targeted integration

critical execution/authority/recovery changes
  -> stronger integration + targeted smoke/E2E
```

Core/product changes run the relevant Tier 1 checks and targeted integration.
Heavy E2E is not part of ordinary PR CI.

## CI job and path policy

The required aggregate check is named `Apex Code CI Gate`. It fails if any
validation layer fails, is cancelled, or otherwise does not conclude
successfully. Jobs are not removed by path filters; targeted jobs decide
applicability inside the job so branch protection never depends on a missing
check.

Pull-request runs use concurrency cancellation for obsolete commits on the same
PR. Main-branch validation is not cancelled by an unrelated PR update.

Node versions and lockfiles are pinned by the workflow. `setup-node` may cache
npm's package cache, but ledgers, runtime sessions, generated canonical state,
credentials, and mutable product truth are never cached. Ordinary PR runs do
not upload large binaries. Acceptance packaging retains only a short-lived
metadata artifact for smoke evidence.

## Secrets and failure semantics

Required PR validation needs no credentials and must be safe for untrusted fork
code. Provider-backed runs may occur only in an explicitly authorized
credential-bearing context; secrets must never appear in logs, traces, browser
storage, or artifacts.

Each CI command is expected to fail nonzero on its own failure. The aggregate
gate preserves that result rather than converting failure to a skipped or
successful check. Temporary failure probes are maintained outside the normal
product path; a local preflight is evidence of command behavior, not a
replacement for required CI.

## Local command parity

The compact local preflight equivalent is:

```text
python3 -B -m unittest discover -s tests -v
python3 scripts/validate_docs.py
git diff --check
cd product_shell/openwork && npm ci && npm run typecheck && npm run build
cd product_shell/desktop && npm ci && npm run typecheck && npm test
```

Run the commands in their listed package directories; CI uses the same locked
install, typecheck, build, and test commands.

## Merge gate

The required CI check must pass on pull requests before review/merge. A future check may be made required only when it is stable, scoped, and documented here.
