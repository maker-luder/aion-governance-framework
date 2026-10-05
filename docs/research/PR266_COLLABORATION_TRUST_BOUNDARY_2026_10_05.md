# PR #266：人機協作 QMS 信任邊界的有界實作

## 授權、來源與狀態

2026-10-05，Human + Teacher 完成 Phase B，使用者另行明確授權 Phase C **只修正人機協作 QMS 的 READY 信任邊界**。本文件是該次授權的工程收據，更新先前 [Phase A 對帳](CCTS_PR266_RECONCILIATION_DECISION_2026_10_05.md)的工程處置；研究問題仍未凍結。

```text
REPOSITORY = maker-luder/aion-governance-framework
MAIN_AT_START = a38a1b5269be99d0af7f25495e49d479608b5dcf
PR266_AT_START = 41098bc514c6f9113748ac8ef4af34e214a288b2
SOURCE_LANE = research/ccts-human-ai-learning-lane
SOURCE_LANE_AT_START = fa85a7f30ec77007280aa4957bd71a74c3a8683f
SOURCE_VS_MAIN = DIVERGED / AHEAD 8 / BEHIND 9
PR_STATE = OPEN / DRAFT
PHASE_B_HUMAN_TEACHER_REVIEW = COMPLETED
PHASE_C = BOUNDED_IMPLEMENTATION
IMPLEMENTATION_AUTHORIZED = YES
MERGE / PUBLICATION / BRANCH_DELETION / EMPIRICAL_EXPERIMENT = NOT_AUTHORIZED
DEPLOYMENT = FALSE
```

開始前重讀 GitHub：唯一 open PR 為 #266；六個分支包含四個保留分支、#266 工作分支，以及已合併 #264 的殘留 `docs/three-line-research-navigation-20261002`。此殘留造成既有 topology failure，不以刪除分支處理。

## 已確認的失敗模式與最小修正

缺陷確認於上述 **source lane**：caller 可直接建構 `HumanAICollaborationQualityAssessment(READY_FOR_HUMAN_REVIEW)`；來源 consumer 只信任型別、disposition（處置）與 control id，未執行六控制評估。空 reasons、偽造理由、將 HOLD 用 `dataclasses.replace()` 改為 READY 都能進入 Full-QMS READY 路徑。未建立 current main 已有此缺陷的證據：main 原先沒有此 integration seam。

| 決定 | 對應失敗模式與限制 |
| --- | --- |
| `ExtendedQualityControls.human_ai_collaboration` 只收原始 controls 的 tuple | 報告不再是輸入通行證；直接建構或 replace 報告均遭 `QualityError` 拒收 |
| `FullQualitySystemEngine.assess()` 每次呼叫可信 evaluator | 六項原始紀錄在 consumer 內重新評估；任一 HOLD 傳遞至 Full-QMS HOLD |
| 原始 controls 與六個巢狀 record 的型別／欄位重新驗證 | frozen dataclass 不被視為安全邊界；先前遭 `object.__setattr__` 破壞的欄位會重新驗證 |
| 管理審閱須包含 control id 及內容摘要 trace | 同 id 改內容、改 id、用舊 trace 都不會沿用舊審閱 |
| 宣告 current SHA 須列入 quality plan 的 `configuration_refs` | `git:{current_state_sha}` 缺失時 HOLD；presented/current SHA 不等也 HOLD |
| 評估報告固定科學／行動權限上限 | 建構及 replace 均不可提升；報告仍可被建構為 READY，但 consumer 不接受它 |
| 不增加 package root exports、authority receipt 或第二個 gate | 最小 API 是 raw tuple 加內容摘要方法；沿用既有 Full-QMS 與管理審閱結構 |
| collaboration 預設為空 tuple | 原有 caller 相容；省略時不宣稱六控制已被評估 |

摘要沿用現有 receipt 的 deterministic JSON / SHA-256 慣例：UTF-8、sorted keys、compact separators、`ensure_ascii=False`；payload 為 `{"schema":"human-ai-collaboration-controls-v1","controls":asdict(raw)}`，包含六紀錄的全部欄位及 control id。trace 格式是 `human-ai-collaboration:{control_id}:sha256:{digest}`。

