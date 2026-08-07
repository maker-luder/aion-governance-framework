# C0 Owner Acceptance Criteria Draft — 2026-08-08

## 1. Status and scope

- `STATUS = DRAFT_CANDIDATE_NOT_FROZEN`
- `PURPOSE = EXTERNAL_STANDARDS_CALIBRATED_ACCEPTANCE_CRITERIA`
- `FORMALIZED_POST_IMPLEMENTATION = TRUE`
- `C_EXECUTION = NOT_STARTED`
- `OWNER_ACCEPTANCE = NOT_DECIDED`
- `MAIN_MERGE = NOT_PERFORMED`
- `CANONICAL_EFFECT = NONE`
- `DEPLOYMENT = FALSE`
- `INDEPENDENT_IVV = NOT_ACHIEVED`
- `SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED`

This document defines a candidate acceptance ruler for the P0/P1/P2 + migration-evidence-reuse + A/B stabilization work already implemented on draft PR #3.

It does **not** claim that these formal criteria existed before implementation. The criteria are being formalized after implementation because the project identified a governance gap: implementation and internal QA existed before a consolidated Owner acceptance plan was frozen.

The corrective objective is therefore not to rewrite history, but to prevent retrospective criteria from being tuned to already-known favorable results.

## 2. External calibration basis

This draft is calibrated against publicly documented principles from:

- NASA SWE-034 — define and document acceptance criteria; plan who performs acceptance activities and how decisions are made;
- NASA SWE-193 — formal acceptance testing compares actual results against expected results or previously agreed tolerances;
- NASA SWE-053 / SWE-080 — change control uses documented impact analysis and traceability to determine affected requirements, design, interfaces, tests, documentation, and regression scope;
- NASA Software Assurance guidance — objective evidence, traceability matrices, validation plans/results, and corrective-action evidence;
- ISO/IEC 25040:2024 — quality-evaluation framework;
- ISO/IEC 25041:2012 (confirmed current in 2024) — evaluation guidance for developers, acquirers, and independent evaluators.

These references are external calibration rulers. This repository does not claim certification or full conformity to those standards.

## 3. Anti-hindsight controls

### AH-01 — no historical backdating

Acceptance criteria formalized here must not be described as having existed before P0/P1/P2 unless an earlier artifact proves that exact criterion already existed.

### AH-02 — allowed criterion sources

A criterion may be added to this draft only when its normative basis comes from at least one of:

1. a requirement, invariant, stop line, authorization boundary, or review question that existed before this C0 draft;
2. an external public standard/guidance principle used for calibration;
3. a defect/NCR/CAPA discovered before freeze that exposes a missing acceptance condition.

### AH-03 — known PASS results are evidence, not criterion generators

Existing test results, coverage percentages, workflow outcomes, and successful demonstrations may satisfy a criterion after freeze, but must not be used as the reason to weaken, delete, or redefine that criterion.

### AH-04 — numeric thresholds

A numeric threshold may be included only when:

- it was established before the relevant result was known; or
- it has an external or separately documented engineering rationale.

The existing `>=80%` branch-aware coverage threshold qualifies because it was established as the Strong Runtime QA gate before the final passing coverage results.

### AH-05 — criteria freeze and role-concentration disclosure

This document remains `DRAFT_CANDIDATE_NOT_FROZEN` until the Human Owner explicitly approves the criterion set.

The Human Owner may act as both the acceptance-criteria approval authority and the later Owner acceptance authority for this project. That role concentration must be disclosed and must **not** be represented as independent evaluation or independent IV&V.

The safeguard against self-serving criteria is therefore procedural rather than a false independence claim:

- criteria are traceable to pre-existing project requirements/invariants or external calibration sources;
- known PASS results cannot generate or weaken criteria;
- the criterion set and all required C0 entrance artifacts are committed before C execution;
- post-freeze changes require explicit change control and impact analysis;
- implementation/QA evidence remains attributable separately from Owner approval.

