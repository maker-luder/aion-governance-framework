# 本輪執行 HOLD：local checkout byte drift 與 Windows symlink

Document-Class: ENGINEERING_EVIDENCE  
Document-Type: Evidence / execution anomaly record  
Status: HOLD  
Last-Reviewed: 2026-09-10

## 事件與即時決策

基線 QualityFactory 20 passed、IncidentStopController 33 passed；root/control 6 failed、129 passed，exit=1。收到結果後暫停 candidate mutation，唯讀查 traceback、Git refs、core.autocrlf 與 raw bytes。保持 stop，不修改 environment/tests/source hashes、不重複 retry，不做 remote write。報告與保存只在 repository 外的 delivery 目錄。

四個失敗為 WinError 1314，發生於 symlink creation；另外兩個是 `tests/test_owner_research_context.py` 的 AION/ASTRA case，`ValueError: reference content hash mismatch`。

## 可驗證直接原因

Git `ls-files --eol`：`i/lf w/crlf`；`git config --get core.autocrlf`：`true`。

`docs/history/OWNER_LEARNING_CONTEXT_2026_09_03.md`：

| 資料 | 值 |
|---|---|
| baseline raw Git blob bytes | 1195 |
| local worktree bytes | 1218 |
| raw blob SHA-256 | 02d853d0991339d87366abbe1dcae47cc9da01494c23e64eded79c5ea4327065 |
| worktree SHA-256 | 100084e9a1e05ecfea6ccc3c79a79e5ac5b9dcc53195fc3f37602f1e08a5d353 |
| 將 CRLF 在記憶體正規化成 LF 後是否等於 blob | true；沒有把正規化結果寫回檔案 |

本輪取得指令只對 clone 使用 `git -c core.autocrlf=false clone --no-checkout ...`；後續 switch/worktree checkout 繼承了本機 true。這個 temporary config scope 不足是本輪準備缺陷，非使用者未指定全部失敗條件。本地測試誠實拒絕 byte drift，是控制有作用的證據；不是放寬 hash check 的理由。

symlink 權限錯誤則是既存 Windows prerequisites，不以 runtime privilege escalation 來修。更改 repo config／重新 materialize LF／Linux validation 都留作後續有界處置，沒有在這輪停止後暗中執行。

## Quarantine 與驗證邊界

在 baseline test 尚在執行時，候選目錄已產生兩個未 commit 的離線 probe 草稿，並完成 compileall。它們不呼叫 GitHub、不寫檔、不接真 transport；只組合現有 models/controller/factory，演示 failure 與刻意構造的 unbound ablation。不能說「只有計畫、完全無候選寫入」；也不能說候選已完成。

停止後僅允許：讀回草稿、保留完整 bytes/hashes、非寫入式 patch applicability 檢查、外部 archive/rollback verification、產生報告；不推動產品實作、測試修復或新提交。候選完整 targeted/component/root/CI effectiveness 尚未完成。保留 verification.json 的逐命令狀態，不以 baseline pass 欄冒充 candidate pass。

## 後續 gate

本輪結果是 SELF_REVIEW / HOLD，不是 independent IV&V。解除環境 HOLD 應採一次明確計畫：建立 byte-exact baseline/candidate、驗證 hashes、在有適當 symlink 能力的既定測試環境執行現有 tests，再決定候選內容。若需要調整系統權限或實際 host writer，先取得具體處置，而不是自行更動。

```text
LOCAL_BASELINE_ROOT = FAIL
FAILURES = 6
CANDIDATE_FULL_VALIDATION = NOT_PERFORMED
REMOTE_CI = NOT_RUN_FOR_THIS_CANDIDATE
CAPA_EFFECTIVENESS = NOT_VERIFIED
UNEXPECTED_REMOTE_MUTATIONS = 0
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```
