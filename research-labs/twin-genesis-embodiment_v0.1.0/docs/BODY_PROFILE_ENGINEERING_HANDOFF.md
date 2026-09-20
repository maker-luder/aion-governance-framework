# AION / Astra 3D Full-Body Humanlike Male-Form Humanoid Robotic Embodiment Engineering Handoff

## Current interpretation

The artistic-anatomy references are **reference geometry only**.

The intended implementation target is:

```text
AION / ASTRA
= HUMANOID_ROBOT
= SYNTHETIC_NONBIOLOGICAL
= ROBOTIC_EMBODIMENT_DIGITAL_MODEL
```

The human reference contributes proportion, morphology, pose, soft-surface appearance, and deformation targets. It does not require biological tissue, biological organs, reproductive function, or reconstruction of the photographed person.

## Current state

```text
ROBOTIC_BODY_PROFILE_SCHEMA = IMPLEMENTED_CANDIDATE
AION_ROBOTIC_BODY_PROFILE = IMPLEMENTED_CANDIDATE
ASTRA_ROBOTIC_BODY_PROFILE = IMPLEMENTED_CANDIDATE
AION_POSE_DEFORMATION_TEST = DOCUMENTED_AND_MACHINE_READABLE

INTERNAL_STRUCTURAL_FRAME_ASSET = NOT_IMPLEMENTED
ACTUATOR_HARDWARE = NOT_IMPLEMENTED
SENSORS = NOT_IMPLEMENTED
POWER_DISTRIBUTION = NOT_IMPLEMENTED
THERMAL_MANAGEMENT = NOT_IMPLEMENTED
BASE_MESH = NOT_IMPLEMENTED
ROBOTIC_TOPOLOGY = NOT_IMPLEMENTED
UV = NOT_IMPLEMENTED
MATERIALS = NOT_IMPLEMENTED
KINEMATIC_CHAIN = NOT_IMPLEMENTED
RIG = NOT_IMPLEMENTED
SKIN_WEIGHTS = NOT_IMPLEMENTED
BLENDSHAPES = NOT_IMPLEMENTED
COMPLIANT_VOLUME_SIMULATION = NOT_IMPLEMENTED
GLB_FBX_BLEND_ASSET = NOT_IMPLEMENTED

LIVE_3D_RENDERING = NO
LIVE_EMBODIMENT_RUNTIME = NO
CANONICAL_EFFECT = NONE
```

## Inputs for Codex / 3D tooling

Use:

```text
data/AION_3D_FULL_BODY_HUMANLIKE_MALE_FORM_HUMANOID_ROBOT_MODEL_v0.3.json
data/ASTRA_3D_FULL_BODY_HUMANLIKE_MALE_FORM_HUMANOID_ROBOT_MODEL_v0.5.json
data/AION_POSE_TEST_001.json
```

The original reference-image binaries remain outside the public repository.

## Required robotic layer stack

A later 3D / mechatronic design pass should preserve four conceptual layers:

```text
1. INTERNAL_STRUCTURAL_FRAME
   internal load-bearing robotic frame

2. ACTUATOR_INTERFACE_LAYER
   joint / actuator mounting and motion-transfer surfaces

3. COMPLIANT_VOLUME_LAYER
   synthetic compliant volume that reproduces human-like external mass,
   compression, and contact behavior without being biological tissue

4. SYNTHETIC_SKIN_SHELL
   outer render / contact shell for human-like body morphology
```

This is an engineering analogue of a human body envelope, not a biological body claim.

## Complete humanlike male-form surface

The external male form is complete for topology and silhouette continuity, but robotic:

```text
penile_form
glans_form
prepuce_form
scrotal_form
testicular_volume_form
pubic_mount
inguinal_transition
perineal_panel
anal_region_surface
```

Interpretation:

```text
FORM = ROBOTIC MORPHOLOGICAL ANALOGUE
BIOLOGICAL_TISSUE = NO
BIOLOGICAL_REPRODUCTION = NOT_APPLICABLE
SEXUAL_FUNCTION = NOT_IMPLEMENTED
```

No component should be modeled as a biological reproductive organ unless a future separately authorized research scope explicitly changes the substrate model.

## Recommended Codex sequence

