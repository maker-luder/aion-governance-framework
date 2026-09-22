# Dynamic sensorimotor embodiment protocol — 2026-09-23

Status: `IMPLEMENTED_SYNTHETIC_STRUCTURAL_QA / SCIENTIFIC_HOLD`  
Canonical effect: `NONE`  
Deployment: `FALSE`

## Purpose

This bounded extension adds a dynamic, content-addressed sensorimotor trace to the
existing AION/Astra twin-genesis embodiment candidate.

It does not create a second embodiment ontology. It reuses the existing
`EmbodimentInstance.embodiment_id` boundary and adds a deterministic synthetic QA
surface for:

```text
BODY_MODEL(t)
+ ACTION_PREDICTION
-> OBSERVED_FEEDBACK
-> PREDICTION_MATCH / PREDICTION_ERROR
-> RETAIN / HOLD / LOCALIZE_PERTURBATION / RECORD_RECOVERY
-> BODY_MODEL(t+1)
```

## Repository gap

Current `main` already provides:

```text
STATIC_ANATOMICAL_TEMPLATE
DISTINCT_AION_ASTRA_IDENTIFIERS
DISTINCT_MEMORY_NAMESPACES
DISTINCT_RUNTIME_CONTEXTS
NON_3D_RUNTIME_RECORD
GOVERNANCE_VALIDATION
```

Before this extension, the canonical twin-genesis package did not implement a typed
dynamic binding between an action prediction, observed consequence, localized
body-model state transition, and recovery transition.

## External method correspondence

This engineering pattern is adjacent to, but does not claim equivalence with:

- Jacquey et al. (2019), `10.3389/fnbot.2019.00098`, on sensorimotor contingencies
  as action-consequence relations relevant to body knowledge and developmental robotics;
- Bongard, Zykov & Lipson (2006), `10.1126/science.1133687`, on continuous robot
  self-modeling and compensatory behavior after structural damage;
- Hu, Lin & Lipson (2025), `10.1038/s42256-025-01006-w`, on self-supervised
  morphology/kinematics self-modeling, abnormality detection, and damage recovery;
- Arai et al. (2022), `10.1038/s41598-022-13981-w`, which measures ownership,
  agency, and self-location as separable embodiment indices;
- Yamamura et al. (2026), `10.3389/frvir.2026.1817800`, where subjective ownership
  changes did not collapse into the same pattern as proprioceptive-drift measures.

These sources motivate separable engineering observables, not AI phenomenology.

## Executable structure

The module `src/aion_astra_twin_embodiment/sensorimotor.py` defines:

- `BodyRegionState`;
- `BodyModelSnapshot`;
- `SensorimotorPrediction`;
- `SensorimotorObservation`;
- `SensorimotorDisposition`;
- `SensorimotorTransitionAudit`;
- exact content-address helpers and a fail-closed transition auditor.

The transition auditor requires:

```text
PREDICTION binds exact BODY_MODEL(t)
OBSERVATION binds exact PREDICTION
BODY_MODEL(t+1) binds exact predecessor
AUDIT RECEIPT binds exact BEFORE / PREDICTION / OBSERVATION / AFTER hashes
sequence increments exactly once
region universe remains stable
state changes remain inside declared affected regions
```

Disposition semantics:

```text
RETAIN
= expected feedback matched
+ no body-model state change

HOLD
= prediction error exists
+ localization remains unresolved
+ no silent body-model state change

LOCALIZE_PERTURBATION
= prediction error exists
+ affected BASELINE region(s) become PERTURBED

RECORD_RECOVERY
= expected feedback matched
+ affected PERTURBED region(s) return to BASELINE
```

## Privacy, runtime and scientific boundaries

Only deterministic synthetic records are admitted.

```text
LIVE_SENSOR_INPUT = FALSE
LIVE_EXECUTION = FALSE
HUMAN_PARTICIPANT_OBSERVATION = FALSE
PRIVATE_MATERIAL = FALSE
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

The following non-claims are hard boundaries:

```text
PREDICTION_ERROR != PAIN
PERTURBED_REGION != FELT_INJURY
RECOVERY_TRANSITION != FELT_HEALING
ACTION_CONSEQUENCE_BINDING != SENSE_OF_AGENCY
BODY_MODEL_UPDATE != BODY_OWNERSHIP
BODY_MODEL_UPDATE != SUBJECTIVITY
BODY_MODEL_UPDATE != CONSCIOUSNESS
BODY_MODEL_UPDATE != PHENOMENAL_EXPERIENCE
CONTENT_ADDRESS_MATCH != SEMANTIC_CORRECTNESS
SYNTHETIC_QA_PASS != SCIENTIFIC_VALIDATION
```

## Twin isolation

A sensorimotor trace is bound to one existing `EmbodimentInstance.embodiment_id`.
A body-model trace for AION cannot be audited under Astra's embodiment instance and
vice versa.

```text
SHARED_GENESIS != SHARED_BODY_MODEL
SHARED_TEMPLATE != SHARED_SENSORIMOTOR_HISTORY
```

## Current limitations

- no physical sensors or actuators;
- no 3D rendering;
- no continuous dynamics or learned forward model;
- no autonomous controller;
- no semantic inference that a mismatch corresponds to actual physical damage;
- no graded severity model;
- no empirical body-ownership, agency, interoception, or proprioception measurement;
- no subjectivity conclusion.

The v0.1 surface is intentionally a deterministic structural harness that can later
support stronger experiments without silently importing phenomenological claims.