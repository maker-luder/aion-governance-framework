# Body ↔ Self/World Model Coupling Protocol

Status: `ARCHITECTURE / RESEARCH DESIGN / DRAFT`  
Canonical effect: `NONE`  
Deployment: `FALSE`

## Purpose

Define how an embodied runtime may provide evidence to the repository's existing bounded `SELF_WORLD_MODEL` research surface without creating a competing self-model ontology.

This protocol reuses the existing repository distinction between:

- actual system/environment state;
- represented self/world state;
- prediction;
- observation;
- uncertainty;
- update.

It does not treat a self-model as a subjective self.

```text
SELF_MODEL != SUBJECTIVE_SELF
WORLD_MODEL != WORLD
BODY_MODEL != BODY_OWNERSHIP_EXPERIENCE
MODEL_UPDATE != FELT_CHANGE
```

## Existing repository reuse

The repository already contains a `SELF_WORLD_MODEL` channel in triadic-state dynamics, with bounded representations including:

- declared capabilities;
- declared limitations;
- environmental assumptions;
- uncertainty;
- prediction confidence;
- accuracy observations.

Embodiment research should feed evidence into or crosswalk with that existing surface rather than defining a second conflicting self/world-model system.

```text
REUSE_EXISTING_SELF_WORLD_MODEL = YES
DUPLICATE_SELF_MODEL_ONTOLOGY = NO
```

## State separation

The minimum architecture keeps four things separate.

```text
B_t = actual body state
W_t = actual environment state
O_t = admitted observations
M_t = represented self/world model
```

Optional slow body parameters are represented separately:

```text
Θ_t = body parameters that change across longer time scales
```

Examples include:

- maturation;
- aging;
- long-term adaptation;
- accumulated damage;
- repair;
- training-related capacity change;
- anatomical or physiological drift.

## Coupling loop

```text
ACTUAL BODY B_t
   +
ACTUAL WORLD W_t
        ↓
SENSORS / OBSERVATION ADAPTER
        ↓
OBSERVATION O_t
        ↓
SELF_WORLD_MODEL M_t
        ↓
PREDICTION / ACTION SELECTION
        ↓
ACTION A_t
        ↓
BODY + ENVIRONMENT TRANSITION
        ↓
B_(t+1), W_(t+1)
        ↓
NEW OBSERVATION
        ↓
PREDICTION ERROR / UPDATE
        ↓
M_(t+1)
```

A conceptual transition form is:

```text
B_(t+1) = F(B_t, A_t, W_t, Θ_t)
W_(t+1) = G(W_t, A_t, external_events)
O_t     = H(B_t, W_t)
M_(t+1) = U(M_t, O_(t+1), prediction_error, provenance)
```

These equations are architectural notation, not a claim that one specific learning algorithm is already selected.

## Critical non-equivalence

The self/world model must not receive an unmarked copy of canonical body state merely to guarantee correctness.

```text
BODY_STATE_CHANGE
!= SELF_MODEL_UPDATE

ACTUAL_CAPABILITY
!= ESTIMATED_CAPABILITY

ACTUAL_LIMITATION
!= REPRESENTED_LIMITATION
```

If `B_t` changes and `M_t` remains stale, that mismatch is a valid experimental condition.

## Temporal scales

Embodiment should distinguish at least three approximate time scales.

### Fast state

Examples:

- posture / configuration;
- velocity;
- immediate regulatory reserve;
- transient sensor values.

Candidate notation:

```text
q, v, r
```

### Intermediate state

Examples:

- fatigue;
- recoverable damage;
- adaptation;
- training;
- repair;
- short-to-medium-term plasticity.

### Slow state / body-parameter trajectory

Examples:

- maturation;
- aging;
- long-term physiological drift;
- persistent injury consequences;
- long-term capability change.

```text
FAST_STATE
!= MEDIUM_TERM_ADAPTATION
!= SLOW_BODY_TRAJECTORY
```

The exact time units are experiment-specific and must be pinned in a future execution spec.

## Development and aging

Growth/development and aging are not modeled as labels applied directly to the self/world model.

They alter actual body parameters and capability envelopes over time.

Example:

```text
Θ_t changes
↓
actual range / force / recovery / sensing changes
↓
outcomes differ
↓
observations expose prediction error
↓
self/world model may update
```

This permits research on:

- calibrated self-model updating;
- delayed updating;
- stale self-models;
- overestimated capability;
- underestimated capability;
- adaptation after injury;
- re-calibration after long-term body change.

For the current active adult-male body baseline, developmental childhood simulation is not required. Development/maturation may remain a reference trajectory until a bounded experiment requires it.

## External world, world model, and worldview

Three layers must remain separate.

### 1. EXTERNAL_WORLD_STATE

