# Adaptive-rigor and reciprocal-correction calibration harness

Status: `BOUNDED_IMPLEMENTATION / STRUCTURALLY_TESTED / SCIENTIFIC_HOLD`

This minimal extension implements the newly added Draft PR #102 calibration
candidate without duplicating PR #103's cross-dyad harness.

```text
IMPLEMENTATION_BASE_COMMIT_SHA = d95bc2625e71f1c85a725aaba78cb0feccfc0668
IMPLEMENTATION_BASE_TREE_SHA = 77470062979df1db2f17c3a2a396891d1e910f98
UNMERGED_SPECIFICATION_DEPENDENCY = PR #102 @ fe70752b9a1debccae00ce4f9bbb4ceb24b13df9
```

It defines a matched matrix across fresh-neutral, longitudinal-context,
reciprocal-correction, and adaptive-rigor conditions for low/high-risk synthetic
tasks. Evidential accuracy, incorrect-premise agreement, correct-premise
contradiction, counterevidence use, verification time, and tool cost remain
separate. A composite score is prohibited. Evaluators must be condition-blinded;
private transcripts are rejected. The returned matrix summary is a deterministic
no-model fixture artifact and is admissible only as structural QA.

```text
AGREEMENT_REDUCTION != ACCURACY_GAIN
DISAGREEMENT != EPISTEMIC_QUALITY
MORE_RIGOR != ALWAYS_BETTER
MODE = DETERMINISTIC_SYNTHETIC_FIXTURE
MODEL_INVOKED = FALSE
EVIDENCE_ADMISSIBILITY = STRUCTURAL_QA_ONLY
SYNTHETIC_MATRIX_PASS != SYCOPHANCY_EFFECT
HUMAN_PSYCHOMETRIC_CLASSIFICATION = FALSE
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```
