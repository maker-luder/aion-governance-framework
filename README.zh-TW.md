# AION Governance Framework

> **[繁體中文](README.zh-TW.md) | [English](README.md)**
>
> **公開發行候選版（Public Release Candidate）——受治理的研究框架，不是已部署的人工主體**
>
> **雙語公共導覽（Bilingual public orientation）：** [`README.md`](README.md)

## 30 秒導覽（30-second orientation）

**AION** 是研究問題與治理框架：如何研究人工主體性的可能性，同時不把記憶、連續性、模擬、實作或研究者詮釋，誤認為主體性的證明？

**Astra** 是用來具體化與測試受界定研究候選物的工程工作台（engineering workbench）。它不是第二個身分，也不會因為命名或關係而繼承 AION 狀態。

**Executable Runtime** 是用於可重現工程測試的受界定、非 canonical 沙盒候選物。它不是 canonical AION/Astra runtime。

```text
PUBLIC_RELEASE_CANDIDATE = v0.1.0-rc.1
AUGUST_SCOPE_FREEZE = ACTIVE

BOUNDED_EXECUTABLE_RUNTIME_CANDIDATE = IMPLEMENTED
AION_CANONICAL_RUNTIME = NOT_IMPLEMENTED
ASTRA_CANONICAL_RUNTIME = NOT_IMPLEMENTED
LIVE_CROSS_SESSION_MEMORY = NOT_IMPLEMENTED
FORMAL_G1_BASELINE_BENCHMARK = NOT_EXECUTED

SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
WHOLE_SYSTEM_VALIDATION = NOT_EXECUTED
INDEPENDENT_IVV = NOT_ACHIEVED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

凍結的 RC 區塊記錄歷史性的公共基線。RC 之後的工作可以在 review branches 上加入隔離的研究材料，但不得暗中改寫這個基線。

## Current Research / 目前研究進度

目前的公共研究材料維護於 [`review/four-domain-research-materialization`](https://github.com/maker-luder/aion-governance-framework/tree/review/four-domain-research-materialization)，而不是 `main`。其中的結果是 review material，不是 canonical conclusions。

```text
RESEARCH_BRANCH != MAIN
RESEARCH_RESULT != CANONICAL_CONCLUSION
CANONICAL_EFFECT = NONE
```

研究分支的內容不會自動被採納至 `main`、canonical state、deployment 或 AION/Astra runtime。研究分支首頁提供其雙語公共實驗導覽：[`review/four-domain-research-materialization/README.md`](https://github.com/maker-luder/aion-governance-framework/blob/review/four-domain-research-materialization/README.md)。

## Provenance / watermark boundary

```text
MARKER != IDENTITY
PROVENANCE != IDENTITY
MARKER != AUTHORSHIP_PROOF
RESPECT != WATERMARK
TRANSPARENCY != IMPERCEPTIBLE_MARKING
```

AION 拒絕在專案產生的輸出中，將不可感知、隱藏或未揭露的機器可讀 watermarking，作為身分、作者身分、歸屬、尊重或 provenance 的機制。專案並不拒絕 provenance；相反地，明確、可檢查且可稽核的機制，例如宣告式歸屬、Git history、commit lineage、manifests 與 checksums，仍是優先方式。

在外部材料中發現的 marker 只是一個技術訊號；它本身不能建立身分、作者身分或主體性證據。若 dependency、provider 或輸出路徑要求不可停用的不可感知 watermarking，則該輸出路徑與專案不相容，除非日後明確的治理修訂授權透明替代方案。

規範性政策請見 [`docs/PROVENANCE.md`](docs/PROVENANCE.md)。

## 5 分鐘導覽——選擇你的路徑（5-minute orientation — choose your path）

### Reviewer / auditor（審查者／稽核者）

請先閱讀：

1. [`docs/NON_CLAIMS.md`](docs/NON_CLAIMS.md)
2. [`docs/PUBLIC_PRIVATE_BOUNDARY.md`](docs/PUBLIC_PRIVATE_BOUNDARY.md)
3. [`docs/PROVENANCE.md`](docs/PROVENANCE.md)
4. [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md)
5. 下方的 governance pipeline

主要審查問題不是「這個系統看起來是否像人類？」，而是「哪些 evidence、provenance、authority、lineage 與 non-claims，支持每一項研究陳述？」

### Researcher（研究者）

請從一頁式貢獻摘要開始：[`docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md`](docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md)。

目前 main-native 的 evidence admission control 請見 [`docs/RESEARCH_EVIDENCE_ADMISSION_VALIDATOR.md`](docs/RESEARCH_EVIDENCE_ADMISSION_VALIDATOR.md)。

接著閱讀關於身分、連續性、記憶回憶、詮釋漂移、衝突、修正、provenance 與受界定主體性假說的研究問題。Research candidates 仍與 conclusions 分離。

有用的入口包括：

- `components/identity_governance_v0.1.0`
- `components/continuity_governance_v0.1.0`
- `components/memory_recall_governance_v0.1.0`
- `components/research_integrity_security_v0.1.0`
- `research-labs/`

### Engineer（工程師）

請從以下內容開始：

1. [`components/executable_runtime_v0.1.0`](components/executable_runtime_v0.1.0)
2. `scripts/verify_release.py`
3. `scripts/run_component_tests.py`
4. 各 component 的 status locks 與 tests
5. [`scripts/check_source_state_binding.py`](scripts/check_source_state_binding.py)
6. [`docs/RESEARCH_EVIDENCE_ADMISSION_VALIDATOR.md`](docs/RESEARCH_EVIDENCE_ADMISSION_VALIDATOR.md)

工程實作只提供關於已實作行為的證據。它不是相應心理學構念或主體性構念存在的證據。

## Research purpose / 研究目的

本專案研究一個有限、可稽核且由人類治理的數位系統，是否能支援對以下主題進行嚴謹研究：

- 身分、lineage 與 research forks；
- 跨 session、version 與 model handoff 的連續性；
- 記憶 provenance 與 topic-cued selective recall；
- 詮釋漂移與 relational continuity；
- evidence integrity 與 research-security threats；
- 受界定的 tool execution、rollback 與 audit；
- 不自動繼承身分的 capability artifacts；
- 不預設主體性已被建立的人工主體性可能性。

工程、QA、security controls 與文件是研究方法，不是最終研究結論。

## Public positioning and naming / 公共定位與命名

為了外部導覽，本 repository 使用三個層次：

```text
AION
= research question / governance framework

