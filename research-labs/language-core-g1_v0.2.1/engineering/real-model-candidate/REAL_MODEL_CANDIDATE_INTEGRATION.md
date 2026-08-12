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

## Governance locks

```text
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
INDEPENDENT_IVV = NOT_ACHIEVED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONCLUSION = NOT_ESTABLISHED
```

The learned components are advisory only. They cannot authorize actions, canonize or rewrite provenance, cross namespace/supersession/deletion/recovery/audit gates, or establish identity, subjectivity or phenomenal status. Semantic-memory integration evidence requires namespace/provenance gating before model scoring.
