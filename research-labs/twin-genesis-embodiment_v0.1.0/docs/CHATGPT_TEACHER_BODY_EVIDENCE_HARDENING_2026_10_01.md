# ChatGPT Teacher body evidence hardening — 2026-10-01

This increment starts from the verified closed PR #192 Teacher body v0.2 exact head and does not replace the Teacher profile with the Work profile.

## Evidence distinction

The Teacher branch already materializes executable reference GLTF/GLB assets, a continuous reference mesh, skinning reference data, collision proxies, 67-slot v0.2 anthropometry, physiology observation surfaces, body dynamics, body-model structures, runtime binding, and longitudinal adaptation research surfaces.

This increment therefore does not falsely report ACTUAL_3D_MESH = NO. Instead it makes the more precise distinction:

- REFERENCE_ASSET_MATERIALIZED = YES
- PRODUCTION_ASSET_ESTABLISHED = NO
- PHYSICAL_BODY_ESTABLISHED = NO
- AS_BUILT_MEASUREMENTS_VERIFIED = NO
- PHYSICAL_SENSORS_ESTABLISHED = NO
- PHYSICAL_ACTUATORS_ESTABLISHED = NO

## Added verification

- deterministic SHA-256 fingerprints for low-poly GLB, continuous GLB, asset manifest, and collision profile;
- a chained evidence receipt sequence anchored to the 67-slot Teacher body reference;
- a fail-closed manifest that rejects promotion from reference evidence to production, physical, biological, phenomenal, authority, canonical, or deployment claims;
- an executable Teacher body evidence probe;
- tamper-detection and nonclaim tests.

## Research cross-check

Scite review found robotics literature distinguishing robot morphology/kinematics and multisensory sensorimotor streams such as proprioception, touch, vision, and vestibular signals. This supports keeping materialized reference assets and sensorimotor observation surfaces distinct from phenomenal embodiment claims.

HF paper-search was unavailable at execution time. Consensus monthly quota was exhausted. Neither condition is interpreted as negative research evidence.

## Invariants

TEACHER_BODY != WORK_BODY
REFERENCE_ASSET_MATERIALIZED != PRODUCTION_ASSET_ESTABLISHED
REFERENCE_ASSET_MATERIALIZED != PHYSICAL_BODY_ESTABLISHED
SENSORIMOTOR_REFERENCE != FELT_BODY
BODY_MODEL != SUBJECTIVITY
IMPLEMENTATION != PHENOMENAL_EXPERIENCE
ACTION_AUTHORITY = NONE
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