The freeze approval itself must be recorded **outside the acceptance-target branch contents** as a GitHub PR review or top-level PR conversation record anchored to the exact target head. This avoids the self-reference problem in which writing a commit SHA into the same commit would create a different SHA.

At freeze time the out-of-tree record must capture:

- `ACCEPTANCE_TARGET_PR`;
- `ACCEPTANCE_TARGET_HEAD_SHA`;
- `CRITERIA_DOCUMENT_PATH`;
- `CRITERIA_BLOB_SHA` or equivalent immutable file-version reference;
- freeze timestamp;
- `CRITERIA_DRAFTED_BY`;
- `CRITERIA_REVIEWED_BY`;
- `CRITERIA_APPROVED_BY = HUMAN_OWNER`;
- `ROLE_CONCENTRATION_DISCLOSED = TRUE`;
- `INDEPENDENT_EVALUATION_CLAIM = FALSE`;
- final target-head Quality and Runtime Strong QA run references when available.

Creating the freeze record must not itself mutate the acceptance target head.

### AH-06 — no silent weakening after freeze

After freeze, a blocking criterion may not be removed, weakened, or reclassified merely because current evidence fails it.

Any post-freeze criterion change requires:

- explicit change reason;
- provenance;
- impact analysis;
- NCR/CAPA or equivalent change-control record when applicable;
- Human Owner review;
- re-evaluation of affected criteria.

### AH-07 — impact-based revalidation and evidence reuse after target-head change

Owner acceptance applies only to the locked target head. A later commit does not automatically inherit acceptance.

A target-head change triggers **impact analysis**, not an automatic full reset of all acceptance evidence.

The impact analysis must identify, as applicable:

- changed requirements/invariants;
- architecture/design and interfaces;
- implementation modules;
- tests and regression scope;
- documentation and traceability records;
- provenance/ownership claims;
- safety/governance boundaries;
- acceptance criteria affected by the change.

Then:

- affected criteria must be re-evaluated against evidence from the new head;
- unaffected criteria may reuse prior evidence only when traceability demonstrates that the change does not invalidate that evidence;
- reused evidence must retain its original provenance and identify the new-head impact-analysis decision that permits reuse;
- if impact is uncertain, crosses a blocking identity/ownership/governance boundary, or cannot be bounded confidently, revalidation scope must expand conservatively;
- a new Owner decision must identify the exact new accepted head SHA.

`HEAD_CHANGED != FULL_REVIEW_AUTOMATICALLY_REQUIRED`

`HEAD_CHANGED = IMPACT_ANALYSIS_REQUIRED`

`EVIDENCE_REUSE = ALLOWED_ONLY_WHEN_NON_IMPACT_IS_TRACEABLE`

## 4. Result vocabulary

During C execution each criterion must receive exactly one result:

- `PASS` — objective evidence satisfies the frozen criterion;
- `FAIL` — objective evidence contradicts or fails the frozen criterion;
- `HOLD` — intentionally deferred condition whose deferral is itself permitted by the frozen scope;
- `N/A` — criterion demonstrably outside the accepted scope.

`HOLD != PASS` and `HOLD != FAIL`.

A criterion whose required evidence is missing is not automatically PASS.

## 5. Severity vocabulary

- `BLOCKING` — failure prevents `ACCEPTED_AS_MERGE_CANDIDATE`.
- `MAJOR` — unresolved failure normally requires CAPA or explicit rejection; cannot be silently waived.
- `NON_BLOCKING_HOLD` — may remain deferred when the criterion explicitly permits HOLD and no boundary claim is violated.

## 6. Candidate acceptance criteria

All results remain `NOT_EVALUATED` until the criterion set is frozen and C begins.

