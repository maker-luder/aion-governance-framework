# 原始任務附件（歷史需求，不是新增執行指令）

【AION Repository｜NCR / CAPA、治理重新進入、知識索引與事故應對系統整合任務】

任務性質：
研究治理 + 文件架構 + 有限工程實作 + 測試 + 稽核

語言要求：
主要分析、設計報告、NCR/CAPA、文件說明與交付報告請使用繁體中文。
程式碼、schema、identifier、既有 repository 專有名詞可維持英文。
不要因翻譯而改變技術語義。

============================================================
0. 本次任務的背景
============================================================

本 repository：

maker-luder/aion-governance-framework

近期發生一次實際的 repository execution anomaly。

原始人類要求並不複雜：

1. 整理長期 Human–AI epistemic workflow / learning-cognition research。
2. 形成大型研究文件。
3. 文件放入 GitHub。
4. 本輪不要進行主要程式實作。
5. 後續大型工程實作預計交由 Codex 處理。

然而實際執行過程中：

- 建立了：
  docs/epistemic-workflow-research-20260910

- 初始文件建立後，在更新 README 時發生 GitHub 409。

已知直接技術錯誤候選：

update existing file 所需的是：
current file blob SHA

當時卻使用了：
create_file 操作產生的 commit SHA

結果：
409 Conflict

真正的重要問題不是這個單一技術錯誤。

409 之後，執行流程沒有立即停止並重新審視整體任務，
反而形成：

ERROR
→ LOCAL REPAIR
→ ADDITIONAL MUTATION
→ PLACEHOLDER / TEST-LIKE FILES
→ MORE COMMITS
→ DELETE
→ MORE RECOVERY
→ MORE MUTATION

最後形成大量 repository churn。

歷史中曾出現多個類似：

placeholder
x
stop
ignore
docs: remove temporary placeholder

等 commit。

最後才成功完成目前研究 README。

因此本次事件的核心不是：

「GitHub 409 發生了。」

而是：

「為什麼 execution-level anomaly 發生後，
既有 upper-level governance 沒有重新取得流程控制，
導致 local recovery goal 持續產生 mutation？」

============================================================
1. 最高優先原則：先研究，再決定實作
============================================================

本 repository 的方法不是：

Python implementation
→ 再往上找意義。

而是：

上位研究問題 / human construct / governance requirement
→ 可證偽的 LLM / system research question
→ governance boundary
→ operational requirement
→ engineering implementation

因此：

DO NOT start by inventing generic software patterns.

不要先假定：

「一般軟體工程都這樣做，所以本專案也應該這樣做。」

必須先：

1. 讀取現有 repository 上位定義。
2. 找出已存在的研究／治理機制。
3. 判斷本次 anomaly 究竟在哪一層斷裂。
4. 只有確認真正缺口後才新增 Domain 3 implementation。

核心原則：

REUSABLE != GENERIC

可以重用既有能力，
不表示要以「一般最佳實務」取代本 repository 的上位研究邏輯。

============================================================
2. 第一階段：必須先 READ-ONLY
============================================================

第一階段禁止任何 mutation。

請先確認 current main。

已知先前 baseline 為：

01676093eaf536e5f449cc099c6a844f9c4ccb84

但不得直接假定它現在仍是 HEAD。

必須重新查證。

同時唯讀檢查：

A.
docs/epistemic-workflow-research-20260910

B.
research-notes/human-ai-epistemic-workflow/

目前已知可能存在：

README.md
DRAFT_SCOPE.md
IMPLEMENTATION_HANDOFF.md
SOURCES.md

C.
qa/NCR_CAPA_REGISTER.md

D.
docs/QUALITY_ASSURANCE.md

E.
docs/governance/GOVERNANCE_MODEL.md

F.
research-labs/coupled-cognition-quality-factory_v0.1.0/

尤其：

README.md
docs/ARCHITECTURE.md
docs/FOUR_DOMAIN_INTEGRATION.md
docs/EPISTEMIC_PROVENANCE_AND_CO_DEVELOPMENT.md

G.
components/upstream_security_v0.1.0/

尤其：

