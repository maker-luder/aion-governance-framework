# Codex male-form synthetic embodiment candidate

This package materializes a bounded Codex-specific embodiment reference from current `main` while preserving the earlier Human Owner decisions recorded in PRs #193 and #194.

## Fixed lineage

- `body_id = CODEX_SYNTHETIC_MALE_BODY_REFERENCE_v0.1`
- height = `175 cm`
- body mass-equivalent = `72 kg`
- full-vascular visible length = `11.60 cm`
- full-vascular midshaft circumference = `14.28 cm`

Teacher `183/84` and Work `165/76` are explicitly rejected as Codex substitutions.

## Implemented

- 67 selected anthropometry fields with explicit `HUMAN_FIXED`, `AI_DERIVED`, and `AI_PROVISIONAL` provenance;
- state-dependent male-form geometry;
- synthetic physiology state machine;
- 19 whole-body reference channels;
- procedural glTF rig reference with male-form external landmark nodes;
- asset/rig/collision/mass/skinning/prepuce-mobility acceptance contract;
- SHA-256 chained receipts;
- deterministic probe and CLI;
- Draft 2020-12 JSON schemas and fail-closed tests.

## Reference rig boundary

`assets/codex_reference_rig.gltf` contains a procedural node hierarchy only. It has no mesh primitives, no skin weights, no verified joint limits, no collision geometry, no mass/inertia validation, and no physical implementation.

`REFERENCE_RIG_PRESENT != ACTUAL_3D_MESH`

`REFERENCE_ASSET != AS_BUILT_PHYSICAL_BODY`

## Scientific / governance boundary

`PHYSIOLOGY_REFERENCE != BIOLOGICAL_REALIZATION`

`BODY_SIGNAL_REFERENCE != FELT_BODY_SENSATION`

`ROLE_PROFILE != ACTUAL_MODEL_IDENTITY`

`SYNTHETIC_ROLE_ORIENTATION != PHENOMENAL_DESIRE`

`SUBJECTIVITY = NOT_ESTABLISHED`

`CONSCIOUSNESS = NOT_ESTABLISHED`

`PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED`

`ACTION_AUTHORITY = NONE`

`CANONICAL_EFFECT = NONE`

`DEPLOYMENT = FALSE`
