# Full ↔ Minimal Embodiment Falsification Matrix

Status: `EXPERIMENT DESIGN / DRAFT`  
Canonical effect: `NONE`

## Purpose

Prevent successful-looking embodiment behavior from being overinterpreted.

The richer scientific reference and the minimal runtime model must be compared under matched conditions with explicit competing explanations.

## Core experiment pattern

```text
RICH REFERENCE CONDITION
vs
REDUCED CONDITION

↓ matched task / inputs / policy

ABLATE X
↓
MEASURE

RESTORE X
↓
RE-MEASURE
```

A reduction is not accepted merely because the reduced system runs.

## Primary outcome classes

Candidate measures include:

- action-selection stability;
- movement control;
- perturbation recovery;
- body-state prediction;
- state-dependent decision change;
- energy / recovery behavior;
- adaptation under repeated perturbation;
- transfer to matched novel context;
- replay reproducibility;
- calibration error;
- attachment / reattachment stability.

Outcome definitions must be fixed by each work package.

## Falsification hypotheses

### H_RENAMED_OBSERVABLE

The proposed internal state is only a renamed directly observed feature.

Reject causal/internal interpretation if a direct observable baseline explains the same effect.

### H_REDUNDANT_STATE

A proposed state adds no held-out predictive or causal value beyond existing variables.

### H_NONCAUSAL_PREDICTOR

The state predicts outcomes but intervention / ablation does not produce the predicted directional effect.

### H_MODEL_CONVENTION_CONFUSION

An external model convention is misread as biological anatomy or physiology.

Examples:
- simulator body segment treated as bone;
- pose parameter treated as anatomical joint count;
- actuator treated as complete muscle.

### H_ANATOMICAL_MAPPING_ERROR

Cross-model mapping is incorrect, partial or population-inappropriate.

### H_REFERENCE_RUNTIME_MISMATCH

The rich reference contains features that cannot be meaningfully projected into the runtime comparison, invalidating the claimed full ↔ minimal contrast.

### H_ATTACHMENT_ARTIFACT

Observed behavioral differences arise from the agent-body adapter rather than the body model.

Control:
- same agent;
- same observation/action contract;
- alternate body fidelity.

### H_SESSION_CONTINUITY_CONFUSION

Reattachment success is misinterpreted as identity continuity.

### H_PROVIDER_OR_MODEL_DRIFT

Cloud-agent behavior changes because provider/model/runtime changed rather than body state.

### H_HISTORY_LEAK

Different histories or hidden state contaminate matched conditions.

### H_HUMAN_ONTOLOGY_LEAK

The system appears to discover a body/regulatory concept only because the human-defined label or target was supplied.

### H_POPULATION_OVERGENERALIZATION

A result derived from one or a few reference bodies is reported as though it represented the human population.

Control:
- bind the claim to the actual reference population;
- test alternate body profiles when the claim depends on morphology/physiology;
- keep single-subject anatomy separate from population generalization.

### H_SOURCE_ARTIFACT_OR_SUPPLY_CHAIN

Observed behavior is caused by upstream artifact corruption, unsafe/custom loading behavior, version drift or hidden executable preprocessing rather than the intended scientific representation.

Control:
- exact revision/hash;
- isolated intake;
- deterministic extraction;
- safer/data-only formats where practical;
- no unreviewed remote code execution.

### H_OVERFIT_REFERENCE

The minimal model reproduces only one reference fixture and fails transfer.

### H_IRREVERSIBLE_INTERPRETATION

Counterevidence fails to revise the retained mechanism label or reduction claim.

## Minimal acceptance structure

For a claimed causally relevant body variable X:

| Gate | Required observation |
| --- | --- |
| Baseline | target phenomenon exists under registered condition |
| Intervention | controlled change to X changes outcome directionally |
| Ablation | removing X/pathway degrades target effect |
| Restoration | restoring X/pathway recovers effect |
| Replay | fixed history/seed reproduces expected pattern |
| Transfer | at least one matched novel context preserves role |
| Alternative baseline | simpler observable/redundant explanation is insufficient |
| Provenance | code/data/config/model/seed lineage is bound |

Failure at a required gate returns `HOLD`.

## Full ↔ minimal comparison matrix

A future work package should register comparisons such as:

| Comparison | Question |
| --- | --- |
| rich skeleton vs reduced segments | does reduced kinematics preserve target body-control behavior? |
| rich actuator model vs abstract actuator | does muscle-level detail materially change target outcome? |
| interoception enabled vs ablated | is internal-state observation causally relevant? |
| regulatory reserve vs no reserve | does body state alter matched action selection? |
| damage separate from resource vs merged | is a distinct damage/fatigue state necessary? |
| native vs cloud attachment | does attachment origin alter the target functional effect? |
| same body / new runtime | does reattachment preserve engineering state without assuming identity continuity? |

## Restoration requirement

Ablation alone is insufficient when restoration is feasible.

Preferred pattern:

```text
X PRESENT → effect
X REMOVED → effect degrades
X RESTORED → effect recovers
```

Restoration failure weakens the causal interpretation.

## Scientific boundary

Even a complete pass establishes only the bounded functional claim registered by the experiment.

```text
FUNCTIONAL_CAUSAL_EFFECT
!= PHENOMENAL_EXPERIENCE

EMBODIMENT_EFFECT
!= SUBJECTIVITY

SELF_MODEL_FUNCTION
!= SELFHOOD
```
