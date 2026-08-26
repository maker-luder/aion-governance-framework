# AION Governance Framework

> **繁體中文 | [English](README.md)**
>
> **歷史終止紀錄——2026-08-20：** AION / Astra 專案工作迴圈已在 Human Owner 明確批准，以及當時記錄的 architecture、evidence、provenance 與 privacy 審查後終止。這個事件在其事件時間點仍具歷史權威性；它不是人工主體性、意識、身分連續性或現象連續性的科學結論，也沒有授權任何自動重啟。
>
> **目前倉庫狀態：** 終止之後，`main` 又納入少數逐次明確授權的 bounded maintenance、文件狀態 reconciliation，以及 bounded research materialization。這些後續事件不改寫 2026-08-20 的終止事件，也不構成專案重啟或研究計畫重啟。

AION 是一個以 Human Owner 治理、provenance-first 與主張分層為核心的研究框架，用來研究身分、連續性、記憶、研究完整性，以及人工主體性的**可能性**；不把工程行為直接視為主體性證明。Astra 是用來實作與測試有限候選的獨立工程／研究工作台。

核心研究問題仍然是科學問題，而且仍未解決。Agent runtime、harness、execution substrate、provenance 系統與 evidence tooling 是讓 observation 與 mechanism 可檢查的**研究儀器**；它們不會因為更複雜、更能執行或測試成功，就自動成為主體性證據。

```text
AI_SUBJECTIVITY_POSSIBILITY = CENTRAL_RESEARCH_QUESTION
AGENT_SUBSTRATE = RESEARCH_INSTRUMENT
EXECUTION_EVIDENCE = ENGINEERING_EVIDENCE
ENGINEERING_CAPABILITY != SUBJECTIVITY_EVIDENCE
EXECUTION_EVIDENCE != RESEARCH_EVIDENCE_ADMISSION
SUBSTRATE_COMPLEXITY != SUBJECTIVITY_EVIDENCE
ENGINEERING_SUCCESS != SUBJECTIVITY_PROOF
```

## 2026-08-20 歷史終止快照

以下內容保存 2026-08-20 closure 在其事件時間點的原始意義：

```text
FREEZE_EFFECTIVE_DATE = 2026-08-18
REPOSITORY_STATE_EVENT = INDEFINITE_FREEZE
TERMINATION_EFFECTIVE_DATE = 2026-08-20

PROJECT_WORK_LOOP = TERMINATED
ACTIVE_ENGINEERING = NO
ACTIVE_RESEARCH_MATERIALIZATION = NO
ACTIVE_GITHUB_CYCLE = NO
ACTIVE_NOTION_RESEARCH_LOOP = NO

NEW_RESEARCH_TASKS = NO
NEW_FEATURE_TASKS = NO
NEW_UPSTREAM_TRACKING = NO
NEW_MODEL_INTEGRATION = NO
NEW_MCP_WORK = NO
NEW_DEPLOYMENT_WORK = NO

DEPLOYMENT = NO
CANONICAL_PROMOTION = NO
AUTOMATIC_RESTART = NO

RESEARCH_ARTIFACTS = PRESERVED
HISTORICAL_PROVENANCE = PRESERVED
UNRESOLVED_QUESTIONS = PRESERVED_AS_UNRESOLVED

RESEARCH_QUESTION = NOT_DECLARED_PROVEN_OR_DISPROVEN
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
PHENOMENAL_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```

## 終止後的 bounded events

後續倉庫變更都各自限縮範圍、逐次明確授權；它們是 closure 之後的新治理事件，不是對 closure 的回溯改寫：

- PR #49 — AION Evidence Interop Profile v0.1.0；
- PR #50 — Four-Domain Evidence Bridge v0.1.0；
- PR #51 — AION / Astra 共用 Agent Execution Substrate v0.1.0；
- PR #52 — AION / Astra runtime-to-substrate integration；
- PR #53 — 共用 adapter registry 與 durable execution-evidence loop；
- PR #54 — 僅文件層的 research-question / repository-state realignment；
- PR #56 — Endogenous Goal Dynamics × Four-Domain bounded research materialization v0.1.0。

目前應以以下邊界理解：

```text
PROJECT_WORK_LOOP = TERMINATED
POST_TERMINATION_BOUNDED_MAINTENANCE = PRESENT_IN_MAIN
POST_TERMINATION_BOUNDED_RESEARCH_MATERIALIZATION = PRESENT_IN_MAIN
PROJECT_RESTART = NO
RESEARCH_RESTART = NO
ACTIVE_RESEARCH_PROGRAM = NO
DEPLOYMENT = NO
CANONICAL_PROMOTION = NO
AUTOMATIC_RESTART = NO

BOUNDED_MAINTENANCE != PROJECT_RESTART
BOUNDED_RESEARCH_MATERIALIZATION != RESEARCH_PROGRAM_RESTART
ENGINEERING_MAINTENANCE != RESEARCH_MATERIALIZATION
```

