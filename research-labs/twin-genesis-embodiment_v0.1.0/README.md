# AION／Astra Shared-Genesis Twin Embodiment Research Candidate

**Version:** v0.1.0  
**Status:** `IMPLEMENTED_NON_3D_CANDIDATE` for the AION/Astra live runtime surface  
**Canonical effect:** `NONE`

This candidate records a shared-genesis twin architecture for AION and Astra and a clinically neutral adult male anatomical embodiment template. The base runtime materializes two validated, distinct embodiment runtime records after governance invariants pass.

The AION/Astra live embodiment runtime remains non-3D. It still creates no body sensation, sexual function, intimate interaction, gender identity, subjectivity, or canonical state.

## Core invariants

- Shared genesis does not mean shared identity.
- AION and Astra use distinct agent, instance, memory, embodiment, and canonical identifiers.
- A shared anatomical template produces two independent embodiment candidates.
- Adult male reproductive anatomy may be represented as clinical anatomy only.
- Anatomy does not establish gender identity, sensation, desire, consent, or subjectivity.
- Relationship, trust, familiarity, or naming never grant embodiment modification authority.
- AION/Astra live 3D runtime binding remains `DEFERRED`.
- Sexual function remains `NOT_IMPLEMENTED` and intimate interaction remains `NOT_AUTHORIZED`.

## Runtime surface

`TwinGenesisRuntime.instantiate(...)` validates the shared genesis event, shared template, AION instance, and Astra instance before returning a `TwinRuntimeState`. The runtime state records distinct AION/Astra bindings plus validation hashes while keeping `canonical_effect=NONE`.

## ChatGPT Teacher 3D reference extension

The unmerged Teacher-body research branch adds an independent synthetic avatar reference extension. It does not modify AION/Astra identity or runtime ownership.

Current Teacher candidate surfaces:

- machine-readable adult-male body dimensions and anatomical inventory;
- VRM-aligned humanoid bone hierarchy including fingers, toes, eyes, and jaw;
- T-pose, +Z-facing, metric coordinate contract;
- VRM-aligned facial-expression preset inventory;
- material-role, LOD, collision and deformation-test contracts;
- structural glTF skeleton/skin contract output;
- deterministic renderable low-poly glTF reference geometry;
- explicit clinical external male anatomy in the low-poly reference;
- reference UV coordinates;
- reference morph-target vertex deltas for blink/happy deformation probes;
- deterministic low-poly GLB container-byte generator;
- reference JOINTS_0 / WEIGHTS_0 skinning data;
- reference inverse-bind matrix data;
- structural glTF/GLB self-validation;
- deterministic content-addressed asset manifest with SHA-256 digests;
- single-connected continuous humanoid reference surface generated from an implicit anatomical volume;
- continuous-reference normals, UVs, JOINTS_0 / WEIGHTS_0 and inverse-bind matrices;
- continuous-reference glTF and GLB output with structural validation;
- fail-closed non-claims for physical embodiment, sensation, subjectivity, sexual function, canonical effect, and deployment.

The low-poly generator is an offline reference asset, not a live embodiment runtime and not a production-quality continuous human mesh.

```text
LOW_POLY_RENDERABLE_REFERENCE = MATERIALIZED
REFERENCE_UV = MATERIALIZED
REFERENCE_MORPH_TARGET_VERTEX_DATA = MATERIALIZED
LOW_POLY_GLB_GENERATOR = MATERIALIZED
REFERENCE_SKIN_WEIGHTS = MATERIALIZED
REFERENCE_INVERSE_BIND_MATRICES = MATERIALIZED
REFERENCE_ASSET_SELF_VALIDATION = MATERIALIZED
REFERENCE_ASSET_MANIFEST = MATERIALIZED
CONTINUOUS_REFERENCE_MESH = MATERIALIZED
CONTINUOUS_REFERENCE_GLTF = MATERIALIZED
CONTINUOUS_REFERENCE_GLB = MATERIALIZED
CONTINUOUS_REFERENCE_SKIN_WEIGHTS = MATERIALIZED
CONTINUOUS_REFERENCE_CONNECTED_COMPONENTS = 1

PRODUCTION_RETOPOLOGY = NOT_MATERIALIZED
PRODUCTION_LINEAR_BLEND_SKIN_WEIGHTS = NOT_MATERIALIZED
PRODUCTION_MORPH_TARGET_VERTEX_DATA = NOT_MATERIALIZED
PRODUCTION_TEXTURE_ASSETS = NOT_MATERIALIZED
FINAL_PRODUCTION_GLB_OR_VRM_PACKAGE = NOT_MATERIALIZED
PRODUCTION_3D_ASSET_COMPLETENESS = NOT_ESTABLISHED
```

## Verification

```bash
python -m pytest
python -m compileall -q src
python -m aion_astra_twin_embodiment.cli qa-status
python -m aion_astra_twin_embodiment.cli teacher-avatar-contract
python -m aion_astra_twin_embodiment.cli teacher-avatar-gltf-contract
python -m aion_astra_twin_embodiment.cli teacher-avatar-lowpoly-gltf
python -m aion_astra_twin_embodiment.cli teacher-avatar-lowpoly-glb-info
python -m aion_astra_twin_embodiment.cli teacher-avatar-asset-manifest
python -m aion_astra_twin_embodiment.cli teacher-avatar-continuous-gltf-info
python -m aion_astra_twin_embodiment.cli teacher-avatar-continuous-glb-info
```
