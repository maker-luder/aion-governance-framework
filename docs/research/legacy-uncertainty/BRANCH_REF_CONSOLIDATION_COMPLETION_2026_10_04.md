# 分支引用收斂完成紀錄（2026-10-04）

## 目的與事件順序

本紀錄承接 2026-10-02 的唯讀盤點與 HOLD 報告。原報告形成時沒有分支刪除權，因此保留其事件時間敘述，不覆寫歷史。使用者檢閱後另行指示：倉庫長期只保留四條分支，並將此拓樸做成倉庫硬性規則。

## 四條長期分支

1. `main`：主核心；AI 主體性可能性持續是長期核心方向。
2. `research/ccts-human-ai-learning-lane`：CCTS／Human–AI Learning／協作研究線。
3. `research/embodiment-lane`：具身獨立研究線。
4. `research/legacy-uncertainty-hold`：尚未分類來源的暫時整理線；不是第四個科學構念。

## 已執行結果

- 收斂前 live branch：193。
- 每一個候選引用均先記錄 `branch + exact head`。
- 建立 189 個一對一 recovery tags：`archive/branch-heads/2026-10-03/<原分支名稱>`。
- 建立並驗證包含收斂前完整引用歷史的 Git bundle。
- 以 exact-SHA lease、無 force-update、無歷史改寫方式移除 188 個舊 branch refs。
- PR #264 審查期間遠端為 5 條 branch：四條長期分支，加上 PR #264 自己的一條暫時 head。
- PR #264 proposed exact head：`96a0c874ccf21c0cc1518cce4834d82521f183d8`。
- PR #264 仍為 `OPEN / DRAFT / NOT_MERGED`；在 Human exact-head approval 與合併完成前，main 尚未取得新規則。

Recovery tags 是可回復引用與 provenance 證據，不會把舊分支內容升格為 canonical、已審查或科學上已驗證的成果。

## PR #264 所提硬性規則

PR #264 在精確 head `96a0c874ccf21c0cc1518cce4834d82521f183d8` 提出：

- 穩定狀態必須且只能有上述四條 durable branches。
- 審查期間最多允許一條同倉庫 open-PR 暫時 head；PR 結束後必須回到四條。
- 建立、刪除、PR 事件、排程與 Quality 都執行 live topology validation。
- closed PR cleanup 只在 branch 非 durable 且 exact head 沒有移動時刪除；API、權限或 SHA 不一致一律 fail closed。
- CI 通過不取代 Human Owner 對 exact head 的合併決定。

## 驗證狀態

- Branch Topology Governance：PASS。
- Quality（Python 3.11／3.12）：PASS。
- Mypy（Python 3.11／3.12）：PASS。
- CodeQL：PASS，沒有此 PR 新增的 alerts。
- 唯一未通過項目：`Fresh exact-head Human Owner approval receipt`；這是刻意保留的合併授權閘門，不是程式回歸。
- 本機 targeted tests：13 passed。
- 本機 Windows root suite：227 passed、4 deselected；另 7 項在 PR #264 原始 head `61f41f39bb9301631b576eb055e408ffbd2251e4` 可等同重現，分類為 baseline／平台限制，不歸因於本輪治理變更。

## 最後狀態與下一閘門

目前已完成引用收斂、歷史封存、規則實作、測試及回復預演。尚待 Human Owner 明確核准 PR #264 的 exact head `96a0c874ccf21c0cc1518cce4834d82521f183d8`。核准後才可把 PR 轉為可審查、合併至 main，並驗證 PR head 被移除、live branch 精確回到四條。

`CANONICAL_EFFECT = NONE`（直到另行核准並合併）  
`MERGE_TO_MAIN = HUMAN_EXACT_HEAD_GATE_REQUIRED`  
`PUBLISH = NO`  
`DEPLOYMENT = FALSE`