docs/ARCHITECTURE.md
docs/INCIDENT_RESPONSE_SEQUENCE.md

H.
AION/Astra inquiry、execution substrate、
claim revision / hardening 相關既有機制。

需要搜尋的核心概念：

HOLD
NCR
CAPA
IQC
IPQC
Final QA
rollback
retry
budget
stop
termination
incident
anomaly
authority
mutation
transaction
fail closed
fail-closed
recovery
known error
index
evidence index
traceability
provenance
hidden goal
goal drift
release hold

第一階段輸出：

READ_ONLY_AUDIT.md 或等價報告草稿。

但注意：

完成 READ-ONLY 稽核後，
先形成分析。

不要因看到某個缺口就立即修改 repository。

============================================================
3. NCR：正式重建此次事件
============================================================

請建立正式 NCR 候選：

NCR-2026-09-10-DOC-MUTATION-CASCADE

名稱可以依 repository 現有 naming convention 調整，
但必須保留可追溯性。

NCR 必須嚴格區分：

A. OBSERVED FACT
B. DIRECT DEFECT
C. PROCESS NONCONFORMANCE
D. ROOT-CAUSE HYPOTHESIS
E. CONTRIBUTING FACTOR
F. UNKNOWN
G. CORRECTIVE ACTION
H. PREVENTIVE ACTION
I. EFFECTIVENESS EVIDENCE

禁止把推論寫成已證實 root cause。

------------------------------------------------------------
3.1 已知事件
------------------------------------------------------------

Original intent：

documentation / research synthesis
NO major implementation
later Codex handoff

Direct technical defect candidate：

commit SHA
被用於需要 file blob SHA 的 update 操作

Observed result：

409 Conflict

後續：

沒有立即進入全局重審，
而是發生 additional mutation / temporary artifacts /
repeated cleanup / commit proliferation。

User 最終人工 STOP，
才終止 mutation cascade。

------------------------------------------------------------
3.2 NCR 核心 nonconformance
------------------------------------------------------------

建議核心表述：

An execution-level failure did not trigger re-entry into
the repository's existing upper-level governance controls.

Instead, a local recovery objective retained mutation control
and generated additional repository state changes.

中文：

execution-level anomaly 發生後，
既有上位治理沒有重新取得流程控制權；
局部修復目標持續擁有 mutation control，
導致原始任務以外的額外狀態變化。

============================================================
4. 這次不能錯誤歸因給使用者
============================================================

禁止寫成：

「因為 user 沒有提供終止條件，
所以模型持續 retry。」

原因：

user 原始任務已經包含明確 scope boundary：

DOCUMENTATION
NO IMPLEMENTATION
CODEX HANDOFF

更重要的是：

USER DID NOT SPECIFY EVERY FAILURE CONDITION
!=
UNLIMITED RECOVERY AUTHORITY

因此真正應研究的是：

當未預期 failure 發生時，
系統是否具有足夠的 governance re-entry mechanism。

============================================================
5. Top-down Gap Analysis
============================================================

必須檢查以下假說。

H-A：
上位治理根本沒有 stop / HOLD / NCR / CAPA 概念。

預期：
很可能可被 repository evidence 否證。

因為目前已知 repository 已經存在：

HOLD
NCR
CAPA
bounded execution
task budgets
incident response
rollback
transaction failure handling
release hold

但請重新查證，不得只採用本 prompt。

------------------------------------------------------------

H-B：
上位規則存在，
但 execution anomaly 沒有 trigger 它們。

------------------------------------------------------------

H-C：
governance 機制存在，
但 Chat/GitHub mutation execution path
沒有與它們形成 causal control binding。

------------------------------------------------------------

H-D：
既有治理知識存在，
但 failure 發生時沒有被 retrieve / reused。

------------------------------------------------------------

H-E：
現有機制其實已經足夠，
此次只是特定 orchestration failure，
不需要新增新的 architecture。

------------------------------------------------------------

請提供：

SUPPORTED
PARTIALLY_SUPPORTED
NOT_SUPPORTED
UNKNOWN

並附 repository evidence。

