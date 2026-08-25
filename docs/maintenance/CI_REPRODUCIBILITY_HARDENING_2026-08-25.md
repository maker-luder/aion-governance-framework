# CI reproducibility hardening — 2026-08-25

```text
CHANGE_CLASS = EXTERNAL_MAINTENANCE_HARDENING
PROJECT_RESTART = NO
RESEARCH_RESTART = NO
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
HISTORICAL_REWRITE = NO
```

## Purpose

Reduce avoidable future CI drift in the preserved research checkpoint without changing scientific claims, runtime behavior, historical event meaning, or deployment authority.

## Changes

- pin the direct Quality QA tools to versions observed in successful 2026-08-25 GitHub Actions runs;
- pin the direct Runtime Strong QA tools to versions observed in successful 2026-08-25 runs;
- keep Quality job labels at `Python 3.11` and `Python 3.12` rather than encoding patch versions;
- make changes to the Runtime Strong QA toolchain file trigger Runtime Strong QA;
- preserve package/component dependency declarations in their own package metadata;
- document that these pins reduce drift but do not create a hermetic environment or independent reproducibility proof;
- preserve the frozen-repository contribution, provenance, non-claim, and deployment boundaries.

## Validated source environment

The preceding successful runs resolved the Quality matrix selectors to CPython 3.11.16 and 3.12.14. The direct QA tool versions recorded here are therefore bounded evidence for the 2026-08-25 maintenance environment, not claims about future runner inventory.

## Explicit non-actions

No dependency-update bot, external model call, new research task, new feature, deployment workflow, canonical promotion, or automatic restart mechanism is introduced.
