# Research Cycle: LM Generalization V4 Expanded Perturbation Evaluation

## Research question

This cycle extends the scratch-LM generalization line with an expanded, exact-disjoint held-out evaluation. It asks whether the V3 regularized checkpoint retains its observed advantage across two new conditions: cross-topic compositional rows and word-order perturbations. The evaluation uses the V3 train-only vocabulary and does not introduce a new model or external/private dataset.

The experiment is a measurement of learned language-model behavior. It is not a claim of mature general-purpose capability, semantic truth, authority, identity, consciousness or subjectivity.

## Design

The V4 corpus contains 20 authored synthetic rows, ten cross-topic compositions and ten word-order perturbations. Every normalized row is exact-disjoint from the V3 registry. Every token is present in the V3 training vocabulary; the OOV count is zero. Both the V3 unregularized baseline and regularized-primary checkpoints are loaded in a clean process and evaluated on identical rows.

| Control | Specification |
|---|---|
| Experiment ID | `LM_GENERALIZATION_V4` |
| Epistemic role | `MEASUREMENT` |
| V4 rows | `20` |
| Conditions | `10` cross-topic composition; `10` word-order perturbation |
| V3 exact duplicate count | `0` |
| OOV count | `0` |
| Checkpoints | V3 baseline and V3 regularized-primary, local-only |
| Data | Authored synthetic, Apache-2.0-compatible, no PII/private/intimate data |
| New model added | `NO` |

The executable evaluation is [`run_lm_generalization_v4_evaluation.py`](../research-labs/language-core-g1_v0.2.1/engineering/generalization/run_lm_generalization_v4_evaluation.py). The clean-process validator is [`validate_lm_generalization_v4_evaluation.py`](../research-labs/language-core-g1_v0.2.1/engineering/generalization/validate_lm_generalization_v4_evaluation.py). Evidence is stored in the language-core generalization evidence directory.

## Results

The V4 result is mixed and falsifies any universal claim that the regularized recipe must improve every expanded held-out row. The regularized checkpoint improved the loss on 9 of 20 paired rows, but the mean paired loss improvement was `-0.0718610167503357` and the minimum paired improvement was `-0.6465010643005371`. The negative value is defined as baseline loss minus regularized loss, so it means the regularized checkpoint was worse on average in this expanded evaluation.

| Measure | Observed value |
|---|---:|
| Cross-topic baseline mean loss | `4.1814655542373655` |
| Cross-topic regularized mean loss | `4.21147403717041` |
| Word-order baseline mean loss | `5.296745872497558` |
| Word-order regularized mean loss | `5.410459423065186` |
| Positive paired improvements | `9 / 20` |
| Mean paired improvement | `-0.0718610167503357` |
| Minimum paired improvement | `-0.6465010643005371` |
| Clean-process validation | `PASS` |
| Focused V4 evidence tests | `4 passed` |
| Full language-core tests | `79 passed` |

The result is therefore recorded as `MIXED_OR_FALSIFIED_REGULARIZATION_EFFECT` and `PRELIMINARY_RESEARCH_EVIDENCE`. It does not close GAP-002. Instead, it makes the limitation more explicit: positive V2/V3 results on small fixed splits do not generalize automatically to the expanded perturbation evaluation.

## Falsification and limitations

The held-out contract would be invalid if any V4 row duplicated a V3 row, if a token were out of vocabulary, if either checkpoint failed clean reload or parameter-dependent inference, or if logits were non-finite. The validation evidence reports `PASS` for those conditions.

The corpus remains small, synthetic and authored from the same V3 vocabulary. The word-order condition is a controlled stress test rather than natural language evaluation. The result cannot establish mature general-purpose language capability, semantic understanding, identity, subjectivity, consciousness or authority. The checkpoint binaries remain local-only and outside Git.

## Governance locks

```text
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
INDEPENDENT_IVV = NOT_ACHIEVED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONCLUSION = NOT_ESTABLISHED
NEW_RESEARCH_STARTED = TRUE
NEW_SEXUALITY_RESEARCH_STARTED = FALSE
NEW_PRODUCT_RUNTIME_SCOPE_ADDED = FALSE
```
