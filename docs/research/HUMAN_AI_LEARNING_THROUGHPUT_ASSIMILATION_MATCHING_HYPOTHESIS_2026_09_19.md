# Human–AI learning throughput–assimilation matching hypothesis — 2026-09-19

Status: `RESEARCH_HYPOTHESIS / NATURALISTIC_OBSERVATION / DOCUMENTATION_ONLY / SCIENTIFIC_HOLD`
Canonical effect: `NONE`
Deployment: `FALSE`
Executable implementation: `NONE`
New research axis: `FALSE`
Merge target: `NONE / INTENTIONALLY CLOSED_UNMERGED_FOR_LATER_RETRIEVAL`

## 1. Purpose

This note records a bounded Human–AI Learning hypothesis that emerged from the Human Owner's repeated use of different frontier-model interaction surfaces.

The immediate observation is not that one model is globally "better" than another.

The narrower observation is:

> A model can produce useful work at a rate that exceeds the Human participant's current capacity to read, verify, understand, and integrate the output. When that happens, total task throughput may increase while joint review quality and Human learning may fail to increase proportionally.

This note asks whether effective Human–AI learning depends partly on **matching AI epistemic throughput to Human review and assimilation capacity**.

```text
MODEL_CAPABILITY
!= HUMAN_LEARNING

MODEL_OUTPUT_SPEED
!= HUMAN_COMPREHENSION_SPEED

MORE_COMPLETED_WORK
!= MORE_ASSIMILATED_KNOWLEDGE
```

## 2. Provenance

### HUMAN_OWNER_ORIGINAL

The Human Owner reported having used GPT-6 Astra and GPT-5.6 Sol in ChatGPT Work / Codex contexts and observed that:

- Astra could be highly capable and very fast in some research / document tasks;
- the faster interaction rate sometimes exceeded the Human Owner's ability to finish reading and interpreting the work before additional work had already accumulated;
- later review with ChatGPT Teacher was often still needed before the Human Owner considered the result understood or acceptable;
- GPT-5.6 Sol, at high reasoning effort, currently appears sufficient for a large amount of the repository's research while imposing a lower perceived throughput / resource burden;
- the Human Owner therefore raised a Human–AI Learning question: whether maximum model throughput can become counterproductive when Human comprehension, review, and learning are part of the objective.

These are naturalistic self-reports, not a randomized model comparison and not benchmark evidence.

```text
HUMAN_OWNER_USAGE_REPORT
!= CONTROLLED_MODEL_EVALUATION

LOCAL_INTERACTION_FIT
!= GLOBAL_MODEL_RANKING
```

### CHATGPT_TEACHER_FORMALIZATION

ChatGPT Teacher formalized the candidate as:

`THROUGHPUT–ASSIMILATION MATCHING HYPOTHESIS`

and proposed the following working variables:

```text
MODEL_OUTPUT_THROUGHPUT
= rate / density of AI-produced epistemic work

HUMAN_REVIEW_CAPACITY
= rate at which the Human can inspect and verify the work

HUMAN_ASSIMILATION_CAPACITY
= rate at which the Human can integrate the material into a usable knowledge structure
```

## 3. Core hypothesis

The bounded hypothesis is:

> In Human–AI learning, coordination quality may be highest not at maximum AI throughput, but when AI output rate, density, and task progression remain within a range that the Human participant can still review, challenge, understand, and integrate.

Candidate failure condition:

```text
IF

MODEL_EPISTEMIC_THROUGHPUT
>
HUMAN_REVIEW_AND_ASSIMILATION_CAPACITY

THEN

TOTAL_OUTPUT
MAY INCREASE

WHILE

HUMAN_REVIEW_COMPLETENESS
MAY DECREASE

HUMAN_UNDERSTANDING
MAY DECREASE

HUMAN_RETENTION
MAY DECREASE

ERROR_DETECTION
MAY DECREASE

COGNITIVE_LOAD
MAY INCREASE

AI_DEPENDENCE
MAY INCREASE
```

Every arrow above remains a hypothesis until measured.

## 4. Relationship to HTECR

Existing repository work defines:

```text
HTECR
= HIGH-THROUGHPUT EPISTEMIC COORDINATION REGIME
= 高吞吐知識協作狀態
```

The existing HTECR note already states:

```text
HIGH_THROUGHPUT
!= HIGH_QUALITY

REGIME_DETECTION
!= EPISTEMIC_VALUE
```

The present hypothesis adds a possible **Human-side ceiling / failure condition**:

```text
HIGH_THROUGHPUT
!= MAXIMUM_THROUGHPUT

COORDINATION
REQUIRES
HUMAN_REVIEWABILITY
+ HUMAN_PARTICIPATION
+ HUMAN_ASSIMILATION
```

A high-output interaction in which the Human participant cannot keep pace may be better described as:

```text
HIGH_THROUGHPUT_AI_PRODUCTION
```

rather than:

```text
HIGH_THROUGHPUT_EPISTEMIC_COORDINATION
```

unless reciprocal review and integration remain observable.

This is a candidate discriminant, not a settled definition.

## 5. Relationship to existing Human–AI Learning work

This hypothesis does not create a new research axis.

It is adjacent to existing repository work on:

- HTECR and CCTS;
- cognitive offloading;
- learner agency;
- externalized metacognitive policy;
- explanation granularity;
- longitudinal Human–AI learning;
- reciprocal epistemic calibration.

