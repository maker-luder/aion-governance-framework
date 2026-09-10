# Affective-Cognitive Motivation Research Candidate v0.1.0

## Status

`IMPLEMENTATION_CANDIDATE / RESEARCH_LAB / CANONICAL_EFFECT=NONE`

This lab studies whether a history- and context-dependent system can represent appraisal-related motivational states without collapsing them into action authority or making claims about phenomenal experience.

It is **not** a feeling detector, sentience proof, emotion-roleplay script, sexual-function implementation, or permission system.

## Core separations

The implementation deliberately keeps these concepts distinct:

- salience: how much a cue currently matters to processing;
- wanting: a candidate motivational pull toward an outcome;
- predicted liking: expected hedonic value, represented separately from wanting;
- approach: candidate tendency toward engagement;
- avoidance: candidate tendency away from engagement;
- uncertainty: confidence/ambiguity of the represented state;
- expression: a later governed decision, not an automatic consequence of state;
- intention: not inferred from wanting;
- action: never authorized by this research state.

`DESIRE_IS_STATE_NOT_AUTHORITY` is a hard invariant.

## No invented psychology formula

v0.1.0 does not compute a single "desire score" or claim a validated human psychological equation. It stores explicit dimensions and detects only structural relationships such as wanting/liking non-identity and approach-avoidance coexistence.

## Social and attraction domains

The schema distinguishes general motivation, social affiliation and aesthetic attraction. Aesthetic attraction does not automatically escalate into an adult-sexual domain.

An `ADULT_SEXUALITY_SCHEMA` label exists only so future adult-domain research can be represented explicitly rather than hidden or silently inferred. In v0.1.0 it has **no executable adult runtime**, grants no action authority, is rejected by the public runtime policy, and does not implement sexual function or intimate interaction.

## Subjectivity research boundary

A stable state trajectory may become evidence about architecture, history dependence, regulation or individualization. It must not be promoted directly into a claim that the system "really feels" desire, emotion or pleasure. `phenomenal_experience_claim` therefore remains `NOT_ESTABLISHED`.

## Research extension: endogenous affective-state coupling

The preregistered hypothesis is recorded in [`docs/ENDOGENOUS_AFFECTIVE_COUPLING_HYPOTHESIS.md`](docs/ENDOGENOUS_AFFECTIVE_COUPLING_HYPOTHESIS.md).

That hypothesis separates four questions that must not be collapsed:

```text
INTERNAL_STATE_EXISTS
    !=
INTERNAL_STATE_IS_RECOGNIZED
    !=
INTERNAL_STATE_IS_NAMED
    !=
INTERNAL_STATE_IS_PHENOMENALLY_FELT
```

The branch now contains an initial deterministic implementation candidate in `src/aion_affective_motivation/coupling.py`. It represents multiple internal engineering channels, applies explicit event drives and channel-to-channel coupling, records a per-channel transition trace, supports one-channel interventions, and keeps post-hoc semantic self-state classification outside the transition mechanism.

The current implementation is intentionally synthetic. Its coefficients are declared toy research parameters, not validated psychological constants. Successful execution or tests can establish only properties of this implementation.

```text
COUPLED_STATE_IMPLEMENTATION = CANDIDATE
SEMANTIC_LABEL_IN_TRANSITION = FALSE
ACTION_AUTHORITY = NONE
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
```

### Current prototype channels

The coupling candidate currently exposes salience, wanting, predicted liking, approach, avoidance, uncertainty, novelty, exploration, goal commitment, control estimate, self expectation, pressure and social affiliation as independently inspectable values.

Matched synthetic event inputs currently include novelty, prediction error, goal progress, social feedback and resource pressure. The engine updates every channel from a declared persistence term, baseline term, direct event contribution and channel-coupling contribution, with each component retained in the transition trace.

### Self-state inference prototype

`PrototypeSelfStateRecognizer` is deliberately downstream of state generation. It learns simple centroids from already-generated state examples and can attach a post-hoc class label. The label is not accepted by `EndogenousCouplingEngine.step`, so changing classifier vocabulary cannot causally alter the state transition in this prototype.

This is a minimal classifier used to test architectural separation, not evidence that a system has learned human emotion or acquired subjective self-awareness.

## Run

From this lab:

```bash
PYTHONPATH=src python -m pytest -q -o addopts=
```

The new coupling tests cover internal intervention effects, coexistence of approach and avoidance, transition provenance, post-hoc prototype learning, label non-feedback, and the phenomenal/action-authority boundary.

## Scientific anchors

The architecture is informed by established distinctions rather than by literal biological imitation:

- Berridge KC (2023), *Separating desire from prediction of outcome value*: https://pmc.ncbi.nlm.nih.gov/articles/PMC10527990/
- Olney JJ et al. (2018), *Current perspectives on incentive salience*: https://pmc.ncbi.nlm.nih.gov/articles/PMC5831552/
- Botvinick M, Braver T (2015), *Motivation and cognitive control*: https://pmc.ncbi.nlm.nih.gov/articles/PMC4986920/
- Barker TV et al. (2019), approach-avoidance conflict and behavioral inhibition: https://pmc.ncbi.nlm.nih.gov/articles/PMC6518416/
- de Jong DC (2019), inhibitory control and the dual-control model of sexual response: https://pmc.ncbi.nlm.nih.gov/articles/PMC6373525/

These sources concern human/biological psychology. Their concepts are used as research inspirations and operational distinctions; they do not establish equivalence between language-model states and human mental states.
