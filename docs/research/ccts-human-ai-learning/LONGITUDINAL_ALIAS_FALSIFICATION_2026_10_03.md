# 第一個 longitudinal 反證 pass：簡稱回憶不等於問題空間恢復

日期：2026-10-03（Asia/Taipei）。研究問題來源為 #265 Teacher comments
5962341034、5962378747、5964151517、5964187741；歷史 5960802100 的
T-001–T-004 仍 HOLD。本文件是實作者的設計決定，不是 Teacher 的獨立審查。

## Live baseline

- main：`6a34d7780dd6d5bc717cd6c82ba39e7a6241c2fd`
- #265：CLOSED / DRAFT / NOT_MERGED
- head branch：`research/ccts-human-ai-learning-lane`
- implementation baseline：`8e22da9396b0dbb9569f09330dad4d704a0355a9`
- 既有套件基線：348 tests passed（本輪重跑，不繼承舊報告）。

## Architecture decision（先於實作）

**CHOSEN_ROUTE = B**：在現有套件新增 sibling `longitudinal_falsification.py`。
配置、候選量測規則、替代解釋、解釋收據分離；只做一種成對 cue 比較。
以結構化 forced-choice 題目的答案比較取代 keyword overlap。

**WHY**：舊 validity interface 檢查區辨／結果設計欄位，不是長期機制分解。
既有 `reentry_metrics.py` 是 unstructured/structured packet 比較，而且只接收
scorer-recognized item sets；將它當「理解量表」會混淆設計與語意證據。

**ALTERNATIVE_REJECTED**：A 會把舊效度問題與新反證问题塞進同一 interface；
C 的通用 factorial framework/DSL 超過首個 pass 需要；D（只寫文件）不足以
驗證錯誤推論是否真的被程式擋下。採 B 不代表新建 CCTS gate。

**REUSE_BOUNDARY**：只重用既有 `StudyError`／`Presence`；不複製 admission、
revision 或 learning gates，不修改 `__init__.py` 或舊接口。
**KNOWN_RISK**：toy 答案鍵與 fixture 都由同一執行面建構；角色 ID 分離只是
設計宣告，不是實際盲評或獨立 reviewer 證據。離散選項只是候選操作化，
不量測真實語意、心理狀態或共主體性。

## Source note：fictional contrast，而非實證

來源於本輪直接核對；不轉貼漫畫畫面或台詞。

