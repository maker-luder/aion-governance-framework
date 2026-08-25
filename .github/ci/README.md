# CI toolchain reproducibility note

This directory records the direct Python QA tools used by the preserved research-checkpoint workflows.

The pins were taken from successful GitHub Actions runs on 2026-08-25 and are intended to reduce avoidable CI drift. They do **not** establish a fully hermetic environment, independent reproducibility, certification, or IV&V.

The Quality matrix intentionally keeps the stable status labels `Python 3.11` and `Python 3.12`. Successful 2026-08-25 runs resolved those selectors to CPython 3.11.16 and 3.12.14 respectively; those patch versions are run evidence, not a guarantee about future GitHub-hosted runner inventory.

## Scope

- `quality-toolchain.txt` pins direct tools for the Quality workflow.
- `runtime-strong-qa-toolchain.txt` pins direct tools for Runtime Strong QA.
- project/component dependencies remain declared by their own package metadata and are built from the checked-out source where applicable.
- preserved historical tags, source maps, and branch provenance remain authoritative for their historical states.

No dependency-update bot is introduced by this maintenance change because automatic upstream-tracking PR generation would conflict with the frozen/non-canonical research-checkpoint boundary.
