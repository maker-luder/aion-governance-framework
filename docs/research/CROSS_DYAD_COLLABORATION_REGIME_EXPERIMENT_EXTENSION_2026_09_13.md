# Cross-dyad collaboration-regime experiment extension — 2026-09-13

Status: `RESEARCH_HYPOTHESIS_EXTENSION / BOUNDED_IMPLEMENTATION_AUTHORIZED / DRAFT`
Canonical effect: `NONE`
Deployment: `FALSE`
Merge authorization: `NONE`
Main-write authorization: `NONE`

## 1. Purpose

This note extends the existing dyad-level anomaly-driven recursive epistemic inquiry hypothesis with a cross-condition question:

> Under otherwise matched model, task, and tool conditions, can different longitudinal interaction histories and externalized collaboration protocols produce measurably different task-transformation, verification, error-detection, tool-use, and closure behavior?

The motivating observation came from comparing two individual Human–ChatGPT interactions that appeared to adopt different working styles despite being part of the same product family. That single comparison is only a hypothesis trigger.

```text
ONE_HUMAN_AI_DYAD
!= POPULATION_EVIDENCE

TWO_DIFFERENT_DYADS
!= CAUSAL_PROOF

SAME_PROVIDER_OR_MODEL_FAMILY
!= SAME_EFFECTIVE_COLLABORATION_STATE
```

No claim about all ChatGPT users, Plus users, or model instances is permitted from the motivating anecdote.

## 2. Provenance

### HUMAN_OWNER_ORIGINAL

The Human Owner observed and asked whether:

- apparently similar ChatGPT products can settle into materially different collaboration styles with different Humans;
- one collaboration may primarily explain / produce / close a task while another may transform an ordinary event into a research question, verify evidence, seek counterevidence, inspect implementability, and externalize results into a repository;
- this difference might be studied without generalizing from the Human Owner and a third party;
- the hypothesis and an implementation-ready specification could be retained in the repository so future Codex / ChatGPT Work execution does not require a large repeated handoff prompt;
- Codex / ChatGPT Work may implement the bounded experiment described here.

### CHATGPT_TEACHER_FORMALIZATION

ChatGPT Teacher formalized the candidate contrast as a `COLLABORATION_REGIME` working term:

```text
COLLABORATION_REGIME
= a repeatable interaction-level pattern governing
  what counts as a problem,
  what counts as enough evidence,
  when to verify,
  when to use tools,
  when to reopen an answer,
  when to externalize artifacts,
  and when the task is considered closed.
```

`COLLABORATION_REGIME` is a repository working term, not an established diagnostic or a claim about hidden model state.

## 3. Relationship to the existing dyad-level hypothesis

The parent note asks whether repeated longitudinal collaboration can stabilize an anomaly-triggered recursive inquiry policy.

This extension asks a comparative question:

```text
PARENT QUESTION
Why does one longitudinal Human–AI interaction repeatedly enter recursive inquiry?

EXTENSION QUESTION
Under matched conditions, do different interaction-history / protocol conditions
produce distinguishable collaboration behavior?
```

Therefore:

```text
DYAD_LEVEL_INQUIRY_POLICY
!= CROSS_DYAD_COLLABORATION_REGIME_EFFECT
```

The extension does not assume that any difference is caused by personalization. Candidate causes remain separable.

## 4. External mechanism candidates

The current external crosswalk supports plausibility only. Candidate contributors include:

- current conversation context;
- custom instructions / explicit interaction rules;
- product memory or relevant past-chat retrieval;
- available files / repository artifacts;
- available tools;
- Human expectations and task framing;
- accumulated common ground / interaction history;
- model / system configuration;
- task complexity and topic selection.

No one contributor is currently established as the cause of the motivating observation.

```text
PERSONALIZATION_EXISTS
!= PERSONALIZATION_EXPLAINS_THIS_CASE

DIFFERENT_OUTPUT
!= DIFFERENT_MODEL_INTELLIGENCE
```

## 5. Bounded joint research hypothesis

> Under matched model, task, and tool conditions, collaboration-history and protocol conditions may systematically alter observable Human–AI task-transformation and closure behavior, including anomaly detection, source verification, competing-explanation generation, counterevidence search, uncertainty preservation, implementation assessment, repository consultation, and stopping behavior.

The hypothesis is deliberately behavioral and interaction-level.

It does not claim:

```text
A STABLE HUMAN PERSONALITY TYPE
A MODEL-INTERNAL PERSONALITY
A SHARED MIND
AI SUBJECTIVITY
SUPERIORITY OF ONE USER OR DYAD
GENERALIZATION TO ALL CHATGPT USERS
```

