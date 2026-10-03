# PR #265 — Human–AI collaboration QMS 去重與架構決策

狀態：`BOUNDED_IMPLEMENTATION / CLOSED_PR_BRANCH / HUMAN_REVIEW_REQUIRED`

本文件是繁體中文 Human Owner review surface。英文 identifier 是可執行介面；本文件提供其控制目的、來源、重用邊界與非主張。這不是 CCTS 科學驗證，也不改寫 canonical CCTS definition。

## Live state 與任務邊界

實作前重新取得的狀態：

```text
MAIN = 6a34d7780dd6d5bc717cd6c82ba39e7a6241c2fd
PR_265 = CLOSED / DRAFT / NOT_MERGED
BRANCH = research/ccts-human-ai-learning-lane
RECONCILED_BRANCH_HEAD = c3cdad31f13323a767a5bccf8a61787c067b3903
PR_CLOSED_DIFF_HEAD = 8e22da9396b0dbb9569f09330dad4d704a0355a9
```

closed PR 的歷史 diff head 與仍存續的 branch head 必須分開報告。舊 head 的 CI 不轉移到新 head。

本輪研究仍只有一條 active falsification path：`alias recall != problem-space reconstruction`。本文件的 QMS 控制是工程品質門檻，不新增第二條研究假說，不實作 F-M7..F-M12。

## Actual gap

既有 Full-QMS 已有 quality plan、measurement assurance、content-addressed receipts、NCR/CAPA、claim withdrawal、audit、management review、固定 scientific/merge/canonical/deployment ceilings。缺口不是第二套 QMS，而是六個 Human–AI collaboration control objectives 尚無一個可一起 fail closed、產生 trace ref、並被 `FullQualitySystemEngine` 消費的 executable surface。

## Control-to-existing-implementation matrix

| CONTROL | CURRENT_EXISTING_CONTROL | GAP | REUSE_PATH | NEW_CODE_NEEDED | RISK_OF_DUPLICATION | DISPOSITION |
|---|---|---|---|---|---|---|
| 1. Human Assimilation and Review Capacity | `ManagementReviewRecord`、Human review boundary、固定 `READY_FOR_HUMAN_REVIEW != authority` | delivered / reviewed / approved / independently usable 尚未分離；unknown review state 未直接阻擋 high-impact transition | 只記錄 review state、capacity hold 與 explicit Human gate；不建立心理量表 | PARTIAL | 若量化 assimilation 會形成心理模型 | IMPLEMENTED；重用 Human review boundary |
| 2. Independent Remediation / Scaffolding | 既有 NCR/CAPA、audit independence、negative tests | 已知 defect 後，同 executor + unchanged handoff 的 blind retry 未被直接拒絕；舊 PASS 可能被誤繼承 | NCR/CAPA 不變；新增 retry admission record，要求 error、violated requirement、independent review、updated handoff 與 negative test | PARTIAL | 若另建 CAPA engine 會重複 | IMPLEMENTED；未建立第二 CAPA |
| 3. Prompt / Recommendation / Authority Separation | content-addressed receipts、configuration refs、management review 不授權 merge | prompt / recommendation / self-report / UI / handoff 與 live Human authorization 尚未形成同一 fail-closed discriminator；stale SHA 未在此 surface 比對 | 重用 repository SHA 與 verification ref；僅 `LIVE_HUMAN_AUTHORIZATION` 可作 transition authority evidence | PARTIAL | 若另建 permission system 會權限漂移 | IMPLEMENTED；不授予 transition |
| 4. Human Reviewability + Bilingual Semantic Parity | repository bilingual documents、Human review requirement | material governance change 的繁中 review ref 與雙 normative surface parity 尚未可檢查 | 記錄繁中說明 ref、英文 governance ref 與 parity verification；不逐行雙語化 source | PARTIAL | 機械雙寫會增加漂移面 | IMPLEMENTED；只檢查 review evidence |
| 5. Research Output and Scope-Growth Disposition | claim quality 的 `HOLD/REVISED/WITHDRAWN`、negative-result retention、claim ceiling | handoff 的 disposition mapping 與 `scope growth -> readmission + Human review` 尚未同時可測 | 重用既有 claim ontology；新增 bounded mapping enum 與 scope gate，不自動建新 lane | PARTIAL | 新增第二 claim ontology | IMPLEMENTED as mapping；negative 可正常結案 |
| 6. Branch Retirement / Provenance Preservation | non-destructive claim withdrawal、closed-PR registry、Git history | branch-level `PRESERVE -> VERIFY -> DELETE` readiness 尚未可測；unknown history 需 HOLD | 只記錄 reachable/unique/preservation/verification/reconstruction evidence；永遠不授予 delete authority | PARTIAL | 將 claim withdrawal 誤當 branch deletion | IMPLEMENTED；deletion 仍需獨立權限 |

