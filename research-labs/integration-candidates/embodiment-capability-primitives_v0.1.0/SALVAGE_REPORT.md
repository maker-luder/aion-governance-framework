# SALVAGE REPORT — rejected embodiment-state candidate

## DISPOSITION

- SOURCE_CANDIDATE: `embodiment-state_v0.1.0`
- SOURCE_STATUS: REJECTED / FAILED IQC
- SALVAGE_BRANCH: `review/embodied-action-regulation-salvage`
- ORIGINAL_SOURCE_HISTORY: preserved only for audit/provenance on the isolated Nemotron session branch
- PROMOTION_STATUS: NONE
- MAIN_EFFECT: NONE
- CANONICAL_EFFECT: NONE
- RUNTIME_EFFECT: NONE

## WHY THE ORIGINAL CANDIDATE WAS REJECTED

The candidate mixed capability declaration, observations, internal measurements, and action commands in one data model. Several configured modalities had no corresponding state representation. Modality ablation could remove a configuration label while leaving state data intact, so it did not reliably represent functional ablation. Measurement units, coordinate/frame semantics, source provenance, and signal identity were also underspecified.

The Human Research Owner classified the artifact as failed and authorized material-only salvage rather than rework. The original candidate package was therefore removed from this salvage branch.

## RETAINED MATERIAL

Only the following mechanism-level ideas were retained:

1. Explicit `agent_id` to `embodiment_id` binding.
2. Template/reference abstraction without treating one body schema as universal.
3. Capability-channel declarations with observation, internal-observation, and action roles kept distinct.
4. Per-channel latency, resolution, noise-floor, unit, and optional frame metadata.
5. Evidence and provenance binding for capability declarations and runtime samples/commands.
6. Separate observation samples and action commands.
7. Explicit confidence for observations.
8. Empty capability profiles are valid as control/ablation material.
9. Body ownership, gender identity, phenomenal experience, volition, motivational authority, and subjectivity remain `NOT_ESTABLISHED`.

## REJECTED / NOT CARRIED FORWARD

The salvage deliberately does not carry forward:

- the original `embodiment-state` package identity
- the old `EmbodimentStateManager` lifecycle implementation
- `ProprioceptiveSignal` as a generic container for interoception and motor commands
- configuration-only ablation
- hard-coded modality claims that exceed implemented state support
- the `adult-male-template` demo fixture as a core architecture assumption
- heart rate represented through a joint-position field
- manually simulated movement presented as sensorimotor dynamics
- silent agent/template rebinding
- restore lineage using sentinel source ids
- repeated-initialize semantics that create false roots

## NEW MINIMAL ARTIFACT

`embodiment-capability-primitives_v0.1.0` is intentionally not an embodiment dynamics model. It contains no lifecycle manager, no simulator, no migration logic, and no claim of bodily selfhood.

It provides:

- `CapabilityChannel`
- `EmbodimentCapabilityProfile`
- `ObservationSample`
- `ActionCommand`
- explicit observation/internal-observation/action channel roles
- measurement units, optional frame references, source refs, evidence, and provenance
- non-claim guards

## INDEPENDENT LOCAL VERIFICATION

The new salvage primitives were reconstructed outside the Nemotron session and executed independently.

```text
9 passed in 0.04s
```

Verification scope:

- UNIT_TEST_RESULT: PASS (9/9)
- GITHUB_CI_RESULT: NOT_EXECUTED
- MAIN_EFFECT: NONE
- CANONICAL_EFFECT: NONE
- RUNTIME_EFFECT: NONE

## INTEGRATION DIRECTION

These primitives are intended to serve as source material for the separate `embodied-action-regulation_v0.1.0` architecture hypothesis together with the previously salvaged `motivational-signal-primitives_v0.1.0`.

The relationship is material provenance, not module promotion:

```text
rejected affective-motivational-dynamics
    -> motivational-signal-primitives

rejected embodiment-state
    -> embodiment-capability-primitives

both material sets
    -> embodied-action-regulation architecture hypothesis
```

## SCIENTIFIC NON-CLAIMS

This salvage does not establish embodiment experience, body ownership, gender identity, subjectivity, sensation, volition, desire, or motivational authority. It is a bounded computational representation layer for later experiments only.
