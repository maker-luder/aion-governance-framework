# CCTS 區辨與結果效度：研究規格候選（2026-10-03）

狀態：`RESEARCH_SPEC_CANDIDATE / IMPLEMENTATION_NOT_JUSTIFIED / SCIENTIFIC_HOLD`。本文件只處理 Co-Constructed Thinking Space（CCTS，共構思考空間）、Human–AI Learning（人機學習）及 Human–AI Collaboration（人機協作）。它是**未經預註冊的研究設計候選**，不是新量表、實證資料、已凍結的工程規格或既有已典藏 CCTS 物件的修訂。`main` 建立時 SHA：`6a34d7780dd6d5bc717cd6c82ba39e7a6241c2fd`；本工作線建立時 SHA：`2452aec3d7ce1afe6dae216dac0c3050944f5bce`。這些是來源快照，執行前必須重新核對 live state。

## 1. 來源與主張上限

- `HUMAN_ORIGIN`：小博原始提出共構思考空間；本輪指定「區辨效度」和「結果效度」為首要問題，並指定不合併、不發布及人工把關。
- `REPOSITORY_STATE`：既有 [CCTS 形式化](../CO_CONSTRUCTED_THINKING_SPACE_FORMALIZATION_2026_09_16.md)定義核心及較強的長期倉庫 profile；[grounding 准入](../CCTS_GROUNDING_ADMISSION_EXTENSION_2026_09_16.md)、[認知修訂](../CCTS_ADVERSARIAL_EPISTEMIC_REVISION_PROTOCOL_2026_09_23.md)、[適用邊界](../CCTS_HUMAN_AI_LEARNING_APPLICABILITY_BOUNDARY_HYPOTHESIS_2026_09_30.md)已有相應控制。適用邊界的既有反審查判定不支持另建獨立 applicability 構念。
- `AI_FORMALIZATION`：本文件的對照矩陣、反例測試、測量候選及停止條件是本輪分析提議；不是對小博原始術語的溯及歸屬。
- `EXTERNAL_SOURCE`：下節論文只支援相鄰方法、替代解釋或特定樣本結果；一篇也沒有測量此倉庫的 CCTS。
- `IMPLEMENTATION_EVIDENCE`：現有 Python 合成契約能驗證指定欄位、摘要與匹配安排；無真實人類的獨立學習觀測。程式存在不等於構念正確。

```text
CCTS_VALIDATION = NOT_ESTABLISHED
HUMAN_LEARNING = NOT_ESTABLISHED
RETENTION = NOT_ESTABLISHED
TRANSFER = NOT_ESTABLISHED
CCTS_SPECIFIC_EFFECT = NOT_ESTABLISHED
CAUSALITY = NOT_ESTABLISHED
HUMAN_AI_SYNERGY = NOT_ESTABLISHED
```

## 2. 本輪外部來源核對（只取對應範圍）

