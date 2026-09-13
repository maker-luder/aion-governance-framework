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