**内容綁定不等於外部驗真。** Caller 仍可提交彼此一致但不真實的原始聲明、任意非空 verification ref，甚至自行生成相符的管理審閱 trace。這只能得到結構上的「可供人類審閱」，不能取得 Human owner approval 或 action authority。SHA 格式與計畫綁定不會連線確認 live GitHub；live-state recovery 仍是獨立治理責任。修改程式本身、任意 monkeypatch、同程序並行惡意記憶體寫入不在此資料輸入 API 的安全模型內。

```text
CALLER_SUPPLIED_READY != TRUSTED_READY
REASON_STRING != PROOF
STRUCTURED_RECORD != VERIFIED_REALITY
LIVE_HUMAN_AUTHORIZATION_LABEL != LIVE_AUTHORIZATION_PROOF
READY_FOR_HUMAN_REVIEW != MERGE_AUTHORITY
COLLABORATION_QMS_READY != HUMAN_OWNER_APPROVAL
```

`MAIN_TRANSITION_AUTHORITY_GATE` 與其外部 Human attestation / receipt 不變。這個 QMS 不發授權收據、不驗簽、不執行 merge、publish、deploy 或 branch delete。

## 六控制的繁體中文審閱介面

所有 `record_id` 是紀錄識別碼；`*_ref` 是呼叫端提交的追溯引用，不是已查證的外部證據。Bool 必須是精確 bool，enum 必須是精確 enum 型別，SHA 必須為小寫十六進位（Git 40 位、handoff SHA-256 64 位）。可選引用允許空字串，但拒絕只有空白。格式錯誤拋 `QualityError`；格式合法但未通過語意條件則回傳 HOLD。

| 型別／控制 | 欄位中文語意 | HOLD 條件 |
| --- | --- | --- |
| `HumanReviewCapacityRecord` 人類審閱容量 | `output_delivered` 已交付；`review_state` 審閱狀態；`high_impact_transition_requested` 請求高影響轉換；`capacity_exceeded` 超出容量；`human_gate_ref` 人類閘門引用 | 容量超限；高影響轉換未記錄足夠審閱狀態或人類閘門 |
| `RemediationRecord` 修復／禁止盲重試 | `defect_detected` 已知缺陷；`prior/retry_executor_ref` 前次／本次執行者；`prior/retry_handoff_sha256` 前後交接內容摘要；`independent_review_ref` 獨立審查；`exact_error_ref` 精確錯誤；`violated_requirement_ref` 違反需求；`negative_test_refs` 負測試；`retry_requested` 請求重試；`inherit_prior_pass` 繼承舊通過 | 繼承舊 PASS；已知缺陷仍由同執行者重試相同 handoff；改變重試方式卻缺修復 scaffold |
| `AuthorityEvidenceRecord` 授權聲明 | `current/presented_state_sha` 宣告的目前／呈現狀態；`source` 來源標籤；`transition_requested` 轉換請求；`authority_asserted` 聲稱授權；`verification_ref` 查證引用 | SHA 不等；轉換請求缺授權聲明／查證引用；聲稱授權卻採非 live-human 標籤。live 標籤通過只代表聲明一致 |
| `BilingualReviewRecord` 雙語可審閱性 | `material_change` 實質變更；`traditional_chinese_review_ref` 繁中審閱面；`english_governance_ref` 英文治理面；`both_surfaces_normative` 兩面皆規範性；`semantic_parity_verified` 聲明語意一致 | 實質變更缺繁中審閱面；雙規範面缺英文引用或語意一致聲明 |
| `ResearchDispositionRecord` 研究處置／範圍成長 | `disposition` 處置；`scope_growth_requested` 擴張範圍；`readmission_ref` 重入收據；`human_review_ref` 人類審查；`scientific_claim_promoted` 提升科學主張；`merge_authority_asserted` 聲稱合併權 | 範圍擴張缺重入／人類審查；提升科學或 merge 主張 |
| `BranchRetirementRecord` 分支來源／退役 | `history_value_known` 已知歷史價值；`all_commits_reachable` 全部提交可達；`unique_history_present` 存在獨特歷史；`preservation_ref` 保存；`verification_ref` 查證；`reconstruction_ref` 重建；`deletion_requested` 請求刪除 | 歷史未知；獨特／不可達歷史缺保存與重建；已知歷史缺驗證；任何刪除請求須另一獨立授權 |

