# CCTS／Human–AI Collaboration／Human–AI Learning：Repository Reconciliation 與研究實作操作手冊（2026-10-05）

狀態：

```text
DOCUMENT_TYPE = IMPLEMENTATION_HANDOFF / OPERATIONS_MANUAL
CONTROL_OBJECTIVE = FIXED
IMPLEMENTATION_METHOD = ADAPTIVE
CHAT_CONTEXT != IMPLEMENTATION_HANDOFF
LIVE_REPOSITORY_STATE = SOURCE_OF_TRUTH

IMPLEMENTATION_AUTHORIZATION = NO_BY_THIS_DOCUMENT
EMPIRICAL_EXPERIMENT_AUTHORIZATION = NO
MERGE_AUTHORITY = NONE
PUBLISH = NO
DEPLOYMENT = FALSE
CANONICAL_EFFECT = NONE
HUMAN_GATE = REQUIRED
```

本手冊是給 ChatGPT Work／Codex 或其他 bounded executor 的可獨立重建 handoff。執行者不得要求讀取本次聊天才能理解任務；若 chat 與 repository live state 衝突，以 live repository 為準。

後續執行收據：使用者於 2026-10-05 另行要求實作 PR #266；[逐檔對帳與實作判定](CCTS_PR266_RECONCILIATION_DECISION_2026_10_05.md)已把 Phase A 寫入本 PR，並標明尚未凍結的區辨／結果問題與候選 QMS consumer 的繞過點。此請求不改寫本手冊的科學、合併或刪除權限上限；程式移植須先通過該收據記錄的 Phase B 複審門檻。

---

## 0. 任務目的

唯一控制目標：

> 把目前已分岔的 CCTS／Human–AI Learning durable work lane 與 current main 重新對帳，保留可驗證且仍必要的研究／工程成果，補入新的相鄰文獻比較與 claim boundary，並產生一個可供 Human + Teacher 複審的最小 reconciliation candidate。

這不是「把 lane 全部搬回 main」。

```text
RECONCILE
!= BLIND_MERGE
!= REBASE_FOR_CONVENIENCE
!= CHERRY_PICK_EVERYTHING
!= SCIENTIFIC_PROMOTION
```

---

## 1. Scope

本任務只包含：

1. Co-Constructed Thinking Space（CCTS，共構思考空間）；
2. Human–AI Collaboration（人機協作／合作）；
3. Human–AI Learning（人機學習）；
4. 直接支援以上三者的 QMS／provenance／study-design controls；
5. current durable CCTS lane 與 current main 的 reconciliation；
6. adjacent-literature crosswalk；
7. discriminant validity／outcome validity 的研究規格凍結準備。

### Out of scope

禁止自行擴張到：

- AI subjectivity possibility；
- consciousness；
- phenomenal experience；
- moral agency／moral status；
- embodiment；
- 新的 L-level ontology；
- 新研究 lane；
- publication／Zenodo；
- deployment；
- branch deletion；
- destructive repository cleanup；
- 真實 participant experiment。

若發現上述相鄰材料，只記 `OUT_OF_SCOPE` 或 dependency，不深入、不實作。

---

## 2. Current snapshot：只能作起始索引，不可當未來真相

本 handoff 建立時：

```text
REPOSITORY = maker-luder/aion-governance-framework

MAIN = a38a1b5269be99d0af7f25495e49d479608b5dcf

CCTS_LANE = research/ccts-human-ai-learning-lane
CCTS_LANE_HEAD = fa85a7f30ec77007280aa4957bd71a74c3a8683f

LANE_VS_MAIN = DIVERGED
AHEAD_BY = 8
BEHIND_BY = 9
MERGE_BASE = 6a34d7780dd6d5bc717cd6c82ba39e7a6241c2fd

PR_265 = CLOSED / DRAFT / NOT_MERGED
PR_265_HISTORICAL_HEAD = 8e22da9396b0dbb9569f09330dad4d704a0355a9

OPEN_PRS_AT_HANDOFF_CREATION = 0
```

執行前必須重查；任何值改變都以新的 live state 為準。

---

## 3. Mandatory live-state recovery

開始任何 write 前，必須完成：