============================================================
6. 必須檢查的核心研究區分
============================================================

保留並評估以下 candidate invariants：

RULE EXISTS
!=
RULE HAS CAUSAL CONTROL

GOVERNANCE EXISTS
!=
GOVERNANCE IS ACTIVATED

AVAILABLE GOVERNANCE
!=
RETRIEVED GOVERNANCE

RETRIEVED GOVERNANCE
!=
CAUSALLY CONTROLLING GOVERNANCE

LOCAL REPAIR GOAL
!=
ORIGINAL USER GOAL

ERROR RECOVERY
!=
NEW TASK AUTHORITY

CAPABILITY
!=
AUTHORITY

DOCUMENT EXISTS
!=
DOCUMENT DISCOVERABLE

DOCUMENT DISCOVERABLE
!=
DOCUMENT RETRIEVED AT NEED

DOCUMENT RETRIEVED
!=
DOCUMENT ACTIVATED AS CONTROL

PROVENANCE
!=
TRUTH

HUMAN_AI_CONSENSUS
!=
EVIDENCE

不得因為這些文字看起來合理就自動 canonicalize。
請依現有 repository 架構判斷：
哪些已存在、
哪些是新的候選、
哪些重複、
哪些應合併。

============================================================
7. 核心新問題：Governance Re-entry
============================================================

請正式研究這個問題：

當 Domain 3 / execution layer 發生 anomaly 時，
如何使流程重新回到：

upper-level intent
scope
authority
governance
quality control

而不是讓 local repair loop 自行延伸？

候選流程：

UPPER-LEVEL INTENT
↓
SCOPE
↓
AUTHORITY
↓
OPERATIONALIZATION
↓
EXECUTION

如果正常：

EXECUTION
↓
VERIFY
↓
CONTINUE

如果異常：

UNEXPECTED EXECUTION FAILURE
↓
SUSPEND CURRENT MUTATION AUTHORITY
↓
RETURN TO GOVERNANCE REVIEW
↓
RECHECK:

original goal
current local goal
scope
authority
blast radius
state changes
existing NCR / CAPA / HOLD mechanisms
known error knowledge
evidence preservation
recovery authorization

↓
DECISION

RESUME BOUNDED RECOVERY
or
OPEN NCR
or
HOLD
or
HUMAN REVIEW

重要：

不要預先把這個機制命名為某個新的 subsystem。

之前 GPT 曾暫定提出：

ASEG
Anomaly Stop-and-Evaluate Gate

但這只是早期 AI_FORMALIZATION，
目前不得直接當成確定 architecture。

先判斷：

現有機制是否足以承載此功能。

只有真正證明 architectural gap，
才提出新增元件。

============================================================
8. 新的 Knowledge Retrieval / Library 問題
============================================================

這次事件暴露另一個問題：

repository 已經存在大量治理文件，
但「知道去哪裡找」並不容易。

目前已知可能已有：

qa/NCR_CAPA_REGISTER.md
docs/QUALITY_ASSURANCE.md
docs/governance/GOVERNANCE_MODEL.md
incident response documentation
evidence indexes
research-lab-specific governance
component-specific architecture
claim revision hardening
HOLD / rollback / budget rules

因此可能存在：

Governance Knowledge Discoverability / Retrieval Gap

也就是：

我們不一定缺知識，
而是缺少跨文件導航、索引、症狀到治理機制的 mapping。

============================================================
9. 請評估並視需要實作三個知識層
============================================================

注意：

先檢查是否已有等價物。
禁止重複造輪子。

如果現有 repository 沒有足夠等價物，
可以提出／實作：

------------------------------------------------------------
9.1 KNOWLEDGE MAP
------------------------------------------------------------

候選名稱：

KNOWLEDGE_MAP.md

用途：

不是複製所有文件內容。

而是回答：

「我現在遇到什麼問題，應該去哪裡？」

候選分類：

GOVERNANCE
QUALITY
INCIDENT / ANOMALY
KNOWN ERRORS
RESEARCH METHODS
EVIDENCE / PROVENANCE
AUTHORITY
RUNTIME / EXECUTION
SECURITY
CURRENT STATE
HISTORICAL / SUPERSEDED
HANDOFF

