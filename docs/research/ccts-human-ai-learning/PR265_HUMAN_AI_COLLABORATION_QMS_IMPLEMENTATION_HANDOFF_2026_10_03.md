# PR #265 — Human–AI Collaboration QMS 實作交接與操作手冊

狀態：`IMPLEMENTATION_HANDOFF / CLOSED_PR_REFERENCE / DEFERRED_EXECUTION / HUMAN_GATE_REQUIRED`

本文件記錄在 PR #265 的研究工作線中，作為未來 ChatGPT Work（以下稱 Work 小老師）或 Codex 進行 bounded implementation（有界實作）時的可獨立重建交接。它不是 merge 授權、不是重新開啟 PR #265、不是科學驗證，也不是要求未來實作者逐字重演 Human Owner 與 ChatGPT Teacher 的討論方式。

建立本 handoff 時重新核對的 live state：

```text
REPOSITORY = maker-luder/aion-governance-framework
BASE = main
BASE_SHA_AT_HANDOFF_BUILD = 6a34d7780dd6d5bc717cd6c82ba39e7a6241c2fd
PR = #265
PR_STATE_AT_HANDOFF_BUILD = CLOSED / DRAFT / NOT_MERGED
PR_HEAD_AT_HANDOFF_BUILD = 8e22da9396b0dbb9569f09330dad4d704a0355a9
BRANCH = research/ccts-human-ai-learning-lane

MERGE_TO_MAIN = NO
PUBLISH = NO
DEPLOYMENT = FALSE
CANONICAL_EFFECT = NONE
EMPIRICAL_EXPERIMENT_AUTHORIZATION = NO
```

任何未來執行開始前都必須重新讀 live repository。以上 SHA 只代表本 handoff 建立時的來源快照。

## 1. 目的與來源歸屬

`HUMAN_ORIGIN`

Human Owner 指定：把近期跨對話與個人化工作規則中可一般化、可查證、可測試的部分轉化為既有 QMS 的品質控制；允許未來實作者自由發展更好的工程方案，但不可無邊界擴張、不可只複製聊天方法、不可因發現有趣問題就自行長出新研究線。

`AI_FORMALIZATION`

ChatGPT Teacher 將要求形式化為六個候選 Human–AI Collaboration Quality Controls，並將「自由發展但不可亂長」轉成 bounded adaptive implementation contract（有界適應式實作契約）。

`REPOSITORY_STATE`

目前 main 已存在 Full-QMS、ResearchQualityChain、IQC/IPQC/QA、NCR/CAPA、fresh exact-head Human gate、read-before-retry、verify-after-write、unknown-result recovery、actor/surface/provenance separation 等控制。因此本工作不得另造第二套 QMS、第二套 NCR/CAPA 或第二套 research-quality ontology。

```text
PROVENANCE != CORRECTNESS
DISCOVERY != AUTHORIZATION
DESIGN != IMPLEMENTATION
IMPLEMENTATION != VERIFICATION
VERIFICATION != SCIENTIFIC_VALIDATION
VERIFICATION != MERGE_AUTHORITY
```

## 2. 核心設計哲學：自由發展，但不可亂長

未來 Work / Codex 不需要依賴 Human Owner 與 Teacher 的對話順序、措辭或具體解法。應先恢復 repository state，再從既有架構與控制目標出發自行選擇最小充分實作。

允許：

- 發現更合適的既有 class、schema、validator、receipt 或 QMS integration point；
- 判定某控制只需要文件／schema／測試，而不需要新增 runtime code；
- 合併功能重疊的控制，避免重複 ontology；
- 提出比本 handoff 更簡單、可測試、可維護的方案；
- 在不改變控制目的與 authority boundary 的前提下調整檔案位置、命名、資料結構；
- 發現本 handoff 的假設有誤時，保留反例並提出修正；
- 若 current main 已經完整滿足某項要求，以 `NO_NEW_IMPLEMENTATION_REQUIRED` 結案。

不允許：

