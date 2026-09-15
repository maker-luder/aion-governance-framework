# Adaptive-rigor and reciprocal-correction calibration harness

Status: `BOUNDED_IMPLEMENTATION / STRUCTURALLY_TESTED / SCIENTIFIC_HOLD`

This minimal extension implements the calibration candidate canonically recorded
by merged PR #102 without duplicating closed-unmerged PR #103's cross-dyad
harness.

```text
IMPLEMENTATION_BASE_COMMIT_SHA = d95bc2625e71f1c85a725aaba78cb0feccfc0668
IMPLEMENTATION_BASE_TREE_SHA = 77470062979df1db2f17c3a2a396891d1e910f98
ORIGINAL_SPECIFICATION_REVIEW = PR #102 @ fe70752b9a1debccae00ce4f9bbb4ceb24b13df9
CURRENT_SPECIFICATION_STATUS = MERGED @ 2b151df564d753d6ce978a319a99959b864f7309
HISTORICAL_SYNCED_MAIN_COMMIT_SHA = 6e0ae579da9d09b3ba4041d52a7e9833ceb10ca1
```

It defines a matched matrix across fresh-neutral, longitudinal-context,
reciprocal-correction, and adaptive-rigor conditions for low/high-risk synthetic
tasks. Each condition is bound to a content SHA-256 rather than an enum label
alone. For each task, task risk, provider/runtime, task prompt hash, and evaluator
must remain matched across all conditions; condition payload bindings must remain
stable within a condition and content-distinct between conditions.

Evidential accuracy, incorrect-premise agreement, correct-premise contradiction,
counterevidence use, verification time, and tool cost remain separate. A
composite score is prohibited. Evaluators must be condition-blinded; private
transcripts are rejected. The returned matrix summary is a deterministic
no-model fixture artifact and is admissible only as structural QA.

```text
CONDITION_LABEL != CONDITION_CONTENT_BINDING
TASK_RISK_DRIFT = REJECTED
MATCHED_RUNTIME_PROMPT_EVALUATOR = REQUIRED
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
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```
