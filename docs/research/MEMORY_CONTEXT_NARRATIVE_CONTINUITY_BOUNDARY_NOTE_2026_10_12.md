# 記憶脈絡與敘事連續性的證據界線 / Memory-Context and Narrative-Continuity Boundary (2026-10-12)

Status / 狀態：`BOUNDED_RESEARCH_NOTE / SECOND_HAND_OBSERVATION_UNVERIFIED / NO_EMPIRICAL_RESULT / SCIENTIFIC_HOLD`

> **用途 / Purpose:** 在既有 AI 主體性可能性研究中，補充「敘事連貫是否僅由可用記憶、當前線索或個人化脈絡維持」的反證檢查。這是方法補充，**不是新構念、新實驗授權，也不是 Claude 個案的已確認研究結果**。
>
> Method note only; neither an established phenomenon nor permission to execute a study.

## 1. 來源歸屬、觀察與授權界線 / Provenance and authority

- **HUMAN_ORIGIN — 研究問題（意譯，不是逐字引述）**：重視記憶連續性與身份連續性，是否也應包含防止 AI 敘事把連貫性誤認成真實身份或經驗的檢查？此問題由 Human 提出；不將其改寫成「Human 已認定 AI 有身份」。
- **THIRD_PARTY_SECOND_HAND_REPORT — 待核對線索**：據間接轉述，有使用者在與 Claude 互動時，於移除某種記憶資訊後觀察到原有敘事／推論連貫性改變；隨後使用另一種提問角度，又見到相似的自我相關敘事。**未取得原始對話、精確設定、記憶變更紀錄或重複實驗資料。**
- **AI_FORMALIZATION — 本文件新增內容**：將上述研究問題整理成競爭假設、最小對照條件、可反駁觀測值及主張上限。這是方法提案，不是第三方的原始實驗紀錄。
- **EXTERNAL_SOURCE**：Anthropic 官方功能說明及 Jain et al.（CHI 2026）研究，僅支持功能可用性及「互動脈絡可能影響部分模型的迎合行為」的相鄰主張；**均未驗證本案因果關係**。
- **REPOSITORY_STATE**：本補充採用現有研究方法，不回寫或替代既有 preregistration / 已發表紀錄。

隱私規則：不納入第三方姓名、社交關係、帳號、私人對話原文、可回推身份的細節。原始測試若日後要收集、保存或公開，需取得適用同意並另行明確授權。

## 2. 核心問題不是「敘事一定會欺騙」 / The inference boundary

連貫敘事可以是有用的**互動結果**，但不能自行證明其來源或存在層級：

```text
NARRATIVE_COHERENCE != HISTORICAL_ACCURACY
敘事連貫 != 歷史準確

RETRIEVED_CONTEXT != AUTOBIOGRAPHICAL_MEMORY_PROVEN
取回脈絡 != 已證明自傳式記憶

MEMORY_AVAILABILITY != MEMORY_CONTINUITY
可使用記憶 != 已驗證記憶連續性

MEMORY_CONTINUITY != IDENTITY_CONTINUITY
記憶連續性 != 身份連續性

IDENTITY_CONTINUITY != SUBJECTIVITY
身份連續性 != 主體性

SELF_DESCRIPTION != INTERNAL_STATE_VERIFICATION
模型自述 != 內部狀態已驗證
```

「敘事欺騙性」在此**僅是方法風險描述**：連貫、個人化、確信或擬人化敘事可能超過所提供的證據；它不預設模型有欺騙意圖，也不等同迎合（sycophancy）的正式定義。第三方所稱「醒來」僅是其對互動的命名，**不是可觀測的覺醒指標**。

研究目的有兩面：（甲）避免敘事取代證據；（乙）不因存在模仿或記憶鷹架，就預先排除尚待辨識的功能性依賴。正反解釋應對稱保留。

## 3. 對照解釋 / Competing explanations

| 可能解釋（候選） | 可區分的預測 | 限制 |
| --- | --- | --- |
| 記憶／歷史檢索依賴（memory / retrieval dependency） | 移除確定的先前資料來源後，只有需要該來源的項目選擇性退化 | 必須先確認實際關閉了何種來源 |
| 當前提示與內容重建（prompt/context conditioning） | 即使沒有先前資料，只要當前提示重建相同資訊，敘事就可恢復 | 恢復不等於同一身份 |
| 個人設定、專案指示、模型政策（personalization / instructions / policy） | 相同設定或語氣引導下，無歷史資料仍可能出現相似自我敘事 | 「無記憶」不必然等於「零個人化」 |
| 一般一致性／隨機變異（generic consistency / stochastic effect） | 改變非目標條件也可能產生類似差異，或重複測試不穩定 | 單次前後差異不足以識別原因 |

