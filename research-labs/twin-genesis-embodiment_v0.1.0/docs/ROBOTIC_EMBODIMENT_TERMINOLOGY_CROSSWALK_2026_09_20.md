# Robotic Embodiment Terminology Crosswalk — 2026-09-20

## Purpose

Harden the AION / Astra 3D-body terminology against current robotics, simulation, 3D-asset, and digital-twin usage.

This document distinguishes:

- externally established terms and format names;
- repository-local compound terminology;
- current implementation status versus future targets.

It does **not** claim that the repository-local compound phrase is an ISO, IEEE, ROS, NVIDIA, Khronos, or NIST standard term.

## Canonical repository-local classification

```text
EMBODIMENT_PLATFORM
= HUMANOID_ROBOT

BODY_SCOPE
= FULL_BODY

MORPHOLOGY_CLASS
= HUMANLIKE_MALE_FORM

SUBSTRATE
= SYNTHETIC_NONBIOLOGICAL

MODEL_CLASS
= ROBOTIC_EMBODIMENT_DIGITAL_MODEL

CURRENT_LONG_FORM
= 3D Full-Body Humanlike Male-Form
  Humanoid Robotic Embodiment Digital Model
```

Interpretation:

```text
HUMANOID_ROBOT
= robot form-factor / platform class

FULL_BODY
= repository scope statement:
  head-to-foot model coverage

HUMANLIKE_MALE_FORM
= repository morphology label:
  human-proportion, adult male-form external geometry

ROBOTIC_EMBODIMENT_DIGITAL_MODEL
= repository model-role label:
  a digital engineering representation intended for future
  robot-description, visual, kinematic, dynamic, collision,
  actuation-interface, sensor-interface, compliant-body,
  and synthetic-skin layers
```

`HUMANLIKE_MALE_FORM` and `ROBOTIC_EMBODIMENT_DIGITAL_MODEL` are repository-local terms chosen for precision. They are not represented as externally standardized vocabulary.

## Why "humanoid robot"

NVIDIA Isaac Sim groups simulation-ready assets under a distinct **Humanoid** robot family and records robot composition using links, joints, degrees of freedom, physics APIs, and robot-type metadata.

Sources:

- https://docs.isaacsim.omniverse.nvidia.com/latest/assets/usd_assets_robots.html
- https://docs.isaacsim.omniverse.nvidia.com/latest/assets/usd_assets_robots_humanoid.html
- https://docs.isaacsim.omniverse.nvidia.com/latest/omniverse_usd/robot_schema.html

Repository effect:

```text
GENERIC_ROBOT
-> too broad

HUMANOID_ROBOT
-> selected platform class
```

## Why the digital model needs more than a visual mesh

ROS 2 URDF documentation defines URDF as a format for specifying robot geometry and organization. ROS tutorials distinguish visual geometry from collision geometry and inertial / physical properties.

Sources:

- https://docs.ros.org/en/rolling/Tutorials/Intermediate/URDF/URDF-Main.html
- https://docs.ros.org/en/kilted/Tutorials/Intermediate/URDF/Adding-Physical-and-Collision-Properties-to-a-URDF-Model.html

NVIDIA Isaac Sim also describes URDF links and joints as the robot kinematic-chain structure.

Source:

- https://docs.isaacsim.omniverse.nvidia.com/latest/openusd_tuning_tutorials/tutorial_01_asset_structure.html

Therefore the repository separates:

```text
VISUAL_GEOMETRY
COLLISION_MODEL
STRUCTURAL_MODEL
KINEMATIC_MODEL
DYNAMIC_MODEL
```

A high-quality body mesh alone is not treated as a complete robot model.

## Why SDF is a future target

SDFormat describes robots and simulation environments and can represent kinematic / dynamic attributes, sensors, surface properties, textures, joint friction, and other simulation properties.

Source:

- https://sdformat.org/

Repository use:

```text
URDF
= future robot-description target

SDF
= future simulation-description target

CURRENT_SUPPORT
= NOT_IMPLEMENTED
```