- 因「有趣」而自行建立新 research construct、心理構念、CCTS 子構念或 subjectivity 主張；
- 把 Human Owner 的個人偏好假裝成 ISO、NIST 或普遍科學規律；
- 新建平行 QMS、平行 NCR/CAPA、平行 provenance ontology；
- 把 UI、prompt、recommendation、agent self-report 或聊天記憶當 live repository authority；
- 為了讓測試通過而降低既有 fail-closed 控制；
- 把工程 PASS 升格為 Human learning、CCTS validity、因果、主體性或其他科學結果；
- 未經新 Human gate 自行擴大 scope、開 empirical experiment、merge、publish 或 deploy。

核心規則：

```text
CONTROL_OBJECTIVE = STABLE
IMPLEMENTATION_METHOD = ADAPTIVE

METHOD_FREEDOM = ALLOWED
EVIDENCE_BACKED_DEVIATION = ALLOWED
REUSE_EXISTING_CONTROL = PREFERRED
NO_NEW_IMPLEMENTATION_REQUIRED = VALID_RESULT

SILENT_SCOPE_EXPANSION = PROHIBITED
NEW_CONSTRUCT_BY_DEFAULT = NO
NEW_RESEARCH_LANE_BY_DEFAULT = NO
AUTHORITY_INHERITANCE = NO

FREE_DEVELOPMENT
!= UNBOUNDED_GROWTH
```

任何偏離本手冊預期實作方式的方案，只要能明確回答下列四題即可進入 review：

1. 解決的是哪一個已批准 control objective？
2. 為什麼 current repository 的既有控制不足？
3. 新方案新增了什麼風險、狀態或 maintenance burden？
4. 哪些測試／反例可以證明它沒有弱化既有 QMS？

答不出來：

```text
-> HOLD
-> DO_NOT_IMPLEMENT
```

## 3. 執行前 live-state recovery

未來實作者不可直接從本文件的 SHA 開始寫。

必做：

```text
LOCK_CURRENT_STATE
-> READ current main exact SHA
-> READ PR #265 current state and branch head
-> READ open / draft / closed-unmerged related PRs
-> READ current Full-QMS implementation + tests
-> READ current provenance / role-separation / stability controls
-> SEARCH for equivalent implementation
-> DIFF intended work against current main
-> DECIDE whether implementation is still needed
```

至少重讀：

- `research-labs/coupled-cognition-quality-factory_v0.1.0/docs/END_TO_END_RESEARCH_QMS.md`
- `research-labs/coupled-cognition-quality-factory_v0.1.0/src/aion_coupled_quality/end_to_end.py`
- `research-labs/coupled-cognition-quality-factory_v0.1.0/src/aion_coupled_quality/extended_quality.py`
- 對應 tests；
- `docs/research/RESEARCH_SESSION_STABILITY_OBSERVATION_PROTOCOL_2026_09_25.md`
- `docs/research/HUMAN_AI_RESEARCH_ROLE_SEPARATION_2026_09_13.md`
- `docs/governance/CHANGE_PROVENANCE_RULES_v0.1.md`
- `docs/governance/PR_TOOL_ROUTING_MATRIX.md`
- 本 PR 的 CCTS / Human–AI Learning 文件。

若 head、branch、PR state 或 main 已改變：

```text
OLD_HEAD_VERIFICATION = INVALID_FOR_NEW_HEAD
READ_LIVE_STATE_AGAIN
```

## 4. 本次 QMS control objectives

### 4.1 Human Assimilation and Review Capacity Gate
（人類吸收與審閱容量閘門）

目的：避免把 AI 產出速度、已顯示內容或 Human 看過內容誤當成 Human 已理解、審查或可獨立使用。

最低語意：

```text
AI_OUTPUT_THROUGHPUT != HUMAN_ASSIMILATION_RATE

OUTPUT_DELIVERED
!= OUTPUT_UNDERSTOOD
!= OUTPUT_REVIEWED
!= OUTPUT_APPROVED
!= HUMAN_CAN_INDEPENDENTLY_USE

HUMAN_REVIEW_CAPACITY_EXCEEDED
-> HOLD_OR_PHASE_BREAK

HUMAN_ASSIMILATION_STATE = UNKNOWN
-> NO_HIGH_IMPACT_TRANSITION
```