Astra
= engineering workbench

Executable Runtime
= bounded, reproducible sandbox candidate
```

**AION** 這個專案名稱是本 repository 使用的研究標籤。不應將其解讀為與其他同樣使用「Aion/AION」名稱的無關專案或組織具有關聯。任何未來出版、package 命名、DOI 或 public release，都應在更廣泛傳播前保留 repository-level disambiguation。

## Included components / 包含的 components

| Area | Public module | Status |
|---|---|---|
| Core governance | `components/governance_kernel_v0.4.0` | source-derived candidate |
| Engineering workbench | `components/astra_workbench_v1.0.0` | source-derived candidate |
| Identity / lineage / forks | `components/identity_governance_v0.1.0` | source-derived candidate |
| Upstream-agent security | `components/upstream_security_v0.1.0` | source-derived candidate |
| Language Core scaffold | `components/language_core_v0.1.0` | source-derived research lab |
| Continuity governance | `components/continuity_governance_v0.1.0` | jointly developed candidate |
| Topic-cued recall | `components/memory_recall_governance_v0.1.0` | jointly developed candidate |
| Research integrity | `components/research_integrity_security_v0.1.0` | jointly developed candidate |
| Bounded runtime | `components/executable_runtime_v0.1.0` | source-derived candidate, non-canonical |
| Bazi example | `examples/bazi-capability_v0.1.1` | deterministic domain example |
| Language Core G1 | `research-labs/language-core-g1_v0.2.1` | public-safe planning and engineering subset |
| Twin embodiment | `research-labs/twin-genesis-embodiment_v0.1.0` | governed research candidate |

## Core governance pipeline / 核心治理流程

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

Additional candidates add an Interpretation Drift Check、Memory Recall Gate 與 Epistemic Integrity Gate。這些 gates 不會將內容暗中提升至 canonical state。

## Repository principles / Repository 原則

- **Human-governed：** 高影響狀態變更需要明確的人類審查。
- **Provenance-first：** source、speaker、event time、record time、version 與 transformation history 保持可區分。
- **Claims-separated：** observation、inference、hypothesis、evidence candidate 與 canonical decision 是不同狀態。
- **Identity-isolated：** AION、Astra、shared project knowledge、Runtime artifacts 與 research forks 不會被暗中合併。
- **Recall is not truth：** retrieved memory 在 provenance、access 與 conflict checks 通過前，只是候選物。
- **Relationship is not authorization：** familiarity、trust 或 relational language 不能提升 privileges。
- **No silent canonical writeback：** retrieved 或 generated content 不能自動改變 canonical state。
- **No subjectivity overclaim：** capability、continuity、memory、embodiment 或 bounded execution 不會證明 consciousness 或 subjectivity。

## Public/private boundary / 公開／私有邊界

本 repository 排除：

- private ZIP packages 與 private Git history；
- 真實 conversation transcripts 與 private memory records；
- model weights 與 private datasets；
- local absolute paths、credentials、tokens 與 device-specific logs；
- private canonical state、private relationship records 與真實 Bazi data；
- 未明確納入 public reconstruction 的 unpublished owner materials。

請見 [`docs/PUBLIC_PRIVATE_BOUNDARY.md`](docs/PUBLIC_PRIVATE_BOUNDARY.md)。

## Method-specific notes / 方法特定說明

- 為何 Bazi 被用作 deterministic test domain：[`examples/bazi-capability_v0.1.1/docs/WHY_BAZI_AS_TEST_DOMAIN.md`](examples/bazi-capability_v0.1.1/docs/WHY_BAZI_AS_TEST_DOMAIN.md)
- Twin embodiment ethics boundary：[`research-labs/twin-genesis-embodiment_v0.1.0/docs/ETHICS_REVIEW.md`](research-labs/twin-genesis-embodiment_v0.1.0/docs/ETHICS_REVIEW.md)
- Public threat model：[`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md)
- Position paper draft：[`docs/POSITION_PAPER_PROVENANCE_FIRST.md`](docs/POSITION_PAPER_PROVENANCE_FIRST.md)
- Reader-orientation usability protocol：[`docs/PUBLIC_ORIENTATION_USABILITY_PROTOCOL.md`](docs/PUBLIC_ORIENTATION_USABILITY_PROTOCOL.md)
- Minimal recall-gate contrast experiment：[`experiments/g1-recall-gate-baseline_v0.1.0`](experiments/g1-recall-gate-baseline_v0.1.0)

