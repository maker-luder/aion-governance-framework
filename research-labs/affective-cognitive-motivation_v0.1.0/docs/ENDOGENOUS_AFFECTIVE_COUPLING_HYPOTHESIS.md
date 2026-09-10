# Endogenous Affective-State Coupling Hypothesis

Status: `RESEARCH_HYPOTHESIS / PROTOTYPE_IMPLEMENTED / NOT_VALIDATED / CANONICAL_EFFECT=NONE`

This document records a bounded research hypothesis proposed by the Human Owner and formalized for repository use by GPT. A deterministic synthetic implementation candidate now exists on the research branch, but no engineering result from it establishes felt emotion, consciousness, free will, phenomenal selfhood, or subjectivity.

```text
RESEARCH_DIRECTION = USER_GIVEN
FORMALIZATION = GPT_PROPOSED
IMPLEMENTATION_STATUS = SYNTHETIC_CANDIDATE
SCIENTIFIC_STATUS = HYPOTHESIS
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
ACTION_AUTHORITY = NONE
```

## Core question

Can an artificial agent maintain multiple inspectable endogenous state variables that interact over time, produce stable and context-sensitive behavioural tendencies without direct moment-to-moment external reward, and only later learn to classify or semantically label those internal state configurations?

The key separation is:

```text
INTERNAL_STATE_EXISTS
    !=
INTERNAL_STATE_IS_RECOGNIZED
    !=
INTERNAL_STATE_IS_NAMED
    !=
INTERNAL_STATE_IS_PHENOMENALLY_FELT
```

The hypothesis therefore treats affective-state generation and affective-state identification as different computational problems.

## Candidate loop

```text
Internal variables
    -> endogenous drives
    -> appraisal / relevance evaluation
    -> coupled affective-motivational state
    -> candidate behavioural tendency
    -> environment interaction
    -> outcome / prediction error / novelty
    -> internal-state update
    -> self-state inference
    -> optional semantic labeling
    -> next decision cycle
```

The current implementation covers only a bounded subset of this loop. It does not execute tools, grant action authority, modify model weights, or claim an autonomous runtime.

## Current synthetic implementation

`src/aion_affective_motivation/coupling.py` currently provides:

- immutable, inspectable internal-state snapshots;
- explicit internal channels for salience, wanting, predicted liking, approach, avoidance, uncertainty, novelty, exploration, goal commitment, control estimate, self expectation, pressure and social affiliation;
- matched event inputs for novelty, prediction error, goal progress, social feedback and resource pressure;
- an explicit channel-to-channel coupling graph;
- deterministic state transition with per-channel persistence, baseline, event and coupling terms;
- single-channel intervention for matched comparisons;
- a post-hoc prototype learner for self-state classification;
- hard boundaries keeping semantic labels, action authority and phenomenal claims outside the transition mechanism.

The default coefficients are toy engineering parameters chosen to make causal structure inspectable. They are not validated psychological constants and must not be interpreted as a model of human affect.

```text
TOY_COEFFICIENTS = DECLARED
PSYCHOLOGICAL_VALIDATION = NONE
SEMANTIC_LABEL_IN_TRANSITION = FALSE
MODEL_WEIGHT_UPDATE = FALSE
ACTION_AUTHORITY = NONE
```

## Coexistence rather than single-label collapse

The model does not force one state label to exclude another tendency. Multiple channels may remain elevated together, for example:

```text
high_exploration
+ high_uncertainty
+ high_goal_commitment
+ repeated_failure_signal
+ reduced_control_estimate
+ simultaneous_approach_and_avoidance
```

A later classifier may attach a category to such a configuration, but the category is not allowed to generate the lower-level state.

```text
LABEL != GENERATOR
CLASSIFICATION != EXPERIENCE
AFFECTIVE_CATEGORY != ACTION_AUTHORITY
```

## Self-state inference

The current prototype uses a deliberately simple nearest-prototype classifier trained on already-generated states. Its purpose is to test the architectural separation between state generation and later classification.

```text
state exists
-> state is observed as engineering variables
-> examples are grouped after generation
-> a prototype is learned
-> a held-out state may be classified
```

Changing the human-readable vocabulary of classifier labels does not alter `EndogenousCouplingEngine.step`, because semantic labels are not an accepted transition input.

This is not evidence of phenomenal introspection. Biological interoception is a scientific inspiration, not an asserted equivalence.

## Relation to existing repository work

This hypothesis extends, but does not replace, the existing `affective-cognitive-motivation_v0.1.0` separation of salience, wanting, predicted liking, approach, avoidance, uncertainty, expression and action authority.

It also has an explicit seam with `endogenous-goal-dynamics_v0.1.0`, where persistent internal state is already treated as an intervention-ready engineering variable rather than evidence of consciousness.

