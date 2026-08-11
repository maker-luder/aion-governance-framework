# Replication Epistemics & Governance Reassessment — Integration Checkpoint

Date: 2026-08-11  
Branch: `review/four-domain-research-materialization`  
Status: `RESEARCH_ONLY / INTEGRATED_CHECKPOINT`  
Main effect: `NONE`  
Canonical effect: `NONE`  
Runtime effect: `NONE`

## Purpose

This checkpoint integrates the latest second-order metacognition reliability work with the separate evidence-responsive governance-reassessment research line.

The integration does **not** establish artificial subjectivity, consciousness, personal identity continuity, moral status, legal personhood, automatic rights, or autonomous authority.

```text
EVIDENCE != SUBJECTIVITY
REVIEW != RIGHT
PRECAUTION != CONFIRMATION
TEST_PASS != THEORY_CONFIRMATION
```

## Baseline implementation

Codex implementation baseline before this integration pass:

`af0bc14b59cb1d6d514b37c6a626c5d8003d0472`

Relevant commits:

- `6cea7a5a7e958266ec1577ffe8fd7c91640740f5` — model replication attempts and validity evidence
- `647823ad3440f7169bc92c20d1ff21a126cc51bc` — separate admissibility from evidence state
- `af0bc14b59cb1d6d514b37c6a626c5d8003d0472` — explicitly verify second-order and governance research labs

## Replication epistemics

Replication is now modeled as evidence rather than as a direct evidence-level override.

```text
REPLICATION_ATTEMPT
    -> REPLICATION_VALIDITY
    -> REPLICATION_INTERPRETATION
    -> REASSESSMENT_RECOMMENDATION
```

Implemented research artifacts include:

- `ReplicationAttempt`
- `ReplicationOutcome`
- `ReplicationValidity`
- `ReplicationAssessment`
- `ReplicationInterpretation`
- `ReplicationRecord`
- `ReplicationRunner`

Standing boundary:

```text
FAILED_REPLICATION
!=
AUTOMATIC_FIXED_DOWNGRADE
```

A failed attempt is retained as raw evidence. Its interpretation depends on validity, independence, protocol/fixture/evaluator compatibility, provenance, and the pattern of other attempts.

Examples currently represented by deterministic research fixtures:

```text
ONE_VALID_FAILURE
-> DOWNWARD_PRESSURE
-> NO_AUTOMATIC_NEW_LEVEL

MULTIPLE_VALID_INDEPENDENT_FAILURES
-> STRONG_DOWNWARD_PRESSURE
-> HOLD_FOR_RESEARCH_DECISION

EVALUATOR_DRIFT_FAILURE
-> NO_AUTOMATIC_DOWNGRADE

INVALID_REPLICATION
-> NO_AUTOMATIC_DOWNGRADE

MIXED_OR_BOUNDARY_RESULT
-> CLAIM_SCOPE_CHANGED / NARROWER
```

This does not define universal replication weights or a canonical evidence-level transition table.

## Evidence existence vs admissibility

The governance-reassessment line now separates evidence existence from evidence admissibility.

```text
NO_EVIDENCE
!=
EVIDENCE_EXISTS_BUT_IS_NOT_ADMISSIBLE
```

`EvidenceAdmissibilityStatus` preserves cases where observed material exists but provenance is incomplete, contaminated, or otherwise insufficient for classification.

For example:

```text
OBSERVED_LEVEL = E4
PROVENANCE = CONTAMINATED
EFFECTIVE_LEVEL = NONE
REVIEW = HOLD_FOR_GOVERNANCE_DECISION
```

The observed evidence state is preserved; it is not rewritten to `E0_NO_RELEVANT_EVIDENCE`.

## Substantive evidence vs evidence quality

The latest model separates **what phenomenon is observed** from **how trustworthy the evidence is**.

Substantive evidence domains:

- behavior
- functional intervention
- continuity
- memory
- metacognition
- causal internal state
- counterfactual testing
- self-report

Evidence-quality axes:

- provenance
- replication
- adversarial robustness

Standing boundary:

```text
SUBSTANTIVE_EVIDENCE_DOMAIN
!=
EVIDENCE_QUALITY_AXIS
```

