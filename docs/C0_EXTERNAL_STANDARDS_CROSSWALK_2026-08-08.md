# C0 External Standards Crosswalk — 2026-08-08

## Status

- `STATUS = C0_CALIBRATION_CANDIDATE`
- `PURPOSE = EXTERNAL_PUBLIC_RULER_FOR_OWNER_ACCEPTANCE_DESIGN`
- `CERTIFICATION_CLAIM = FALSE`
- `FULL_CONFORMITY_CLAIM = FALSE`
- `C_EXECUTION = NOT_STARTED`
- `CANONICAL_EFFECT = NONE`

This document records the public external standards/guidance used to calibrate the project-specific Owner acceptance process for the P0/P1/P2 Runtime candidate.

It is a **crosswalk**, not a certification statement. A project mapping of `ALIGNED` or `PARTIAL` means only that the current project practice is directionally consistent with the cited public principle at the level described here.

## Calibration vocabulary

- `ALIGNED` — current project practice directly reflects the public principle and has candidate evidence.
- `PARTIAL` — direction is consistent, but evaluation criteria/evidence/process coverage remains incomplete.
- `GAP` — a C0 acceptance-governance or evidence gap that should be corrected before C begins.
- `HOLD` — relevant topic intentionally deferred from this Runtime acceptance scope.
- `N/A` — not applicable to the current Runtime candidate.

## Public calibration sources

### ISO/IEC/IEEE 12207:2026

Public source: ISO standards catalogue, *Systems and software engineering — Software life cycle processes*.

Calibration use:

- lifecycle/process completeness;
- stakeholder/Owner involvement;
- process control and change-control framing.

Interpretation limit:

- this project does not claim full 12207 process conformity;
- deployment, operation, maintenance, and retirement are not all in the current Runtime acceptance scope.

### ISO/IEC 25040:2024

Public source: ISO standards catalogue, *Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — Evaluation framework*.

Calibration use:

- evaluation must be planned rather than inferred from test success alone;
- evaluation evidence and decision criteria should be explicit.

Interpretation limit:

- this project uses the evaluation framing only; it does not claim a complete SQuaRE evaluation implementation.

### ISO/IEC 25041:2012 — confirmed current in 2024

Public source: ISO standards catalogue, *Evaluation guide for developers, acquirers and independent evaluators*.

Calibration use:

- distinguish developer/implementer evidence, Owner/acquirer-like evaluation, and genuinely independent evaluation;
- avoid treating creator-side review as independent IV&V.

Interpretation limit:

- Human Owner review remains project-internal Owner evaluation;
- `INDEPENDENT_IVV = NOT_ACHIEVED` remains explicit.

### ISO/IEC 25010:2023

Public source: ISO standards catalogue, *Product quality model*.

Calibration use:

- software quality is broader than tests passing;
- acceptance review should consider suitability, reliability-like behavior, maintainability/operability evidence, and other relevant quality characteristics instead of equating coverage with whole-product quality.

Interpretation limit:

- the current C0 does not attempt a complete nine-characteristic product-quality certification matrix.

### ISO/IEC 25045:2010 — confirmed current in 2024

Public source: ISO standards catalogue, *Evaluation module for recoverability*.

Calibration use:

- independently challenge whether P2 restart/recovery/rollback/migration acceptance criteria adequately represent recoverability rather than only code-path correctness.

Interpretation limit:

- the project does not claim formal 25045 measurement-module conformity.

### NASA SWE-034 — Acceptance Criteria

Public source: NASA Software Engineering Handbook.

Calibration use:

- acceptance criteria should be defined/documented and traceable;
- acceptance planning should identify who performs acceptance activities and how acceptance decisions are made;
- criteria should be reasonable, measurable, and tied to requirements/stakeholder expectations and evidence.

Project consequence:

- formal C criteria are explicitly labeled `FORMALIZED_POST_IMPLEMENTATION = TRUE` rather than backdated;
- criteria are frozen before C evaluation;
- known PASS results cannot generate or weaken criteria.

### NASA SWE-193 — Acceptance Testing for Affected System and Software Behavior

Public source: NASA Software Engineering Handbook.

Calibration use:

- acceptance testing for loaded or uplinked data, rules and code that affect software or software-system behavior;
- nominal and off-nominal scenarios for those loaded or uplinked artifacts.

Project consequence:

- SWE-193 is applicable only where the evaluated scope actually includes loaded or uplinked behavior-affecting data, rules or code;
- general C acceptance-criteria and acceptance-planning calibration remains under SWE-034;
- passing engineering tests remain evidence, not the acceptance decision by themselves.

### NASA SWE-052 / SWE-053 / SWE-080 — Bidirectional Traceability, Requirements Change Management, and Tracking/Evaluating Software Product Changes

Public source: NASA Software Engineering Handbook.

Calibration use:

