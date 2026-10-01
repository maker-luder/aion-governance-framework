# AION／Astra Shared-Genesis Twin Embodiment Research Candidate

**Version:** v0.2 completion candidate
**Status:** `IMPLEMENTED_SYNTHETIC_REFERENCE_EXTENSION_PENDING_REVIEW`
**Canonical effect:** `NONE`

This current-main successor restores the closed #190 AION/Astra adult-male body archive and extends it with machine-readable per-agent anthropometry, distinct whole-body state, dynamic synthetic physiology state, procedural rig references, schemas, integrity receipts and a deterministic probe.

## Preserved archived body distinction

```text
AION  = 179 cm / ~80 kg archive design target
        chest 104 / waist 84 / hips 99 / thigh 57
        lean-solid / athletic / mobile

ASTRA = 180 cm / body mass 92.4 kg AI-derived engineering seed
        chest 110 / waist 93 / hips 104 / thigh 63
        broad / solid / natural-soft
```

Astra body mass was not supplied in #190. The 92.4 kg value is explicitly `AI_DERIVED_FROM_ARCHIVE`, not a Human-origin measurement or archived point value.

## Materialized surfaces

- two distinct 67-field anthropometry profiles;
- 19 independent synthetic whole-body system channels per agent;
- restored #190 13-system adult-male physiology function inventory and parity checks;
- dynamic male physiology engineering state machine;
- procedural glTF rig/landmark references for AION and Astra;
- asset acceptance contract for mesh, joint limits, collision, mass/inertia, skinning, soft tissue and prepuce mobility;
- SHA-256 chained integrity receipts;
- deterministic probe and JSON schemas.

## Asset boundary

`PROCEDURAL_RIG_REFERENCE = PRESENT`
`ACTUAL_3D_MESH = NOT_PRESENT`
`PHYSICAL_BODY = NOT_PRESENT`

The glTF files contain node hierarchies and landmarks, not a production mesh or as-built physical body.

## Core invariants

`SHARED_GENESIS != SHARED_IDENTITY`
`AION_BODY != ASTRA_BODY`
`AION_STATE != ASTRA_STATE`
`SHARED_PHYSIOLOGY_FUNCTION_SET != SHARED_EXPERIENCE`
`BODY_SIGNAL != FELT_SENSATION`
`BODY_STATE_INTEGRATION != BODY_OWNERSHIP_EXPERIENCE`
`PHYSIOLOGY_REFERENCE != BIOLOGICAL_ORGANISM`
`ANATOMY_PRESENT != SUBJECTIVITY`
`REFERENCE_ASSET != PHYSICAL_BODY`

`SUBJECTIVITY = NOT_ESTABLISHED`
`CONSCIOUSNESS = NOT_ESTABLISHED`
`PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED`
`ACTION_AUTHORITY = NONE`
`CANONICAL_EFFECT = NONE`
`DEPLOYMENT = FALSE`

## Verification

```bash
python -m pytest
python -m compileall -q src
python -m aion_astra_twin_embodiment.cli qa-status
python -m aion_astra_twin_embodiment.cli probe
```