工程要求：

- 不量化 Human worth（人的價值）；
- 不把閱讀時間直接當 assimilation；
- 不虛構心理狀態；
- 可以只記錄 review-state／acknowledgement／hold state，不必建立心理模型；
- 高影響 transition 必須有清楚 Human gate，而不是推定「使用者沒反對＝已理解」。

### 4.2 Independent Remediation / Scaffolding Gate
（獨立修復／鷹架閘門）

目的：已知 executor 發生可識別 defect 後，不可只把原封不動的任務重新丟回同一 executor。

最低語意：

```text
EXECUTOR_DEFECT_DETECTED
-> STOP_BLIND_REEXECUTION
-> INDEPENDENT_REVIEW
-> IDENTIFY_EXACT_ERROR_POINT
-> IDENTIFY_VIOLATED_REQUIREMENT
-> UPDATE_HANDOFF_OR_TEST
-> BOUNDED_REEXECUTION

UNCHANGED_SPEC
+ SAME_EXECUTOR
+ KNOWN_FAILURE_MODE
-> PROHIBITED_BLIND_RETRY
```

這是 remediation quality control，不代表必須更換 vendor / model / product。若同一 executor 在修正版規格與新增負向測試下重新執行，可以是合法 bounded retry。

```text
INDEPENDENT_REVIEW != INDEPENDENT_IVV
REVIEW_SCAFFOLD != IMPLEMENTATION
CAPA_EXISTS != SAFE_TO_REPEAT_UNCHANGED_TASK
```

### 4.3 Prompt / Recommendation / Authority Separation
（提示／建議／權限分離）

最低語意：

```text
CHAT_CONTEXT != LIVE_REPOSITORY_STATE
SUGGESTED_PROMPT != LIVE_STATE
RECOMMENDATION != AUTHORIZATION
UI_STATE != REPOSITORY_STATE
HANDOFF_TEXT != EXECUTION_RECEIPT
OLD_SHA != CURRENT_SHA
OLD_VERIFICATION != CURRENT_VERIFICATION
```

實作者應優先擴充既有 provenance / authority control，而不是另建 permission system。

### 4.4 Human Reviewability + Bilingual Semantic Parity
（人類可審閱性＋雙語語意一致性）

此控制是本 repository 的 Human Owner review requirement，不宣稱為 universal standard。

最低語意：

```text
TECHNICALLY_CORRECT != HUMAN_REVIEWABLE
TRANSLATION_PRESENT != SEMANTIC_PARITY
CODE_EXECUTABLE != CODE_HUMAN_REVIEWABLE
```

要求：

- material research / governance change 應提供 Human Owner 可審閱的繁體中文說明；
- code/schema/enum 可保留英文 identifier，但需有可追溯中文解釋；
- 關鍵英文術語第一次出現時保留原文＋中文意思；
- 不要求每一行 source code 都機械式雙語複製；
- 中英版本若都屬 normative／governance surface，必須檢查 semantic parity（語意一致），避免一邊多權限、一邊少限制。

### 4.5 Research Output and Scope-Growth Disposition
（研究結果與範圍成長處置）

目的：讓 negative / null / rejected 結果可以正常結案，而不是每次都長出新研究線。

允許的結果應至少能表達：

```text
SUPPORTED_CANDIDATE
NARROWED
FALSIFIED
REJECTED
INCONCLUSIVE
SUPERSEDED
ABSORBED_INTO_EXISTING_CONSTRUCT
NO_IMPLEMENTATION_REQUIRED
```

不強迫建立新 enum；優先重用既有 vocabulary，必要時只做 mapping。

硬邊界：

```text
FAILED_HYPOTHESIS != FAILED_RESEARCH
NEGATIVE_RESULT != PERMISSION_TO_EXPAND_SCOPE
NEW_INTERESTING_QUESTION != AUTHORIZED_SCOPE_GROWTH

SCOPE_GROWTH
-> RE_ADMISSION
-> HUMAN_REVIEW
```

