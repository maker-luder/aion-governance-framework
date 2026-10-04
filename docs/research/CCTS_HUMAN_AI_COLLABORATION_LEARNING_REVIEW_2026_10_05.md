# CCTS／Human–AI Collaboration／Human–AI Learning：研究複審、live-state checkpoint 與下一階段 gate（2026-10-05）

狀態：

```text
RECORD_TYPE = RESEARCH_REVIEW_CHECKPOINT
SCOPE = CCTS + HUMAN_AI_COLLABORATION + HUMAN_AI_LEARNING
IMPLEMENTATION_AUTHORIZED = NO
EMPIRICAL_EXPERIMENT_AUTHORIZED = NO
MERGE_TO_MAIN = NO_BY_THIS_RECORD
PUBLISH = NO
DEPLOYMENT = FALSE
CANONICAL_EFFECT = NONE
SCIENTIFIC_DISPOSITION = HOLD
HUMAN_GATE = REQUIRED
```

本文件保存 2026-10-05 的 repository live-state recovery、外部研究交叉檢查、反例／替代解釋與下一階段研究 gate。它不是新 CCTS 定義，不修訂既有公開學術物件，也不把工程控制或外部相鄰文獻升格成 CCTS／Human–AI Learning 的科學驗證。

---

## 1. Provenance／來源歸屬

### HUMAN_ORIGIN

使用者在本輪先要求重新檢查 GitHub 倉庫中的：

1. Co-Constructed Thinking Space（CCTS，共構思考空間）；
2. Human–AI Collaboration（人機協作／合作）；
3. Human–AI Learning（人機學習）。

完成複審後，使用者再明確要求：

- 建立一個新的 PR 保存本輪結果；
- 將研究紀錄與操作手冊寫完整；
- 延續既有 repository-first、QMS、claim boundary、Human gate 與可獨立重建 handoff 的寫法；
- 若 executor 已有已知 failure mode，不可只把工作丟回去重想；Teacher 應先在 PR 直接標出問題位置、邊界與修正鷹架。

### AI_FORMALIZATION

ChatGPT Teacher 本輪負責：

- live-state recovery；
- 把 CCTS／合作品質／Human learning 結果分成三個不同層級；
- 形式化 current issue register；
- 外部文獻 crosswalk 與限制；
- 將下一步轉為 discriminant validity（區辨效度）、outcome validity（結果效度）與 repository reconciliation（倉庫重新對帳）的可反證 gate；
- 建立獨立 implementation handoff／操作手冊。

### JOINT_SYNTHESIS

目前使用的三層工作區分：

```text
CCTS STRUCTURE
!= HUMAN_AI_COLLABORATION QMS
!= HUMAN_AI_LEARNING OUTCOME
```

是目前共同工作上的研究整理方式，不宣稱它是外部既有 taxonomy（分類學）或新的心理構念。

### REPOSITORY_STATE

本文件中的 SHA、PR、branch、diff 與 CI 判斷來自 2026-10-05 重新讀取 GitHub live state，不沿用舊對話 checkpoint。

### EXTERNAL_SOURCE

外部來源只支援相鄰構念、方法、替代解釋或特定研究結果；沒有任何一篇本輪來源直接測量本 repository-defined CCTS。

### IMPLEMENTATION_EVIDENCE

工作支線已存在 executable synthetic interfaces 與 Human–AI Collaboration QMS controls，但 exact current lane head 尚無本輪取得的 remote workflow/status evidence。

### UNKNOWN／NOT_ESTABLISHED

```text
CCTS_VALIDITY = NOT_ESTABLISHED
CCTS_DISTINCT_CONSTRUCT_STATUS = NOT_ESTABLISHED
HUMAN_AI_COLLABORATION_SYNERGY = NOT_ESTABLISHED
HUMAN_LEARNING = NOT_ESTABLISHED
RETENTION = NOT_ESTABLISHED
TRANSFER = NOT_ESTABLISHED
CCTS_SPECIFIC_EFFECT = NOT_ESTABLISHED
CAUSALITY = NOT_ESTABLISHED
```

---

## 2. Live repository checkpoint

查證日期：2026-10-05。

