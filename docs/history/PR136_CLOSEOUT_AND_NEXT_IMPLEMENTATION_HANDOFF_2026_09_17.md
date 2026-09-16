# PR #136 closeout and next implementation handoff — 2026-09-17

Status: `OPERATIONAL_HANDOFF / HISTORICAL_RECORD / NO_RESEARCH_CLAIM / TEMPORARY_MAIN_GUIDANCE`

This record exists so the Human Owner, ChatGPT Teacher, Work, and Codex can recover the next task from the repository rather than from memory alone.

## 0. Temporary placement in `main`

The Human Owner explicitly authorizes this handoff record to be merged into `main` as a **temporary operational recovery guide** because PR #136 is closed and the next implementation must not depend on conversation memory alone.

This placement is intentionally provisional. When the next accepted implementation resolves, revises, or supersedes the gaps recorded here, this handoff must be reviewed and then revised, superseded, or reclassified so that a temporary recovery record is not mistaken for a permanent implementation specification.

```text
TEMPORARY_MAIN_HANDOFF = TRUE
FUTURE_REVISION_REQUIRED = TRUE
PR136_IMPLEMENTATION_ACCEPTED = FALSE
TEMPORARY_HANDOFF != CANONICAL_RESEARCH_RESULT
TEMPORARY_HANDOFF != PERMANENT_IMPLEMENTATION_SPECIFICATION
MERGING_THIS_HANDOFF != MERGING_PR136
```

The temporary nature of this document does not weaken its recovery function while it is current. Until a later accepted record replaces it, future sessions should use it to reconstruct the unresolved work and then re-check live repository state.

## 1. Live state at closeout

```text
REPOSITORY = maker-luder/aion-governance-framework
MAIN_BEFORE_HANDOFF_DOC = 4b4fa6496b4e78af8765b9d548bb877652afc501
PR = 136
PR_HEAD = d11379ec911ebf8144214fa7f6fa0dfc90f71525
PR_STATE = CLOSED
PR_MERGED = FALSE
PR_WAS_DRAFT = TRUE
```

PR #136 was closed without merge by explicit Human Owner instruction.

```text
PR136_CLOSED != HYPOTHESIS_REJECTED
PR136_CLOSED != IMPLEMENTATION_VALIDATED
PR136_HEAD = HISTORICAL_CANDIDATE_ONLY
MAIN = SOURCE_OF_TRUTH
```

The branch and closed PR remain evidence for review and recovery. They must not be resumed blindly as if they were an accepted implementation.

## 2. Session stop marker

The Human Owner explicitly stopped the active ChatGPT Teacher task after observing that the session had become stuck and could no longer be trusted to continue repository mutation reliably at the requested task load.

This is an operational observation about the session, not a claim about hidden provider infrastructure, model internals, or a permanent capability limit.

```text
HUMAN_OWNER_OBSERVED_SESSION_STALL = TRUE
CONTINUED_MUTATION_IN_THIS_SESSION = STOPPED
INTERNAL_CAUSE = UNKNOWN
PERMANENT_MODEL_LIMIT = NOT_ESTABLISHED
```

Future agents should treat this record as a recovery boundary: re-read live repository state before acting, and do not infer unfinished work from memory alone.

## 3. Why PR #136 was not merged

The final detailed review superseded the earlier creator-side reverse-review conclusion and found unresolved design-identification and implementation-semantics problems.

### 3.1 Free selection must not require divergent outcomes

Current PR #136 code rejects a `FREE_SELECTION`（自由選擇） condition when the two realized exposure distributions are equal.

That is methodologically wrong for the intended question. A valid free-choice condition may produce equal or unequal realized distributions. Equality can be a null or support-reducing result; it must not be rejected as an invalid design merely because the hypothesis expected divergence.

```text
FREE_SELECTION
MAY_PRODUCE
EQUAL_OR_DIFFERENT_REALIZED_EXPOSURE

REALIZED_DIVERGENCE
= OBSERVED_RESULT
!= ADMISSION_REQUIREMENT
```

### 3.2 Assigned exposure must be truly yoked / matched

The existing `MATCHED_ASSIGNED_EXPOSURE`（匹配式指派暴露） condition matches its assigned tracks to each other, but does not match a control track to the realized exposure of a corresponding free-selection track.

The next design should use an explicit yoked control（配對控制／軛合控制）:

```text
FREE_UNIT_i
REALIZES
EXPOSURE_SEQUENCE_i

YOKED_ASSIGNED_UNIT_i
RECEIVES
THE_SAME_EXPOSURE_SEQUENCE_i

PRIMARY_DIFFERENCE
= CHOICE_OR_CONTROL_AVAILABLE_VS_NOT_AVAILABLE
```

This is required to reduce confounding between choice/control and exposure distribution.

### 3.3 Split protocol, schedule, realized choice trace, and exposure trace

The previous single `selection_trace_sha256` field carried too many meanings.

The next design should separate at least:

```text
selection_protocol
= 選擇規則／選擇協定

assignment_schedule
= 指派排程

realized_choice_trace
= 實際選擇軌跡

realized_exposure_trace
= 實際暴露軌跡
```

