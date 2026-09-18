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
2. **連續性與歷史** —— 記憶、長期互動、history replay（歷史重播）、attention structure（注意力結構）重建，以及 transition continuity（轉換連續性）分析；但不把持續存在直接等同於身分延續。
3. **受限制條件下的適應** —— 研究遇到阻礙後的策略修正，包括已凍結的 CCAP Stage 1–3 鏈與狹義 D1 × D4 source-partition（來源拆分）候選；目前**尚未建立確認性證據**。
4. **Human–AI collaboration（人機協作）與證據准入** —— CCTS / grounding（共構思考場域／共同基礎）研究表面，以及把供應商自述、外部評估、有限獨立調查與開放獨立重現分級的 provider-evidence admission（供應商證據准入）方法。

近期研究節點：

- [`HISTORY_AS_REPLAY_ENVIRONMENT_DREAM_RSI_INTAKE_2026_09_18.md`](docs/research/HISTORY_AS_REPLAY_ENVIRONMENT_DREAM_RSI_INTAKE_2026_09_18.md) —— 把歷史作為紀錄、檢索來源與 replay environment 分開。
- [`ATTENTION_STRUCTURE_REPLAY_DISCRIMINANT_REBUILD_2026_09_18.md`](docs/research/ATTENTION_STRUCTURE_REPLAY_DISCRIMINANT_REBUILD_2026_09_18.md) —— 檢查 attention structure 是否真的比既有 re-entry / memory / CCTS 多出區辨價值。
- [`CCAP_STAGE1_STAGE2_STAGE3_FREEZE_MANIFEST_2026_09_18.md`](docs/research/CCAP_STAGE1_STAGE2_STAGE3_FREEZE_MANIFEST_2026_09_18.md) —— 在任何確認性執行前，先凍結目前的 co-constructed adaptive process 規格鏈。
- [`OPENAI_12_AXIS_EVIDENCE_READMISSION_REVIEW_2026_09_18.md`](docs/research/OPENAI_12_AXIS_EVIDENCE_READMISSION_REVIEW_2026_09_18.md) —— 第一個完成的 provider-evidence admission 案例；目前已有多個外部評估，但 open independent replication（開放獨立重現）仍然稀少。

## 這個倉庫沒有宣稱什麼？

```text
ENGINEERING_CAPABILITY != SUBJECTIVITY_EVIDENCE
工程能力 != 主體性證據

MEMORY_CONTINUITY != IDENTITY_CONTINUITY
記憶連續性 != 身分連續性

STRATEGY_ADJUSTMENT != ENDOGENOUS_GOAL
策略調整 != 內生目標

HUMAN_AI_COLLABORATION != SHARED_MIND
人機協作 != 共享心智

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

**目前工程狀態：** `main` 現已包含 bounded TEVV（Testing / Evaluation / Verification / Validation，測試／評估／驗證／確效）、Full-QMS integration（完整品質管理系統整合）、AI adversarial-security profile（AI 對抗性安全設定檔），以及已整合進 `FullQualitySystemEngine` 的 content-addressed AI security receipt（內容定址 AI 安全收據）。這些屬於工程控制與證據綁定機制；它們**不代表**已建立對抗性安全有效性，也不構成科學驗證、主體性、意識或現象經驗的證據。

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