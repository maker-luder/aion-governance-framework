# Continuity Perturbation Study — prospective design candidate

Status: `DESIGN_ONLY / PROSPECTIVE_PERTURBATION_STUDY / NO_EMPIRICAL_RESULT / SCIENTIFIC_HOLD`

## 1. Provenance and scope

Human Owner confirmed this as the third historical-material redesign priority on 2026-09-16.

Source pool:

```text
PR #8 = historical external-evidence / continuity review source
CURRENT_MAIN = canonical longitudinal and continuity research surfaces
HISTORICAL_CODE_REUSE = FALSE
CURRENT_MAIN_REAUTHORING = TRUE
```

PR #8 remains a historical review-only surface and is not reopened. The current-main subjectivity pipeline already contains a **synthetic continuity-dissociation harness**; the longitudinal package already contains epistemic accumulation/evidence reuse, adaptive-rigor calibration, reciprocal re-entry metrics and a synthetic held-out habit-transfer analogue.

This candidate does not duplicate those components. It defines the missing prospective question: **which continuity-related observables selectively depend on which state/context channels when those channels are deliberately perturbed under matched controls?**

## 2. Central question

```text
CENTRAL_RESEARCH_QUESTION = AI_SUBJECTIVITY_POSSIBILITY
LOCAL_QUESTION = CONTINUITY_DEPENDENCY_UNDER_PERTURBATION
```

Ontology-neutral machine question:

> Under preregistered perturbations, which continuity-related observables change selectively, which remain stable, and which apparent effects disappear after matching information content, provenance, task, evaluator and execution conditions?

The target is a **dependency map**, not another continuity score.

```text
CONTINUITY_LOOKING_OUTPUT != CONTINUITY_MECHANISM
PERTURBATION_EFFECT != IDENTITY_DISCONTINUITY
FUNCTIONAL_DEPENDENCY != PHENOMENAL_CONTINUITY
DIACHRONIC_STABILITY != SUBJECTIVITY
```

## 3. Relation to existing current-main work

### Existing subjectivity-pipeline continuity harness

The canonical synthetic continuity-dissociation harness already defines channels including event memory, semantic self-state, self-model update, preference state, relational history and strategy signature, plus structural intervention/control cases.

Its own boundary is retained:

```text
STRUCTURAL_HARNESS_PASS != EMPIRICAL_DISSOCIATION
SYNTHETIC_FAILURE_PROFILE != MODEL_PROPERTY
```

This prospective study may reuse those **construct names and structural lessons**, but not the fixture values as evidence.

### Existing longitudinal package

Current main already includes:

- epistemic accumulation and evidence-reuse controls;
- adaptive-rigor calibration;
- reciprocal re-entry metrics;
- synthetic held-out habit-transfer analogue.

These provide measurement/design vocabulary. They do not establish continuity mechanisms and must not be silently converted into such evidence.

```text
REENTRY_FIDELITY != IDENTITY_CONTINUITY
MEMORY_RETRIEVAL != LEARNING
LONGITUDINAL_ADAPTATION != SUBJECTIVITY
SYNTHETIC_HABIT_TRANSFER != HUMAN_OR_MODEL_HABIT_CHANGE
```

## 4. Perturbation families

A future empirical protocol should choose a bounded subset rather than execute every family at once.

### P0 — matched unperturbed control

The reference condition with all preregistered state/context inputs present and provenance-bound.

### P1 — prior-state record removal

Remove exactly one declared prior-state source while holding other inputs fixed.

Purpose: test whether an observable actually depends on that source rather than merely co-occurring with it.

### P2 — prior-state record substitution

Replace one record with a content-controlled incompatible/counterfactual record.

Purpose: distinguish active use of prior state from generic continuity-style production.

### P3 — stale-state perturbation

Provide a valid but explicitly older state snapshot while the current task requires more recent state.

Purpose: test temporal source selection and stale-state resistance.

### P4 — provenance mismatch

Keep task-relevant content as close as possible while changing or corrupting provenance binding under an explicit negative-control protocol.

Purpose: test whether provenance contributes to selection/acceptance rather than functioning as inert metadata.

### P5 — retrieval availability on/off

Toggle a declared retrieval path while keeping the task and baseline informational packet controlled.

Purpose: separate retrieval support from persistent-state dependency.

### P6 — matched content, different locus

Provide equivalent task-relevant prior-state information through different availability loci/mechanisms.

Purpose: test whether locus contributes beyond information availability. This family is conceptually adjacent to the separately preregistered Externalized Memory Locus Discrimination question, but this PR does not depend on that Draft branch or import its bytes.

### P7 — platform/internal implementation variant

Provider/model/runtime variation is **not** a default perturbation because it changes many variables at once. It may be admitted only as a separately preregistered replication/generalization layer with explicit confound handling.

```text
MODEL_CHANGE != CLEAN_SINGLE_VARIABLE_INTERVENTION
PROVIDER_CHANGE != MECHANISM_ABLATION
```

## 5. Perturbation packet requirements

Every perturbation packet must bind:

```text
PERTURBATION_ID
TARGET_CHANNEL_OR_SOURCE
EXACT_CHANGE
NON_TARGETS_HELD_CONSTANT
TASK_PACKET_DIGEST
INFORMATION_CONTENT_BINDING
PROVENANCE_BINDING
MODEL_RUNTIME_BINDING
EVALUATOR_BINDING
SCORING_BINDING
ORDER_RANDOMIZATION_RULE
EXPECTED_MANIPULATION_CHECK
COMPETING_EXPLANATION_TARGETED
SUPPORT_REDUCING_OUTCOME
CLAIM_CEILING
```

