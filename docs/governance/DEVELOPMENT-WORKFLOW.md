# Development Workflow

## Branches

`main` is the protected integration branch. Routine direct commits to `main` are not part of the workflow. Work starts from an up-to-date `main` branch and uses one of these prefixes:

`feature/*`, `fix/*`, `docs/*`, `chore/*`, `refactor/*`, or `test/*`.

The branch name should describe the change. DPT-related work remains an optional capability concern; it must not be used as a reason to merge DPT into Apex Code Core.

## Pull requests

The required path is:

```text
branch -> pull request -> required validation -> review -> merge
```

Every pull request targets `main`, explains its scope, and links relevant architecture or evidence changes. Required CI must pass before merge. Review confirms that the change is within scope, preserves evidence discipline, and does not silently change frozen architecture decisions.

## Merge and history

The default merge strategy is squash merge for normal implementation and maintenance pull requests. It keeps `main` linear and makes each merged change easy to revert. Exceptions should be documented in the pull request when preserving multiple commits or a merge topology is materially useful. Existing history is not rewritten by this policy.

## Exceptions

Emergency or administrative changes still require a recorded review decision and post-change validation. They are exceptions to the workflow, not a replacement for it.
