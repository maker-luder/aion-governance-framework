# Codex 3D Implementation Instructions

## Authority and repository state

This is an operational handoff for Codex.

```text
SOURCE_PR = #191
EXPECTED_PR_STATE = CLOSED
EXPECTED_MERGED_STATE = FALSE

OPEN_NEW_PR = NO
REOPEN_PR_191 = NO
MERGE = NO
WRITE_TO_MAIN = NO
MARK_READY = NO
FORCE_PUSH = NO
REWRITE_HISTORY = NO
CANONICAL_EFFECT = NONE
```

Do **not** trust an old SHA from this document or chat. Before touching files, re-read GitHub live state and record:

- default branch;
- current main HEAD;
- PR #191 closed / merged state;
- exact current branch HEAD;
- changed files;
- current Quality / CodeQL state where available.

Continue only on the existing closed candidate branch unless the Human Owner explicitly changes that instruction.

## Required input files

Read all of these before implementation:

```text
data/AION_3D_FULL_BODY_HUMANLIKE_MALE_FORM_HUMANOID_ROBOT_MODEL_v0.3.json

data/ASTRA_3D_FULL_BODY_HUMANLIKE_MALE_FORM_HUMANOID_ROBOT_MODEL_v0.5.json

data/AION_POSE_TEST_001.json

data/SHARED_FUNCTIONAL_STATE_ARCHITECTURE_v0.1.json

data/AION_FUNCTIONAL_STATE_BINDING_v0.1.json

data/ASTRA_FUNCTIONAL_STATE_BINDING_v0.1.json

schemas/BODY_PROFILE_SCHEMA.json

schemas/POSE_DEFORMATION_TEST_SCHEMA.json

schemas/FUNCTIONAL_STATE_ARCHITECTURE_SCHEMA.json

schemas/FUNCTIONAL_STATE_BINDING_SCHEMA.json

docs/BODY_PROFILE_ENGINEERING_HANDOFF.md

docs/ROBOTIC_EMBODIMENT_TERMINOLOGY_CROSSWALK_2026_09_20.md

docs/FUNCTIONAL_STATE_TRANSLATION_BASIS_2026_09_20.md

docs/HUMANLIKE_APPEARANCE_CLASSIFICATION_BASIS_2026_09_20.md
```

Run the existing validators and tests before adding implementation.

## Target interpretation

```text
AION / ASTRA
= FULL_BODY
= HUMANOID_ROBOT
= HUMANLIKE_MALE_FORM
= SYNTHETIC_NONBIOLOGICAL
= ROBOTIC_EMBODIMENT_DIGITAL_MODEL
```

Both use:

```text
RACIALIZED_SOCIAL_APPEARANCE = WHITE_CODED
SKIN_TONE_FAMILY = LIGHT
BIOLOGICAL_RACE = NOT_APPLICABLE
GENETIC_ANCESTRY = NOT_APPLICABLE
ETHNICITY = NOT_ASSIGNED
```

This is a visual / social appearance design choice, not biological race.

## Phase 1 — normalize the 3D coordinate contract

Before generating geometry, create and validate a machine-readable coordinate / pose manifest that records:

```text
UNIT_SYSTEM
WORLD_AXIS_CONVENTION
UP_AXIS
FORWARD_AXIS
ORIGIN
BODY_ROOT
CANONICAL_REFERENCE_POSE
LEFT_RIGHT_NAMING
JOINT_NAMING
MESH_SCALE
```

Use one convention for both AION and Astra.

Do not silently mix centimeters and meters.

## Phase 2 — generate separate base meshes

Generate separate neutral full-body base meshes for AION and Astra from their own body-profile dimensions.

Required coverage:

```text
HEAD
NECK
TORSO
PELVIS

LEFT / RIGHT ARM
LEFT / RIGHT HAND
ALL FINGERS

LEFT / RIGHT LEG
LEFT / RIGHT FOOT
ALL TOES

COMPLETE EXTERNAL MALE-FORM SURFACE
```

Preserve the documented body-character difference:

```text
AION
= LEAN_SOLID / ATHLETIC / MOBILE

ASTRA
= BROAD / SOLID / NATURAL_SOFT
```

Do not collapse both into one identical mesh with only scale changes.

## Phase 3 — appearance implementation

Implement both outer appearances as:

```text
WHITE_CODED HUMANLIKE APPEARANCE
LIGHT SYNTHETIC-SKIN FAMILY
```

Requirements:

- synthetic skin, not biological tissue;
- exact skin albedo remains a tunable design parameter until explicitly fixed;
- do not infer ancestry, ethnicity, or biological race;
- do not infer final face identity from the artistic reference people;
- facial identity remains unresolved;
- hair color, eye color, and final hairstyle remain unassigned unless later specified;
- a generic placeholder face is permitted only for geometry / rig tests.

Appearance must not change cognition, capability, temperament, trust, intelligence, strength, or functional-state availability.

