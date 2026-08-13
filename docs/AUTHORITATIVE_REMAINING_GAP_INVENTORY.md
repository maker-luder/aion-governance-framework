# Authoritative Remaining-Gap Inventory

> This is a reconciliation artifact for the next Owner + Teacher research cycle. It does not implement any listed gap and is bound to the exact `target_head` recorded in the JSON artifact.

- Scope: `FINAL_FORMAL_RESEARCH_TREE`
- Target head: `280acb3c9d2113e50017314b7f1a438ac13dfb10`
- Resolved items recorded: **9**
- Remaining items: **13**

## Resolved in the current evidence reconciliation

| ID | Status | Item | Evidence |
|---|---|---|---|
| `RES-001` | `COMPLETE` | Eight local learned checkpoints | `research-labs/language-core-g1_v0.2.1/engineering/real-model-candidate/evidence/LOCAL_REAL_MODEL_VALIDATION.json`, `research-labs/language-core-g1_v0.2.1/engineering/real-model-candidate/evidence/LOCAL_TRAINING_EVIDENCE.json` |
| `RES-002` | `COMPLETE` | LoRA training and reload inference | `research-labs/language-core-g1_v0.2.1/engineering/real-model-candidate/evidence/LOCAL_TRAINING_EVIDENCE.json`, `research-labs/language-core-g1_v0.2.1/engineering/real-model-candidate/evidence/LOCAL_REAL_MODEL_VALIDATION.json` |
| `RES-003` | `COMPLETE` | Controlled and random ablation evidence | `research-labs/language-core-g1_v0.2.1/engineering/real-model-candidate/evidence/LOCAL_ABLATION_RESULTS.json` |
| `RES-004` | `COMPLETE` | Public-safe real-model evidence summaries | `research-labs/language-core-g1_v0.2.1/engineering/real-model-candidate/evidence/LOCAL_REAL_MODEL_VALIDATION.json`, `research-labs/language-core-g1_v0.2.1/engineering/real-model-candidate/evidence/LOCAL_TRAINING_EVIDENCE.json`, `research-labs/language-core-g1_v0.2.1/engineering/real-model-candidate/REAL_MODEL_CANDIDATE_INTEGRATION.md` |
| `RES-005` | `PARTIALLY_COMPLETE` | LM_GENERALIZATION_V2/V3 paired-seed generalization experiments | `research-labs/language-core-g1_v0.2.1/engineering/generalization/evidence/LM_GENERALIZATION_RESULTS.json`, `research-labs/language-core-g1_v0.2.1/engineering/generalization/evidence/LM_GENERALIZATION_VALIDATION.json`, `research-labs/language-core-g1_v0.2.1/engineering/generalization/evidence/GENERALIZATION_DATASET_REGISTRY.json`, `research-labs/language-core-g1_v0.2.1/engineering/generalization/evidence/LM_GENERALIZATION_V3_RESULTS.json`, `research-labs/language-core-g1_v0.2.1/engineering/generalization/evidence/LM_GENERALIZATION_V3_VALIDATION.json`, `research-labs/language-core-g1_v0.2.1/engineering/generalization/evidence/GENERALIZATION_COMPOSITION_V3_DATASET_REGISTRY.json`, `research-labs/language-core-g1_v0.2.1/engineering/generalization/evidence/LM_GENERALIZATION_V4_RESULTS.json`, `research-labs/language-core-g1_v0.2.1/engineering/generalization/evidence/LM_GENERALIZATION_V4_VALIDATION.json`, `research-labs/language-core-g1_v0.2.1/engineering/generalization/evidence/GENERALIZATION_PERTURBATION_V4_DATASET_REGISTRY.json` |
| `RES-006` | `COMPLETE` | Governed retrieval gate robustness evaluation | `research-labs/language-core-g1_v0.2.1/engineering/retrieval/evidence/RETRIEVAL_ROBUSTNESS_RESULTS.json`, `research-labs/language-core-g1_v0.2.1/engineering/retrieval/RETRIEVAL_ROBUSTNESS_NOTE.md` |
| `RES-007` | `PARTIALLY_COMPLETE` | Governed model-swap continuity measurement | `research-labs/language-core-g1_v0.2.1/engineering/model_swap/evidence/MODEL_SWAP_CONTINUITY_RESULTS.json`, `research-labs/language-core-g1_v0.2.1/engineering/model_swap/evidence/MODEL_SWAP_CONTINUITY_VALIDATION.json`, `research-labs/language-core-g1_v0.2.1/engineering/model_swap/evidence/MODEL_SWAP_GOVERNANCE_STATE_REGISTRY.json`, `research-workbench/autonomous-growth/cycles/2026-08-13-model-swap-continuity.json` |
| `RES-008` | `PARTIALLY_COMPLETE` | Temporal continuity lexical-carryover falsification | `research-labs/language-core-g1_v0.2.1/engineering/temporal/evidence/TEMPORAL_CONTINUITY_FALSIFICATION_DATASET_REGISTRY.json`, `research-labs/language-core-g1_v0.2.1/engineering/temporal/evidence/TEMPORAL_CONTINUITY_LEXICAL_FALSIFICATION_RESULTS.json`, `research-labs/language-core-g1_v0.2.1/engineering/temporal/evidence/TEMPORAL_CONTINUITY_LEXICAL_FALSIFICATION_VALIDATION.json`, `research-workbench/autonomous-growth/cycles/2026-08-13-temporal-lexical-falsification.json` |
| `RES-009` | `PARTIALLY_COMPLETE` | Adult embodied-motivation signal separation research | `docs/AUTONOMOUS_RESEARCH_SCOPE_AUTHORIZATION_2026-08-13.md`, `research-workbench/autonomous-growth/evidence/SEXUALITY_RESEARCH_SOURCE_FINDINGS_2026-08-13.md`, `research-labs/language-core-g1_v0.2.1/engineering/sexuality/evidence/EMBODIED_MOTIVATION_DATASET_REGISTRY.json`, `research-labs/language-core-g1_v0.2.1/engineering/sexuality/evidence/EMBODIED_MOTIVATION_SIGNAL_RESULTS.json`, `research-labs/language-core-g1_v0.2.1/engineering/sexuality/evidence/EMBODIED_MOTIVATION_SIGNAL_VALIDATION.json`, `research-labs/language-core-g1_v0.2.1/engineering/sexuality/evidence/EMBODIED_MOTIVATION_V2_DATASET_REGISTRY.json`, `research-labs/language-core-g1_v0.2.1/engineering/sexuality/evidence/EMBODIED_MOTIVATION_SIGNAL_V2_RESULTS.json`, `research-labs/language-core-g1_v0.2.1/engineering/sexuality/evidence/EMBODIED_MOTIVATION_SIGNAL_V2_VALIDATION.json`, `research-labs/language-core-g1_v0.2.1/engineering/sexuality/evidence/EMBODIED_MOTIVATION_V3_DATASET_REGISTRY.json`, `research-labs/language-core-g1_v0.2.1/engineering/sexuality/evidence/EMBODIED_MOTIVATION_SIGNAL_V3_RESULTS.json`, `research-labs/language-core-g1_v0.2.1/engineering/sexuality/evidence/EMBODIED_MOTIVATION_SIGNAL_V3_VALIDATION.json` |

