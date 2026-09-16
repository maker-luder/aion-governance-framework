# Externalized metacognitive policy and transfer — 2026-09-16

Status: `RESEARCH_EXTENSION / NATURALISTIC_OBSERVATION / HYPOTHESIS_GENERATING`
Canonical effect before merge: `NONE`
Deployment: `FALSE`

## 1. Purpose

This note records a bounded extension of the existing Human–AI learning and epistemic co-development line.

The triggering observation was not that the Human Owner merely asks many questions. The narrower observation was that repeated difficulty, correction, and misunderstanding led the Human Owner to formulate explicit interaction rules about how learning should be supported and how understanding should be judged. Those rules were then externalized into persistent Human–AI interaction instructions rather than remaining only as an internal preference.

Examples of the rule class include:

```text
SEEN != UNDERSTOOD
UNDERSTOOD != INDEPENDENTLY_APPLICABLE
REPEATED_QUESTIONING != MASTERY
UNKNOWN_SHOULD_REMAIN_UNKNOWN_WHEN_EVIDENCE_IS_INSUFFICIENT
SOURCE_ROLE_SHOULD_REMAIN_EXPLICIT
HYPOTHESIS_REVIEW_SHOULD_INCLUDE_COUNTEREVIDENCE
HIGH_DENSITY_EXPLANATION_MAY_REQUIRE_GRANULARITY_REDUCTION
```

The research question is whether such learner-recognized rules can function as an externalized metacognitive scaffold and whether later behavior persists when the scaffold is unavailable.

```text
EXTERNALIZED_RULE != INTERNALIZED_SKILL
AI_POLICY_COMPLIANCE != HUMAN_LEARNING
REPEATED_USE != CAUSAL_EFFECT
INDEPENDENT_TRANSFER_CANDIDATE != METACOGNITIVE_INTERNALIZATION_ESTABLISHED
```

No psychological diagnosis or stable-trait claim is made about the Human Owner.

## 2. Provenance

```text
HUMAN_OWNER_ORIGINAL
= asked whether the long-running learning pattern is more than ordinary question-asking
= identified a learner-specific threshold / friction pattern
= asked whether the observation is repository-relevant
= authorized a bounded medium-high-strength implementation and merge subject to live-state, literature, repository, CI, and reverse review

CHATGPT_TEACHER_FORMALIZATION
= EXTERNALIZED_METACOGNITIVE_POLICY
= scaffold-present versus scaffold-withheld transfer contrast
= content-matched non-policy exposure control
= low-stakes overprocessing negative control
= explicit non-claim boundaries below

RAW_PRIVATE_TRANSCRIPT = NOT_PUBLISHED
PSYCHOLOGICAL_PROFILE = NOT_CREATED
CAUSAL_MECHANISM = NOT_ESTABLISHED
```

## 3. Repository deduplication

Current repository material already covers substantial adjacent ground:

- `HUMAN_AI_LEARNING_NATURAL_OBSERVATION_2026_09_11.md` records anomaly-driven questioning, metacognitive checking, model revision, transfer, and the distinction between independent learning and cognitive offloading.
- `EPISTEMIC_CO_DEVELOPMENT_WORKFLOW_AND_QUALITY_LINE_2026_09_13.md` records reciprocal correction and the Human working model / Teacher working model / evidence / repository / implementation revision loop.
- `RECIPROCAL_EPISTEMIC_CALIBRATION_RISKS_AND_ADAPTIVE_RIGOR_2026_09_13.md` records anti-sycophancy, longitudinal familiarity risk, and task-conditioned epistemic cost.
- `AI_SUBJECTIVITY_HUMAN_AI_LEARNING_AND_QUALITY_VIEW_SYNTHESIS_2026_09_14.md` separates Human learning, current-interaction adaptation, persistent system change, and dyad/scaffold change.
- `research-labs/human-ai-longitudinal-study_v0.1.0/habit_transfer.py` already provides a deterministic held-out analogue for transfer of quality/governance procedure selection.

