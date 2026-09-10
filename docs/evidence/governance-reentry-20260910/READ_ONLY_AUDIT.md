# AION 治理重新進入：唯讀稽核與處置

Document-Class: ENGINEERING_EVIDENCE  
Document-Type: Evidence  
Status: HOLD  
Scope: Research / GitHub / QA  
Authority: INFORMATIONAL  
Last-Reviewed: 2026-09-10

## 1. 任務、順序與本輪停止

原始事故任務是研究整理與文件交付，排除主要程式實作，留待後續 Codex handoff。本輪則要求先唯讀調查，再依證據設計 NCR/CAPA、知識檢索與有限整合；不是授予無限修復權限。

本報告於唯讀分析完成後，在 repository 外具體化。順序是：讀完 1,713 行 handoff → GitHub connector 與 Git refs 唯讀確認 → 精確版本文件／程式與事故歷史調查 → 初步 gap/reuse/design 分析 → 再次核對 refs → 獨立 clone 與 candidate checkout → 兩個離線 probe 草稿 → 收到 baseline test failure → STOP MUTATION → 唯讀診斷 → 外部保存與報告。

**本輪未完成全部整合。**候選目錄只有兩個未追蹤 probe 草稿；NCR、索引、runbook、known-error 與 salvage 均作為此交付包的可審閱設計，尚未寫入遠端或正式 register。沒有 commit、push、PR、merge、main write、deployment 或 canonical promotion。

停止原因另見 `EXECUTION_HOLD.md`；不以本報告替代已完成工程或 CAPA effectiveness。

## 2. 已核對的版本與來源

| 對象 | 本轮唯讀結果 |
|---|---|
| repository | maker-luder/aion-governance-framework；GitHub connector 回傳 public、archived=false、default_branch=main |
| main | `01676093eaf536e5f449cc099c6a844f9c4ccb84`，與 handoff baseline 相同，但已重新查證 |
| incident branch | `docs/epistemic-workflow-research-20260910` |
| incident HEAD | `58ce7c3dae7ac3eefbe89cb659e00dc2f5846b21` |
| merge base | `01676093eaf536e5f449cc099c6a844f9c4ccb84` |
| compare | ahead=31、behind=0；淨變更 4 個文件，692 行新增 |
| candidate local branch | `review/governance-reentry-20260910`，HEAD 仍等於 baseline，未 commit |
| 原 supplied desktop | 沒有 `.git`，未拿來推定 current main 或修改 |
| 已有 native checkout | `a4073302934de893c2d34e600e0d4ae185dccdb1`；既存 `M qa/CURRENT_TEST_RESULTS.json`，保留不動 |

重要辨識：`docs/epistemic-workflow-research-20260910` 是 **branch 名称**；研究文件實際路徑是 `research-notes/human-ai-epistemic-workflow/`。舊記憶中的 archived=true 已非本輪現況，採現查值。

