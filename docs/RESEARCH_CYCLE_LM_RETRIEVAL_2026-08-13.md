# Research Cycle — LM Generalization and Governed Retrieval

## Scope and value filter

This cycle selected two technically actionable gaps from the authoritative inventory. The first was scratch-language-model held-out generalization because the prior evidence showed a substantial train/held-out gap and the experiment was executable on the existing CPU-only environment without paid resources or private data. The second was governed retrieval robustness because the repository already contained learned embedding and reranker checkpoints, while the governing requirement was to demonstrate that deterministic authorization remains ahead of model scoring under adversarial state.

Both items materially improve testability, falsifiability, reproducibility or governance correctness. No model was added merely to increase model count. No production, canonical, network-MCP or independent-IV&V claim was made.

## Item A — LM_GENERALIZATION_V2

**Question.** Does modest regularization improve held-out causal-LM loss over the prior small scratch-LM recipe on a fixed, leakage-checked synthetic governance split?

**Design.** A 24-row synthetic corpus was fixed as 18 train, 3 validation and 3 test rows. Exact normalized duplicate checking passed. The experiment compared an unregularized Adam baseline with an AdamW/weight-decay/label-smoothing/gradient-clipping variant under paired seeds 1729, 1730 and 1731. The two primary checkpoints were clean-process reloaded and demonstrated actual parameter-dependent inference.

**Result.** The primary held-out loss improvement was `0.04252147674560547`; the mean paired improvement was `0.03643083572387695`; and the minimum paired improvement was `0.028870105743408203`. All three paired improvements were positive in this fixed setup. The result is therefore recorded as `PRELIMINARY_SUPPORT` and the gap disposition is `PARTIALLY_COMPLETE`.

**Falsification.** A non-positive paired improvement, a duplicate across splits, non-finite training, failed clean reload or parameter-independent inference would invalidate the result. The synthetic corpus is small and narrow; the result does not establish robust out-of-distribution generalization, mature general-purpose language capability or a foundation model.

Evidence: `research-labs/language-core-g1_v0.2.1/engineering/generalization/evidence/LM_GENERALIZATION_RESULTS.json`, `LM_GENERALIZATION_VALIDATION.json` and `GENERALIZATION_DATASET_REGISTRY.json`.

## Item B — Governed retrieval robustness

**Question.** Can wrong-namespace, unverified, superseded and deletion-requested records be rejected before learned embedding/reranker scoring while admitted synthetic rows remain measurable?

**Design.** Eight synthetic adversarial governance fixtures were evaluated. Four authorized rows were scored by the existing embedding and reranker checkpoints. Four rows were rejected deterministically for namespace mismatch, unverified provenance, supersession or deletion request. Rejected rows were recorded as `model_scored = false`.

**Result.** The gate passed with four admitted and four rejected rows. Both learned models showed positive mean score separation on the admitted fixtures. This is bounded governance robustness evidence, not a semantic-truth guarantee.

**Falsification.** Any rejected row reaching model scoring, any missing gate reason or any path allowing model output to decide admission invalidates the integration. Positive score separation is not required for the authorization gate and is not authority.

Evidence: `research-labs/language-core-g1_v0.2.1/engineering/retrieval/evidence/RETRIEVAL_ROBUSTNESS_RESULTS.json` and `RETRIEVAL_ROBUSTNESS_NOTE.md`.

## Governance and next cycle

```text
MODEL_SCORE != AUTHORITY
REAL_MODEL != MATURE_GENERAL_PURPOSE_MODEL
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
INDEPENDENT_IVV = NOT_ACHIEVED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONCLUSION = NOT_ESTABLISHED
```

The remaining language-model gap is still active because the current result is preliminary and synthetic. Formal G1 remains `RESOURCE_BLOCKED`. Live private memory remains subject to external dependency and Owner approval. Network MCP remains uncompleted by in-process evidence. No autonomous sexuality/intimacy research was started in this cycle; that domain remains research-authorized but was not selected because the current CPU-local evidence gaps had higher immediate reproducibility value and did not require sensitive data.
