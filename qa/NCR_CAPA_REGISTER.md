# NCR / CAPA Register

## NCR-PRC-001 — cross-platform absolute-path validation

- **Observation:** the source-derived Astra Workbench test for a Windows drive path (`C:\\escape.txt`) failed on the Linux reconstruction host because `PurePath` followed host semantics.
- **Risk:** a Windows-form absolute path could be treated as a relative filename on POSIX.
- **Corrective action:** the public reconstruction adds `PureWindowsPath` drive and absolute-path checks.
- **Evidence:** Astra Workbench now reports 89 passed.
- **Canonical effect:** none.

## NCR-PRC-002 — monorepo Runtime test dependency resolution

- **Observation:** the bounded Runtime tests initially could not import the Governance Kernel and Astra Workbench when run directly from the reconstructed monorepo.
- **Corrective action:** the repository test runner supplies explicit local source roots, with no package download or network access.
- **Evidence:** bounded Runtime reports 12 passed.
- **Component source change:** none for this item.

## NCR-QA-MYPY-20260917-01 — mypy QA coverage and exact-head evidence integrity

- **Status:** `OPEN / CAPA_IN_PROGRESS / EFFECTIVENESS_NOT_VERIFIED`.
- **Severity:** `MAJOR_HIGH_CANDIDATE`; `CRITICAL_NOT_ESTABLISHED`.
- **Observation:** repository-level mypy coverage had diverged between QA lanes; restoring centralized execution surfaced latent required-check failures. The first remediation attempt also exposed that a GitHub pull-request synthetic merge ref can be mistaken for the exact PR source head unless source-state identity is explicitly verified.
- **Containment:** PR #133 remains Draft and unmerged; repository-wide mypy pass is not claimed; failing static-analysis evidence is preserved rather than broadly suppressed.
- **Corrective / preventive action:** PR #133 is the remediation candidate for centralized package dispositions, fail-closed package discovery, exact-head Python 3.11/3.12 mypy evidence, package-local configuration reuse, MYPYPATH / PEP 561 handling, and policy regression tests.
- **Effectiveness:** not yet verified. CAPA closure requires exact-head required-check success, fail-closed discovery/source-state verification, subsequent re-entry evidence, and an explicit independent-review disposition.
- **Detailed record:** `docs/quality/NCR_CAPA_MYPY_EXACT_HEAD_INTEGRITY_2026_09_17.md`.
- **Canonical effect:** none.