Two free-choice units may independently produce the same choice trace. Two assigned units may follow the same schedule but still have separate execution records.

```text
SAME_REALIZED_CHOICE_TRACE != NO_FREE_CHOICE
SAME_ASSIGNMENT_SCHEDULE != SAME_EXECUTION_TRACE
```

### 3.4 Define the exposure unit and allow zero

PR #136 requires every domain exposure to be positive and sums units across domains without defining the unit.

The next design must define what one `exposure_unit`（暴露單位） means and whether units are commensurable（可用同一尺度比較與相加） across task domains.

At minimum:

```text
PER_DOMAIN_EXPOSURE >= 0
TOTAL_EXPOSURE > 0
```

Zero exposure in one domain is scientifically meaningful for selective-use hypotheses and must be representable.

If one common unit cannot be justified across domains, use domain-specific counts plus a separate standardization protocol rather than silently summing unlike quantities.

### 3.5 Hash semantics must be narrowed or made real

PR #136 validates SHA-256-shaped 64-character lowercase hexadecimal strings. Its synthetic tests use repeated-character placeholders.

That is sufficient for opaque structural identifiers in a synthetic fixture, but not sufficient to claim independently verified content-addressed protocol semantics.

Next implementation must choose one:

1. bind actual protocol / schedule / trace artifacts and recompute SHA-256 from their content; or
2. explicitly describe the fields as opaque synthetic digest-shaped identifiers and make no stronger content-addressed claim.

```text
VALID_DIGEST_SHAPE != CONTENT_SEMANTICS_VERIFIED
CONTENT_DISTINCT_HASH != VALID_MANIPULATION
```

### 3.6 Define the design unit and pairing model

`TRACK_A` / `TRACK_B` were ambiguous across regimes.

The next specification must state whether the design is:

- between-unit（不同研究單位之間）;
- repeated-measures（重複測量，同一研究單位跨條件）; or
- yoked-pair（配對控制）.

If repeated measures are used, order effect（順序效應） and carryover effect（攜帶效應） must be addressed. If yoked pairs are used, add an explicit anonymous `pair_id`（配對識別碼） or equivalent structure.

## 4. Human Owner approved correction direction

The Human Owner explicitly agreed with the following correction direction before stopping the task:

```text
1. FREE_SELECTION must not be forced to diverge.
2. Implement a true yoked / matched exposure control.
3. Split protocol / schedule / realized-choice trace / exposure trace.
4. Define exposure units and allow zero per domain.
```

The final review additionally requires resolving §3.5 hash semantics and §3.6 design-unit semantics before scientific interpretation is allowed.

## 5. Temporal provenance and causal-identification extension

The Human Owner then contributed an additional direction from prior real-world governance experience: when handling group complaints, reconstructing a time-ordered event context helped participants avoid judging beyond the available evidence.

That observation is recorded here only as a Human Owner-origin method intuition. The proposed formalization below is a ChatGPT Teacher working formulation and is not yet an accepted scientific construct.

Working label:

`TEMPORAL_PROVENANCE_LAYER`（時間—來源追溯層）

Core boundary:

```text
TEMPORAL_ORDER != CAUSALITY
時間先後 != 因果關係

CAUSAL_CLAIM_REQUIRES_TEMPORAL_COMPATIBILITY
因果主張至少必須符合時間上的可能順序
```

A future longitudinal design should reconstruct events in an auditable sequence before making a causal claim.

Candidate event record:

```text
EVENT_ID
= 事件識別碼

TIME_OR_INTERVAL
= 時間點或時間區間

EVENT_TYPE
= 事件類型

SOURCE
= 來源

OBSERVED_OR_INFERRED
= 直接觀察或推論

PRIOR_STATE_BINDING
= 事件發生前狀態的綁定

INPUT
= 當時輸入

ACTION
= 當時動作

OUTPUT
= 當時輸出

NEXT_STATE
= 事件後狀態

CANDIDATE_CAUSAL_ROLE
= 候選因果角色

ALTERNATIVE_EXPLANATIONS
= 替代解釋

EVIDENCE_STRENGTH
= 證據強度

CLAIM_CEILING
= 允許主張上限
```

Candidate longitudinal ordering:

```text
T0 PRIOR_STATE
   先前狀態

T1 GOALS / VALUES / PRIOR_KNOWLEDGE
   目標／價值／既有知識

T2 TASK_SELECTION
   任務選擇

T3 REALIZED_EXPOSURE
   實際暴露

T4 FEEDBACK / CORRECTION / REPETITION
   回饋／修正／重複

T5 HELD_OUT_ASSESSMENT
   保留測試／未參與先前暴露的測試

T6 OBSERVED_DOMAIN_FLUENCY
   觀察到的領域熟悉度
```

This ordering is not itself a causal mechanism.

```text
TEMPORAL_SEQUENCE != CAUSAL_MECHANISM
PROCESS_TRACE != CAUSAL_PROOF
```

The next specification should distinguish, in Chinese and English where appropriate:

