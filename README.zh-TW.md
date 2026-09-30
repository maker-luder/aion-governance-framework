# AION Governance Framework｜AION 治理研究框架

> **繁體中文 | [English](README.md)**
>
> **60 秒研究地圖：** [`docs/RESEARCH_MAP.md`](docs/RESEARCH_MAP.md)  
> **5 分鐘導覽：** [`docs/START_HERE.md`](docs/START_HERE.md)  
> **語意現況摘要：** [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md)  
> **精確 tip 工程狀態：** 以即時 GitHub / CI 為準

AION 是一個由人類治理、以來源追溯為優先的研究框架，用來研究**人工主體性的可能性**，但不會把看起來有說服力的 AI 行為直接當成主體性證明。

用白話說，這個倉庫正在問：

> 當 AI 系統出現類記憶連續性、策略改變、長時間持續工作、協作或自我相關行為時，其中多少其實可以由模型、提示、harness（研究／執行框架）、工具、記憶、環境或人類引導解釋？排除這些較簡單來源後，還需要什麼證據，才有資格提出更強的主體性相關主張？

目前答案刻意維持保守：

```text
AI_SUBJECTIVITY_POSSIBILITY = CENTRAL_RESEARCH_QUESTION
人工主體性可能性 = 中央研究問題

SCIENTIFIC_DISPOSITION = HOLD
科學結論狀態 = 保留判斷

SUBJECTIVITY = NOT_ESTABLISHED
主體性 = 尚未建立

CONSCIOUSNESS = NOT_ESTABLISHED
意識 = 尚未建立

PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
現象經驗 = 尚未建立
```

## 研究目前走到哪裡？

目前 `main` 可整理成四條彼此相連的研究線：

