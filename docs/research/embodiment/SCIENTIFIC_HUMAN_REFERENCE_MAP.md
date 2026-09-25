# Scientific Human Reference Map

Status: `REFERENCE DESIGN / DRAFT`  
Canonical effect: `NONE`

## Purpose

This map prevents two opposite errors:

1. treating a minimal runtime abstraction as if it were a biologically complete human model;
2. forcing the runtime to simulate every known biological layer before the research question requires it.

Each layer is therefore tracked separately as a scientific reference, an abstraction candidate and a possible runtime dependency.

## Cross-cutting population and biological variability

No single body, donor, mesh, simulator or parameter set is treated as the universal human reference.

The map should track, where relevant:

- subject count;
- age;
- sex/anatomical configuration;
- body size / anthropometry;
- population provenance;
- specimen/donor-specific features;
- pathology or health-state assumptions;
- laterality / handedness where material;
- model calibration population.

```text
ONE_REFERENCE_BODY != HUMAN_POPULATION
ONE_MALE_MODEL != UNIVERSAL_MALE_BODY
ONE_FEMALE_MODEL != UNIVERSAL_FEMALE_BODY
REFERENCE_GEOMETRY != POPULATION_DISTRIBUTION
```

A future runtime may intentionally instantiate one bounded body profile. That engineering choice must remain distinct from claims about human population anatomy.

## Reference layers

| Layer | Reference target | Initial candidate sources | Default runtime disposition |
| --- | --- | --- | --- |
| L0 | morphology / surface geometry | SOMA-X and comparable parametric body models | minimal representation allowed |
| L1 | skeleton / joints / segments | SOMA-X; Visible Human / BoneHub | likely required in normalized form |
| L2 | musculoskeletal biomechanics | OpenSim / Rajagopal-family models | conditional |
| L3 | neural / sensorimotor / sensory organization | neuroscience, biomechanics and validated sensory-system references | likely required functionally |
| L4 | organ topology / soft tissue | Visible Human; BodyParts3D | reference first |
| L5 | circulation / respiration / metabolism | physiology literature / validated models | conditional |
| L6 | interoception / homeostasis / allostasis | literature + existing repository regulatory-state work | high research priority |
| L7 | endocrine / immune / autonomic coupling | literature / validated models | reference required, runtime conditional |
| L8 | tissues / extracellular matrix | anatomy / histology references | reference required, runtime conditional |
| L9 | cells | cell biology references | reference required, runtime conditional |
| L10 | proteins / molecular mechanisms | molecular biology references | reference required, runtime conditional |
| L11 | gene expression / regulation | genomics / systems biology references | reference required, runtime conditional |

## Cross-cutting environmental coupling

Embodiment is not defined by an isolated body alone. Reference coverage must record the environment variables that materially constrain or stimulate the body, including where relevant:

- gravity;
- contact / support surfaces;
- collision;
- temperature;
- external forces;
- resource availability;
- sensory stimulus structure.

```text
BODY_MODEL_WITHOUT_ENVIRONMENT
!= COMPLETE_EMBODIMENT_REFERENCE
```

The runtime may use simplified environments, but matched full ↔ minimal comparisons must hold environmental conditions fixed unless environment is the experimental variable.

## Cross-cutting temporal biology

Reference coverage should also record processes that alter the body across time:

- development / maturation;
- adaptation and plasticity;
- tissue repair;
- recovery;
- aging;
- accumulated fatigue / damage.

These processes are reference dimensions. They enter runtime only when required by a bounded research claim.

## Neural and sensory reference coverage

The neural/sensory layer should distinguish, where relevant:

- central nervous system;
- peripheral nervous system;
- autonomic nervous system;
- motor pathways;
- proprioception;
- vestibular sensing;
- touch / mechanoreception;
- nociception;
- thermoreception;
- vision;
- audition;
- olfaction;
- gustation;
- chemoreception and internal sensing.

A computational sensor channel is not equivalent to biological sensation or phenomenal experience.

## Completeness definitions

```text
REFERENCE_COMPLETE
= important layer, terminology, dependency, source and limitation are recorded

MODEL_COMPLETE
= layer has an executable or computable abstraction

BIOPHYSICAL_COMPLETE
= model approaches relevant physical/biological detail for the target claim
```

These are not interchangeable.

Reference completeness means cross-layer scientific coverage for the research question. It does not require enumerating every human cell, every protein molecule, every molecular species or every gene-expression event.