`HumanReviewState`：UNKNOWN 未知、DELIVERED 已交付、REVIEWED 已審閱、APPROVED 已核可、INDEPENDENTLY_USABLE 可獨立使用。這些都是紀錄狀態，不推論人的理解。

`AuthoritySource`：LIVE_HUMAN_AUTHORIZATION 現時人類授權聲明、PROMPT 提示、RECOMMENDATION 建議、SELF_REPORT 自述、UI_STATE 介面狀態、HANDOFF_TEXT 交接文字、HISTORICAL_VERIFICATION 歷史驗證。任何值都不能單獨證明授權。

`ResearchDisposition`：SUPPORTED_CANDIDATE 候選支持、NARROWED 縮限、FALSIFIED 被反證、REJECTED 拒絕、INCONCLUSIVE 未定、SUPERSEDED 已取代、ABSORBED_INTO_EXISTING_CONSTRUCT 吸收入既有構念、NO_IMPLEMENTATION_REQUIRED 無須實作。負面／結案結果可留存，不強迫擴張範圍。

`CollaborationControlDisposition`：READY_FOR_HUMAN_REVIEW 僅可供人類審閱，HOLD 暫停。

Full-QMS 新增理由：`HUMAN_AI_COLLABORATION_CONTROL_HOLD` 為六控制之一 HOLD；`COLLABORATION_STATE_NOT_BOUND_TO_QUALITY_PLAN` 為狀態未綁計畫；沿用 `MANAGEMENT_REVIEW_EXTENDED_CONTROL_INPUTS_INCOMPLETE` 表示審閱未涵蓋 id／摘要。僅 Full-QMS 整體 READY 且有實際 collaboration inputs 時，才記 `HUMAN_AI_COLLABORATION_CONTROLS_READY_FOR_HUMAN_REVIEW`。可獨立呼叫 evaluator 查看每項 HOLD 的具體原因；其報告不能回填 consumer。

## 移植邊界

| 路徑（相對 QMS package） | 處置 |
| --- | --- |
| `src/aion_coupled_quality/human_ai_collaboration.py` | 取 source lane 六控制語意，加入遞迴驗證、摘要與固定報告上限；非原樣複製 |
| `src/aion_coupled_quality/extended_quality.py` | 在 current main 的現行 receipt/plan 邏輯上加入 raw-input seam；不採用 lane 的 assessment consumer |
| `tests/test_human_ai_collaboration_controls.py` | 沿用 source lane 17 個單元測試與合成 fixture |
| `tests/test_collaboration_trust_boundary.py` | 新增 25 個負例／正路徑／相容性測試 |
| `src/aion_coupled_quality/__init__.py` | NO_CHANGE，不擴大 root exports |
| `tests/test_extended_quality.py` | NO_CHANGE，重用 current-main fixtures；不移植直接 READY 的 lane 測試 |

未移植 `ccts_validity_study_design.py`、`longitudinal_falsification.py`、其 tests／exports、lane empirical 文件與 runner；未執行人類參與者、學習 outcome、retention、transfer 實驗。未建立新 construct／sub-construct。未整批移植 17 檔。

## Test-first 工程證據與重建

runtime 修改前，在 exact source lane 上寫回歸測試：先執行 forged／replace／metadata 8 個測試，8 failed；全 25 個測試則 23 failed / 2 passed。直接偽造 READY 確實由真實 Full-QMS 回傳 READY，非 mock。部分新 raw API 測試因來源仍要求 assessment 而失敗，應與直接漏洞重現區分。

| HEAD / 工作內容 | SUITE | COUNT |
| --- | --- | --- |
| PR266 起點 `41098bc514c6f9113748ac8ef4af34e214a288b2` | QMS package baseline | 200 passed |
| source `fa85a7f30ec77007280aa4957bd71a74c3a8683f` | source QMS baseline | 218 passed |
| 同 source SHA + 新回歸測試；runtime 不變 | trust boundary RED | 23 failed / 2 passed |
| PR266 起點 + 本文件所屬實作 tree | trust boundary GREEN | 25 passed |
| 同實作 tree | source six-control unit suite | 17 passed |
| 同實作 tree | 完整 QMS package | 242 passed |
| 同實作 tree | repository core `tests` | 278 passed |