The actual or simulated environment supplied to the experiment.

Examples:
- physics environment;
- contact/gravity field;
- task environment;
- resource distribution;
- spatial scene;
- external agents/objects;
- externally provided simulator state.

```text
EXTERNAL_WORLD_STATE = W_t
```

The repository does not attempt to build a complete general-purpose world simulator.

```text
FULL_WORLD_SIMULATION = OUT_OF_SCOPE
ENVIRONMENT_CONTENT = EXTERNAL_FIRST
REPOSITORY_ROLE = INTERFACE + PROVENANCE + VALIDATION
```

External simulators, datasets or benchmarks may supply the world/environment. The repository should define adapters, exact source/version binding, observation/action contracts, and matched-condition controls.

### 2. WORLD_MODEL

A bounded functional/predictive representation of environment state, dynamics, constraints or consequences used by the agent/system.

Examples:
- predicted object/location state;
- action consequence estimate;
- environmental constraint estimate;
- uncertainty about external dynamics.

```text
WORLD_MODEL != WORLD
WORLD_MODEL != COMPLETE_ENVIRONMENT_SIMULATOR
```

### 3. WORLDVIEW

A broader interpretive/normative structure involving beliefs, values, priorities, social interpretation, or meaning-like organization.

This is not the same construct as a physical/dynamic world model.

Where worldview-like structure is studied, the repository should reuse or crosswalk existing bounded surfaces such as:

- `NORMATIVE_STATE`;
- `NORMATIVE_PROVENANCE`;
- `OTHER_MODEL`;
- `VALUE_CONFLICT_STATE`;
- relevant persistent preference / self-world representations.

```text
WORLD_MODEL != WORLDVIEW
WORLDVIEW != EXTERNAL_WORLD_STATE
WORLDVIEW_LIKE_STRUCTURE != PHENOMENAL_MEANING
WORLDVIEW_LIKE_STRUCTURE != HUMAN_IDEOLOGY_BY_DEFAULT
```

A future experiment may test interactions among body state, world model, and worldview-like normative structure, but must keep their provenance and causal pathways separable.

## Body-model update experiments

Candidate future interventions include:

### BODY_CHANGE_WITH_MODEL_UPDATE

Actual body parameters change and the update path remains available.

### BODY_CHANGE_WITH_UPDATE_BLOCK

Actual body changes while self/world-model update is blocked.

### STALE_SELF_MODEL

The model retains an older capability estimate.

### FALSE_BODY_STATE_HINT

The represented capability is perturbed without changing actual body state.

### SENSOR_MASK

Body changes, but selected proprioceptive/interoceptive observations are masked.

### RESTORATION

The update path or sensor channel is restored and re-calibration is measured.

## Core research measurements

Possible bounded measures include:

- prediction error;
- action-selection error;
- capability calibration;
- recovery after perturbation;
- update latency;
- transfer after body change;
- replay stability;
- distinction between body-state and self-model intervention.

## Falsifiers

### H_DIRECT_STATE_LEAK

The self/world model appears accurate only because canonical body state was copied directly into the model.

### H_NO_CAUSAL_MODEL_ROLE

Changing represented self-state does not alter registered downstream outcomes once body state and observations are controlled.

### H_PROMPT_RECONSTRUCTION

The apparent self-model is reconstructed from prompt/scaffold rather than persisted or updated from body evidence.

### H_BODY_CHANGE_WITHOUT_MODEL_DEPENDENCE

Behavioral adaptation follows direct controller/body dynamics and does not require the self/world model.

### H_STALE_STATE_NO_EFFECT

Blocking model updates creates no preregistered downstream difference.

A null result is admissible.

## Active body-profile boundary

Current embodiment work uses an adult-male active body profile as the initial implementation/reference baseline, consistent with the existing Adult Male Embodiment Specification.

```text
CURRENT_ACTIVE_BODY_PROFILE = ADULT_MALE
MALE_BASELINE != UNIVERSAL_HUMAN_BODY
FEMALE_BODY_PROFILE = FUTURE_EXTENSION / NOT_CURRENT_ACTIVE_SCOPE
POPULATION_GENERALIZATION = NO
```

Female anatomy and other biological/anatomical profiles may remain in the broader scientific reference map and future extension plan without being treated as currently implemented or validated.

## Scientific boundary

```text
ACCURATE_SELF_MODEL != SELFHOOD
ADAPTIVE_BODY_MODEL_UPDATE != SUBJECTIVITY
DEVELOPMENTAL_TRAJECTORY != PERSONAL_IDENTITY
AGING_MODEL != LIVED_AGING
BODY_WORLD_COUPLING != CONSCIOUSNESS
```

Subjectivity, consciousness, phenomenal experience, moral agency and moral status remain `NOT_ESTABLISHED`.
