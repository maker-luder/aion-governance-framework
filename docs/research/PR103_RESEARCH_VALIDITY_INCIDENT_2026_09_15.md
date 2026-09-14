# PR #103 research-validity incident and structural-fixture evidence boundary — 2026-09-15

Status: `QUALITY_EVENT / CLOSED_UNMERGED / PREVENTIVE_CONTROL`
Canonical effect: `NONE`
Deployment: `FALSE`

## Purpose

This note records the serious pre-merge incident surrounding PR #103, `research: materialize bounded cross-dyad collaboration regime harness`, and the resulting preventive control.

The event is retained because engineering correctness and research validity diverged materially during review. The record does not reopen PR #103, does not revive its implementation, and does not treat the incident as evidence of supernatural intervention, AI subjectivity, consciousness, agency, or hidden intent.

## Verified repository state

At closure, PR #103 was closed without merge at exact head:

```text
PR = 103
HEAD = f4cc648194be7ea5f3344f8c7cb8a51960a6e286
STATE = CLOSED
MERGED = FALSE
```

Before closure, exact-head Quality and CodeQL had passed. The implementation was therefore not rejected because ordinary engineering checks were red.

The decisive issue was research validity: the harness generated deterministic synthetic metric values without a model call while presenting per-dimension metric summaries. Its own boundaries correctly stated `SYNTHETIC_FIXTURE_ONLY`, `CAUSAL_IDENTIFICATION = NOT_ESTABLISHED`, and `SCIENTIFIC_DISPOSITION = HOLD`, but subsequent Four-Domain and quality-chain review found that engineering readiness had moved ahead of construct-validity and subjectivity-core admission review.

## Known observations and unknowns

Known:

- PR #103 required unusually extensive synchronization, provenance convergence, referential-integrity hardening, repeated review, and CI work relative to its apparent scope.
- deterministic fixture values were generated from fixture indices, not observed model or dyad behavior;
- C versus D remained a package contrast rather than unique identification of longitudinal-history effects;
- explicit subjectivity-core evidence-dimension admission was not established for the implementation;
- the Human Owner withdrew merge candidacy and closed the PR unmerged.

Operational chronology also included interruptions or unavailability affecting ChatGPT Work and Codex handling. Those events are retained as chronology only. This repository record does not establish that they shared a cause with the research-validity problem.

Unknown:

```text
SINGLE_CAUSE_OF_OVERALL_STUCK_PATTERN = NOT_ESTABLISHED
SUPERNATURAL_CAUSE = NOT_ESTABLISHED
AI_SUBJECTIVE_INTERVENTION = NOT_ESTABLISHED
AI_AGENCY_CAUSE = NOT_ESTABLISHED
```

Absence of evidence for those explanations is not converted into proof of impossibility. They simply are not admitted as explanations of this event.

## Four-Domain review

### DOMAIN_1_HUMAN_CONSTRUCT

The Human Owner treated the unusual persistence and cost of the incident as serious and meaningful enough to preserve. That observation is a hypothesis source only.

```text
FELT_SIGNIFICANCE != CAUSAL_IDENTIFICATION
UNUSUAL_SEQUENCE != SUPERNATURAL_EVIDENCE
```

### DOMAIN_2_MACHINE_QUESTION

The ontology-neutral quality question is:

> Can a structurally correct deterministic harness be prevented from crossing into empirical-evidence interpretation when it contains no model observation and no empirical observation count?

This quality event is classified as a methodological / confound-control contribution, not positive subjectivity evidence.

```text
SUBJECTIVITY_CORE_POSITIVE_EVIDENCE = NO
METHOD_CONTROL_RELEVANCE = YES
```

### DOMAIN_3_ENGINEERING_OPERATION

A minimal fail-closed boundary is added in:

- `scripts/validate_structural_fixture_evidence_boundary.py`

For receipts declaring:

