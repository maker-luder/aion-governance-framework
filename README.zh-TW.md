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

目前 `main` 包含經 Human Owner 明確批准後收斂的 bounded research / instrumentation baseline，包括主體性相關 evidence handling、Endogenous Goal Dynamics、Four-Domain interpretation、Evidence Interop、governed knowledge sources、multimodal evidence handling、bounded research campaigns、provenance / quality controls，以及 Human–AI longitudinal research surfaces。語意現況請讀 [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md)，完整導航請讀 [`docs/INDEX.md`](docs/INDEX.md)。

最新 bounded convergence 為 PR #126 -> #127 -> #128，新增 repository-defined 的 **共構思考場域（Co-Constructed Thinking Space, CCTS）** 研究表面。[`CO_CONSTRUCTED_THINKING_SPACE_FORMALIZATION_2026_09_16.md`](docs/research/CO_CONSTRUCTED_THINKING_SPACE_FORMALIZATION_2026_09_16.md) 定義 local construct 與來源歸屬；後續 hardening 要求雙向 substantive `REVISES` / `CHALLENGES`、可追溯綁定的 longitudinal repository artifacts，以及 typed grounding checkpoint。只有當 grounding 為 `SUFFICIENT_FOR_CURRENT_PURPOSE` 且沒有 unresolved mismatch 時，CCTS admission 才可通過。詳見 [`CCTS_GROUNDING_ADMISSION_EXTENSION_2026_09_16.md`](docs/research/CCTS_GROUNDING_ADMISSION_EXTENSION_2026_09_16.md)。

```text
CCTS_STRUCTURAL_CONFORMANCE != SHARED_MIND
GROUNDING_ADEQUACY != MUTUAL_UNDERSTANDING_PROVEN
CCTS != AI_SUBJECTIVITY
HARNESS_PASS != HYPOTHESIS_CONFIRMED
```

CCTS 提升的是結構可稽核性；它**不會**因此建立主體性、意識、現象經驗、相互理解、道德能動性、道德地位、身分連續性、獨立 replication、whole-system validation 或 independent IV&V。

若要確認某一顆 exact commit 的工程狀態，請看即時 GitHub / CI evidence，而不是靜態文件。

## 依目的閱讀

- **第一次進來：** [`docs/START_HERE.md`](docs/START_HERE.md)
- **目前語意狀態：** [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md)
- **查看 CCTS：** [`docs/research/CO_CONSTRUCTED_THINKING_SPACE_FORMALIZATION_2026_09_16.md`](docs/research/CO_CONSTRUCTED_THINKING_SPACE_FORMALIZATION_2026_09_16.md) 與 [`docs/research/CCTS_GROUNDING_ADMISSION_EXTENSION_2026_09_16.md`](docs/research/CCTS_GROUNDING_ADMISSION_EXTENSION_2026_09_16.md)
- **安裝：** [`docs/INSTALLATION.md`](docs/INSTALLATION.md)
- **快速開始：** [`docs/QUICKSTART.md`](docs/QUICKSTART.md)
- **目前程式介面：** [`docs/API.md`](docs/API.md)
- **語言中立整合：** [`docs/INTEROPERABILITY.md`](docs/INTEROPERABILITY.md)
- **研究貢獻摘要：** [`docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md`](docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md)
- **主體性 evidence method：** [`docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md`](docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md)
- **架構與 non-claims：** [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) 與 [`docs/NON_CLAIMS.md`](docs/NON_CLAIMS.md)
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