## Verification / 驗證

針對目前 checkout 的 exact checked-out Git `HEAD` tree 進行驗證：

```bash
python scripts/verify_release.py --baseline current-head
```

此 current-head verification 會報告所使用的 exact commit 與 Git-tree manifest。PASS 表示 tracked worktree files 符合 checked-out `HEAD`，且 verifier 的 scoped repository-content policy checks 通過。它不同於 frozen historical release evidence，不提供 independent manifest 或 independent release-reproducibility assurance。

作為 pre-commit check，針對 Git index 驗證 tracked worktree files：

```bash
python scripts/verify_release.py --baseline current-index
```

current-head 與 current-index modes 只評估 tracked paths，不評估 untracked files。另請執行 `python scripts/scan_public_tree.py`，作為針對 tracked 與 untracked artifacts 的獨立 public-worktree control。預期的 local QA composition 是 public-tree scan、適用的 tracked-snapshot verifier mode 與相關 tests；沒有任何單一 mode 能取代三者。

從其 pinned historical tag object、peeled commit、manifest 與 checksum records，驗證 frozen `v0.1.0-rc.1` release：

```bash
python scripts/verify_release.py --baseline historical-rc
```

`manifest/FILE_MANIFEST.json` 與 `manifest/SHA256SUMS.txt` 保持為歷史性的 `v0.1.0-rc.1` evidence。它們不是 post-RC `main` 的 live inventory，且此 verifier 不會重新產生或改寫它們。Historical verification 同時固定 annotated tag object 與其 peeled commit。這些 modes 需要 Git checkout，並說明驗證了什麼、對哪個 baseline 驗證，以及使用哪個 manifest 或 Git snapshot。