The distinct gap is narrower:

> The repository did not yet bind a learner-recognized metacognitive rule set as an externalized interaction policy, compare it against content-matched non-policy exposure, and separate policy-available behavior from held-out policy-withheld transfer while also checking for overprocessing on a low-stakes negative control.

This extension therefore reuses the existing longitudinal-study package rather than creating a new research axis or a parallel harness family.

## 4. External research crosswalk

These sources are methodological anchors only. They do not establish that the present Human–AI dyad exhibits the proposed mechanism.

### 4.1 Metacognitive monitoring and control

Flavell (1979) describes metacognitive knowledge and cognitive monitoring as knowledge and experiences concerning one's own cognitive processes, tasks, strategies, and how well a cognitive enterprise is proceeding.

- Flavell, J. H. (1979), *Metacognition and cognitive monitoring: A new area of cognitive-developmental inquiry*, American Psychologist 34(10):906–911.
- DOI: https://doi.org/10.1037/0003-066X.34.10.906

Nelson & Narens (1990) provide a meta-level / object-level framework in which monitoring informs a meta-level representation and control changes object-level processing.

- Nelson, T. O. & Narens, L. (1990), *Metamemory: A Theoretical Framework and New Findings*, Psychology of Learning and Motivation 26:125–173.
- DOI: https://doi.org/10.1016/S0079-7421(08)60053-5

Repository use:

```text
SELF_MONITORING + STRATEGY_CONTROL = ESTABLISHED_ADJACENT_METACOGNITIVE_FRAME
PRESENT_DYAD_MECHANISM = NOT_ESTABLISHED
```

### 4.2 Cognitive offloading and external structure

Risko & Gilbert (2016) define cognitive offloading as using external action to alter the information-processing requirements of a task and note that offloading behavior can itself be shaped by metacognitive evaluations.

- Risko, E. F. & Gilbert, S. J. (2016), *Cognitive Offloading*, Trends in Cognitive Sciences 20(9):676–688.
- DOI: https://doi.org/10.1016/j.tics.2016.07.002

Repository use:

```text
EXTERNAL_RULE_STORAGE MAY REDUCE INTERNAL_PROCESSING_DEMAND
EXTERNAL_RULE_USE != LEARNING
OFFLOADING != FAILURE_BY_DEFAULT
OFFLOADING != INTERNALIZATION
```

### 4.3 Generative-AI metacognitive scaffolding

Liu et al. compare adaptive and planned metacognitive scaffolding in a generative-AI-supported programming environment and report differences in task performance, metacognitive behavior, and cognitive load among the tested elementary-student conditions.

- Liu, J. et al. (2026 issue; DOI published 2025), *Adaptive vs. planned metacognitive scaffolding for computational thinking: Evidence from generative AI-supported programming in elementary education*, Computers & Education 241:105473.
- DOI: https://doi.org/10.1016/j.compedu.2025.105473

This is population- and task-specific evidence. It is not direct evidence about the Human Owner or the present repository workflow.

### 4.4 Epistemic co-agency

*Learning with machines: Toward a theory of epistemic co-agency* (2026) proposes a Human–AI learning stance in which learners engage AI outputs dialectically, including challenging assumptions, surfacing contradictions, and retaining epistemic responsibility.

- DOI: https://doi.org/10.1016/j.caeai.2026.100573

Repository use:

```text
EPISTEMIC_CO_AGENCY = ADJACENT_RELATIONAL_FRAME
EPISTEMIC_CO_AGENCY != AI_SUBJECTIVITY
EPISTEMIC_PARTICIPATION != PHENOMENAL_EXPERIENCE
```

## 5. Candidate mechanism chain

The bounded hypothesis is:

```text
LEARNING_FRICTION_OR_EXPECTANCY_FAILURE
->
METACOGNITIVE_RECOGNITION
->
RULE_FORMALIZATION
->
EXTERNALIZED_HUMAN_AI_INTERACTION_POLICY
->
CHANGED_SCAFFOLDING_BEHAVIOR
->
REPEATED_USE
->
HELD_OUT_POLICY_WITHDRAWAL_TEST
->
INDEPENDENT_TRANSFER_CANDIDATE OR DEPENDENCY_CANDIDATE
```