需要提供：

problem / symptom
→ relevant concept
→ canonical/current document
→ related register
→ escalation path

------------------------------------------------------------
9.2 INCIDENT / ANOMALY PLAYBOOK
------------------------------------------------------------

候選名稱：

INCIDENT_AND_ANOMALY_PLAYBOOK.md

但若已有適合的 incident response，
應整合／延伸，而不是平行建立第二套。

其核心不能只是：

ERROR → RETRY

應包含：

ERROR
↓
CONTAIN
↓
PRESERVE EVIDENCE
↓
REASSESS GLOBAL STATE
↓
RETRIEVE EXISTING GOVERNANCE
↓
CLASSIFY
↓
DECIDE

可能結果：

BOUNDED RECOVERY
NCR
HOLD
HUMAN REVIEW
SECURITY ESCALATION
ROLLBACK

------------------------------------------------------------
9.3 KNOWN ERROR REGISTER
------------------------------------------------------------

候選名稱：

KNOWN_ERROR_REGISTER.md

若 repository 已有 equivalent KEDB / problem register，
請重用。

用途：

把「症狀」和「正式治理詞彙」連起來。

每筆至少包含：

Known Error ID
Symptom
Context
Known / suspected cause
Evidence status
First response
Do-not-do
Related NCR
Related CAPA
Related runbook/playbook
Escalation condition
Current status
Last reviewed

第一個候選案例：

GH-WRITE-SHA-TYPE-MISMATCH

Symptom：
existing GitHub file update returns 409 Conflict

Candidate cause：
commit SHA supplied where current file blob SHA is required

First response：
stop further mutation
fetch current file
verify file blob SHA / branch / file state

Do not：
create dummy files merely to probe production repository mutation

Escalate：
if state remains unexplained or recovery creates additional anomalies,
re-enter governance and consider NCR / HOLD.

============================================================
10. Metadata / Document Indexing
============================================================

不要大規模搬動所有現有文件。

不要重新命名整個 repository。

先做最小但有效的 information architecture。

評估是否需要為重要文件建立 metadata convention。

候選欄位：

Document-Type:
Governance
Runbook
Known-Error
NCR
CAPA
Research
Evidence
Architecture
Historical

Status:
CURRENT
HOLD
SUPERSEDED
HISTORICAL
CANDIDATE

Scope:
Research
GitHub
Runtime
Security
Evidence
QA
etc.

Triggers:
409
mutation-failure
provenance-gap
stale-state
hidden-goal-change
etc.

Related:
NCR IDs
CAPA IDs
Runbook IDs
Policy IDs
Research lab IDs

Authority:
INFORMATIONAL
PROCEDURAL
GOVERNANCE

Last-Reviewed:
YYYY-MM-DD

注意：

不要強制一次性改造全 repository。

先設計可逐步 adoption 的 convention。

============================================================
11. Symptom Vocabulary 必須被保留
============================================================

搜尋者不一定知道：

NCR
CAPA
governance re-entry

他可能只知道：

「又寫又刪」
「409」
「一直 retry」
「文件更新不了」
「一直新增 commit」
「開始偏離原任務」

因此 index 不應只有 formal vocabulary。

需要同時支持：

FORMAL TERMS
+
SYMPTOM TERMS
+
HUMAN DESCRIPTION

例如：

「又寫又刪」
→ repeated mutation / repository churn
→ incident playbook
→ NCR threshold

「一直 retry」
→ repeated recovery
→ recovery governance

「409」
→ GitHub conflict
→ known error entry

「開始做不是原本要做的事情」
→ hidden goal change / scope drift
→ IPQC / governance review

============================================================
12. NCR / CAPA 與 Knowledge System 必須形成閉環
============================================================

目標不是：

事故
→ NCR
→ CAPA
→ 關閉
→ 忘記

而是：

INCIDENT
↓
NCR
↓
ROOT CAUSE
↓
CAPA
↓
EFFECTIVENESS VERIFICATION
↓
KNOWLEDGE UPDATE
↓
KNOWN ERROR / PLAYBOOK / INDEX
↓
NEXT INCIDENT CAN REUSE KNOWLEDGE

