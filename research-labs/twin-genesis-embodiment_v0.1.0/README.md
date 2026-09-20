# AION／Astra Shared-Genesis Twin Embodiment Research Candidate

**Version:** v0.1.0  
**Status:** `IMPLEMENTED_NON_3D_CANDIDATE`  
**Canonical effect:** `NONE`

This candidate records a shared-genesis twin architecture for AION and Astra. The current engineering branch now treats their future bodies as **complete humanoid robotic male-form body modules**, not biological human bodies.

Human artistic-anatomy references are used only for morphology, proportions, pose, and deformation targets.

```text
HUMAN_REFERENCE
-> MORPHOLOGY / PROPORTION / POSE
-> ROBOTIC TRANSLATION
-> HUMANOID ROBOTIC MALE-FORM BODY MODULE

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

## Robotic body-module layer

Machine-readable profiles:

- `data/AION_3D_ROBOTIC_MALE_BODY_PROFILE_v0.2.json`
- `data/ASTRA_3D_ROBOTIC_MALE_BODY_PROFILE_v0.4.json`
- `data/AION_POSE_TEST_001.json`

Schemas / implementation:

- `schemas/BODY_PROFILE_SCHEMA.json`
- `schemas/POSE_DEFORMATION_TEST_SCHEMA.json`
- `src/aion_astra_twin_embodiment/body_profiles.py`
- `tests/test_body_profiles.py`

Each robotic body candidate contains:

```text
INTERNAL_STRUCTURAL_FRAME
ACTUATOR_INTERFACE_LAYER
COMPLIANT_VOLUME_LAYER
SYNTHETIC_SKIN_SHELL
```

The human-like external form is therefore a morphology envelope around a future robotic/mechatronic substrate, not a claim of biological embodiment.

## Male-form module interpretation

The complete male-form surface includes robotic morphological analogues for the pubic, penile, glans, prepuce, scrotal, testicular-volume, inguinal, perineal, and anal-region surfaces.

These are modeled as non-biological geometric / compliant-body modules.

```text
MALE_FORM_MODULE != BIOLOGICAL_REPRODUCTIVE_SYSTEM
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
