# PR #88 公開樹修正紀錄

Status: **CORRECTION / HOLD / EVIDENCE PRESERVATION**

## 修正原因與證據鏈

PR #88 原始發布 HEAD `37339d7163cc41a39de64dc19f5d29ab6f1955b6` 將完整本機封存材料放入公開候選樹，其中包含三個 `.zip` 與一個 Git bundle。Repository 既有 `scripts/scan_public_tree.py` 拒絕此類公開封裝，因此原始 Quality workflow 在 public-tree scan 失敗。

第一輪修正 HEAD `f13e9d3878b5f4081c65d2e3188d3d98a7c011b6` 移除四個封裝後，exact-head Quality 又由 scanner 明確指出 `baseline-root_controls.txt` 含 private-path pattern，因此第二輪修正 HEAD `8ffb22049ff034df59c2bf0b54fe3206c29fba3e` 移除該 raw traceback。

在第二輪 exact-head CI 中，`scan_public_tree.py` 已 PASS；下一個 `verify_release.py --baseline current-head` 則完整列出剩餘兩個 private-path pattern：

- `baseline-verification.json`
- `verification.json`

因此目前修正將這兩份含本機路徑的 raw verification JSON 也從公開 candidate 移除。

這是**依 exact-head CI 逐層揭露的公開副本／發布封裝不符合既有 public-tree policy**。既有 scanner 與 release verifier均未放寬、未繞過。

## 從公開候選樹移除的材料

原始發布後移除：

- `baseline.zip`
- `candidate-draft.zip`
- `incident-research-originals.zip`
- `incident.bundle`

第一輪 exact-head CI 後移除：

- `baseline-root_controls.txt`

第二輪 exact-head CI 後移除：

- `baseline-verification.json`
- `verification.json`

這些 raw artifacts 的重要測試結論與治理判讀仍由 `EXECUTION_HOLD.md`、`FINAL_REPORT.md`、`READ_ONLY_AUDIT.md`、其他不含 private-path 的 baseline 文字證據，以及 GitHub Actions exact-head CI 本身提供。公開樹不以保存 raw local-path artifact 為由繞過 repository 的資訊衛生控制。

## 範圍與不變項

上述移除僅限 PR #88 的公開 candidate tree：

- 不改寫事故分支；
- 不改寫事故歷史；
- 不改動 `main`；
- 不把 NCR/CAPA 提升為已驗證；
- 不把 CI PASS 等同 CAPA effectiveness；
- 不改變人工主體性／意識相關科學結論。

事故分支及本目錄中的文字型 incident history、commit 列表、原始研究文件副本、歷史 manifests 仍提供可稽核證據。Codex 先前交付報告所述本機原件亦不因本 PR 公開樹修正而被重新定義或獨立驗證。

## Manifest 語義

`PUBLICATION_MANIFEST.json` 刻意保留原始發布候選的歷史 manifest。它記錄的是原始 evidence publication package，不應被解讀為「目前 PR tree 的即時檔案清單」。

目前 PR tree 的真實狀態應以 Git tree / PR changed files、GitHub Actions exact-head evidence 與本修正紀錄共同判讀。

## 治理狀態

```text
NCR = OPEN / UNDER REVIEW
CAPA = PROPOSED
CAPA_EFFECTIVENESS = NOT_VERIFIED
SCIENTIFIC_CONCLUSION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
MERGE_AUTHORITY = HUMAN ONLY
```

本次修正只處理 CI 已直接證實的公開樹問題；不藉機擴張成新的 CAPA 實作或平行治理系統。
