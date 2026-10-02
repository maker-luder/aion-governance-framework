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

**AI 主體性可能性一直是中央研究問題。** 往後工作依下列順位路由；這份導覽不重新啟動已終止的 project work loop（專案工作循環），也不代表取得新的科學結論：

1. **第一核心／`main`：AI 主體性可能性。** Four-Domain（四域）解讀、六個證據維度、因果來源、連續性與適應仍屬核心問題的不同面向。主體性、意識與現象經驗尚未建立。
2. **第二：[CCTS／人機學習](https://github.com/maker-luder/aion-governance-framework/blob/research/ccts-human-ai-learning-lane/docs/research/ccts-human-ai-learning/README.md)。** [首份 CCTS 學術物件](docs/research/publication/CCTS_RELEASE_METADATA_CURRENT.md)已有公開典藏（DOI [10.5281/zenodo.22945883](https://doi.org/10.5281/zenodo.22945883)）；[目前手稿草稿](docs/research/publication/CCTS_PREPRINT_DRAFT_V0_1.md)仍是 `NOT_RELEASED`。人類學習、保持、遷移、因果及 CCTS 特定效果尚未建立。
3. **第三：[獨立具身工作支線](https://github.com/maker-luder/aion-governance-framework/blob/research/embodiment-lane/docs/research/embodiment/README.md)。** main 保留較早的 baseline（基礎候選）；已關閉、未合併的實驗仍須分開審查。合成實作不能建立生物量測、感受或主體性。

[歷史來源歸屬待定的臨時整理線](https://github.com/maker-luder/aion-governance-framework/blob/research/legacy-uncertainty-hold/docs/research/legacy-uncertainty/README.md)只保存待審來源指標，不是第四個研究構念；舊分支仍保留。

## 目前研究快照

有日期的現況與完整地圖請見 [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md) 和 [`docs/INDEX.md`](docs/INDEX.md)。

- **連續性與記憶：** history replay、attention-structure 區辨、exact-structure longitudinal claim admission，以及 matched-information memory-locus dependency 測試。
- **人機協作：** CCTS 沿用有界問題及依當前目的判定的 grounding；未採納新的獨立適用性構念或適用性閘門。學習相關區分僅作研究設計提醒，不得以 CCTS 狀態作為學習測量閘門。
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

PUBLICATION != SCIENTIFIC_VALIDATION
公開典藏 != 科學驗證

IMPLEMENTATION != SCIENTIFIC_ESTABLISHMENT
已有實作 != 科學結論成立
```

典藏不代表同儕審查、科學驗證，也不代表目前草稿版本已發布。

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