| 來源、出版狀態與識別碼 | 實際設計／發現 | 對本研究的用途與限制 |
| --- | --- | --- |
| Vaccaro, Almaatouq & Malone (2024), *Nature Human Behaviour* 8:2293–2303；[DOI 10.1038/s41562-024-02024-1](https://doi.org/10.1038/s41562-024-02024-1) | 同儕審查的系統回顧與統合分析：74 篇文章、106 項實驗、370 個效果量；所納研究的平均人機表現優於單獨人類，卻低於人類／AI 單獨表現的較佳者。 | 要記錄 Human alone、AI alone、Human+AI；其研究任務與樣本不是 CCTS，平均數不能外推每種人機合作。 |
| Järvelä, Nguyen & Hadwin (2023), *British Journal of Educational Technology* 54:1057–1076；[DOI 10.1111/bjet.13325](https://doi.org/10.1111/bjet.13325) | 同儕審查的理論／方法文章，提出 trigger（觸發事件）概念與 Human–AI Shared Regulation in Learning（HASRL，人機共享學習調節）模型，以既有實例說明 AI 支援 SSRL 的可能性。 | 這是相鄰調節框架與方法來源，不能把模型提案或例子讀成已測得 CCTS 特定的持久學習增益。 |
| Edwards, Nguyen, Lämsä, Sobocinski, Whitehead, Dang, Roberts & Järvelä (2025), *British Journal of Educational Technology* 56:712–733；[DOI 10.1111/bjet.13534](https://doi.org/10.1111/bjet.13534) | 同儕審查的 MAI 設計與示範：52 名職前教師、14 組、60 分鐘任務；語音介入以 Wizard of Oz（人類模擬系統能力）處理。作者報告對 socially shared regulation of learning（SSRL，共同調節學習）的語言影響不清楚，能力／可靠性感知較低。 | 角色清晰與可靠性感知是調節／替代解釋候選；不能宣稱介入已促進 CCTS 或長期學習。 |
| Wu, Lee, Chai & Tsai (2025), *Educational Researcher* 54(6)；[DOI 10.3102/0013189X251333628](https://doi.org/10.3102/0013189X251333628) | 同儕審查的**概念文章**，討論學習者的 epistemic stance（知識判斷立場）與 human epistemic agency（人類知識判斷主導權）；不是本研究的效果試驗。 | 概念重疊很大；「shared epistemic agency」在該文是理論用語，不能反推本倉庫已有被證明的共享心智或主導權。 |
| Saqr, Misiejuk & López-Pernas (2026), *The Internet and Higher Education* 70:101087；[DOI 10.1016/j.iheduc.2026.101087](https://doi.org/10.1016/j.iheduc.2026.101087) | 同儕審查的互動時序分析，把一些學生互動描述為 instruct–serve–repeat（指令、服務、重複）；觀察性互動分類不等於學習因果試驗。 | 普通助手使用的強負例；互動多輪、提示變長或任務完成都不能直接算雙向修訂。 |
| Li, Wang, Yang, Guo, Liu & Wen (2026), *Information Processing & Management* 63(6):104711；[DOI 10.1016/j.ipm.2026.104711](https://doi.org/10.1016/j.ipm.2026.104711) | 同儕審查論文提出 CCD；[作者程式庫](https://github.com/arenceLi/CoCoDial)公布 1,460 段跨八領域的生成對話與評估。論文檢索文本稱 *Cognitive Collaboration Dialogue*，程式庫 README 稱 *Cognitive Collaborative Dialogue*；需保留原文版本差異。 | 漸進式問題對齊、相互協調與軌跡修正高度重疊。生成資料及任務完成指標不能替 CCTS 做獨立區辨或人類學習驗證。 |
| Zhang, Meng, Feng & Lin (2026), AIED 會議論文，頁 318–326；[正式 DOI 10.1007/978-3-032-29770-9_35](https://doi.org/10.1007/978-3-032-29770-9_35)，另有 [arXiv:2604.08344](https://arxiv.org/abs/2604.08344) | 平行組隨機實驗，71 名大學生；GenAI 可用與不可用組的人類對話調節模式不同，向 hybrid co-regulation（人機混合共同調節）移動。 | 誰設定目標、監控、修補與結案可作次要過程測量；不同調節分布不等於 CCTS 的獨立效度或學習效果。 |
| Lu, Yan, Huang, Yin & Zhang (2025), *Group Decision and Negotiation* 34:235–271；[DOI 10.1007/s10726-024-09912-x](https://doi.org/10.1007/s10726-024-09912-x)；2024-12-03 先行發表 | 三項線上、兩階段、受試者間情緒分類實驗；人機雙向學習並非自動產生，回饋與工作流可能造成不均或負效果。 | 個體分離後的表現是有用的 outcome 類型；任務、AI 更新機制與樣本不可直接外推 CCTS。 |
| Fan 等 (2025), *British Journal of Educational Technology* 56:489–530；[DOI 10.1111/bjet.13544](https://doi.org/10.1111/bjet.13544) | 117 名大學生、寫作任務的隨機比較；論文報告 ChatGPT 組短期文章分數改善，但知識獲得與遷移未顯著優於對照。 | 即時作品改善與獨立知識／遷移必須分開；單一任務不能當 CCTS 反證或證明。 |
| Riedl, Savage & Zvelebilova (2026), *ACM Transactions on Computer-Human Interaction*；[DOI 10.1145/3805039](https://doi.org/10.1145/3805039) | 作者機構摘要報告兩項隨機實驗：AI 曝光後的人與人互動有語言、注意、共享心智模型及社會凝聚的 spillover（外溢）變化。 | 只列為次要新問題；來源描述是特定設計的 AI 曝光效果，不是本倉庫 CCTS 外溢效果。 |

Wolfram 的語意查詢對構念區辨沒有可用結果；Scite 此輪查詢回 `INVALID_ARGUMENT`，未取得其引文分類，不能當作已完成反證檢索。Consensus 的結果已對 Lu、Fan 取得個別記錄，重要結論另以出版者或作者機構來源核對。Hugging Face 的 [Qwen/Qwen3-8B 模型卡](https://huggingface.co/Qwen/Qwen3-8B)只表明模型版本／設定可追溯的工程例子；沒有跑模型，也不能用它解釋特定互動。

## 3. 區辨矩陣：`NOVEL_LABEL != DISTINCT_CONSTRUCT`

| 鄰近現象／構念 | 主要重疊 | 可能的 CCTS 剩餘部分及最低可觀測證據 | 若觀測不到的處置 |
| --- | --- | --- | --- |
| 普通助手使用；instruct–serve–repeat | 人給任務，AI 回答，可能多輪 | 有具時間順序的雙向**實質**挑戰與修改，且修改了同一問題的可核對內容 | 不標 CCTS；多輪數量不是證據 |
| prompt refinement（提示改寫）；ordinary iterative dialogue（一般反覆對話） | 人反覆改寫需求，AI 跟著修稿 | 保留人與 AI 各自的原始主張、互相反駁、拒絕分支、來源和主張上限；盲碼者能指出雙向實質差異 | 若只能見到人改提示、AI 順從，降為反覆提示 |
| CCD（認知協作對話） | 漸進對齊、協調、問題軌跡更新 | 外部證據到具體主張的來源鏈、權限分離、被拒假說與跨次重入之同一 artifact 綁定 | 若這些只是紀錄格式，將 CCTS 重述為 CCD 類互動的倉庫治理 profile |
| SSRL／co-regulation／HASRL（共同或混合調節學習） | 目標、監控、修補、策略調整 | CCTS 的 provenance（來源追溯）、主張邊界和決策權限可測，卻未必是新的心理構念 | 調節動態只作次要測量；不新增 CCTS 必要欄位 |
| Human–AI teaming／shared mental models（人機團隊／共享任務模型） | 互補工作、任務協調、共同表示 | 以來源鏈和反例留存檢查研究主張的可重建性 | 若現有 teamwork 加研究治理已解釋資料，降級為方法 profile |
| distributed cognition／interactive team cognition（分散式認知／互動團隊認知） | 人、工具、artifact 與時間構成任務系統 | 可稽核的 actor 與 authority 分離、每次重入的版本及拒絕鏈 | 系統層描述絕非共享意識；沒有新增預測即不要宣稱獨立構念 |
| epistemic co-agency（知識共同能動性） | 質疑、修正、人類判斷責任 | 觀察的是治理及主張來源，而非兩者主體同一性 | 若不能提供增量區辨，把 CCTS 保留作研究流程名 |

候選「獨特剩餘」目前更像 **provenance-bounded research/governance profile（來源有界的研究治理型態）**。其組合是否具有超過鄰近構念的增量效度尚未知；獨特紀錄格式也可能只是工程便利。先允許 `DOWNGRADE_TO_METHOD_PROFILE`，不要保護名稱免於反證。

## 4. 首要問題 A：區辨效度之最小研究設計候選

1. **單位與材料**：事先界定 task、一次連續互動 episode、其後 artifact/re-entry；保留原始順序和版本。用有權使用且已去識別的真實互動，另保留人工合成負例作編碼訓練，不把合成例算入實證結果。不得只從已通過 CCTS manifest 的樣本抽樣。
2. **比較類別**：一般單次助手；人改提示／AI 順從；多輪共同釐清但無雙向修訂；CCD 型軌跡；帶來源／權限鏈而無實質互修；有互修但無可重建來源鏈；候選 CCTS。加入困難的近鄰反例，不用容易區分的短對話灌高準確率。
3. **盲碼**：先獨立定義「實質修訂」與「只是改寫格式」；至少兩位不知道候選標籤與 outcome 的編碼者，記錄分歧、協議程序與可靠度；不能讓編碼者只因看見欄位名就判定 CCTS。原始資料與 typed manifest 分開封存。
4. **最低證據**：同一問題的前後主張及反例、Human→AI 和 AI→Human 的可定位修訂、來源到主張的鏈、權限與最後決策、被拒分支的內容或指標；長期 profile 另需可重建的跨次 artifact 版本。摘要雜湊只能證明綁定，不能證明語意、品質或真實 actor 身分。
5. **增量檢驗**：先以 CCD／SSRL／team cognition 等相鄰編碼預測分類或獨立 outcome，再加入 CCTS 候選剩餘項；報告盲碼一致性、近鄰誤判、增量預測及不確定區間。分析方案、樣本選取與判定界限須在看結果前凍結。沒有增量或可靠辨識時，`DOWNGRADE_TO_METHOD_PROFILE`，不得用事後重命名救回假說。

現況：倉庫 `co_constructed_thinking_space.py`、`epistemic_revision.py` 的確能拒絕一向互動、澄清邊偽裝實質修訂、缺少 grounding 和摘要不一致；但資料是 typed synthetic declarations（帶型別的合成宣告）。**自然語料的語意編碼準則、獨立標註樣本與跨編碼者測量均未完成**，因此首要問題 A 尚不能凍結為程式接口。

## 5. 首要問題 B：結果效度之最小研究設計候選

結構通過記作預測變項／過程狀態，不作結果。預先分開：`INDEPENDENT_HUMAN_JUDGEMENT`（關閉 AI 的個人判斷）、`IMMEDIATE_PERFORMANCE`、`DELAYED_RETENTION`（預定延遲的個人回憶或運用）、`HELD_OUT_TRANSFER`（未見任務的個人運用）、`INDEPENDENT_RECONSTRUCTION`、`ERROR_DETECTION`、`CALIBRATION`、`TASK_PERFORMANCE`。逐一宣告評分規則、盲評、測量時點；未量測填 `NOT_OBSERVED`，不能拿 `NOT_ESTABLISHED` 當零分。

最小對照考慮：人類獨立前測、AI 單獨任務表現、人機合作、非 CCTS 但匹配資訊量／時長／練習／測驗暴露的互動；配對同一任務家族與困難度，held-out 另有未見內容。記錄先備知識、自我調節學習、AI literacy（AI 素養）、初始獨立表現、模型版本與生成設定、角色說明與可靠性感知。測量本身可能造成 retrieval-practice（提取練習）效果；評估是否需要不立即測驗的對照。人類自生策略及組間污染要記錄。能比較的隨機化／交叉安排、樣本量、延遲時長、缺失資料規則及主要 outcome 都必須預先指定；未指定時只有候選設計。

`LEARNING_CONTRAST_DESIGN` 已有五臂、matched non-CCTS practice comparator（匹配的非 CCTS 練習比較組）、曝光序列、先備知識摘要、即時／延遲 assessment events（評估事件）、AI-withheld（不給 AI）獨立判斷與 held-out 任務綁定。它**只審核設計聲明**，`FalsifierOutcome` 是宣告值；沒有人的真實分數、盲評與統計識別。不要複製 adapter 或把欄位合格解讀為效果。Human+AI 是否勝過較佳單獨基線為次要 synergy 問題，與 CCTS 結構及學習分開。

## 6. 對抗式替代解釋（A–H）

| 競爭說明 | 何時支持；何時削弱 | 反證條件與可量測區分 | 現有控制／缺口 |
| --- | --- | --- | --- |
| A 既有協作／調節構念加治理包裝 | 若去掉來源欄仍可同樣分類／預測則支持；若新增欄在盲碼與獨立結果上有穩定增量則削弱 | 預先比較近鄰模型與新增項的增量、近鄰誤判；增量持續為零是獨立構念主張的反證 | 形式化有概念 crosswalk；**無**自然樣本增量比較 |
| B 雙向修訂只是普通 iterative prompting | 若 AI 只是順應人改寫則支持；雙方各有可定位的反證、被改主張則削弱 | 原始 turn 與內容差異的雙向盲碼；若無 AI→Human 實質挑戰，CCTS 候選不成立 | 圖上雙向邊與修訂 trace 已有；**無**語意獨立判定 |
| C 學習增益來自反覆曝光／練習 | 匹配曝光後增益消失則支持；在等量曝光比較仍有預先指定差異則削弱 | 曝光量、任務順序、提取測驗與回饋的匹配；無差異反駁特定增益 | matched comparator／暴露摘要有；**無**實際人類結果 |
| D held-out 表現來自先備知識 | 前測充分解釋後測差異則支持；分層／配對後仍有差異則削弱 | 盲評先備測量、基線分層、同域不同題；零增量反駁學習效果 | prior-knowledge digest／AI-withheld 前測有；**無**量表效度與資料 |
| E 表現增益來自 AI 品質 | 模型／設定改變跟著結果走則支持；固定模型／跨模型再現較削弱 | 固定版本、提示、工具、AI-alone 表現；替換模型後消失反駁一般化 | 角色與條件分離有；**無**模型品質操弄資料 |
| F 長期變化來自 Human 自生策略 | AI 不在場仍自行發展策略且非 CCTS 組相同則支持；預註冊條件差異較削弱 | 策略形成時間、AI-withheld 再測、跨人配對；同樣變化反駁特定歸因 | 長期重入／獨立條件有；**無**識別自生策略的真實時序 |
| G 角色清晰／可靠性感知驅動 | 控制這兩者後差異消失則支持；匹配後仍有差異則削弱 | 相同角色說明與可靠度、分開測知覺；匹配後消失反駁 CCTS 特定解釋 | 來源角色結構有；**無**知覺測量 |
| H 合作沒有 synergy，甚至下降 | 人機低於較佳單獨基線則支持；高於兩者且可信區間排除無差異才削弱 | 同一 outcome 的 Human alone、AI alone、Human+AI；勝過人類 alone 不足以稱 synergy | 獨立人類基線候選有；**無**一致的 AI-alone／真實人機分數 |

## 7. 去重與最小工程交接（尚未啟動）

**重用**：`research-labs/human-ai-longitudinal-study_v0.1.0/src/aion_human_ai_longitudinal/` 中 `co_constructed_thinking_space.py`（核心結構）、`epistemic_revision.py`（反證與拒絕鏈）、`ccts_human_epistemic_agency.py`（獨立判斷／held-out）、`learning_contrast_design.py`（五臂比較）、`task_selection_exposure.py`（暴露及任務控制）、`empirical_gate.py`（防止結構狀態循環當效果）。對應 `tests/test_*.py` 已有合成反例。**本輪新增**：只有此候選研究文件。**不新增** applicability gate、learning construct、revision／agency／contrast adapter、longitudinal harness 或第二套 synthetic fixture。

將來若人類審閱並凍結兩個首要研究問題，最小工程順序為：(1) 在現有研究套件旁建立**研究設計資料介面**，保存盲碼來源、負例類別、預定 outcome 和評分者盲態；(2) 重用現有匹配比較器並將真實觀測與 synthetic fixture 強制分離；(3) 預定好樣本、編碼手冊、指標、缺失處理及失敗門檻後才考慮執行。新 module 是最後選擇，secondary/moderator 不變成核心 gate。

交接條件：先 live-verify `main`、`research/ccts-human-ai-learning-lane`、PR、diff 與 Actions；只在與 #264 無關的 CCTS 工作線或其隔離分支改動；列出具體檔案與接口、負例、targeted tests、整包測試、型別及品質檢查；任何新 head 重新驗證本地與遠端 CI。`SYNTHETIC_DISCRIMINATION != EMPIRICAL_DISCRIMINANT_VALIDITY`；`SYNTHETIC_OUTCOME_FIXTURE != HUMAN_OUTCOME_OBSERVED`。新 PR 應是 DRAFT，禁止 merge。授權界限：`MERGE_TO_MAIN = NO / PUBLISH = NO / DEPLOYMENT = FALSE / CANONICAL_EFFECT = NONE / HUMAN_GATE = REQUIRED`。

### 解凍前的明確接受條件

- 盲碼手冊可以重現「實質雙向修訂」與近鄰互動的區別，預先指定多位編碼者的一致性報告與差異處理；不能由 manifest 欄位自動給自己標籤。
- 事前註明 CCTS 被 CCD、SSRL 等鄰近構念吸收時的 downgrade 規則；既有敘事不得充作 validation。
- 主要 outcome、延遲、held-out 題、AI-withheld 條件、Human／AI alone 基線、評分規則及樣本排除條件事前凍結，保留零或負結果。
- 已確認可以合規取得並隔離真實觀測，明定 actor/provenance 與隱私；合成資料只用於工程 QA。

任何一項未定：`IMPLEMENTATION_NOT_JUSTIFIED`。這是目前判定；不能為了交付程式擅自補答案。