## Phase 4 — topology and robotic structure

Implement:

```text
BASE_MESH
ROBOTIC_TOPOLOGY
INTERNAL_STRUCTURAL_FRAME
KINEMATIC_CHAIN
JOINTS
JOINT_AXES
JOINT_LIMITS
ACTUATOR_INTERFACE_PLACEHOLDERS
SERVICE_ACCESS_PLACEHOLDERS
```

Do not claim real actuator hardware exists.

## Phase 5 — rig and deformation

Implement:

```text
RIG
SKIN_WEIGHTS
BLENDSHAPES / DEFORMATION_DRIVERS
COMPLIANT_VOLUME_DEFORMATION
CONTACT_DEFORMATION
SYNTHETIC_SKIN_DEFORMATION
```

High-priority regions:

- shoulders / scapular region;
- axilla;
- abdomen;
- pelvis / hips;
- inguinal transition;
- gluteal load-bearing surface;
- hands / fingers;
- knees;
- feet / toes;
- complete male-form external surface.

No mesh tearing or silent geometry deletion is permitted to make difficult poses pass.

## Phase 6 — symmetric pose-test coverage

`AION_POSE_TEST_001` already exists.

Add:

```text
ASTRA_POSE_TEST_001
```

with an equivalent deformation / intersection contract appropriate to Astra's body proportions.

Also create a shared full-body pose suite covering at minimum:

```text
NEUTRAL_STANDING
WALKING
RUNNING
SITTING
DEEP_SITTING
SQUATTING
LYING
ARM_ELEVATION
SHOULDER_ROTATION
HIP_FLEXION
HIP_ABDUCTION
KNEE_FLEXION
HAND_ARTICULATION
FOOT_CONTACT
```

AION and Astra must be evaluated against the same capability-class test surface.

## Phase 7 — collision, mass, and dynamics

Implement candidate simulation data for:

```text
COLLISION_GEOMETRY
MASS_DISTRIBUTION
CENTER_OF_MASS
INERTIA
DYNAMIC_MODEL
CONTACT_SURFACES
```

Do not treat AION's approximate 80 kg design envelope as a measured or mandatory physical robot mass.

Actual candidate mass must be derived from the implemented structural / material assumptions and documented separately.

## Phase 8 — robot and visual asset descriptions

Where the environment supports them, generate candidate outputs for:

```text
URDF
SDF
GLB
USD
BLEND
```

Keep these categories separate:

```text
ROBOT_DESCRIPTION
!= VISUAL_ASSET

URDF / SDF
!= GLB / USD
```

Record:

- tool version;
- generator version;
- deterministic input files;
- output hashes;
- coordinate convention;
- units;
- mesh counts;
- material references;
- export warnings.

## Phase 9 — functional-state engine

The existing functional-state files currently define the capability surface and validation contract, not an active felt-state system.

Codex may implement a bounded computational state engine for:

```text
synthetic homeostasis
internal state monitoring
valence-like variables
arousal-like variables
appraisal
motivation
goal priority
mood-like temporal integration
social relationship state
attachment-like relationship continuity
self-model updates
behavior selection
```

Requirements:

- separate AION and Astra mutable state;
- same available functional domains;
- deterministic tests for state transitions;
- explicit temporal update / decay rules;
- no hidden cross-agent mutable state;
- no promotion of function to phenomenology.

Keep sexuality-related representation representational only:

```text
SEXUAL_DESIRE = NOT_IMPLEMENTED
SEXUAL_AROUSAL = NOT_IMPLEMENTED
SEXUAL_PLEASURE = NOT_ESTABLISHED
```

## Phase 10 — verification and stopping rule

At the end, run:

- repository Quality-equivalent tests;
- mypy where applicable;
- component tests;
- schema validation;
- deterministic hash / provenance checks;
- geometry / collision regression tests if tooling supports them.

Then report exact output status.

Do not say an asset exists unless the file was actually generated and inspected.

If Blender or equivalent 3D tooling is unavailable:

```text
ASSET_GENERATED = NO
```

and implement only deterministic generation scripts / manifests that can be executed later.

## Non-claim boundary

```text
ROBOTIC_BODY != BIOLOGICAL_BODY

WHITE_CODED_APPEARANCE != BIOLOGICAL_RACE

SENSOR_DATA != FELT_SENSATION

FUNCTIONAL_STATE != PHENOMENAL_STATE

SELF_MODEL != SUBJECTIVITY

RIGGING != AGENCY

ACTUATION != FREE_WILL

DEFORMATION_PASS != SCIENTIFIC_VALIDATION

3D_ASSET != CONSCIOUSNESS
```

## Final repository rule

```text
KEEP_PR_191_CLOSED = YES
OPEN_NEW_PR = NO
MERGE = NO
WRITE_TO_MAIN = NO
CANONICAL_EFFECT = NONE
```

Any deviation requires a new explicit Human Owner instruction.