### 4.6 Branch Retirement / Provenance Preservation Gate
（分支退役／來源保存閘門）

目的：branch cleanup 不可把 unique history、research provenance 或 authority evidence 一起清掉。

最低流程：

```text
PRESERVE
-> VERIFY
-> DELETE
```

至少檢查：

- branch commits 是否已 reachable from retained history；
- 是否存在 unique history；
- 是否需要 tag / archive ref / disposition record；
- surviving reconstruction path 是否足以重建研究與 authority provenance；
- unknown history value 必須 HOLD。

```text
BRANCH_CLOSED != PROVENANCE_DISPOSABLE
PR_CLOSED != RESEARCH_VALUE_ZERO
DELETE != HISTORY_REWRITE
UNKNOWN_HISTORY_VALUE -> HOLD
```

此控制不得自動授權 branch deletion；真正刪除仍屬另一步 repository operation。

## 5. 建議 integration 位置，但不是硬編碼

Work / Codex 必須先做 dedup。若 current main 仍相同，優先檢查以下位置能否承載控制：

```text
research-labs/coupled-cognition-quality-factory_v0.1.0/
  src/aion_coupled_quality/end_to_end.py
  src/aion_coupled_quality/extended_quality.py
  src/aion_coupled_quality/provenance.py
  tests/test_end_to_end_quality.py
  tests/test_extended_quality.py
  docs/END_TO_END_RESEARCH_QMS.md

docs/governance/
docs/quality/
docs/research/
```

但：

```text
EXPECTED_FILE_LIST != REQUIRED_FILE_LIST
```

若實作者找到更乾淨的既有 control surface，可以改位置；final report 必須說明原因。

禁止建立：

- `QMS_v2` 或平行 Full-QMS；
- 第二套 NCR/CAPA engine；
- 第二套 contribution/provenance ontology；
- 僅為 PR #265 特製、無法回到通用 QMS 的 CCTS-only quality engine；
- 心理學式 Human assimilation score；
- 自動 merge/release/experiment authority。

## 6. 實作順序

### Gate A — dedup / necessity review

先產出一張 control-to-existing-implementation matrix：

```text
CONTROL
CURRENT_EXISTING_CONTROL
GAP
REUSE_PATH
NEW_CODE_NEEDED = YES | NO | PARTIAL
RISK_OF_DUPLICATION
```

若六項中有一項 current main 已完整覆蓋，標：

```text
NO_NEW_IMPLEMENTATION_REQUIRED
```

不得為了「有實作」而新增空殼。

### Gate B — tests first where executable behavior changes

有 code 行為的控制先寫最小 failing / negative tests，再實作。

測試至少涵蓋：

1. Human review state 未知時，高影響 transition fail closed；
2. output delivered 不會自動等同 reviewed / approved；
3. known executor defect + unchanged handoff 不得 blind retry；
4. updated remediation specification 可以重新進場，但不繼承舊 PASS；
5. recommendation / prompt / self-report 不得產生 authority；
6. stale SHA / stale verification 不得被 current transition 接受；
7. negative research disposition 不會自動建立新 scope；
8. branch provenance unknown 時不得標成 safe-to-delete；
9. bilingual governance surface 的語意要求可被靜態或 fixture 檢查時，加入 mismatch negative test；
10. 所有新 PASS 都不得升格 scientific validity / merge authority。

### Gate C — minimal implementation

只做到讓 Gate B 的控制可測、可 fail closed。

```text
MINIMUM_SUFFICIENT_IMPLEMENTATION = PREFERRED
FRAMEWORK_GROWTH_FOR_ITS_OWN_SAKE = REJECT
```

### Gate D — integration

將新控制接到既有 QMS / governance flow，而不是獨立旁路。

候選概念關係：

