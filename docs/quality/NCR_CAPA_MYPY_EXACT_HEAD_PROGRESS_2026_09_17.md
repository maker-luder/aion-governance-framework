# NCR / CAPA progress — mypy exact-head remediation — 2026-09-17

Related NCR: `NCR-QA-MYPY-20260917-01`
Incident record: `docs/quality/NCR_CAPA_MYPY_EXACT_HEAD_INTEGRITY_2026_09_17.md`
Remediation candidate: PR #133
Status: `CAPA_IN_PROGRESS / EFFECTIVENESS_NOT_VERIFIED`

## Purpose

This progress note records corrective-action evidence without rewriting the original incident chronology and without closing the NCR.

```text
INCIDENT_RECORD != REMEDIATION_PR
REMEDIATION_PR != CAPA_EFFECTIVENESS_VERIFICATION
CAPA_APPLIED != CAPA_EFFECTIVENESS_VERIFIED
```

## Current remediation candidate

```text
PR = 133
STATE = OPEN / DRAFT
MERGED = FALSE
EXACT_HEAD = 07f55dbafb0405745d44c068149d26424540fcf5
```

## Exact-head evidence

Dedicated exact-head mypy jobs for Python 3.11 and Python 3.12 explicitly checked out and verified the candidate source head before running mypy.

Observed Python 3.11 evidence:

```text
MYPY_EXPECTED_SOURCE_HEAD = 07f55dbafb0405745d44c068149d26424540fcf5
MYPY_CHECKED_SOURCE_HEAD  = 07f55dbafb0405745d44c068149d26424540fcf5
MYPY_EXACT_HEAD           = 07f55dbafb0405745d44c068149d26424540fcf5
MYPY_POLICY_PACKAGE_COUNT = 36
MYPY_POLICY_STRICT_COUNT = 13
MYPY_POLICY_CONFIGURED_COUNT = 0
MYPY_POLICY_EXEMPT_COUNT = 23
MYPY_REQUIRED_CHECKS = PASS
REPOSITORY_WIDE_MYPY_PASS = NOT_ESTABLISHED
```

Python 3.12 exact-head mypy also completed successfully at the same exact candidate head.

The exact-head result therefore supports only:

```text
ALL_CURRENTLY_REQUIRED_MYPY_CHECKS_PASS = TRUE
```

It does not support:

```text
REPOSITORY_WIDE_MYPY_PASS = TRUE
```

because 23 pre-existing package roots remain explicitly classified as `EXEMPT_WITH_EXPLICIT_REASON` migration debt.

## Corrective findings resolved in the current candidate

The restored checker surfaced and the remediation addressed typed-contract issues including:

- invariant mapping boundaries in the AION/Astra inquiry event hashing path;
- explicit Optional service state in bounded research campaign construction;
- platform-specific subprocess creation flags in Astra Workbench;
- missing generic annotation for Bazi seasonal relation counters;
- dataclass instance narrowing before `asdict`;
- monorepo memory-recall dependency typing, including SQLite row/session boundaries, generic JSON data, Optional replacement content, and helper signatures;
- third-party `tzdata` typing through a pinned typeshed stub package rather than broad import suppression.

No blanket `ignore_missing_imports` policy or repository-wide `# type: ignore` suppression was introduced as the corrective strategy.

## Quality controls at the same exact head

```text
QUALITY = SUCCESS
RUNTIME_STRONG_QA = SUCCESS
CODEQL = SUCCESS
AION_ASTRA_BOUNDED_INQUIRY = SUCCESS
AION_ASTRA_RESEARCH_CLOSURE = SUCCESS
```

The Main Transition Authority Gate remains fail-closed because no fresh merge authorization has been granted. That failure is not treated as a remediation defect.

## Effectiveness criteria progress

### EV-1 — exact-head execution

```text
STATUS = CURRENT_CANDIDATE_PASS
PYTHON_3_11_EXACT_HEAD_MYPY = PASS
PYTHON_3_12_EXACT_HEAD_MYPY = PASS
CHECKED_HEAD = EXPECTED_PR_HEAD
```

### EV-2 — fail-closed package discovery

`tests/test_repository_mypy_policy.py` contains a regression test proving an unclassified discovered package causes policy validation failure.

```text
STATUS = IMPLEMENTED_AND_EXERCISED
```

### EV-3 — source-state mismatch rejection

The dedicated exact-head jobs check out the PR source SHA and require `git rev-parse HEAD` to equal the expected PR head before mypy can execute and emit accepted evidence.

```text
STATUS = IMPLEMENTED_AND_EXERCISED
```

### EV-4 — subsequent re-entry / recurrence check

This criterion intentionally requires a later unrelated Python-package change after the remediation enters `main`.

```text
STATUS = NOT_YET_POSSIBLE
```

### EV-5 — independent review disposition

Creator-side implementation and CI reruns are not independent IV&V.

```text
STATUS = NOT_YET_VERIFIED
```

## Merge sequencing clarification

The Human Owner has approved the merge sequence: record the NCR/CAPA incident in `main` first, then re-check PR #133 against the resulting latest `main` and only then transition the remediation candidate.

EV-4 and EV-5 are CAPA effectiveness / closure criteria. They are not prerequisites for placing either the open NCR/CAPA record or its remediation implementation into `main`.

```text
EV4_OR_EV5_PENDING
!= MERGE_PROHIBITED

EV4_OR_EV5_PENDING
= NCR_REMAINS_OPEN
= CAPA_EFFECTIVENESS_NOT_VERIFIED
```

## Current CAPA disposition

```text
NCR = OPEN
CAPA = IN_PROGRESS
CAPA_EFFECTIVENESS = NOT_VERIFIED
PR133 = REMEDIATION_CANDIDATE
PR133_MERGED = FALSE
ALL_CURRENTLY_REQUIRED_MYPY_CHECKS_PASS = TRUE
EXEMPT_PACKAGE_COUNT = 23
REPOSITORY_WIDE_MYPY_PASS = NOT_ESTABLISHED
```

No CAPA closure is claimed by this progress record.


## 2026-09-19 current-state reconciliation

The sections above remain event-time evidence and are not rewritten.

Current state is controlled by:
`docs/quality/NCR_CAPA_MYPY_EXACT_HEAD_CLOSURE_REVIEW_2026_09_19.md`.

~~~text
PR133_MERGED = TRUE
PR133_EXACT_HEAD = f9b69d0c1f0d59778975f6bfc4464125e0114a1c
EV_1 = PASS
EV_2 = PASS
EV_3 = PASS
EV_4 = PASS
EV_5 = COMPLETE_WITH_EXPLICIT_LIMITATION
CLOSURE_REVIEW = PASS
HUMAN_OWNER_CLOSURE_APPROVAL = GIVEN
NCR = CLOSED
CAPA_EFFECTIVENESS = VERIFIED_WITH_LIMITATIONS
INDEPENDENT_IVV = NOT_ACHIEVED
~~~

The historical statements `PR133_MERGED = FALSE` and `EV_4 = NOT_YET_POSSIBLE`
describe the earlier review time and are not current-state assertions.
