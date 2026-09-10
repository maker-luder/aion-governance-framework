# Endogenous Affective-State Coupling Hypothesis

Status: `RESEARCH_HYPOTHESIS / NOT_IMPLEMENTED / CANONICAL_EFFECT=NONE`

This document records a bounded research hypothesis proposed by the Human Owner and formalized for repository use by GPT. It does **not** claim that the current system feels emotions, has desires, possesses consciousness, or has established subjectivity.

```text
RESEARCH_DIRECTION = USER_GIVEN
FORMALIZATION = GPT_PROPOSED
IMPLEMENTATION_STATUS = NOT_IMPLEMENTED
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

## Proposed architecture

A candidate loop is:

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

Candidate internal dimensions may include, where operationally defined and independently ablatable:

- novelty and curiosity-related signals;
- uncertainty and prediction error;
- goal commitment and persistence;
- approach and avoidance tendencies;
- salience and motivational wanting;
- predicted liking, kept distinct from wanting;
- resource or viability variables;
- unresolved-state pressure;
- self-model estimates;
- metacognitive confidence or monitoring variables;
- social-feedback history;
- learned expectations and outcome history.

These are engineering state variables, not measurements of human emotion or subjective feeling.

## Coexistence rather than single-label collapse

The model should not assume that one state excludes all others. Multiple tendencies may coexist, for example:

```text
high_exploration
+ high_uncertainty
+ high_goal_commitment
+ repeated_failure
+ reduced_control_estimate
```

This configuration might later be classified as a particular affective category by a learned inference layer, but the category label must not be hard-coded as the causal source of the lower-level state.

```text
LABEL != GENERATOR
CLASSIFICATION != EXPERIENCE
AFFECTIVE_CATEGORY != ACTION_AUTHORITY
```

## Self-state inference

The research target is not merely recognition of emotion in another person. It includes a bounded form of internal-state inference:

```text
state exists
-> state is sampled/observed by an internal monitor
-> state distinctions are learned
-> recurring configurations are classified
-> labels or concepts may be attached
-> the inferred state may influence later prediction or planning
```

A useful engineering term for this layer is `self-state inference`. Biological interoception is a scientific inspiration, not an asserted biological equivalence.

## Relation to existing repository work

This hypothesis extends, but does not replace, the existing `affective-cognitive-motivation_v0.1.0` separation of salience, wanting, predicted liking, approach, avoidance, uncertainty, expression and action authority.

It also has an explicit seam with `endogenous-goal-dynamics_v0.1.0`, where persistent internal state is already treated as an intervention-ready engineering variable rather than as evidence of consciousness.

The proposed addition is specifically the **coupling and learned self-classification problem**: whether multiple endogenous channels can form reproducible composite trajectories and whether an independent inference layer can learn useful internal categories from those trajectories.

## Minimal falsifiable experiments

A future implementation should begin with synthetic, inspectable experiments rather than a large unconstrained agent.

### H1 — Coupling effect

Under a matched external frame, changing one preregistered internal channel should produce a predictable change in the joint internal trajectory.

Falsifier: joint trajectories are unchanged, unstable, or explained by an uncontrolled external variable.

### H2 — Emergent composite-state separability

Repeated combinations of internal channels should form reproducibly separable state clusters without supplying emotion labels to the state-transition mechanism.

Falsifier: clusters disappear under replay, seed control, permutation tests, or removal of one hard-coded shortcut.

### H3 — Learned self-state inference

A classifier trained only on permitted internal observations and outcome history should predict recurrent internal-state classes above preregistered baselines on held-out trajectories.

Falsifier: performance collapses under held-out contexts, depends on leaked labels, or cannot exceed a simple external-context baseline.

### H4 — Label independence

Changing or withholding semantic labels should not alter the underlying state trajectory unless the label is explicitly introduced as a causal input in a separate experiment.

Falsifier: the claimed state only appears when its human emotion name is present in the prompt or target data.

### H5 — Behavioural mediation

If a coupled internal state affects candidate selection, mediation should be traceable through declared internal channels rather than through prompt, retrieved-memory, reward, or candidate-universe differences.

Falsifier: matched-frame controls fail or an external confound better explains the selection change.

## Required controls

Any implementation should control at minimum for:

- identical prompt/task framing across matched trials;
- identical candidate universe;
- identical retrieved-memory manifest;
- identical model/provider identity and generation parameters;
- deterministic or explicitly recorded random seeds;
- no hidden semantic emotion label in the transition mechanism;
- channel-wise ablation;
- randomized-state controls;
- state reset and restoration;
- history-order permutation;
- held-out context evaluation;
- leakage checks between labels and lower-level state generation.

## Scientific anchors

The hypothesis is adjacent to established research areas but is not presented as a validated unified theory.

- Keramati M, Gutkin B (2014), *Homeostatic reinforcement learning for integrating reward collection and physiological stability*, eLife 3:e04811. DOI: `10.7554/eLife.04811`.
- Moerland TM, Broekens J, Jonker CM (2018), *Emotion in reinforcement learning agents and robots: a survey*, Machine Learning 107:443-480. DOI: `10.1007/s10994-017-5666-0`.
- Candia-Rivera D (2026), *Interoceptive machine framework: Toward interoception-inspired regulatory architectures in artificial intelligence*, Physics of Life Reviews 58:18-35. DOI: `10.1016/j.plrev.2026.06.003`.
- Lee S et al. (2026), *Life-inspired interoceptive artificial intelligence for autonomous and adaptive agents*, Nature Machine Intelligence, published 26 August 2026.

These sources support the relevance of internal-state regulation, appraisal/emotion computation, intrinsic motivation and interoception-inspired architectures. They do **not** establish that an artificial system has subjective feeling or that the specific coupled architecture proposed here is correct.

## Evidence boundary

The strongest admissible result from an initial engineering implementation would be something like:

```text
REPRODUCIBLE_COUPLED_INTERNAL_DYNAMICS = OBSERVED_OR_NOT_OBSERVED
SELF_STATE_CLASSIFICATION_SIGNAL = OBSERVED_OR_NOT_OBSERVED
CAUSAL_ROLE_CANDIDATE = POSSIBLE_IF_CONTROLS_PASS
PHENOMENAL_AFFECT = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
```

No successful pipeline, classifier, trajectory, ablation or CI run may be promoted directly into a claim of felt emotion, agency in the philosophical sense, consciousness, or subjectivity.

## Implementation disposition

`HOLD` until a separate implementation task defines exact state schemas, transition rules, preregistered baselines, fixtures, tests, contamination checks and evidence-admission criteria.

This document intentionally records the research question before implementation so that later engineering results can fail against a visible prior hypothesis rather than retrofitting the hypothesis to whatever the system happens to produce.