```text
REPOSITORY = maker-luder/aion-governance-framework

MAIN_BRANCH = main
MAIN_SHA = a38a1b5269be99d0af7f25495e49d479608b5dcf

CCTS_WORK_LANE = research/ccts-human-ai-learning-lane
CCTS_WORK_LANE_HEAD = fa85a7f30ec77007280aa4957bd71a74c3a8683f

LANE_VS_MAIN = DIVERGED
LANE_AHEAD_BY = 8
LANE_BEHIND_BY = 9
MERGE_BASE = 6a34d7780dd6d5bc717cd6c82ba39e7a6241c2fd

PR_265 = CLOSED / DRAFT / NOT_MERGED
PR_265_HISTORICAL_HEAD = 8e22da9396b0dbb9569f09330dad4d704a0355a9
PR_265_HISTORICAL_BASE = 6a34d7780dd6d5bc717cd6c82ba39e7a6241c2fd

OPEN_PRS_AT_CHECK = 0
CURRENT_LANE_REMOTE_WORKFLOW_EVIDENCE_OBTAINED = NO
CURRENT_LANE_COMBINED_STATUS_EVIDENCE_OBTAINED = NO
```

### Critical interpretation

```text
PR_265_HEAD
!= CURRENT_CCTS_LANE_HEAD

OLD_LOCAL_TEST_REPORT
!= CURRENT_HEAD_VERIFICATION

OLD_REVIEW
!= CURRENT_HEAD_REVIEW

DIVERGED_LANE
!= CLEAN_EXTENSION_OF_MAIN
```

PR #265 記錄過的 local test／review evidence 屬於當時 head；它不能自動轉移到目前 `fa85a7f...`。任何後續 re-entry 都必須以 current main 與 current lane 重新建立 exact-head evidence。

---

## 3. Current issue register：直接標出問題位置

### ISSUE A — 工作支線已與 current main 分岔

位置：

```text
main@a38a1b5269be99d0af7f25495e49d479608b5dcf
research/ccts-human-ai-learning-lane@fa85a7f30ec77007280aa4957bd71a74c3a8683f
```

事實：

```text
STATUS = diverged
AHEAD = 8
BEHIND = 9
```

風險：

- 直接在 durable lane 繼續堆疊會讓 stale assumptions、conflict 與驗證來源更難拆分；
- 舊 main baseline `6a34d...` 不能代表目前 `main@a38a1b5...`；
- 不可把 lane 的 code presence 說成 main 已採納。

修正鷹架：

```text
READ CURRENT MAIN
-> READ CURRENT LANE
-> COMPARE exact heads
-> CLASSIFY each delta
-> RECONCILE onto current main in a non-destructive isolated working branch
-> FRESH TEST / CI
-> HUMAN REVIEW
```

禁止用 force-push／reset-hard 把差異「洗掉」。

### ISSUE B — PR #265 的 historical head 與 durable lane current head 不同

位置：

```text
PR #265 historical head = 8e22da9396b0dbb9569f09330dad4d704a0355a9
current durable lane head = fa85a7f30ec77007280aa4957bd71a74c3a8683f
```

這不是 metadata 小問題。PR 關閉後 durable lane 仍增加研究文件與 QMS implementation，因此：

```text
PR_265_VERIFICATION
!= CURRENT_LANE_VERIFICATION
```

後續若建立 implementation PR，必須從新的 exact head 重新審查，不可「reopen 舊證據」。

### ISSUE C — current lane head 缺 fresh remote exact-head CI evidence

本輪查詢 current lane exact SHA 時，沒有取得 associated workflow runs 或 combined status。

正確處置：

```text
NO_REMOTE_STATUS_OBSERVED
=> VERIFICATION = UNKNOWN
!= FAIL
!= PASS
```

不得把舊 `348 tests passed` 或其他歷史 head 的 CI 套用到 `fa85a7f...`。

### ISSUE D — 相鄰研究框架正在收斂到更強的比較基線

目前 CCTS 的最大科學風險不是「功能不夠多」，而是可能被既有協作／學習構念吸收。

需要正面比較的鄰近範圍至少包括：

- ordinary iterative prompting（一般反覆提示）；
- common ground（共同基礎）／Joint Problem Space（共同問題空間）；
- CCD 類認知協作對話；
- CoRL／SSRL（共同調節／社會共享調節學習）；
- HASRL（Human–AI Shared Regulation in Learning，人機共享學習調節）；
- epistemic co-agency（知識共同能動性）；
- Human–AI teaming／complementarity（人機團隊／互補性）；
- metacognitive dialogue regulation（後設認知對話調節）。