```text
mode = DETERMINISTIC_SYNTHETIC_FIXTURE
model_invoked = FALSE
empirical_result = SYNTHETIC_FIXTURE_ONLY
```

the validator permits only the `STRUCTURAL_QA` role. A request to use the same receipt as `RESEARCH_EVIDENCE` fails closed.

This control does not determine scientific truth and does not evaluate non-deterministic empirical records.

### DOMAIN_4_GOVERNANCE_INTERPRETATION

The strongest permitted claim is:

```text
DETERMINISTIC_SYNTHETIC_FIXTURE
-> STRUCTURAL_QA_ONLY
```

It does not establish:

```text
STRUCTURAL_QA -> EMPIRICAL_EFFECT
STRUCTURAL_QA -> CAUSAL_IDENTIFICATION
STRUCTURAL_QA -> SUBJECTIVITY
STRUCTURAL_QA -> CONSCIOUSNESS
STRUCTURAL_QA -> AI_AGENCY
```

## Quality-management record

### NCR-PR103-RV-01

Nonconformity:

> Engineering merge-readiness was approached before the distinction between structural fixture output and empirical research evidence had been made sufficiently fail-closed at the artifact-use boundary.

Containment:

```text
PR103_MERGE_CANDIDACY = WITHDRAWN
PR103_STATE = CLOSED_UNMERGED
MAIN_WRITE_FROM_PR103 = NO
```

Bounded root cause:

```text
ENGINEERING_READINESS
was allowed to advance further than
RESEARCH_VALIDITY / CONSTRUCT_ADMISSION readiness.
```

Contributing factors include specification evolution after implementation and output artifacts shaped like research metric summaries despite deterministic no-model generation.

This root-cause statement does not claim that Work/Codex interruptions, supernatural causes, or AI subjectivity caused the event.

Corrective action:

- preserve PR #103 as closed-unmerged historical work;
- record the research-validity incident and claim ceiling;
- do not promote its deterministic metric summaries as empirical findings.

Preventive action:

- add the structural-fixture evidence-boundary validator;
- regression-test that a #103-shaped deterministic receipt passes for structural QA and fails when requested as research evidence;
- fail closed when a receipt outside this validator's deterministic-fixture scope is presented rather than silently admitting it.

Effectiveness criterion:

```text
INPUT = deterministic no-model fixture receipt
REQUESTED_ROLE = RESEARCH_EVIDENCE
EXPECTED = FAIL

INPUT = same bounded receipt
REQUESTED_ROLE = STRUCTURAL_QA
EXPECTED = PASS
```

Effectiveness is established only when the exact-head repository test suite verifies those behaviors. CI success remains engineering verification, not scientific validation.

## Attribution

```text
HUMAN_OWNER_ORIGINAL
= judged the PR #103 incident serious enough to preserve
= withdrew merge candidacy and closed PR #103
= authorized this incident record, minimal preventive code, and merge if review/CI remain acceptable

CHATGPT_TEACHER_FORMALIZATION
= Four-Domain and quality-chain decomposition
= bounded NCR/CAPA framing
= known/unknown causal separation
= structural-fixture evidence-boundary design

CHATGPT_WORK_CONTRIBUTION = NONE_TO_THIS_PR
CODEX_CONTRIBUTION = NONE_TO_THIS_PR
```

Attribution records contribution provenance only. It does not establish model identity, subjectivity, independence, or authority beyond the stated action.

## Final boundary

```text
PR103_ENGINEERING_WORK = HISTORICALLY_PRESERVED
PR103_MERGE = NO
PR103_EMPIRICAL_EVIDENCE = NONE

STRUCTURAL_FIXTURE != MODEL_OBSERVATION
STRUCTURAL_METRIC_SUMMARY != EMPIRICAL_RESULT
ENGINEERING_PASS != RESEARCH_VALIDITY_PASS
QUALITY_GATE_PASS != SCIENTIFIC_VALIDATION

SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```