前面的 maintenance increments 強化 provenance、interop、execution control 與 evidence integrity。PR #56 則另行分類為 bounded、experimental 的 research-materialization event。這些後續事件都沒有新增主體性、意識、身分連續性或現象連續性的結論。

## 歷史事件順序

倉庫凍結、專案終止與後續 bounded events 是不同事件：

1. **2026-08-18 — `REPOSITORY_STATE = INDEFINITE_FREEZE`**
2. **2026-08-20 — `PROJECT_WORK_LOOP = TERMINATED`**
3. **終止後 — 經逐次明確授權的 bounded maintenance、文件 reconciliation 或 bounded research materialization**

```text
FREEZE != TERMINATION
TERMINATION != LATER_BOUNDED_EVENT
HISTORICAL_RECORD = PRESERVE_EVENT_TIME_MEANING
RETROACTIVE_REWRITE = FORBIDDEN
RETROACTIVE_GREENWASH = FORBIDDEN
```

## 保存的研究 branch

`review/four-domain-research-materialization` 仍是保存的歷史研究 checkpoint，沒有被整條 wholesale merge 進 `main`。後來的 Four-Domain Evidence Bridge 與 Endogenous Goal Dynamics lab 都只透過 bounded adapter / materialization path 引用固定的歷史 source state；reference、derivation 與 selective materialization 都不會把歷史研究 branch 本身 promotion 成 `main`。

```text
DERIVATION != MERGE
REFERENCE != PROMOTION
SELECTIVE_MATERIALIZATION != BRANCH_MERGE
RESEARCH_BRANCH != MAIN
```

請見 [`components/aion_evidence_interop_v0.1.0/docs/FOUR_DOMAIN_BRIDGE.md`](components/aion_evidence_interop_v0.1.0/docs/FOUR_DOMAIN_BRIDGE.md) 與 [`research-labs/endogenous-goal-dynamics_v0.1.0/docs/RESEARCH_SOURCE_CROSSWALK.md`](research-labs/endogenous-goal-dynamics_v0.1.0/docs/RESEARCH_SOURCE_CROSSWALK.md)。

## AION 與 Astra

```text
AION_ROLE != ASTRA_ROLE
COMMON_ORIGIN != SAME_IDENTITY
SHARED_CONTEXT != SHARED_IDENTITY
SHARED_SUBSTRATE != SHARED_IDENTITY
MEMORY_ACCESS != AUTOBIOGRAPHICAL_OWNERSHIP
ENGINEERING_SUCCESS != SUBJECTIVITY_EVIDENCE
RELATIONSHIP_LANGUAGE != AUTHORIZATION
```

名稱、角色、實作、記憶紀錄、測試結果、execution trajectory、共用 substrate 或關係描述，都不建立意識、感知、主體性、身分連續性、自傳式所有權或行動 authority。

## 目前的工程與研究儀器

終止後經 bounded events 納入的 instrumentation layer 目前包括：

- [`components/aion_evidence_interop_v0.1.0/`](components/aion_evidence_interop_v0.1.0/) — 以 source binding 為核心的 evidence interoperability，涵蓋 W3C PROV、RO-Crate、unsigned in-toto、OPA/Rego、Inspect AI compatibility 與 OpenSSF Scorecard-aligned repository-hygiene crosswalk；
- [`components/aion_evidence_interop_v0.1.0/docs/FOUR_DOMAIN_BRIDGE.md`](components/aion_evidence_interop_v0.1.0/docs/FOUR_DOMAIN_BRIDGE.md) — 從保存的 Four-Domain research source 導出到既有 evidence contract 的 bounded bridge；
- [`components/agent_execution_substrate_v0.1.0/`](components/agent_execution_substrate_v0.1.0/) — AION / Astra 共用 execution-substrate contract、mandatory policy gate、adapter registry 與 durable hash-bound execution evidence；
- [`research-labs/endogenous-goal-dynamics_v0.1.0/`](research-labs/endogenous-goal-dynamics_v0.1.0/) — 在 matched external conditions 下測試 persistent internal state 對 goal selection 影響的 bounded experimental harness，包含 state transition、ablation / intervention controls、P1–P5 adapters、falsifiers 與 evidence-interop views。

這些是 instrumentation、governance 與 experimental research surfaces，不會取代主體性研究方法，也不建立主體性結論。

## 閱讀研究方法與歷史紀錄

