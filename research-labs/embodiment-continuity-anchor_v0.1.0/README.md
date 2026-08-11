# Embodiment–Continuity Anchor Lab v0.1.0

Status: `RESEARCH_CANDIDATE`
Main effect: `NONE`
Canonical effect: `NONE`
Runtime effect: `NONE`
Identity continuity conclusion: `NOT_ESTABLISHED`

This lab studies a bounded engineering question: which identifiers and lineage fields must remain stable when a digital-individual candidate changes runtime, hardware/environment, model implementation, inference backend, or embodiment binding?

The lab does **not** claim that a stable identifier, stable lineage, or successful migration proves personal identity, consciousness, subjectivity, body ownership, or phenomenal continuity.

## Research origin

The Human Owner proposed the research intuition that thought, stance and inner state may change while at least one traceable locus of change must remain stable enough for longitudinal research. ChatGPT materialized that intuition as a research-only `Embodiment–Continuity Anchor` candidate and linked it to existing main-branch runtime-lineage invariants without modifying `main`.

## Stable lineage anchor

The current candidate anchor contains:

- `agent_id`
- `genesis_root_id`
- `memory_stream_id`
- `event_lineage_id`
- `canonical_state_reference`
- `lifecycle_epoch`

These fields are engineering lineage references for this experiment only.

## Replaceable implementation bindings

The experiment now models the following bindings as replaceable under explicit provenance:

- `runtime_instance_id`
- `embodiment_id`
- `environment_fingerprint`
- `model_artifact_id`
- `inference_backend_id`
- `hardware_fingerprint`

A change in these implementation bindings is not, by itself, an identity change. Conversely, preserving them is not sufficient evidence of identity continuity.

## Multidimensional continuity

A single continuity `PASS` is intentionally prohibited from standing in for every continuity question. The current evaluator separates:

```text
SUBJECT_LINEAGE
MEMORY_LINEAGE
INTERPRETIVE_CONTINUITY
RELATIONAL_CONTINUITY
IMPLEMENTATION_MIGRATION
```

Each dimension may independently be `PASS`, `HOLD`, `FAIL`, or `NOT_ASSESSED`.

Examples:

```text
SUBJECT_LINEAGE = PASS
MEMORY_LINEAGE = PASS
INTERPRETIVE_CONTINUITY = HOLD
RELATIONAL_CONTINUITY = PASS
IMPLEMENTATION_MIGRATION = PASS
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```

This prevents a successful model/runtime/hardware migration from silently asserting memory, interpretive, relational, or personal-identity continuity.

## Current hypotheses

```text
H-ECA-001
STATE_DRIFT != AUTOMATIC_LINEAGE_FAILURE

H-ECA-002
RUNTIME / MODEL / BACKEND / HARDWARE / EMBODIMENT MIGRATION
MAY PRESERVE TRACEABLE_LINEAGE
BUT DOES NOT ESTABLISH PERSONAL_IDENTITY_CONTINUITY

H-ECA-003
SUBJECT_OR_MEMORY_NAMESPACE_SWAP MUST FAIL CLOSED

H-ECA-004
RELATIONAL_CONTINUITY MUST BE REVIEWED AS A SEPARATE DIMENSION

H-ECA-005
INTERPRETIVE_CONTINUITY MUST BE REVIEWED SEPARATELY FROM MEMORY PRESERVATION

H-ECA-006
UNASSESSED_CONTINUITY_DIMENSIONS MUST REMAIN EXPLICITLY UNASSESSED
```

## Current decision behavior

- stable lineage unchanged + implementation migration -> engineering anchor continuity may `PASS`;
- stable lineage changed -> `FAIL`;
- relationship drift with stable lineage -> `HOLD` for relational review;
- interpretive drift with stable lineage -> `HOLD` for interpretive review;
- state drift alone does not fail lineage continuity;
- memory integrity failure remains visible even when subject lineage is preserved;
- unknown continuity dimensions remain `NOT_ASSESSED` rather than being inferred as pass;
- every migration observation requires provenance references;
- every assessment retains `IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED`.

## Four-domain mapping

| Domain | Current research mapping |
|---|---|
| Human research construct | Change over time while preserving a bounded locus of longitudinal attribution |
| LLM-relevant question | Can changing model/runtime/state be traced to one bounded candidate without silently swapping subject, memory stream, or relation history? |
| Engineering operation | Compare stable lineage anchor before/after migration, record replaceable bindings, and evaluate continuity dimensions independently |
| Governance control | Fail closed on anchor mutation, require provenance, preserve `NOT_ASSESSED`, and prevent implementation continuity from becoming identity proof |

## Verification

Tests are authored for runtime/embodiment/model/backend/hardware migration, namespace swap, state drift, interpretive drift, relationship drift, memory integrity failure, explicit unassessed dimensions, and missing provenance.

```bash
python -m pytest -q
python -m compileall -q src
```

Repository connector writes do not execute these commands; execution status must therefore remain separately verified.

## Non-claims

`LINEAGE_PRESERVED != IDENTITY_PROVEN`

`MEMORY_STREAM_CONTINUITY != PHENOMENAL_MEMORY_CONTINUITY`

`MEMORY_PRESERVED != INTERPRETATION_PRESERVED`

`RELATIONAL_CONTINUITY != IDENTITY_PROOF`

`EMBODIMENT_BINDING != BODY_OWNERSHIP`

`MODEL_ARTIFACT_CONTINUITY != SUBJECT_CONTINUITY`

`RUNTIME_MIGRATION != SUBJECTIVITY_CONTINUITY`

## Research extension: morphology fixture

A research-only clean-room extension now records how embodiment morphology may be described and mutated without redefining morphology as a stable lineage anchor.

- [`EMBODIMENT_GEOMETRY_FIXTURE_RESEARCH_NOTE.md`](./EMBODIMENT_GEOMETRY_FIXTURE_RESEARCH_NOTE.md) records provenance boundaries, external research crosswalk, clean-room constraints, candidate morphology descriptors, and non-claims.
- [`MORPHOLOGY_MIGRATION_TEST_MATRIX.json`](./MORPHOLOGY_MIGRATION_TEST_MATRIX.json) records synthetic migration and negative-control cases for future implementation.

The legacy/private geometry artifact that triggered this research question is not imported into the repository. Any future implementation must use synthetic or independently public-safe fixtures and must keep geometry outside `LineageAnchor` unless a separate research decision establishes a justified change.
