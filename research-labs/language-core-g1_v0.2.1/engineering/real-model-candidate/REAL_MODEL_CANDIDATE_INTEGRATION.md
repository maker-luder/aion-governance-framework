# Real-Model Candidate Integration Note

This directory records a public-safe research candidate surface from the local AION/Astra real-model completion workspace. It is not a production model release, a canonical runtime promotion or a mature general-purpose language-model claim.

## A. Original local workspace artifacts

The original local workspace contained PyTorch model definitions, CPU training and dataset-materialization scripts, clean-process validation scripts, governed semantic-memory integration tests, registries, evidence summaries, eight learned checkpoint binaries and synthetic dataset binaries. The original workspace artifacts remain local resources and are not treated as public repository files merely because their summaries are referenced here.

## B. Public-safe evidence summaries committed to formal research

The following reviewed public-safe summaries are committed in this formal research tree and are current research evidence, subject to their own recorded provenance and the exact research HEAD:

- `evidence/LOCAL_REAL_MODEL_VALIDATION.json`
- `evidence/LOCAL_TRAINING_EVIDENCE.json`
- `evidence/LOCAL_REAL_MEMORY_INTEGRATION.json`
- `evidence/LOCAL_ABLATION_RESULTS.json`
- `evidence/LOCAL_MODEL_SWAP_RESULTS.json`
- `evidence/MODEL_REGISTRY.json`
- `evidence/DATASET_REGISTRY.json`

They record checkpoint SHA-256 values, clean-process reload/inference status, learned-parameter dependence, training provenance, dataset/provenance boundaries and declared non-claims. They are committed evidence summaries; they are not the original local binary artifacts.

## C. Binaries intentionally absent from Git

Checkpoint binaries and synthetic dataset binaries are deliberately **not copied into the formal research tree** by this integration. The public registries retain hashes, provenance, license/PII assessments, local artifact disposition and verification references without fabricating repository presence. Future redistribution requires explicit Owner review of license, privacy, security and repository policy.

## D. Hashes and provenance for later verification

The committed evidence and registries contain the SHA-256 values and provenance fields needed to compare a later authorized copy of each binary with the original local artifact. A matching hash can support artifact identity verification; it does not establish model quality, generalization, production readiness, canonical status or scientific validity.

## Scientific status

The evidence supports `REAL_LEARNED_MODEL = TRUE` for eight local research checkpoints: seven trained from scratch and one PEFT-adapted local scratch-base language adapter. The LoRA evidence records non-zero trainable parameters, optimizer updates, loss reduction and clean reload inference. The controlled and random ablation evidence is recorded in `evidence/LOCAL_ABLATION_RESULTS.json`.

`REAL_MODEL != MATURE_GENERAL_PURPOSE_MODEL` and `TRAINING_SUCCESS != GENERALIZATION_SUCCESS`. The scratch language model training loss decreases from approximately `4.491575050354004` to `0.0025797318667173386`, while held-out loss is `8.133516788482666`; this is a material train/held-out generalization warning. The current evidence therefore supports a **real learned research model**, not a mature general-purpose AION language model.

The declared `G1-Qwen3-4B-Instruct-2507` baseline remains `RESOURCE_BLOCKED`: its external weights/runtime were unavailable under local resource and dependency constraints and were not substituted by the scratch models. The local LoRA artifact is not the formal G1-Qwen adapter.

## LM_GENERALIZATION_V2 research result

The active generalization gap was tested with a fixed 24-row synthetic governance corpus split into 18 train, 3 validation and 3 test rows. The experiment compared the prior-style unregularized Embedding-GRU-CausalLM recipe against a modestly regularized AdamW variant under paired seeds `1729`, `1730` and `1731`. Exact normalized duplicate checks passed, no private or intimate data was ingested, and both primary checkpoints were clean-process reloaded with actual parameter-dependent inference.

The paired held-out result provides **preliminary support** for the regularization hypothesis in this setup: the primary test-loss improvement was `0.04252147674560547`, the mean paired improvement was `0.03643083572387695`, and the minimum paired improvement was `0.028870105743408203`. Full evidence is in `engineering/generalization/evidence/LM_GENERALIZATION_RESULTS.json`, `LM_GENERALIZATION_VALIDATION.json` and `GENERALIZATION_DATASET_REGISTRY.json`.

This result remains `PARTIALLY_COMPLETE`, not complete. The corpus is synthetic and small, the evaluation is narrow, and the result does not establish robust out-of-distribution generalization, broad language capability or a mature general-purpose AION foundation model. The experiment is recorded as an `OPTIONAL_RESEARCH_MODEL` and is intentionally not added to the formal model registry. Its falsification conditions require that a non-positive paired improvement, split leakage, non-finite training, failed reload or parameter-independent inference would invalidate the claimed result.

## LM_GENERALIZATION_V3 research result

The next-cycle follow-up used a fixed 42-row synthetic governance corpus with 26 train, 8 validation and 8 cross-topic compositional test rows. The tokenizer was built from training rows only; exact normalized duplicate checks passed and validation/test rows contained zero out-of-vocabulary tokens. The experiment compared the prior-style unregularized Embedding-GRU-CausalLM recipe with the same modest AdamW, label-smoothing and gradient-clipping regularization family under paired seeds `2027`, `2028` and `2029`.

The paired compositional held-out result provides **preliminary support** in this setup: the primary test-loss improvement was `0.17763042449951172`, the mean paired improvement was `0.13621012369791666`, and the minimum paired improvement was `0.028661489486694336`. Both primary checkpoints were clean-process reloaded with actual parameter-dependent inference. Full evidence is in `engineering/generalization/evidence/LM_GENERALIZATION_V3_RESULTS.json`, `LM_GENERALIZATION_V3_VALIDATION.json` and `GENERALIZATION_COMPOSITION_V3_DATASET_REGISTRY.json`.

V3 remains `PARTIALLY_COMPLETE`, not complete. The corpus is synthetic, the test set is small, and the evaluation still does not establish robust out-of-distribution generalization, broad language capability or a mature general-purpose AION foundation model. The checkpoints are `OPTIONAL_RESEARCH_MODEL` artifacts, remain outside the formal model registry and remain local-only. The result cannot authorize actions, convert scores into authority, bypass governance gates or establish subjectivity, identity or phenomenal status.

## Governance locks

```text
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
INDEPENDENT_IVV = NOT_ACHIEVED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONCLUSION = NOT_ESTABLISHED
```

The learned components are advisory only. They cannot authorize actions, canonize or rewrite provenance, cross namespace/supersession/deletion/recovery/audit gates, or establish identity, subjectivity or phenomenal status. Semantic-memory integration evidence requires namespace/provenance gating before model scoring.