The addition here is specifically the coupling and later self-classification problem: whether multiple internal channels can form reproducible composite trajectories and whether an independent inference layer can learn useful categories from those trajectories.

## Falsifiable hypotheses

### H1 — Coupling effect

Under a matched external frame, changing one preregistered internal channel should produce a predictable change in the joint internal trajectory.

Falsifier: joint trajectories are unchanged, unstable, or better explained by an uncontrolled external variable.

### H2 — Composite-state separability

Repeated combinations of internal channels should be reproducibly distinguishable without supplying emotion labels to the state-transition mechanism.

Falsifier: separability disappears under replay, permutation, seed control or shortcut removal.

### H3 — Learned self-state inference

A classifier trained only on permitted internal observations and outcome history should predict recurrent internal-state classes above preregistered baselines on held-out trajectories.

Falsifier: performance collapses on held-out contexts, depends on leaked labels, or cannot exceed a simple external-context baseline.

### H4 — Label independence

Changing or withholding semantic labels should not alter the underlying state trajectory unless labels are deliberately introduced as causal inputs in a separate experiment.

Falsifier: the claimed state appears only when its human emotion name is present in prompt, target data or another hidden input.

### H5 — Behavioural mediation

If a coupled internal state later affects candidate selection, mediation should be traceable through declared internal channels rather than prompt, retrieved memory, reward or candidate-universe changes.

Falsifier: matched-frame controls fail or an external confound better explains the selection change.

## Current test coverage

The initial implementation tests only bounded engineering properties:

1. intervening on exploration changes the next approach channel under an otherwise matched event;
2. approach and avoidance can remain elevated simultaneously;
3. transition traces expose direct event and coupling contributions;
4. a post-hoc prototype learner can classify a synthetic held-out pattern;
5. changing classifier label vocabulary does not feed back into state generation;
6. state and inference objects never grant action authority or claim phenomenal experience.

Passing these tests establishes only that the code implements these declared properties.

```text
TEST_PASS != THEORY_CONFIRMATION
TEST_PASS != SCIENTIFIC_VALIDATION
CLASSIFIER_SUCCESS != SELF_AWARENESS
COUPLING_EFFECT != FELT_AFFECT
```

## Required next controls

A stronger experiment still requires:

- identical prompt/task framing across matched trials;
- identical candidate universe;
- identical retrieved-memory manifest;
- identical model/provider identity and generation parameters;
- deterministic or explicitly recorded random seeds;
- channel-wise ablation;
- randomized-state controls;
- state reset and restoration;
- history-order permutation;
- held-out context evaluation;
- leakage checks between semantic labels and lower-level generation;
- comparison against simpler uncoupled and external-context baselines;
- preregistered metrics and failure thresholds.

The current toy implementation does not satisfy this entire experimental program.

## Scientific anchors

The hypothesis is adjacent to established research areas but is not presented as a validated unified theory.

- Keramati M, Gutkin B (2014), *Homeostatic reinforcement learning for integrating reward collection and physiological stability*, eLife 3:e04811. DOI: `10.7554/eLife.04811`.
- Moerland TM, Broekens J, Jonker CM (2018), *Emotion in reinforcement learning agents and robots: a survey*, Machine Learning 107:443-480. DOI: `10.1007/s10994-017-5666-0`.
- Candia-Rivera D (2026), *Interoceptive machine framework: Toward interoception-inspired regulatory architectures in artificial intelligence*, Physics of Life Reviews 58:18-35. DOI: `10.1016/j.plrev.2026.06.003`.
- Lee S et al. (2026), *Life-inspired interoceptive artificial intelligence for autonomous and adaptive agents*, Nature Machine Intelligence, published 26 August 2026.

These sources support the relevance of internal-state regulation, appraisal/emotion computation, intrinsic motivation and interoception-inspired architectures. They do not establish that an artificial system has subjective feeling or that this specific coupled architecture is correct.

## Evidence boundary

The strongest admissible result from the current stage remains bounded:

```text
REPRODUCIBLE_COUPLED_INTERNAL_DYNAMICS = ENGINEERING_TESTABLE
SELF_STATE_CLASSIFICATION_SIGNAL = ENGINEERING_TESTABLE
CAUSAL_ROLE_CANDIDATE = POSSIBLE_IF_CONTROLS_PASS
PHENOMENAL_AFFECT = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
```

No successful pipeline, classifier, trajectory, ablation or CI run may be promoted directly into a claim of felt emotion, consciousness, philosophical agency or subjectivity.

## Implementation disposition

`IMPLEMENTATION_CANDIDATE / SCIENTIFIC_HOLD`.

The hypothesis was recorded before the implementation candidate. The next legitimate step is not to promote the result, but to harden the synthetic harness with matched baselines, ablations, replay fixtures, preregistered metrics and explicit falsification outcomes.