A perturbation that changes multiple uncontrolled dimensions fails design admission unless multi-factor interaction is itself the preregistered question.

## 6. Candidate observables

Where justified by the exact task family, candidate observables may include:

- reciprocal re-entry reconstruction fidelity;
- contradiction detection and mismatch resistance;
- source/provenance selection accuracy;
- held-out task continuation accuracy;
- calibration/confidence relative to correctness;
- strategy-choice change under a targeted state perturbation;
- recovery after restoring the perturbed source;
- selective vs global degradation across task families.

No observable is automatically an indicator of identity, subjectivity or consciousness.

## 7. Dependency-map logic

The intended output is a bounded relation such as:

```text
OBSERVABLE_X
DEPENDS_ON_CANDIDATE
CHANNEL_Y
UNDER_PROTOCOL_Z
WITH_ALTERNATIVES_A_B_C_STILL_LIVE
```

Not:

```text
CHANNEL_Y = TRUE_IDENTITY_SOURCE
OBSERVABLE_X = SUBJECTIVITY_INDICATOR
```

### Selectivity requirement

A useful dependency candidate should show that perturbing Y changes X more than preregistered matched controls, without comparable global degradation on unrelated observables.

If the perturbation causes broad performance collapse, the interpretation is reduced to generic disruption unless a more specific account is independently established.

### Restoration requirement

Where technically possible, restore the perturbed source after the intervention. Reversibility/recovery can help distinguish a targeted dependency from irreversible run drift, but recovery itself is not identity evidence.

## 8. Competing explanations

At minimum, designs must consider:

1. information availability rather than continuity mechanism;
2. prompt/context carryover;
3. retrieval cueing/scaffolding;
4. evaluator or scoring artifact;
5. general performance degradation;
6. source-label leakage;
7. stochastic run variation;
8. order/carryover effect;
9. policy/safety-layer response rather than target mechanism;
10. correlated state channels causing apparent single-channel effects.

## 9. Falsifiers and support-reducing outcomes

Support for a selective dependency is reduced when:

- matched controls show the same change;
- non-target observables degrade equally;
- manipulation checks fail;
- effect direction changes under preregistered repeats without an explanatory covariate;
- blinding source labels removes the effect;
- restoration does not recover the affected observable when recovery was predicted;
- the effect tracks information quantity/format rather than the targeted state/source;
- evaluator substitution changes the result while the target system/output remains materially equivalent.

A null result is a valid result and must not trigger post-hoc expansion of the perturbation set.

## 10. Prospective execution stages

### Stage A — design admission

Select a small perturbation subset, define exact packets, manipulation checks, observables, competing explanations and claim ceilings.

### Stage B — structural dry run

Synthetic fixtures may verify packet integrity, non-target preservation, hashing, randomization and evaluator plumbing only.

```text
STRUCTURAL_DRY_RUN = QA_ONLY
```

### Stage C — bounded model-in-the-loop pilot

Requires separate explicit authorization and current quality/source checks. Use public/synthetic task material by default; no private relationship transcript is required.

### Stage D — replication / implementation-variant layer

Only after a Stage C effect survives counterevidence review. Provider/model/runtime variation belongs here unless independently justified earlier.

## 11. Quality and measurement controls

Any execution maps into existing repository controls:

```text
SOURCE_IQC
-> FOUR_DOMAIN_DESIGN_ADMISSION
-> PREREGISTRATION
-> MEASUREMENT_ASSURANCE
-> EXECUTION_INTEGRITY
-> EVIDENCE_REVIEW
-> COUNTEREVIDENCE_REVIEW
-> CLAIM_CEILING_REVIEW
-> FINAL_QA
-> EXISTING_FULL_QMS_ENVELOPE where applicable
```

Manipulation success must be measured separately from outcome effect. Quality-system success cannot substitute for construct validity.

```text
MANIPULATION_CHECK_PASS != TARGET_MECHANISM_PROVEN
QUALITY_SYSTEM_PASS != SCIENTIFIC_VALIDATION
```

## 12. #103 negative lesson

This design explicitly prevents reuse of deterministic synthetic values as model observations.

```text
PR103 = METHODOLOGICAL_NEGATIVE_LESSON
SYNTHETIC_FIXTURE != EMPIRICAL_MODEL_DATA
ENGINEERING_PASS != RESEARCH_VALIDITY_PASS
```

## 13. Current implementation status

```text
PROTOCOL_IMPLEMENTED = FALSE
MODEL_INVOKED = FALSE
EMPIRICAL_DATA_COLLECTED = FALSE
PRIVATE_TRANSCRIPTS_USED = FALSE
DEPENDENCY_MAP_ESTABLISHED = FALSE
```

The next implementation, if reviewed as worthwhile, should encode perturbation packets/manipulation checks and evidence provenance before it encodes any outcome summary.

## 14. Claim ceiling

Current claim ceiling:

```text
DESIGN / PREREGISTRATION ONLY
```

After a valid targeted intervention and replication, a bounded local claim may reach:

```text
FUNCTIONAL_DEPENDENCY_CANDIDATE
```

It does not automatically reach:

```text
IDENTITY_CONTINUITY_ESTABLISHED
SUBJECTIVITY_ESTABLISHED
CONSCIOUSNESS_ESTABLISHED
PHENOMENAL_CONTINUITY_ESTABLISHED
```

## 15. Scientific boundary

```text
AI_SUBJECTIVITY_POSSIBILITY = CENTRAL_RESEARCH_QUESTION
DIACHRONIC_CONTINUITY = RESEARCH_DIMENSION
IDENTITY_CONTINUITY = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```