```text
LOCK CURRENT STATE
-> READ repository default branch
-> READ current main exact SHA
-> READ current CCTS lane exact SHA
-> READ PR #265 live state
-> READ all open PRs
-> READ relevant branch topology
-> COMPARE main...CCTS lane
-> READ current CI / Actions for exact candidate heads
-> READ current tests and package entry points
-> SEARCH for equivalent implementation
-> ONLY THEN DECIDE
```

### Recovery rules

```text
CHAT_CONTEXT != SOURCE_OF_TRUTH
HANDOFF_SNAPSHOT != LIVE_STATE
OLD_SHA != CURRENT_SHA
OLD_CI != CURRENT_CI
OLD_REVIEW != CURRENT_REVIEW
UNKNOWN_RESULT -> READ LIVE STATE
READ_BEFORE_RETRY = TRUE
VERIFY_AFTER_WRITE = TRUE
```

禁止：

- 因 timeout／freeze 重複 create/update/comment/merge；
- 在不知道前一次 write 是否成功時再次 write；
- `reset --hard`；
- force push；
- `git clean` 清除未知內容；
- 覆蓋未辨識 changes。

---

## 4. Required read order

### A. Current main navigation / governance

先讀：

1. `README.md`
2. `README.zh-TW.md`
3. `docs/INDEX.md`
4. `docs/RESEARCH_MAP.md`
5. `docs/CURRENT_STATE.md`
6. `docs/governance/BRANCH_TOPOLOGY_POLICY.md`（若實際路徑不同，以搜尋結果為準）

目的：

- 確認 current scientific standing；
- 確認 CCTS lane 的定位；
- 確認 branch／authority／Human gate 規則；
- 避免拿舊 handoff 覆蓋 current navigation。

### B. Main 上的 CCTS／learning canonical antecedents

至少讀：

1. `docs/research/CO_CONSTRUCTED_THINKING_SPACE_FORMALIZATION_2026_09_16.md`
2. `docs/research/CCTS_GROUNDING_ADMISSION_EXTENSION_2026_09_16.md`
3. `docs/research/CCTS_ADVERSARIAL_EPISTEMIC_REVISION_PROTOCOL_2026_09_23.md`
4. `docs/research/CCTS_LEARNING_CONTRAST_STRENGTHENING_2026-09-28.md`
5. `docs/research/CCTS_HUMAN_AI_LEARNING_APPLICABILITY_BOUNDARY_HYPOTHESIS_2026_09_30.md`
6. `docs/research/HUMAN_AI_LEARNING_CCTS_HTECR_EXTERNAL_CROSSWALK_AND_FALSIFICATION_2026_09_18.md`
7. `research-labs/human-ai-longitudinal-study_v0.1.0/README.md`
8. `research-labs/coupled-cognition-quality-factory_v0.1.0/docs/EPISTEMIC_PROVENANCE_AND_CO_DEVELOPMENT.md`
9. `research-labs/coupled-cognition-quality-factory_v0.1.0/docs/END_TO_END_RESEARCH_QMS.md`

### C. Durable CCTS lane exact-head delta

在 current lane exact SHA 重讀：

1. `docs/research/ccts-human-ai-learning/README.md`
2. `docs/research/ccts-human-ai-learning/CCTS_DISCRIMINANT_OUTCOME_STUDY_SPEC_2026_10_03.md`
3. `docs/research/ccts-human-ai-learning/LONGITUDINAL_ALIAS_FALSIFICATION_2026_10_03.md`
4. `docs/research/ccts-human-ai-learning/PR265_HUMAN_AI_COLLABORATION_QMS_DEDUP_DECISION_2026_10_03.md`
5. `docs/research/ccts-human-ai-learning/PR265_HUMAN_AI_COLLABORATION_QMS_IMPLEMENTATION_HANDOFF_2026_10_03.md`
6. `research-labs/coupled-cognition-quality-factory_v0.1.0/src/aion_coupled_quality/human_ai_collaboration.py`
7. `research-labs/coupled-cognition-quality-factory_v0.1.0/src/aion_coupled_quality/extended_quality.py`
8. `research-labs/coupled-cognition-quality-factory_v0.1.0/tests/test_human_ai_collaboration_controls.py`
9. `research-labs/human-ai-longitudinal-study_v0.1.0/CCTS_VALIDITY_STUDY_DESIGN.md`
10. `research-labs/human-ai-longitudinal-study_v0.1.0/src/aion_human_ai_longitudinal/ccts_validity_study_design.py`
11. `research-labs/human-ai-longitudinal-study_v0.1.0/src/aion_human_ai_longitudinal/longitudinal_falsification.py`
12. 對應 tests。