- SWE-052: bidirectional traceability should support identification of affected requirements, design/interfaces, implementation, tests and documentation;
- SWE-053: requirements changes require management and impact analysis;
- SWE-080: changes to software products require tracking and evaluation;
- revalidation should be scoped by demonstrated impact, not mechanically reset everything.

Project consequence:

- AH-07 uses impact-based revalidation;
- unaffected evidence may be reused only when non-impact is traceable;
- uncertain/high-impact identity or governance changes expand revalidation scope conservatively.

### NIST SP 800-218 SSDF v1.1

Public source: NIST Cybersecurity publications, *Secure Software Development Framework (SSDF) Version 1.1*.

Calibration use:

- secure development practices should be integrated into the software lifecycle;
- release/build/integrity evidence should be visible rather than assumed.

Project consequence:

- public-tree scanning, local wheel builds, cold virtual-environment install, `--no-index` wheelhouse installation, and cold import smoke provide candidate build/package integrity evidence.

Interpretation limit:

- the current Runtime C0 does not claim a complete SSDF practice implementation or attestation.

## Project crosswalk

| Calibration area | External ruler | Current project state | Classification | C0/C action |
|---|---|---|---|---|
| Lifecycle/process traceability | ISO/IEC/IEEE 12207:2026 | requirements/invariants → architecture → implementation → tests → reports/change history exist; later lifecycle phases are outside current scope | PARTIAL | define acceptance scope explicitly; do not imply deployment/operations completion |
| Evaluation planning | ISO/IEC 25040:2024 | Quality and Strong QA exist; formal Owner acceptance criteria are now being constructed | GAP → C0 corrective work | freeze criteria and evidence index before C |
| Evaluator-role transparency | ISO/IEC 25041:2012 | implementer, automated QA, Human Owner, and independent-IV&V status are separately named | ALIGNED | retain role-concentration disclosure and `INDEPENDENT_IVV = NOT_ACHIEVED` |
| Product quality beyond test pass | ISO/IEC 25010:2023 | functional/identity/lifecycle tests plus packaging evidence exist; no complete product-quality matrix | PARTIAL | C reviews architecture/docs/governance/limitations as well as tests |
| Recoverability | ISO/IEC 25045:2010 | restart, chain verification, rollback and migration semantics have tests; explicit recoverability acceptance set needs challenge | PARTIAL / GAP | review AC-LIFE severities and failure/recovery conditions before freeze |
| Predefined acceptance criteria | NASA SWE-034 | formal C criteria were created after implementation | GAP acknowledged | no backdating; anti-hindsight rules; freeze before C |
| Loaded/uplinked behavior-affecting data, rules or code | NASA SWE-193 | applicability to the current C scope has not been established | N/A unless the required scope is present | use SWE-193 only when loaded/uplinked artifacts affecting behavior are actually evaluated; include nominal/off-nominal scenarios |
| Impact-based revalidation | NASA SWE-052/SWE-053/SWE-080 | AH-07 now requires impact analysis and traceable evidence reuse | ALIGNED candidate | new head requires impact analysis; revalidate affected criteria only where bounded |
| Build/release integrity evidence | NIST SSDF v1.1 | Strong QA builds local wheels and performs cold offline/no-index install/import smoke | ALIGNED candidate | retain as AC-QA evidence; do not treat as complete SSDF conformity |
| Independent IV&V | ISO/IEC 25041 + project governance | not performed | HOLD / NOT_ACHIEVED | do not promote internal review into independent-IV&V claim |
| Deployment/canonical promotion | lifecycle/governance boundary | not performed | HOLD | D merge decision and E canonical-promotion decision remain separate future gates |

## C0 gaps identified by this crosswalk

### GAP-01 — acceptance criteria formalized after implementation

Disposition: acknowledged and controlled by AH-01 through AH-06. No historical backdating.

### GAP-02 — acceptance evidence was distributed across reports/tests/workflows

Disposition: create `C0_ACCEPTANCE_EVIDENCE_INDEX_2026-08-08.md` before freeze.

### GAP-03 — recoverability needs explicit acceptance challenge

Disposition: review AC-LIFE-01 through AC-LIFE-06 for severity, completeness, and non-overlap before freeze.

### GAP-04 — C requires explicit entrance/exit and immutable target identification

Disposition: C entrance/exit are defined in the acceptance-criteria draft; final freeze is recorded outside branch contents against the exact target head.

## Non-claims

This crosswalk does not establish:

- ISO certification;
- NASA process compliance certification;
- NIST SSDF attestation;
- independent IV&V;
- canonical Runtime status;
- deployment readiness beyond the explicitly evaluated acceptance scope;
- subjectivity or consciousness.

## Provenance

- Need for an external public standards ruler: `PROPOSED_BY = HUMAN_OWNER`.
- External calibration research and project mapping: `IMPLEMENTED_BY = CHATGPT`.
- External organizations/standards are calibration sources, not project authors, reviewers, or approvers.
- `CODEX_CONTRIBUTION_THIS_CHANGE = NONE`.
