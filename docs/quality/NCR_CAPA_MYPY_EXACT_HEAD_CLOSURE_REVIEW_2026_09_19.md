# NCR / CAPA closure review — mypy QA coverage and exact-head evidence integrity — 2026-09-19

Related NCR: `NCR-QA-MYPY-20260917-01`  
Status: `CLOSURE_REVIEW_PASS / OWNER_CLOSURE_DECISION_PENDING`  
Canonical effect: `NONE`  
Deployment: `FALSE`

## 1. Purpose

This review evaluates whether the effectiveness evidence required by the existing
mypy / exact-head NCR is now mature enough for Human Owner closure.

It does not rewrite the original incident chronology and does not claim independent IV&V.

~~~text
CLOSURE_REVIEW_PASS
!= NCR_CLOSED

OWNER_CLOSURE_DECISION
= STILL_REQUIRED
~~~

## 2. Live remediation state

GitHub live state re-check on 2026-09-19 establishes:

~~~text
PR_133
= MERGED

PR_133_MERGED_AT
= 2026-09-16T19:07:36Z

PR_133_EXACT_HEAD
= f9b69d0c1f0d59778975f6bfc4464125e0114a1c
~~~

Therefore the older progress-record fields saying `PR133_MERGED = FALSE`
are historical snapshots and are no longer current-state descriptions.

## 3. EV-1 — exact-head execution

The remediation candidate already established dedicated exact-head mypy execution
for Python 3.11 and Python 3.12 with the checked source head bound to the expected
PR head.

~~~text
EV_1
= PASS
~~~

This review preserves the existing limitation:

~~~text
ALL_CURRENTLY_REQUIRED_MYPY_CHECKS_PASS
!= REPOSITORY_WIDE_MYPY_PASS
~~~

Explicit exemptions remain governance-visible debt and are not silently promoted
to type-check success.

## 4. EV-2 — fail-closed package discovery

The remediation includes a regression test requiring an unclassified discovered
Python package to fail policy validation.

~~~text
EV_2
= PASS
~~~

## 5. EV-3 — source-state mismatch rejection

The dedicated exact-head jobs require the checked-out Git HEAD to equal the
expected pull-request source head before accepted mypy evidence is emitted.

~~~text
EV_3
= PASS
~~~

This preserves:

~~~text
PR_SYNTHETIC_MERGE_REF
!= PR_EXACT_HEAD
~~~

## 6. EV-4 — subsequent re-entry / recurrence check

EV-4 required a later unrelated Python-package change after the remediation
entered `main`.

That condition has now occurred repeatedly.

### Evidence A — PR #139

~~~text
PR
= 139

HEAD
= 377845ccb589e9ea9ee8f61e771889f72896ecc5

CHANGE
= unrelated human-ai-longitudinal Python package implementation

QUALITY
= SUCCESS

MYPY_EXACT_HEAD_PYTHON_3_11
= SUCCESS

MYPY_EXACT_HEAD_PYTHON_3_12
= SUCCESS
~~~

### Evidence B — PR #157

PR #157 added the `ai-tevv-profile_v0.1.0` Python package and modified the
repository mypy policy.

~~~text
PR
= 157

HEAD
= e68d152de263fd191e71fa1f65146faefd604a89

NEW_PYTHON_PACKAGE
= research-labs/ai-tevv-profile_v0.1.0

MYPY_POLICY_UPDATED
= YES

QUALITY
= SUCCESS

MYPY_EXACT_HEAD_PYTHON_3_11
= SUCCESS

MYPY_EXACT_HEAD_PYTHON_3_12
= SUCCESS
~~~

Current `.github/ci/mypy-policy.json` includes explicit dispositions for both the
human-AI longitudinal package and the AI TEVV package.

### Evidence C — later recurrence

PR #160 subsequently changed another Python research/security package and again
completed exact-head mypy successfully on Python 3.11 and 3.12.

Therefore the effectiveness signal is not limited to the remediation PR itself.

~~~text
EV_4
= PASS

LATER_UNRELATED_REENTRY
= OBSERVED

SILENT_ESCAPE_FROM_MYPY_DISPOSITION_GOVERNANCE
= NOT_OBSERVED_IN_THE_REVIEWED_REENTRY_CASES
~~~

This is bounded recurrence evidence, not proof that future packages can never escape.

## 7. EV-5 — independent review disposition

The original closure rule required either independent review or an explicitly
documented absence of independent IV&V.

Current state:

~~~text
INDEPENDENT_IVV
= NOT_ACHIEVED

ABSENCE_OF_INDEPENDENT_IVV
= EXPLICITLY_DOCUMENTED

CREATOR_SIDE_CI
!= INDEPENDENT_IVV

CHATGPT_TEACHER_REVIEW
!= INDEPENDENT_IVV
~~~

Therefore EV-5 has a valid disposition, but not an independent-validation claim.

~~~text
EV_5_DISPOSITION
= COMPLETE_WITH_EXPLICIT_LIMITATION
~~~

## 8. Effectiveness assessment

~~~text
EV_1 = PASS
EV_2 = PASS
EV_3 = PASS
EV_4 = PASS
EV_5 = COMPLETE_WITH_EXPLICIT_LIMITATION

CAPA_APPLIED
= YES

CAPA_EFFECTIVENESS_REVIEW
= PASS

RECURRENCE_SIGNAL_IN_REVIEWED_POST_MERGE_CASES
= NOT_OBSERVED
~~~

The closure assessment is limited to the NCR's two identified governance defects:

1. implicit / incomplete mypy disposition governance;
2. exact-head evidence-source identity binding.

It does not assert full repository type correctness, runtime correctness,
scientific validity, or independent IV&V.

## 9. Closure recommendation

~~~text
NCR
= OPEN_PENDING_OWNER_DECISION

CLOSURE_REVIEW
= PASS

RECOMMENDED_OWNER_DISPOSITION
= CLOSE_WITH_LIMITATIONS_RECORDED

INDEPENDENT_IVV
= NOT_ACHIEVED

REPOSITORY_WIDE_MYPY_PASS
= NOT_ESTABLISHED

CANONICAL_EFFECT
= NONE

DEPLOYMENT
= FALSE
~~~

The NCR must remain open until the Human Owner explicitly accepts closure.
