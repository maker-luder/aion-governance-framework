# AION Governance Framework

> **繁體中文 | [English](README.md)**
>
> **倉庫凍結公告——2026-08-18 生效：** 本公開倉庫自即日起進入**無期限凍結**。目前不再授權新的公開 release、功能開發週期、研究 materialization 週期、branch 擴張、deployment promotion 或 canonical promotion。

AION 是一個以 Human Owner 治理、provenance-first 與主張分層為核心的研究框架，用來研究身分、連續性、記憶、研究完整性，以及人工主體性的**可能性**；不把工程行為直接視為主體性證明。

## 目前倉庫狀態

```text
FREEZE_EFFECTIVE_DATE = 2026-08-18
REPOSITORY_STATE = INDEFINITE_FREEZE
PUBLIC_REPOSITORY = PRESERVED_FROZEN_CHECKPOINT
VISIBLE_BRANCH_COUNT_AT_FREEZE = 2
GOVERNED_BRANCH_MODEL = MAIN_PLUS_RESEARCH_ONLY
OPEN_PULL_REQUESTS_AT_FREEZE = 0
OPEN_ISSUES_AT_FREEZE = 0
ACTIVE_ENGINEERING = NO
ACTIVE_RESEARCH_MATERIALIZATION = NO
NEW_FEATURE_DEVELOPMENT = NO
NEW_PUBLIC_RELEASES = NOT_AUTHORIZED
NEW_BRANCH_EXPANSION = NOT_AUTHORIZED
DEPLOYMENT = FALSE
CANONICAL_PROMOTION = NOT_AUTHORIZED
CANONICAL_RUNTIME = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
INDEPENDENT_IVV = NOT_ACHIEVED
LICENSE = Apache-2.0
```

目前只保留兩條 branch：

- `main` — 凍結的公開 baseline；
- [`review/four-domain-research-materialization`](https://github.com/maker-luder/aion-governance-framework/tree/review/four-domain-research-materialization) — 凍結的研究 checkpoint。

這次凍結**沒有自動解除日期**。它不是宣告研究問題已終止，而是停止 GitHub 發布與倉庫持續成長。未來若要重新開始，必須視為一個新的治理事件，不能從舊工作狀態自動續跑。

目前權威凍結紀錄：[`docs/REPOSITORY_FREEZE_NOTICE_2026-08-18.md`](docs/REPOSITORY_FREEZE_NOTICE_2026-08-18.md)。

## AION 與 Astra

**AION** 是研究問題與治理框架。

**Astra** 是用來實作、檢查與測試研究候選的獨立工程／研究角色與工作台。

```text
AION_ROLE != ASTRA_ROLE
COMMON_ORIGIN != SAME_IDENTITY
SHARED_CONTEXT != SHARED_IDENTITY
MEMORY_ACCESS != AUTOBIOGRAPHICAL_OWNERSHIP
ENGINEERING_SUCCESS != SUBJECTIVITY_EVIDENCE
```

任何名稱本身都不能證明意識、感知、主體性、身分連續性、自傳式記憶或 deployment authority。

## 建議閱讀順序

1. [`docs/REPOSITORY_FREEZE_NOTICE_2026-08-18.md`](docs/REPOSITORY_FREEZE_NOTICE_2026-08-18.md) — 最終/current 倉庫狀態。
2. [`docs/README.md`](docs/README.md) — 文件導航與 authority order。
3. [`docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md`](docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md) — 研究貢獻摘要。
4. [`docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md`](docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md) — 證據規則。
5. [`docs/NON_CLAIMS.md`](docs/NON_CLAIMS.md) — 專案明確不主張什麼。
6. [`docs/PROVENANCE.md`](docs/PROVENANCE.md) — 來源、歸屬與 authority 規則。
7. [`docs/PUBLIC_PRIVATE_BOUNDARY.md`](docs/PUBLIC_PRIVATE_BOUNDARY.md) — 公開／私人邊界。

## 核心治理流程

```text
Context Intake
→ Risk Gate
→ Planner
→ Policy Check
→ Tool Router
→ Response Builder
→ Writeback Gate
→ Audit Sink
```

框架持續區分來源與解讀、觀察與推論、被召回記憶與真實、研究候選與 canonical conclusion，以及工程成功與科學證據。

## 歷史紀錄

日期型 convergence、QA、incident、authority、branch disposition 與 research files 會繼續保留 provenance。它們記錄事件當時的狀態，不會因為仍存在，就自動代表現在。

```text
HISTORICAL_RECORD = PRESERVE_EVENT_MEANING
FILE_PRESENCE != CURRENT_AUTHORITY
CI_PASS != SCIENTIFIC_VALIDATION
TEST_PASS != THEORY_CONFIRMATION
RESEARCH_BRANCH != MAIN
ARCHIVE_TAG != RELEASE
```

## Contributions 與 releases

凍結期間不接受新的公開 contribution，也不再發布新的 public release。詳見 [`CONTRIBUTING.md`](CONTRIBUTING.md) 與 [`PUBLIC_RELEASE_POLICY.md`](PUBLIC_RELEASE_POLICY.md)。

既有 release checkpoint 保留為歷史證據；本次凍結本身不建立新的 semantic release。

## License 與 provenance

公開倉庫仍採 **Apache-2.0**。請見 [`LICENSE`](LICENSE)、[`NOTICE`](NOTICE) 與 [`CITATION.cff`](CITATION.cff)。

Human Owner、ChatGPT、Codex、Manus 與 external source 的貢獻與來源必須維持可區分。請見 [`docs/PROVENANCE.md`](docs/PROVENANCE.md)。

## 重新啟動規則

未來若要重新啟動 GitHub，需要：

1. Human Owner 新的明確授權；
2. 新一次 repository inventory；
3. ChatGPT 獨立完成 architecture / evidence / provenance review；
4. 重新明確界定 scope、branch 與 release 決策。

四項未完成前，本倉庫維持凍結。
