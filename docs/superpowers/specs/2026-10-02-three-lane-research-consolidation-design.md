# 三條研究工作線與歷史分支收束設計 — 2026-10-02

狀態：待小博審閱的架構規格；尚未開始搬檔、整合程式、清理分支。  
Repository：`maker-luder/aion-governance-framework`。  
設計時 main exact SHA：`6a34d7780dd6d5bc717cd6c82ba39e7a6241c2fd`。  
設計時分支盤點：188 條（含 main；須在執行前重新盤點），open PR 查詢為空。  
來源：小博確認 **AI 主體性可能性一直是核心，`main` 為往後的第一研究主線；CCTS／人機學習第二；具身為獨立的第三工作支線**。保留既有 main 歷史、加上銜接，待收束完成後清理雜支。這是研究重心與工作路由的明確排序，不把 CCTS 的既有出版紀錄或具身 baseline 從 main 歷史抹去。  
`DESIGN != IMPLEMENTATION != VERIFICATION != AUTHORIZATION != MERGE`。

## 1. 實際倉庫邊界

main 目前首頁及研究地圖把工作拆成四組：證據與因果歸屬、連續性與歷史、受限適應與區辨測試、人機協作與學習。前三組是長期核心主線的方法與問題面向；整理導覽不是宣稱 AI 主體性可能性今天才成為核心。main 同時已保存 CCTS 學術物件的公開典藏 metadata（Zenodo record `22945883`／DOI `10.5281/zenodo.22945883`）、人機長期研究程式，以及較早的 twin-genesis embodiment 候選。這些已存在的內容不得為了改成「一主兩支」而被描寫成從未在 main 出現。

Git branch 從 main 建立時會繼承共同祖先的全部內容。因此「三條線」是**往後的研究導覽、檔案歸屬及工作／審查路由**，不是三條完全沒有共同檔案或歷史的平行倉庫。既有 Git 提交、PR、DOI 與公開連結保持可追溯。

## 2. 目標拓樸

| 工作線 | 後續工作位置 | 主題／現有內容對應 | 禁止的跨線推論 |
| --- | --- | --- | --- |
| 第一研究主線：AI 主體性可能性（長期核心） | `main`；所有 main 修改仍須獨立 PR、審查及 Human 授權 | 四域、六個主體性相關證據維度、連續性／記憶來源、受限適應、因果歸屬及 claim ceiling。治理、QA、provenance 是橫向控制，不強行列為第四個研究構念 | 記憶延續、工程能力或具身模擬通過不建立主體性、意識或身分 |
| 第二研究線：CCTS＋人機學習 | 建議 `research/ccts-human-ai-learning-lane`，從同一次 current main exact SHA 建立 | CCTS 後續 grounding、互相修訂、歷時重入、學習設計／對照；在同支線內保持 CCTS 論文與 Human-learning 實證問題兩個子題 | 已發布論文、結構測試或合成對照不等於人類學習、保持、遷移、因果效果或 CCTS 特定效果 |
| 第三研究線：獨立具身工作支線 | 建議 `research/embodiment-lane`，從實作時重新核對的 main exact SHA 建立 | AION／Astra、Teacher、Work、Codex 的具身候選，人體文獻參照、工程狀態、模擬、測試及獨立來源清單；已關閉的實驗 PR 是可審查來源 | 合成身體／模擬值不等於生物量測、感受、性慾、主體性或 main 已採納 |

這個第一、第二、第三排序表示往後的研究優先順序；不等於三個構念互相依附，也不撤銷 main 既存內容。CCTS 已發布紀錄及其 DOI metadata 維持在 main 的原路徑，該學術物件不轉為具身或主體性論文。main 可以有兩條支線的簡短入口及歷史連結；這種導航不改變每條支線的 scientific disposition。

## 3. 檔案路由與相容方案

### 3.1 主線入口

