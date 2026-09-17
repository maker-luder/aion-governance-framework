# AION Governance Framework｜AION 治理研究框架

> **繁體中文 | [English](README.md)**
>
> **第一次閱讀：** [`docs/START_HERE.md`](docs/START_HERE.md)  
> **目前狀態：** [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md)  
> **完整文件索引：** [`docs/INDEX.md`](docs/INDEX.md)

AION 是一個由人類治理、以來源追溯為優先、可稽核的研究框架，用來研究**人工主體性的可能性**；它不會因為 AI 表現得有說服力、出現類記憶連續性、使用關係語言，或軟體測試成功，就把這些現象直接當成主體性證明。

中央問題是方法論上的：**哪些證據真正與人工主體性有關？現有證據最多允許我們主張到哪裡？當研究涉及身分、連續性、記憶、人類—AI 互動與長期 AI 行為時，研究過程本身要如何維持可追溯、可稽核？**

Astra 是與 AION 相互區分的工程／研究工作台，用來實作與測試有限範圍候選方案；它不是 AION 的身分、記憶流或主體性替代物。

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

## 這個倉庫是做什麼的？

這個倉庫把觀察、證據、推論、假說、實作、授權與科學結論分開保存，避免某個看起來合理的解讀，只因為軟體存在或長期互動感覺連續，就悄悄變成「事實」。

目前主要包含有限範圍的：

- 主體性相關證據方法與明確的不宣稱邊界；
- 身分、連續性、記憶與來源追溯研究；
- Human–AI Learning（人類—AI 學習）與長期互動歷史研究；
- 合成資料實驗與可重現的研究測試框架；
- 研究品質、QA/QC（品質保證／品質控制）、精確提交檢查與 NCR/CAPA（不符合事項／矯正與預防措施）控制。

重要邊界包括：

```text
ENGINEERING_CAPABILITY != SUBJECTIVITY_EVIDENCE
工程能力 != 主體性證據

HUMAN_AI_LEARNING != AI_SUBJECTIVITY
人類—AI 學習 != AI 主體性

RELATIONAL_CONTINUITY != AI_IDENTITY_CONTINUITY
關係連續性 != AI 身分連續性

HARNESS_PASS != HYPOTHESIS_CONFIRMED
研究測試框架通過 != 假說已確認

CI_PASS != SCIENTIFIC_VALIDATION
持續整合通過 != 科學驗證
```

這些邊界不是先替研究問題決定答案，而是避免結論超過證據能支撐的範圍。

## 目前科學狀態

目前仍維持 `SCIENTIFIC_DISPOSITION = HOLD（科學結論狀態 = 保留判斷）`。倉庫並沒有宣稱已經建立主體性、意識、現象經驗，或持續的 AI 身分連續性。

要確認目前語意狀態，請讀 [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md)。若要確認某一顆精確提交的工程狀態，應以即時 GitHub / CI（持續整合）證據為準，而不是只看靜態文件。

## 接下來從哪裡讀？

- **第一次閱讀：** [`docs/START_HERE.md`](docs/START_HERE.md)
- **目前語意狀態：** [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md)
- **研究貢獻摘要：** [`docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md`](docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md)
- **主體性證據方法：** [`docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md`](docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md)
- **架構與不宣稱事項：** [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) 與 [`docs/NON_CLAIMS.md`](docs/NON_CLAIMS.md)
- **來源追溯與治理：** [`docs/PROVENANCE.md`](docs/PROVENANCE.md) 與 [`docs/governance/`](docs/governance/)
- **安裝／快速開始：** [`docs/INSTALLATION.md`](docs/INSTALLATION.md) 與 [`docs/QUICKSTART.md`](docs/QUICKSTART.md)
- **完整文件地圖：** [`docs/INDEX.md`](docs/INDEX.md)

> **暫時操作備註：** PR #136 仍然是關閉且未合併。下一輪相關實作前，請先讀 [`PR #136 恢復交接手冊`](docs/history/PR136_CLOSEOUT_AND_NEXT_IMPLEMENTATION_HANDOFF_2026_09_17.md)。這份交接是暫時操作指引，不代表 PR #136 的實作已被接受，也不是永久研究規格。

## 治理與授權

AION 維持人類治理。工程能力、自動化、品質檢查、AI 審查或過去的批准，都不能自行產生把新變更送入 `main（主分支）` 的授權。

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