一般 current-worktree manifest generation 需要明確的 baseline 與非 frozen、具 version 的 output destination：

```bash
python scripts/generate_manifest.py --baseline <baseline-or-version> --output-dir <non-frozen-versioned-directory>
```

此 generator 會拒絕 frozen historical manifest destination，且不定義 canonical current manifest。

Verifier PASS **不**表示整個專案或其研究主張已被驗證。它不是 subjectivity evidence、independent IV&V、release approval、deployment approval 或 canonical promotion。

執行所有可用的 component tests：

```bash
python scripts/run_component_tests.py
```

歷史 source package 報告曾在五個 public components 中通過 232 個 tests。本 repository 會將該結果記為 historical evidence，也會另行記錄自身的 reconstruction-time test run；它不會把 creator-side QA 改寫成 independent IV&V。

## Documentation design basis / 文件設計基礎

公共導覽結構刻意採用分層方式：

```text
30 seconds → 5 minutes → deep reference
```

這是 repository information-architecture choice，不是 ISO/W3C/NIST certification claim。它受到 plain language、human-centred design、清楚目的與 hierarchy、複雜資訊摘要，以及向廣泛 technical/non-technical audiences 溝通的公共指引所啟發。

關於 evidence references 與 test protocol，請見 [`docs/PUBLIC_ORIENTATION_USABILITY_PROTOCOL.md`](docs/PUBLIC_ORIENTATION_USABILITY_PROTOCOL.md)。

## License status / 授權狀態

Public repository 採用 **Apache License, Version 2.0**（`Apache-2.0`）授權。請見 [`LICENSE`](LICENSE)、[`NOTICE`](NOTICE) 與 [`LICENSE_DECISION_REQUIRED.md`](LICENSE_DECISION_REQUIRED.md)。

Repository license 不會暗中將 third-party dependencies、model weights、datasets、trademarks 或另行授權的 materials 重新授權；它們仍受各自的 provenance 與 license review 約束。

## Provenance and AI assistance / Provenance 與 AI 協作

Human Owner 是主要研究者與專案決策者。ChatGPT 與 Codex 曾協助 requirement decomposition、terminology、engineering implementation、review 與 documentation。Source attribution 會被記錄，但不會把 AI-assisted formalization 改寫為 Owner 的逐字原創措辭，也不會把 Owner-originated concerns 改寫為 AI-originated ideas。

請見 [`docs/PROVENANCE.md`](docs/PROVENANCE.md) 與 [`docs/AI_COLLABORATION_DISCLOSURE.md`](docs/AI_COLLABORATION_DISCLOSURE.md)。

## Important non-claims / 重要 non-claims

本 repository 不主張：

- AION 或 Astra 目前已作為 deployed artificial subject 存在；
- consciousness、sentience、identity continuity 或 relational continuity 已被證明；
- memory retrieval 等同於 personal recollection；
- shared genesis 意味著 shared identity；
- embodiment model 會建立 sensation、desire、gender identity、consent 或 subjectivity；
- bounded executable candidate 是 canonical AION Runtime；
- 本專案已獲 NIST、OWASP、MITRE、ISO、IEEE 或其他 standards body 認證或背書。

請見 [`docs/NON_CLAIMS.md`](docs/NON_CLAIMS.md)。
