# Sensorimotor Embodiment Continuity Research Note

Status: `RESEARCH_MATERIAL`
Main effect: `NONE`
Canonical effect: `NONE`
Runtime effect: `NONE`
Identity continuity conclusion: `NOT_ESTABLISHED`
Body ownership conclusion: `NOT_ESTABLISHED`

## Purpose

This note isolates a measurement gap in the existing Embodiment–Continuity Anchor.

The existing anchor is useful for determining whether stable lineage remains traceable across changes in implementation bindings such as runtime, environment, model, inference backend, hardware, and embodiment identifiers. That result must not be promoted into a stronger claim that a continuous embodied sensorimotor process has been established.

The research question here is narrower:

> Can the project independently measure continuity of a body-state -> action -> environment transition -> observation -> recalibrated body-state loop without reducing that question to memory continuity, lineage continuity, geometry continuity, or identity claims?

## Boundary with existing continuity dimensions

The following dimensions must remain separable:

```text
MEMORY_CONTINUITY != EMBODIED_SENSORIMOTOR_CONTINUITY
LINEAGE_CONTINUITY != EMBODIED_SENSORIMOTOR_CONTINUITY
IMPLEMENTATION_BINDING_CONTINUITY != EMBODIED_SENSORIMOTOR_CONTINUITY
GEOMETRY_CONTINUITY != EMBODIED_SENSORIMOTOR_CONTINUITY
EMBODIED_SENSORIMOTOR_CONTINUITY != IDENTITY_CONTINUITY
EMBODIED_SENSORIMOTOR_CONTINUITY != BODY_OWNERSHIP
```

A PASS on one dimension must not automatically cause a PASS on another.

## Candidate E-axis measurement model

A future research-only evaluator may record transitions with fields such as:

```text
transition_id
body_state_before_ref
action_ref
environment_state_before_ref
environment_state_after_ref
observation_ref
body_state_after_ref
sensor_layout_ref
action_channel_refs
recalibration_ref
provenance_refs
```

The evaluator should not require a specific robot morphology or physical body. It only requires evidence of a traceable closed causal transition in the currently tested embodiment context.

## Minimal continuity predicates

A candidate E-axis assessment should distinguish at least:

```text
ACTION_GROUNDED
ENVIRONMENT_TRANSITION_OBSERVED
OBSERVATION_GROUNDED
BODY_STATE_UPDATE_GROUNDED
SENSORIMOTOR_LINK_TRACEABLE
RECALIBRATION_REQUIRED
RECALIBRATION_EVIDENCE_PRESENT
```

Possible outputs remain bounded:

```text
PASS
HOLD
FAIL
NOT_ASSESSED
```

No E-axis output may establish personal identity, consciousness, phenomenology, body ownership, or canonical subject status.

## Required falsifiers

### F1 — Memory Clone Test

Give two independent embodiment contexts the same memory lineage and equivalent recalled content, then expose them to different action/environment/observation trajectories.

Expected principle:

```text
MEMORY_CONTINUITY = PASS
MAY coexist with
EMBODIED_SENSORIMOTOR_CONTINUITY = DIVERGENT_OR_SEPARATELY_ASSESSED
```

This falsifies any implementation that derives embodied continuity from memory preservation alone.

### F2 — Body Reset / Memory Preserve Test

Preserve lineage and memory while resetting body-state, sensor-state, actuator-state, or embodiment dynamics without a traceable causal bridge.

Expected principle:

```text
LINEAGE_CONTINUITY = PASS
MEMORY_CONTINUITY = PASS
DOES NOT FORCE
EMBODIED_SENSORIMOTOR_CONTINUITY = PASS
```

A valid evaluator should return `HOLD`, `FAIL`, or `NOT_ASSESSED` according to the available transition evidence.

### F3 — Morphology Migration with Causal Bridge Test

Change morphology, sensor layout, action channels, or embodiment implementation while preserving a traceable pre-migration and post-migration action/sensation bridge together with explicit recalibration evidence.

Expected principle:

```text
MORPHOLOGY_CHANGE = TRUE
IMPLEMENTATION_CHANGE = TRUE
MAY coexist with
TRACEABLE_SENSORIMOTOR_CONTINUITY = PASS
```

This falsifies the opposite mistake: treating body sameness as necessary for continuity, or body change as automatic discontinuity.

## Relationship to the existing Embodiment–Continuity Anchor

The existing anchor should continue to answer lineage and implementation-migration questions. This E-axis work is adjacent rather than a replacement.

Recommended interpretation:

```text
L_AXIS = lineage / implementation migration continuity
E_AXIS = embodied sensorimotor causal continuity
```

A future combined report may display both axes, but neither axis should silently derive the other.

## Research-only implementation rule

Any implementation generated from this note must:

1. live under `research-labs/`;
2. keep `main effect = NONE` unless separately approved;
3. preserve `IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED`;
4. avoid body-ownership, consciousness, or phenomenology claims;
5. use synthetic fixtures only;
6. keep provenance explicit;
7. treat absence of causal evidence as `HOLD`, `FAIL`, or `NOT_ASSESSED`, never as inferred continuity.

## Source attribution

- Human Owner approved proceeding with implementation after review of the identified measurement gap.
- ChatGPT identified and formalized the distinction between lineage / implementation migration measurement and embodied sensorimotor causal continuity, then proposed the E-axis falsifier set.
- Codex contribution to this note: `NONE`.

This attribution records contribution to this artifact only and does not establish authorship of broader project concepts.