以獨立 Draft PR 提出最小導航修改：`README.md`、`README.zh-TW.md`、`docs/RESEARCH_MAP.md`、`docs/START_HERE.md`、`docs/CURRENT_STATE.md`、`docs/INDEX.md` 中真正需要改的地方。英文與繁體中文首頁語意對稱。由現行四組研究問題整理為有順位的三條研究線：一直作為核心的 AI 主體性可能性為第一，CCTS／人機學習為第二，獨立具身工作為第三；原四組的證據／連續性／適應仍能從主體性主線查得，不刪除其研究結果。main 上的具身與 CCTS 既有路徑標為歷史或已發布來源，不冒稱被移出 main。

支線入口使用明確 GitHub branch URL 與當前狀態文字，不讓相對連結默默落回 main 的同名檔案。exact SHA 只作審查快照；長期入口可用 branch ref，並於入口顯示最後核對 head。

### 3.2 CCTS／人機學習支線

建立 `docs/research/ccts-human-ai-learning/README.md` 連接 current CCTS 定義、正式出版 metadata、未發布手稿草稿、grounding 與 Human–AI longitudinal study 實作。新研究文件逐步放入支線目錄；已發布、已引用或原路徑被其他文件依賴的歷史文件先保留原位，用入口及必要的舊路徑銜接說明。若後續確需實體移動，逐一建立舊路徑 stub、更新相對連結及 CI 導覽檢查，並保留 Git history 可讀。

CCTS 的概念／方法論文和 Human–AI learning 的待檢驗效果分開標示；在同一工作支線不等於同一構念或共同驗證結果。

### 3.3 具身支線

先建立 `docs/research/embodiment/README.md` 作一個可閱讀的總入口及 provenance／claim 邊界表；按主題列出 main 已存在的 baseline、已關閉未合併的 Teacher／Work／Codex 等候選、主體性無涉的模擬與待整合缺口。新文件集中在 `docs/research/embodiment/`，實作仍在既有 package（例如 `research-labs/twin-genesis-embodiment_v0.1.0/`）中，以免無證據搬動 Python import、entry point、測試與證據 manifest。若要移動程式目錄，必須另有逐引用清單及可執行驗證。

不能把 #261、#262、#263 或其他 closed/unmerged 分支整批 merge 到 main 或新支線。逐項重建時須有來源 PR、exact head、diff、處置、測試與新 head；前輪的 `design/teacher-continuous-embodied-observation-20261001` 只作設計來源，不能假裝是最新 #263 祖先。

## 4. 執行順序與收束判準

1. **鎖定即時狀態。** 重新讀取 main SHA、兩條預定 branch 名稱是否仍空白、全部 branches、open PR、recent merges、相關 source docs、程式及 CI；把 188 條分支盤點當成歷史快照，不作永久名單。
2. **建立兩條工作支線。** 僅由同一個 newly verified main exact SHA 建立；既有 PR 保持原狀。每條支線先放入口、來源矩陣及明確 HOLD／UNKNOWN。
3. **彙整檔案與概念。** 對每個現有檔案／PR 標記：歸屬線、是否 main 已存在、是否 published、canonical effect、內容是否 unique、是否需要複製／重建／保留連結。避免同一份研究文本三處複製；研究內容的實際重入另走各支線的審查。
4. **更新 main 的導覽 PR。** 只描述已存在且可核對的三線入口，main 不直接寫入。保留舊 CCTS DOI 與出版路由。
5. **驗證收束。** 英／繁中首頁語意一致，所有相對與跨 branch 連結能解析；每個原四組問題有可找到的歸屬；publication 與 scientific validation、implementation 與 scientific establishment、branch existence 與 canonical status 分開；兩條支線各有 exact head 和 CI 狀態。
6. **最後才進行分支清理。** 在兩條支線及導覽 PR 的結果可檢視、來源差異已保存後，建立逐支可審查的 `BRANCH_DISPOSITION_MATRIX`，再處理下節條件。