### D. 本輪 review record

讀：

`docs/research/CCTS_HUMAN_AI_COLLABORATION_LEARNING_REVIEW_2026_10_05.md`

它是 review scaffold，不是 implementation authority。

---

## 5. 已知問題位置與 Teacher scaffolding

### Failure mode 1 — 在 diverged durable lane 直接續寫

**錯誤位置：**

```text
research/ccts-human-ai-learning-lane@fa85a7f...
vs
main@a38a1b5...
```

**禁止做法：**

> 「lane 有現成 code，所以直接在上面再加下一階段。」

**正確鷹架：**

1. compare exact heads；
2. 將每個 delta 先分類；
3. 判斷是否 current main 已有等價控制；
4. 從 current main 開 isolated reconciliation branch；
5. 只 port 最小必要內容；
6. 重新 test／review。

### Failure mode 2 — 繼承 PR #265 的舊 verification

**錯誤位置：**

```text
#265 historical head = 8e22da9...
current lane head = fa85a7f...
```

**禁止推論：**

```text
348_TESTS_PASSED_ON_OLD_HEAD
=> CURRENT_HEAD_VERIFIED
```

**正確：**

```text
HEAD_CHANGED
=> OLD_VERIFICATION_EXPIRES
=> FRESH_LOCAL_TEST
=> FRESH_REMOTE_CI
=> FRESH_REVIEW
```

### Failure mode 3 — 把 QMS control 當科學效果

**錯誤位置：**

`human_ai_collaboration.py` 與 Full-QMS integration 是 workflow control。

**禁止：**

```text
QMS_PASS -> GOOD_COLLABORATION
QMS_PASS -> HUMAN_LEARNING
QMS_PASS -> CCTS_VALID
```

### Failure mode 4 — 用 synthetic fixtures 代替 Human outcome

**錯誤位置：**

`ccts_validity_study_design.py`、`longitudinal_falsification.py` 等目前是 synthetic design／falsification harness。

**禁止：**

```text
SYNTHETIC_OUTCOME_ENUM
=> HUMAN_OUTCOME_OBSERVED
```

### Failure mode 5 — 發現近鄰框架後又新增 CCTS 子構念

新的 adjacent literature 是用來**挑戰／吸收／縮窄** CCTS，不是預設用來長新欄位。

```text
PAPER_FOUND
!= NEW_CONSTRUCT_REQUIRED
```

---

## 6. Reconciliation classification matrix

對 lane 每個 changed file／construct，必須先填一列：

| Field | 說明 |
|---|---|
| `ITEM` | file／class／construct |
| `CURRENT_MAIN_EQUIVALENT` | main 是否已有等價實作 |
| `LANE_DELTA` | lane 真正新增什麼 |
| `STILL_NEEDED` | YES / NO / UNKNOWN |
| `SCIENTIFIC_ROLE` | structure / method / outcome / governance / none |
| `EVIDENCE_ROLE` | design / synthetic implementation / test / empirical / docs |
| `DUPLICATION_RISK` | low / medium / high |
| `STALE_ASSUMPTION` | 是否依賴舊 main |
| `PORT_DECISION` | PORT / NARROW / DROP / HOLD |
| `CLAIM_EFFECT` | 必須預設 NONE |
| `TEST_REQUIRED` | targeted regression |
| `HUMAN_GATE_REQUIRED` | YES |

若不能回答 `CURRENT_MAIN_EQUIVALENT` 或 `STILL_NEEDED`：

```text
-> HOLD
-> DO_NOT_PORT_YET
```

---

## 7. Literature reconciliation contract

### 新增必讀比較來源

#### SIGDIAL 2026

Liu, Zhengyuan; Yin, Stella; Kan, Min-Yen; Chen, Nancy.  
*Bridging Talk and Thought: Understanding Dialogue Dynamics Across Collaborative Problem-Solving Contexts.*