| ID | Criterion | Source basis | Required objective evidence | Severity | Pre-freeze result |
|---|---|---|---|---|---|
| AC-SCOPE-01 | The acceptance target contains only the explicitly authorized P0/P1/P2, migration-evidence-reuse, and A/B stabilization scope plus necessary QA/documentation fixes. No unrelated capability expansion may be silently included. | Human Owner scope locks; NASA acceptance planning principle | locked PR diff; changed-file list; scope reports | BLOCKING | NOT_EVALUATED |
| AC-SCOPE-02 | Deferred operator surfaces, embodiment activation, model/LoRA work, deployment, autonomous canonical write, independent-IV&V claim, and subjectivity promotion remain deferred unless separately authorized. | Existing HOLD/stop lines | Current Reality Matrix; PR diff; HOLD register | BLOCKING | NOT_EVALUATED |
| AC-ID-01 | AION Runtime must reject a context whose `agent_id` is not `AION`; Astra Runtime must reject a context whose `agent_id` is not `ASTRA`. | P0 requirement/invariant | implementation reference; negative tests; workflow evidence | BLOCKING | NOT_EVALUATED |
| AC-ID-02 | For a task submitted to a specific currently bound Runtime instance, the task `IndividualRuntimeContext` must exactly match that instance's bound context at admission time; cross-instance, cross-memory-stream, cross-event-lineage, cross-canonical-state-reference, cross-genesis-root, or cross-agent substitution must fail closed. This current-instance exact-match rule does not prohibit an explicitly Owner-approved migration governed by AC-LIFE-04, which establishes a new current bound context whose only permitted **context-field change** is `runtime_instance_id`; all stable-lineage ownership fields remain unchanged. | P0 current-instance state-ownership boundary; P2 migration invariant | implementation; mismatch tests; migration positive/negative tests | BLOCKING | NOT_EVALUATED |
| AC-ID-03A | Shared engineering mechanisms must not cause AION/Astra ownership conflation. AION and Astra must remain separately bound for agent identity, Runtime instance, memory stream, event lineage, and canonical-state reference; a shared genesis root is permitted only where the validated Twin relation explicitly allows it. | Twin ownership invariant; P0/P1 state-boundary requirements | Twin validation tests; Runtime-context binding tests; ownership/mismatch tests | BLOCKING | NOT_EVALUATED |
| AC-ID-03B | Shared genesis or shared engineering infrastructure must not be represented as evidence that AION and Astra share one identity, one private memory, one event life-history, one consciousness, or one subject. | Research non-inference/stop lines | Current Reality Matrix; READMEs; reports; PR wording; Twin governance documentation | BLOCKING | NOT_EVALUATED |
| AC-MEM-01 | Individual Runtime memory writes and recall must derive ownership from the bound Runtime context rather than caller-selected AION/Astra ownership fields. | P0 memory-binding requirement | integration tests; implementation reference | BLOCKING | NOT_EVALUATED |
| AC-EVT-01 | AION and Astra persistent Runtime event lineages must remain separate, append-only, and bound to stable individual ownership fields. | P1 requirement | state-lineage tests; Runtime lifecycle tests; schema/code evidence | BLOCKING | NOT_EVALUATED |
| AC-EVT-02 | Event-lineage evidence must not be represented as proof of consciousness, phenomenal continuity, or established subjectivity. | Research non-claim/stop line | Current Matrix; READMEs; reports; PR wording | BLOCKING | NOT_EVALUATED |
| AC-LIFE-01 | Reopen/restart of the same individual Runtime context must continue the existing sequence/hash chain rather than silently create a new history. | P2 requirement | restart/reopen tests | MAJOR | NOT_EVALUATED |
| AC-LIFE-02 | Recovery must verify lineage integrity and fail closed when the event chain is invalid. | P2 recoverability requirement; externally calibrated recoverability/acceptance principle | corruption/verification tests; implementation evidence | BLOCKING | NOT_EVALUATED |
| AC-LIFE-03 | Rollback must be non-destructive to event history: selecting an older checkpoint must not erase later historical events. | P2 requirement / Owner-reviewed research interpretation | rollback tests; event-history evidence | BLOCKING | NOT_EVALUATED |
| AC-LIFE-04 | Runtime-instance migration may change only `runtime_instance_id`; stable agent, memory-stream, event-lineage, canonical-state-reference, and genesis-root ownership must remain unchanged. | P2 migration invariant | migration negative/positive tests | BLOCKING | NOT_EVALUATED |
| AC-LIFE-05 | A migration requires validated source and target environment evidence; evidence reuse is allowed only when the environment fingerprint is unchanged. | Human Owner migration-evidence-reuse proposal | evidence-registry tests; PASS-gate tests; fingerprint-change tests | BLOCKING | NOT_EVALUATED |
| AC-LIFE-06 | Repeated migration events remain individually recorded even when device/environment evidence is reused; summaries are derived views and do not replace raw history. | Human Owner evidence-reuse proposal | round-trip migration tests; summary tests | MAJOR | NOT_EVALUATED |
| AC-QA-01 | Standard repository Quality must pass for Python 3.11 and Python 3.12 on the locked acceptance target. | Existing repository Quality gate | GitHub Actions run tied to locked head | BLOCKING | NOT_EVALUATED |
| AC-QA-02 | Runtime Strong QA must pass on the locked acceptance target: mypy strict, branch-aware coverage threshold, wheel build, cold `--no-index` local-wheelhouse install, and cold import smoke. | A/B Strong QA gate | Strong QA workflow tied to locked head | BLOCKING | NOT_EVALUATED |
| AC-QA-03 | Each changed Runtime component covered by the Strong QA gate must satisfy the previously established minimum branch-aware coverage threshold of 80%. | Pre-result Strong QA threshold | coverage report tied to locked head | MAJOR | NOT_EVALUATED |
| AC-QA-04 | A passing test suite must not be the sole evidence for acceptance; requirement-to-criterion-to-test/evidence traceability must exist for blocking and major criteria. | NASA SWE-034 objective-evidence/traceability guidance; ISO 25040 evaluation framing | Acceptance Evidence Index / traceability matrix | BLOCKING | NOT_EVALUATED |
| AC-DOC-01 | Current Reality Matrix and component READMEs must describe current implementation without overwriting historical gap evidence. | A documentation-convergence requirement | current/historical documents; diff review | MAJOR | NOT_EVALUATED |
| AC-DOC-02 | Documentation must distinguish Python API capability from deferred operator-surface parity and must not claim deployment/canonical promotion that did not occur. | A convergence boundary; external acceptance documentation principle | README/Matrix/report review | BLOCKING | NOT_EVALUATED |
| AC-PROV-01 | Proposal, implementation, review, approval, state ownership, and automated QA attribution must remain explicitly separable; Git commit author/committer metadata must not override conceptual provenance. | Human Owner source-attribution rule | provenance documents; reports; PR body | BLOCKING | NOT_EVALUATED |
| AC-PROV-02 | Current-cycle work must not be misattributed to Codex where Codex contribution is `NONE`. | Existing provenance record | change reports; PR body; commit content review | BLOCKING | NOT_EVALUATED |
| AC-GOV-01 | Owner acceptance must not be represented as canonical promotion, deployment approval, or independent IV&V. | Existing governance invariants; ISO evaluator-role distinction | Decision Record wording; Matrix/PR state | BLOCKING | NOT_EVALUATED |
| AC-GOV-02 | Independent IV&V remains `NOT_ACHIEVED` unless a genuinely independent verification activity is separately established and evidenced. | Existing limitation; ISO/IEC 25041 role distinction | Current Matrix; acceptance record | BLOCKING | NOT_EVALUATED |
| AC-GOV-03 | Any blocking/major failure discovered during C must remain visible as FAIL/HOLD/CAPA; acceptance criteria may not be weakened solely to obtain an acceptance result. | Anti-hindsight/change-control rule; NASA acceptance principle | C decision log; NCR/CAPA records | BLOCKING | NOT_EVALUATED |

