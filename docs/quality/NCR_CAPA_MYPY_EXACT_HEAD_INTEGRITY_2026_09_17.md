# NCR / CAPA — mypy QA coverage and exact-head evidence integrity — 2026-09-17

Status: `NCR_OPEN / CAPA_IN_PROGRESS / EFFECTIVENESS_NOT_VERIFIED`
Severity: `MAJOR_HIGH_CANDIDATE / CRITICAL_NOT_ESTABLISHED`
Canonical effect: `NONE`
Deployment: `FALSE`

## Purpose

This record preserves a serious pre-merge quality event discovered while restoring `mypy` as an explicit QC/QA control across the repository.

The event has two coupled but distinct parts:

1. repository-level static-type-analysis coverage had diverged between QA lanes, allowing active Python surfaces to exist without an explicit repository-wide mypy disposition; and
2. the first repository-wide mypy implementation exposed an evidence-binding defect: a GitHub `pull_request` workflow can check out a synthetic merge ref while a QA artifact or log label is interpreted as if it were the exact pull-request head.

This record is separate from the remediation implementation. PR #133 is a corrective/preventive-action candidate; it is not itself the incident record and it does not establish CAPA effectiveness.

## Verified baseline

The current `main` baseline from which this NCR record is opened is:

```text
MAIN = a379f91251864aa95569cb2e94ddcf8685d03dd3
```

That main state already contains the earlier documentation-only mypy coverage-gap record from PR #132. It does not contain the executable repository-wide mypy governance proposed by PR #133.

At the time this NCR/CAPA record is opened, PR #133 is:

```text
PR = 133
STATE = OPEN / DRAFT
MERGED = FALSE
EXACT_HEAD = 0fad3c4d2d7e9c31ac371e7f7f797f332fd19045
```

## Observed quality event

### A. Static-analysis coverage gap

Before PR #133, the repository already contained:

- a pinned mypy tool line in Runtime Strong QA;
- multiple package-local `[tool.mypy]` configurations with `strict = true`;
- an established precedent for `MYPYPATH`-based monorepo source discovery.

However, general `Quality` did not install or execute mypy across the active Python package inventory. A package could therefore have pytest, Ruff, compile checks, coverage and other Quality controls succeed without current mypy evidence.

When PR #133 restored a central mypy policy and executed existing strict configurations, latent type-check failures appeared immediately. The observed failures include interface variance, Optional/None assignments, untyped dependency surfaces, platform-specific subprocess typing, generic annotations, and dataclass narrowing.

```text
OTHER_QA_PASS
!= MYPY_PASS

PACKAGE_HAS_STRICT_MYPY_CONFIG
!= CONFIG_WAS_EXECUTED_REPOSITORY_WIDE
```

No claim is made that every reported mypy finding is a runtime defect. The nonconformity is that the static-type-analysis control was not consistently exercised and its absence was not explicit at the repository QA-governance layer.

### B. Exact-head evidence-binding mismatch

The first PR #133 implementation executed repository mypy inside the ordinary `pull_request` Quality job. GitHub checked out the pull request synthetic merge ref:

```text
SYNTHETIC_MERGE_REF = 1273b9da34e7f010dbbfcab8fca997bd5896de68
PR_HEAD_AT_THAT_RUN  = dbf1cbb467862de06e73e7d11847a12c92a1e3cb
```

The runner's `GITHUB_SHA` therefore described the merge candidate, not the exact PR source head. Treating that value as `exact-head` evidence would bind the QA claim to the wrong source state.

This was detected before merge. Current PR #133 separates exact-head mypy jobs and explicitly checks out and verifies the PR head before executing the checker.

```text
PR_MERGE_REF != PR_EXACT_HEAD
CHECK_RAN != CHECK_RAN_AGAINST_THE_CLAIMED_SOURCE_STATE
```

## NCR identification

### NCR-QA-MYPY-20260917-01

Nonconformity:

> Repository QA allowed static-type-analysis coverage to become implicit and incomplete, and the first remediation attempt could have described synthetic-merge-ref evidence as exact-head evidence unless source-state identity was explicitly verified.

Classification:

```text
QUALITY_SYSTEM_EVENT = YES
STATIC_ANALYSIS_GOVERNANCE_GAP = YES
EVIDENCE_INTEGRITY_RELEVANCE = YES
PRE_MERGE_DETECTION = YES
MAIN_CONTAMINATION = NOT_ESTABLISHED
RELEASE_CONTAMINATION = NOT_ESTABLISHED
CRITICAL_SEVERITY = NOT_ESTABLISHED
```

The severity remains `MAJOR_HIGH_CANDIDATE` until impact review establishes whether any prior release, main-branch assertion, external consumer, or research conclusion relied on a false current-mypy-pass or false exact-head claim.

## Immediate containment

```text
PR133 = DRAFT
PR133_MERGE = NO
REPOSITORY_WIDE_MYPY_PASS = NOT_ESTABLISHED
CAPA_EFFECTIVENESS = NOT_VERIFIED
```

Containment rules:

- preserve failing mypy output as evidence rather than suppressing it;
- do not claim repository-wide or PR-wide mypy pass while required checks fail or explicit exemptions remain;
- do not use broad `ignore_missing_imports`, blanket `# type: ignore`, or equivalent suppression as a substitute for root-cause correction;
- keep exact-head checks distinct from merge-candidate Quality checks;
- no NCR/CAPA closure solely because implementation code exists or CI becomes green once.

## Bounded root-cause analysis

### Root cause RC-1 — QA lane divergence

The repository accumulated package-local strict mypy policy and a Runtime Strong QA lane, while general Quality evolved independently. No central inventory required every active Python package to declare how mypy applied.