此順序不承諾把具身實驗自動併入 main，也不承諾 main PR 自動 merge。

## 5. 雜支清理與 fail-closed 條件

`雜支` 指**在本次三線收束後，已被某條保留分支或 main 完整涵蓋，且沒有仍需保留的獨特工作、開啟 PR、出版／治理／CI 依賴或歷史引用的分支**。名字像 `tmp/`、`research/`、`codex/`，甚至 PR 已關閉，都不是安全刪除證據。

清理矩陣每列至少包括：branch、exact head、對應 PR 與 state、相對 main 的 ahead/behind 與 unique commit/file 摘要、目標工作線、保存去處及 exact target SHA、外部／內部連結、保留理由、CI 影響、可恢復 commit SHA、處置 `KEEP_ACTIVE / KEEP_ARCHIVE / SAFE_DELETE / HOLD_UNKNOWN`。無法核對 exact head 或 unique diff 的分支保持 `HOLD_UNKNOWN`。

刪除只適用於 `SAFE_DELETE` 且**已先驗證**新入口與保存去處的 exact head；刪除時再讀 live ref，若它在矩陣審查後變動，停止並重新審。絕不刪 `main`、保護分支、發行 tag、尚有 open PR 的 branch、未審閱的獨特來源，或無法重建的歷史證據。清理操作逐支記錄結果；工具不支援或授權不足時回報 HOLD，不用 force push、reset 或冒險批次指令。

小博已表明「收束完之後刪除雜支」的方向；**具體可刪名單及其證據仍須在收束後提供審閱**。泛稱「全部」不讓任何 branch 在未知狀態下被判為 `SAFE_DELETE`。若最後仍有 `KEEP_ARCHIVE` 或 `HOLD_UNKNOWN`，明列原因和待決問題，不能報作已清空所有雜支。

## 6. 驗證與逆向審查

- 檢查沒有把三條 Git branch 說成完全隔離的三個 repository；沒有假裝 current main 未含 CCTS 發表或具身 baseline。
- 檢查 subjectivity main 的四域六維仍是證據方法，沒有把具身模擬、CCTS 結構或 Human-learning fixture 當成主體性結果。
- 檢查 CCTS 的 Zenodo 學術物件和 `NOT_RELEASED` 當前草稿分開；出版不等於同儕審查或實證確認。
- 檢查沒有藉「搬檔」改寫來源／actor 歸屬，沒有遺失歷史 PR 和 exact SHA。
- 檢查所有 moved source 在舊路徑可導航，package imports、tests、manifest、README link 與 CI 能在**新 exact head** 通過；remote CI success 與 local tests 分開。
- 檢查分支刪除前後 main 及保留分支 exact SHA，所有刪除目標可由存檔 SHA 與證據表追溯。
- 對分支清理的每個 `SAFE_DELETE` 找反例：是否有未保存的 unique commit、外部引用、開啟 PR、保護規則或仍在使用的流程？任一 YES 改為 HOLD。

## 7. 身分、權限與科學邊界

`HUMAN_ORIGIN`：小博提出一主兩支、保留加銜接、完成後清理雜支，並澄清 AI 主體性可能性一直是核心，CCTS／人機學習第二，具身獨立工作支線第三。  
`AI_FORMALIZATION`：本規格將意圖拆為 branch topology、路徑相容、來源矩陣、刪除閘門與驗收。  
`REPOSITORY_STATE`：第 1 節 exact main、既有四組入口、188 branches 的查詢快照。  
`PROVENANCE != CORRECTNESS`。Actor label、interaction surface 與 verified model identity 保持分開。

`MERGE_TO_MAIN = NO`，除非另有具體 exact-head Human 授權。  
`SCIENTIFIC_ESTABLISHMENT = NOT_ESTABLISHED`。  
`CANONICAL_EFFECT = NONE`（設計文件本身）。  
`DEPLOYMENT = FALSE`。