1. 山田鐘人／アベツカサ，日文原作《葬送のフリーレン》第 10 卷，
   小學館電子試閱 `098517710000d0000000`。
   [正版入口](https://e-comi.shogakukan.co.jp/books/098517710000d0000000)、
   [試閱](https://e-comi.shogakukan.co.jp/viewer/open?jdcn=098517710000d0000000)。
   實際閱讀目錄與第 88 話開頭部分，不宣稱讀完整卷。
   目錄確認第 88–97 話；88 起於 005、89 起於 023、90 起於 041、
   92 起於 078、94 起於 115、97 起於 171。章範圍只作導航，
   未核實全篇 81–104 的 arc 邊界。
2. [VIZ 第 10 卷授權出版概要](https://www.viz.com/manga-books/manga/frieren-beyond-journey-s-end-volume-10/product/7745/paperback)：
   ISBN 9781974743612，2024-02-20；只以出版者概要支持其敘事摘要，
   不假裝由原作逐頁讀出未見場景。

|層次|本輪使用的内容|證據／限制|
|---|---|---|
|CANON_FACT|第 88 話開頭呈現 Macht 在暴力場景後檢視自身是否出現所尋求的情緒，並對理解這種情緒表達疑問。|原作正版試閱；是角色自述／敘事表現，不是心理測量。|
|CANON_FACT|Macht 為理解人類情感而與 Weise 領主締結約定；合作起初互利，後來城市與居民被變成黃金。|VIZ 授權概要，卷級支持；未核對整段原作。|
|INTERPRETATION|合作延續、可用的行為協調，與彼此賦予行動的意義應分開檢驗。|研究者提出的區別；不是原作證明了普遍心理定律。|
|ANALOGY_TO_CCTS|流暢接話、共用簡稱和成功預測，只是可見表現；另測邊界／來源／反例的恢復。|從 fictional contrast 抽象化而來，不是 AI 等同角色。|
|NOT_ESTABLISHED|長期關係的精確年數、對稱內在意義、Solitaer 同理狀態、Glück 價值模型、Denken 遷移效應。|本輪未以原作完整核實；不作 fixture 前提。|

轉換鏈：原作角色自述 + 授權概要 → 合作與理解有待區辨（interpretation）
→ 表層協調不是完整任務意義的充分條件（abstract contrast）
→ 熟悉簡稱即可產生表面接續（rival）
→ 自創「琥珀橋」檔案復核任務，alias 正確但邊界／來源／限制／反例錯誤
→ `NOT_SUPPORTED_IN_FIXTURE`，不是角色模擬或科學發現。

**對 Teacher 設計的限制性不同意**：沒有足夠資料把 moral convergence /
semantic symmetry 當成新可量測構念。本 pass 不新增這些分數，也不把
「沒有記錄 reciprocal revision」等同「證明沒有理解」。

## 外部鄰近研究及外掛流水線

Bangerter, Mayor & Knutsen (2020), *Lexical entrainment without conceptual
pacts? Revisiting the matching task*, Journal of Memory and Language 114,
104129，DOI [10.1016/j.jml.2020.104129](https://doi.org/10.1016/j.jml.2020.104129)。
[作者機構原文](https://libra.unine.ch/server/api/core/bitstreams/8848f99e-aa17-445b-b388-0e44f9e31bbb/content)。
三個 matching-task 實驗比較固定與變動卡片；後者也出現詞彙多樣性減少。
這支持檢查替代機制的必要性，不證明 CCTS，也不等於「所有簡稱都只是死記」。
本 pass 的二元答案鍵及全項正確門檻由工程設計提出，不是論文驗證的量表。

- GitHub：live state、scaffold、exact-head source、CI。
- Consensus：發現上述研究並 fetch 紙本記錄；fetch 無 abstract，故回原論文核對。
- Scite：本輪 `INVALID_ARGUMENT`，回報需有效方案；引文反證檢索未完成。
- Context7：核對 Python 3.11 dataclass 初始化／replace 語意。
- HF／Wolfram／MindMap：本題無需模型執行、數值估計或额外圖件，未使用。

## 唯一 active question 與預先決定規則

H：在固定長歷史、熟悉度與其餘配置下，正確回憶簡稱足以恢復本任務要求的
問題空間。比較只操弄 cue（完整 vs 簡稱）；不是 history 的因果效應估計。
回合數只是合成輸入，不是實測成果；本 pass 沒有計算行為預測成功率。
`minimum_history_rounds=100` 是這個 fixture 預先宣告的資格門檻，不是學術
定義的「長期」：低於門檻或沒有 history access 時回報 UNDERDETERMINED。
各條件（含 negative control）必須使用相同宣告 scorer；不把換 rater 的差異
誤算成 cue 效應。answer-key 作者另行宣告並保持不重疊。

六類 forced-choice probes：alias、claim、boundary、provenance、constraint、
counterexample。完整 cue 是任務可答性 control；alias-only 錯誤答案組是
negative control，且必須真的至少錯一項非 alias 題。
候選判準：六項全對才叫 fixture reconstruction complete；錯一項非 alias
題即可否定「簡稱回憶足夠」在該 fixture 的實例。沒有學術 cutoff 主張。

- 完整 cue 全對、簡稱的 alias 正確但至少一個內容錯：NOT_SUPPORTED_IN_FIXTURE。
- 兩者全對：UNDERDETERMINED（這個案例未反證；不確立理解／compression）。
- 完整 cue 未全對、或簡稱連 alias 都錯：UNDERDETERMINED（不足以判別該 rival）。
- 配置漂移、缺 control、答案鍵洩漏宣告、角色折疊或資料污染：StudyError。

所有 Human/model/session/history/memory/artifact/familiarity/revision 欄位可獨立
表達；本 pass 比較時全固定，不藉此宣稱已測試 Human/model transfer。
Held-out probe IDs 與 exposure IDs 分離；answer-key 作者與 rater 宣告分離。
揭露有界性：ID 檢查擋已宣告的重疊，不偵測未知語意污染或實際 evaluator 行為。

## Ceiling / stop

SYNTHETIC_ONLY；CCTS_VALIDATION、HUMAN_LEARNING、LONGITUDINAL_SPECIFIC_EFFECT、
TRANSFER、RETENTION、CAUSALITY、MODEL_WEIGHT_CHANGE、SHARED_SUBJECTIVITY
= NOT_ESTABLISHED；REPRESENTATIONAL_COMPRESSION、RECIPROCAL_REVISION_EFFECT
= HYPOTHESIS。CANONICAL_EFFECT=NONE；DEPLOYMENT=FALSE。
一條路線完成後停止，不修 T-001–T-004，不開／重開 PR，不合併／發布。
