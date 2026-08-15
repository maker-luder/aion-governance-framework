# AION Four-Domain Research Workbench

> **繁體中文 | [English](README.md)**
>
> **保留的公開研究 checkpoint——不是 `main` 發行分支，也不是 canonical state。**

```text
BRANCH = review/four-domain-research-materialization
RESEARCH_STATE = FROZEN_CHECKPOINT
ACTIVE_RESEARCH_MATERIALIZATION = NO
NEW_RESEARCH = NO
NEW_FEATURES = NO
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
INDEPENDENT_IVV = NOT_ACHIEVED
```

這個 branch 保留 AION/Astra 的研究工作台，用來研究人工主體性的**可能性**，而不預設主體性、意識、身分連續性或道德地位已被建立。

研究 lineage 已於 2026-08-15 完成收斂。Branch history 現在包含 Four-Domain materialization lineage、research-consolidation / literature-grounding snapshot、CSOMI、terminal SLSH reconciliation，以及 CSOMI × SLSH read-only integration。收斂保留 Git ancestry，沒有改寫或 squash 研究歷史。

目前 branch standing 的唯一 current 入口請讀 [`RESEARCH_BRANCH_STATUS.md`](RESEARCH_BRANCH_STATUS.md)。

## 目前應閱讀的入口

- **Branch standing：** [`RESEARCH_BRANCH_STATUS.md`](RESEARCH_BRANCH_STATUS.md)
- **Whitepaper × web standing reconciliation：** [`WHITEPAPER_WEB_BRANCH_RECONCILIATION_2026-08-12.md`](research-workbench/four-domain-materialization/2026-08-12/WHITEPAPER_WEB_BRANCH_RECONCILIATION_2026-08-12.md)
- **Four-Domain repository crosswalk：** [`FOUR_DOMAIN_REPOSITORY_CROSSWALK.md`](research-workbench/four-domain-materialization/2026-08-09/FOUR_DOMAIN_REPOSITORY_CROSSWALK.md)
- **Research-consolidation historical snapshot：** [`docs/research-consolidation/`](docs/research-consolidation/)
- **CSOMI research package：** [`research-labs/cross-substrate-other-minds-inference_v0.1.0/`](research-labs/cross-substrate-other-minds-inference_v0.1.0/)
- **SLSH research package：** [`research-labs/subjective-load-sensitivity-hypothesis_v0.1.0/`](research-labs/subjective-load-sensitivity-hypothesis_v0.1.0/)
- **CSOMI × SLSH read-only integration：** [`research-labs/csomi-slsh-integration_v0.1.0/`](research-labs/csomi-slsh-integration_v0.1.0/)

## 歷史 snapshot 規則

`research-workbench/`、`docs/research-consolidation/` 與較早 QA/handoff 文件中的 dated records 都保留為 historical research evidence。部分文件記錄事件當時正確的 branch 名稱、exact head、test count 或 workflow state。

2026-08-15 lineage closure 後，不會為了讓歷史看起來像現在而暗中改寫那些紀錄。新的 branch-standing record 可以在 current navigation 範圍內 supersede 舊狀態，但不會抹除舊紀錄的 provenance。

```text
HISTORICAL_RECORD = PRESERVED_NOT_CURRENT
CANDIDATE != AUTOMATIC_SUPERSESSION
TRANSFORMABILITY != IDENTITY_CONTINUITY
CI_SUCCESS != SCIENTIFIC_VALIDATION
TEST_PASS != THEORY_CONFIRMATION
```

## Main 邊界

這個 branch 的任何內容都不會因為 research convergence 而自動進入 `main`、canonical state、runtime authority 或 deployment。

```text
RESEARCH_BRANCH != MAIN
RESEARCH_RESULT != CANONICAL_CONCLUSION
RESEARCH_CONVERGENCE != CANONICAL_PROMOTION
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

公開/default `main` 仍是受保護的公共 baseline。沒有被明確採納的 promotion candidates，會保持為 historical/deferred candidates，不會因為 branch cleanup 就變成研究結論。

## 重新啟動規則

本 branch 現在是 frozen checkpoint。未來若要重新開始研究、experiment、runtime work 或 canonical promotion，必須另外建立一個明確授權的新週期；不能從舊的 `ACTIVE` 或 autonomous-growth 狀態欄位自動續跑。
