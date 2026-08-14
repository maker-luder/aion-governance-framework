# AION 外部來源驗證紀錄 — 2026-08-14

## Provenance 與治理狀態

| 欄位 | 值 |
|---|---|
| `RECORD_TYPE` | `EXTERNAL_SOURCE_VERIFICATION` |
| `ACTOR` | `MANUS` |
| `SOURCE` | Human Owner 提供的 `aion_incomplete_web_sources.md`，以及下列官方 primary sources |
| `BASE_SHA` | `7779ebb0c5597e773b3350141e42b4b44a069134` |
| `SANDBOX_HEAD` | `7779ebb0c5597e773b3350141e42b4b44a069134` |
| `AUTHORITY_STATUS` | `NON_CANONICAL / SANDBOX_RESEARCH` |
| `REVIEWED_BY` | `MANUS`；Human Owner review `PENDING` |
| `APPROVED_BY` | `NONE / PENDING` |
| `RUNTIME_EFFECT` | `NONE` |
| `CANONICAL_EFFECT` | `NONE` |
| `DEPLOYMENT` | `FALSE` |

> 本紀錄保存來源觀察與 repository 對照，不把 Manus 的 inference 寫成 Human Owner 立場，也不把外部文件、內部測試或 sandbox 結果提升為 canonical conclusion、scientific validation 或 independent IVV。

## External primary-source observations

| 編號 | 官方來源 | 已核對的觀察 | 不能由來源單獨推出的結論 |
|---|---|---|---|
| 1 | [Qwen3-4B model card][1] | Qwen3-4B model card lists 4.0B parameters, 3.6B non-embedding parameters, 36 layers, native 32,768-token context, and long-text handling validated up to 131,072 tokens with YaRN. | It does not establish an AION-local benchmark, hardware threshold, model execution, or score. |
| 2 | [Qwen3 official repository][2] | The official repository provides Qwen3 README and deployment/inference documentation with named framework paths and model variants. | Documentation does not establish a pinned AION serving stack, environment capture, deployment, or reproducible benchmark execution. |
| 3 | [Hugging Face PEFT LoRA documentation][3] | LoRA freezes pretrained weights and injects trainable low-rank matrices; the API exposes explicit adapter choices such as rank, target modules, scaling and modules to save. | A method description or configuration is not a real adapter run, checkpoint, dataset-provenance record, or validation result. |
| 4 | [Hugging Face Transformers Trainer documentation][4] | Trainer provides a PyTorch training/evaluation loop and documents distributed/mixed-precision support plus reproducibility-relevant training, evaluation, checkpoint and resume controls. | It does not establish that AION executed training or produced a validated checkpoint. |
| 5 | [Ollama generate API][5] | The response contract includes model, creation time, response, completion status/reason, nanosecond timing fields, prompt/output token counts, and optional log probabilities. | The contract does not establish a live Ollama call, pinned model/runtime, or AION metric result. |
| 6 | [Ollama usage documentation][6] | Usage fields distinguish `total_duration`, `load_duration`, `prompt_eval_count`, `prompt_eval_duration`, `eval_count` and `eval_duration`. | No service call, tokenizer benchmark, streaming-parity run or performance claim was produced here. |
| 7 | [NIST AI TEVV][7] | NIST describes AI evaluation as context-sensitive measurement work involving quantitative and qualitative metrics, testbeds, datasets, tools, standards-oriented guidance, and technical gaps/limitations. | This is methodological context, not repository certification, approval or independent review. |
| 8 | [NIST AI Risk Management Framework][8] | NIST describes AI RMF 1.0 as voluntary guidance for incorporating trustworthiness considerations into AI design, development, use and evaluation; the page also notes ongoing revision. | NIST does not certify or approve AION, and internal QA cannot become independent IVV by citation alone. |

## Repository evidence comparison

| Area | Repository observation | Classification | Current boundary |
|---|---|---|---|
| Formal G1 | `research-labs/language-core-g1_v0.2.1/evaluation/G1_BASELINE_EXECUTION_STATUS.json` records `BLOCKED_BY_COMPUTE_ENVIRONMENT`, `model_loaded=false`, `benchmark_executed=false`, and `metrics=null`. | `REPOSITORY_EVIDENCE` | The task remains unexecuted; no score or local hardware threshold is inferred. |
| Real LoRA | `engineering/lora/LORA_ENVIRONMENT_DECISION.json` records `REAL_LORA_TRAINING=BLOCKED_BY_COMPUTE_ENVIRONMENT`; the dry-run records `DRY_RUN_PASS` with `real_training=false` for LIGHT and STANDARD. | `REPOSITORY_EVIDENCE` | Dry-run and configuration readiness remain distinct from real training and checkpoint evidence. |
| Tokenizer／telemetry | `evaluation/OFFLINE_TOKENIZER_TELEMETRY_FIXTURE.json` records `OFFLINE_CONTRACT_ONLY`, `tokenizer_execution_status=NOT_EXECUTED`, null token counts, nanosecond `/api/generate` assumptions, malformed payload cases, `benchmark_execution=NOT_EXECUTED`, and `streaming_parity=NOT_VALIDATED`. | `REPOSITORY_EVIDENCE` | The fixture validates a model-free contract only; it is not a tokenizer run, Ollama run or benchmark. |
| Global status | `qa/CURRENT_RELEASE_STATUS_LOCK.json` records formal G1, real LoRA and actual ablation as `NOT_EXECUTED`, whole-system validation as `NOT_EXECUTED`, and `independent_ivv` as `NOT_ACHIEVED`. | `REPOSITORY_EVIDENCE` | External sources do not alter these locked status words. |
| IVV | `docs/IVV_READINESS_PACKET.md` is `PREPARE_EVIDENCE_ONLY` and states that creator/assistant implementation, repository tests and CI are not independent IVV. | `GOVERNANCE_BOUNDARY` | NIST methodology is consistent with this separation but does not perform the review. |

## Mapping and non-claims

The verified sources support future preparation requirements: pin a model revision and serving stack, capture hardware and dependency versions, preserve dataset/config/base-model hashes, record seeds and checkpoint/resume state, validate telemetry field types and units, and distinguish offline fixtures from live execution. These are `MANUS_INFERENCE` combined with `REPOSITORY_EVIDENCE`, not upstream Qwen, Hugging Face, Ollama or NIST statements.

No model was downloaded, no real benchmark was executed, no LoRA adapter was trained, no Ollama service was called, no deployment occurred, and no independent IVV was performed in this research cycle. Existing `DEFERRED`, `HOLD`, `NOT_EXECUTED`, `NOT_ACHIEVED`, `CANONICAL_EFFECT = NONE`, and `DEPLOYMENT = FALSE` boundaries remain unchanged.

## References

[1]: https://huggingface.co/Qwen/Qwen3-4B "Qwen/Qwen3-4B model card"
[2]: https://github.com/QwenLM/Qwen3 "QwenLM/Qwen3 official repository"
[3]: https://huggingface.co/docs/peft/en/package_reference/lora "Hugging Face PEFT LoRA documentation"
[4]: https://huggingface.co/docs/transformers/en/main_classes/trainer "Hugging Face Transformers Trainer documentation"
[5]: https://docs.ollama.com/api/generate "Ollama generate API"
[6]: https://docs.ollama.com/api/usage "Ollama usage documentation"
[7]: https://www.nist.gov/ai-test-evaluation-validation-and-verification-tevv "NIST AI test, evaluation, validation and verification"
[8]: https://www.nist.gov/itl/ai-risk-management-framework "NIST AI Risk Management Framework"