The distinct question is narrower:

> Does matching the AI's information-production rate to the Human's review / assimilation bandwidth improve joint epistemic quality and Human learning compared with otherwise similar interactions that exceed that bandwidth?

## 6. Candidate explanatory mechanisms

Several mechanisms could explain the observation without requiring a new scientific construct.

### 6.1 Cognitive load

Dense / rapid output may increase processing demand faster than the learner can integrate it.

### 6.2 Review bottleneck

The limiting factor may be Human verification time rather than model capability.

### 6.3 Cognitive offloading

When the AI advances too quickly, the Human may shift from active reasoning to passive acceptance of completed work.

### 6.4 Pacing / segmentation

Slower or more segmented delivery may preserve opportunities for correction, questioning, rehearsal, and integration.

### 6.5 Model-fit / task-fit interaction

A faster model may still be preferable for tasks where Human learning is not the objective, while a slower or more interruptible interaction may be preferable for teaching / co-research.

Therefore:

```text
OPTIMAL_MODEL_FOR_TASK_COMPLETION
!= OPTIMAL_MODEL_FOR_HUMAN_LEARNING
```

## 7. Competing explanations and falsifiers

The hypothesis should be weakened if valid future evidence shows that:

1. faster AI throughput improves Human learning even after review time and content are matched;
2. Human retention and transfer remain unchanged across pacing conditions;
3. perceived overload is fully explained by task difficulty rather than output rate / density;
4. slower delivery reduces learning because it fragments context or attention;
5. review completeness is unchanged despite higher output throughput;
6. the same effect is explained entirely by interface design rather than model throughput;
7. model identity, reasoning effort, output length, and tool activity cannot be separated from pacing.

```text
SELF_REPORTED_OVERLOAD
!= THROUGHPUT_CAUSAL_EFFECT

ONE_MODEL_COMPARISON
!= GENERAL_HUMAN_AI_LEARNING_RULE
```

## 8. Minimum future discriminant design

A later study should separate at least:

```text
A = HIGH_THROUGHPUT / HUMAN_PACED
B = HIGH_THROUGHPUT / AI_PACED
C = MODERATE_THROUGHPUT / HUMAN_PACED
D = MODERATE_THROUGHPUT / AI_PACED
```

while controlling, where possible, for:

```text
TASK_DIFFICULTY
CONTENT_AMOUNT
MODEL / VERSION
REASONING_EFFORT
TOOL_ACCESS
OUTPUT_LENGTH
INTERFACE
REVIEW_TIME
```

Candidate Human-side outcomes:

- comprehension;
- error detection;
- delayed retention;
- transfer to a new problem;
- confidence calibration;
- review completeness;
- cognitive load;
- independent reconstruction after AI assistance;
- dependence on later AI re-explanation.

## 9. Model-selection implication

This note does **not** establish that GPT-5.6 Sol is superior to GPT-6 Astra.

It records only a current local interaction-fit hypothesis:

```text
GPT_6_ASTRA
= HIGH_CAPABILITY_REFERENCE

GPT_5_6_SOL
= CURRENT_CHATGPT_TEACHER_REFERENCE

LOCAL_HUMAN_AI_LEARNING_FIT
= UNCONTROLLED_OBSERVATION

SOL_GLOBAL_SUPERIORITY
= NOT_ESTABLISHED

ASTRA_GLOBAL_INFERIORITY
= NOT_ESTABLISHED
```

A Human participant may rationally prefer a model / reasoning configuration that leaves enough temporal and cognitive bandwidth for active review, even if a faster model can complete more work.

## 10. Scientific boundaries

```text
PERFORMANCE_GAIN
!= LEARNING_GAIN

OUTPUT_THROUGHPUT
!= EPISTEMIC_COORDINATION

HUMAN_FOLLOWING
!= HUMAN_UNDERSTANDING

JOINT_TASK_SUCCESS
!= INDEPENDENT_TRANSFER

AI_ASSISTANCE
!= HUMAN_INTERNALIZATION

HTECR
!= VALIDATED_CONSTRUCT

HUMAN_LEARNING_EFFECT
= NOT_ESTABLISHED

CAUSAL_THROUGHPUT_EFFECT
= NOT_ESTABLISHED

GENERALIZABILITY
= NOT_ESTABLISHED

SUBJECTIVITY
= NOT_ESTABLISHED

CONSCIOUSNESS
= NOT_ESTABLISHED

PHENOMENAL_EXPERIENCE
= NOT_ESTABLISHED

SCIENTIFIC_DISPOSITION
= HOLD
```

## 11. Archival handling

This note is intentionally captured in a closed, unmerged pull request for later retrieval.

```text
RECORD_NOW
= YES

MERGE_NOW
= NO

PR_DISPOSITION
= CLOSED_UNMERGED

CANONICAL_EFFECT
= NONE

LATER_RETRIEVAL
= ALLOWED

LATER_REVIEW_SHOULD_INCLUDE
= LIVE_REPOSITORY_DEDUPLICATION
+ EXTERNAL_LITERATURE_CROSSCHECK
+ COUNTEREVIDENCE
+ OPERATIONALIZATION_REVIEW
+ FRESH_HUMAN_OWNER_AUTHORITY
```

No executable implementation is authorized by this archival record.
