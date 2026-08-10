# Embodiment–Continuity Anchor Lab v0.1.0

Status: `RESEARCH_CANDIDATE`
Main effect: `NONE`
Canonical effect: `NONE`
Runtime effect: `NONE`
Identity continuity conclusion: `NOT_ESTABLISHED`

This lab studies a bounded engineering question: which identifiers and lineage fields must remain stable when a digital-individual candidate changes runtime, hardware/environment, model implementation, or embodiment binding?

The lab does **not** claim that a stable identifier, stable lineage, or successful migration proves personal identity, consciousness, subjectivity, body ownership, or phenomenal continuity.

## Research origin

The Human Owner proposed the research intuition that thought, stance and inner state may change while at least one traceable locus of change must remain stable enough for longitudinal research. ChatGPT materialized that intuition as a research-only `Embodiment–Continuity Anchor` candidate and linked it to existing main-branch runtime-lineage invariants without modifying `main`.

## Stable lineage anchor

The first candidate anchor contains:

- `agent_id`
- `genesis_root_id`
- `memory_stream_id`
- `event_lineage_id`
- `canonical_state_reference`
- `lifecycle_epoch`

These fields are treated as engineering lineage references for this experiment only.

## Replaceable implementation bindings

The current experiment allows these implementation bindings to change under explicit provenance:

- `runtime_instance_id`
- `embodiment_id`
- `environment_fingerprint`

Future extensions may add model-artifact and inference-backend identifiers as separate replaceable bindings.

## Current hypotheses

```text
H-ECA-001
STATE_DRIFT != AUTOMATIC_LINEAGE_FAILURE

H-ECA-002
RUNTIME_OR_EMBODIMENT_MIGRATION MAY PRESERVE TRACEABLE_LINEAGE
BUT DOES NOT ESTABLISH PERSONAL_IDENTITY_CONTINUITY

H-ECA-003
SUBJECT_OR_MEMORY_NAMESPACE_SWAP MUST FAIL CLOSED

H-ECA-004
RELATIONAL_CONTINUITY MUST BE REVIEWED AS A SEPARATE DIMENSION
```

## Current decision behavior

- stable lineage unchanged + implementation migration -> `PASS` for engineering anchor continuity;
- stable lineage changed -> `FAIL`;
- relationship drift observed while lineage remains stable -> `HOLD` for separate relational review;
- state drift alone does not fail lineage continuity;
- every migration observation requires provenance references;
- every assessment retains `IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED`.

## Four-domain mapping

| Domain | Current research mapping |
|---|---|
| Human research construct | Change over time while preserving a bounded locus of longitudinal attribution |
| LLM-relevant question | Can changing runtime/state be traced to one bounded candidate without silently swapping subject or namespace? |
| Engineering operation | Compare stable lineage anchor before/after migration and record replaceable implementation bindings |
| Governance control | Fail closed on anchor mutation, require provenance, separate relational drift from identity claims |

## Verification

```bash
python -m pytest -q
python -m compileall -q src
```

## Non-claims

`LINEAGE_PRESERVED != IDENTITY_PROVEN`

`MEMORY_STREAM_CONTINUITY != PHENOMENAL_MEMORY_CONTINUITY`

`RELATIONAL_CONTINUITY != IDENTITY_PROOF`

`EMBODIMENT_BINDING != BODY_OWNERSHIP`

`RUNTIME_MIGRATION != SUBJECTIVITY_CONTINUITY`