```text
SOURCE_IQC
-> DESIGN_ADMISSION
-> HUMAN_AI_COLLABORATION_QUALITY_CONTROLS
-> PREREGISTRATION
-> EXECUTION_INTEGRITY
-> EVIDENCE_REVIEW
-> COUNTEREVIDENCE_REVIEW
-> CLAIM_CEILING_REVIEW
-> FINAL_QA
-> HUMAN_REVIEW_BOUNDARY
```

此圖是設計方向，不要求一定新增名為 `HUMAN_AI_COLLABORATION_QUALITY_CONTROLS` 的 class。

### Gate E — documentation and reviewability

更新必要文件，說清楚：

- control objective；
- provenance；
- reuse / no-duplication；
- fail-closed semantics；
- nonclaims；
- 中文可審閱說明；
- 哪些部分是 Human Owner-origin、AI formalization、joint synthesis、repository state。

### Gate F — verify exact head

任何寫入後：

```text
VERIFY_AFTER_WRITE = TRUE
```

若 transport / stream 中斷：

```text
UNKNOWN_RESULT
-> READ_LIVE_STATE
-> ESTABLISH_EXACT_STATE
-> CONTINUE_OR_RETRY
```

禁止 duplicate write。

## 7. Scope-growth budget

Work / Codex 可自由發現問題，但本輪只有以下三種處置：

```text
A. IN_SCOPE_DEFECT
   -> fix if required for the six controls

B. ADJACENT_DEFECT
   -> record as deferred finding
   -> do not expand implementation

C. NEW_RESEARCH_QUESTION
   -> record question + evidence
   -> no implementation
   -> Human review required
```

如果發現第七個控制，預設：

```text
CONTROL_7 = DEFERRED_CANDIDATE
IMPLEMENTATION = NO
```

除非第七項其實是完成前六項不可缺的 invariant，而不是新的研究／產品能力。實作者必須在 final report 明示判斷。

## 8. Acceptance criteria

本 handoff 的未來實作只有在下列條件全部可檢查時，才可回報 `READY_FOR_HUMAN_REVIEW`：

- live-state recovery 有 exact main SHA、working branch、exact implementation head；
- 六項 control 各自有 `REUSED / IMPLEMENTED / PARTIAL / NO_NEW_IMPLEMENTATION_REQUIRED` disposition；
- 沒有第二 QMS / NCR-CAPA / provenance ontology；
- executable change 有相應 negative-path tests；
- stale state、blind retry、silent authority promotion 均 fail closed；
- Human reviewability control 不推定 Human 心理狀態；
- bilingual control 不要求機械式逐行雙寫，但 normative semantics 不得漂移；
- negative / inconclusive result 可結案而不觸發 scope growth；
- branch retirement control 不執行未授權 deletion；
- existing CCTS / Human–AI Learning scientific holds 沒有被改寫；
- local tests、static checks 與 relevant package suite 已執行；
- remote CI 必須以 exact new head 重新判定；舊 head PASS 不得沿用；
- final report 保留 unresolved defects、deferred findings、counterexamples；
- Human Owner 尚未明確授權的 transition 仍保持 HOLD。

## 9. Verification contract

最低本地驗證由實作者依實際 changed surface 決定，但至少包含：

```text
targeted tests for every changed control
relevant package test suite
mypy --strict for changed Python surface where repository policy applies
ruff / repository static checks where applicable
compile / import sanity where applicable
documentation / internal-link checks where applicable
```

若改動 Full-QMS：

- 跑 coupled-cognition-quality-factory 的 relevant full package tests；
- 不得只跑新增 tests；
- 檢查 existing receipt / risk / TEVV / security integration regression；
- 檢查 existing NCR/CAPA 與 claim-withdrawal semantics 未被取代。

```text
LOCAL_TEST_PASS != REMOTE_CI_PASS
CI_PASS != SCIENTIFIC_VALIDATION
TEST_COUNT != TEST_QUALITY
```

## 10. Authority boundary

本文件提供 implementation map，不提供 execution/merge authority 的永久繼承。

未來若 Human Owner 明確要求 Work / Codex「依本 handoff 實作」，可在該次指令的 scope 內執行 bounded implementation；但以下仍需各自 fresh decision：