```text
REFERENCE_COMPLETE != EXHAUSTIVE_BIOLOGICAL_ENUMERATION
REFERENCE_MAP != MOLECULE_BY_MOLECULE_DIGITAL_HUMAN
```

## Representation cautions

External models encode modeling conventions.

Examples:

```text
SOMA-X JOINT COUNT
!= COMPLETE HUMAN ANATOMICAL JOINT COUNT

BONEHUB SEGMENTATION POLICY
!= UNIVERSAL BIOLOGICAL PARTITION

OPENSIM BODY
!= ANATOMICAL BONE

MUSCLE ACTUATOR
!= COMPLETE MUSCLE PHYSIOLOGY
```

Every source must therefore record:

- what the source represents;
- what it omits;
- its coordinate conventions;
- segmentation or topology conventions;
- applicable population and subject count;
- sex / age assumptions where relevant;
- donor/subject provenance and access terms where relevant;
- validation status;
- license;
- exact source version or revision;
- suitability for runtime versus reference-only use.

## Functional bridges of highest research priority

The current AI subjectivity-possibility research line prioritizes functional bridges over exhaustive molecular fidelity:

1. body geometry and action constraints;
2. sensorimotor closed loop;
3. proprioception;
4. interoception;
5. body-state regulation;
6. homeostatic pressure;
7. energy / recovery;
8. fatigue or damage;
9. bidirectional body-state ↔ decision coupling.

This does not exclude lower biological levels.

```text
CELLULAR_REFERENCE = REQUIRED
CELLULAR_RUNTIME = CONDITIONAL

PROTEIN_REFERENCE = REQUIRED
PROTEIN_RUNTIME = CONDITIONAL
```

## Cross-scale admission rule

A lower biological layer should enter the active runtime only when all of the following hold:

1. the higher-level abstraction fails reproducibly;
2. the failure matters to the target research phenomenon;
3. a lower-level mechanism plausibly distinguishes competing explanations;
4. the added detail produces a testable prediction;
5. the added layer can be bounded and provenance-traced;
6. the added layer does not silently redefine the scientific claim.

## Reference-source classes

### Geometry / pose

Preferred role: runtime representation candidate.

Candidate:
- NVIDIA SOMA-X.

Use:
- canonical pose representation;
- joint hierarchy;
- transforms;
- body geometry abstraction.

Do not infer:
- anatomical completeness;
- biological sensorimotor validity;
- phenomenology.

### Skeletal anatomy

Preferred role: scientific reference and crosswalk validation.

Candidates:
- NLM Visible Human;
- BoneHub Visible Human full-skeleton models.

Use:
- bone identity;
- geometry;
- skeletal relations;
- anatomy crosswalk.

Do not automatically vendor large meshes or CT-derived artifacts into the main repository.

### Musculoskeletal biomechanics

Preferred role: actuator, joint, force and movement reference.

Candidates:
- OpenSim;
- Rajagopal-family full-body models.

Use:
- degrees of freedom;
- joint coordinates;
- muscle/actuator abstractions;
- dynamics constraints.

Do not equate a simulator actuator with the complete biological muscle.

### Dynamics

Preferred role: validation dataset.

Candidate:
- ImDy.

Use:
- inverse-dynamics comparison;
- motion ↔ force/torque validation;
- held-out dynamics evaluation.

Initial disposition:
`EXTERNAL_PINNED_REFERENCE`.

### Organ / soft-tissue topology

Candidates:
- Visible Human;
- BodyParts3D.

Use:
- organ hierarchy;
- spatial relation;
- terminology.

Initial disposition:
reference first.

## Repository crosswalk

Current repository material already includes:

- embodiment candidate structures;
- AION/Astra individual runtime binding;
- interoception and homeostasis source concepts;
- latent regulatory-state discovery protocol.

Known current gap classes include:

- no repository-wide normalized human-body ontology;
- no proprioception implementation in the embodiment candidate;
- no unified scientific-model intake pipeline;
- no cloud-agent body attachment protocol equivalent to the native AION/Astra lineage;
- no full ↔ minimal embodiment reduction harness.

These are design gaps, not proof of required implementation.

## Nonclaims

```text
REFERENCE_MAP != COMPLETE_HUMAN_SIMULATION
BIOLOGICAL_DETAIL != SUBJECTIVITY_EVIDENCE
FUNCTIONAL_REGULATION != FELT_STATE
FULL_BODY_REFERENCE != DIGITAL_HUMAN_PERSON
```