## Remaining gaps

| ID | Status | Dimensions | Item | Reason |
|---|---|---|---|---|
| `GAP-001` | `RESOURCE_BLOCKED` | `MODEL_REQUIRED`, `RESOURCE_BLOCKED` | Formal G1-Qwen3-4B-Instruct-2507 baseline and benchmark | The declared external baseline weights/runtime were unavailable under the local compute and dependency constraints; scratch models were not substituted. |
| `GAP-002` | `PARTIALLY_COMPLETE` | `MODEL_REQUIRED`, `RESEARCH_REQUIRED` | Scratch language model held-out and compositional generalization | V2 and V3 fixed synthetic splits with paired seeds show positive regularization improvements (V2 minimum 0.028870105743408203; V3 minimum 0.028661489486694336), but the results remain preliminary and do not establish robust out-of-distribution generalization or mature general-purpose capability. |
| `GAP-003` | `RESEARCH_REQUIRED` | `MODEL_REQUIRED`, `RESEARCH_REQUIRED` | Mature general-purpose AION language model usability | A mature general-purpose model claim is not established by the current small synthetic-corpus research checkpoints. |
| `GAP-004` | `SCIENTIFIC_OPEN_QUESTION` | `MODEL_REQUIRED`, `RESEARCH_REQUIRED` | Required-model completeness across all future AION/Astra capabilities | The current reconciliation closes known local model evidence but does not prove that every future capability has a complete learned-model requirement specification. |
| `GAP-005` | `EXTERNAL_DEPENDENCY` | `EXTERNAL_DEPENDENCY`, `OWNER_DECISION_REQUIRED` | Live private cross-session memory service | A live private service, data policy and owner-approved operational boundary are outside this local research reconciliation. |
| `GAP-006` | `OWNER_DECISION_REQUIRED` | `OWNER_DECISION_REQUIRED` | Canonical AION/Astra runtime promotion | Research integration remains non-canonical; no promotion decision is made in this task. |
| `GAP-007` | `OWNER_PROHIBITED` | `OWNER_PROHIBITED` | Production deployment | Deployment is explicitly outside this task and remains DEPLOYMENT=FALSE. |
| `GAP-008` | `INDEPENDENT_PARTY_REQUIRED` | `INDEPENDENT_PARTY_REQUIRED` | Independent IV&V | Independent review by a party separate from the implementer has not been achieved. |
| `GAP-009` | `SCIENTIFIC_OPEN_QUESTION` | `SCIENTIFIC_OPEN_QUESTION`, `INDEPENDENT_PARTY_REQUIRED` | Subjectivity, identity and relational conclusions | Current engineering evidence does not establish these scientific conclusions and no such claim is made. |
| `GAP-010` | `EXTERNAL_DEPENDENCY` | `EXTERNAL_DEPENDENCY`, `RESEARCH_REQUIRED` | Network MCP transport | The current candidate intentionally does not enable network MCP transport; in-process evidence is not network completion. |
| `GAP-011` | `PARTIALLY_COMPLETE` | `RESEARCH_REQUIRED`, `OWNER_PROHIBITED` | Twin embodiment, visual assets, sensation and sexuality-related scope | Three adult, scientific, research-only embodied-motivation cycles are complete as bounded evidence; V3 found paraphrase robustness inconclusive and broader sexuality/intimacy research remains open, while twin embodiment, sexual-response runtime, productization and deployment remain prohibited. |
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