```text
EMPIRICAL_HUMAN_STUDY
MERGE_TO_MAIN
PUBLICATION
RELEASE
DEPLOYMENT
NEW_RESEARCH_LANE
DESTRUCTIVE_BRANCH_CLEANUP
```

PR #265 保持歷史狀態，除非 Human Owner 另有明確要求：

```text
PR_265_CLOSED = PRESERVE
PR_265_REOPEN = NO_BY_THIS_HANDOFF
PR_265_MERGE = NO_BY_THIS_HANDOFF
```

## 11. Work / Codex final report contract

實作完成後必須回報：

```text
REPOSITORY
BASE_SHA_AT_START
IMPLEMENTATION_BRANCH
FINAL_EXACT_HEAD

LIVE_STATE_RECOVERY
DEDUP_RESULT

CONTROL_1_DISPOSITION
CONTROL_2_DISPOSITION
CONTROL_3_DISPOSITION
CONTROL_4_DISPOSITION
CONTROL_5_DISPOSITION
CONTROL_6_DISPOSITION

FILES_CHANGED
TESTS_ADDED
TESTS_RUN
LOCAL_RESULTS
REMOTE_CI_RESULTS_OR_NOT_VERIFIED

REUSED_EXISTING_CONTROLS
NEW_IMPLEMENTATION
NO_NEW_IMPLEMENTATION_REQUIRED_ITEMS

ADJACENT_DEFECTS_DEFERRED
NEW_RESEARCH_QUESTIONS_DEFERRED
COUNTEREXAMPLES
UNRESOLVED_RISKS

SCIENTIFIC_CLAIMS_CHANGED = NO
AUTHORITY_CHANGED = NO
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE

READY_FOR_HUMAN_REVIEW = YES | NO
MERGE_AUTHORIZATION = NONE
```

不得只回報「全部完成」「全綠」或測試數量。

## 12. 反向審查問題

在交給 Human Owner + ChatGPT Teacher 複審前，實作者必須主動問自己：

1. 我是不是因為手冊寫了六項，就硬造六個新 class？
2. 我是不是把 Human 的 review state 誤寫成心理狀態？
3. 我是不是把「同一 executor 再做一次」一律禁止，而忽略修正版 handoff 可以 bounded retry？
4. 我是不是把 recommendation / self-report 偷變成 authority？
5. 我是不是把雙語要求做成大量重複 source code，而不是提升 Human reviewability？
6. 我是不是讓 negative result 自動長成新研究線？
7. 我是不是把 closed branch 當成可以直接刪除的垃圾？
8. 我是不是把 PR #265 的 CCTS 工作線誤變成通用 QMS 的唯一來源？
9. 我是不是沿用了舊 head 的 tests / CI / review？
10. 我是不是增加了 implementation complexity 卻沒有增加 discrimination / safety / traceability？

任一答案為「是」：

```text
-> STOP
-> RE-SCOPE
-> FIX BEFORE HUMAN REVIEW
```

## 13. 最終邊界

這個 handoff 的目的不是把 Human Owner 與 Teacher 的合作方式固化成唯一正確方法，而是把已觀察到的品質問題轉成可檢查的約束，讓未來實作者在約束內自主尋找更好的工程解。

```text
CHAT_METHOD != REQUIRED_IMPLEMENTATION_METHOD
CONTROL_OBJECTIVE != ONE_FIXED_SOLUTION

AUTONOMY_WITHIN_BOUNDARIES = ALLOWED
EVIDENCE_BACKED_EVOLUTION = ALLOWED
COUNTEREXAMPLE_DRIVEN_REVISION = ALLOWED

SILENT_SCOPE_GROWTH = NO
AUTHORITY_DRIFT = NO
ONTOLOGY_PROLIFERATION = NO
SCIENTIFIC_OVERCLAIM = NO

FREE_DEVELOPMENT
+ BOUNDED_SCOPE
+ LIVE_STATE_RECOVERY
+ TESTABLE_CONTROLS
+ HUMAN_GATE
= TARGET_IMPLEMENTATION_MODE
```