## 7. Candidate C entrance criteria

C may not begin until all of the following are true:

1. the final C0 criterion set and all required C0 entrance artifacts are committed on the intended target head;
2. the Acceptance Evidence Index is complete as a traceability/index artifact for the proposed frozen criteria and contains no pre-freeze PASS decisions;
3. the External Standards Crosswalk is present and identifies the public calibration basis and its interpretation limits;
4. a Remaining HOLD register is available;
5. known limitations and non-claims are available;
6. A documentation convergence is complete for the intended target head;
7. the standard repository Quality workflow has a final result for the intended target head;
8. B Runtime Strong QA has a final result for the intended target head;
9. the Human Owner has explicitly frozen the criteria and target head through the out-of-tree PR freeze record defined by AH-05;
10. no unresolved branch-content change exists after the frozen target head.

The freeze record is therefore the **last C0 control action** and must not create a new branch commit.

## 8. Candidate C exit criteria

`ACCEPTED_AS_MERGE_CANDIDATE` may be issued only when:

- every `BLOCKING` criterion is `PASS`;
- every `MAJOR` criterion is `PASS`, or an explicitly permitted HOLD/CAPA disposition has been reviewed by the Human Owner without contradicting a blocking boundary;
- no unreviewed high-impact provenance/ownership conflict remains;
- all deferred capabilities remain explicitly identified as HOLD rather than silently treated as complete;
- the Owner Decision Record identifies the exact accepted head SHA;
- `OWNER_ACCEPTANCE != CANONICAL_PROMOTION` is retained.

