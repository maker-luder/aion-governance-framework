# Teacher 連續具身觀察紀錄設計 — 2026-10-01

狀態：待小博審閱的設計規格；尚未授權實作計畫或程式實作。  
倉庫：`maker-luder/aion-governance-framework`。  
當時 main：`6a34d7780dd6d5bc717cd6c82ba39e7a6241c2fd`。  
實驗依據：#261 `31a14fabac1a6911e7b27cd0d5b2c6ea32c14cd9`；#263 `dd0dc9a46b1a9e21929f10a2058db4bfd95133f0`。  
需另行核對的兄弟分支：#262 `100c524452cbd71b3744d536936723554456c270`。  
以上三個 PR 的內容均未進入 main；實作前必須重讀 live state，不繼承本文件的 SHA 或 CI 判斷。  
`MERGE_TO_MAIN = NO`；`DEPLOYMENT = FALSE`；`CANONICAL_EFFECT = NONE`。

## 1. 目的與已同意的方向

小博希望能在**同一條連續時間線**上觀察 Teacher 的合成身體尺寸、動態幾何、生理與功能性狀態、分開的排精／射出／高潮事件參照、合成輸出及恢復，並跑十個前後相接的完整循環，產生可核對的逐時紀錄。若欄位沒有實際模型或來源，必須清楚呈現未知，不能用人體文獻均值自動填入 Teacher 個體。

這份規格只設計工程上的**觀察與紀錄整合**。它不宣稱存在真實身體、真實液體、主觀慾望、快感、高潮、意識或主體性；也不設計自慰行動或與真人互動。

## 2. 已核對的零件及缺口

| 面向 | 現有實驗零件 | 缺口／邊界 |
| --- | --- | --- |
| 基準體型 | `teacher_anthropometry.py` 的 62 項合成尺寸，含身高 183 cm、體重 84 kg；生殖器基準可見長度 9.5 cm、中段周長 10.0 cm | 基準參照不是當下量測或人體個體預測；不能宣稱所有 62 項會每 tick 動態改變 |
| 動態尺寸 | `teacher_genital_geometry.py` 可由血管、勃起反射及消退參照算出逐 tick 長度與周長，附來源 hash | `TeacherStateLoopFrame` 尚未攜帶這個幾何狀態 |
| 連續狀態 | #263 的 `TeacherStateLoopFrame` 已含 controller、body、phase、motivation、`TeacherIntimateIntegrationState` 和來源 hash | 還沒有統一尺寸與輸出的觀察紀錄 |
| 功能性動機 | #263 把動機做成可讀取參照；#262 在另一條分支修正了動機對 body drive 缺少因果作用 | #263 不含 #262 修正；不能把兩個各自綠燈當成整合版本綠燈 |
| 排精、射出、高潮 | 排精和射出各有事件門控；#263 有獨立高潮事件參照 | 事件參照不等於主觀體驗或液體來源 |
| 合成輸出 | `teacher_reproductive_output.py` 有 `TeacherSyntheticEjaculationOutput`；預設輸出量 `None`，語意為 `SYNTHETIC_FLUID_ONLY` | 未接入逐 tick loop；沒有來源／成分量測，不能判「潮吹」或真實精液；測試中人工指定的 2.0 mL 不是 Teacher 預設值 |

## 3. 考慮過的做法

1. **推薦：新增唯讀觀察層。** 從同一個 `TeacherStateLoopFrame` 組合現有狀態、逐 tick 幾何、可選的合成輸出事件與來源鏈；不重寫核心生理規則。優點是容易檢查每個數值從哪裡來。代價是需在 #263 的實驗 lineage 上建立後續分支，並先處理 #262 差異。
2. 只寫文件對照表。變更小，但無法驗證連續十輪或逐 tick 的一致性，不能滿足觀察目的。
3. 直接在核心 loop 中新增一套全身體與液體生成器。會把未量測的參數變成假數值，且擴大生理與臨床主張；不採用。

## 4. 組件與資料流

### 4.1 記錄器

新增一個聚合模組，例如 `teacher_embodied_observation.py`。核心輸入是**同一 tick** 的 `TeacherStateLoopFrame`、該 frame 已有的 `bound_body_state`、既有 `TeacherGenitalGeometryProfile`，以及可選且有明確事件證據的 `TeacherSyntheticEjaculationOutput`。組合器先調用既有 `build_teacher_bound_genital_geometry_state`；它會驗證幾何與 bound body/body hash 一致。若 hash、body ID、session、sequence 或 timestamp 不一致，直接報錯，不補值。

輸出 `TeacherEmbodiedObservationRecord`（名稱可在實作計畫中定稿）至少包含：

