# Normalized Human Body Ontology Specification

Status: `SCHEMA DESIGN / DRAFT`  
Canonical effect: `NONE`

## Objective

Provide a stable repository-level ontology that can map heterogeneous human-body models into common research concepts without pretending that their internal representations are biologically identical.

## Core principle

```text
COMMON ONTOLOGY
!= COMMON UPSTREAM REPRESENTATION
```

The ontology is an adapter boundary.

## Canonical concept classes

### Anatomical structure

- bone;
- joint;
- body segment;
- organ;
- tissue;
- muscle;
- tendon;
- ligament;
- fascia;
- cartilage;
- vessel;
- nerve;
- sensor / receptor class.

### Mechanical structure

- degree of freedom;
- coordinate;
- transform;
- mass / inertia;
- constraint;
- actuator;
- force;
- torque;
- contact surface.

### Sensory structure

- exteroceptive channel;
- proprioceptive channel;
- interoceptive channel;
- sensor uncertainty;
- observation latency;
- observation mask.

### Regulatory structure

- resource state;
- homeostatic target;
- regulatory error;
- fatigue;
- damage;
- recovery;
- perturbation;
- intervention.

## Minimum record structure

A normalized concept should support fields equivalent to:

```text
concept_id
concept_class
canonical_name
parent_concept_id
side
source_mappings[]
units
coordinate_frame
runtime_required
reference_only
provenance[]
limitations[]
```

## Source mapping structure

Each mapping should record:

```text
source_system
source_revision
source_identifier
source_semantics
mapping_type
transformation
confidence_or_status
evidence_reference
```

Mapping types may include:

- `EXACT`;
- `APPROXIMATE`;
- `AGGREGATED`;
- `SPLIT`;
- `DERIVED`;
- `UNMAPPED`;
- `CONFLICT`.

## Semantic non-equivalence rules

The following must never be collapsed without an explicit mapping:

```text
BONE != JOINT
JOINT != DOF
DOF != POSE_PARAMETER
BODY_SEGMENT != BONE
MUSCLE != ACTUATOR
SENSOR_VARIABLE != FELT_SENSATION
REGULATORY_VARIABLE != FELT_NEED
```

## Crosswalk examples

### Example: femur

```text
AION concept:
LEFT_FEMUR

Possible mappings:
BoneHub → left femur mesh / segmentation label
OpenSim → body/segment reference associated with femur
SOMA-X → nearest relevant segment/joint representation

Mappings may be exact, approximate or absent.
```

### Example: knee flexion

```text
AION concept:
RIGHT_KNEE_FLEXION

Possible mappings:
SOMA-X → pose parameter / joint transform
OpenSim → knee coordinate
BoneHub → geometry relationship only, not dynamic coordinate
```

No crosswalk may invent an equivalence that the source does not contain.

## Versioning

The ontology is versioned independently from source models.

```text
AION_ONTOLOGY_VERSION
!= SOMA_X_VERSION
!= OPENSIM_MODEL_VERSION
!= BONEHUB_DATASET_VERSION
```

Upstream changes require mapping review, not automatic ontology replacement.

## Runtime abstraction

A full ontology may contain many reference concepts while the active runtime exposes only a minimal projection.

```text
FULL ONTOLOGY
↓ projection
RUNTIME BODY STATE
↓ observation adapter
AGENT OBSERVATION
```

This makes richer future models replaceable without forcing agent interfaces to consume every source-specific field.

## Validation requirements

A normalized ontology implementation must eventually test:

- unique stable IDs;
- acyclic parent relations where required;
- valid side / laterality;
- units and coordinate metadata;
- source revision presence;
- mapping-type validity;
- no silent conflicting mappings;
- complete provenance for derived fields;
- deterministic extraction where generated from upstream.

## Nonclaims

```text
ONTOLOGY_COVERAGE != BIOLOGICAL_COMPLETENESS
MAPPING_EXISTS != EQUIVALENCE_PROVEN
COMMON_SCHEMA != COMMON_PHENOMENOLOGY
```