六項都不是 `NO_NEW_IMPLEMENTATION_REQUIRED`，但每項都有可重用 ancestry，因此只新增一個小型 control module 與 Full-QMS consumer seam。

## Architecture chosen

```text
HumanAICollaborationQualityControls
-> assess_human_ai_collaboration_controls(...)
-> HumanAICollaborationQualityAssessment
-> ExtendedQualityControls.human_ai_collaboration
-> FullQualitySystemEngine
-> READY_FOR_HUMAN_REVIEW | HOLD
```

### Why code instead of docs only

手冊列出的風險包含 stale SHA、blind retry、silent authority promotion、unknown branch history 與 negative-result scope growth。這些都是可判定輸入與明確 fail-closed outcome；只寫文件無法提供回歸測試。因此新增最小 typed records、deterministic evaluator 與 negative tests。

### Rejected routes

1. **直接擴張 `EndToEndQualitySystemEngine.assess` 的必填參數**：拒絕。所有研究 QMS 不一定都是 Human–AI collaboration，強制改變既有 caller 會擴大回歸面。
2. **建立 `QMS_v2`、第二套 permission/NCR/CAPA/provenance ontology**：拒絕。與 existing Full-QMS 重複。
3. **六個 control 各建一個 engine**：拒絕。增加形式複雜度，沒有增加 discrimination。
4. **documentation-only**：拒絕。無法測試手冊要求的 fail-closed behavior。
5. **把 F-M7 negative-result escalation 一併實作**：本輪拒絕。會違反 `ONE_ACTIVE_FALSIFICATION_PATH`，而舊 alias-reconstruction 反證 pass 已進入完成與驗證階段。

## Reuse boundary

- `FullQualitySystemEngine` 仍是唯一整合引擎。
- `ExtendedQualityControls.trace_refs()` 將 collaboration assessment 的 `control_id` 納入 management-review trace completeness。
- collaboration assessment 為可選：非 Human–AI collaboration 的既有 QMS caller 不受破壞；一旦提供，`HOLD` 必須使 Full-QMS `HOLD`。
- 新 result 固定：`scientific_disposition=HOLD`、`merge_authority=NONE`、`canonical_effect=NONE`、`deployment=False`、`branch_delete_authority=NONE`。
- record 的 `LIVE_HUMAN_AUTHORIZATION` 只是目前授權證據類別，不是此 evaluator 自行創造權限；最終 transition 仍由現行 repository governance 決定。

## Provenance roles

- **HUMAN_PARTICIPANT / Human Owner origin**：要求可審閱繁中 surface、容量界線、舊任務完成、新 handoff 實作。
- **CHATGPT_TEACHER formalization**：六項 control objectives、acceptance tests、scope-growth budget 與 final-report contract。
- **CHATGPT_WORK / CODEX implementation**：去重、typed data model、fail-closed evaluator、Full-QMS integration 與測試設計。
- **REPOSITORY STATE**：既有 QMS、NCR/CAPA、claim withdrawal、receipt、authority ceiling 與 closed-PR history。

## Counterexamples and known risks

- `review_state=APPROVED` 只是有記錄的 workflow state，不證明實際理解。
- `independent_review_ref` 是 trace evidence，不等於 independent IV&V。
- `semantic_parity_verified=True` 是可稽核聲明，不是自動自然語言等價證明；若未來有兩份 normative fixture，可另加 content-level validator。
- branch commits reachable 仍不代表 branch 可刪；本 module 永遠不授權 deletion。
- same executor 在 updated handoff、independent review、exact error、violated requirement、negative tests 下可 bounded retry；仍必須 fresh verify，不能繼承舊 PASS。

## Scientific and authority ceiling

```text
TEST_PASS != HUMAN_COMPREHENSION
READY_FOR_HUMAN_REVIEW != APPROVAL
INDEPENDENT_REVIEW != INDEPENDENT_IVV
NEGATIVE_RESULT != SCOPE_GROWTH_AUTHORITY
RETIREMENT_READINESS != BRANCH_DELETE_AUTHORITY
QMS_PASS != CCTS_VALIDATION

SCIENTIFIC_CLAIMS_CHANGED = NO
AUTHORITY_CHANGED = NO
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```