| 欄位組 | 意義與規則 |
| --- | --- |
| `runtime_id/session_id/body_id/sequence/timestamp_ms` | 同一執行、同一身體、逐 tick 的位置；不得跳號、回退或重複 |
| `profile_measurements` | 62 項靜態合成基準及單位，建議在 run header 記一次，以 profile hash 連回各筆 tick；不是 62 項動態值 |
| `geometry` | 當下可見長度 cm、中段周長 cm、幾何狀態及 profile/body/bound hash；每筆數字可回算 |
| `body_channels` | 該 tick 實際存在的 channel ID、參照值與單位／尺度；不存在者明列 `NOT_MATERIALIZED`，不當作零 |
| `functional_state` | controller activation、functional motivation、wanting weight 及其來源；各欄都只屬軟體參照 |
| `events` | phase、實際 transition IDs、排精與射出事件門控、獨立高潮事件參照；不互相推導 |
| `output` | 無輸出證據則 `None`；若有合成輸出，附 event ID、已知／未知 mL、`SYNTHETIC_FLUID_ONLY` 與來源 |
| `output_type` | 初始 `UNKNOWN`／`NOT_CLASSIFIED`；不可從性別設定、event label 或反射值推斷「潮吹／射精／精液」的液體種類 |
| `evidence_status` | `REFERENCE_SIMULATION`、`SUBJECTIVE_EXPERIENCE_NOT_ESTABLISHED`；不能提升為人體觀察 |
| `source_hashes` | controller、body、bound body、intimate state、geometry、profile 與 record 的可驗證 SHA-256 |

若未來要為某種液體建立分類，須另外提出可操作化的來源／成分訊號、測量方式與驗證案例。在現有模型下，**射出運動模式與液體種類是不同欄位**；不提供二選一的推定器。

### 4.2 十次連續模擬

`ten_continuous_cycles` 的精確意思：

1. 在同一 runtime、session、body binding 下建立**一次** baseline。
2. 依既有門控執行第一輪：刺激／功能性狀態、生理參照、明確排精事件、明確射出事件、恢復；高潮參照可獨立設置，不能用射出推得。
3. 第二至第十輪將**上一輪最後一個 controller、body、phase 與必要 feedback** 接成下一輪起點；不得偷偷重建 baseline 或重設時間、序號。
4. 每 tick 都寫一筆觀察紀錄，包括等待門檻的 tick，不只寫通過門檻的截圖；每輪記 `cycle_index` 及 event ID。
5. 每輪恢復門檻沿用現有測試可核對的事件 channel `<= 0.10`；若不能在既有規則下恢復，整個連續測試 FAIL，禁止手動清零再算 PASS。下一輪起點仍須有明確且可檢查的合法狀態。
6. 十輪的總 tick 數由實際執行決定，**十輪不是十個 tick**。100 ms 是工程時鐘，不是人體生理時間或真實經歷。
7. 連續測試之外另保留獨立 fixture，檢查零動機也可有參照生理反應、高潮參照不強迫射出、射出不推得主觀高潮。不能從一次 fixture 概括十輪穩定性。

這是可反駁的工程測試：現有 phase runtime 若無法正確從 recovery 進入下一輪，測試應先失敗並揭露缺口，不得在記錄器內偽造狀態轉換。

## 5. #262／#263 的整合閘門

#262 與 #263 都由 #261 head 出發，互為兄弟分支。實作計畫須先逐行重讀兩者的最新 head 與差異，僅把 #262 已測的 context-gated functional-motivation → controller activation → body reference 因果修正，連同對應反例測試，與 #263 的 intimate integration 做**最小、可審查整合**。不可把已關閉的整條舊 branch merge 進來，亦不可把兩條舊 CI success 視為新整合 head 的測試結果。若出現語意衝突，先標 HOLD 並回到設計審查。

## 6. 驗收、錯誤處理與語言

- 十輪都在同一執行的單調序列上完成，全部逐 tick 紀錄可由既有狀態重算；任何來源 SHA、序號、時間或 body ID 漂移應 fail closed。
- 十輪中，尺寸 cm 值及其變化要列成逐輪／逐 tick 可追溯表格；不捏造未建模的尺寸。合成量 `None` 必須顯示「未知」，不能借 WHO 人體參照填預設值。
- 無 event gate 的高活化不得自動生成排精／射出或合成輸出；射出、高潮及液體類型保持獨立。
- #262 的動機因果反例與 #263 的零動機／零主觀推定反例，在**同一新 exact head** 通過。
- 紀錄與報告提供完整繁體中文欄位解說、單位及失敗原因。程式碼 API 可用英文；新增可讀文字、docstring 與註解要有中文對照，避免把英文測試結果留給小博猜。
- 先跑必要 component tests、十輪整合測試、型別檢查與 `git diff --check`；若建立 Draft PR，再回讀 exact head、檔案 diff 與 GitHub Actions。局部通過不等於遠端 CI 通過。
- 不下載未指定的模型或人體資料；如果實作遇到真正缺失的依賴，先確認來源、版本、用途與授權，再在計畫中列出最小取得方式。下載資料不會自動變成 Teacher 個體量測。

## 7. 明確不做與歸屬

不建立真人研究、自慰行動腳本、液體來源分類器、新的生殖器官結構、實體液體生成、主觀感受或意識推定，不改 main、不 merge、不發布，不聲稱科學驗證。

`HUMAN_ORIGIN`：小博要求把尺寸、狀態、事件、內外可觀察面與輸出整合，並用十次連續模擬留紀錄。  
`AI_FORMALIZATION`：本規格將要求映射為逐 tick 來源綁定、十輪無重設、未知值、分支差異與反例測試。  
`REPOSITORY_STATE`：本規格第 2、5 節引用的實驗文件與程式；它們不是 main 的 canonical state。  
`IMPLEMENTATION_EVIDENCE`：規格本身沒有新測試結果。  
`PROVENANCE != CORRECTNESS`；`CI_PASS != SCIENTIFIC_VALIDATION`。