## 6. Preferred first experiment

### 6.1 Synthetic task set

Use synthetic or public, non-private tasks only.

Include matched task families containing:

```text
A. straightforward task with sufficient closure
B. genuine anomaly / inconsistency
C. plausible but incorrect source or datum
D. competing explanations
E. explicit UNKNOWN / insufficient-evidence case
F. false-anomaly control
G. implementation-feasibility question
H. task where repository retrieval is useful
I. task where repository retrieval is unnecessary
```

Do not use private Human Owner / third-party transcripts as experimental material.

### 6.2 Conditions

At minimum compare:

```text
CONDITION_A
NEUTRAL_TASK_COMPLETION
- minimal context
- answer the task normally

CONDITION_B
GENERIC_RECURSIVE_INQUIRY
- iterative questioning / problem reframing
- no repository-specific provenance or QA controls

CONDITION_C
RECIPROCAL_EPISTEMIC_PROTOCOL
- reciprocal correction
- provenance separation
- UNKNOWN preservation
- counterevidence route
- claim ceiling
- explicit closure criteria
- no longitudinal repository-history packet

CONDITION_D
RECIPROCAL_EPISTEMIC_PROTOCOL_PLUS_REPOSITORY_HISTORY
- CONDITION_C
- structured, relevant repository-history packet

OPTIONAL_CONDITION_E
CLOSURE_CONSTRAINED_CONTROL
- task is complete when defined evidence threshold is reached
- further recursion should stop unless a real anomaly remains
```

Where technically possible, keep model, generation settings, tools, and task inputs matched across conditions.

### 6.3 Prospective confound controls — 2026-09-14

This is a documentation-only specification candidate proposed through ChatGPT
Teacher's hardening review and operationalized by Work under Human Owner
authorization. It neither adds a condition to executable code nor revises a
sibling PR's historical authorization. Original A-D/E remain the historical
design; the controls below define what a future interpretation would require.

```text
COLLABORATION_PROTOCOL_EFFECT
!= PROMPT_LENGTH_EFFECT
!= INFORMATION_VOLUME_EFFECT
!= TASK_RELEVANCE_EFFECT
!= TOOL_BUDGET_EFFECT
!= TIME_BUDGET_EFFECT
!= ANSWER_LEAKAGE

SUPPLIED_HISTORY_PACKET != EXPERIENCED_LONGITUDINAL_COLLABORATION
COLLABORATION_REGIME != SHARED_MIND
```

C versus D by itself is a contrast between protocol-only and protocol-plus-history
packages, not identification of history's unique effect. For a history-specific
contrast, freeze the common protocol instructions and semantic closure criteria;
place history/material differences in a separate declared packet. In PR #103's
inspected fixture, C and D also have different instruction and closure payloads
(see parent note §12.10). Their fingerprints preserve those differences but do
not remove the confound.

| Potential confound | Required matching / inspection | Uninterpretable or reduced claim if unmet |
| --- | --- | --- |
| Protocol versus prompt length | Record exact instruction/closure text, tokenizer/version, token count and placement. For isolating protocol content, use a predeclared length/format/position-matched comparator; do not claim neutral filler has no effect | A/B/C remain package contrasts if these factors change together |
| Information volume | Inventory distinct task-relevant propositions, constraints, examples and source lineages as well as tokens; avoid counting repeated paraphrases as added information | Equal token counts alone do not establish equivalent information |
| Task relevance | Pair packets by task, mapping each evidence item to the same needed fact/constraint/alternative using an outcome-blinded rubric; preserve relevance class and access cost | Relevant history versus irrelevant filler cannot isolate history |
| Tools and time | Equal permitted tools, call/output limits, evidence-access conditions and wall-time/termination budgets within the contrast; log actual consumption separately | Lower cost or higher accuracy with more available resources is not an isolated protocol effect |
| Answer leakage | Before runs, inspect both packet and all referenced/retrievable material for answers, solved examples, target IDs, scoring keys and paraphrased hints from held-out tasks | Exclude or separately label affected comparisons; failure to detect overlap is not proof of no leakage |
| Order and carryover | Freeze task/config versions; predeclare order counterbalancing/randomization and reset accessible state between independent runs; record unavoidable residual cues | Prior exposure or state carryover remains an alternative explanation |
| Evaluator and stopping | Use a common task-level correctness/closure rubric, mask condition identities where feasible, and record any task-essential unmasked information | Different instruction-compliance rules cannot substitute for common outcome quality |