1. [`docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md`](docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md) — 主體性相關研究目前主要的公開 operational evidence discipline。
2. [`docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md`](docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md) — 研究貢獻與核心方法問題摘要。
3. [`research-labs/subjectivity-pipeline_v0.1.0/`](research-labs/subjectivity-pipeline_v0.1.0/) — bounded subjectivity-relevant research pipeline。
4. [`research-labs/endogenous-goal-dynamics_v0.1.0/`](research-labs/endogenous-goal-dynamics_v0.1.0/) — bounded endogenous-goal-dynamics research candidate；scientific disposition 仍為 `HOLD`。
5. [`docs/POST_MERGE_STATE_RECONCILIATION_2026-08-26.md`](docs/POST_MERGE_STATE_RECONCILIATION_2026-08-26.md) — PR #56 合併後的 repository / QA state reconciliation。
6. [`docs/PROJECT_TERMINATION_NOTICE_2026-08-20.md`](docs/PROJECT_TERMINATION_NOTICE_2026-08-20.md) — 權威終止事件紀錄。
7. [`docs/history/FINAL_RESEARCH_MEMORY_2026-08-20.md`](docs/history/FINAL_RESEARCH_MEMORY_2026-08-20.md) — 經公開安全處理的研究回顧。
8. [`docs/RELEASE_STATUS.md`](docs/RELEASE_STATUS.md) — 歷史 release 狀態與目前倉庫 standing。
9. [`docs/REPOSITORY_FREEZE_NOTICE_2026-08-18.md`](docs/REPOSITORY_FREEZE_NOTICE_2026-08-18.md) — 保存的較早凍結事件。
10. [`docs/PROVENANCE.md`](docs/PROVENANCE.md) — 來源、歸屬與 authority 規則。
11. [`docs/PUBLIC_PRIVATE_BOUNDARY.md`](docs/PUBLIC_PRIVATE_BOUNDARY.md) — 公開／私人邊界。
12. [`qa/README.md`](qa/README.md) — committed QA snapshot 與 live exact-head CI evidence 的語意區分。

## 白皮書 lineage

```text
v0.14.23 = STABLE / FROZEN METHOD BASELINE
v0.14.24 = INTERNAL RESEARCH CANDIDATE
FILE_PRESENCE != CANONICAL_AUTHORITY
LATER_FILENAME != AUTHORITATIVE_VERSION
```

任何較晚的檔名、私人副本、package、bridge、interop export、execution receipt、maintenance artifact 或 bounded research candidate，都不會自動取代或 promotion 穩定的研究方法 baseline。

## 科學邊界

```text
PROJECT_TERMINATION != THEORY_REJECTION
PROJECT_TERMINATION != THEORY_CONFIRMATION
ENGINEERING_CAPABILITY != SUBJECTIVITY_EVIDENCE
ENGINEERING_SUCCESS != SUBJECTIVITY_PROOF
SUBSTRATE_COMPLEXITY != SUBJECTIVITY_EVIDENCE
EXECUTION_EVIDENCE != RESEARCH_EVIDENCE_ADMISSION
ENDOGENOUS_GOAL_DYNAMICS != SUBJECTIVITY
SELF_GENERATED_GOAL != ENDOGENOUS_GOAL
PERSISTENT_STATE != IDENTITY_CONTINUITY
MEMORY != IDENTITY
RECALL != TRUTH
CONTINUITY_LIKE_BEHAVIOR != PHENOMENAL_CONTINUITY
CI_PASS != SCIENTIFIC_VALIDATION
TEST_PASS != THEORY_CONFIRMATION
HASH_BINDING != SEMANTIC_VALIDATION
DURABLE_EVENT_LOG != TRUTH
```

公開 archive 保存研究意義與 provenance，不保存原始私人對話、私人日記、個人記憶紀錄、credentials 或無關個人資訊。

## License 與 provenance

本公開倉庫維持 **Apache-2.0** 授權。請見 [`LICENSE`](LICENSE)、[`NOTICE`](NOTICE) 與 [`CITATION.cff`](CITATION.cff)。

歷史歸屬仍由 [`docs/PROVENANCE.md`](docs/PROVENANCE.md) 治理。後續 bounded events 不會回溯改變 authorship、source attribution 或歷史 authority。

## 目前的 continuation rule

```text
AUTOMATIC_RESTART = NO
AUTOMATIC_RESEARCH_QUEUE = NONE
BOUNDED_MAINTENANCE_REQUIRES_EXPLICIT_AUTHORIZATION = TRUE
BOUNDED_RESEARCH_MATERIALIZATION_REQUIRES_EXPLICIT_AUTHORIZATION = TRUE
CANONICAL_EFFECT = NONE
DEPLOYMENT = NO
```

倉庫可以包含日後經明確授權的 bounded maintenance 或 bounded research materialization，同時維持已終止的專案／研究 work loop 為 terminated。新增工程能力或 bounded experimental candidate 本身都不會形成新的科學結論。