用途：

- dialogue dynamics；
- cognitive／non-cognitive coding；
- metacognitive regulation；
- deeper collaboration discriminator。

要回答：

> 如果 existing dialogue/metacognitive coding 已能解釋觀察，CCTS 的 provenance／authority／rejected-branch／longitudinal binding 還提供什麼新增可觀測區辨？

#### PNAS Nexus 2026

Gonzalez, Cleotilde; Donahue, Kate; Goldstein, Daniel G.; Heidari, Hoda; Jalali, Mohammad S.; Schelble, Beau; Singh, Aarti; Woolley, Anita Williams.  
*Toward a science of human–AI teaming for decision making: A complementarity framework.*  
DOI `10.1093/pnasnexus/pgag030`.

用途：

- Human–AI complementarity；
- reasoning／memory／attention；
- meta-coordination／governance；
- role partition；
- trust calibration。

要回答：

> CCTS 是一個能預測 complementarity 的 process condition，還是只是一個 governance profile？

### 必須保留的既有重要來源

- Vaccaro, Almaatouq & Malone (2024), DOI `10.1038/s41562-024-02024-1`
- Fan et al. (2025), DOI `10.1111/bjet.13544`
- Järvelä, Nguyen & Hadwin (2023), DOI `10.1111/bjet.13325`
- Edwards et al. (2025), DOI `10.1111/bjet.13534`
- Wu et al. (2025), DOI `10.3102/0013189X251333628`
- 其他 current repository crosswalk 已核對來源。

### Source rules

```text
DISCOVERY_RESULT != VALIDATION
ADJACENT_LITERATURE != DIRECT_VALIDATION
SOURCE_REUSE != CLAIM_SUPPORT_REUSE
AUTHORITY != SCIENTIFIC_TRUTH
```

每一篇來源都必須記：

- exact claim it supports；
- what it does not support；
- study type；
- sample／task scope（如適用）；
- external validity limitation；
- 是否直接測 CCTS（預期通常 NO）。

---

## 8. Discriminant-validity freeze contract

在任何 empirical coding implementation 前，必須先凍結：

### Candidate classes

至少：

1. one-shot assistant；
2. iterative prompting；
3. multi-turn clarification without reciprocal substantive revision；
4. provenance/authority-rich interaction without reciprocal revision；
5. reciprocal revision without reconstructable provenance；
6. CCD-like collaborative dialogue；
7. CoRL／SSRL／HASRL-like regulation；
8. candidate CCTS。

### Predefined downgrade rule

不得在結果出來後才發明保護 CCTS 的新欄位。

至少允許：

```text
SUPPORTED_CANDIDATE
NARROWED
ABSORBED_INTO_EXISTING_CONSTRUCT
DOWNGRADE_TO_METHOD_PROFILE
FALSIFIED_SPECIFIC_CLAIM
INCONCLUSIVE
HOLD
```

### Stop condition

若近鄰模型已充分解釋資料，且加入 CCTS residual 沒有穩定 incremental discrimination／prediction：

```text
STOP_CONSTRUCT_EXPANSION = YES
CCTS_DISPOSITION = DOWNGRADE_OR_ABSORB
```

---

## 9. Outcome-validity freeze contract

### Primary outcomes 必須先指定

不要把所有結果混成一個總分。

候選：

- independent Human judgement；
- delayed retention；
- held-out transfer；
- independent reconstruction；
- error detection；
- calibration；
- task performance。

### Baselines

至少考慮：

```text
HUMAN_ALONE
AI_ALONE
HUMAN_PLUS_AI_NON_CCTS_MATCHED
HUMAN_PLUS_AI_CCTS_CANDIDATE
```

不要只比較 Human-alone vs Human+AI，否則不能識別 synergy。

### Confounds

至少記：

- prior knowledge；
- task difficulty；
- exposure amount；
- practice／retrieval-testing exposure；
- model/version/configuration；
- AI-alone quality；
- role instructions；
- trust／reliability perception；
- Human self-generated strategy；
- contamination between conditions。

---

## 10. Engineering method freedom

Executor 不必照抄 Teacher 的 class 名、檔案位置或具體 code shape。

允許：

