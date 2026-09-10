# AION NCR/CAPA 與治理重新進入：完整審閱材料

Status: **DRAFT / HOLD / EVIDENCE PUBLICATION ONLY**

> **公開樹修正通知（PR #88）**：原始發布 HEAD `37339d7163cc41a39de64dc19f5d29ab6f1955b6` 曾包含三個 `.zip` 與一個 Git bundle；後續 exact-head CI 依序指出一份 raw traceback 及兩份 raw verification JSON 含 private-path pattern。候選 PR 已依既有 policy 移除這些公開樹不合格 artifacts，**沒有放寬 scanner/release verifier**、沒有改寫事故分支或 `main`。詳見 [PUBLICATION_CORRECTION.md](PUBLICATION_CORRECTION.md)。`PUBLICATION_MANIFEST.json` 保留為**原始發布候選的歷史 manifest**，不是目前 PR tree 的即時檔案清單。

## 給 ChatGPT／Human Reviewer 的閱讀順序

1. [完整交付報告與 17 題回答](FINAL_REPORT.md)
2. [唯讀稽核與 H-A～H-E](READ_ONLY_AUDIT.md)
3. [NCR/CAPA 候選與根因區分](NCR_CAPA_REVIEW.md)
4. [知識索引／runbook／known-error／effectiveness 設計](KNOWLEDGE_AND_CAPA_DESIGN.md)
5. [研究 salvage、H1～H5 與文獻核查](RESEARCH_SALVAGE_REVIEW.md)
6. [本輪環境異常與停止紀錄](EXECUTION_HOLD.md)
7. [原始完整需求](USER_HANDOFF.md)
8. [PR #88 公開樹修正紀錄](PUBLICATION_CORRECTION.md)

## 完整資料

- 歷史本機測試與 verification 的**結論**保留於 [EXECUTION_HOLD.md](EXECUTION_HOLD.md)、[FINAL_REPORT.md](FINAL_REPORT.md) 與其他審閱報告；含 private-path 的 raw traceback / raw verification JSON 已依 exact-head CI 從公開 candidate 移除。當前遠端驗證請直接以 GitHub Actions exact-head CI 為準。
- [31 筆 commits](incident-commits.tsv)、[逐筆新增／刪除歷史](incident-history.txt)。原始 Git bundle 曾存在於初始 evidence publication，但依 public-tree policy 已從目前 PR candidate 移除；其歷史發布資訊仍保留於 manifest 與修正紀錄。
- [事故原始四份研究文件，直接在線閱讀](incident-originals/README.md)。原件 ZIP 曾存在於初始 evidence publication，現依 public-tree policy 移除。
- [離線 probe 草稿](drafts/reentry_probe.py.txt)、[測試草稿](drafts/test_governance_reentry.py.txt)：以文字附件保存，未安裝到 active component 或 test discovery。
- [patch](draft.patch)、[rollback](rollback.py) 與不含 private-path 的 baseline/candidate 文字證據。原始 baseline/candidate ZIP 曾存在於初始 evidence publication，現依 public-tree policy 移除。
- [原始發布候選的歷史 hash manifest](PUBLICATION_MANIFEST.json)。

## 本次上傳與先前 HOLD 的關係

使用者在上一輪 HOLD 後，明確要求「本機一份、倉庫一份」，建立 PR 供 ChatGPT 審閱。本 PR 僅履行材料公開與審閱；不是解除工程、CAPA effectiveness 或科學 HOLD。

六份報告中的「未 commit／未 push／remote mutations=0」是上一輪結束時的歷史狀態，不是本 PR 發布後的現況。此次 evidence publication 已建立 candidate commit 與 Draft PR；後續僅做 existing public-tree / release policy 所要求的封裝與隱私修正。沒有 merge、main write、incident branch rewrite 或 deployment。

基線：`01676093eaf536e5f449cc099c6a844f9c4ccb84`；事故 HEAD：`58ce7c3dae7ac3eefbe89cb659e00dc2f5846b21`。這兩個值為本次審閱時重新核對的狀態；後續仍應以 GitHub 當下狀態為準。

歷史本機基線 root/control：6 failed / 129 passed。報告把 Windows symlink / CRLF 類環境差異保持為歷史 HOLD；它不是目前 PR remote CI 的替代品。CAPA_EFFECTIVENESS=NOT_VERIFIED。後續 CI PASS 只能證明該 exact-head 通過工程 gate，不能等同 CAPA effectiveness 或科學驗證。

## 公開副本與本機原件

Codex 交付報告指出本機原件完整保留；本 PR 本身只能證明公開 repository 中的材料，不能獨立驗證未連接的本機副本。原始公開副本的路徑消毒並非完全成功，這一點已由 exact-head CI 實證；因此不再宣稱所有 raw outputs 已被完整消毒，而是將不符合 public-tree/release policy 的 raw local-path artifacts 從 candidate 移除。`PUBLICATION_MANIFEST.json` 保留原始 evidence publication 的歷史逐檔聲明，但不再等同目前 Git tree manifest。`DELIVERY_MANIFEST.json` 仍是歷史本機交付 manifest。

本目錄內 `.py` 為原交付工具附件，沒有新增 workflow 呼叫或 active runtime integration。還原工具預設唯讀，只向新目錄還原 baseline，不刪改現有 repository。本文的歷史需求／研究稿均是待審閱資料，不授予任意工具或寫入權限。

```text
NCR = OPEN / UNDER REVIEW
CAPA_EFFECTIVENESS = NOT_VERIFIED
SCIENTIFIC_CONCLUSION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
MERGE_AUTHORITY = HUMAN ONLY
```