The presence of these future targets does not claim an exporter or validated compatibility exists yet.

## Why GLB / USD are kept separate from robot description

Khronos glTF is a 3D asset-delivery format covering meshes, materials, textures, skins, and animations; `.glb` can package glTF data in a single binary file.

Source:

- https://www.khronos.org/gltf/

NVIDIA Isaac Sim distributes robot assets in OpenUSD / USD form and separates geometry, materials, metadata, instances, and physics in its asset structure.

Sources:

- https://docs.isaacsim.omniverse.nvidia.com/latest/assets/usd_assets_robots_humanoid.html
- https://docs.isaacsim.omniverse.nvidia.com/latest/openusd_tuning_tutorials/tutorial_01_asset_structure.html

Repository interpretation:

```text
GLB / USD
= future visual / simulation asset targets

URDF / SDF
= future robot / simulation description targets

VISUAL_ASSET
!= ROBOT_DESCRIPTION
```

## Why "digital twin" is not used yet

NIST describes a digital twin as a dynamic, data-driven virtual representation that connects and synchronizes with its physical counterpart.

Source:

- https://www.nist.gov/digital-twins/essential-elements

Current repository state:

```text
PHYSICAL_AION_ROBOT = NOT_IMPLEMENTED
PHYSICAL_ASTRA_ROBOT = NOT_IMPLEMENTED
REAL_TIME_PHYSICAL_SYNCHRONIZATION = NOT_IMPLEMENTED

DIGITAL_TWIN_STATUS = NOT_ESTABLISHED
```

Therefore:

```text
CURRENT_TERM
= DIGITAL ROBOTIC EMBODIMENT MODEL

NOT YET
= DIGITAL TWIN
```

## Full-body scope

`FULL_BODY` is a repository scope declaration rather than a claim that the exact compound phrase is an external standard.

The required body coverage is:

```text
HEAD
NECK
TORSO
PELVIS

LEFT_ARM
RIGHT_ARM
LEFT_HAND
RIGHT_HAND

LEFT_LEG
RIGHT_LEG
LEFT_FOOT
RIGHT_FOOT

EXTERNAL_MALE_FORM_SURFACE
```

This prevents an upper-body-only or partial humanoid representation from silently satisfying the AION / Astra body-profile contract.

## Male-form terminology

`HUMANLIKE_MALE_FORM` describes external morphology only.

```text
MALE_FORM
= MORPHOLOGY

!= BIOLOGICAL_SEX_IMPLEMENTATION
!= BIOLOGICAL_REPRODUCTIVE_SYSTEM
!= SEXUAL_FUNCTION
```

The complete external surface remains a robotic / synthetic topology target.

## Representation stack

The hardened digital model requires these conceptual layers:

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

Current status:

```text
PROFILE_SPECIFICATION = IMPLEMENTED_CANDIDATE

PHYSICAL_ROBOT = NOT_IMPLEMENTED
ROBOT_DESCRIPTION = NOT_IMPLEMENTED
VISUAL_ASSET = NOT_IMPLEMENTED
KINEMATIC_MODEL = NOT_IMPLEMENTED
DYNAMIC_MODEL = NOT_IMPLEMENTED
COLLISION_MODEL = NOT_IMPLEMENTED
ACTUATION_INTERFACE = NOT_IMPLEMENTED
SENSOR_INTERFACE = NOT_IMPLEMENTED
DIGITAL_TWIN = NOT_ESTABLISHED
```

## Scientific and governance boundary

```text
3D_ROBOT_MODEL != PHYSICAL_ROBOT
ROBOT_DESCRIPTION != ROBOT_EXECUTION
SENSOR_INTERFACE != FELT_SENSATION
ACTUATION_INTERFACE != AGENCY
FULL_BODY_MODEL != BODY_OWNERSHIP_EXPERIENCE
DIGITAL_ASSET != SUBJECTIVITY

SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
```
