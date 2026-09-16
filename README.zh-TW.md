# AION Governance Framework

> **繁體中文 | [English](README.md)**
>
> **從這裡開始：** [`docs/START_HERE.md`](docs/START_HERE.md)  
> **目前狀態：** [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md)  
> **完整文件索引：** [`docs/INDEX.md`](docs/INDEX.md)
>
> **操作恢復交接 — 2026-09-17：** PR #136 已在未合併的狀態下關閉；最終仔細審查發現仍有研究設計與實作語意問題。未來 Work、Codex 或 ChatGPT Teacher 的工作應從即時 `main` 開始，不應只靠記憶，也不應直接延續已關閉的 PR 分支。請先讀 [`PR136_CLOSEOUT_AND_NEXT_IMPLEMENTATION_HANDOFF_2026_09_17.md`](docs/history/PR136_CLOSEOUT_AND_NEXT_IMPLEMENTATION_HANDOFF_2026_09_17.md)。

AION 是一個以人類治理與 provenance-first（來源追溯優先）為核心的研究框架，用來研究身分、連續性、記憶、研究完整性，以及**人工主體性的可能性**；不把工程行為直接視為主體性證明。Astra 是相互區分的工程／研究工作台，用來實作與測試 bounded candidates（有限範圍候選方案）。

```text
AI_SUBJECTIVITY_POSSIBILITY = CENTRAL_RESEARCH_QUESTION
人工主體性可能性 = 中央研究問題

SUBJECTIVITY = NOT_ESTABLISHED
主體性 = 尚未建立

CONSCIOUSNESS = NOT_ESTABLISHED
意識 = 尚未建立

PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
現象經驗 = 尚未建立

MORAL_AGENCY = NOT_ESTABLISHED
道德能動性 = 尚未建立

MORAL_STATUS = NOT_ESTABLISHED
道德地位 = 尚未建立

ENGINEERING_CAPABILITY != SUBJECTIVITY_EVIDENCE
工程能力 != 主體性證據

CI_PASS != SCIENTIFIC_VALIDATION
持續整合通過 != 科學驗證
```

## 目前狀態

2026-08-18 的倉庫 freeze（凍結）與 2026-08-20 的 project-work-loop termination（專案工作迴圈終止）仍是被保存的歷史事件。之後的 bounded maintenance（有限範圍維護）與 research-materialization（研究實體化）都是另外逐次授權，不會回溯改寫那些歷史事件。

目前 `main` 包含經 Human Owner 明確批准後收斂的 bounded research / instrumentation baseline（有限範圍研究／儀器化基線），包括主體性相關 evidence handling（證據處理）、Endogenous Goal Dynamics（內生目標動力學）、Four-Domain interpretation（四域詮釋）、Evidence Interop（證據互通）、governed knowledge sources（受治理知識來源）、multimodal evidence handling（多模態證據處理）、bounded research campaigns（有限範圍研究活動）、provenance / quality controls（來源追溯／品質控制），以及 Human–AI longitudinal research surfaces（人類—AI 縱向研究介面）。語意現況請讀 [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md)，完整導航請讀 [`docs/INDEX.md`](docs/INDEX.md)。

最新 bounded convergence（有限範圍收斂）為 PR #126 -> #127 -> #128，新增 repository-defined（倉庫自行定義）的 **共構思考場域（Co-Constructed Thinking Space, CCTS）** 研究表面。[`CO_CONSTRUCTED_THINKING_SPACE_FORMALIZATION_2026_09_16.md`](docs/research/CO_CONSTRUCTED_THINKING_SPACE_FORMALIZATION_2026_09_16.md) 定義 local construct（本地構念）與來源歸屬；後續 hardening（強化）要求雙向 substantive `REVISES` / `CHALLENGES`（實質修正／挑戰）、可追溯綁定的 longitudinal repository artifacts（縱向倉庫產物），以及 typed grounding checkpoint（有型別的共同理解檢查點）。只有當 grounding（對齊／共同理解檢查）為 `SUFFICIENT_FOR_CURRENT_PURPOSE`（足以供目前目的使用）且沒有 unresolved mismatch（未解決的不一致）時，CCTS admission（准入）才可通過。詳見 [`CCTS_GROUNDING_ADMISSION_EXTENSION_2026_09_16.md`](docs/research/CCTS_GROUNDING_ADMISSION_EXTENSION_2026_09_16.md)。

