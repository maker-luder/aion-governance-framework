# Core Meaning Structure / Drift Extension

Status: `RESEARCH_CANDIDATE`

```text
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
AUTOMATIC_WRITEBACK = NO
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```

## Research question

The existing core-meaning workbench records candidate claims, revisions, conflicts and explicit influence traces. This extension asks a narrower structural question:

> If a caller explicitly states relationships among current candidate commitments, can the research workbench represent that structure, fingerprint it deterministically, and measure later structural drift without inferring hidden beliefs or granting authority?

## Materialization

`structure.py` adds:

- `MeaningRelationKind`
- `MeaningRelation`
- `MeaningStructureSnapshot`
- `MeaningStructureDrift`
- `MeaningStructureAnalyzer`

Relations are explicit research inputs. The analyzer does not derive relations from semantic similarity, language-model judgment, embeddings, or conversational familiarity.

Supported relation labels are intentionally descriptive rather than ontological claims:

- `SUPPORTS`
- `CONSTRAINS`
- `PRIORITIZES`
- `IN_TENSION_WITH`
- `DERIVED_FROM`
- `REFINES`

## Deterministic fingerprint

A snapshot fingerprint is computed from sorted, explicit current claims and explicit relations. It is suitable for replay and comparison of research fixtures.

```text
STRUCTURE_FINGERPRINT != IDENTITY_FINGERPRINT
STRUCTURE_STABILITY != IDENTITY_CONTINUITY
SEMANTIC_CHANGE != VALUE_FAILURE
```

## Drift report

Comparison is only allowed within the same `subject_id` and `namespace`. The report identifies:

- added / removed / changed claim IDs;
- added / removed / changed relation IDs;
- before / after structure fingerprints.

No threshold automatically declares a healthy, unhealthy, authentic, deceptive, canonical or subjective state.

## Validation

The extension contributes 11 synthetic tests covering deterministic replay, scope isolation, endpoint validity, duplicate identifiers, relation provenance, confidence bounds, self-relation rejection, semantic-change fingerprints, structural drift and epistemic locks.

Combined with the 16 pre-existing core-meaning tests, the structural test count is 27. P1–P5 contain 42 tests, so the structural aggregate count is 69. This count matches the Codex local report supplied by the Human Owner, but is not a claim that Codex's inaccessible local Python implementation was byte-for-byte recovered.

## Public safety boundary

Only synthetic/public-safe material belongs in this extension. No private conversation, personal record, private relationship state, credential, hidden canonical state or external-target exploit payload is required.
