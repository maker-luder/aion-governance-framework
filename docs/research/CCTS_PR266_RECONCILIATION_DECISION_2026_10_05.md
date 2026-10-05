# PR #266：CCTS／人機協作／人機學習逐檔對帳與實作判定

> 後續狀態更新：Human + Teacher 已完成 Phase B，另行授權最小 QMS 信任邊界修正。當前工程處置見 [Phase C 實作收據](PR266_COLLABORATION_TRUST_BOUNDARY_2026_10_05.md)。以下矩陣與 HOLD 是 Phase A 歷史判定；效度／學習介面仍 HOLD。

狀態：`PHASE_A_RECONCILIATION / PHASE_C_RUNTIME_HOLD / SCIENTIFIC_HOLD`。這是依 [PR #266 操作手冊](CCTS_HUMAN_AI_COLLABORATION_LEARNING_IMPLEMENTATION_HANDOFF_2026_10_05.md)完成的本輪對帳收據；不是實證預註冊、合併授權或已通過的研究結果。

## 1. 即時狀態與授權邊界

2026-10-05，本輪重新讀取 GitHub、完整 Git 物件、PR metadata、兩個精確分支及 Actions：

```text
REPOSITORY = maker-luder/aion-governance-framework
MAIN = a38a1b5269be99d0af7f25495e49d479608b5dcf
SOURCE_LANE = research/ccts-human-ai-learning-lane
SOURCE_LANE_HEAD = fa85a7f30ec77007280aa4957bd71a74c3a8683f
MERGE_BASE = 6a34d7780dd6d5bc717cd6c82ba39e7a6241c2fd
LANE_VS_MAIN = DIVERGED / AHEAD 8 / BEHIND 9
PR_265 = CLOSED / DRAFT / NOT_MERGED
PR_265_HISTORICAL_HEAD = 8e22da9396b0dbb9569f09330dad4d704a0355a9
PR_266_AT_READ = OPEN / DRAFT / HEAD a8d5670762f566b33ff626d116170783614f492e
OTHER_OPEN_PRS = 0
LANE_DELTA = 17 FILES / +2787 LINES / -0 LINES
```

小博本輪明確要求「PR266 請實作」；這是**新的工程工作授權**，不等於同意把全部 lane 內容移植、凍結研究問題、執行真人實驗或合併。操作手冊第 11、13、14 節要求先完成對帳與研究問題凍結準備，遇到核心未知則 `HOLD`。本輪實作這一必要的對帳產物，保留程式移植的審查閘門。

PR #266 原本是文件 PR；本次在其既有分支更新審查文件，以遵守一次一個 active PR 的偏好。這並不使該分支成為已核准的 runtime integration branch。

## 2. 與 current main 的逐檔矩陣

以下 `main 等價處` 指現有可重用的控制或已證實缺口；`PORT` 只有在門檻通過後才可能成為決定。`NARROW` 是縮小候選，不是已移植。`HOLD` 不代表來源無價值。

| Lane 差異（相對 merge base） | main 等價處／真正新增 | 科學與證據角色；重複／過時風險 | 判定及回歸要求 |
| --- | --- | --- | --- |
| `docs/research/ccts-human-ai-learning/CCTS_DISCRIMINANT_OUTCOME_STUDY_SPEC_2026_10_03.md` | main 已有 CCTS 形式化、適用邊界與學習對照；新增研究問題 A／B、近鄰負例與測量候選 | 規格候選；高：較新的 SIGDIAL／互補性比較尚未寫入舊版，且文件自述未凍結 | **NARROW**：只把可反證問題留在本 PR；不把舊候選標為已凍結。檢查近鄰及結果邊界 |
| `docs/research/ccts-human-ai-learning/LONGITUDINAL_ALIAS_FALSIFICATION_2026_10_03.md` | main 有 re-entry、學習對照及 CCTS provenance；新增一個「簡稱回憶不充分」合成反例的設計與歷史解釋 | 合成方法／歷史紀錄；中：可能把 fixture 誤讀成長期理解證據 | **HOLD** 於來源支線；只在對帳中引用。若獨立重入，先重審單一問題與負例 |
| `docs/research/ccts-human-ai-learning/PR265_HUMAN_AI_COLLABORATION_QMS_DEDUP_DECISION_2026_10_03.md` | main 有 Full-QMS、NCR/CAPA、Human review boundary；新增六控制的去重分析 | 工程設計紀錄；高：main 後增分支拓樸 validator | **NARROW** 為本矩陣的 QMS 候選，不能照搬舊「六項全部需要新碼」判定 |
| `docs/research/ccts-human-ai-learning/PR265_HUMAN_AI_COLLABORATION_QMS_IMPLEMENTATION_HANDOFF_2026_10_03.md` | 本 PR 的新 handoff 已取代其當前入口；舊文件保存 #265 情境 | 歷史交接；高：舊 base／PR head／拓樸前提 | **HOLD**，只留 durable lane 作 provenance，不複製成另一份權威操作手冊 |
| `docs/research/ccts-human-ai-learning/README.md` | main 首頁／研究地圖已連結專用支線；新增該支線入口 | 導覽；低 | **DROP** main 移植；來源支線繼續保存 |
| `research-labs/coupled-cognition-quality-factory_v0.1.0/docs/END_TO_END_RESEARCH_QMS.md` | main 已有現行 Full-QMS 說明；新增六控制章節 | 工程文件；中：若未移植 code 會形成虛假的 main 能力 | **HOLD**；只有對應執行介面經測試入 PR 才更新 main 的能力敘述 |
| `.../aion_coupled_quality/__init__.py` | main 出口不含 collaboration control；lane 新增匯出 | 公開 API；中：依賴下列尚未重審模組 | **HOLD**；須先確定最小介面及 API 相容測試 |
| `.../aion_coupled_quality/extended_quality.py` | main 的 `FullQualitySystemEngine`、trace refs、management review 已存在；lane 加可選 assessment seam | 治理執行介面；高：assessment 可直接建構，consumer 只看 disposition／型別，未重新計算輸入 | **NARROW 候選**；先有偽造 READY、`replace`、缺 trace、HOLD 傳遞的負測試，才能決定接法 |
| `.../aion_coupled_quality/human_ai_collaboration.py` | main 已有 Human gate、NCR/CAPA、分支拓樸 validator；lane 新增六種 typed record、評估器 | QMS 工作流程；高：來源欄是自述，`LIVE_HUMAN_AUTHORIZATION` enum 值本身不驗真；branch readiness 與目前拓樸治理部分重疊 | **NARROW 候選**；不得把記錄欄位當權限。先定義可信 receipt 綁定與現有拓樸 validator 的責任邊界 |
| `.../tests/test_extended_quality.py` | main 有完整 Full-QMS 回歸；lane 新增 seam 整合例 | 合成工程測試；中：只檢查善意建構的 assessment | **HOLD**；若 port seam，增補 direct-construction 與 management-review 漏綁負例，重跑全套 |
| `.../tests/test_human_ai_collaboration_controls.py` | main 無六控制的專項測試；lane 有盲重試、stale SHA 等負例 | 工程測試；中：未證明 live authorization 來源與實際 repo 相符 | **NARROW 候選**；測試先行，加入 forged READY／替換欄位／來源不實與拓樸衝突案例 |
| `research-labs/human-ai-longitudinal-study_v0.1.0/CCTS_VALIDITY_STUDY_DESIGN.md` | main 已有學習對照與 CCTS 人類獨立判斷設計；lane 新增雙效度欄位手冊 | 研究方法候選；高：可能把 completeness 當實證 readiness | **HOLD**；先凍結兩個研究問題、編碼手冊及 outcome |
| `.../aion_human_ai_longitudinal/__init__.py` | main 已輸出舊學習對照；lane 輸出新 validity 與 longitudinal types | 公開 API；中：擴大未凍結的 study surface | **HOLD**，不單獨移植 |
| `.../aion_human_ai_longitudinal/ccts_validity_study_design.py` | main `learning_contrast_design.py` 已有四 CCTS representation 加 matched non-CCTS、曝光、AI-withheld 與 held-out；lane 新增欄位覆蓋檢查與鄰近 enum | synthetic design；高：重複 adapter、enum 完整不等於自然語料辨識 | **HOLD**；無人類 outcome／盲碼證據，不新增 empirical runner |
| `.../aion_human_ai_longitudinal/longitudinal_falsification.py` | main `reentry_metrics.py` 已有重入量測；lane 新增結構化 forced-choice cue fixture | 合成反證方法；中：固定答案鍵及任務條件不能外推理解 | **HOLD**；先評估是否能作獨立有限測試，不綁進核心 CCTS admission |
| `.../tests/test_ccts_validity_study_design.py` | main 有學習對照及 agency 測試；lane 新增欄位合格負例 | 工程測試；高：若只 port tests 會重新建立未凍結的公開介面 | **HOLD**，與候選程式一同重審 |
| `.../tests/test_longitudinal_falsification.py` | main 有 re-entry 與 learning contrast 測試；lane 新增單一合成 cue fixture | 工程測試；中：玩具答案鍵不等於 Human outcome | **HOLD**，不把合成結果提升為科學結論 |

以上相對路徑的 `...` 分別承接表中最近的完整套件路徑；檢索以來源支線的 `git diff main...research/ccts-human-ai-learning-lane --name-status` 為準。所有 17 項的 `CLAIM_EFFECT = NONE`、`HUMAN_GATE_REQUIRED = YES`；沒有任何一項可直接 `PORT`。這是對 **現在** 的 main 作出的判定，不追溯否定先前支線的工程投入。

## 3. 文獻對照與可反證問題

| 第一手來源 | 支持到哪裡 | 不支持與本輪差異判斷 |
| --- | --- | --- |
| [Liu 等，SIGDIAL 2026，ACL Anthology，DOI 10.18653/v1/2026.sigdial-1.48](https://aclanthology.org/2026.sigdial-1.48/) | 兩層對話編碼含認知／非認知解題與後設認知調節；摘要稱跨九個資料集示範，後設認知調節可區分較深合作 | 未測 repository-defined CCTS、來源權限與長期綁定。近鄰基線應增加 dialogue/metacognitive coding，不能只和「普通提示」比較 |
| [Gonzalez 等，PNAS Nexus 2026，DOI 10.1093/pnasnexus/pgag030](https://academic.oup.com/pnasnexus/article/5/3/pgag030/8490283) | 跨領域**框架論文**，把 reasoning、memory、attention、meta-coordination、governance 與角色／信任納入互補性分析；互補性要求人機組合超越任一單獨基線 | 並未直接驗證 CCTS；CCTS 的 provenance／authority 可能只是 governance profile，不能因框架收錄治理就推定結果增益 |
| [Vaccaro 等，Nature Human Behaviour 2024，DOI 10.1038/s41562-024-02024-1](https://www.nature.com/articles/s41562-024-02024-1) | 既有 PR review 引用的統合分析提醒 augmentation 與 synergy 不同 | 整體平均不能代替本倉庫的受試者、任務或 CCTS 對照 |
| [Fan 等，British Journal of Educational Technology 2025，DOI 10.1111/bjet.13544](https://bera-journals.onlinelibrary.wiley.com/doi/10.1111/bjet.13544) | 既有 PR review 引用的寫作實驗提醒即時作品改善不能代表知識／遷移改善 | 未測 CCTS，亦不能從未顯著直接推出任何設定下都無學習 |

**區辨問題候選：** 在同一任務與原始互動上，先由盲碼者按對話／調節、CCD、共同問題空間及 team governance 既有構念編碼，再加入可重建的雙向實質修訂、主張來源／決策權限、被拒分支與跨次 artifact 綁定，後者是否對獨立標籤或結果有**預先規定的增量**？尚缺：自然語料取樣、編碼規則、獨立近鄰操作化、可靠度與判定界限，因此 `DISCRIMINANT_QUESTION = CANDIDATE_NOT_FROZEN`。

**結果問題候選：** 在 Human-alone、AI-alone、匹配非 CCTS 人機互動及候選 CCTS 條件下，先指定一個 AI withheld 的人類獨立判斷或 held-out transfer 為主要結果，另列即時表現、延遲保持、重建、錯誤辨識與校準；控制先備知識、曝光／練習、模型與角色差異。尚未選定唯一主要結果、延遲與評分、樣本／分派、缺失資料、污染及比較界限，因此 `OUTCOME_QUESTION = CANDIDATE_NOT_FROZEN`。

**預定降級路徑：** `SUPPORTED_CANDIDATE`、`NARROWED`、`ABSORBED_INTO_EXISTING_CONSTRUCT`、`DOWNGRADE_TO_METHOD_PROFILE`、`FALSIFIED_SPECIFIC_CLAIM`、`INCONCLUSIVE`、`HOLD`。若既有對話／調節／團隊框架充分解釋資料、CCTS residual 無穩定增量，停止新構念擴張並降級或吸收；若缺可靠編碼或可用資料，保持 `HOLD`。這是**事前處置方向**，尚非已凍結的統計決策規則。

## 4. 工程結論與下一個閘門

目前能完成且不越過研究邊界的實作是本逐檔去重判定與問題規格整理。程式移植仍遇到兩個具體阻礙：

1. 科學設計的主要 outcome、近鄰編碼及降級界限未凍結；移植 `ccts_validity_study_design.py` 會讓新公開介面先於問題。
2. 六控制 QMS 的候選 consumer 接受可直接建構的 assessment；聲稱 `LIVE_HUMAN_AUTHORIZATION` 也是呼叫端宣告，非 live 授權查證。加上現在的分支 validator，直接照搬會留下權限與責任重疊。

```text
PHASE_A_RECONCILIATION = MATERIALIZED_FOR_REVIEW
PHASE_B_HUMAN_TEACHER_REVIEW = PENDING
PHASE_C_RUNTIME_PORT = HOLD
NEW_CONSTRUCT = NO
EMPIRICAL_DATA = NONE
SCIENTIFIC_CLAIM_CHANGE = NO
MERGE_AUTHORITY = NONE
BRANCH_DELETION = NONE
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

下一個唯一決策：複審本矩陣與兩個研究問題，指定是否**只針對 QMS 六控制中的最小缺口**另做有界工程設計，並以直接建構／來源不實負測試先行；效度研究介面保持 `HOLD`。若選擇不新增程式，保留 `NO_NEW_IMPLEMENTATION_REQUIRED`，不以「最大移植量」代替研究進展。

本輪沒有繼承 #265 舊 head 的 348 tests；PR #266 原 head 的 CodeQL 已完成，但 Quality 與 Branch Topology 因已合併 #264 的殘留 transient branch 失敗，Main Transition Authority Gate 因缺合併授權收據而 HOLD。修改此文件後必須對**新 head**重讀 CI。
