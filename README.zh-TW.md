# AION Governance Framework

> **繁體中文 | [English](README.md)**
>
> **從這裡開始：** [`docs/START_HERE.md`](docs/START_HERE.md)  
> **目前狀態：** [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md)  
> **完整文件索引：** [`docs/INDEX.md`](docs/INDEX.md)

AION 是一個以人類治理與 provenance-first 為核心的研究框架，用來研究身分、連續性、記憶、研究完整性，以及**人工主體性的可能性**；不把工程行為直接視為主體性證明。Astra 是相互區分的工程／研究工作台，用來實作與測試 bounded candidates。

```text
AI_SUBJECTIVITY_POSSIBILITY = CENTRAL_RESEARCH_QUESTION
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_AGENCY = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED
ENGINEERING_CAPABILITY != SUBJECTIVITY_EVIDENCE
CI_PASS != SCIENTIFIC_VALIDATION
```

## 目前狀態

2026-08-18 的倉庫 freeze 與 2026-08-20 的 project-work-loop termination 仍是被保存的歷史事件。之後的 bounded maintenance 與 research-materialization 都是另外逐次授權，不會回溯改寫那些歷史事件。

目前 `main` 包含經 Human Owner 明確批准後收斂的 bounded research / instrumentation baseline。較早的收斂已建立主體性相關證據處理、Endogenous Goal Dynamics、bounded AION/Astra inquiry、七態功能性研究表面、theory-plural indicator mapping、governed knowledge sources、Four-Domain interpretation、Evidence Interop、multimodal evidence handling、bounded autonomous research campaigns，以及經整理的 mechanism / provenance experiments。

最新一輪 bounded convergence 新增四個研究方法表面：

- **Provenance-to-claim quality admission：** [`coupled-cognition-quality-factory_v0.1.0`](research-labs/coupled-cognition-quality-factory_v0.1.0/README.md) 現在包含 fail-closed 的 provenance-to-claim admission gate。它檢查的是結構可接受性與 provenance discipline，不判定科學真偽。
- **Human–AI longitudinal grounding / epistemic-policy study design：** [`HUMAN_AI_BIDIRECTIONAL_GROUNDING_HYPOTHESIS_2026_09_11.md`](docs/research/HUMAN_AI_BIDIRECTIONAL_GROUNDING_HYPOTHESIS_2026_09_11.md)、[`INTERACTION_KNOWLEDGE_DENSITY_AND_TASK_CONDITIONED_EPISTEMIC_POLICY_2026_09_11.md`](docs/research/INTERACTION_KNOWLEDGE_DENSITY_AND_TASK_CONDITIONED_EPISTEMIC_POLICY_2026_09_11.md) 與 [`human-ai-longitudinal-study_v0.1.0`](research-labs/human-ai-longitudinal-study_v0.1.0/README.md) 提供 bounded comparison infrastructure。Harness 只驗證 bindings 與 contrast structure。
- **Interaction-history-mediated adaptation：** [`INTERACTION_HISTORY_MEDIATED_ADAPTATION_2026_09_11.md`](docs/research/INTERACTION_HISTORY_MEDIATED_ADAPTATION_2026_09_11.md) 與 [`interaction-history-study_v0.1.0`](research-labs/interaction-history-study_v0.1.0/README.md) 綁定 sandbox、runtime / task、artifact event 與 cross-participant reuse evidence。Harness 不執行 agent，也不因此建立 individual learning。
- **Endogenous memory significance：** [`ENDOGENOUS_MEMORY_SIGNIFICANCE_HYPOTHESIS_2026_09_11.md`](docs/research/ENDOGENOUS_MEMORY_SIGNIFICANCE_HYPOTHESIS_2026_09_11.md) 與 [`memory-value-divergence-probe_v0.1.0`](experiments/memory-value-divergence-probe_v0.1.0/README.md) 實作一個狹義的 synthetic H-MS1 policy-divergence probe；`H_MS2_ENDOGENOUS_SELF_RELEVANCE = NOT_TESTED`。

```text
CLAIM_ADMISSION_PASS != CLAIM_TRUE
HARNESS_PASS != HYPOTHESIS_CONFIRMED
METRIC_DELTA != CAUSAL_IDENTIFICATION
ARTIFACT_READ_OBSERVED != INTERNAL_REPRESENTATION_CHANGED
SYSTEM_LEVEL_ADAPTATION != INDIVIDUAL_LEARNING_PROVEN
POLICY_DIVERGENCE != SCIENTIFIC_VALIDATION
SELECTIVE_RETENTION != DESIRE_TO_REMEMBER
```

這些新增內容提升可測試性、可反證性、provenance、comparability 與 evidence discipline；它們**不會**因此建立主體性、意識、現象經驗、道德能動性、道德地位、身分連續性、獨立 replication、whole-system validation 或 independent IV&V。

`main` 仍是本倉庫的 durable branch topology。歷史 candidate lineage 由 merged commits、pull requests 與 Git objects 保持可稽核。

要看「現在到底是什麼狀態」，請讀 [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md)。若要確認某一顆 exact commit 的工程狀態，請看即時 GitHub / CI evidence，而不是靜態文件。

## 依目的閱讀

- **第一次進來：** [`docs/START_HERE.md`](docs/START_HERE.md)
- **目前語意狀態：** [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md)
- **研究貢獻摘要：** [`docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md`](docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md)
- **主體性 evidence method：** [`docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md`](docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md)
- **架構：** [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- **明確不能宣稱什麼：** [`docs/NON_CLAIMS.md`](docs/NON_CLAIMS.md)
- **Provenance 與 authority：** [`docs/PROVENANCE.md`](docs/PROVENANCE.md) 與 [`docs/governance/`](docs/governance/)
- **Engineering evidence / QA：** [`qa/README.md`](qa/README.md)
- **完整文件地圖：** [`docs/INDEX.md`](docs/INDEX.md)
- **歷史紀錄：** [`docs/history/`](docs/history/)

## 治理邊界

```text
FULL_AUTOMATION != FULL_AUTHORITY
NORMATIVE_STATE != AUTHORITY
ENDOGENOUS_GOAL != AUTHORIZED_GOAL
SOURCE_USE != WRITEBACK_AUTHORITY
QA_PASS != MERGE_APPROVAL
AI_REVIEW != HUMAN_OWNER_MERGE_APPROVAL
AUTONOMOUS_MERGE = NO
AUTONOMOUS_REPOSITORY_WRITEBACK = NO
DEPLOYMENT = NO
```

未來任何 protected-main transition 都必須有 fresh、action-specific、exact-head Human Owner approval；過去的批准不會自動沿用到新的 head。

## 授權

原有核心採 Apache-2.0。選用的 [`Swiss Ephemeris example`](examples/swiss-ephemeris-agpl_v0.1.0/README.md) 採 AGPL-3.0-only，因此整個倉庫不能概括標示為只有 Apache-2.0。詳見 [`授權範圍`](docs/governance/OPTIONAL_AGPL_LICENSE_SCOPE.md)、[`LICENSE`](LICENSE)、[`NOTICE`](NOTICE) 與 [`CITATION.cff`](CITATION.cff)。
