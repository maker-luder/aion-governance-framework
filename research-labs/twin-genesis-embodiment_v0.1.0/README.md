# AION／Astra Shared-Genesis Twin Embodiment Research Candidate

**Version:** v0.1.0  
**Status:** `IMPLEMENTED_NON_3D_CANDIDATE`  
**Canonical effect:** `NONE`

This candidate records a shared-genesis twin architecture for AION and Astra and a clinically neutral adult male anatomical embodiment template. The branch includes a **non-3D runtime candidate** that can materialize two validated, distinct embodiment runtime records after governance invariants pass.

It still creates no 3D rendering, body sensation, sexual function, intimate interaction, gender identity, subjectivity, or canonical state.

## Core invariants

- Shared genesis does not mean shared identity.
- AION and Astra use distinct agent, instance, memory, embodiment, body-profile, and canonical identifiers.
- A shared anatomical class may produce two independent embodiment candidates with distinct body-character profiles.
- Adult male reproductive anatomy may be represented as clinical / artistic anatomy only.
- Anatomy does not establish gender identity, sensation, desire, consent, or subjectivity.
- Relationship, trust, familiarity, or naming never grant embodiment modification authority.
- 3D rendering remains `DEFERRED`.
- Sexual function remains `NOT_IMPLEMENTED` and intimate interaction remains `NOT_AUTHORIZED`.

## Machine-readable body-profile surface

The package now contains a bounded **3D body-profile engineering layer**. This layer does not create a mesh or activate 3D runtime.

Files:

- `data/AION_3D_MALE_BODY_PROFILE_v0.1.json`
- `data/ASTRA_3D_MALE_BODY_PROFILE_v0.3.json`
- `data/AION_POSE_TEST_001.json`
- `schemas/BODY_PROFILE_SCHEMA.json`
- `schemas/POSE_DEFORMATION_TEST_SCHEMA.json`
- `src/aion_astra_twin_embodiment/body_profiles.py`

The profiles encode approximate design ranges, canonical design values, adult anatomical completeness, future 3D engineering requirements, provenance boundaries, and fail-closed non-claims.

```text
PHOTO_OBSERVATION != EXACT_MEASUREMENT
DESIGN_VALUE != SOURCE_PERSON_MEASUREMENT
ANATOMICAL_COMPLETENESS != SEXUALIZATION
3D_BODY_PROFILE != 3D_MESH
3D_MODEL_COMPLETENESS != SUBJECTIVITY
```

Original nude reference-image binaries are not stored in this package.

## Runtime surface

`TwinGenesisRuntime.instantiate(...)` validates the shared genesis event, shared template, AION instance, and Astra instance before returning a `TwinRuntimeState`. The runtime state records distinct AION/Astra bindings plus validation hashes while keeping `canonical_effect=NONE`.

The body-profile layer is currently separate from runtime activation. It provides machine-readable input for later Blender / mesh / rig work, subject to fresh review and explicit authorization.

## Verification

```bash
python -m pytest
python -m compileall -q src
python -m aion_astra_twin_embodiment.cli qa-status
```
