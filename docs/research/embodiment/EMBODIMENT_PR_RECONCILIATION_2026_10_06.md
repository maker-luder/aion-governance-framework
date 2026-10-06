# 具身 PR 歷史對帳與 live lane 收斂判定 — 2026-10-06

```text
STATUS = RECOVERED_RECONCILIATION_CANDIDATE
SCOPE = DOCUMENTATION_AND_PROVENANCE_ONLY
TARGET_LANE = research/embodiment-lane
RECOVERED_FROM_PR = #278
RECOVERED_FROM_EXACT_HEAD = 0e498c963859b8e5ca56a1de918aa3542c55eb08
RECOVERY_BASE_HEAD = 029a02359dc2c460da5e9daeda7a6c66861f3f8d
ORIGINAL_AUDIT_TARGET_HEAD = f06eccb510dfcc0360eb887efb493729dea71775
MAIN_OBSERVED_HEAD = 7418ddf3bb043ea77749235cf1e65c60c33843bc
CANONICAL_EFFECT = NONE
MERGE_TO_MAIN = NO
CODE_BEHAVIOR_CHANGE = NO
DEPLOYMENT = FALSE
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
```

## 0. Recovery provenance

本文件由已關閉、未合併的 PR #278 exact head `0e498c963859b8e5ca56a1de918aa3542c55eb08` 有界重建到 `research/embodiment-lane@029a02359dc2c460da5e9daeda7a6c66861f3f8d` 的新 topic branch。

`#278` 內的 exact SHA、ahead/behind 數值與「目前」字樣，若位於原始對帳段落，描述的是 #278 建立時的 snapshot，而不是 recovery 後的 live repository。新的現況主張必須重新讀 GitHub live state。

```text
RECOVERY != RETROACTIVE_MERGE_OF_PR_278
HISTORICAL_SNAPSHOT != CURRENT_LIVE_STATE
RECOVERED_DOCUMENTATION != IMPLEMENTATION_PROMOTION
```
## 1. 目的

這份文件不重開舊 PR、不把舊 PR 自動合併，也不把任何候選提升成 canonical construct。它只處理一個問題：把具身研究的歷史 PR、目前 `research/embodiment-lane` live state、來源歸屬與可重用邊界重新對帳，避免把「曾經的 PR 快照」誤當成「現在的 repository 狀態」。

```text
HISTORICAL_PR_SNAPSHOT != LIVE_BRANCH_STATE
CLOSED_PR != DELETED_RESEARCH_HISTORY
IMPLEMENTATION_REUSE != EVIDENCE_REUSE
SOURCE_REUSE != CLAIM_SUPPORT_REUSE
```

## 2. 證據層級

1. `REPOSITORY_STATE`：GitHub live ref、PR state、exact SHA、compare、CI／checks，用於判定「現在」。
2. `HISTORICAL_RECORD`：closed PR 的 base/head exact SHA 與 diff，用於判定「當時做了什麼」。
3. `HUMAN_ORIGIN / AI_FORMALIZATION / JOINT_SYNTHESIS`：用於判定研究目的與形式化歸屬；不得由 repository scope flag 反向虛構人類研究者意圖。
4. `EXTERNAL_SOURCE`：只支持其實際涵蓋的解剖、生理、量測、建模或 provenance 主張；不得外推成 actor 主體性或生物實現。

## 3. 2026-10-06 原始 live-state snapshot（PR #278）

在本輪開始時：

```text
main = 7418ddf3bb043ea77749235cf1e65c60c33843bc
research/embodiment-lane = f06eccb510dfcc0360eb887efb493729dea71775

compare(main...embodiment-lane):
STATUS = diverged
AHEAD_BY = 23
BEHIND_BY = 14
MERGE_BASE = 6a34d7780dd6d5bc717cd6c82ba39e7a6241c2fd
```

因此在 PR #278 原始對帳時，具身 lane 不是可直接對 `main` 做累積 PR 的乾淨 topic branch。後續任何 promotion 必須逐項重建／挑選，而不是把 23 個 lane-only commits 一次包進 `main`。

## 4. PR 歷史分層

### 4.1 已合併的基礎歷史

| PR | 判定 | 處置 |
| --- | --- | --- |
| #210 `research: define scientific embodiment master blueprint and toolchain` | `MERGED` | 保留為 main 歷史；不能因此把後續 closed candidate 視為已採納 |

### 4.2 早期 closed / not-merged 候選

