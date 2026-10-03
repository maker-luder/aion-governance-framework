# Four durable branches policy｜固定四支分支規則

狀態：`PROPOSED_CANONICAL_CONTROL`，須由 PR #264 的精確 head 通過既有 main-transition Human gate 並合併後生效。

## 1. 長期拓樸

倉庫的穩定狀態固定只有四個 live branch（仍存在於 GitHub Branches 清單中的分支）：

1. `main` — AI 主體性可能性長期核心與跨線治理基底。
2. `research/ccts-human-ai-learning-lane` — CCTS／Human–AI learning／collaboration。
3. `research/embodiment-lane` — 獨立具身研究與工程候選。
4. `research/legacy-uncertainty-hold` — 尚未能可靠分類的臨時來源與恢復索引；不是第四個科學構念。

規則由 [`.github/branch-topology-policy.json`](../../.github/branch-topology-policy.json) 機器可讀地固定。增加第五個**長期** branch、改名、移除任一固定 branch，皆須先修改 policy、走獨立 PR、通過既有 Human exact-head authority gate；分支建立本身不構成核准。

## 2. PR 所需的短期 branch

四支穩定拓樸不能取消 code review，因此容許同時最多一個 transient branch（短期工作分支）：

- 必須是同倉庫 open PR 的 head；沒有 open PR 的額外 branch 立即違規。
- 名稱只允許 `work/`、`docs/`、`fix/`、`feat/`、`governance/`、`quality/` 或 `review/` 前綴。
- 第二個同時存在的 transient branch 立即違規。
- PR 關閉或合併時，workflow 只在 branch 仍是經審查 exact SHA、且不屬四支固定分支時刪除；若 SHA 移動則 fail closed，不刪除。
- PR 分支是運輸／審查載體，不是第五條研究線；工作完成後穩定狀態必須回到四支。

需要並行工作時，使用本地 worktree、fork 或依序排隊，不以多條長期 remote branch 代替工作管理。

## 3. 可回復清理

刪除舊 branch ref 前必須依序完成：

1. 重新讀取 live branch exact head。
2. 建立 `archive/branch-heads/YYYY-MM-DD/<original-branch>` tag，tag 必須指向完全相同的 commit。
3. 建立完整 `git bundle` 與 SHA-256 manifest，並執行 `git bundle verify`。
4. 檢查沒有 open PR 以該 branch 為 head，且 branch 不是四支固定分支。
5. 使用 `branch + expected SHA` 的 lease 式刪除；任何 head 漂移都停止。
6. 刪除後重讀 branches 與 tags，確認穩定拓樸及恢復指標。

Tag 保存 commit history 與原分支名稱的對應，但不賦予該歷史 main 採納、科學效度、出版或 merge authority。需要恢復時，從精確 tag 建立新候選 branch，仍須走當時的研究／治理審查；禁止用 force push 改寫四支固定分支。

## 4. 自動化與失敗語意

- `scripts/validate_branch_topology.py` 以 GitHub live API 檢查 fixed set、open-PR 關聯與 hard cap；也支援固定輸入檔供離線測試。
- `.github/workflows/branch-topology-governance.yml` 在 branch 建立／刪除、PR 事件、每日排程與手動觸發時檢查；關閉同倉庫 PR 時執行 guarded cleanup。
- `Quality` 亦執行 live topology check，使不合規拓樸不能被誤報為完整 Quality pass。
- API、權限、資料格式或 exact-head 核對失敗時狀態是 `ERROR`／`FAIL`，不是默認通過。

```text
FOUR_DURABLE_BRANCHES = REQUIRED
UNASSOCIATED_EXTRA_BRANCH = FAIL
MORE_THAN_ONE_TRANSIENT_BRANCH = FAIL
CLOSED_PR_TRANSIENT_BRANCH = DELETE_IF_EXACT_HEAD_UNCHANGED
ARCHIVE_TAG = RECOVERY_POINTER
ARCHIVE_TAG != CANONICAL_PROMOTION
CI_PASS != HUMAN_MERGE_AUTHORITY
```

## 5. 權限邊界

本規則控制 repository topology，不改變各研究線的科學主張上限。`main` 的合併仍受 `MAIN_TRANSITION_AUTHORITY_GATE.md` 約束；Quality、CodeQL 或 topology pass 都不替代當前 exact-head Human Owner 決定。
