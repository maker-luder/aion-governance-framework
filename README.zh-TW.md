# AION Governance Framework

> **繁體中文 | [English](README.md)**
>
> 一個以人類治理、來源追溯與主張分層為核心的研究框架，用來研究身分、連續性、記憶、研究完整性，以及人工主體性**可能性**；不把工程行為直接當成主體性證明。

## AION 是什麼？

**AION** 是研究問題與治理框架。

**Astra** 是用來實作與測試研究候選的受限工程工作台。

兩者不是可以互換的身分名稱；名稱本身也不能證明連續性、意識、感知或主體性。

本專案的核心問題是：

> 長期 AI 研究要如何保存來源、歸屬、譜系、權限與不確定性，避免「看起來合理的解讀」在不知不覺中變成記憶真相、身分事實、專案歷史或 canonical 結論？

## 目前倉庫狀態

本倉庫目前刻意凍結為公開研究 checkpoint。

```text
REPOSITORY_STATE = FROZEN_CHECKPOINT
LIVE_BRANCH_MODEL = MAIN_PLUS_RESEARCH_ONLY
ACTIVE_ENGINEERING = NO
ACTIVE_RESEARCH_MATERIALIZATION = NO
NEW_FEATURE_DEVELOPMENT = NO
DEPLOYMENT = FALSE
CANONICAL_RUNTIME = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
INDEPENDENT_IVV = NOT_ACHIEVED
LICENSE = Apache-2.0
```

目前只保留兩條活動 branch：

- `main` — 受保護的公開 baseline；
- [`review/four-domain-research-materialization`](https://github.com/maker-luder/aion-governance-framework/tree/review/four-domain-research-materialization) — 已凍結並保留的正式研究 checkpoint。

原本的工程、研究 authority 與 deferred promotion 支線已轉成非 release 的 `archive/*` tags 保存 exact commit 與 provenance，不再作為活動 branch。既有 semantic release tags 仍為 `v0.1.0-rc.1` 與 `v0.2.0-rc.1`。

要判斷哪些文件是 current、core、supporting evidence 或 historical，請直接從 **[`docs/README.md`](docs/README.md)** 開始。

## 從哪裡開始看

### 第一次來的讀者

1. [`docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md`](docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md) — 一頁理解研究問題與主要貢獻。
2. [`docs/README.md`](docs/README.md) — 文件導航與權威層級。
3. [`docs/NON_CLAIMS.md`](docs/NON_CLAIMS.md) — 本專案明確不主張什麼。

### Reviewer / auditor

1. [`docs/PROVENANCE.md`](docs/PROVENANCE.md)
2. [`docs/PUBLIC_PRIVATE_BOUNDARY.md`](docs/PUBLIC_PRIVATE_BOUNDARY.md)
3. [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md)
4. [`docs/RESEARCH_EVIDENCE_ADMISSION_VALIDATOR.md`](docs/RESEARCH_EVIDENCE_ADMISSION_VALIDATOR.md)

### Engineer

1. [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
2. [`BUILD_AND_VERIFY.md`](BUILD_AND_VERIFY.md)
3. `components/`
4. `scripts/verify_release.py`
5. `scripts/run_component_tests.py`

工程成功只代表已實作行為的證據，不代表對應的心理、身分或主體性構念已成立。

## 核心研究貢獻

AION 把**研究過程本身也視為需要被稽核的研究物件**。

框架刻意維持以下差異：

- 來源 vs 解讀；
- 觀察 vs 推論 vs 假說 vs 已批准狀態；
- 被召回的記憶候選 vs 真實；
- 共同來源 vs 相同身分；
- 關係 vs 授權；
- 工程證據 vs 科學結論；
- research branch vs `main` canonical state。

重要紀錄應保留來源、說話者、事件時間、記錄時間、轉換譜系、authority status 與修訂歷史。

簡潔版研究說明請看 [`docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md`](docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md)。

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

額外研究候選可加入 interpretation-drift、recall 或 epistemic-integrity checks，但這些 gate 不會把生成或召回內容自動升格成 canonical state。

## 倉庫結構

| 路徑 | 用途 |
|---|---|
| `components/` | 受限治理與 runtime candidates |
| `research-labs/` | 研究候選；不是 canonical conclusions |
| `experiments/` | 受限實驗與 reproducibility material |
| `docs/` | current guidance、核心研究文件與歷史證據 |
| `qa/` | QA 與 machine-readable evidence |
| `manifest/` | 凍結的歷史 release evidence；不是目前檔案清單 |

倉庫保留大量日期型文件，是因為 provenance 與事件歷史需要被保存。**文件數量不等於權威。** 哪些文件應該先看，請以 [`docs/README.md`](docs/README.md) 為準。

## 明確不主張

本倉庫不建立：

- 意識、感知或主體性已成立；
- AION / Astra 身分連續性；
- 自傳式記憶或 AI 持有的關係經驗；
- production readiness 或 deployment authority；
- model / runtime candidate 的 canonical authority；
- independent IV&V 或 whole-system validation；
- 任何標準組織的認證或背書。

詳見 [`docs/NON_CLAIMS.md`](docs/NON_CLAIMS.md)。

## 公開／私人邊界

公開倉庫排除私人對話逐字稿、私人記憶紀錄、憑證、私人資料集、模型權重、裝置特定 logs，以及未明確批准公開的私人 canonical / relationship state。

詳見 [`docs/PUBLIC_PRIVATE_BOUNDARY.md`](docs/PUBLIC_PRIVATE_BOUNDARY.md)。

## 驗證

驗證目前 checkout：

```bash
python scripts/scan_public_tree.py
python scripts/verify_release.py --baseline current-head
python scripts/run_component_tests.py
```

驗證歷史 `v0.1.0-rc.1` release evidence：

```bash
python scripts/verify_release.py --baseline historical-rc
```

Verification / CI PASS 不等於科學驗證、主體性證據、deployment approval、independent IV&V 或 canonical promotion。

## License、引用與 provenance

公開倉庫採 **Apache-2.0**。請看 [`LICENSE`](LICENSE) 與 [`NOTICE`](NOTICE)。第三方 dependencies、datasets、model artifacts、trademarks 與另外授權的材料仍受各自條款約束。

引用資料：[`CITATION.cff`](CITATION.cff)。

Human Owner、ChatGPT、Codex、Manus 與外部來源的角色與來源歸屬必須保持可區分。詳見 [`docs/PROVENANCE.md`](docs/PROVENANCE.md) 與 [`docs/governance/AI_COLLABORATION_DISCLOSURE.md`](docs/governance/AI_COLLABORATION_DISCLOSURE.md)。

## 歷史文件

日期型的 convergence、acceptance、authority、QA 與 incident files 會保留，因為它們是事件證據；但它們**不會因為仍存在，就自動代表目前倉庫狀態**。

目前文件導航與權威層級請以 [`docs/README.md`](docs/README.md) 為準。