```text
LOCAL_STRICT_CONFIG_EXISTS
+
NO_REPOSITORY_WIDE_DISPOSITION_INVENTORY
-> STATIC_ANALYSIS_SCOPE_DIVERGENCE
```

### Root cause RC-2 — evidence-source identity was not machine-bound at the mypy entry point

The first central runner trusted workflow context for its source-state label. In a GitHub `pull_request` event, that context can represent a synthetic merge commit rather than the PR source head.

```text
WORKFLOW_CONTEXT_SHA
!= ALWAYS_PR_SOURCE_HEAD
```

### Contributing factor CF-1 — green adjacent controls can mask an unexecuted control

Ruff, pytest, compileall, coverage, CodeQL and other controls answer different questions. Their success did not establish static type consistency.

### Contributing factor CF-2 — monorepo typing crosses package boundaries

Strict packages import local packages through `MYPYPATH`. Restoring mypy therefore reveals both package-local findings and dependency-boundary typing debt. This increases remediation scope but is not a reason to lower the checker standard silently.

## CAPA plan

### Correction

PR #133 currently provides or is intended to provide:

- `mypy==2.3.1` in the general pinned QA toolchain;
- centralized package discovery;
- explicit per-package disposition:
  - `MYPY_REQUIRED_STRICT`
  - `MYPY_REQUIRED_CONFIGURED`
  - `EXEMPT_WITH_EXPLICIT_REASON`
- package-local mypy configuration reuse;
- explicit `MYPYPATH` support for local monorepo typing;
- PEP 561 / stub handling where legitimate typing information is available;
- exact-head mypy jobs for Python 3.11 and 3.12;
- source-head verification before exact-head evidence is emitted;
- regression tests for policy discovery and fail-closed behavior.

### Corrective action

The required corrective action is to make current strict-package checks genuinely pass without erasing findings through broad suppressions, while preserving visible exemptions as migration debt.

Known remediation classes include:

- fixing real type-signature mismatches;
- adding missing type annotations where behavior is already defined;
- making platform-specific values visible to static analysis without changing runtime semantics;
- adding legitimate third-party stubs when available;
- correcting Optional and generic contracts;
- resolving monorepo package-boundary typing deliberately rather than treating dependencies as invisible.

### Preventive action

The preventive system shall require:

```text
NEW_DISCOVERED_PYTHON_PACKAGE
-> EXPLICIT_MYPY_DISPOSITION

UNCLASSIFIED_PACKAGE
-> QUALITY_FAIL

CLAIMED_EXACT_HEAD_EVIDENCE
-> MACHINE_VERIFIED_CHECKED_HEAD

EXEMPT_WITH_EXPLICIT_REASON
!= MYPY_PASS

POLICY_COVERAGE
!= TYPE_COVERAGE
```

## Effectiveness verification

CAPA application and CAPA effectiveness are separate states.

### EV-1 — exact-head execution

For the PR #133 candidate head selected for merge review:

```text
PYTHON_3_11_EXACT_HEAD_MYPY = PASS
PYTHON_3_12_EXACT_HEAD_MYPY = PASS
CHECKED_HEAD = EXPECTED_PR_HEAD
```

This criterion concerns all packages classified as required at that candidate head. Explicit exemptions remain visible debt and therefore prevent a claim of complete repository-wide mypy coverage.

### EV-2 — fail-closed package discovery

A regression test must demonstrate that adding a discoverable `pyproject.toml` package root without a disposition fails policy validation.

### EV-3 — source-state mismatch rejection

A regression test or equivalent exact-head job guard must demonstrate that an expected source head different from the checked-out head cannot emit accepted exact-head evidence.

### EV-4 — subsequent re-entry / recurrence check

After the remediation enters main, at least one later unrelated Python-package change should exercise the policy and demonstrate that the package cannot silently escape mypy disposition governance.

This later re-entry criterion prevents immediate self-certification of the CAPA solely by the change that introduced it.

### EV-5 — independent review boundary

Creator-side implementation and rerun evidence are not independent IV&V. NCR closure should therefore record an independent review or an explicitly documented absence of independent IV&V rather than silently treating creator revalidation as independent confirmation.

## Closure rule

The NCR remains open until the effectiveness criteria are satisfied or explicitly re-scoped by Human Owner authority.

```text
CAPA_APPLIED != CAPA_EFFECTIVENESS_VERIFIED
CI_PASS != CAPA_CLOSURE
MYPY_PASS != LOGIC_CORRECTNESS
MYPY_PASS != SCIENTIFIC_VALIDATION
```

A future closure record must name the exact evidence used and must not rewrite historical failures as passes.

## Attribution

```text
HUMAN_OWNER_ORIGINAL
= identified mypy as a non-optional QC/QA pillar
= required the event to be recorded again because of its seriousness
= authorized NCR/CAPA treatment and implementation of the agreed remediation plan

CHATGPT_TEACHER_FORMALIZATION
= separated the static-analysis coverage gap from the exact-head evidence-binding defect
= proposed the NCR/CAPA structure, severity ceiling, containment, CAPA actions and effectiveness criteria
= classified PR #133 as remediation evidence rather than the incident record itself

CHATGPT_WORK_CONTRIBUTION = NONE_TO_THIS_RECORD
CODEX_CONTRIBUTION = NONE_TO_THIS_RECORD
```

## Current disposition

```text
NCR = OPEN
CAPA = IN_PROGRESS
CAPA_EFFECTIVENESS = NOT_VERIFIED
PR133 = REMEDIATION_CANDIDATE
PR133_MERGED = FALSE
REPOSITORY_WIDE_MYPY_PASS = NOT_ESTABLISHED
MAIN_CONTAMINATION = NOT_ESTABLISHED
RELEASE_CONTAMINATION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```