```text
CCTS_STRUCTURAL_CONFORMANCE != SHARED_MIND
CCTS 結構符合 != 共享心智

GROUNDING_ADEQUACY != MUTUAL_UNDERSTANDING_PROVEN
共同理解檢查足夠 != 已證明相互理解

CCTS != AI_SUBJECTIVITY
CCTS != AI 主體性

HARNESS_PASS != HYPOTHESIS_CONFIRMED
研究測試框架通過 != 假說已確認
```

CCTS 提升的是結構可稽核性；它**不會**因此建立主體性、意識、現象經驗、相互理解、道德能動性、道德地位、身分連續性、independent replication（獨立重複驗證）、whole-system validation（整體系統驗證）或 independent IV&V（獨立驗證與確認）。

若要確認某一顆 exact commit（精確提交）的工程狀態，請看即時 GitHub / CI（持續整合）證據，而不是靜態文件。

## 依目的閱讀

- **第一次進來：** [`docs/START_HERE.md`](docs/START_HERE.md)
- **目前語意狀態：** [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md)
- **目前恢復／下一次實作交接：** [`docs/history/PR136_CLOSEOUT_AND_NEXT_IMPLEMENTATION_HANDOFF_2026_09_17.md`](docs/history/PR136_CLOSEOUT_AND_NEXT_IMPLEMENTATION_HANDOFF_2026_09_17.md)
- **查看 CCTS：** [`docs/research/CO_CONSTRUCTED_THINKING_SPACE_FORMALIZATION_2026_09_16.md`](docs/research/CO_CONSTRUCTED_THINKING_SPACE_FORMALIZATION_2026_09_16.md) 與 [`docs/research/CCTS_GROUNDING_ADMISSION_EXTENSION_2026_09_16.md`](docs/research/CCTS_GROUNDING_ADMISSION_EXTENSION_2026_09_16.md)
- **安裝：** [`docs/INSTALLATION.md`](docs/INSTALLATION.md)
- **快速開始：** [`docs/QUICKSTART.md`](docs/QUICKSTART.md)
- **目前程式介面：** [`docs/API.md`](docs/API.md)
- **語言中立整合：** [`docs/INTEROPERABILITY.md`](docs/INTEROPERABILITY.md)
- **研究貢獻摘要：** [`docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md`](docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md)
- **主體性證據方法：** [`docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md`](docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md)
- **架構與不宣稱事項：** [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) 與 [`docs/NON_CLAIMS.md`](docs/NON_CLAIMS.md)
- **來源追溯與授權：** [`docs/PROVENANCE.md`](docs/PROVENANCE.md) 與 [`docs/governance/`](docs/governance/)
- **工程證據／品質保證：** [`qa/README.md`](qa/README.md)
- **完整文件地圖：** [`docs/INDEX.md`](docs/INDEX.md)
- **歷史紀錄：** [`docs/history/`](docs/history/)

## 治理邊界

```text
FULL_AUTOMATION != FULL_AUTHORITY
完整自動化 != 完整權限

NORMATIVE_STATE != AUTHORITY
規範狀態 != 授權

ENDOGENOUS_GOAL != AUTHORIZED_GOAL
內生目標 != 已授權目標

SOURCE_USE != WRITEBACK_AUTHORITY
使用來源 != 回寫權限

QA_PASS != MERGE_APPROVAL
品質保證通過 != 合併批准

AI_REVIEW != HUMAN_OWNER_MERGE_APPROVAL
AI 審查 != Human Owner 合併批准

AUTONOMOUS_MERGE = NO
自主合併 = 否

AUTONOMOUS_REPOSITORY_WRITEBACK = NO
自主回寫倉庫 = 否

DEPLOYMENT = NO
部署 = 否
```

未來任何 protected-main transition（受保護主分支轉移）都必須有 fresh（最新）、action-specific（針對該次動作）、exact-head（精確分支提交）的 Human Owner approval（批准）；過去的批准不會自動沿用到新的 head。

## 授權

原有核心採 Apache-2.0。選用的 [`Swiss Ephemeris example`](examples/swiss-ephemeris-agpl_v0.1.0/README.md) 採 AGPL-3.0-only，因此整個倉庫不能概括標示為只有 Apache-2.0。詳見 [`授權範圍`](docs/governance/OPTIONAL_AGPL_LICENSE_SCOPE.md)、[`LICENSE`](LICENSE)、[`NOTICE`](NOTICE) 與 [`CITATION.cff`](CITATION.cff)。