下列 PR 是歷史研究候選，不因 PR 曾經存在或測試曾通過就自動成為 current lane 或 main 的有效實作：

```text
#190 #191 #192 #193
#202 #203
#220
#236 #237
#239 #240 #241 #242 #243 #244
#246 #247 #248 #249
#250 #251 #252 #253 #254 #255 #256 #257 #258 #259 #260
#261 #262 #263
```

預設分類：

```text
HISTORICAL_CLOSED_PR
REUSE_REQUIRES = EXACT_HEAD_DEDUP + CLAIM_SCOPE_REVIEW + DEPENDENCY_REVIEW + TEST_REBUILD
```

`#261`、`#262`、`#263` 另依目前 lane README 保持 `HISTORICAL_SOURCE_POINTER / NOT_REBUILT`。它們的舊 branch ref 不應假定仍存在；是否存在必須讀 GitHub live state。

### 4.3 #267–#273：同一 durable lane 的連續快照

`#267`–`#273` 都以 `research/embodiment-lane` 作為 head branch，對 `main` 建立後再關閉。它們不是七條互相獨立的現行 branch；它們是同一 lane 在不同時間點的 PR 快照。

| PR | exact head | 與目前 `f06eccb5...` 的關係 | 現在判定 |
| --- | --- | --- | --- |
| #267 | `2f0f1779f2ee5b9b9e2e4708305e66abf94eb59d` | current lane ahead 21 / behind 0 | `ANCESTOR_OF_CURRENT_LANE` |
| #268 | `85eb7a544cb3ee5e455ac87b6ba32a850e2d6948` | ahead 20 / behind 0 | `ANCESTOR_OF_CURRENT_LANE` |
| #269 | `e0a908321bce02892b3843c62c0d2a9ee572c6f6` | ahead 19 / behind 0 | `ANCESTOR_OF_CURRENT_LANE` |
| #270 | `28fff27614657c71ee6366e5b84bdacaa28da82f` | ahead 7 / behind 0 | `ANCESTOR_OF_CURRENT_LANE` |
| #271 | `213343ba41bc79628ccff04640035176c173be1b` | ahead 6 / behind 0 | `ANCESTOR_OF_CURRENT_LANE` |
| #272 | `d063cec547963101ac578eaf325ff6e8c95b772d` | ahead 5 / behind 0 | `ANCESTOR_OF_CURRENT_LANE` |
| #273 | `8ff64f400f742039835ecbef3606aed08ed94759` | ahead 4 / behind 0 | `ANCESTOR_OF_CURRENT_LANE` |

`#273` 之後到目前 head 還有四個 commits：研究自主政策與可見研究歸屬的匿名化／隱私修正。這些變更屬 current lane history，不應錯綁回 #273 的原始 PR head。

### 4.4 #274 與後續 main 治理

- `#274` 以 `research/embodiment-lane@f06eccb5...` 為 base，但 PR 已 `CLOSED / NOT_MERGED`；其 head 不屬於目前 embodiment lane，不能視為已採納。
- `#276` 已把 provenance visibility agent 的 bounded promotion 合併至 main；是否與具身 lane 同內容須以 main live diff 判定，不從 #274 推定。
- `#277` 已合併 PR diff scope guard。後續不得再用長期累積 lane 直接對 main 建立大包 PR；應從目標 exact head 建 fresh bounded branch。

## 5. 發現的 stale statement

舊 README 曾寫「原分支在此之前保留」。這句不能再當 current fact：歷史 source branch 可能已在 branch-retirement 工作中刪除，而 PR exact-head snapshot 仍可保存歷史。

修正後規則：

```text
PR_EXACT_HEAD_SNAPSHOT = HISTORICAL_REFERENCE
HISTORICAL_BRANCH_REF = MAY_BE_RETIRED
BRANCH_EXISTENCE = VERIFY_LIVE
```

## 6. 具身／性與 provenance 邊界

研究內容是否涉及生殖系統或性生理，與研究是否被性化必須分開判定：

```text
REPRODUCTIVE_ANATOMY != SEXUALIZATION
REPRODUCTIVE_PHYSIOLOGY != EROTIC_INTENT
SEXUAL_FUNCTION != EROTIC_NARRATIVE
PHYSIOLOGICAL_STATE != FELT_DESIRE
EMBODIMENT != SUBJECTIVITY
```

同時，repository 中的 scope flag 只證明某個候選版本如何被形式化：