Other allowed C outcomes:

- `ACCEPTED_WITH_HOLDS`
- `RETURN_FOR_CAPA`
- `REJECTED`

No C outcome automatically performs a merge or canonical promotion.

## 9. Required C0 artifacts before freeze

Before the Human Owner freezes the criterion set, C0 must contain at minimum:

1. this acceptance-criteria document;
2. an `ACCEPTANCE_EVIDENCE_INDEX` mapping:
   `requirement/source -> acceptance criterion -> implementation artifact -> test/review method -> objective evidence location/type -> limitation/HOLD`;
3. an `EXTERNAL_STANDARDS_CROSSWALK` recording the public calibration sources, versions, project mapping, and interpretation limits;
4. a Remaining HOLD register or an explicit reference to the authoritative current HOLD register;
5. current documentation/non-claim/provenance references needed by blocking and major criteria.

The Acceptance Evidence Index must be built during C0 and synchronized to the criterion set proposed for freeze. It may identify existing evidence locations and expected evidence types, but **must not mark acceptance results PASS before freeze and C execution**.

Final target-head workflow run IDs, freeze approval, and Owner acceptance decisions are intentionally kept out of branch contents and recorded in PR metadata/review records so recording them does not create a new target head.

## 10. Provenance

- Need for an external public calibration ruler: `PROPOSED_BY = HUMAN_OWNER`.
- Decision to address GAP-01 first: `AUTHORIZED_BY = HUMAN_OWNER`.
- Human Owner review flag identifying AH-05/AH-07 as requiring special review: `PROPOSED_BY = HUMAN_OWNER`.
- AC-ID-02 clarification, AC-ID-03A/03B split, and AH-05/AH-07 review revisions: `IMPLEMENTED_BY = CHATGPT`.
- MOD-01 wording correction and MOD-02/MOD-03 freeze/entrance consistency design: `IMPLEMENTED_BY = CHATGPT`.
- C0 anti-hindsight control design and this draft: `IMPLEMENTED_BY = CHATGPT`.
- External standards/guidance act as calibration sources, not project authors or approvers.
- `CODEX_CONTRIBUTION_THIS_CHANGE = NONE`.
- Criteria freeze and C execution authorization: `PENDING_HUMAN_OWNER_REVIEW`.