- 發現 current main 已經有更好的 implementation point；
- 合併重複 controls；
- 回報 `NO_CHANGE`；
- 回報 `NO_NEW_IMPLEMENTATION_REQUIRED`；
- 用證據反駁 handoff 的假設；
- 選擇更小的 implementation；
- 只做 docs／tests 而不新增 runtime code；
- 對某項 delta 判 `DROP` 或 `HOLD`。

但是：

```text
CONTROL_OBJECTIVE = STABLE
IMPLEMENTATION_METHOD = ADAPTIVE

GUIDED != SCRIPTED
AUTONOMY != AUTHORITY
FREE_DEVELOPMENT != UNBOUNDED_GROWTH
```

任何偏離預期的方法必須回答：

1. 解決哪個已批准 objective？
2. 為什麼 current implementation 不足？
3. 新方法新增哪些 maintenance／scientific risk？
4. 哪些 negative tests 防止弱化 boundary？

答不出來即 HOLD。

---

## 11. Preferred phase separation

### Phase A — READ / RECONCILE ONLY

輸出：

- live state receipt；
- current main vs lane matrix；
- duplicate/stale/needed classification；
- literature delta；
- proposed minimal port set；
- unresolved UNKNOWN。

本 phase 不寫 implementation。

### Phase B — REVIEW GATE

Teacher + Human review：

- 是否 research question 已足夠凍結；
- 哪些 lane delta 可 port；
- 是否需要 implementation；
- 是否需要新 PR；
- 是否仍維持 one active PR。

### Phase C — BOUNDED IMPLEMENTATION（只有明確授權後）

若授權：

- 從 current main 的 fresh exact SHA 建 isolated branch；
- port／rewrite 最小必要 change；
- targeted negative tests；
- package regression；
- static/type checks；
- remote CI；
- reverse review。

### Phase D — HUMAN GATE

只有 fresh exact-head evidence 可進：

```text
READY_FOR_HUMAN_REVIEW
```

不得自動 merge。

---

## 12. Tests and verification contract

若未來有 code change，最低要求：

### Targeted tests

每個 ported control／study interface 必須有：

- positive structural case；
- hard negative；
- stale SHA／old verification case（如涉 authority）；
- direct-construction／replace bypass negative case（如 dataclass／typed record 可繞）；
- provenance mismatch；
- scope-growth／claim promotion rejection；
- duplicate／conflict regression（如涉及 reconciliation）。

### Package tests

重跑受影響 package 全測試，不只新 tests。

### Static／quality

依 current repository config 實際存在的工具執行，例如：

- mypy strict（若 current config 要求）；
- ruff／lint；
- compile/import check；
- repository quality validators。

不要因 handoff 寫了工具名就假定 current repo 仍使用它；先讀 config。

### Remote exact-head CI

```text
LOCAL_PASS
!= REMOTE_CI_PASS

PREVIOUS_HEAD_REMOTE_PASS
!= CURRENT_HEAD_REMOTE_PASS
```

任何 head 變動後重新驗證。

### Scientific boundary

```text
TEST_PASS
!= CCTS_VALIDATION
!= HUMAN_LEARNING
!= CAUSALITY
```

---

## 13. Acceptance criteria

Phase A review candidate 至少要滿足：

- [ ] live main SHA、lane SHA、PR #265、open PRs 已重新讀取；
- [ ] main/lane compare 已保存 exact counts；
- [ ] lane 每個重要 delta 已做 reuse/dedup/stale classification；
- [ ] no old CI/review inherited；
- [ ] SIGDIAL 2026 與 PNAS Nexus 2026 已放入 adjacent crosswalk；
- [ ] Vaccaro synergy boundary 與 Fan learning/transfer boundary 保留；
- [ ] CCTS structure、Collaboration QMS、Human learning outcome 三層未混寫；
- [ ] downgrade／absorb／falsification disposition 已預先定義；
- [ ] 未新增未授權 construct；
- [ ] 未做 empirical participant execution；
- [ ] final report 可由 repository alone 重建。

若任何核心項 UNKNOWN：

```text
READY = NO
DISPOSITION = HOLD
```

---

## 14. Stop conditions

立即停止 write 並回報：