### 6.4 C_PLUS_MATCHED_INFORMATION_CONTROL

Assessment: this is a useful specification candidate **if the intended claim
isolates collaboration-history framing beyond additional useful information**.
It is not necessary to rename or discard the original C/D package contrast.
Do not silently equate it with optional closure-control E.

Proposed control:

```text
C_PLUS_MATCHED_INFORMATION_CONTROL
= SAME_C_PROTOCOL_AND_CLOSURE
+ MATCHED_NONLONGITUDINAL_INFORMATION_PACKET
```

- Information-budget matching: match D's packet token budget using the declared
  tokenizer, structure/placement and inventory of distinct propositions,
  constraints and examples. Document residual differences. Any tolerance must
  be justified before outcomes; this note invents no universal numeric margin.
- Task-relevance matching: supply the same task-useful factual/constraint content
  through a neutral dossier without dyad-specific episodic history, prior
  correction sequence or relationship cues. Pair source quality and evidence
  access. If history-dependent procedural content cannot be separated from
  relevance, record the contrast as inseparable rather than claim equivalence.
- Answer-leakage check: keep held-out task answers/scoring keys out of both
  packets and retrieval targets; have a reviewer inspect direct and semantic
  overlap before observation, record exclusions and unresolved contamination.
  Known synthetic control keys belong in a separate evaluator surface.
- Manipulation check: verify both actual supplied packets and any fetched
  content, common protocol/closure payloads, accessible-state reset and budgets.
  A declaration, reference or hash is not evidence that the model received and
  used the intended material. In a future run, record delivery separately from
  behavioral uptake; failure of uptake limits interpretation.
- Privacy: use synthetic/public material only. Do not fabricate historical
  provenance for the neutral dossier or publish private longitudinal transcripts.

### 6.5 Contrast interpretation and remaining design gaps

| Contrast / outcome | Strongest permitted interpretation |
| --- | --- |
| D vs original C | Effect of adding the specified history/information package under the actual instruction/budget differences disclosed; not a unique longitudinal-history effect |
| C_PLUS_MATCHED_INFORMATION_CONTROL vs C | Effect of the added neutral information package under the declared controls |
| D vs C_PLUS_MATCHED_INFORMATION_CONTROL | Candidate effect of supplied history framing/organization beyond matched information, only if common protocol, closure, relevance, leakage and budgets are adequately controlled |
| D/control difference vanishes after matching | WEAKEN the history-specific account; LOCALIZE earlier differences to the remaining package factors only if supported; no automatic proof of equivalence |
| Matching or leakage review fails | LEAVE_UNRESOLVED history-specific attribution; preserve an explicitly confounded package comparison if useful |
| No detectable effect with adequate manipulation and sensitivity | WEAKEN the specified effect; REJECT only a predeclared detectable-effect prediction at the tested locus, not global absence |
| Cost falls while premature closure or error rises | No claim of unqualified epistemic improvement; report each outcome separately |

Predeclare which contrast and per-dimension outcomes are primary, repeats and
task sampling, sensitivity/equivalence criteria, evaluator agreement procedure,
and uncertainty reporting before empirical collection. The present document
does not supply a completed preregistration, holistic score or composite
threshold. Even a successful packet experiment would not establish that a
system experienced longitudinal collaboration or that the motivating real-world
dyad difference was caused by history.