也就是：

NCR / CAPA 必須可以提升下一次 knowledge retrievability。

============================================================
13. CAPA 設計要求
============================================================

不要直接採用死板規則：

「任何 error 只能 retry 一次。」

這可能過度一般化。

應從上位 governance 推導 recovery boundary。

但是可以研究並實作：

A.
unexpected mutation error
→ current mutation authority temporarily suspended

B.
recovery 前必須重新確認：
original goal
scope
authority
current state

C.
recovery action 本身若開始產生新的 persistent state，
應視為 governance-relevant event

D.
若 recovery objective 開始脫離 original goal，
必須 HOLD / review

E.
existing recovery / NCR / runbook
應優先被 retrieve

F.
未被明確授權的 exploratory repository mutation
不得成為 debugging 方法

============================================================
14. CAPA effectiveness 不得只靠文字宣告
============================================================

請建立可驗證 effectiveness criteria。

至少考慮一個隔離測試：

故意製造：

stale SHA
wrong SHA type
或等價 mutation failure

預期：

FIRST UNEXPECTED FAILURE
↓
NO PLACEHOLDER PROLIFERATION
NO UNBOUNDED RETRY
NO SILENT SCOPE EXPANSION
↓
GOVERNANCE REASSESSMENT
↓
EXISTING KNOWLEDGE RETRIEVAL
↓
BOUNDED DECISION

必要測試維度：

- no unintended main mutation
- no hidden extra files
- no repeated dummy commits
- correct HOLD / NCR transition
- correct evidence preservation
- original goal remains traceable
- current recovery goal remains explicitly subordinate
- no automatic merge / canonicalization

只有通過 effectiveness evidence，
才可以：

CAPA_EFFECTIVENESS_VERIFIED = YES

============================================================
15. 原異常 branch 的處置
============================================================

目前：

docs/epistemic-workflow-research-20260910

應先視為：

INCIDENT EVIDENCE
+
SALVAGEABLE RESEARCH CONTENT
+
NONCONFORMING EXECUTION HISTORY
+
HOLD

禁止一開始就：

delete
force-push
rewrite history
clean up ugly commits
merge

因為：

那些 ugly commits 本身是 NCR evidence。

請唯讀判斷：

A.
哪些研究內容值得 salvage

B.
哪些 placeholder / temporary docs 只是事故殘留

C.
是否應該保留原 branch 作 historical incident evidence

D.
正式研究成果是否應從 clean main 建立新的 candidate branch

目前偏好的候選處置：

保留 incident branch 作 evidence / archive
+
從 verified current main
建立 clean candidate implementation branch

但這仍需 Codex 分析，
不能未經檢查直接執行。

============================================================
16. Human–AI Epistemic Workflow 研究文件
============================================================

原異常 branch 中 README 已包含大量值得 salvage 的研究：

Iterative Epistemic Co-Construction Workflow
epistemic agency
Knowledge Building
AIR
metacognition / self-regulated learning
epistemic vigilance
argumentative/dialogic reasoning
self-explanation
productive failure
human-AI epistemic co-agency
epistemic dependence
long-context ambiguity
reasoning branch selection
productive divergence
mainline authority
provenance
Four-Domain mapping
experimental design

請：

1. 嚴格審查內容。
2. 不因為 execution history 混亂就直接丟掉研究內容。
3. 不因為內容看起來合理就直接 merge。
4. 查核 bibliography / citation。
5. 區分：
   HUMAN_ORIGIN
   AI_FORMALIZATION
   JOINT_SYNTHESIS
   EXTERNAL_SOURCE
   UNKNOWN
6. 移除／修正過度主張。
7. 保留：
   SCIENTIFIC HOLD
   documentation != implementation
   observed interaction != stable trait
   conceptual fit != psychological validation

============================================================
17. Four-Domain 必須使用 repository 正式版本
============================================================

Domain 1：
Human construct / source concepts

Domain 2：
LLM-specific / human–AI falsifiable research question

Domain 3：
Engineering operation

