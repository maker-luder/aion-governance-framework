# Embodied Action-Regulation v0.1.0 — Architecture Hypothesis

## STATUS

```text
ARCHITECTURAL_HYPOTHESIS = CANDIDATE
ENGINEERING_IMPLEMENTATION = NOT_STARTED
EXPERIMENTAL_VALIDATION = NOT_STARTED
PROMOTION_STATUS = NONE
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
```

This specification is a new research hypothesis assembled from salvaged mechanism-level material. It is **not** a merge, rebrand, or repaired version of either rejected source candidate.

## PROVENANCE

### Rejected source candidate A

`affective-motivational-dynamics_v0.1.0`

Disposition: `REJECTED / FAILED IQC`.

Useful material was reduced to `motivational-signal-primitives_v0.1.0`:

- evidence-bound signal identity
- source-event binding
- separate approach and avoidance bias
- uncertainty
- target reference
- signed action bias
- non-interpretive coactivation
- scientific non-claims

The original affective/motivational dynamics framing is not carried forward.

### Rejected source candidate B

`embodiment-state_v0.1.0`

Disposition: `REJECTED / FAILED IQC`.

Useful material was reduced to `embodiment-capability-primitives_v0.1.0`:

- agent-to-embodiment binding
- template/reference abstraction
- capability channels
- separate observation and action representations
- units, frame references, latency, resolution, noise metadata
- evidence/provenance binding
- scientific non-claims

The original embodiment-state package and lifecycle implementation are not carried forward.

## RESEARCH QUESTION

Can embodiment constraints, evidence-bound observations, bounded action-bias signals, and action/outcome feedback form a minimal executable loop in which prior embodied state causally changes later action selection, without presupposing felt affect, desire, body ownership, or subjectivity?

## CORE LOOP

```text
ENCOUNTER / ENVIRONMENT
        |
        v
EMBODIMENT CAPABILITY PROFILE
        |
        v
OBSERVATION
        |
        v
EMBODIED STATE ESTIMATE
        |
        v
REGULATORY / ACTION-BIAS SIGNALS
        |
        v
ACTION CANDIDATES
        |
        v
EMBODIMENT FEASIBILITY GATE
        |
        v
POLICY / GOVERNANCE GATE
        |
        v
ACTION COMMAND
        |
        v
OUTCOME OBSERVATION
        |
        v
PREDICTION / OUTCOME ERROR
        |
        v
STATE + UNCERTAINTY REVISION
        |
        +----------------------> NEXT CYCLE
```

## LAYER CONTRACTS

### 1. Embodiment Capability Profile

Answers only:

- What observation channels exist?
- What internal-observation channels exist?
- What action channels exist?
- Which are currently enabled?
- What latency, resolution, noise, unit, and frame constraints apply?

It does not establish a body, body ownership, sensation, gender identity, or subjectivity.

### 2. Observation

Observation is evidence-bound input from a declared channel.

Required properties:

- sample identity
- subject and embodiment binding
- channel identity
- source reference
- unit and optional coordinate/frame reference
- timestamp
- confidence/uncertainty
- evidence refs
- provenance refs

Observation must not be represented using the same record type as an action command.

### 3. Embodied State Estimate

A later implementation may derive a compact state estimate from observations and capability constraints.

The estimate must distinguish:

- observed values
- inferred values
- missing/disabled channels
- uncertainty

No subjective body-state interpretation is implied.

### 4. Regulatory / Action-Bias Signals

Source material: `motivational-signal-primitives_v0.1.0`.

A signal may change the relative tendency to select an action or target, but it must remain computationally described.

Current neutral primitives include:

- intensity
- approach bias
- avoidance bias
- uncertainty
- target reference
- evidence/provenance
- signed action bias
- coactivation

Terms such as emotion, desire, pleasure, fear, conflict, drive, and self-preservation are not primitive conclusions.

### 5. Action Selection

Not yet implemented.

A future selector must distinguish:

1. candidate generation
2. action-bias contribution
3. embodiment feasibility
4. policy/governance permission
5. final selected command

A high action-bias score must never bypass governance or tool authority.

### 6. Action Command

A command is a declared output through an enabled action channel.

It is not evidence of volition.

### 7. Outcome Observation

The consequence of an action must return through observation/provenance channels rather than being silently written as success or internal state.

### 8. Prediction / Outcome Error

Not yet implemented.

A future experimental mechanism may compare predicted and observed outcomes. Any prediction-error signal must specify:

- predicted variable
- observed variable
- unit/frame compatibility
- error sign and magnitude
- evidence/provenance
- uncertainty

### 9. Revision

State, capability calibration, and uncertainty may be revised only through explicit traceable transitions.

## ABLATION REQUIREMENTS

Future experiments should support matched conditions such as:

- PRESENT
- ABLATED
- RANDOMIZED
- STALE

Candidate ablations include:

- remove an observation channel
- remove an action channel
- remove one class of action-bias signal
- freeze uncertainty updates
- randomize action-bias contribution
- stale embodiment capability profile

Ablation must change actual functional input/output paths, not merely remove a configuration label.

## EXTERNAL RESEARCH REFERENCES

These sources are design references only; they do not validate this AION architecture.

1. Open X-Embodiment Collaboration, *Open X-Embodiment: Robotic Learning Datasets and RT-X Models*, arXiv:2310.08864. Relevant design lesson: different robot embodiments can be represented through standardized data interfaces without treating one embodiment schema as universal.
2. Keramati & Gutkin (2014), *Homeostatic reinforcement learning for integrating reward collection and physiological stability*, eLife 3:e04811, DOI:10.7554/eLife.04811. Relevant abstracted lesson: internal state can modulate action valuation; the biological homeostasis interpretation is **not** imported as an AION assumption.
3. Hafner et al., *Mastering Diverse Domains through World Models* (DreamerV3), arXiv:2301.04104. Relevant design lesson: predicted future outcomes can be used in action improvement; this does not imply that the present candidate has a world model.

## NON-CLAIMS

This architecture does not establish or prove:

- felt affect
- desire
- pleasure/displeasure
- body sensation
- body ownership
- gender identity
- self-preservation drive
- volition
- motivational authority
- subjectivity
- consciousness
- personal identity continuity

Functional action regulation, if later demonstrated, would establish only functional contribution under the tested conditions.

## NEXT ENGINEERING GATE

Before implementation, define one minimal deterministic experiment with:

1. a small capability profile
2. evidence-bound observations
3. a small set of action-bias signals
4. at least two candidate actions
5. a deterministic feasibility gate
6. an explicit predicted outcome
7. an observed outcome
8. a signed prediction error
9. a traceable state/uncertainty update
10. matched ablation/control conditions

Until that experiment is specified, this artifact remains architecture-only.