1. **證據與因果來源** —— Four-Domain（四域）解讀、六個主體性相關證據維度、來源追溯，以及 model / system / harness / context / tool / environment 的因果位置拆分。
2. **連續性與歷史** —— 記憶、長期互動、history replay（歷史重播）、attention structure（注意力結構）重建、transition continuity（轉換連續性）分析，以及在資訊內容匹配條件下的 memory-locus dependency discrimination（記憶資訊所在位置／依賴區辨）；但不把持續存在直接等同於身分延續。
3. **受限制條件下的適應與區辨測試** —— CCAP Stage 1–3 已推進到 TEVV 執行前映射、Four-Domain × 六維結構壓力測試、系統邊界／區辨硬化，以及 synthetic D2 × D4 differential probe（合成差異探針）。目前只顯示**測試夾具層級的可分離性**；D2 支持、D4 支持與獨立驗證仍然**尚未建立**。
4. **Human–AI collaboration / learning（人機協作／學習）與證據准入** —— CCTS 是倉庫定義的結構框架，第一份學術物件已公開典藏於 [Zenodo](https://zenodo.org/records/22945883)（DOI [10.5281/zenodo.22945883](https://doi.org/10.5281/zenodo.22945883)）；目前的手稿草稿**尚未發布**。`main` 現也有 synthetic matched learning contrast（合成匹配學習對照）設計；Human learning（人類學習）、retention（保持）、transfer（遷移）、causal effect（因果效果）與 CCTS-specific effect（CCTS 特定效果）仍**尚未建立**。

## 目前研究快照

首頁只保留最高層級的目前圖像。若要看有日期的里程碑、精確 merged 現況與完整文件地圖，請進入 [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md) 與 [`docs/INDEX.md`](docs/INDEX.md)。

- **連續性與記憶：** history replay、attention-structure 區辨、exact-structure longitudinal claim admission，以及 matched-information memory-locus dependency 測試。
- **Human–AI learning / collaboration（人機學習／協作）：** CCTS 的結構適用範圍沿用有界問題及依當前目的判定的 grounding（共同理解校準）。目前無理由新增獨立的 applicability（適用性）構念；學習相關性只作研究設計提醒。合成匹配對照沒有建立學習效果。
- **證據准入：** bounded 12-axis provider-evidence admission 已擴展到多個 provider family，但 open independent replication 仍然稀少。
- **Assurance / quality：** TEVV、Full-QMS、adversarial-security、FAIR4RS、NCR/CAPA 與 bounded supply-chain Phase 1 提高 traceability，但不代表科學驗證、release authority 或 SLSA conformance。

## 這個倉庫沒有宣稱什麼？

```text
ENGINEERING_CAPABILITY != SUBJECTIVITY_EVIDENCE
工程能力 != 主體性證據

MEMORY_CONTINUITY != IDENTITY_CONTINUITY
記憶連續性 != 身分連續性

RETRIEVABILITY != MEMORY_CONTINUITY
能檢索到資訊 != 記憶連續性

STRUCTURAL_ADMISSIBILITY != FUNCTIONAL_DEPENDENCY
結構可接受性 != 功能依賴已建立

ADMISSION_PASS != CLAIM_TRUE
主張准入通過 != 主張為真

PROVIDER_ADMISSION != INDEPENDENT_VALIDATION
供應商證據准入 != 獨立驗證

HUMAN_AI_LEARNING_CROSSWALK != SUBJECTIVITY_EVIDENCE
人機學習交叉比對 != 主體性證據

STRATEGY_ADJUSTMENT != ENDOGENOUS_GOAL
策略調整 != 內生目標

HUMAN_AI_COLLABORATION != SHARED_MIND
人機協作 != 共享心智

STRUCTURAL_INTEGRITY != DISCRIMINANT_VALIDITY
結構完整性 != 區辨效度

SYNTHETIC_SEPARABILITY != D2_OR_D4_SUPPORT
合成可分離性 != D2 或 D4 的科學支持

HARNESS_PASS != HYPOTHESIS_CONFIRMED
研究測試框架通過 != 假說已確認

CI_PASS != SCIENTIFIC_VALIDATION
持續整合通過 != 科學驗證
```

這些邊界不是先替研究問題決定答案，而是避免結論超過證據能支撐的範圍。

## CCTS 與人機學習入口

- **已典藏的學術物件：** [目前發布 metadata（詮釋資料）](docs/research/publication/CCTS_RELEASE_METADATA_CURRENT.md)記錄第一份 CCTS 學術物件及 DOI [10.5281/zenodo.22945883](https://doi.org/10.5281/zenodo.22945883)已公開典藏；**尚未經同儕審查，也未獲科學驗證**。
- **目前手稿：** [倉庫中的手稿草稿](docs/research/publication/CCTS_PREPRINT_DRAFT_V0_1.md)標為 `NOT_RELEASED`（尚未發布）。既有 DOI 不代表這份草稿版本已發布。
- **框架與研究設計：** 依序閱讀 [CCTS 形式化](docs/research/CO_CONSTRUCTED_THINKING_SPACE_FORMALIZATION_2026_09_16.md)、[grounding 准入](docs/research/CCTS_GROUNDING_ADMISSION_EXTENSION_2026_09_16.md)、[合成學習對照](docs/research/CCTS_LEARNING_CONTRAST_STRENGTHENING_2026-09-28.md)。[適用性審查](docs/research/CCTS_HUMAN_AI_LEARNING_APPLICABILITY_BOUNDARY_HYPOTHESIS_2026_09_30.md)沒有新增獨立的 CCTS／學習構念或閘門。

```text
PUBLICATION != SCIENTIFIC_VALIDATION
公開典藏 != 科學驗證

IMPLEMENTATION != SCIENTIFIC_ESTABLISHMENT
已有實作 != 科學結論成立

HUMAN_LEARNING / RETENTION / TRANSFER / CAUSAL_EFFECT / CCTS_SPECIFIC_EFFECT = NOT_ESTABLISHED
人類學習／保持／遷移／因果效果／CCTS 特定效果 = 尚未建立
```

## 依閱讀深度選入口

- **我只有一分鐘：** [`docs/RESEARCH_MAP.md`](docs/RESEARCH_MAP.md)
- **我想先被帶著看懂：** [`docs/START_HERE.md`](docs/START_HERE.md)
- **我要確認正式語意現況：** [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md)
- **我要一頁看研究貢獻：** [`docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md`](docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md)
- **我要看主體性證據方法：** [`docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md`](docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md)
- **我要看架構／不宣稱事項：** [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) 與 [`docs/NON_CLAIMS.md`](docs/NON_CLAIMS.md)
- **我要查來源與治理：** [`docs/PROVENANCE.md`](docs/PROVENANCE.md) 與 [`docs/governance/`](docs/governance/)
- **我要完整文件地圖：** [`docs/INDEX.md`](docs/INDEX.md)

若要確認某一顆精確提交的工程狀態，請以即時 GitHub / CI 證據為準，而不是只看靜態文件。

## 工程與互通

- 安裝／快速開始：[`docs/INSTALLATION.md`](docs/INSTALLATION.md)、[`docs/QUICKSTART.md`](docs/QUICKSTART.md)
- 公開 API 參考：[`docs/API.md`](docs/API.md)
- 互通整合：[`docs/INTEROPERABILITY.md`](docs/INTEROPERABILITY.md)

Astra 是與 AION 相互區分的工程／研究工作台，用來實作與測試有限範圍候選方案；它不是 AION 的身分、記憶流或主體性替代物。

**目前工程狀態：** `main` 已包含 quality、security、evidence admission、continuity、CCAP、Human–AI learning contrast 與 supply-chain Phase 1 的 bounded research / assurance 工具；它們不代表科學驗證、人類學習、主體性、身分連續性、安全有效或 release readiness。

## 治理與授權

AION 維持人類治理。工程能力、自動化、品質檢查、AI 審查或過去的批准，都不能自行產生把新變更送入 `main` 的授權。

```text
QA_PASS != MERGE_APPROVAL
品質保證通過 != 合併批准

AI_REVIEW != HUMAN_OWNER_MERGE_APPROVAL
AI 審查 != Human Owner 合併批准

AUTONOMOUS_MERGE = NO
自主合併 = 否

AUTONOMOUS_REPOSITORY_WRITEBACK = NO
自主回寫倉庫 = 否
```

核心倉庫採 Apache-2.0。選用的 [`Swiss Ephemeris（瑞士星曆）範例`](examples/swiss-ephemeris-agpl_v0.1.0/README.md) 採 AGPL-3.0-only，因此不能把整個倉庫簡化描述為「全部都是 Apache-2.0」。詳見 [`LICENSE`](LICENSE)、[`NOTICE`](NOTICE)、[`CITATION.cff`](CITATION.cff) 與 [`docs/governance/OPTIONAL_AGPL_LICENSE_SCOPE.md`](docs/governance/OPTIONAL_AGPL_LICENSE_SCOPE.md)。

若要參與貢獻、回報安全問題或引用本研究，請見 [`CONTRIBUTING.md`](CONTRIBUTING.md)、[`SECURITY.md`](SECURITY.md) 與 [`CITATION.cff`](CITATION.cff)。