本文件不內嵌自身未來 commit SHA；最終 exact remote head、重新驗證與 CI 狀態記於 PR #266 與執行報告。不可把上列 baseline 或工作樹結果當成其他 head 的驗證。

| 必要測試 | 結果／觀察 |
| --- | --- |
| Forged READY／empty/fabricated reasons | consumer 拒收，無 trusted READY |
| replace HOLD→READY、改 control id | report 不能充當 raw input |
| replace metadata | 科學 PASS、merge／branch-delete GRANTED、MAIN canonical effect、deployment True 皆拒絕 |
| fake LIVE label | 無 verification 引用則 HOLD；捏造非空引用仍無任何 action authority |
| provenance mismatch | 改 id、同 id 改內容仍用舊 review、state 未綁 plan 皆 HOLD |
| 六類 HOLD propagation | 每類均透過真實 Full-QMS 驗證 HOLD |
| positive path | 完整 raw controls + content trace + state plan 綁定，可達 bounded READY |
| malformed mutation／whitespace／mutable collection | 重新驗證或精確型別檢查拒絕 |
| optional omitted | 舊 caller 正常，但不宣稱 collaboration 已評估 |

重建指令（Python 3.12；QA 版本依 `.github/ci/quality-toolchain.txt`）：

```bash
# repository root
python -m pytest -q tests
ruff check --config ruff.toml .
python scripts/run_repository_mypy.py --root . --policy .github/ci/mypy-policy.json
# QMS package directory
python -m pytest -q tests/test_collaboration_trust_boundary.py
python -m pytest -q
```

QMS 依目前 repository policy 是 `EXEMPT_WITH_EXPLICIT_REASON`。另加跑 QMS 全 source `mypy --strict` 發現兩個既有問題：`claim_quality.py:436` 缺 return annotation，`longitudinal_claim_bridge.py:474` set/tuple assignment；未修改版本重跑同樣兩錯，本輪未擴張修復。不可將 policy PASS 說成所有 QMS 檔案 strict PASS。

## 獨立 adversarial reverse review

獨立 reviewer 審查本次 code diff、raw controls、真實 Full-QMS integration 與 user requirements，重跑 42 個 tests，並探查「合法巢狀 mutation 搭配舊 review」、「raw subclass」、「替換 raw 後 stale presented state」。未發現 Critical／Important 問題；唯一 Minor 是沿用測試的寬泛 `pytest.raises(Exception)`，已收窄為 `QualityError`。reviewer 未修改任何檔案。

反向結論：可建構 READY 報告但 consumer 拒收；replace 不提供通行；enum／字串無法提升權限；不同內容的舊 trace 與未綁計畫的 SHA 不能通過。宣告與外部現實是否相符仍由人類及既有外部治理查證，不假裝由摘要證明。既有 Full-QMS 報告的其他下游信任介面、任意 interpreter 改碼、並行惡意記憶體 mutation 屬此次資料輸入 API 範圍外。沒有第二套 authority system、未凍結 empirical code 或科學主張擴張。工程 verdict 僅 `READY_FOR_HUMAN_REVIEW`。

## 不變的結論與下一閘門

```text
NEW_CONSTRUCT_CREATED = NO
SCIENTIFIC_CLAIMS_CHANGED = NO
EMPIRICAL_INTERFACE_PORTED = NO
CCTS_VALIDITY = NOT_ESTABLISHED
CCTS_DISTINCT_CONSTRUCT_STATUS = NOT_ESTABLISHED
HUMAN_AI_COLLABORATION_SYNERGY = NOT_ESTABLISHED
HUMAN_LEARNING / RETENTION / TRANSFER / CAUSALITY = NOT_ESTABLISHED
EMPIRICAL_INTERFACE_PORT = HOLD
SCIENTIFIC_DISPOSITION = HOLD
MERGE_AUTHORITY = NONE
BRANCH_DELETE_AUTHORITY = NONE
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

下一個唯一閘門：Human + Teacher 對 exact-head 工程修正、測試證據與剩餘限制進行複審。最高工程處置為 `READY_FOR_HUMAN_REVIEW`，不是 `MERGE_READY`；既有 topology residual、authority gate 與科學問題各自保持原責任邊界。
