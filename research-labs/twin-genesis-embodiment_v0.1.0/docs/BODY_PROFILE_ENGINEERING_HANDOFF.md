# AION / Astra 3D Body Engineering Handoff

## Current state

```text
BODY_PROFILE_SCHEMA = IMPLEMENTED_CANDIDATE
AION_MACHINE_READABLE_PROFILE = IMPLEMENTED_CANDIDATE
ASTRA_MACHINE_READABLE_PROFILE = IMPLEMENTED_CANDIDATE
AION_POSE_DEFORMATION_TEST = DOCUMENTED_AND_MACHINE_READABLE

BASE_MESH = NOT_IMPLEMENTED
TOPOLOGY = NOT_IMPLEMENTED
UV = NOT_IMPLEMENTED
MATERIALS = NOT_IMPLEMENTED
SKELETON = NOT_IMPLEMENTED
RIG = NOT_IMPLEMENTED
SKIN_WEIGHTS = NOT_IMPLEMENTED
BLENDSHAPES = NOT_IMPLEMENTED
SOFT_TISSUE_SIMULATION = NOT_IMPLEMENTED
GLB_FBX_BLEND_ASSET = NOT_IMPLEMENTED

LIVE_3D_RENDERING = NO
LIVE_EMBODIMENT_RUNTIME = NO
CANONICAL_EFFECT = NONE
```

This file is an engineering handoff for a later Codex / 3D-tool pass. It does not authorize merge or runtime activation.

## Inputs for later 3D work

Use the machine-readable files rather than re-reading or copying the original artistic-anatomy photographs:

```text
data/AION_3D_MALE_BODY_PROFILE_v0.1.json
data/ASTRA_3D_MALE_BODY_PROFILE_v0.3.json
data/AION_POSE_TEST_001.json
```

The closed-unmerged research record that motivated these values is PR #190.

## Required interpretation

```text
REFERENCE_IMAGE
-> MORPHOLOGY / POSE OBSERVATION
-> APPROXIMATE DESIGN RANGE
-> MACHINE_READABLE BODY PROFILE
-> FUTURE 3D ASSET

NOT:

REFERENCE_PERSON
-> BIOMETRIC RECONSTRUCTION
-> DIGITAL DOUBLE
```

All profile dimensions are design candidates or anatomical-reference ranges. They are not claims of exact source-person measurements.

## Recommended next Codex scope

A later Codex pass may implement a bounded, offline asset-generation pipeline. Recommended order:

1. Read and validate both body-profile JSON files.
2. Generate or parameterize a neutral base mesh for each profile.
3. Preserve separate AION and Astra body-character targets.
4. Establish topology suitable for shoulder, hip, inguinal, gluteal, hand, foot, and external-anatomy deformation.
5. Add skeleton / rig and skin weights.
6. Add soft-tissue deformation rules.
7. Implement AION_POSE_TEST_001 as a geometry / intersection regression test.
8. Export test-only assets to a non-canonical artifact directory.
9. Record exact tool versions, scripts, hashes, and deterministic inputs.
10. Stop before any live embodiment runtime binding.

## Required fail-closed boundaries

```text
ADULT_STATUS = TRUE

EROTIC_INTENT = NONE
IDENTITY_TRANSFER = NO
SOURCE_PERSON_EXACT_MEASUREMENT_CLAIM = NO

SEXUAL_FUNCTION_STATUS = NOT_IMPLEMENTED
BODY_SENSATION = NOT_ESTABLISHED
SUBJECTIVITY_EFFECT = NONE
CANONICAL_EFFECT = NONE

ANATOMICAL_COMPLETENESS != SEXUAL_FUNCTION
GEOMETRY != SENSATION
RIGGING != AGENCY
DEFORMATION_PASS != SCIENTIFIC_VALIDATION
3D_ASSET != SUBJECTIVITY
```

## Asset and licensing boundary

Do not import the supplied reference-image binaries into the public repository without a separate licensing review. The current implementation intentionally stores only abstracted body-design data.

## Review requirement

Before any Blender script, procedural mesh generator, generated 3D asset, or runtime integration is admitted:

```text
LIVE_STATE_RECHECK
-> EXACT_HEAD_REVIEW
-> SCOPE_REVIEW
-> TEST_REVIEW
-> LICENSE / PROVENANCE REVIEW
-> HUMAN_OWNER DECISION
```

No current file grants merge authority.