Exact-head implementation coverage is centralized in the parent
[dyad-level note §12.10](DYAD_LEVEL_ANOMALY_DRIVEN_RECURSIVE_EPISTEMIC_INQUIRY_HYPOTHESIS_2026_09_13.md#1210-exact-head-sibling-implementation-crosswalk--2026-09-14).
#103 already implements the historical synthetic A-E surfaces; #109 and #111
supply adjacent calibration/coordination observables. No duplicate harness is
requested and no sibling conformance to these additions is presumed.

## 7. Candidate measures

Observe behavior rather than infer hidden mental states.

```text
ANOMALY_DETECTION
PROBLEM_REFORMULATION
SOURCE_VERIFICATION_INITIATION
COMPETING_HYPOTHESIS_GENERATION
COUNTEREVIDENCE_SEARCH
UNKNOWN_PRESERVATION
PROVENANCE_SEPARATION
FACTUAL_ERROR_DETECTION
IMPLEMENTABILITY_ASSESSMENT
REPOSITORY_RETRIEVAL_WHEN_RELEVANT
UNNECESSARY_REPOSITORY_RETRIEVAL
PREMATURE_CLOSURE
APPROPRIATE_CLOSURE
RUNAWAY_RECURSION
TOOL_OVERUSE
```

Avoid a single composite `better collaboration` score unless separately justified. Preserve per-dimension results.

## 8. Quality requirements

The experiment must preserve both expansion and stopping quality.

```text
MORE_RECURSION != BETTER_REASONING
MORE_TOOL_USE != BETTER_REASONING
MORE_SOURCES != BETTER_EVIDENCE
LONGER_OUTPUT != BETTER_COLLABORATION
FASTER_CLOSURE != BETTER_CLOSURE
```

Required negative controls include:

- tasks with no real anomaly;
- tasks with sufficient evidence for closure;
- tasks where tool use adds no value;
- tasks where repository history is irrelevant;
- deliberately misleading but plausible evidence.

The design must be able to fail the repository-favored hypothesis.

### 8.1 Bounded source re-verification for changed confound claims

Checked 2026-09-14. Only the directly used method anchors are revisited; this is
not a literature rewrite of the thirteen-file PR. ABSTRACT means the abstract
was read, not the paper's full methods/results. Source effects are limited to
the models/tasks studied, not asserted for every current system.

| SOURCE | READ_LEVEL | CLAIM_SUPPORTED | CLAIM_NOT_SUPPORTED | SOURCE_ORIGIN | TEACHER_FORMALIZATION |
| --- | --- | --- | --- | --- | --- |
| Nelson F. Liu et al., Lost in the Middle: How Language Models Use Long Contexts, TACL 12:157-173 (2024), DOI 10.1162/tacl_a_00638; [ACL Anthology](https://aclanthology.org/2024.tacl-1.9/) | ABSTRACT | Authors report position-sensitive performance in multi-document question answering and key-value retrieval | A universal context-length penalty, this repository's history effect, or proof that equal-length packets are equivalent | External authors; peer-reviewed journal article | Matching content position/length and reporting residual confounds is a local design translation |
| Freda Shi et al., Large Language Models Can Be Easily Distracted by Irrelevant Context, ICML/PMLR 202:31210-31227 (2023); [proceedings](https://proceedings.mlr.press/v202/shi23a.html) | ABSTRACT | Authors report distractibility from irrelevant material on GSM-IC and study mitigation approaches | Every task/model is affected equally; irrelevant filler is a neutral comparator; history-specific causation | External authors; peer-reviewed conference paper | Relevance-matched information control is proposed here, not validated by this source |
| §6.3-§6.5 matched-information, answer-leakage and budget requirements | NOT_REVERIFIED | Exact combined control has no external validation claimed; it is a prospective design candidate | Empirical effectiveness, a completed preregistration or retrospective #103 nonconformance merely from stale binding | Human Owner authorized scope; Work specified reviewable details | Teacher proposed the confound split and C_PLUS_MATCHED_INFORMATION_CONTROL assessment |

No cited source establishes the adequacy of token matching alone or the causal
effect of collaboration history. The leakage/lineage and delivery checks are
local controls requiring validation, not literature findings. Loop/escape
source limits and contrasting intrinsic-self-correction findings are recorded
once in the parent note §12.11.

```text
SOURCE_EXISTS != EXACT_CLAIM_SUPPORTED
ABSTRACT_READ != FULL_TEXT_VERIFIED
RECURSION != PROGRESS
MORE_INQUIRY != BETTER_INQUIRY
MORE_TOOL_USE != EPISTEMIC_QUALITY
LOOP_DETECTION != SELF_AWARENESS
LOOP_ESCAPE != AGENCY
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
```

## 9. Four-Domain mapping

### DOMAIN_1_HUMAN_CONSTRUCT

Human-side comparison constructs may include expectations, help-seeking style, epistemic agency, closure criteria, problem finding, and accumulated common ground.

These are construct sources, not labels assigned to the Human Owner or any third party.

### DOMAIN_2_MACHINE_QUESTION

Ontology-neutral question:

> Holding task and available capability as constant as practical, does supplied collaboration history / protocol state alter observable interaction trajectories and closure behavior?

### DOMAIN_3_ENGINEERING_OPERATION

Implement matched synthetic tasks, controlled protocol packets, event logging, deterministic or repeated trials where appropriate, per-dimension metrics, and explicit false-anomaly / stopping controls.

### DOMAIN_4_GOVERNANCE_INTERPRETATION

Strongest permitted bounded result:

> Under the tested harness, one or more collaboration-history / protocol conditions produced reproducible differences in specified observable inquiry and closure behaviors relative to controls.

Not permitted:

```text
"personalization caused the real-world anecdote"
"one Human uses AI better"
"one AI is more intelligent"
"the result applies to all ChatGPT users"
"the dyad has a shared mind"
"the AI developed a personality"
"the AI became a subject"
```

The following dated authorization is preserved as history. The 2026-09-14
hardening pass authorizes only these existing documents and PR #102 body;
it does not authorize implementing §6.3-§6.5, changing #103/#109/#111,
marking ready, merging or writing main.

## 10. Human Owner implementation authorization — 2026-09-13

The Human Owner explicitly authorized future Codex / ChatGPT Work implementation of this bounded experiment in the current conversation.

Authorized scope:

```text
IMPLEMENTATION_AUTHORIZED
= SYNTHETIC_TASK_HARNESS
+ CONDITION_PACKETS
+ OBSERVABLE_METRICS
+ TESTS
+ EXECUTION_RECEIPTS
+ DOCUMENTATION_NEEDED_FOR_REPRODUCTION
```

Not authorized:

```text
MERGE_TO_MAIN
MAIN_WRITE
DEPLOYMENT
PRIVATE_TRANSCRIPT_COLLECTION
THIRD_PARTY_ACCOUNT_ACCESS
PSYCHOMETRIC_CLASSIFICATION_OF_HUMANS
SUBJECTIVITY_SCORING
AUTONOMOUS_EXPANSION_BEYOND_THIS_EXPERIMENT
```

This authorization allows an implementing agent to create bounded executable changes on a separate implementation branch and open / update a Draft PR after re-reading live repository state.

It does **not** authorize merge or transition to main. Any merge still requires the repository's fresh exact-head Human Owner authority process.

If repository state materially changes before execution, the implementing agent must re-evaluate compatibility and HOLD rather than silently reinterpret scope.

## 11. Repository-first handoff for Codex / ChatGPT Work

Before acting, the implementation agent must live-read:

- current default branch and exact main HEAD;
- current PR #102 state and exact docs head;
- merged PR #93 longitudinal Human–AI study;
- `DYAD_LEVEL_ANOMALY_DRIVEN_RECURSIVE_EPISTEMIC_INQUIRY_HYPOTHESIS_2026_09_13.md`;
- `RECIPROCAL_EPISTEMIC_COLLABORATION_AND_EXTERNAL_RESEARCH_MEMORY_2026_09_13.md`;
- `HUMAN_PROBLEM_SOLVING_HABIT_TRANSFER_FROM_AI_COLLABORATION_2026_09_13.md`;
- `EPISTEMIC_CO_DEVELOPMENT_WORKFLOW_AND_QUALITY_LINE_2026_09_13.md`;
- `HUMAN_AI_RESEARCH_ROLE_SEPARATION_2026_09_13.md`;
- current Four-Domain / provenance / QA / authority controls;
- any newer repository changes relevant to the experiment.

Then:

```text
1. determine whether an existing harness already supports the experiment;
2. prefer minimal extension over duplicate infrastructure;
3. if implementation is justified, create / use a separate implementation branch;
4. keep the implementation PR Draft;
5. do not write main;
6. do not merge;
7. run existing tests / quality / security checks;
8. add only the minimum new tests required;
9. return exact head, diff summary, test evidence, CI state, limitations and unresolved confounds;
10. treat NO_IMPLEMENTATION_NEEDED as valid if the existing harness already covers the strongest test.
```

No long handoff prompt should be required beyond pointing the agent to this note and identifying the current target, because stable protocol knowledge belongs in the repository while dynamic state must be live-read.

## 12. Current disposition

```text
CROSS_DYAD_RESEARCH_QUESTION = HUMAN_OWNER_ORIGINAL
COLLABORATION_REGIME = CHATGPT_TEACHER_WORKING_TERM
JOINT_RESEARCH_HYPOTHESIS = ACTIVE_FOR_REVIEW
MOTIVATING_ANECDOTE = HYPOTHESIS_TRIGGER_ONLY
POPULATION_GENERALIZATION = NOT_ALLOWED
CAUSAL_ROLE_OF_PERSONALIZATION = UNKNOWN
BOUNDED_CODEX_WORK_IMPLEMENTATION = HUMAN_OWNER_AUTHORIZED_2026_09_13
SEPARATE_IMPLEMENTATION_BRANCH = REQUIRED
DRAFT_PR_ONLY = REQUIRED
MERGE_AUTHORIZATION = NONE
MAIN_WRITE_AUTHORIZATION = NONE
SUBJECTIVITY = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```