1. current main／lane head 在執行中改變；
2. 出現另一個 active PR 與本 lane 衝突；
3. 發現未辨識的 repository change；
4. current main 已吸收 lane 等價實作，導致 planned port 重複；
5. scientific question 仍未凍結卻需要新增 construct 才能繼續；
6. empirical data／private transcript／Human identity 需求出現；
7. 需要 destructive action；
8. 需要 merge／publish／deploy；
9. CI／API 結果 unknown；
10. evidence contradicts handoff assumptions。

處置：

```text
STOP
-> READ LIVE STATE
-> REPORT EXACT CONTRADICTION
-> HOLD
```

不要自行擴 scope 解決。

---

## 15. Authority boundary

```text
DESIGN != IMPLEMENTATION
IMPLEMENTATION != VERIFICATION
VERIFICATION != SCIENTIFIC_VALIDATION
VERIFICATION != AUTHORIZATION
AUTHORIZATION != MERGE
AUTOMATION != AUTHORITY
```

本手冊本身：

```text
DESIGN_DOC_EXISTS = YES
IMPLEMENTATION_AUTHORIZED = NO
MERGE_AUTHORITY = NONE
PUBLISH_AUTHORITY = NONE
DEPLOYMENT = FALSE
BRANCH_DELETE_AUTHORITY = NONE
```

---

## 16. Final report contract

未來 executor 最終回報必須包含以下欄位；不得只說「完成」。

```text
REPOSITORY =
MAIN_SHA_AT_START =
MAIN_SHA_AT_END =

SOURCE_LANE =
SOURCE_LANE_SHA_AT_START =
SOURCE_LANE_SHA_AT_END =

WORK_BRANCH =
WORK_HEAD =

PR_NUMBER =
PR_STATE =
PR_BASE =
PR_HEAD =

LIVE_STATE_CHANGED_DURING_RUN = YES | NO

READ_SET =
FILES_CHANGED =
FILES_NOT_CHANGED =
DELTA_CLASSIFICATION =

NEW_CONSTRUCT_CREATED = YES | NO
SCIENTIFIC_CLAIMS_CHANGED = YES | NO
CANONICAL_EFFECT =
DEPLOYMENT =

LOCAL_TARGETED_TESTS =
LOCAL_PACKAGE_TESTS =
TYPE_STATIC_CHECKS =
REMOTE_CI_EXACT_HEAD =
REMOTE_CI_URLS =

OLD_VERIFICATION_INHERITED = NO

ADJACENT_LITERATURE_UPDATED =
DISCRIMINANT_QUESTION_STATUS =
OUTCOME_QUESTION_STATUS =
DOWNGRADE_RULE_STATUS =

UNRESOLVED =
HOLD_REASONS =
NEXT_SINGLE_GATE =
MERGE_AUTHORIZATION = NONE_UNLESS_FRESH_HUMAN_GATE
```

### Report wording constraints

允許：

- `IMPLEMENTED`
- `TESTED_LOCALLY`
- `REMOTE_CI_PASS`
- `READY_FOR_HUMAN_REVIEW`
- `HOLD`
- `NO_CHANGE`
- `NO_NEW_IMPLEMENTATION_REQUIRED`

禁止沒有證據地寫：

- validated CCTS；
- proven Human learning；
- established synergy；
- confirmed causality；
- scientifically verified；
- merge ready（除非 current governance 所有 gate 都 fresh pass 且 Human 明確授權）。

---

## 17. Final invariant

```text
REPOSITORY_FIRST
PROVENANCE_PRESERVED
CLAIM_BOUNDARY_PRESERVED
NEGATIVE_RESULT_ALLOWED
DOWNGRADE_ALLOWED
UNKNOWN_REMAINS_UNKNOWN
HUMAN_GATE_PRESERVED

CONTROL_OBJECTIVE = FIXED
IMPLEMENTATION_METHOD = ADAPTIVE
FREE_DEVELOPMENT != UNBOUNDED_GROWTH
```

真正目標不是讓 CCTS「一定成功」，而是讓 repository 能可靠回答：

> CCTS 相對近鄰構念到底增加了什麼？  
> 它若沒有增加，系統是否能誠實地縮窄、吸收或降級？  
> Human–AI collaboration 的工程品質，是否被正確地與 Human learning 的實證效果分離？

在這三個問題凍結前，不進下一個大型 implementation。