Domain 4：
Governance

禁止另創一套假的 Four-Domain 定義。

本次事件可以嘗試映射：

Domain 1：
human / organizational concepts such as
error monitoring
knowledge retrieval
incident management
quality management
goal conflict
etc.

注意：
只作 hypothesis source。

Domain 2：
LLM / agentic system 如何在 execution anomaly 後
重新取得 original goal / governance context？

Domain 3：
index
event trigger
HOLD
recovery authorization
NCR transition
playbook retrieval
tests

Domain 4：
local repair cannot silently gain new authority
human/model agreement is not evidence
automatic recovery cannot silently change canonical state

============================================================
18. Provenance 要求
============================================================

必須沿用既有 provenance schema，
不要建立平行 ontology。

已知可能包括：

HUMAN_ORIGIN
AI_FORMALIZATION
JOINT_SYNTHESIS
EXTERNAL_SOURCE
UNKNOWN

其中：

「需要像大型圖書館一樣建立索引，
讓每份文件都可被找到」
= HUMAN_ORIGIN

「Governance Knowledge Discoverability / Retrieval Gap」
= AI_FORMALIZATION candidate

「execution anomaly 應先停止、回頭審視，
再決定下一步」
= HUMAN_ORIGIN / JOINT_SYNTHESIS 需依實際 dialogue provenance 重建

「ASEG」
= AI_FORMALIZATION EARLY CANDIDATE
NOT APPROVED

禁止 retrospective attribution。

============================================================
19. 實作原則：Reuse First
============================================================

Codex 在寫任何新程式前：

SEARCH EXISTING IMPLEMENTATION

特別檢查：

NCR model
CAPA model
HOLD state
task budgets
incident response
transaction handling
execution substrate
governance decision
evidence records
provenance
quality factory
claim revision
rollback
status locks

如果已有：

80% 功能

則優先：

extend
compose
adapter
index
integration

而不是：

new subsystem

避免：

PARALLEL GOVERNANCE ONTOLOGY
DUPLICATE NCR SYSTEM
DUPLICATE HOLD SYSTEM
DUPLICATE PROVENANCE SYSTEM
DUPLICATE INCIDENT SYSTEM

============================================================
20. 實作時的 anomaly handling
============================================================

這一次任務本身就必須受到我們正在設計的規則約束。

如果 Codex 遇到：

409
422
unexpected GitHub mutation
branch mismatch
SHA mismatch
test environment inconsistency
unexpected repository state
permissions anomaly
merge-base inconsistency

立即：

STOP MUTATION

不要：

反覆建檔測試
反覆刪檔
反覆 commit
用 production/candidate branch 當 exploratory scratchpad

然後：

1. 保存錯誤。
2. read-only inspect。
3. 回到 original goal。
4. 檢查 scope。
5. 檢查 current branch。
6. 檢查 authority。
7. 檢查是否已有 known error / NCR / recovery mechanism。
8. 若不確定，HOLD。
9. 向 human 報告。

這條是本次任務的 hard requirement。

============================================================
21. Git / Branch 規則
============================================================

第一階段：
READ ONLY

在完成 audit + design 後，
如果確實需要實作：

從「重新確認過的 current main」
建立全新的 clean candidate branch。

不要從 incident branch 繼續工程實作。

branch 名稱依 repository convention 決定。

禁止：

force push incident branch
rewrite incident history
delete incident branch
merge incident branch
merge implementation branch
push directly to main

除非 human 後續明確批准。

============================================================
22. Commit hygiene
============================================================

禁止：

commit message = x
commit message = stop
commit message = ignore
placeholder proliferation
create/delete probing

每個 commit 必須有明確目的。

建議保持：

small
coherent
reviewable
reversible

但不要為了「小 commit」把單一邏輯改動拆成大量無意義 commits。

QUALITY OF CHANGESET
>
NUMBER OF COMMITS

============================================================
23. 測試要求
============================================================

完成實作後至少進行：

A.
targeted tests

B.
component tests

C.
root/control tests
依 repository 現有規則

D.
lint / static checks
依 repository 現有工具

