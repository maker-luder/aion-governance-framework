# Four durable branches policy｜固定四支分支規則

狀態：`PROPOSED_CANONICAL_CONTROL`，須由 PR #264 的精確 head 通過既有 main-transition Human gate 並合併後生效。

## 1. 長期拓樸

倉庫的穩定狀態固定只有四個 live branch（仍存在於 GitHub Branches 清單中的分支）：

1. `main` — AI 主體性可能性長期核心與跨線治理基底。
2. `research/ccts-human-ai-learning-lane` — CCTS／Human–AI learning／collaboration。
3. `research/embodiment-lane` — 獨立具身研究與工程候選。
4. `research/legacy-uncertainty-hold` — 尚未能可靠分類的臨時來源與恢復索引；不是第四個科學構念。

規則由 [`.github/branch-topology-policy.json`](../../../.github/branch-topology-policy.json) 機器可讀地固定。增加第五個**長期** branch、改名、移除任一固定 branch，皆須先修改 policy、走獨立 PR、通過既有 Human exact-head authority gate；分支建立本身不構成核准。

## 2. PR 所需的短期 branch

四支穩定拓樸不能取消 code review，因此容許多個 transient branch（短期工作分支）並行。`maximum_open_pr_branches = null` 代表不設定同時 open PR branch 的數量硬上限；這不改變 durable branch 固定為四支的規則：

- 必須是同倉庫 open PR 的 head；沒有 open PR 的額外 branch 立即違規。
- 名稱只允許 `work/`、`docs/`、`fix/`、`feat/`、`governance/`、`quality/` 或 `review/` 前綴。
- 多個 transient branch 可同時存在，只要每一支都是同倉庫 open PR 的 head 且符合允許前綴；數量本身不構成違規。
- PR 關閉或合併時只啟動唯讀 retirement assessment。非 durable 加上 SHA 相同只證明分支未漂移，不是刪除許可。merged 與 closed-unmerged 分別分類，兩者皆保持 HOLD。
- PR 分支是運輸／審查載體，不是第五條研究線；工作完成後穩定狀態必須回到四支。

需要並行工作時，可以各自使用合法 transient branch + open PR；這些 branch 仍是短期審查載體，不因此升格為 durable branch。PR 完成後可依 retirement／保存程序批次清理。

## 3. 可回復清理

刪除舊 branch ref 前必須依序完成：

1. 重新讀取 live branch exact head。
2. 建立 `archive/branch-heads/YYYY-MM-DD/<original-branch>` tag，tag 必須指向完全相同的 commit。
3. 建立完整 `git bundle` 與 SHA-256 manifest，並執行 `git bundle verify`。
4. 檢查沒有 open PR 以該 branch 為 head，且 branch 不是四支固定分支。
5. 核對與本次 branch、exact SHA、保存及重建狀態綁定的獨立、新鮮 Human 刪除授權；合併授權不是刪除授權。
6. 刪除前立即重讀並重驗 head、保存及授權；以 `branch + expected SHA` 的原子 lease 執行。先 GET 再無條件 HTTP DELETE 存在競態，不滿足此要求。
7. 刪除後重讀 branches 與 tags，確認穩定拓樸及恢復指標。

上述是未來破壞性執行必須滿足的條件；本次 remediation 不執行分支刪除，也沒有啟用這條執行路徑。

Tag 保存 commit history 與原分支名稱的對應，但不賦予該歷史 main 採納、科學效度、出版或 merge authority。需要恢復時，從精確 tag 建立新候選 branch，仍須走當時的研究／治理審查；禁止用 force push 改寫四支固定分支。

## 4. 自動化與失敗語意

