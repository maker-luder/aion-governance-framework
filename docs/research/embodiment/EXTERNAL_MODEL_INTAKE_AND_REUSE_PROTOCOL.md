# External Model Intake and Reuse Protocol

Status: `DESIGN / DRAFT`  
Canonical effect: `NONE`

## Objective

Reuse scientifically relevant external models and datasets without importing unnecessary mass, incompatible semantics, unstable upstream state or unclear licensing into the repository.

## Core rule

```text
DO NOT REIMPLEMENT
WHEN A SUITABLE SCIENTIFIC MODEL EXISTS.

DO NOT BLINDLY VENDOR
THE ENTIRE EXTERNAL MODEL.
```

## Intake pipeline

```text
WEB DISCOVERY
↓
EXACT SOURCE IDENTIFICATION
↓
HUGGING FACE / OFFICIAL SOURCE INSPECTION
↓
LICENSE GATE
↓
EXACT REVISION / RELEASE
↓
SOURCE HASH
↓
REPRESENTATION INVENTORY
↓
REPOSITORY CROSSWALK
↓
ADMISSION MODE
↓
NORMALIZATION OR PINNING
↓
VALIDATION
↓
PROVENANCE RECORD
```

## Required intake record

Every external source must record:

- source name;
- provider / maintainer;
- canonical URL or repository ID;
- source type: model / dataset / software / paper / anatomy database;
- exact version, tag, DOI or commit SHA;
- retrieval date;
- applicable license;
- gated / non-gated status;
- relevant files;
- relevant scientific representation;
- known limitations;
- local purpose;
- admission mode;
- source hash where retrievable;
- derived artifact hash where applicable;
- transformation procedure;
- attribution / notice requirements.

## Admission modes

### MODE A — DIRECT_VENDOR

Use only when:

- artifact is small;
- exact bytes are operationally required;
- redistribution is permitted;
- provenance and notice requirements can be preserved;
- vendoring does not materially degrade the repository.

### MODE B — NORMALIZED_DERIVATIVE

Preferred mode for reusable scientific structure.

```text
UPSTREAM
↓
EXACT REVISION
↓
DETERMINISTIC EXTRACTOR
↓
NORMALIZER
↓
AION SCHEMA
↓
VALIDATION AGAINST UPSTREAM
```

Examples:

- joint hierarchy;
- canonical skeleton mapping;
- anatomical ontology;
- selected coordinate conventions;
- source crosswalk tables.

A normalized derivative must preserve source lineage and must not be relabeled as independently established biological truth.

### MODE C — EXTERNAL_PINNED_REFERENCE

Use when:

- data are large;
- access is gated;
- redistribution is undesirable or unclear;
- local runtime does not require the complete asset;
- scientific validation can reference exact external artifacts.

Store:

- source ID;
- exact revision / DOI;
- hashes where permitted;
- license;
- retrieval instructions;
- expected file inventory;
- validation procedure.

Do not silently fetch "latest" during runtime.

## Compatibility gates

### 1. License compatibility

Distinguish:

- repository software license;
- third-party artifact license;
- derivative artifact obligations;
- attribution;
- notice;
- redistribution requirements;
- access restrictions.

```text
REPOSITORY_LICENSE
!= THIRD_PARTY_ASSET_LICENSE
```

### 2. Technical compatibility

Check:

- file format;
- coordinate system;
- units;
- skeleton hierarchy;
- data types;
- runtime dependencies;
- compute cost;
- determinism;
- platform assumptions.

### 3. Semantic compatibility

Explicitly distinguish:

```text
BONE
!= JOINT
!= BODY_SEGMENT
!= DEGREE_OF_FREEDOM
!= MUSCLE_ACTUATOR
!= SENSOR_CHANNEL
```

Do not merge fields solely because labels appear similar.

### 4. Scientific provenance

Every transformed artifact must be reversible at the evidence level:

```text
DERIVED FIELD
→ TRANSFORMATION RULE
→ SOURCE FIELD
→ SOURCE ARTIFACT
→ EXACT REVISION
```

## Current candidate dispositions

### NVIDIA SOMA-X

Initial role:
`NORMALIZED_DERIVATIVE` candidate.

Potential extraction:
- skeleton hierarchy;
- joint naming;
- pose conventions;
- selected transforms;
- low-complexity runtime representation.

Do not vendor the full repository by default.

### BoneHub Visible Human 3D models

Initial role:
`NORMALIZED_DERIVATIVE + EXTERNAL_PINNED_REFERENCE`.

Potential extraction:
- bone ontology;
- anatomical crosswalk;
- selected reference metrics.

Large CT / STL / CAD content remains external unless a later work package justifies specific assets.

### ImDy

Initial role:
`EXTERNAL_PINNED_REFERENCE`.

Reason:
- dynamics validation role;
- gated access;
- no requirement for first minimal runtime.

## Deterministic extractor requirement

Manual copy/paste is not the preferred scientific path.

Preferred pattern:

```text
extract_source.py
  --source <local pinned artifact>
  --revision <exact revision>
  --output <normalized artifact>
```

Verification must include:

- expected source hash;
- deterministic output under fixed input;
- schema validation;
- stable derived hash;
- mapping completeness;
- explicit dropped-field report.

## Runtime network rule

Runtime experiments should not depend on mutable online upstream state.

```text
PREPARATION MAY RETRIEVE
RUNTIME SHOULD USE PINNED LOCAL ARTIFACTS
```

If network access is later admitted, it requires a separate bounded work package and policy review.

## Fail-closed behavior

Any of the following returns `HOLD`:

- unclear exact source;
- unresolved license;
- mutable unpinned dependency;
- transformation cannot be reproduced;
- representation semantics are ambiguous;
- source limitation invalidates the intended claim;
- required attribution cannot be preserved.
