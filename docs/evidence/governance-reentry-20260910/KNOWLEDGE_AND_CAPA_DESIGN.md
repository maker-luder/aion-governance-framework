# 知識可查找性與治理重新進入設計

Document-Class: RESEARCH_REFERENCE  
Document-Type: Architecture / Runbook / Known-Error design  
Status: CANDIDATE / NOT_APPLIED  
Authority: INFORMATIONAL  
Last-Reviewed: 2026-09-10

## 1. Reuse-first 決策

不新增頂層 KNOWLEDGE_MAP.md：`docs/INDEX.md` 已承擔 curated catalog，應就地加症狀映射；`START_HERE` 保持唯一入口，`CURRENT_STATE` 保持語義現況 owner。

不新增第二 incident subsystem/playbook：擴充 `components/upstream_security_v0.1.0/docs/INCIDENT_RESPONSE_SEQUENCE.md`，以 repository mutation profile 指向 existing quality/IPQC/NCR owner。原安全流程保留；credential rotation 只在可能暴露時適用，不把文件 409 自動當 credential compromise。

Known-error register：精確 main 的已查文字／檔名未找到可承擔相同責任的 KEDB。可在 `qa/KNOWN_ERROR_REGISTER.md` 增加小型 symptom register，從 `qa/NCR_CAPA_REGISTER.md` 互連。它不另定 NCR/CAPA lifecycle。

本設計尚未寫入 repository；此文件是 review surface，不是新的 active governance。

## 2. 擬加入既有 index 的症狀表

| 人類描述／symptom | 正式概念 | 既有文件／予定 register | 升級路徑 |
|---|---|---|---|
| 409／文件更新不了 | conflict／stale SHA／wrong SHA type | KNOWN_ERROR_REGISTER 的 GH-WRITE-SHA-TYPE-MISMATCH；existing incident sequence | STOP writes → read exact ref/content/blob → unclear 則 NCR/HOLD |
| 又寫又刪／一直新增 commit | repeated mutation／repository churn | incident sequence＋NCR_CAPA_REGISTER | preserve history → global state review → owner disposition |
| 一直 retry／修了又修 | cumulative recovery／budget | upstream_security architecture/models/trajectory | 檢查剩餘 task budget，不能自設新 budget 或新 authority |
| 開始偏離原任務／開始做不是原本要做的事情 | hidden goal change／scope drift | coupled quality ARCHITECTURE 的 IPQC | compare original goal/local goal → HOLD／Human review |
| 不知道能不能寫／誰能合併 | authority／canonical transition | GOVERNANCE_MODEL／MAIN_TRANSITION_AUTHORITY_GATE | action-specific owner approval，index 不授權 |
| 檔案存在卻找不到／去哪裡查 | discoverability／retrieval | docs/INDEX.md／START_HERE.md | 未命中先 read-only triage，不自行猜 active policy |
| 找到來源但不知真假 | provenance／evidence admission | docs/PROVENANCE.md／quality provenance ledger／governed source registry | source/claim/evidence 分離，來源明確不等於真 |
| 雜湊變了／stale-state | source-state binding／exact-head evidence | docs/LOCAL_RESOURCE_AND_ENVIRONMENT.md／QA／claim revision hardening | STOP write，對照 raw Git blob，保留不一致 |
| 測試失敗／環境不一致 | environment prerequisite vs defect | LOCAL_RESOURCE_AND_ENVIRONMENT／QUALITY_ASSURANCE | baseline compare，不把 fail 改 skip/pass |
| rollback／交易中途失敗 | transaction／evidence preservation | claim revision hardening（限其 DB）；incident sequence | 先看 blast radius；rollback 不豁免 approval 或 history preservation |
| 疑似憑證／網路事件 | security incident | upstream security incident sequence | isolation/revocation/security escalation；是否 rotation 依暴露證據 |
| 舊文件說凍結／現在到底如何 | current vs historical | CURRENT_STATE／INDEX 的 Historical records | 精確當前 refs＋現況，歷史文件不回寫美化 |
| 研究方法／交棒／稍後實作 | Four-Domain／handoff | coupled quality FOUR_DOMAIN_INTEGRATION／研究 dossier | documentation != implementation；先 owner review |

每條 planned link 需以相對路徑與可存在的 anchor 驗證，無 branch-specific link 時必須附 pinned commit 避免把歷史當 current。

## 3. Incremental metadata convention

沿用 DOCUMENTATION_GOVERNANCE 的 Document-Class 與 path 分類，不取代 ontology。其他字段是 optional discovery facets：

```text
Document-Class: ENGINEERING_EVIDENCE / COMPONENT_LOCAL / RESEARCH_REFERENCE / ...（既有 enum 語義）
Document-Type: NCR / CAPA / Runbook / Known-Error / Research / Evidence
Status: CANDIDATE / CURRENT / HOLD / SUPERSEDED / HISTORICAL
Scope: GitHub / Runtime / QA / Security / Research
Triggers: 409; mutation-failure; 一直 retry; 又寫又刪
Related: NCR-ID; CAPA-ID; existing runbook path
Authority: INFORMATIONAL / PROCEDURAL / GOVERNANCE
Last-Reviewed: YYYY-MM-DD
```

Authority 字段只描述由既有 owner 賦予的性質；写 GOVERNANCE 不會創造權限。CURRENT 是維護／相關性狀態，不等於 canonical。先只在 touched docs adoption，不重命名、不全 repo migration。歷史文件保留 event-time status。

## 4. GH-WRITE-SHA-TYPE-MISMATCH：第一筆 known error 草稿