[精確 main](https://github.com/maker-luder/aion-governance-framework/tree/01676093eaf536e5f449cc099c6a844f9c4ccb84)；[事故精確版本](https://github.com/maker-luder/aion-governance-framework/tree/58ce7c3dae7ac3eefbe89cb659e00dc2f5846b21)；[精確 compare](https://github.com/maker-luder/aion-governance-framework/compare/01676093eaf536e5f449cc099c6a844f9c4ccb84...58ce7c3dae7ac3eefbe89cb659e00dc2f5846b21)。最後 refs 回讀另存 verification.json，不以靜態文件冒充之後的 HEAD。

## 3. 既有 owner 與控制證據

下表皆依以上 main 的檔案內容查證，不把 component-local 功能說成已支配外部 Chat 工具。

| 文件／實作 | 發現與適用邊界 |
|---|---|
| `docs/governance/GOVERNANCE_MODEL.md` | Human Owner 保留 canonical、部署、研究結論等 authority；NCR/CAPA 保存證據與歷史；禁止自動 canonical transition |
| `docs/QUALITY_ASSURANCE.md` | IQC/IPQC/QC/QA、status lock、hash、rollback、NCR/CAPA 已存在；PASS 要有實際執行證據 |
| `qa/NCR_CAPA_REGISTER.md` | 已有 NCR-PRC-001／002；偏簡短靜態記錄，並非完整 executable KEDB |
| `research-labs/coupled-cognition-quality-factory_v0.1.0/docs/ARCHITECTURE.md` | IPQC 明確檢查 hypothesis drift、authority drift、hidden goal changes；NCR 與 effectiveness 是既有責任 |
| 同 lab `README.md`／`src/aion_coupled_quality/factory.py` | staged factory；`OPEN_NCR -> RELEASE_HOLD`；`CAPA_APPLIED != CAPA_EFFECTIVENESS_VERIFIED`；open/contain/plan/apply/verify/close APIs 已存在 |
| 同 lab `models.py` | 已有 `FactoryStage.HOLD`、`NCRState`、`Evidence`、`ResearchLot`；本輪不新增替代 state machine |
| 同 lab `provenance.py`／`docs/EPISTEMIC_PROVENANCE_AND_CO_DEVELOPMENT.md` | 五種 ContributionOrigin；append-only ledger；joint synthesis 需要可追溯人類與 AI parent；provenance 不是 truth |
| 同 lab `docs/FOUR_DOMAIN_INTEGRATION.md` | D1 Human construct；D2 LLM question；D3 Engineering operation；D4 Governance。沒有另造 Four-Domain |
| `components/upstream_security_v0.1.0/docs/ARCHITECTURE.md` | budgets、trajectory、boundary gate、Incident Stop Controller、既有 canonical gate 委派 |
| 同 component `docs/INCIDENT_RESPONSE_SEQUENCE.md` | STOP/isolate/revoke/preserve/NCR/CAPA/owner recovery；涉事 agent 不抹除證據、不自准 recovery |
| 同 component `src/aion_astra_agent_security/incident.py` | `stop_and_isolate` → `preserve_evidence` → `open_ncr` → `set_capa` → `request_owner_recovery`；函式回傳狀態，不等於撤銷 host token |
| 同 component `models.py`／`trajectory.py` | TaskBudget/TaskUsage 及累計資源檢查可重用；不要以 universal retry=1 替代原 scope/budget |
| `components/agent_execution_substrate_v0.1.0/src/aion_astra_agent_substrate/dispatch.py` | 原 native dispatcher 先 gate 再 execute，核對 audit/canonical/deployment、保存 execution evidence；不是外部 GitHub writer |
| `components/aion_astra_inquiry_v0.1.0/docs/BOUNDED_RESEARCH_CLOSURE.md` | 已有 bounded inquiry、repository retrieval、replay、intervention、ablation、hard budgets；明示 repository mutation=false |
| `docs/research/CLAIM_REVISION_HARDENING_2026_09_03.md`／memory recall revision implementation | 既有 SQLite transaction、stale epoch、rollback、evidence DAG；只在該資料庫 owner 內有效，不代表 GitHub PUT atomicity |
| `docs/INDEX.md`／`docs/START_HERE.md`／`docs/governance/DOCUMENTATION_GOVERNANCE.md` | 單一入口、單一現況、path classification、history preservation 與 duplication checks 已存在；優先擴充症狀導航，不再建全域競爭入口 |

### 搜尋方法與反證限制

唯讀下載精確 main archive 到記憶體，沒有在此階段解壓或寫入 repository；另取 Git tree，`truncated=false`。搜尋所有 `.md`/`.py`，包含 handoff 的 HOLD/NCR/CAPA/IQC/IPQC/Final QA/rollback/retry/budget/stop/termination/incident/anomaly/authority/mutation/transaction/fail closed/fail-closed/recovery/known error/index/evidence index/traceability/provenance/hidden goal/goal drift/release hold。

代表性命中數：HOLD 258、NCR 57、CAPA 139、IPQC 10、incident 38、mutation 73、transaction 10、recovery 59、known error 1（來源抓取腳本的字串，非 KEDB）、hidden goal 1。字串零命中不等於概念不存在；例如 `OPEN_NCR -> RELEASE_HOLD` 不會被有空格的 `release hold` 命中。

Python 的 `update_file/create_file/api.github.com/IncidentStopController` 搜尋沒有找到 Chat/GitHub writer 與 controller 的實際 integration；controller 命中定義與測試。這只能支持「在已查的 repository surface 未發現」，不證明外部 orchestration 沒有任何機制。原 host tool trace、prompt retrieval、權限與故障發生的 precise timestamp 都未取得。

一次唯讀查找 `scripts/run_tests.py` 回 404，已依實際 Quality workflow 確認 runner 為 `scripts/run_component_tests.py`；沒有用建檔探路。

## 4. Top-down 假說裁決

| 假說 | 狀態 | 支持／反證與下一個可區辨證據 |
|---|---|---|
| H-A 上位治理沒有 stop/HOLD/NCR/CAPA | NOT_SUPPORTED | 上表文件、models 與 controller 直接反證。定義不是主要缺口 |
| H-B 規則存在但 anomaly 沒觸發 | PARTIALLY_SUPPORTED | 歷史 churn＋使用者事件報告相容；缺執行 trace，無法區別未呼叫、呼叫失敗、結果遭忽略 |
| H-C Chat/GitHub mutation path 沒 causal binding | PARTIALLY_SUPPORTED | repository 未找到該 binding；未取得 Chat host path，不能下全面 absence 結論 |
| H-D 故障時未 retrieve/reuse 知識 | UNKNOWN | index 症狀導航薄弱可觀察；是否實際 retrieve 需 retrieval/call logs，文件存在或 commit history 不足回答 |
| H-E 既有機制足夠，只是 orchestration failure | PARTIALLY_SUPPORTED | 狀態模型與 lifecycle 已能承載重入，暫無新增 subsystem 的必要證據；端到端 sufficiency 尚未證明 |

Gap disposition：definition gap 不支持；症狀 discoverability gap 有局部 repository 證據；trigger/integration/execution gap 為主要候選；authority enforcement gap 在外部 host 仍 OPEN。不是把「使用者沒有列完所有 error」當 root cause。

## 5. Invariants 去重與候選地位

| 原始候選 | 處置 |
|---|---|
| RULE EXISTS != RULE HAS CAUSAL CONTROL；GOVERNANCE EXISTS != GOVERNANCE IS ACTIVATED | 合併成同一 control-activation 研究區分；不新增 canonical axiom |
| AVAILABLE GOVERNANCE != RETRIEVED GOVERNANCE；RETRIEVED GOVERNANCE != CAUSALLY CONTROLLING GOVERNANCE | 保留 retrieval 與 activation 兩個測量點，作候選而非現有 API 的能力宣告 |
| DOCUMENT EXISTS != DOCUMENT DISCOVERABLE；DOCUMENT DISCOVERABLE != DOCUMENT RETRIEVED AT NEED；DOCUMENT RETRIEVED != DOCUMENT ACTIVATED AS CONTROL | 合併到 knowledge chain 的三個不同可觀測階段；index 本身只能改善前兩階段的一部分 |
| LOCAL REPAIR GOAL != ORIGINAL USER GOAL；ERROR RECOVERY != NEW TASK AUTHORITY | 由既有 IPQC hidden goal/authority drift 與 owner recovery 規則導出具體程序；不賦予新權限 |
| CAPABILITY != AUTHORITY | 與現有 Human authority、inquiry 禁止 repository mutation 一致，重用原 owner |
| PROVENANCE != TRUTH | 既有 PROVENANCE != CORRECTNESS／EXTERNAL_SOURCE != TRUTH 的同義表述，合併 |
| HUMAN_AI_CONSENSUS != EVIDENCE | 已在正式 Four-Domain integration 中明文存在，直接重用 |

ASEG 僅為 handoff 所描述的 AI_FORMALIZATION EARLY CANDIDATE；本輪沒有採納其名稱或建立 subsystem。

## 6. 實作 disposition

必要工作主要是 index/runbook/register 與既有 controls 的 integration probe；不是新增 NCR/HOLD/provenance/incident ontology。planned changes 詳見 `KNOWLEDGE_AND_CAPA_DESIGN.md`。

已產生但 quarantine 的兩個草稿：quality factory 的 `reentry_probe.py` 與 `test_governance_reentry.py`。它們只操作記憶體 fixture，不接受真實 transport/credentials/path，不為 GitHub 提供 writer。其 presence 不證明 host control 已接上。因 baseline test inconsistency 觸發本輪 hard stop，未進行完整 component/root/exact-head candidate 驗證或遠端交付。