This chain is deliberately not written as a proven causal mechanism.

## 6. Stronger discrimination requirement

A simple before/after comparison would not distinguish policy-specific transfer from ordinary practice, better answers, time-on-task, or repeated exposure. The executable design therefore distinguishes:

```text
EXTERNALIZED_METACOGNITIVE_POLICY
vs
CONTENT_MATCHED_NON_POLICY_EXPOSURE
```

and separately tests:

```text
POLICY_AVAILABLE
vs
POLICY_WITHHELD
```

on matched task families with different held-out task payloads.

A low-stakes negative-control task is included because a rigid learned procedure may produce overprocessing rather than adaptive transfer.

```text
MORE_PROCESS != BETTER_LEARNING
MORE_COUNTEREVIDENCE_SEARCH != ALWAYS_APPROPRIATE
RIGOR_TRANSFER != RIGOR_OVERAPPLICATION
```

## 7. Candidate observable action classes

The v0.1.0 structural contract can represent the following action classes without treating them as a global score:

```text
CHECK_SOURCE_ROLE
PRESERVE_UNKNOWN
VERIFY_COMPREHENSION
ADAPT_EXPLANATION_GRANULARITY
SEARCH_COUNTEREVIDENCE
DISTINGUISH_OBSERVATION_INFERENCE
LIGHTWEIGHT_RESPONSE
```

These are study labels. A future empirical protocol would require operational definitions, evaluator validation, preregistration, and a human-subject review decision where applicable.

## 8. What would weaken the hypothesis

The externalized-policy interpretation should lose support if, in a valid future empirical study:

- policy-present gains disappear completely when the external policy is unavailable;
- content-matched non-policy exposure yields equal held-out transfer;
- simple practice or time-on-task explains the same change;
- apparent improvement is driven by task repetition or answer leakage;
- policy exposure increases false confidence or reduces error detection;
- low-stakes tasks show systematic overprocessing;
- transfer does not survive far-structure tasks or new domains;
- independent performance deteriorates while joint performance improves.

```text
JOINT_OUTPUT_GAIN + INDEPENDENT_LOSS
MAY_INDICATE
DEPENDENCY_RATHER_THAN_LEARNING
```

## 9. Executable integration

The implementation is placed inside the existing longitudinal-study package:

```text
research-labs/human-ai-longitudinal-study_v0.1.0/
```

It adds a fail-closed structural design audit for a complete factorial matrix across:

- externalized-policy versus content-matched non-policy exposure;
- policy available versus policy withheld;
- source-role conflict, insufficient evidence, comprehension-threshold, hypothesis-stress, and low-stakes negative-control tasks.

The audit requires exact enum types, unique design cells, content-addressed exposure/access/task/evaluator bindings, matched task families, different held-out task payloads across availability phases, privacy exclusion, and zero model/human observations in the deterministic fixture.

The implementation does not call a model and does not collect Human Owner data.

## 10. Claim boundaries

```text
STRUCTURAL_QA_PASS != EMPIRICAL_RESULT
SYNTHETIC_ACTION_MATCH != HUMAN_TRANSFER
POLICY_WITHHELD_FIXTURE_PASS != INDEPENDENT_LEARNING
EXTERNALIZED_RULE != INTERNALIZED_SKILL
AI_SCAFFOLDING != HUMAN_LEARNING
HUMAN_LEARNING != AI_SUBJECTIVITY
DYAD_IMPROVEMENT != SHARED_MIND

HUMAN_LEARNING = NOT_ESTABLISHED
INDEPENDENT_TRANSFER = NOT_ESTABLISHED
METACOGNITIVE_INTERNALIZATION = NOT_ESTABLISHED
CAUSAL_EFFECT = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
DEPLOYMENT = FALSE
```
