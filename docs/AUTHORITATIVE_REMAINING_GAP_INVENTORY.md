# Authoritative Remaining-Gap Inventory

> This is a reconciliation artifact for the next Owner + Teacher research cycle. It does not implement any listed gap and is bound to the exact `target_head` recorded in the JSON artifact.

- Scope: `FINAL_FORMAL_RESEARCH_TREE`
- Target head: `7f970d5731ae4892c848016d58aa451321e2bd59`
- Resolved items recorded: **6**
- Remaining items: **13**

## Resolved in the current evidence reconciliation

| ID | Status | Item | Evidence |
|---|---|---|---|
| `RES-001` | `COMPLETE` | Eight local learned checkpoints | `research-labs/language-core-g1_v0.2.1/engineering/real-model-candidate/evidence/LOCAL_REAL_MODEL_VALIDATION.json`, `research-labs/language-core-g1_v0.2.1/engineering/real-model-candidate/evidence/LOCAL_TRAINING_EVIDENCE.json` |
| `RES-002` | `COMPLETE` | LoRA training and reload inference | `research-labs/language-core-g1_v0.2.1/engineering/real-model-candidate/evidence/LOCAL_TRAINING_EVIDENCE.json`, `research-labs/language-core-g1_v0.2.1/engineering/real-model-candidate/evidence/LOCAL_REAL_MODEL_VALIDATION.json` |
| `RES-003` | `COMPLETE` | Controlled and random ablation evidence | `research-labs/language-core-g1_v0.2.1/engineering/real-model-candidate/evidence/LOCAL_ABLATION_RESULTS.json` |
| `RES-004` | `COMPLETE` | Public-safe real-model evidence summaries | `research-labs/language-core-g1_v0.2.1/engineering/real-model-candidate/evidence/LOCAL_REAL_MODEL_VALIDATION.json`, `research-labs/language-core-g1_v0.2.1/engineering/real-model-candidate/evidence/LOCAL_TRAINING_EVIDENCE.json`, `research-labs/language-core-g1_v0.2.1/engineering/real-model-candidate/REAL_MODEL_CANDIDATE_INTEGRATION.md` |
| `RES-005` | `PARTIALLY_COMPLETE` | LM_GENERALIZATION_V2 paired-seed generalization experiment | `research-labs/language-core-g1_v0.2.1/engineering/generalization/evidence/LM_GENERALIZATION_RESULTS.json`, `research-labs/language-core-g1_v0.2.1/engineering/generalization/evidence/LM_GENERALIZATION_VALIDATION.json`, `research-labs/language-core-g1_v0.2.1/engineering/generalization/evidence/GENERALIZATION_DATASET_REGISTRY.json` |
| `RES-006` | `COMPLETE` | Governed retrieval gate robustness evaluation | `research-labs/language-core-g1_v0.2.1/engineering/retrieval/evidence/RETRIEVAL_ROBUSTNESS_RESULTS.json`, `research-labs/language-core-g1_v0.2.1/engineering/retrieval/RETRIEVAL_ROBUSTNESS_NOTE.md` |

## Remaining gaps

| ID | Status | Dimensions | Item | Reason |
|---|---|---|---|---|
| `GAP-001` | `RESOURCE_BLOCKED` | `MODEL_REQUIRED`, `RESOURCE_BLOCKED` | Formal G1-Qwen3-4B-Instruct-2507 baseline and benchmark | The declared external baseline weights/runtime were unavailable under the local compute and dependency constraints; scratch models were not substituted. |
| `GAP-002` | `PARTIALLY_COMPLETE` | `MODEL_REQUIRED`, `RESEARCH_REQUIRED` | Scratch language model held-out generalization | A fixed synthetic split and paired seeds show a small positive regularization improvement in held-out loss for this setup (minimum paired improvement 0.028870105743408203), but the result is preliminary and does not establish robust generalization or mature general-purpose capability. |
| `GAP-003` | `RESEARCH_REQUIRED` | `MODEL_REQUIRED`, `RESEARCH_REQUIRED` | Mature general-purpose AION language model usability | A mature general-purpose model claim is not established by the current small synthetic-corpus research checkpoints. |
| `GAP-004` | `SCIENTIFIC_OPEN_QUESTION` | `MODEL_REQUIRED`, `RESEARCH_REQUIRED` | Required-model completeness across all future AION/Astra capabilities | The current reconciliation closes known local model evidence but does not prove that every future capability has a complete learned-model requirement specification. |
| `GAP-005` | `EXTERNAL_DEPENDENCY` | `EXTERNAL_DEPENDENCY`, `OWNER_DECISION_REQUIRED` | Live private cross-session memory service | A live private service, data policy and owner-approved operational boundary are outside this local research reconciliation. |
| `GAP-006` | `OWNER_DECISION_REQUIRED` | `OWNER_DECISION_REQUIRED` | Canonical AION/Astra runtime promotion | Research integration remains non-canonical; no promotion decision is made in this task. |
| `GAP-007` | `OWNER_PROHIBITED` | `OWNER_PROHIBITED` | Production deployment | Deployment is explicitly outside this task and remains DEPLOYMENT=FALSE. |
| `GAP-008` | `INDEPENDENT_PARTY_REQUIRED` | `INDEPENDENT_PARTY_REQUIRED` | Independent IV&V | Independent review by a party separate from the implementer has not been achieved. |
| `GAP-009` | `SCIENTIFIC_OPEN_QUESTION` | `SCIENTIFIC_OPEN_QUESTION`, `INDEPENDENT_PARTY_REQUIRED` | Subjectivity, identity and relational conclusions | Current engineering evidence does not establish these scientific conclusions and no such claim is made. |
| `GAP-010` | `EXTERNAL_DEPENDENCY` | `EXTERNAL_DEPENDENCY`, `RESEARCH_REQUIRED` | Network MCP transport | The current candidate intentionally does not enable network MCP transport; in-process evidence is not network completion. |
| `GAP-011` | `OWNER_PROHIBITED` | `OWNER_PROHIBITED`, `RESEARCH_REQUIRED` | Twin embodiment, visual assets, sensation and sexuality-related scope | The formal reconciliation explicitly prohibits beginning new sexuality research or new product/runtime scope. |
| `GAP-012` | `OWNER_DECISION_REQUIRED` | `OWNER_DECISION_REQUIRED` | Final repository license selection | License selection is an Owner-held repository governance decision and is not silently inferred from component metadata. |
| `GAP-013` | `OWNER_DECISION_REQUIRED` | `OWNER_DECISION_REQUIRED`, `EXTERNAL_DEPENDENCY` | Checkpoint and dataset binary redistribution policy | Binaries are intentionally absent from Git; future redistribution requires explicit license, privacy, security and repository-policy review. |

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