- `scripts/validate_branch_topology.py` 以 GitHub live API 檢查 fixed set、open-PR 關聯、允許前綴，以及 policy 可選的數量上限；目前 `maximum_open_pr_branches=null`，因此不設 hard cap。也支援固定輸入檔供離線測試。
- `.github/workflows/branch-topology-governance.yml` 在 branch 刪除、PR 事件、每日排程與手動觸發時檢查。刻意不在 branch `create` 瞬間 fail，避免合法 branch 尚未來得及建立 PR 時產生短暫假紅燈；若 branch 最終沒有 open PR，仍會在排程／手動巡檢中被判違規。關閉同倉庫 PR 時只執行唯讀 assessment，token 僅 `contents: read`。不從 PR ref 直接插值組合 shell 指令。
- `Quality` 亦執行 live topology check，使不合規拓樸不能被誤報為完整 Quality pass。
- API、權限、資料格式或 exact-head 核對失敗時，retirement 為 `HOLD`（exit 10）；一般拓樸驗證為 `ERROR`／`FAIL`，不是默認通過。
- 相容欄位 `delete_after_pull_request_close=true` 表示「嘗試 guarded retirement assessment」，不表示 PR 關閉即刪除。舊 `--delete-closed-pr-head` 參數回傳 HOLD，沒有網路寫入；HTTP helper 限制為 GET，舊 DELETE transport 已移除。
- HOLD 可能保留第五支已關閉 PR branch，使 topology check 顯示 FAIL；保存與授權優先，禁止為了變綠而刪除。workflow 即使 assessment HOLD 仍執行最後的唯讀拓樸讀回。

```text
FOUR_DURABLE_BRANCHES = REQUIRED
UNASSOCIATED_EXTRA_BRANCH = FAIL
MORE_THAN_ONE_TRANSIENT_BRANCH = ALLOWED_WHEN_EACH_IS_OPEN_PR_ASSOCIATED
OPEN_PR_TRANSIENT_HARD_CAP = NONE
CLOSED_PR_TRANSIENT_BRANCH = READ_ONLY_RETIREMENT_ASSESSMENT
RETIREMENT_READINESS != BRANCH_DELETE_AUTHORITY
DELETE_EXECUTION = DISABLED_PENDING_VERIFIED_AUTHORITY_ADAPTER
ARCHIVE_TAG = RECOVERY_POINTER
ARCHIVE_TAG != CANONICAL_PROMOTION
CI_PASS != HUMAN_MERGE_AUTHORITY
```

## 5. 權限邊界

本規則控制 repository topology，不改變各研究線的科學主張上限。`main` 的合併仍受 `MAIN_TRANSITION_AUTHORITY_GATE.md` 約束；Quality、CodeQL 或 topology pass 都不替代當前 exact-head Human Owner 決定。

## 6. Teacher blocker remediation 與剩餘閘門

現有 `validate_main_transition_authority.py` 綁定 `MERGE_PR_INTO_MAIN`，不支援把其 receipt 轉成 branch deletion authority。既有 workbench 的 `DESTRUCTIVE_CHANGE` grant 是本機 task-bound 結構驗證，尚無 live GitHub branch retirement 的可信授權來源接線；本輪不把 caller JSON、prompt、review 文字、UI、handoff、workflow event、舊核准或 agent 自述視為這條接線。

因此採較嚴格的隔離修正：

- `assess_closed_pr` 驗證 live closed PR 的 repository／number／branch／SHA 與 merged boolean。
- 以 reviewed head 對每個 durable exact head 的 ancestry comparison 判定 reachability；squash／rebase 的 merged 標記不當作可達證據。
- 讀取 `refs/tags/archive/branch-heads/pr-<number>/<exact-head>` 並要求 lightweight commit tag 的 SHA 完全相同；tag 缺失、錯誤、碰撞、annotated tag 或 lookup failure 均 HOLD，不建立或覆寫 tag。
- live tag 存在不等於 bundle 可重建；history classification、bundle/reconstruction verification、verification receipt 在尚未獨立驗證時維持未知／缺失。
- 即使傳入完整保存證據，pure assessment 最多報 `preservation_readiness=READY`，整體仍為 `HOLD`、`deletion_authority=NONE`、`mutation_performed=false`。此 READY 僅是輸入條件檢查，不是外部證据真實性的驗證或執行 capability。

**尚待 Teacher 複審的明確差額：** 本輪封閉了弱刪除路徑，但沒有完成 review §9.13／§10 的「有效獨立授權後刪除一次」正向執行路徑。正向測試只驗證完整保存資料達到 readiness 仍維持 authority HOLD。沒有宣稱完整自動 retirement 已可用；後續接入可信刪除 authority、可重建驗證與原子 exact-SHA deletion transport，須另經 bounded 設計／審查，不能用 fake grant 代替正式接線。

PR #265 的 direct-construction promotion blocker 未在本輪修正，也未引用其 assessment 當作 authority。別名 negative-control 的方法學命名亦維持 deferred。PR #264 保持 OPEN／DRAFT／NOT_MERGED，交回 Teacher 決定這個較強的 HOLD 隔離是否足以解除目前 blocker，或指定後续 adapter 的可信來源。
