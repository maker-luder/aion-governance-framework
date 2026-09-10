# PR #88 公開樹修正紀錄

Status: **CORRECTION / HOLD / EVIDENCE PRESERVATION**

## 修正原因

PR #88 的原始發布 HEAD `37339d7163cc41a39de64dc19f5d29ab6f1955b6` 將完整本機封存材料一併放入公開候選樹，其中包含三個 `.zip` 與一個 Git bundle。Repository 既有 `scripts/scan_public_tree.py` 明確拒絕 `.zip` 等封裝／二進位產物，因此 Quality workflow 在 public-tree scan 階段失敗。

這是**發布封裝不符合既有 public-tree policy**，不是理由去放寬或繞過 scanner。既有 public-tree policy 保持不變。

## 從公開候選樹移除的四個封裝

- `baseline.zip`
- `candidate-draft.zip`
- `incident-research-originals.zip`
- `incident.bundle`

移除僅限 PR #88 的公開 candidate tree。此動作：

- 不改寫事故分支；
- 不改寫事故歷史；
- 不改動 `main`；
- 不把 NCR/CAPA 提升為已驗證；
- 不改變任何人工主體性／意識相關科學結論。

事故分支本身及本目錄中的文字型 incident history、commit 列表、原始研究文件副本、hash/manifests 仍提供可稽核證據。Codex 先前交付報告所述本機原件亦不因本 PR 公開樹修正而被重新定義或驗證。

## Manifest 語義

`PUBLICATION_MANIFEST.json` 刻意保留原始發布候選的歷史 manifest。它記錄的是原始 evidence publication package，不應被解讀為「目前 PR tree 的即時檔案清單」。

目前 PR tree 的真實狀態應以 Git tree / PR changed files 與本修正紀錄共同判讀。

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

本次修正只處理已被 CI 直接證實的公開樹封裝問題；不藉機擴張成新的 CAPA 實作或平行治理系統。
