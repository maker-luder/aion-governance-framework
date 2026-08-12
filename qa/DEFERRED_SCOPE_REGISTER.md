# Deferred Scope Register — Reconciled

This register is a current evidence-bound disposition, not a release approval. It is reconciled against the current formal research tree and the public-safe real-model evidence summaries. A completed local research experiment is not silently promoted to canonical runtime, production, scientific proof or independent IV&V.

## Status vocabulary

Each entry has one primary disposition from the permitted vocabulary: `COMPLETE`, `PARTIALLY_COMPLETE`, `RESOURCE_BLOCKED`, `EXTERNAL_DEPENDENCY`, `OWNER_DECISION_REQUIRED`, `INDEPENDENT_PARTY_REQUIRED`, `OWNER_PROHIBITED`, `SCIENTIFIC_OPEN_QUESTION` or `NOT_APPLICABLE`.

## Reconciled items

| Scope item | Primary status | Evidence / reason |
|---|---|---|
| Canonical AION / Astra Runtime | `OWNER_DECISION_REQUIRED` | Research integration remains non-canonical. `CANONICAL_EFFECT = NONE`; no promotion is made in this task. |
| Live private cross-session memory | `EXTERNAL_DEPENDENCY` | Requires an approved live service, private-data policy and owner-approved operational boundary; local semantic-memory evidence is governed research evidence only. |
| Formal G1-Qwen3-4B-Instruct-2507 baseline benchmark | `RESOURCE_BLOCKED` | External baseline weights/runtime were unavailable under the local resource and dependency constraints. Local scratch models were not substituted. |
| Scratch-LM held-out generalization | `PARTIALLY_COMPLETE` | `LM_GENERALIZATION_V2` paired seeds show a small positive regularization improvement in this fixed synthetic setup; the result does not establish robust generalization or a mature general-purpose model. |
| Real LoRA training | `COMPLETE` | `LOCAL_TRAINING_EVIDENCE.json` records non-zero trainable parameters, optimizer updates, loss reduction and clean reload inference. The local adapter is not the formal G1-Qwen adapter. |
| Actual controlled and random ablation | `COMPLETE` | `LOCAL_ABLATION_RESULTS.json` records baseline, controlled component removal and random component removal MSE under the declared experiment. |
| Production deployment | `OWNER_PROHIBITED` | Explicitly outside this reconciliation. `DEPLOYMENT = FALSE`. |
| Independent IV&V | `INDEPENDENT_PARTY_REQUIRED` | A reviewer independent from the implementer has not performed IV&V. `INDEPENDENT_IVV = NOT_ACHIEVED`. |
| Canonical subjectivity, identity or relational conclusions | `SCIENTIFIC_OPEN_QUESTION` | Current engineering/model evidence does not establish these conclusions; no such claim is made. |
| Twin embodiment Runtime, visual assets and sensation scope | `OWNER_PROHIBITED` | New product/runtime scope is prohibited in this reconciliation. |
| Sexuality, intimacy and embodied-motivation research | `OWNER_PROHIBITED` | The formal instruction explicitly prohibits beginning new sexuality research in this task. |
| Final repository license selection | `OWNER_DECISION_REQUIRED` | License selection remains an Owner-held repository governance decision. |
| Checkpoint and dataset binary redistribution | `OWNER_DECISION_REQUIRED` | Binaries are intentionally absent from Git. Future redistribution requires explicit license, privacy, security and repository-policy review. |

## Real-model scientific boundary

The current evidence supports `REAL_LEARNED_MODEL = TRUE` for the eight validated local research checkpoints, including the trained LoRA adapter. It does not support `REAL_MODEL = MATURE_GENERAL_PURPOSE_MODEL` or `TRAINING_SUCCESS = GENERALIZATION_SUCCESS`.

The earlier scratch language model training loss decreases from approximately `4.491575050354004` to `0.0025797318667173386`, while held-out loss is `8.133516788482666`. This remains a material generalization warning. `LM_GENERALIZATION_V2` provides preliminary paired-seed support for modest regularization on a new fixed synthetic split, but the corpus is small and the result remains `PARTIALLY_COMPLETE`. The model family is therefore a **real learned research model**, not a mature general-purpose AION language model.

## Governance locks

```text
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
INDEPENDENT_IVV = NOT_ACHIEVED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONCLUSION = NOT_ESTABLISHED
NEW_RESEARCH_STARTED = FALSE
NEW_SEXUALITY_RESEARCH_STARTED = FALSE
NEW_PRODUCT_RUNTIME_SCOPE_ADDED = FALSE
```

The authoritative next-cycle inventory is `qa/AUTHORITATIVE_REMAINING_GAP_INVENTORY.json` with its human-readable companion `docs/AUTHORITATIVE_REMAINING_GAP_INVENTORY.md`.