### ISSUE E — 結構 conformance、QMS quality 與 learning outcome 仍有被混寫的風險

必須固定：

```text
CCTS_STRUCTURAL_CONFORMANCE
!= EMPIRICAL_MECHANISM

QMS_PASS
!= CCTS_VALIDITY

TASK_PERFORMANCE
!= HUMAN_LEARNING

IMMEDIATE_GAIN
!= RETENTION
!= TRANSFER

HUMAN_AI_AUGMENTATION
!= HUMAN_AI_SYNERGY
```

---

## 4. CCTS：目前合理保留的結構層

現有 repository-defined CCTS core 已包含：

```text
EXPLICIT_PROBLEM_REPRESENTATION
+ HUMAN -> AI substantive REVISES / CHALLENGES
+ AI -> HUMAN substantive REVISES / CHALLENGES
+ SOURCE_ROLE_PROVENANCE
+ CLAIM_BOUNDARY
+ AUTHORITY_SEPARATION
+ REJECTED_BRANCH_PRESERVATION
+ LONGITUDINAL_REENTRY
```

因此以下不足以單獨構成 CCTS：

- 對話輪數很多；
- prompt 越寫越長；
- AI 持續順從修改；
- 雙方使用相同簡稱；
- 任務最後完成；
- 有 Git history；
- 有 QMS；
- 有 publication。

### 目前最重要的科學問題

```text
NOVEL_LABEL != DISTINCT_CONSTRUCT
```

若 CCTS 相較 CCD／SSRL／team cognition／epistemic co-agency 等沒有穩定的 incremental discriminant value（增量區辨價值）或 independent outcome value（獨立結果價值），允許：

```text
DOWNGRADE_TO_METHOD_PROFILE
```

候選降級描述：

> provenance-bounded research/governance profile  
> 來源有界、可追溯的研究／治理型態。

這不是失敗迴避條款，而是預先指定的反證處置。

---

## 5. Human–AI Collaboration：科學現象與 QMS 控制必須分開

current lane 的 Human–AI Collaboration QMS 實作針對六項 workflow quality controls：

1. Human review capacity（人工審閱／容量 gate）；
2. known-defect remediation（已知缺陷後禁止 blind retry）；
3. authority-source separation（prompt／recommendation／self-report 不得當授權）；
4. bilingual Human reviewability（繁中可審閱與雙 normative surface parity）；
5. research disposition / scope-growth readmission（研究處置與擴張再准入）；
6. branch provenance preservation（分支歷史保留／刪除權限分離）。

其中有價值的工程規則包括：

```text
PROMPT != AUTHORIZATION
RECOMMENDATION != AUTHORIZATION
SELF_REPORT != AUTHORIZATION
STALE_SHA != LIVE_STATE
OUTPUT_DELIVERED != HUMAN_APPROVED
OLD_PASS != CURRENT_PASS

KNOWN_DEFECT
+ SAME_EXECUTOR
+ UNCHANGED_HANDOFF
= PROHIBITED_BLIND_RETRY
```

但科學上仍必須維持：

```text
QMS_PASS
!= GOOD_COLLABORATION_SCIENTIFICALLY_ESTABLISHED

READY_FOR_HUMAN_REVIEW
!= HUMAN_COMPREHENSION

GOOD_GOVERNANCE
!= CCTS_VALIDITY
```

---

## 6. Human–AI Learning：結果層不得被作品品質替代

目前 outcome（結果）至少要分開：

- `INDEPENDENT_HUMAN_JUDGEMENT`：AI withheld（不提供 AI）下的人類獨立判斷；
- `IMMEDIATE_PERFORMANCE`：即時任務表現；
- `DELAYED_RETENTION`：延遲保持；
- `HELD_OUT_TRANSFER`：未見任務上的遷移；
- `INDEPENDENT_RECONSTRUCTION`：獨立重建問題／方法；
- `ERROR_DETECTION`：錯誤辨識；
- `CALIBRATION`：信心與正確性的校準；
- `TASK_PERFORMANCE`：任務產物品質。

```text
BETTER_ARTIFACT
!= HUMAN_LEARNING

TASK_COMPLETION
!= RETENTION

SHORT_TERM_SCORE_GAIN
!= TRANSFER
```

