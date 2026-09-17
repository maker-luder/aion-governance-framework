# PR #136 Human Owner advice correction — 2026-09-17

Status: `HISTORICAL_CORRECTION / SOURCE_ATTRIBUTION / NO_SCIENTIFIC_CLAIM`

This record preserves a correction explicitly made by the Human Owner after the PR #136 closeout and the PR #139 reimplementation review.

## 1. What is being corrected

The Human Owner now explicitly states that an earlier Human Owner-origin suggestion contributed to the mistaken design direction in which `FREE_SELECTION` was treated as if valid study admission required divergent realized exposure distributions.

The corrected position is:

```text
FREE_SELECTION
MAY_PRODUCE
EQUAL_OR_DIFFERENT_REALIZED_EXPOSURE

REALIZED_DIVERGENCE
= OBSERVED_RESULT
!= DESIGN_ADMISSION_REQUIREMENT
```

A null or equal realized distribution may weaken support for a selective-use hypothesis. It must not be rejected merely because it does not match the expected hypothesis direction.

## 2. Attribution boundary

This correction is deliberately narrow.

```text
HUMAN_OWNER_PRIOR_ADVICE_ERROR = ACKNOWLEDGED
HUMAN_OWNER_PRIOR_ADVICE_ERROR != SOLE_CAUSE_OF_PR136_FAILURE
```

The Human Owner supplied part of the earlier research direction. ChatGPT Teacher / implementation-side formalization was still responsible for challenging that direction against research-design logic instead of encoding it as an admission rule without sufficient falsification checks.

Therefore the historical lesson is not "the Human Owner caused the failure." The supported record is:

1. an earlier Human Owner-origin suggestion was incorrect;
2. the implementation/formalization process did not reject that suggestion early enough;
3. final review later identified the design-identification defect;
4. the Human Owner accepted the correction and explicitly asked that their own mistaken suggestion be recorded;
5. PR #139 reimplements the design so divergence is a derived observation rather than a validity requirement.

```text
SOURCE_ATTRIBUTION != BLAME_ASSIGNMENT
HUMAN_SUGGESTION != AUTOMATIC_RESEARCH_AUTHORITY
AI_FORMALIZATION != AUTOMATIC_RESEARCH_AUTHORITY
DISAGREEMENT_WITH_PRIOR_OWNER_ADVICE = ALLOWED_WHEN_EVIDENCE_OR_DESIGN_LOGIC_REQUIRES_IT
```

## 3. Methodological significance

This correction is useful to the repository because it demonstrates a concrete case of bidirectional calibration:

```text
HUMAN_PROPOSES
-> AI_FORMALIZES
-> REVIEW_CHALLENGES
-> DEFECT_IDENTIFIED
-> HUMAN_REVISES_PRIOR_POSITION
-> IMPLEMENTATION_REVISED
```

The value of the event is procedural, not evidentiary proof of the research hypothesis.

```text
CORRECTION_EVENT != SCIENTIFIC_VALIDATION
SELF_CORRECTION != HUMAN_INFALLIBILITY
AI_CHALLENGE != AI_AUTHORITY
REVISED_IMPLEMENTATION != EMPIRICAL_CONFIRMATION
```

## 4. Relation to repository records

Relevant records:

- `docs/history/PR136_CLOSEOUT_AND_NEXT_IMPLEMENTATION_HANDOFF_2026_09_17.md`
- `docs/research/TASK_SELECTION_YOKED_CONTROL_AND_TEMPORAL_PROVENANCE_2026_09_17.md`
- PR #136: closed, unmerged historical candidate
- PR #139: fresh reimplementation candidate

This file does not rewrite the historical record. It adds the Human Owner's later explicit correction so future reviewers do not incorrectly attribute the original divergence requirement solely to AI implementation or, conversely, treat Human Owner guidance as exempt from methodological challenge.

## 5. Standing boundaries

```text
OWNER_ORIGIN != VALIDATED_CLAIM
AI_ORIGIN != VALIDATED_CLAIM
EVIDENCE != PROOF
CI_PASS != SCIENTIFIC_VALIDATION
PR139_REIMPLEMENTATION != EMPIRICAL_RESULT
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```
