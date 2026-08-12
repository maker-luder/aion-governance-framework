# Real-Model Candidate Integration Note

This directory records the public-safe code, configuration, evaluation evidence and provenance metadata from the local AION/Astra real-model completion workspace. It is a research candidate surface, not a production model release.

## Scope

The candidate contains the PyTorch model definitions, CPU training/materialization scripts, clean-process validation scripts, governed semantic-memory integration test, model/dataset public-safe registries, and local evidence summaries. The local evidence covers eight learned checkpoints: seven trained from scratch and one PEFT-adapted local scratch-base language adapter.

## Artifact boundary

Checkpoint binaries and synthetic dataset binaries are deliberately **not copied into the formal research tree by this integration**. The public registries retain hashes, provenance, license/PII assessments, local artifact status and retrieval instructions without fabricating repository presence. Any future checkpoint redistribution requires explicit Owner review of license, privacy, security and repository policy.

The declared G1-Qwen3-4B-Instruct-2507 baseline remains `RESOURCE_BLOCKED`: its external weights were not available in the local environment and were not substituted by the scratch models. The local LoRA artifact is not the formal G1-Qwen adapter.

## Governance locks

```text
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
INDEPENDENT_IVV = NOT_ACHIEVED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONCLUSION = NOT_ESTABLISHED
```

The learned components are advisory only. They cannot authorize actions, canonize or rewrite provenance, cross namespace/supersession/deletion/recovery/audit gates, or establish identity, subjectivity or phenomenal status. The semantic-memory integration evidence requires namespace/provenance gating before model scoring.

## Evidence references

The evidence filenames are `evidence/LOCAL_REAL_MODEL_VALIDATION.json`, `evidence/LOCAL_TRAINING_EVIDENCE.json`, `evidence/LOCAL_REAL_MEMORY_INTEGRATION.json`, `evidence/LOCAL_ABLATION_RESULTS.json` and `evidence/LOCAL_MODEL_SWAP_RESULTS.json`. Their original local-workspace files remain outside the formal repository tree and are not represented as current GitHub state until separately reviewed against the final research head.