任何未實際量測的 outcome 應標 `NOT_OBSERVED` 或 `NOT_ESTABLISHED`，不得以 synthetic fixture 的 enum 值代替真人資料。

---

## 7. External literature crosswalk：本輪新增／重新確認

### 7.1 Vaccaro, Almaatouq & Malone (2024)

*When combinations of humans and AI are useful: A systematic review and meta-analysis.*  
Nature Human Behaviour 8, 2293–2303.  
DOI: `10.1038/s41562-024-02024-1`

出版社來源：
https://www.nature.com/articles/s41562-024-02024-1

可支持：

- 系統回顧／統合分析納入 74 篇文章、106 個實驗、370 個 effect sizes；
- Human+AI 平均優於 Human-alone，但平均低於 Human 與 AI 之中較佳的一方；
- pooled human–AI synergy effect 為負值 `g = -0.23`，且 task type 有重要異質性。

對本研究的用途：

```text
HUMAN_AI_AUGMENTATION
!= HUMAN_AI_SYNERGY
```

未支持：

- CCTS 有 synergy；
- CCTS 是造成任何表現差異的機制；
- 特定 CCTS learning effect。

### 7.2 Fan et al. (2025)

*Beware of metacognitive laziness: Effects of generative artificial intelligence on learning motivation, processes, and performance.*  
British Journal of Educational Technology 56, 489–530.  
DOI: `10.1111/bjet.13544`

出版社來源：
https://bera-journals.onlinelibrary.wiley.com/doi/10.1111/bjet.13544

可支持：

- randomised experimental study；
- 117 名大學生；
- ChatGPT support 可提高短期 essay score improvement；
- knowledge gain 與 transfer 未顯著改善。

對本研究的用途：

```text
SHORT_TERM_TASK_IMPROVEMENT
!= KNOWLEDGE_GAIN
!= TRANSFER
```

### 7.3 Liu, Yin, Kan & Chen (SIGDIAL 2026)

*Bridging Talk and Thought: Understanding Dialogue Dynamics Across Collaborative Problem-Solving Contexts.*  
Proceedings of the 27th Annual Meeting of SIGDIAL.

ACL Anthology：
https://aclanthology.org/2026.sigdial-1.48/

可支持：

- hierarchical dialogue coding；
- cognitive／non-cognitive problem solving 與 metacognitive regulatory mechanisms 的分離；
- 作者在九個 datasets 中示範，metacognitive regulation 可作 deeper collaboration 的重要 discriminator。

對 CCTS 的主要價值是**強比較物／反例來源**：

> 如果既有 dialogue + metacognitive coding 已能區分我們稱作 deeper collaboration 的現象，CCTS 必須證明額外的 provenance／authority／rejected-branch／longitudinal binding 帶來增量可觀測價值，而不能只靠名稱差異。

### 7.4 Gonzalez, Singh & Woolley (2026)

*Toward a science of human–AI teaming for decision making: A complementarity framework.*  
PNAS Nexus 5(3), `pgag030`.  
DOI: `10.1093/pnasnexus/pgag030`

出版社來源：
https://academic.oup.com/pnasnexus/article/5/3/pgag030/8490283

可支持：

- complementarity 定義成 Human–AI team 超越 Human-alone 與 AI-alone 的條件；
- reasoning、memory、attention、meta-coordination、governance、role partition、trust calibration 等是重要比較面向。

對本研究的用途：

```text
CCTS_STRUCTURE
-> MAY BE A PROCESS CONDITION

CCTS_STRUCTURE
!= COMPLEMENTARITY ESTABLISHED
```

### 7.5 本輪工具限制

研究流程中：

- Exa 用於多角度外部 discovery；
- ACL Anthology／PNAS Nexus／Nature／Wiley 第一手頁面用於重要 metadata 與結果核對；
- Consensus 本月搜尋額度已耗盡；
- Scite MCP 需要付費方案或有效 trial；
- Hugging Face `paper_search` 在本輪 runtime 回報 tool unavailable。

```text
EXA_RESULT != VALIDATION
TOOL_UNAVAILABLE != EVIDENCE_ABSENT
PAPER_FOUND != CLAIM_SUPPORT
```

工具不可用不得被寫成「沒有反證／沒有文獻」。

---

## 8. 目前最小研究模型

