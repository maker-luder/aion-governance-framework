# AION Governance Framework｜AION 治理研究框架

> **繁體中文 | [English](README.md)**
>
> **60 秒研究地圖：** [`docs/RESEARCH_MAP.md`](docs/RESEARCH_MAP.md)  
> **5 分鐘導覽：** [`docs/START_HERE.md`](docs/START_HERE.md)  
> **嚴格現況：** [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md)

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
4. **Human–AI collaboration（人機協作）與證據准入** —— CCTS / grounding（共構思考場域／共同基礎）研究表面、provider-evidence admission（供應商證據准入），以及在 bounded L0 claim（有限範圍 L0 主張）准入前重新驗證 exact baseline / intervention 結構的 longitudinal claim-admission bridge（縱向主張准入橋接）。

近期研究節點：

- [歷史重播](docs/research/HISTORY_AS_REPLAY_ENVIRONMENT_DREAM_RSI_INTAKE_2026_09_18.md)區分紀錄、檢索與 replay environment。
- [注意力結構區辨重建](docs/research/ATTENTION_STRUCTURE_REPLAY_DISCRIMINANT_REBUILD_2026_09_18.md)檢查它是否比 re-entry / memory / CCTS 多出區辨價值。
- [縱向主張准入橋接](research-labs/coupled-cognition-quality-factory_v0.1.0/src/aion_coupled_quality/longitudinal_claim_bridge.py)會在 bounded L0 claim 准入前重新驗證 exact longitudinal baseline / intervention 結構，並把 claim、evidence、provenance 的內容定址身分綁在一起；但這仍是工程／結構准入控制，**不等於**主張為真，也不等於主體性支持。
- [記憶所在位置／依賴區辨 harness](research-labs/subjectivity-pipeline_v0.1.0/docs/MEMORY_LOCUS_DEPENDENCY_HARNESS.md)在 task / information content 匹配條件下，把 availability locus（資訊所在位置）、freshness（新鮮度）、provenance（來源綁定）與 retrieval dependency（檢索依賴）從既有 continuity-channel removal（連續性通道移除）中拆開。現在只建立 Stage B synthetic structural admissibility（合成結構可接受性）；functional dependency（功能依賴）與 identity continuity（身分連續性）仍未建立。
- [CCAP Stage 1–3 凍結](docs/research/CCAP_STAGE1_STAGE2_STAGE3_FREEZE_MANIFEST_2026_09_18.md)、[D1 × D4 TEVV 執行前設計](docs/research/CCAP_D1_D4_TEVV_PRE_EXECUTION_DESIGN_2026_09_18.md)與[Four-Domain × 六維壓力測試](docs/research/CCAP_FOUR_DOMAIN_SIX_DIMENSION_CORE_STRESS_TEST_2026_09_18.md)負責凍結、映射與結構壓力測試，不把結構完整性當成實證支持。
- [評估系統邊界](docs/research/CCAP_ASSESSMENT_SYSTEM_BOUNDARY_2026_09_18.md)、[區辨硬化](docs/research/EXTERNAL_CALIBRATION_DIMENSION_DISCRIMINANT_HARDENING_2026_09_18.md)、[D2 × D4 協議](docs/research/D2_D4_DIFFERENTIAL_PROTOCOL_CANDIDATE_2026_09_18.md)與[合成執行](docs/research/D2_D4_SYNTHETIC_DIFFERENTIAL_EXECUTION_2026_09_18.md)加入前瞻式差異測試；最新結果仍只在測試夾具層級成立。
- [OpenAI 12 軸證據重新准入](docs/research/OPENAI_12_AXIS_EVIDENCE_READMISSION_REVIEW_2026_09_18.md)是第一個完成的 provider-evidence admission 案例；開放獨立重現仍然稀少。

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

**目前工程狀態：** `main` 已包含具精確量測語意綁定的 bounded TEVV、Full-QMS、AI 對抗性安全設定檔與內容定址安全收據、用於來源拆分／區辨／synthetic D2 × D4 測試的有限範圍 CCAP harness、exact-structure longitudinal claim-admission bridge（精確結構縱向主張准入橋接），以及 matched-information memory-locus dependency harness（資訊匹配的記憶所在位置／依賴區辨框架）。這些是工程控制與測試夾具範圍的研究工具；**不代表**已建立安全有效性、功能性記憶依賴、身分連續性、D2／D4 支持、獨立科學驗證、主體性、意識或現象經驗。

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