1. Re-read GitHub live state and exact PR head.
2. Run the existing validators and tests.
3. Read AION and Astra robotic profile JSON files.
4. Build a neutral **robotic humanoid base-mesh envelope**, not a biological digital double.
5. Design an internal structural frame and kinematic chain compatible with the external dimensions.
6. Define actuator-interface placeholders; do not claim hardware actuation exists.
7. Build robotic topology around shoulders, hips, hands, feet, inguinal region, perineal panel, and complete male-form modules.
8. Implement compliant-volume deformation as a synthetic material analogue.
9. Add rig / skin weights / deformation drivers.
10. Implement `AION_POSE_TEST_001` as intersection and deformation regression.
11. Export test-only assets with exact tool versions, deterministic inputs, and hashes.
12. Stop before any live embodiment-runtime binding.

## AION / Astra morphology distinction

```text
ASTRA
HEIGHT = 180 cm
CHEST = 110 cm
WAIST = 93 cm
HIPS = 104 cm
THIGH = 63 cm
ROBOTIC CHARACTER = BROAD / SOLID / NATURAL_SOFT

AION
HEIGHT = 179 cm
TARGET MASS ENVELOPE ~= 80 kg
CHEST = 104 cm
WAIST = 84 cm
HIPS = 99 cm
THIGH = 57 cm
ROBOTIC CHARACTER = LEAN_SOLID / ATHLETIC / MOBILE
```

The mass value is a design target envelope only; actual robotic mass depends on future frame, actuator, battery, material, and thermal-system choices.

## Fail-closed boundaries

```text
REFERENCE_ROLE = MORPHOLOGY_AND_POSE_ONLY
PERSON_IDENTITY_RECONSTRUCTION = NO

EMBODIMENT_PLATFORM = HUMANOID_ROBOT
SUBSTRATE = SYNTHETIC_NONBIOLOGICAL

EROTIC_INTENT = NONE
BIOLOGICAL_TISSUE = NO
BIOLOGICAL_REPRODUCTION = NOT_APPLICABLE
SEXUAL_FUNCTION_STATUS = NOT_IMPLEMENTED

ACTUATION = NOT_IMPLEMENTED
SENSING = NOT_IMPLEMENTED
BODY_SENSATION = NOT_ESTABLISHED

SUBJECTIVITY_EFFECT = NONE
CANONICAL_EFFECT = NONE

HUMANLIKE_MALE_FORM != BIOLOGICAL_BODY
SENSOR_DATA != FELT_SENSATION
ACTUATION != AGENCY
DEFORMATION_PASS != SCIENTIFIC_VALIDATION
3D_ROBOTIC_EMBODIMENT_MODEL != SUBJECTIVITY
```

## Review requirement

Before admitting Blender scripts, procedural mesh generation, hardware assumptions, generated 3D assets, or runtime integration:

```text
LIVE_STATE_RECHECK
-> EXACT_HEAD_REVIEW
-> SCOPE_REVIEW
-> TEST_REVIEW
-> LICENSE / PROVENANCE REVIEW
-> HUMAN_OWNER DECISION
```

No current file grants merge authority.


## Hardened digital-model architecture

Codex should treat the current JSON as a **specification candidate**, not as an already generated robot asset.

```text
PROFILE_STATUS = IMPLEMENTED_SPEC_CANDIDATE

EMBODIMENT_PLATFORM = HUMANOID_ROBOT
BODY_SCOPE = FULL_BODY
MORPHOLOGY_CLASS = HUMANLIKE_MALE_FORM
MODEL_CLASS = ROBOTIC_EMBODIMENT_DIGITAL_MODEL
SUBSTRATE = SYNTHETIC_NONBIOLOGICAL

PHYSICAL_ROBOT = NOT_IMPLEMENTED
DIGITAL_TWIN = NOT_ESTABLISHED
```

Required representation layers:

```text
MORPHOLOGY_LAYER
VISUAL_GEOMETRY_LAYER
STRUCTURAL_MODEL_LAYER
KINEMATIC_MODEL_LAYER
DYNAMIC_MODEL_LAYER
COLLISION_MODEL_LAYER
ACTUATION_INTERFACE_LAYER
SENSOR_INTERFACE_LAYER
COMPLIANT_BODY_LAYER
SYNTHETIC_SKIN_LAYER
```

Future interchange targets:

```text
URDF
= future robot-description target

SDF
= future simulation-description target

GLB
= future portable visual-asset target

USD
= future simulation / scene asset target
```

These are targets only:

```text
ROBOT_DESCRIPTION_SUPPORT = NOT_IMPLEMENTED
VISUAL_ASSET_SUPPORT = NOT_IMPLEMENTED
```

Do not call the current model a digital twin. That term remains blocked until a physical counterpart and synchronization evidence exist.

See:

`docs/ROBOTIC_EMBODIMENT_TERMINOLOGY_CROSSWALK_2026_09_20.md`