三層分離：

```text
LAYER 1 — CCTS STRUCTURE
  explicit problem
  reciprocal substantive revision
  provenance
  claim boundary
  authority separation
  rejected branches
  longitudinal re-entry

LAYER 2 — HUMAN_AI_COLLABORATION QUALITY
  review gate
  remediation / no blind retry
  live authority
  bilingual reviewability
  scope control
  branch provenance

LAYER 3 — HUMAN_AI_LEARNING OUTCOMES
  independent judgement
  immediate performance
  delayed retention
  held-out transfer
  reconstruction
  error detection
  calibration
```

禁止：

```text
LAYER_1_PASS -> automatically infer LAYER_3_EFFECT
LAYER_2_PASS -> automatically infer LAYER_1_VALIDITY
```

---

## 9. 下一階段唯一合理 gate

### Gate 1 — Repository reconciliation

```text
main@a38a1b5...
vs
research/ccts-human-ai-learning-lane@fa85a7f...
```

先逐檔分類：

- still-needed current implementation；
- stale against current main；
- duplicate of main；
- docs-only historical record；
- candidate to port；
- candidate to drop；
- conflict／UNKNOWN。

### Gate 2 — Adjacent-literature crosswalk update

最低加入：

- SIGDIAL 2026 dialogue/metacognitive coding；
- PNAS Nexus 2026 complementarity framework；

並重新映射：

- common ground／JPS；
- CCD；
- CoRL／SSRL／HASRL；
- epistemic co-agency；
- Human–AI teaming／complementarity。

### Gate 3 — Freeze discriminant question

預先寫清：

```text
ordinary iterative prompting
vs
adjacent collaboration constructs
vs
CCTS candidate residual
```

並指定什麼結果會：

```text
SUPPORT_CANDIDATE
NARROW
ABSORB_INTO_EXISTING_CONSTRUCT
DOWNGRADE_TO_METHOD_PROFILE
FALSIFY_SPECIFIC_CLAIM
HOLD
```

### Gate 4 — Freeze outcome question

至少區分：

```text
performance
learning
retention
transfer
independent judgement
reconstruction
error detection
calibration
```

### Gate 5 — Empirical readiness

只有在前四個 gate 凍結、真實資料合法取得方式與 privacy／ethics／blind coding／independent scoring 都明確後，才討論真人實證。

```text
UNFROZEN_RESEARCH_QUESTION
!= READY_FOR_CODEX
!= READY_FOR_EMPIRICAL_EXECUTION
```

---

## 10. Explicit non-goals

本 checkpoint 不授權：

- 新 CCTS construct／sub-construct；
- 新 learning construct；
- 修改 canonical CCTS definition；
- 把 CCTS 接入 AI subjectivity evidence chain；
- 真人 participant recruitment；
- 處理私人 transcript 作實證資料；
- merge durable CCTS lane；
- branch deletion；
- main write；
- publication／Zenodo 更新；
- deployment；
- subjectivity／consciousness／phenomenal experience claim promotion。

---

## 11. Claim boundary

```text
DOCUMENTED != VALIDATED
PUBLICATION != EMPIRICAL_VALIDATION
STRUCTURAL_CONFORMANCE != EMPIRICAL_MECHANISM
IMPLEMENTATION != SCIENTIFIC_ESTABLISHMENT
LOCAL_TEST_PASS != REMOTE_CI_PASS
REMOTE_CI_PASS != SCIENTIFIC_VALIDATION
QMS_PASS != HUMAN_LEARNING
AUGMENTATION != SYNERGY
PROVENANCE != CORRECTNESS
AUTHORITY != SCIENTIFIC_TRUTH
CCTS != AI_SUBJECTIVITY_EVIDENCE
```

本輪結論：

```text
CCTS_STRUCTURAL_FRAMEWORK = PRESENT
COLLABORATION_QMS_CONTROLS = PRESENT_ON_DIVERGED_LANE
EMPIRICAL_STUDY_DESIGN = CANDIDATE
CURRENT_LANE_VERIFICATION = UNKNOWN_FOR_EXACT_HEAD
SCIENTIFIC_DISPOSITION = HOLD
```

下一步不是再增加大型構念，而是讓 CCTS 面對更強的近鄰比較、明確的 downgrade/falsification 規則，以及真正獨立的 Human outcome measurement。
