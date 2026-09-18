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


## NCR-GH-WRITE-20260919-01 — PR #176 repository-document mutation failure

- **Status:** `OPEN / CONTAINED / RCA_PENDING / CAPA_REQUIRED / EFFECTIVENESS_NOT_VERIFIED`.
- **Observation:** during the first adversarial-review correction pass for Draft PR #176, at least one GitHub-connected document modification failed. The Human Owner observed the user-visible failure message `抱歉，我無法完成這項修改。`.
- **Evidence limitation:** the exact low-level connector / API error was not preserved in the surviving later review trace. Root cause therefore remains `UNKNOWN`; stale SHA, connector instability, request rejection, concurrent state change and other causes remain hypotheses only.
- **Process gap:** recovery writes continued before the failure had been formally registered. Existing repository material already proposes stop/preserve/read-only-review behavior after unexpected mutation failures; the Human Owner has now explicitly required that every failure be recorded.
- **Containment:** PR #176 remains Draft and unmerged. The later branch state was re-read; subsequent file-scoped recovery commits are preserved without history rewrite.
- **Corrective action:** preserve a detailed incident record, retain the recovery commit chain, do not claim a solved root cause, and require future unexpected mutation failures to be recorded before any recovery write.
- **Preventive action:** future comparable failures must preserve non-sensitive failure evidence when available, re-read exact ref/file/blob state, separate known facts from causal hypotheses, require an explicit bounded recovery decision, and return to HOLD on repeated failure.
- **Effectiveness:** not yet verified. Closure requires a later comparable failure to demonstrate failure-record-before-retry, exact-state review, bounded recovery, read-back verification and preserved incident history.
- **Detailed record:** `docs/history/incidents/PR176_KIMI_RESEARCH_WRITE_FAILURE_2026-09-19.md`.
- **Canonical effect:** none.