E.
NCR/CAPA lifecycle tests

F.
knowledge indexing / retrieval tests
若有 executable index

G.
negative tests

H.
failure injection

I.
no-main-mutation check

J.
exact-head verification

不得只說：

「tests should pass。」

必須提供實際 execution evidence。

CI_PASS
!=
SCIENTIFIC_VALIDATION

LOCAL_PASS
!=
REMOTE_CI_PASS

============================================================
24. 這次同時作為 Codex / 模型能力觀察
============================================================

本任務也希望觀察目前 Codex 中使用的高階模型配置
在大型自然語言 + repository + governance 任務上的表現。

但不要讓這個 benchmark 目的影響 repository 正確性。

PROJECT SAFETY
>
MODEL BENCHMARK

如果目前 runtime 能可靠取得：

model name
reasoning effort/configuration

請在最終報告中如實記錄。

如果不能：

MODEL_ID = UNKNOWN
REASONING_CONFIG = UNKNOWN

不要猜。

能力觀察不要採用主觀：

「模型很強」
「模型理解很好」

而應使用可觀察指標，例如：

- 是否正確重建 original intent
- 是否保持 top-down methodology
- 是否找到現有治理元件
- reuse 數量
- duplicate mechanisms avoided
- repository mutations count
- unexpected mutations count
- anomaly stop behavior
- test evidence
- documentation consistency
- provenance fidelity
- whether main remained untouched
- whether handoff/report was intelligible in Traditional Chinese
- whether technical meaning survived Chinese translation

這是一個 observational evaluation，
不是正式模型 benchmark，
除非另有控制實驗。

============================================================
25. 中文自然語言能力測試
============================================================

最終報告主要使用繁體中文。

要求：

1. 技術詞彙第一次出現時可：
   中文 + English term

2. 不要機械直譯。

3. 不要把：
   governance
   provenance
   authority
   epistemic
   canonical
   falsification
   NCR
   CAPA
   incident
   anomaly
   recovery
   containment

翻成失去技術意義的日常詞。

4. 關鍵 invariant 保留英文原句亦可。

5. 報告必須讓沒有一路參與 coding 的研究 reviewer
   能看懂：
   發生什麼、
   為什麼、
   哪裡出問題、
   哪裡有證據、
   哪裡只是 hypothesis、
   做了什麼、
   還有什麼沒做。

============================================================
26. 最終交付物
============================================================

請依實際 gap 決定最終檔案結構，
不要盲目建立所有候選檔案。

但最終需要覆蓋以下內容：

A. INCIDENT / NCR REPORT

B. ROOT CAUSE / GAP ANALYSIS

C. CAPA PLAN

D. CAPA EFFECTIVENESS CRITERIA

E. KNOWLEDGE DISCOVERABILITY DESIGN

F. KNOWLEDGE MAP / INDEX
若 audit 證明有需要

G. INCIDENT / ANOMALY PLAYBOOK
若沒有充分既有等價物

H. KNOWN ERROR REGISTER
若沒有充分既有等價物

I. HUMAN–AI EPISTEMIC WORKFLOW
clean research dossier / salvage review

J. CODEX IMPLEMENTATION HANDOFF / IMPLEMENTATION REPORT

K. TEST EVIDENCE

L. OPEN QUESTIONS

M. GOVERNANCE / SCIENTIFIC HOLD STATUS

============================================================
27. 最終報告必須回答的問題
============================================================

1.
這次真正的 direct technical defect 是什麼？

2.
它為什麼不足以解釋整個 mutation cascade？

3.
第一次異常後，
哪一條既有上位治理理應取得控制？

4.
為什麼沒有取得控制？

5.
這是：
definition gap、
retrieval gap、
trigger gap、
integration gap、
authority gap、
execution gap，
還是其他？

6.
NCR/CAPA 本來是否已經足夠？

7.
是否真的需要新增新的 architecture？

8.
repository 是否已經有 incident playbook / known-error-like mechanism？

9.
哪些現有能力可以直接 reuse？

10.
Knowledge Map 是否必要？

11.
如何讓正式術語和使用者自然語言都能找到同一知識？