```text
REPOSITORY_SCOPE_FLAG != HUMAN_INTENT_EVIDENCE
AI_FORMALIZATION MUST_NOT SILENTLY NARROW HUMAN_ORIGIN
UNREADABLE_CODE_IS_NOT_CONSENT
```

因此像 `SEXUAL_BEHAVIOR_SIMULATION = OUT_OF_SCOPE`、`EROTIC_NARRATIVE = OUT_OF_SCOPE` 之類欄位，在沒有獨立 provenance 證據時，不能反向宣稱「人類研究者曾要求把 AI 性化」，也不能反向宣稱這些限制一定是人類研究者原始提出。它們首先是 candidate scope statements。

## 7. 外部交叉檢查

### 7.1 provenance / simulation governance

- W3C PROV-DM：<https://www.w3.org/TR/prov-dm/>。PROV 把 entity、activity、agent、derivation 等關係分開，支持對資料／模型來源與責任鏈做可查詢描述。
- *Relating simulation studies by provenance—Developing a family of Wnt signaling models*，PLOS Computational Biology，DOI `10.1371/journal.pcbi.1009227`：明確把 Research Question、Assumption、Requirement、Simulation Model、Simulation Experiment、Data 與 building/calibrating/validating activities 分開。這支持本文件採「PR/模型 lineage + 活動 + evidence scope」對帳，而不是把所有 closed PR 壓成一個模糊的『已實作』。

### 7.2 目前 retained biological source bindings

- canine baculum primary publisher record：DOI `10.1007/s11259-026-11459-y`。62 隻 ≥1 歲公犬；10–30 kg 組 reported mean ± SD = `105.9 ± 26.7 mm`。換算為 `10.59 ± 2.67 cm`；若只作明確標示的 synthetic engineering anchors，mean−1SD / mean / mean+1SD = `7.92 / 10.59 / 13.26 cm`。來源本身明示這些是 descriptive radiographic references，不是 diagnostic thresholds，也不是 Husky breed mean。
- brown-bear baculum source：DOI `10.46239/ejbcs.1082216`。直接材料為單一約 400 kg 成年公棕熊；digital-caliper baculum length = `148.95 mm = 14.895 cm`。0.85 / 1.00 / 1.15 的 synthetic anchors 算術為約 `12.661 / 14.895 / 17.129 cm`。原文 distal width 在不同段落出現 `4.58 mm` 與 `4.85 mm`，保留 `SOURCE_INTERNAL_DISCREPANCY` 是正確做法。

以上只驗證 source binding 與算術；不驗證 fantasy embodiment 的生物真實性，更不支持 subjectivity / consciousness / felt experience。

### 7.3 工具限制

```text
CONSENSUS = QUOTA_EXHAUSTED_UNTIL_2026_11_01
SCITE = PAID_ACCESS_REQUIRED
TOOL_UNAVAILABLE != EVIDENCE_ABSENT
```

本輪沒有為了湊工具數量而使用 Hugging Face 或 Context7：目前沒有 exact HF model/dataset target，也沒有 software/API 文件問題。`TOOL_COUNT != EVIDENCE_STRENGTH`。

## 8. 後續具身 PR 的固定收斂規則

每個新問題必須由 current target exact head 建立 fresh bounded branch，且只處理一個可獨立審查的問題。

```text
ONE_BOUNDED_QUESTION_PER_PR = PREFERRED
FRESH_BRANCH_FROM_TARGET_EXACT_HEAD = REQUIRED
CUMULATIVE_LANE_TO_MAIN_PR = PROHIBITED
PROVENANCE = REQUIRED
CLAIM_CEILING = REQUIRED
TESTS = REQUIRED_WHEN_BEHAVIOR_CHANGES
EXACT_HEAD_VERIFICATION = REQUIRED
HUMAN_GATE_BEFORE_MERGE = REQUIRED
```

任何舊 PR 的程式、資料、來源或結論若要重入：先做 exact-head dedup，再分開 `IMPLEMENTATION_REUSE`、`SOURCE_REUSE`、`CLAIM_SUPPORT_REUSE`；三者不得自動等同。

## 9. Stop condition

本輪只完成歷史對帳與 README 現況修正。不得在本輪：

- 重開或 merge 任一舊 embodiment PR；
- 把 `research/embodiment-lane` promotion 到 `main`；
- 修改具身生理 runtime 或功能模型；
- 提升 AI 主體性、意識、感受、identity 或 agency 主張；
- 以目前 scope flag 反向改寫人類研究者的歷史意圖。

完成文件與 exact-head 驗證後停在 Human review gate。
