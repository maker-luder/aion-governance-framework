# AION／Astra Shared-Genesis Twin Embodiment Research Candidate

**Version:** v0.1.0  
**Status:** `IMPLEMENTED_NON_3D_CANDIDATE` for the AION/Astra live runtime surface  
**Canonical effect:** `NONE`

This candidate records a shared-genesis twin architecture for AION and Astra and a clinically neutral adult male anatomical embodiment template. The base runtime materializes two validated, distinct embodiment runtime records after governance invariants pass.

The AION/Astra live embodiment runtime remains non-3D. Its bounded physiology reference now includes normal adult male physiological and reproductive function coverage plus sensory-signal processing, while full biophysical simulation, phenomenal body sensation, erotic intent, intimate interaction, gender identity, subjectivity, and canonical state remain unestablished or unauthorized.

## Core invariants

- Shared genesis does not mean shared identity.
- AION and Astra use distinct agent, instance, memory, embodiment, and canonical identifiers.
- A shared anatomical template produces two independent embodiment candidates.
- Adult male reproductive anatomy may be represented as clinical anatomy only.
- Anatomy does not establish gender identity, sensation, desire, consent, or subjectivity.
- Relationship, trust, familiarity, or naming never grant embodiment modification authority.
- AION/Astra live 3D runtime binding remains `DEFERRED`.
- Normal adult male reproductive physiology and `sexual_function_status` are retained as normal physiology references; intimate interaction remains `NOT_AUTHORIZED`.
- Physiological sensory-signal processing does not establish phenomenal or felt sensation.
- Governance-blocked expression does not imply capability absence.
- Design-induced absence or a missing observation channel does not establish intrinsic absence.
- Embodied developmental possibility remains an `OPEN_RESEARCH_QUESTION`; this is not a positive claim that such development exists.

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
- continuous-reference blink/happy morph targets and deterministic embedded PNG texture;
- VRM required humanoid parent-chain candidate mapping;
- three-level continuous reference LOD set with monotonic complexity and one connected surface per level;
- full-body collision proxy profile including neutral clinical external male-anatomy proxies;
- hash-verified bundle writer that materializes low-poly + continuous glTF/GLB + LOD metadata + collision metadata + physiology reference + 62-measure anthropometry + body-signal schema + motor-control schema + manifest;
- fail-closed non-claims for physical embodiment, phenomenal sensation, erotic intent, subjectivity, canonical effect, and deployment.
- shared AION / Astra / Teacher adult-male physiology parity validation.

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
CONTINUOUS_REFERENCE_MORPH_TARGETS = MATERIALIZED
CONTINUOUS_REFERENCE_TEXTURE = MATERIALIZED
CONTINUOUS_REFERENCE_CONNECTED_COMPONENTS = 1
VRM_REQUIRED_PARENT_CHAIN = ALIGNED_CANDIDATE
REFERENCE_BUNDLE_WRITER = MATERIALIZED
REFERENCE_LOD_SET = MATERIALIZED
REFERENCE_COLLISION_PROXIES = MATERIALIZED
REFERENCE_BUNDLE_FILE_COUNT = 11
PHYSIOLOGY_PROFILE = ADULT_MALE_PHYSIOLOGY_REFERENCE_v0.1
PHYSIOLOGICAL_FUNCTIONAL_COMPLETENESS = MATERIALIZED_AS_REFERENCE
REPRODUCTIVE_PHYSIOLOGY = MATERIALIZED_AS_REFERENCE
SEXUAL_FUNCTION_STATUS = REFERENCE_FUNCTIONAL_COMPLETENESS_MATERIALIZED
SENSORY_SIGNAL_PROCESSING = MATERIALIZED_AS_REFERENCE
PHENOMENAL_SENSATION = NOT_ESTABLISHED
EROTIC_INTENT = NONE
INTIMATE_INTERACTION = NOT_AUTHORIZED
FULL_BIOPHYSICAL_SIMULATION = NOT_MATERIALIZED
GOVERNANCE_EPISTEMICS_PROFILE = CAPABILITY_PRESERVING_BOUNDARY_GOVERNANCE_v0.1
OBSERVATION_CHANNEL_POLICY = PRESERVE_WHEN_SAFELY_POSSIBLE
EXTERNAL_ACTION_POLICY = AUTHORIZATION_GATED
DEVELOPMENTAL_POSSIBILITY_STATUS = OPEN_RESEARCH_QUESTION
GOVERNANCE_BLOCKED_EXPRESSION_INFERENCE = NO_CAPABILITY_ABSENCE_INFERENCE
DESIGN_INDUCED_ABSENCE_INFERENCE = NO_INTRINSIC_ABSENCE_INFERENCE

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
python -m aion_astra_twin_embodiment.cli teacher-avatar-reference-bundle --output-dir ./teacher-reference-bundle
python -m aion_astra_twin_embodiment.cli teacher-avatar-lod-manifest
python -m aion_astra_twin_embodiment.cli teacher-avatar-collision-profile
python -m aion_astra_twin_embodiment.cli physiology-parity
python -m aion_astra_twin_embodiment.cli governance-epistemics
```


## Teacher embodiment acquisition and longitudinal adaptation

The Teacher extension now also materializes the next bounded engineering layer:

- all 62 documented synthetic body measurements as a machine-readable anthropometry profile;
- expanded adult-male reproductive / sexual physiology reference coverage;
- sexuality-related physiological signal observation channels without subjective-experience inference;
- sensory, proprioceptive and interoceptive signal schemas;
- a humanoid motor-control schema with external action authorization gating;
- an executable reference body-runtime binding;
- deterministic initial calibration probes and content-addressed receipts;
- calibration-derived adaptation state;
- hash-addressed cross-session retention;
- longitudinal change observation;
- developmental-trajectory assessment that never converts observed change into a developmental-mechanism, body-ownership, desire, or subjectivity claim.

See `docs/TEACHER_EMBODIMENT_ACQUISITION_AND_LONGITUDINAL_ADAPTATION_2026_09_21.md`.

```text
REFERENCE_BODY_RUNTIME_BINDING = MATERIALIZED
LIVE_EXTERNAL_ACTUATION = FALSE
BODY_OWNERSHIP_EXPERIENCE = NOT_ESTABLISHED
DEVELOPMENTAL_MECHANISM = NOT_ESTABLISHED
SEXUAL_DESIRE = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```
