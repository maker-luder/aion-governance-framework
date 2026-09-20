# AION／Astra Shared-Genesis Twin Embodiment Research Candidate

**Version:** v0.1.0  
**Status:** `IMPLEMENTED_NON_3D_CANDIDATE`  
**Canonical effect:** `NONE`

This candidate records a shared-genesis twin architecture for AION and Astra. The current engineering branch now treats their future bodies as **3D full-body humanlike male-form humanoid robotic embodiment digital models**, not biological human bodies.

Human artistic-anatomy references are used only for morphology, proportions, pose, and deformation targets.

```text
HUMAN_REFERENCE
-> MORPHOLOGY / PROPORTION / POSE
-> ROBOTIC TRANSLATION
-> 3D FULL-BODY HUMANLIKE MALE-FORM HUMANOID ROBOTIC EMBODIMENT DIGITAL MODEL

NOT:

HUMAN_REFERENCE
-> BIOLOGICAL CLONE
-> DIGITAL DOUBLE
```

The branch still creates no live 3D rendering, physical robot, body sensation, sexual function, intimate interaction, gender identity, subjectivity, or canonical state.

## Core invariants

- AION and Astra remain distinct agent, instance, memory, embodiment, body-profile, and canonical identities.
- Both body profiles use `HUMANOID_ROBOT` as the embodiment platform.
- Both use `SYNTHETIC_NONBIOLOGICAL` substrate.
- Both use a complete robotic male-form morphology derived from human anatomy as reference only.
- Adult male-form completeness does not implement biological reproductive organs or reproductive function.
- Synthetic male-form external modules remain non-erotic anatomy / morphology surfaces.
- Relationship, trust, familiarity, or naming never grant embodiment modification authority.
- 3D rendering remains `DEFERRED`.
- Actuation, sensing, power distribution, thermal management, and live runtime remain unimplemented.
- Sexual function remains `NOT_IMPLEMENTED`.
- Body sensation and subjectivity remain `NOT_ESTABLISHED`.

## Robotic embodiment digital-model layer

Machine-readable profiles:

- `data/AION_3D_FULL_BODY_HUMANLIKE_MALE_FORM_HUMANOID_ROBOT_MODEL_v0.3.json`
- `data/ASTRA_3D_FULL_BODY_HUMANLIKE_MALE_FORM_HUMANOID_ROBOT_MODEL_v0.5.json`
- `data/AION_POSE_TEST_001.json`

Schemas / implementation:

- `schemas/BODY_PROFILE_SCHEMA.json`
- `schemas/POSE_DEFORMATION_TEST_SCHEMA.json`
- `src/aion_astra_twin_embodiment/body_profiles.py`
- `tests/test_body_profiles.py`

Each profile now distinguishes the physical robotic layer stack:

```text
INTERNAL_STRUCTURAL_FRAME
ACTUATOR_INTERFACE_LAYER
COMPLIANT_VOLUME_LAYER
SYNTHETIC_SKIN_SHELL
```

The human-like external form is therefore a morphology envelope around a future robotic/mechatronic substrate, not a claim of biological embodiment.

## Male-form morphology interpretation

The complete male-form surface includes robotic morphological analogues for the pubic, penile, glans, prepuce, scrotal, testicular-volume, inguinal, perineal, and anal-region surfaces.

These are modeled as non-biological geometric / compliant-body modules.

```text
HUMANLIKE_MALE_FORM != BIOLOGICAL_REPRODUCTIVE_SYSTEM
ANATOMICAL_REFERENCE != BIOLOGICAL_SUBSTRATE
FORM_COMPLETENESS != SEXUAL_FUNCTION
GEOMETRY != SENSATION
ROBOT_BODY != SUBJECTIVITY
```

## Runtime surface

`TwinGenesisRuntime.instantiate(...)` remains a non-3D governed runtime candidate. The robotic body-module layer is not bound to live runtime.

## Verification

```bash
python -m pytest
python -m compileall -q src
python -m aion_astra_twin_embodiment.cli qa-status
```


## Hardened model classification

```text
EMBODIMENT_PLATFORM = HUMANOID_ROBOT
BODY_SCOPE = FULL_BODY
MORPHOLOGY_CLASS = HUMANLIKE_MALE_FORM
SUBSTRATE = SYNTHETIC_NONBIOLOGICAL
MODEL_CLASS = ROBOTIC_EMBODIMENT_DIGITAL_MODEL
DIGITAL_TWIN_STATUS = NOT_ESTABLISHED
```

The full-body contract covers head, neck, torso, pelvis, both arms/hands, both legs/feet, and the complete external male-form surface.

The digital representation stack is separated into morphology, visual geometry, structural, kinematic, dynamic, collision, actuation-interface, sensor-interface, compliant-body, and synthetic-skin layers.

Future interchange targets are recorded without claiming current implementation:

```text
ROBOT_DESCRIPTION_TARGETS = URDF / SDF
VISUAL_ASSET_TARGETS = GLB / USD

CURRENT_EXPORT_SUPPORT = NOT_IMPLEMENTED
```

Terminology rationale and external-source cross-check:

- `docs/ROBOTIC_EMBODIMENT_TERMINOLOGY_CROSSWALK_2026_09_20.md`

```text
REPOSITORY_LOCAL_COMPOUND_TERM
!= EXTERNAL_STANDARD_TERM
```
