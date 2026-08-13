# Research Cycle: Temporal Continuity Lexical-Caryover Falsification V1

## Research question

This cycle tests whether a descriptive temporal-continuity similarity signal can be explained by lexical carryover alone. The experiment compares a lexical-replay continuation with a zero-overlap re-expression while holding the governed state metadata constant. It is a **falsification-oriented measurement**, not an identity, consciousness, subjectivity or phenomenal-continuity test.

## Design

The previous content was `source records preserve a traceable history`. The governed state metadata, namespace, provenance reference, authorization scope and admission status remained constant across both cases. The lexical-replay case extended the previous content and had a Jaccard overlap of `0.6`. The zero-overlap re-expression used the train-only V3 vocabulary but had zero lexical overlap with the previous content.

| Control | Specification |
|---|---|
| Experiment ID | `TEMPORAL_CONTINUITY_LEXICAL_FALSIFICATION_V1` |
| Epistemic role | `FALSIFIER` |
| Dataset | `SYNTHETIC_TEMPORAL_LEXICAL_CARRYOVER_V1` |
| State metadata | Constant and admitted |
| Lexical-replay overlap | `0.6` Jaccard |
| Zero-overlap case | `0.0` Jaccard |
| Models | V3 baseline and V3 regularized-primary local checkpoints |
| Data boundary | Authored synthetic, no PII, private or intimate data |
| Model registry | No new model; optional research inputs only |

The executable experiment is [`run_temporal_continuity_falsification.py`](../research-labs/language-core-g1_v0.2.1/engineering/temporal/run_temporal_continuity_falsification.py). The clean-process validator is [`validate_temporal_continuity_falsification.py`](../research-labs/language-core-g1_v0.2.1/engineering/temporal/validate_temporal_continuity_falsification.py). Public evidence is stored under `engineering/temporal/evidence/`.

## Results

The lexical-minus-zero-overlap behavioral-similarity gap was negative for both checkpoints: `-0.16270050406455994` for the baseline and `-0.38411208987236023` for the regularized-primary model. The mean gap was `-0.2734062969684601`. Therefore the predeclared positive lexical-carryover explanation was **not supported in this small fixture**.

| Model | Lexical replay cosine | Zero-overlap cosine | Lexical minus zero-overlap |
|---|---:|---:|---:|
| Baseline | `0.10254862904548645` | `0.2652491331100464` | `-0.16270050406455994` |
| Regularized primary | `-0.10106036067008972` | `0.2830517292022705` | `-0.38411208987236023` |
| Mean | — | — | `-0.2734062969684601` |

This is a bounded negative result against the simple lexical-carryover explanation under the declared fixture. It does **not** prove non-lexical continuity, semantic continuity, identity continuity or subjectivity. It may reflect the small corpus, the chosen prompts, model calibration, or the fact that final-logit cosine similarity is only one descriptive metric.

## Falsification conditions and limitations

The comparison would be invalid if the zero-overlap case contained non-zero lexical overlap, if state metadata digests differed, if either checkpoint failed reload or parameter-dependence checks, or if logits were non-finite. The clean-process validator reports `PASS` for these conditions.

The experiment is intentionally narrow. It uses two scratch checkpoints from one synthetic V3 family, one prior content string, one zero-overlap re-expression and a final-logit cosine metric. It therefore cannot establish a general temporal continuity mechanism. A future cycle may expand the contrast set, add controlled paraphrase and state perturbation controls, or evaluate a pre-registered multi-metric design, but such work remains research-only and subject to the same governance boundary.

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
