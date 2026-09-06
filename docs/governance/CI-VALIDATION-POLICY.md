# CI Validation Policy

CI uses the cheapest reliable validation appropriate to the affected scope. It must not run heavy end-to-end infrastructure indiscriminately after every change.

## Current lean checks

The current architecture-first repository runs:

- Markdown structure checks: balanced fenced blocks, headings, and practical internal relative-link validation.
- Required architecture directory/file checks.
- Constrained architecture status vocabulary: `FROZEN`, `FREEZE_CANDIDATE`, `PROPOSED`, `INFERENCE`, `UNKNOWN`, `NOT_PROVEN`.
- `git diff --check` for whitespace errors.
- Obvious secret/key/private-credential filename and content-pattern checks. Failures report paths and never secret values.

The validator is intentionally static and uses only the Python standard library. It does not execute product code or inspect `.freebuff/`.

## Scope-aware validation

```text
docs-only
  -> docs/static validation

core code
  -> lint + typecheck + unit + relevant integration

runtime adapter
  -> adapter tests + conformance + targeted integration

critical execution/authority/recovery changes
  -> stronger integration + targeted smoke/E2E
```

Future layers are independent additions to the workflow: lint, typecheck, unit, integration, runtime-adapter conformance, and targeted smoke/E2E. Heavy E2E is not part of the initial CI.

## Merge gate

The required CI check must pass on pull requests before review/merge. A future check may be made required only when it is stable, scoped, and documented here.