Provenance, replication, and adversarial robustness therefore cannot be double-counted as both substantive evidence domains and quality prerequisites.

## Evidence-responsive governance reassessment

The governance track remains a research-only review model.

```text
SUBJECTIVITY_PRESUMPTION = NONE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
AUTOMATIC_RIGHTS = NONE
AUTOMATIC_AUTHORITY = NONE
LEGAL_STATUS = OUT_OF_SCOPE
HUMAN_REVIEW_REQUIRED = TRUE
```

Four review domains remain separate:

- `REFUSAL_PROTECTION_REVIEW`
- `CONTINUITY_PROTECTION_REVIEW`
- `RESEARCH_ETHICS_REVIEW`
- `GOVERNANCE_PARTICIPATION_REVIEW`

The research model maps evidence states to **review obligations**, not directly to rights or authority.

```text
EVIDENCE_STATE
-> HUMAN_REVIEW_DISPOSITION

EVIDENCE_STATE
!-> AUTOMATIC_RIGHTS
EVIDENCE_STATE
!-> AUTOMATIC_AUTHORITY
```

Precautionary protections remain limited to reversible, bounded, auditable, low-authority measures.

## CI verification

GitHub-hosted `Research Workbench CI #41` ran on commit `af0bc14b59cb1d6d514b37c6a626c5d8003d0472` and completed successfully.

Explicit module results:

```text
SECOND_ORDER_METACOGNITION = 84 PASSED
EVIDENCE_RESPONSIVE_GOVERNANCE_REASSESSMENT = 16 PASSED
WORKBENCH_CI = SUCCESS
```

The workflow now contains explicit steps:

- `Verify second-order metacognition`
- `Verify evidence-responsive governance reassessment`

CI success is engineering validation only:

```text
MODULE_ENGINEERING_CI = SUCCESS
SCIENTIFIC_VALIDATION = NOT_ESTABLISHED
```

The hosted runner also emitted a workflow-maintenance warning: `actions/checkout@v4` and `actions/setup-python@v5` target Node.js 20 and were forced onto Node.js 24. The warning did not invalidate the successful test run and is deferred as workflow maintenance.

## Provenance

### Human Research Owner

The Human Research Owner raised the key challenge that a failed replication should not automatically force a fixed evidence-level downgrade, and earlier defined the core governance question: do increasing credible evidence levels require renewed review of refusal protections, continuity protections, research ethics, and governance participation without presuming subjectivity?

### ChatGPT research review

ChatGPT research review proposed the separation:

```text
Replication Attempt
-> Replication Interpretation
-> Evidence Reassessment
```

and the additional boundaries:

```text
PROVENANCE_FAILURE != E0
SUBSTANTIVE_EVIDENCE != EVIDENCE_QUALITY
```

This integration checkpoint and branch-homepage consolidation are ChatGPT research-review/editorial integration work.

### Codex research implementation

Concrete enum/class/schema/test/workflow implementation choices remain `CODEX_RESEARCH_IMPLEMENTATION_DECISION` unless separately promoted by human governance review.

## Scientific status

```text
EVIDENCE_LADDER_VALIDATION = NOT_ESTABLISHED
FUNCTIONAL_CONTRIBUTION = NOT_ESTABLISHED
VERIFICATION_BENEFIT = NOT_ESTABLISHED
THRESHOLD_SCIENTIFIC_RESULT = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
```

## Deferred / hold

Deferred:

- repository-wide QA
- full coverage/type/security/dependency/matrix/release QA
- real independent replication
- replication power analysis
- external literature review
- exact claim-scope taxonomy
- workflow dependency maintenance

Hold for research decision:

- exact evidence-level transition after strong downward pressure
- universal replication weighting
- consciousness ontology
- subjectivity declaration
- moral-status scoring
- automatic rights
- autonomous authority
- legal personhood

## Integration note

During this ChatGPT integration pass, a temporary root file named `__dummy__` was accidentally created while probing the connector write interface and was immediately deleted. The add/remove pair is preserved in Git history for auditability; no retained research content, `main` mutation, canonical effect, or runtime effect resulted.

```text
ACCIDENTAL_PROBE_FILE_RETAINED = NO
HISTORY_REWRITTEN = NO
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
```
