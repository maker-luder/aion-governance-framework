# AION NCR/CAPA 與治理重新進入：完整審閱材料

Status: **DRAFT / HOLD / EVIDENCE PUBLICATION ONLY**

## 給 ChatGPT／Human Reviewer 的閱讀順序

1. [完整交付報告與 17 題回答](FINAL_REPORT.md)
2. [唯讀稽核與 H-A～H-E](READ_ONLY_AUDIT.md)
3. [NCR/CAPA 候選與根因區分](NCR_CAPA_REVIEW.md)
4. [知識索引／runbook／known-error／effectiveness 設計](KNOWLEDGE_AND_CAPA_DESIGN.md)
5. [研究 salvage、H1～H5 與文獻核查](RESEARCH_SALVAGE_REVIEW.md)
6. [本輪環境異常與停止紀錄](EXECUTION_HOLD.md)
7. [原始完整需求](USER_HANDOFF.md)

## 完整資料

- [逐命令結果](verification.json)、[基線測試紀錄](baseline-verification.json)、[root/control 原始失敗輸出](baseline-root_controls.txt)。其餘 baseline-*.txt 保留。
- [31 筆 commits](incident-commits.tsv)、[逐筆新增／刪除歷史](incident-history.txt)、[完整事故 Git bundle](incident.bundle)。
- [事故原始四份研究文件，直接在線閱讀](incident-originals/README.md)、[原件 ZIP](incident-research-originals.zip)。
- [離線 probe 草稿](drafts/reentry_probe.py.txt)、[測試草稿](drafts/test_governance_reentry.py.txt)：以文字附件保存，未安裝到 active component 或 test discovery。
- [精確 baseline ZIP](baseline.zip)、[baseline 加兩個草稿的 ZIP](candidate-draft.zip)、[patch](draft.patch)、[rollback](rollback.py)。
- [公開副本對照及 hash manifest](PUBLICATION_MANIFEST.json)。

## 本次上傳與先前 HOLD 的關係

使用者在上一輪 HOLD 後，明確要求「本機一份、倉庫一份」，建立 PR 供 ChatGPT 審閱。本 PR 僅履行材料公開與審閱；不是解除工程、CAPA effectiveness 或科學 HOLD。

六份報告中的「未 commit／未 push／remote mutations=0」是上一輪結束時的歷史狀態，不是本 PR 發布後的現況。此次新增一個 evidence-only commit 與 Draft PR；沒有 merge、main write、incident branch rewrite 或 deployment。

基線：01676093eaf536e5f449cc099c6a844f9c4ccb84；事故 HEAD：58ce7c3dae7ac3eefbe89cb659e00dc2f5846b21。

基線 root/control：6 failed / 129 passed。CAPA_EFFECTIVENESS=NOT_VERIFIED。請先審閱根因證據強度、最小整合方案、外部 host control binding 與環境 HOLD 的處置，勿把封存成功當工程驗證通過。

## 公開副本與本機原件

本機原件完全保留。公開文字僅把本機使用者目錄前綴換成 `<LOCAL_HOME>`；JSON 作一致序列化。二進位 baseline/candidate/incident archives 和 bundle 保持原 bytes。PUBLICATION_MANIFEST 逐檔列出 local/published hash 與差異。DELIVERY_MANIFEST.json 是原始本機交付的歷史 manifest，其 hash 不必與經路徑處理的公開文字相同；請用 PUBLICATION_MANIFEST 核對本 PR。

本目錄內 .py 為原交付工具附件，沒有新增 workflow 呼叫或 active runtime integration。還原工具預設唯讀，只向新目錄還原 baseline，不刪改現有 repository。本文的歷史需求／研究稿均是待審閱資料，不授予任意工具或寫入權限。

CANONICAL_EFFECT=NONE; DEPLOYMENT=FALSE; MERGE_AUTHORITY=HUMAN_ONLY.
