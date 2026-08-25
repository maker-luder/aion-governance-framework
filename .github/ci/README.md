# CI toolchain reproducibility note

This directory records the direct Python QA tools used by the preserved repository workflows.

The pins were taken from successful GitHub Actions runs on 2026-08-25 and are intended to reduce avoidable CI drift. They do **not** establish a fully hermetic environment, independent reproducibility, certification, or IV&V.

## Python job labels

The Quality matrix intentionally remains `3.11` and `3.12` rather than embedding patch versions in the job names. The active `Main Protection` GitHub ruleset requires the exact status contexts `Python 3.11` and `Python 3.12`; changing those labels without an atomic ruleset update could strand the protected branch.

The successful 2026-08-25 runs resolved those minor-version selectors to CPython 3.11.16 and 3.12.14 respectively. Those resolved patch versions are evidence about that run, not a promise that GitHub-hosted runners will retain them indefinitely.

## Scope

- `quality-toolchain.txt` pins direct tools for the main Quality workflow.
- `runtime-strong-qa-toolchain.txt` pins direct tools for Runtime Strong QA.
- project/component dependencies remain declared by their own package metadata and are built from the checked-out source where applicable.
- historical release manifests and tags remain authoritative for their historical release states.

No dependency-update bot is enabled by this maintenance change because the repository is frozen and the project work loop is terminated; automatic upstream-tracking PR generation would conflict with that standing boundary.
