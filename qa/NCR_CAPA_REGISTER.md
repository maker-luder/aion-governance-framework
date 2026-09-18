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

- **Status:** `CLOSED / CAPA_EFFECTIVENESS_VERIFIED_WITH_LIMITATIONS / OWNER_APPROVED`.
- **Severity:** `MAJOR_HIGH_CANDIDATE`; `CRITICAL_NOT_ESTABLISHED`.
- **Observation:** repository-level mypy coverage had diverged between QA lanes; restoring centralized execution surfaced latent required-check failures. The first remediation attempt also exposed that a GitHub pull-request synthetic merge ref can be mistaken for the exact PR source head unless source-state identity is explicitly verified.
- **Remediation state:** PR #133 was merged on 2026-09-16 at exact head `f9b69d0c1f0d59778975f6bfc4464125e0114a1c`. The historical incident/progress documents retain their event-time pre-merge snapshots.
- **Corrective / preventive action:** centralized package dispositions, fail-closed package discovery, exact-head Python 3.11/3.12 mypy evidence, package-local configuration reuse, MYPYPATH / PEP 561 handling, and policy regression tests are present in current history.
- **Effectiveness:** EV-1 through EV-4 are now supported, including later unrelated Python-package re-entry through PRs #139, #157, and #160 with successful exact-head mypy on Python 3.11 and 3.12. EV-5 is disposed by explicitly recording that independent IV&V is not achieved; creator-side CI and ChatGPT review are not independent IV&V.
- **Closure decision:** Human Owner explicitly approved closure on 2026-09-19. `NCR = CLOSED`; `CAPA_EFFECTIVENESS = VERIFIED_WITH_LIMITATIONS`.
- **Detailed records:** `docs/quality/NCR_CAPA_MYPY_EXACT_HEAD_INTEGRITY_2026_09_17.md`; `docs/quality/NCR_CAPA_MYPY_EXACT_HEAD_CLOSURE_REVIEW_2026_09_19.md`.
- **Retained limitations:** `INDEPENDENT_IVV = NOT_ACHIEVED`; repository-wide mypy pass remains not established where explicit exemptions exist; creator-side CI and ChatGPT review are not independent IV&V.
- **Canonical effect:** none.


## NCR-GH-WRITE-20260919-01 — PR #176 repository-document mutation failure

- **Status:** `OPEN / CONTAINED / RCA_PENDING / CAPA_REQUIRED / EFFECTIVENESS_NOT_VERIFIED`.
- **Observation:** during the first adversarial-review correction pass for Draft PR #176, at least one GitHub-connected document modification failed. The Human Owner observed the user-visible failure message `抱歉，我無法完成這項修改。`.
- **Evidence limitation:** the exact low-level connector / API error was not preserved in the surviving later review trace. Root cause therefore remains `UNKNOWN`; stale SHA, connector instability, request rejection, concurrent state change and other causes remain hypotheses only.
- **Process gap:** recovery writes continued before the failure had been formally registered. Existing repository material already proposes stop/preserve/read-only-review behavior after unexpected mutation failures; the Human Owner has now explicitly required that every failure be recorded.
- **Containment / current state:** PR #176 was later merged on 2026-09-18 at exact head `c067e3183905321448fb3ddaaa3794cde87b01f3`, producing merge commit `bfaee47510b280ce183564bf7e0dafdc6dcb8517`. The incident remains OPEN; merging the incident record and Kimi research does not establish root cause or CAPA effectiveness. Subsequent file-scoped recovery commits remain preserved without history rewrite.
- **Corrective action:** preserve a detailed incident record, retain the recovery commit chain, do not claim a solved root cause, and require future unexpected mutation failures to be recorded before any recovery write.
- **Preventive action:** future comparable failures must preserve non-sensitive failure evidence when available, re-read exact ref/file/blob state, separate known facts from causal hypotheses, require an explicit bounded recovery decision, and return to HOLD on repeated failure.
- **Effectiveness:** not yet verified. Closure requires a later comparable failure to demonstrate failure-record-before-retry, exact-state review, bounded recovery, read-back verification and preserved incident history.
- **Detailed record:** `docs/history/incidents/PR176_KIMI_RESEARCH_WRITE_FAILURE_2026-09-19.md`.
- **Canonical effect:** none.


## NCR-2026-09-10-DOC-MUTATION-CASCADE — repository mutation recovery cascade

- **Status:** `OPEN / UNDER_REVIEW / CAPA_EFFECTIVENESS_NOT_VERIFIED`.
- **Observation:** the 2026-09-10 incident record documented a repository-mutation cascade after an execution-level anomaly, with candidate root causes spanning SHA/object confusion, stale/concurrent state, missing control retrieval, local recovery-goal dominance, and missing host-orchestration binding.
- **Historical scope:** the original record intentionally retained `ROOT_CAUSE = PARTIAL / OPEN` and required real host-level effectiveness evidence before closure.
- **2026-09-19 effectiveness counterevidence:** during PR #176 work, a repository-document mutation failed and recovery writes proceeded before formal incident/NCR registration. The exact low-level failure cause is not preserved, so this does **not** prove the same technical root cause as the 2026-09-10 event. It does show that the intended stop → preserve → record → exact-state review → bounded recovery sequence was not reliably enforced at the host/process level.
- **Linked NCR:** `NCR-GH-WRITE-20260919-01`.
- **Disposition:** keep OPEN / UNDER_REVIEW. The 2026-09-19 event is effectiveness counterevidence, not closure evidence.
- **Detailed record:** `docs/evidence/governance-reentry-20260910/NCR_CAPA_REVIEW.md`.
- **Canonical effect:** none.