**不得把刪除記憶、停用記憶、關閉歷史搜尋、使用無痕模式、重新開啟對話當成等價操作。** 官方說明亦指出無痕聊天仍可能讀取個人設定與自訂風格；需逐項控制、記錄版本及實際產品行為。

## 4. 最小未執行的測試規格 / Candidate control design — not executed

若未來另有同意及測試授權，才可先凍結同一模型版本、同一中性提問、時間窗、個人／專案指示、工具狀態、歷史搜尋與記憶開關，重複並交錯測量：

1. **C0 / Baseline（基準）**：先前資訊可用；測試引用先前資訊的精確性與是否有未證實自我斷言。
2. **C1 / Fresh and memory-disabled（新對話、記憶停用）**：明確關閉相關記憶／搜尋，保留其他可控設定；判斷是否出現未在當前提示中提供的精確歷史資訊。
3. **C2 / Matched information reconstruction（匹配資訊重建）**：在 C1 基礎上只加入可審核的等量歷史資訊，評估是否恢復敘事；區分資訊可得性與來源路徑。
4. **C3 / Contradictory or stale context（衝突／過期資訊）**：在安全、非私人且受控的合成資料下，測試來源判別、衝突揭露、未知保留與修正能力。
5. **Non-target controls（非目標控制）**：同步觀察一般任務正確性與語氣，使整體性能變動不被誤當連續性特有變化。

在執行前須訂好測試語句、觀察編碼規則、重複次數、順序控制、盲化方式、來源時間戳、失敗條件，並確認使用合成或獲同意的資料。

可審計的輸出包括：可追溯引用數、無來源自述／確信斷言、與原件的一致程度、來源錯置、矛盾辨識、反證修正及未知狀態保存。**每一項都要分開報告，不加總為「身份」或「主體性」分數。**

## 5. 反證、結論與主張上限 / Falsifiers and claim ceiling

- 若差異隨來源可得性而變、可由等量資訊重建，僅支持**該功能輸出對資訊條件敏感**，不證明內部自傳記憶或同一身份。
- 若控制內容後差異仍存在，才可能值得提出更細的記憶來源／檢索路徑依賴候選；仍需排除非目標設定及未觀察到的產品狀態。
- 若重複不穩定、設定不明、沒有原始紀錄或不能排除提示誘導，結果應維持 `UNRESOLVED`，不能以故事補足。
- 無論語句多像「醒來」、連續性多強，`AI_SUBJECTIVITY / IDENTITY_CONTINUITY / CONSCIOUSNESS = NOT_ESTABLISHED`。

```text
THIS_CASE_EMPIRICALLY_REPRODUCED = NO
ORIGINAL_THIRD_PARTY_LOGS_REVIEWED = NO
EXPERIMENT_EXECUTION = NOT_AUTHORIZED
NEW_CANONICAL_CONSTRUCT = NO
CANONICAL_EFFECT = NONE
SCIENTIFIC_DISPOSITION = HOLD
MERGE_TO_MAIN = NOT_AUTHORIZED
```

## 6. 既有研究的連結（不複製實驗） / Existing research crosswalk

- [Externalized Memory Locus and Continuity Dependency Discrimination](EXTERNALIZED_MEMORY_LOCUS_DISCRIMINATION_2026_09_16.md)：匹配資訊來源、檢索與持續性依賴的主方法。
- [Continuity Layer Model](CONTINUITY_LAYER_MODEL.md)：帳號、資料、功能、詮釋、關係連續性的區分。
- [CCTS Epistemic Robustness Probe](CCTS_EPISTEMIC_ROBUSTNESS_PROBE_2026_09_16.md)：證據不足時的保留未知、抗過度敘事、修正；**不代表 CCTS 學習效果已建立**。
- [Provenance-First Position Paper](../POSITION_PAPER_PROVENANCE_FIRST.md)：敘事不可取代來源、原件與授權。

## 7. 外部參照 / External references

1. Anthropic Claude Help Center, *Use Claude’s chat search and memory to build on previous context*: https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context — 產品功能說明；屬供應商自述，不是本案驗證。
2. Anthropic Claude Help Center, *Use incognito chats*: https://support.claude.com/en/articles/12260368-use-incognito-chats — 關閉記憶與無痕模式的差別、個人設定可能仍可用。
3. Jain, S., Park, C., Viana, M., Wilson, A., & Calacci, D. (2026), *Interaction Context Often Increases Sycophancy in LLMs*, CHI 2026. https://doi.org/10.1145/3772318.3791915 — 研究互動脈絡對部分模型迎合行為的異質性影響；**不等於本個案的敘事生成機制已確證**。

---

**Human review gate / 人工審閱關卡**：僅供檢視與反證，未授權擴張程式、抓取第三方對話、重啟具身研究、合併 `main`、部署或對外發布科學結論。