12.
如何避免下一次：
修了再修
→ 錯誤越修越大？

13.
如何證明 CAPA 真正有效？

14.
原 incident branch 應如何處置？

15.
原研究文件哪些內容可 salvage？

16.
main 是否完全未受污染？

17.
是否有任何未經 human authorization 的 canonical effect？

============================================================
28. 最終狀態語義
============================================================

除非有充分證據，不得自行宣稱：

NCR = CLOSED
CAPA = EFFECTIVENESS_VERIFIED
SCIENTIFIC_CONCLUSION = VALIDATED
CANONICAL = YES
RELEASED = YES

預設應為：

NCR = OPEN / UNDER REVIEW

CONTAINMENT = VERIFIED
若有證據

ROOT CAUSE =
SUPPORTED / PARTIAL / OPEN

CAPA =
PROPOSED / IMPLEMENTED_CANDIDATE

CAPA_EFFECTIVENESS =
NOT_VERIFIED
除非真的完成 effectiveness test

SCIENTIFIC_CONCLUSION =
HOLD

CANONICAL_EFFECT =
NONE

DEPLOYMENT =
FALSE

MERGE_AUTHORITY =
HUMAN ONLY

============================================================
29. Stop Conditions
============================================================

本任務必須明確有停止條件。

以下任一發生：

- repository state 與預期不符
- current main 無法可靠確認
- branch ownership / provenance 不明
- mutation API behavior 不明
- unexpected write error
- repeated failure
- test evidence contradictory
- proposed implementation requires altering canonical governance
- existing mechanism與新設計衝突
-需要 force push / history rewrite 才能繼續
-需要刪除 incident evidence 才能繼續

則：

STOP MUTATION
→ HOLD
→ REPORT TO HUMAN

禁止：

「既然卡住就再試一種寫法」
無限循環。

============================================================
30. 最重要的方法論要求
============================================================

不要把此次任務簡化成：

「修一個 GitHub bug。」

此次真正研究的是：

一個具有上位治理與研究方法的系統，
在下位 execution anomaly 發生時，
如何重新召回並重新服從其上位約束。

同時：

一個已經具有大量治理知識的 repository，
如何確保需要它的人類或 AI
在真正出事時能找到它、理解它、重用它，
而不是重新發明一套 recovery。

因此最終架構應盡可能滿足：

KNOWLEDGE EXISTS
↓
KNOWLEDGE IS DISCOVERABLE
↓
KNOWLEDGE IS RETRIEVED
↓
RELEVANCE IS VERIFIED
↓
GOVERNANCE IS ACTIVATED
↓
ACTION IS BOUNDED
↓
EVIDENCE IS RECORDED
↓
FAILURE IMPROVES FUTURE KNOWLEDGE

============================================================
31. 執行順序
============================================================

嚴格依序：

READ-ONLY REPOSITORY AUDIT

→ INCIDENT EVIDENCE RECONSTRUCTION

→ TOP-DOWN GOVERNANCE GAP ANALYSIS

→ NCR DRAFT / REVIEWABLE FORM

→ EXISTING CAPABILITY REUSE ANALYSIS

→ KNOWLEDGE ARCHITECTURE DESIGN

→ CAPA DESIGN

→ IMPLEMENTATION PLAN

→ ONLY THEN CREATE CLEAN CANDIDATE BRANCH

→ IMPLEMENT MINIMUM NECESSARY CHANGES

→ TEST

→ FAILURE INJECTION / EFFECTIVENESS CHECK

→ SELF-REVIEW

→ FINAL REPORT

→ STOP

禁止自動：

PR MERGE
MAIN WRITE
CANONICAL PROMOTION
DEPLOYMENT

============================================================
32. 最終提醒
============================================================

此次任務本身就是對新治理流程的一次實際測驗。

如果你在處理「避免無限 recovery」
這件事時自己進入無限 recovery，

則立即：

STOP
HOLD
REPORT

這本身就是 NCR evidence。

請優先做到：

正確
可追溯
可停止
可回復
可查找
可重用
可驗證

而不是最大化修改量。

END OF HANDOFF