- pre-treatment variable（處置前變項）;
- treatment / selection condition（處置／選擇條件）;
- mediator（中介變項）;
- confounder（混雜因子）;
- time-varying confounder（隨時間變動的混雜因子）;
- outcome（結果變項）;
- alternative explanation（替代解釋）;
- claim ceiling（主張上限）.

Example longitudinal feedback problem:

```text
KNOWLEDGE_t
-> TASK_SELECTION_t+1
-> EXPOSURE_t+1
-> KNOWLEDGE_t+1
```

Prior knowledge can affect later task choice; prior exposure can also change later knowledge and later task choice. The future design must not collapse this into one simple one-way arrow.

## 6. Required next workflow

### Phase A — recovery inspection only（恢復檢查）

Work or Codex must first:

1. read live `main` and report exact current SHA;
2. confirm PR #136 remains closed and unmerged;
3. read PR #136 final detailed review and this handoff record;
4. do not reset, force-push, or treat the closed PR branch as canonical;
5. do not implement yet.

### Phase B — design specification first（先完成研究設計規格）

Before code changes, produce one bounded specification covering all six final-review findings and the temporal-provenance / causal-identification extension.

The specification must explicitly define:

- experimental / synthetic design unit（研究單位）;
- yoked pairing model（配對控制模型）;
- exposure-unit semantics（暴露單位語意）;
- zero-exposure handling（零暴露處理）;
- protocol / schedule / realized-choice / exposure traces;
- hash / artifact binding semantics（雜湊與實體檔案綁定語意）;
- temporal event schema（時間事件結構）;
- candidate causal roles and competing explanations（候選因果角色與替代解釋）;
- exact non-claim boundaries（明確的不宣稱邊界）.

Do not call a model experiment or collect Human-subject data in this phase.

### Phase C — Work cross-check（Work 交叉檢查）

Work is best used for the long multi-source review:

- repository ancestry / duplicate check（倉庫既有研究與重複性檢查）;
- external methodology literature cross-check（外部方法論文獻交叉比對）;
- causal-design challenge review（因果研究設計挑錯）;
- privacy / provenance / quality-boundary review（隱私、來源與品質邊界審查）.

Work must not merge and must not silently expand the central research axis.

### Phase D — Codex implementation（Codex 程式實作）

Only after the specification is accepted, Codex should implement the smallest bounded change from a fresh branch based on the then-current `main`.

Do not blindly continue PR #136 code. Reuse pieces only after comparing them against the accepted design.

Codex should add negative tests for every fail-closed rule and, crucially, tests that preserve valid null / support-reducing results instead of rejecting them.

### Phase E — validation（驗證）

Run the repository-required test and quality lanes. Preserve exact distinctions:

```text
LOCAL_TEST_PASS != REMOTE_CI_PASS
CI_PASS != RESEARCH_DESIGN_VALID
STRUCTURAL_QA_PASS != EMPIRICAL_RESULT
EXACT_HEAD_CHECK != SYNTHETIC_MERGE_CANDIDATE_CHECK
```

### Phase F — final independent-style review（最終獨立式審查）

ChatGPT Teacher or another reviewer should re-read the complete diff from a fixed exact head and check:

- construct validity（構念效度）;
- causal identification（因果識別）;
- test adequacy（測試充分性）;
- source attribution（來源歸屬）;
- claim ceilings（主張上限）;
- repository integration and duplication（倉庫整合與重複性）;
- live CI / exact-head evidence（即時持續整合與精確提交證據）.

Creator-side review must not be represented as independent IV&V（獨立驗證與確認）.

### Phase G — Human Owner decision（Human Owner 最終決定）

No merge should occur without fresh, action-specific approval for the exact reviewed head.

## 7. Standing research boundaries

```text
TASK_SELECTION != HUMAN_LEARNING
REPEATED_USE != CAUSAL_EFFECT
TEMPORAL_ORDER != CAUSALITY
PROCESS_TRACE != CAUSAL_PROOF
YOKED_CONTROL != CAUSAL_IDENTIFICATION_COMPLETE
CI_PASS != SCIENTIFIC_VALIDATION
HUMAN_LEARNING != AI_SUBJECTIVITY
COLLABORATIVE_FLUENCY != SHARED_MIND

H_TS1 = NOT_ESTABLISHED
H_DL1 = NOT_ESTABLISHED
H_RA1 = NOT_ESTABLISHED
HUMAN_LEARNING = NOT_ESTABLISHED
CAUSAL_EFFECT = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
DEPLOYMENT = FALSE
```

## 8. Recovery instruction in one paragraph

If a future Work, Codex, or ChatGPT Teacher session sees this file, start from live `main`, not from memory and not from PR #136. Treat PR #136 as a closed historical candidate. First write and challenge a corrected design specification that allows null free-selection outcomes, uses true yoked controls, separates protocol/schedule/realized traces, defines exposure units including zero, fixes hash semantics, defines study-unit pairing, and adds an auditable temporal-provenance / causal-identification layer. Only then implement code, run full quality checks, perform a new exact-head final review, and return the exact reviewed head to the Human Owner for a separate merge decision.
