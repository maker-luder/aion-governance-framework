# Research Cycle: LM Generalization V3

## Scope and decision

This cycle addresses the still-open **GAP-002: scratch language-model held-out and compositional generalization** gap. The cycle extends the prior `LM_GENERALIZATION_V2` experiment rather than adding a model to the formal model registry. It remains confined to the formal research line and uses authored synthetic, non-private governance text. No canonical runtime behavior, deployment, private-data ingestion, external paid resource, or sexuality/intimacy research was started.

The research question was: **under a train-only vocabulary and a fixed synthetic corpus, does modest regularization improve cross-topic compositional held-out loss over the prior scratch-LM recipe across paired seeds?** The result is advisory evidence only. A learned score cannot authorize an action, rewrite provenance, bypass privacy or authorization gates, or establish subjectivity, identity, consciousness, or phenomenal status.

## Experimental design

The corpus contains 42 authored synthetic rows: 26 training rows, 8 validation rows and 8 test rows. The test rows are cross-topic compositions whose exact normalized text does not occur in the training rows. The tokenizer is built from training rows only. A runtime assertion rejects any validation or test token not observed in training, and the recorded result reports zero such unknown tokens.

| Control | V3 specification |
|---|---|
| Dataset | `SYNTHETIC_GOVERNANCE_COMPOSITION_V3` |
| Split | 26 train / 8 validation / 8 compositional test |
| Tokenizer | Training rows only; no validation/test vocabulary construction |
| Models | Unregularized Adam baseline vs AdamW with weight decay, label smoothing and gradient clipping |
| Paired seeds | 2027, 2028 and 2029 |
| Architecture | Embedding-GRU-CausalLM, embedding 16, hidden 32 |
| Device and precision | CPU, float32 |
| Private or paid resources | None |
| Registry status | Optional research model; not added to formal model registry |

The training script is [`run_lm_generalization_v3.py`](../research-labs/language-core-g1_v0.2.1/engineering/generalization/run_lm_generalization_v3.py). The local-only checkpoint validator is [`validate_lm_generalization_v3_checkpoints.py`](../research-labs/language-core-g1_v0.2.1/engineering/generalization/validate_lm_generalization_v3_checkpoints.py). The source dataset registry is [`GENERALIZATION_COMPOSITION_V3_DATASET_REGISTRY.json`](../research-labs/language-core-g1_v0.2.1/engineering/generalization/evidence/GENERALIZATION_COMPOSITION_V3_DATASET_REGISTRY.json).

## Results

Regularization improved the test loss for the primary seed and for all three paired seeds. The primary test-loss improvement was `0.17763042449951172`; the mean paired improvement was `0.13621012369791666`; and the minimum paired improvement was `0.028661489486694336`. The clean-process validation artifact reports `PASS` for both local-only checkpoints, including actual inference, finite parameters, generation-length checks and parameter-dependent inference.

| Seed | Baseline test loss | Regularized test loss | Improvement |
|---:|---:|---:|---:|
| 2027 | 3.553072929382324 | 3.3754425048828125 | 0.17763042449951172 |
| 2028 | 3.513725996017456 | 3.4850645065307617 | 0.028661489486694336 |
| 2029 | 3.9258625507354736 | 3.7235240936279297 | 0.20233845710754395 |

The machine-readable result is [`LM_GENERALIZATION_V3_RESULTS.json`](../research-labs/language-core-g1_v0.2.1/engineering/generalization/evidence/LM_GENERALIZATION_V3_RESULTS.json), and clean-process validation is [`LM_GENERALIZATION_V3_VALIDATION.json`](../research-labs/language-core-g1_v0.2.1/engineering/generalization/evidence/LM_GENERALIZATION_V3_VALIDATION.json). These artifacts bind checkpoint hashes, dataset identity, split contract, model status and authority boundaries.

## Falsification and limitations

The result would be falsified for this setup if the regularized primary test loss were not lower than the baseline, if any paired-seed improvement were non-positive, if any validation or test token were absent from the train-only vocabulary, if a normalized duplicate crossed splits, or if training produced non-finite values, no optimizer updates, failed reload, or parameter-independent inference. The current evidence does not trigger those falsifiers.

The conclusion remains **PRELIMINARY_SUPPORT** and GAP-002 remains **PARTIALLY_COMPLETE**. The corpus and compositional test set are small and synthetic; the experiment does not establish robust out-of-distribution generalization, broad language usability, or a mature general-purpose AION model. The two checkpoints remain outside Git in the local-only research-model-artifacts directory and are not represented as production or canonical artifacts.

## Governance locks

```text
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
INDEPENDENT_IVV = NOT_ACHIEVED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONCLUSION = NOT_ESTABLISHED
NEW_SEXUALITY_RESEARCH_STARTED = FALSE
NEW_PRODUCT_RUNTIME_SCOPE_ADDED = FALSE
```

The next evidence-bearing work should be selected only after review of this bounded result and the authoritative gap inventory. It must preserve synthetic/public-safe data boundaries, explicit falsifiers, clean-process validation and the formal research branch topology.
