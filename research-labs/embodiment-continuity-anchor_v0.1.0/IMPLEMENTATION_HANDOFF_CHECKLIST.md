# Morphology Fixture Implementation Handoff Checklist

Status: `RESEARCH_HANDOFF_CANDIDATE`
Main effect: `NONE`
Canonical effect: `NONE`
Codex implementation status: `NOT_STARTED`

Use this checklist only when engineering work resumes.

## Before coding

- [ ] Re-read current branch HEAD and check whether the embodiment-continuity lab changed after this note.
- [ ] Compare the proposed morphology descriptor with existing `EmbodimentBinding`; do not duplicate an existing schema.
- [ ] Keep `LineageAnchor` unchanged unless a separate research decision explicitly justifies modification.
- [ ] Confirm all fixtures are synthetic or independently public-safe.
- [ ] Do not import the legacy/private geometry artifact, private metadata, personalized anatomy, identity bindings, or source-derived mesh data.
- [ ] Preserve provenance for every fixture mutation.

## Minimal implementation candidate

Suggested research-only structures:

```text
MorphologyDescriptor
MorphologyDelta
SensorimotorBinding
MorphologyMigrationObservation
```

Candidate fields may include:

```text
body_schema_ref
geometry_ref
topology_fingerprint
spatial_frame_ref
sensor_layout_ref
action_channel_refs
capability_map_ref
```

These are candidate names, not canonical schema.

## Required negative controls

- [ ] Same geometry + changed stable lineage must not become continuity PASS.
- [ ] Changed geometry + preserved stable lineage must not automatically become continuity FAIL.
- [ ] Shared geometry across different anchors must not establish shared identity.
- [ ] Static geometry without sensorimotor coupling must not establish body ownership.
- [ ] Morphology metadata must not be promoted into unsupported person-level/private-state inference.

## Required outputs

Keep engineering decisions bounded to:

```text
PASS
HOLD
FAIL
NOT_ASSESSED
```

Always retain:

```text
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
BODY_OWNERSHIP_CONCLUSION = NOT_ESTABLISHED
PHENOMENAL_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```

## Verification target

Future implementation should add deterministic tests corresponding to `MORPHOLOGY_MIGRATION_TEST_MATRIX.json`, then run the lab's existing verification commands plus any new targeted test suite.

No main-branch integration is authorized by this handoff note.