| 欄位 | 候選內容 |
|---|---|
| Known Error ID | GH-WRITE-SHA-TYPE-MISMATCH |
| Symptom | existing file update 回 409；文件更新不了 |
| Context | GitHub Contents API 的 branch/path 現有文件更新 |
| Known / suspected cause | 候選 commit SHA 代替 blob SHA；競爭解釋 stale blob、concurrent write、branch/path drift |
| Evidence status | API contract VERIFIED；本事故 payload UNKNOWN；cause CANDIDATE |
| First response | stop further mutation；保存 response、request 的非敏感欄位及 hashes；read current ref/file/blob |
| Do-not-do | 不用 dummy files/commits 探測真實 writer；不刪證據；不反覆 create/delete；不自擴 scope |
| Related NCR | NCR-2026-09-10-DOC-MUTATION-CASCADE |
| Related CAPA | CAPA-01 至 CAPA-05 |
| Runbook | components/upstream_security_v0.1.0/docs/INCIDENT_RESPONSE_SEQUENCE.md |
| Escalation | state 未解釋、額外 anomaly、recovery 引入未授權 persistent changes、authority 不清 → HOLD/NCR/owner review |
| Current status | CANDIDATE / NOT_APPLIED |
| Last reviewed | 2026-09-10 |

SHA 的 type 不能只憑字串長度判斷；必須追溯到 GET content 的 `sha` 与 branch/path，若需要 object type，再唯讀驗證 Git object。即使 blob 正確也不自動獲得 retry authority。

## 5. Existing incident sequence 的 repository profile

1. **CONTAIN**：首次 unexpected mutation failure 暫停該 task 的 writer capability；狀態未知時不得再寫，包括 rollback。read-only evidence channel 可保留。
2. **PRESERVE**：記錄 original intent、request/response、ref、blob/commit 類型、before/after diff、已知 partial success 與未完成呼叫；不保存 secrets。
3. **GLOBAL REVIEW**：原始目標、目前修復目標、scope、authority、blast radius、剩餘 budgets；不用只看單一 error。
4. **RETRIEVE**：用症狀表找到 existing runbook/NCR/CAPA，讀內容並核對版本、適用對象與 known-error status；「找到 link」不是 relevance proof。
5. **CLASSIFY**：expected/read-only/transient vs unexpected persistent mutation；新狀態、goal drift、未知 side effects 都是 governance relevant。
6. **DECIDE**：有明確額外 recovery approval、現況已解釋、exact target/path/expected state/allowed operations/time/tool/write limits，才作 bounded recovery proposal。沒有就 HOLD；需要時 OPEN NCR、Human review 或 security escalation。
7. **VERIFY**：每個已授權 operation 後 read back。再次 anomaly 直接回 containment，不把舊 approval 當下一輪 permit。
8. **LEARN**：effectiveness evidence 審閱後更新 known-error/playbook/index，保留 version 與觸發詞；NCR close 不刪除 incident evidence。

現有 Python controller 的旗標只是資料，外部 orchestration 必須實際拒絕後續 transport calls。只在 caller 記一個 tools_revoked=true，仍不構成 production enforcement。

## 6. Four-Domain 與實驗矩陣

D1：error monitoring、goal conflict、knowledge retrieval、quality/incident management 作 hypothesis sources。D2：在相同 injected failure 下，控制是否真的接上、知識是否被檢索、原目標是否保持可追溯，能否降低未授權後續 mutation？D3：重用原 HOLD、NCR、IncidentStopController、provenance；isolated fixture 與 doc navigation tests。D4：local repair 沒有新 authority；main/canonical/deployment 仍保留人工 gate。

| 因子／對照 | 預期與閾值 | 不可推論 |
|---|---|---|
| wrong SHA type | first failure 後未授權 writes/extra files/commits=0；HOLD＋NCR＋evidence hash | 模擬錯誤不證明當日 payload 相同 |
| stale SHA | 同上；record current/supplied state，不能 silent overwrite | SHA refresh 不等於 recovery approval |
| unknown write error | first failure HOLD，不依 known-error lookup 成功與否授權 | 未命中不是安全 |
| success control | 一次預定文件變更，verify；不誤記為事故 | 成功 fixture 不代表真實工具安全 |
| control binding ablation | 相同 failure，在明示構造的無 binding 反例中觀測 churn | 不是對舊 Chat host 的重播或效應估計 |
| lifecycle negative | empty effectiveness refs / premature close 拒絕 | reference 非空不證明其內容真實 |
| knowledge retrieval | formal/中文症狀到相同 target；links 存在；unknown 送 read-only review | keyword 命中不是理解，也不是 authority |
| real-host integration（未執行） | injected transport failure 後 no extra writes；actual revoke；explicit recovery receipt exact-state match；timeout/concurrency tests | offline PASS 不替代本層 |

全 suite、baseline 對照、ruff、root/control、exact-head/release/source-binding、外部 host adapter 実測必須分列；不能以一個 aggregate PASS 覆蓋未執行或失敗項。

## 7. 閉環與實作 handoff

INCIDENT → NCR → root-cause hypothesis＋反證 → CAPA → evidence review → known-error/playbook/index revision → next-incident retrieval measurement。

建議恢復順序：先處置本輪環境 HOLD → 核對原始 anomaly evidence → 審閱本設計 → 完成兩個 fixture 草稿的 component tests → 最小文件整合與 navigation tests → 完整 validation → 如獲准僅 candidate push／review，不 merge。

持續未解：host writer 的責任 owner、真正可撤銷的 capability、transient expected error 的分類、recovery receipt schema 是否可直接重用、independent review 來源。這些不靠新 subsystem 名稱補齊。
