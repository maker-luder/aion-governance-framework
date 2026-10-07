# Text visibility v0.3 implementation plan / 隱藏文字顯影實作計畫

> For agentic workers: execute inline with superpowers:executing-plans; finish with a fresh whole-branch review.

Goal / 目標：依本輪 Human 提供的 36 節工程規格，延伸既有 v0.2 顯影，而不建立另一套來源權威。
Architecture / 架構：保留 TextRevealReport 與公開函式；Unicode 資料/位置、差異視圖各自分離，JSON 與 Markdown 同源。
Tech stack / 技術：Python >=3.11 標準庫，離線 Unicode 15.0.0 官方資料衍生表。
Spec / 規格來源：本輪附件 Hidden Text Signal Reveal / Imperceptible Text Visibility；具體範圍如下。
Base / 基線：70d89e0942e3cbf28e3e0590be0f7773d9dcd4fd。

## Global constraints / 全域限制

- TEXT_ONLY；保留原始 bytes、SHA256；不修改來源；不在執行時連網。
- 無浮水印產生、移除、規避、作者辨識；verdict = NOT_ESTABLISHED。
- exact observation 與 heuristic 分開；無總機率、無虛構 p-value。
- 不碰具身、main、治理規則或既有浮水印工具；單一 PR，不合併。
- 0-based byte/codepoint index；1-based line/column；CRLF 作一個換行，欄計碼點不是螢幕寬度。
- grapheme_cluster_index = NOT_IMPLEMENTED；不冒充完整 UAX #29 或 UTS #39。
- Unicode 固定表版本與 Python UCD 版本分別揭露；跨執行環境不承諾相同結果。

## Review focus / 反向檢查重點

1. BOM、多位元組、CR/LF/CRLF、尾端插入座標不可混淆。
2. 不同來源報告或 ledger 混用必須可被 digest 核對識別。
3. 惡意 Markdown fence、bidi、ESC 不可操控報告顯示。
4. 超出 heuristics/display 範圍需明示；exact 掃描與全檔 hash 不截斷。
5. 合法 emoji、波斯文、希伯來文、CJK、組合重音不升格惡意/浮水印。

## Task 1: exact source evidence / 精確來源證據

Files：新增 unicode_evidence.py、unicode_tables.json、UNICODE_LICENSE.txt；修改 text_reveal.py。
Interfaces：source_positions(text, encoding, bom_size)；character_inventory(text, data, positions)。
- [x] 加入多編碼位置、所有 Unicode 類別、合法控制、資料表校驗的失敗測試。
- [x] 執行測試確認缺功能；新增固定版本資料與 Unicode 正式名稱/中文解說/byte hex context。
- [x] 維持舊 cue_type；以 inventory 補充分類，避免同族多次計票。
- [x] 重跑 targeted tests、commit。

## Task 2: contrast and report / 對照與報告

Files：新增 normalization_views.py、text_compare.py；修改 text_reveal.py、__init__.py。
Interfaces：normalization_views(text)；compare_hidden_text_bytes(a,b)；render_text_reveal_json(report)。
- [x] 先測 NFC/NFD/NFKC/NFKD、雙來源位置、BOM/newline、safe Markdown、determinism、coverage。
- [x] 差異表示為有界、可重建區間；大文本使用共同前後綴精確區間，不冒充最小 edit script。
- [x] 報告綁 input digest、工具/Python/UCD/table 版本；ledger 每列綁同一 digest。
- [x] heuristic 只取前 4096 tokens；display 前 160 tokens/4096 codepoints；全部揭露範圍。
- [x] 六種分析副本敏感度；period scan 含 score/threshold/eligible；安全 Markdown/ASCII JSON。
- [x] targeted tests、strict mypy、commit。

## Task 3: verification and PR / 驗證及交付

Files：測試、docs/research/PROVENANCE_VISIBILITY_AGENT.md、docs/PROVENANCE.md。
- [x] 完整 tests、component tests、mypy 3.11/3.12、lint、compile、治理 validators。
- [x] fresh reviewer 檢查 claim/source binding/offset/rendering/large-input；修正後重測。
- [ ] 記錄第一手來源、限制、精確 SHA、測試數；單一 Draft PR；遠端讀回與 CI（完成狀態見 PR exact-head 回報）。

## Provenance / 來源分工

HUMAN_ORIGIN：來源可見性與本輪需求；JOINT_SYNTHESIS：既有 montage；AI_FORMALIZATION：本輪工程拆解。
EXTERNAL_SOURCE：Unicode UAX #15/#9、UTS #39、Python 官方文件、Unicode 15.0.0 資料。
REPOSITORY_STATE：GitHub 分支/PR/main 讀回；IMPLEMENTATION_EVIDENCE：實際測試/CI；UNKNOWN：浮水印、作者、模型歸屬。

## Execution rulings / 執行判定

- 附件已明確要求完成實作與 PR；本計畫承接該授權。使用新 clone 的獨立 feature branch。
- CLI = DEFERRED：既有 Python bytes/file 介面足夠，本輪不增加命令列寫入介面。
- 不建立統計新主張，不觸發 Wolfram/學術驗證；Context7 + 官方來源足以查證本輪 Unicode/stdlib 行為。

## 執行紀錄 / Ledger

- 基線相關測試 38 PASS；首輪新測試 49 FAIL / 5 PASS，失敗對應缺少 inventory/normalization/compare/report 欄位。
- Task 1/2 已完成；109 targeted PASS；核心 387 PASS；37 元件 2123 PASS。
- 獨立 reviewer：兩個 Important（全報告綁定、比較環境版本），兩個顯示一致性問題。
- Ruling：顯示截斷與新控制摘要雖被 reviewer 列 Minor，因直接違反 coverage/visibility 需求，列入同一修正 pass。
  若不修，使用者可能把部分顯示理解為完整，或誤解已有精確觀察；故以四項失敗測試後修正。
- 修正後 targeted 113 PASS、strict package mypy PASS、repository lint PASS。
- 不修改治理規則；元件 runner 產生 qa/CURRENT_TEST_RESULTS.json 後移出暫存證據並還原該檔，避免夾帶全倉庫生成物。
- CLI/字素分段/串流/完整 UTS #39 非此輪交付；不產生統計驗證主張。
- 最後 exact-head CI 與遠端狀態記錄於 PR，不以本文的 earlier test run 冒充最終驗證。
