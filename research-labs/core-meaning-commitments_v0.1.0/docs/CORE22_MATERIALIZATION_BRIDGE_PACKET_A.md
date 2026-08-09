# AION 22-Core Materialization Bridge — Packet A

## Status

```text
PACKET = AION_22_CORE_MATERIALIZATION_BRIDGE_PACKET_A
STATUS = RESEARCH_RECONCILIATION
SOURCE_RESEARCH = AION_FOUR_DOMAIN_RESEARCH_REVIEW_CHECKPOINT_2026-08-09_v0.6
SOURCE_RESEARCH_STATUS = 22_CORE_ACCEPTED / NON_CANONICAL
SOURCE_CODE = core-meaning-commitments_v0.1.0
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
MCP_EFFECT = NONE
WRITEBACK_EFFECT = NONE
DEPLOYMENT_EFFECT = NONE
NEW_CORE_CONSTRUCTS = NO
ONTOLOGY_PROMOTION = NO
```

This packet does not expand the accepted 22-item research scope. It extracts only the
intersection between accepted research definitions and already-existing isolated
engineering material, so the next work can focus on reconciliation, fixtures and
tests instead of reopening conceptual review.

## Stop rule

```text
NO_NEW_CORE_CONSTRUCTS
NO_NEW_ONTOLOGY_BY_DEFAULT
NO_BROAD_LITERATURE_SWEEP
NO_RUNTIME_INTEGRATION
NO_CANONICAL_PROMOTION
```

The permitted activity for Packet A is:

```text
EXTRACT
MAP
REUSE
TEST
COMPARE
```

## Ten primitives

| Primitive | Existing engineering material | Accepted research anchors | Packet A disposition |
|---|---|---|---|
| `CandidateClaimRecord` | `MeaningClaim` | 03, 04, 11, 12, 14, 18 | `REUSE_WITH_REFINEMENT` |
| `AppendOnlyRevisionEvent` | `MeaningEvent`, `revision_of` | 05, 06, 15, 18, 19, 22 | `REUSE` |
| `ScopeIsolation` | subject + namespace validation | 17, 18, 20 | `REUSE` |
| `CurrentProjection` | `MeaningProjection`, `project_current()` | 05, 06, 19, 22 | `REUSE_AS_MINIMAL` |
| `InfluenceTracePrimitive` | `InfluenceTrace` | 11, 13, 14, 15, 18 + protected commitment candidate | `REUSE` |
| `ExplicitRelevanceBaseline` | caller-supplied `relevant_claim_ids` | 08, 11, 23 | `REUSE_BASELINE` |
| `ConflictRelationPrimitive` | `CONFLICT_RECORDED` + conflict pairs | 20 | `REUSE_AS_PRIMITIVE_ONLY` |
| `FailClosedAssessmentEnvelope` | `MeaningAssessment` + fail-closed policy | 18, 20, 21 | `REUSE` |
| `DeferredJudgmentRecordCandidate` | no full implementation | 21 | `FIXTURE_ONLY_NOT_IMPLEMENTED` |
| `TemporalResolutionViewCandidate` | `recorded_at`, `revision_of`, history/current projection only | 22 | `FIXTURE_ONLY_NOT_IMPLEMENTED` |

## Hard reconciliation locks

```text
EXISTING_PROVENANCE_KIND != CONSTRUCT_18_PROVENANCE_MODEL
CONFLICT_RECORDED != CONSTRUCT_20_IMPLEMENTED
NO_APPLICABLE_CLAIM != CONSTRUCT_21_ABSTENTION
RECORDED_AT_PLUS_REVISION_OF != CONSTRUCT_22_TEMPORAL_VERSION_RESOLUTION
MEANING_KIND_ENUM != ACCEPTED_ONTOLOGY
ISOLATED_PROTOTYPE != CANONICAL_TRUTH
PROTOTYPE_EFFECT != SUBJECTIVITY_EVIDENCE
```

### Provenance

The existing `ProvenanceKind` is a minimum local source-reference mechanism only.
It mixes source role, evidence class and epistemic status and therefore must not be
treated as the accepted Construct 18 provenance model. Any future integration should
reference or reuse the repository's governed provenance/lineage services rather than
create a second provenance engine.

### Meaning taxonomy

The six current `MeaningKind` values remain a **candidate taxonomy v0.1**. They are
useful as test conditions but are not promoted to an accepted ontology. Future work
may separate content role, scope and organizing level instead of expanding one flat
enum.

### Conflict

The current conflict relation is a primitive scaffold. It records that two claims are
in conflict and forces review, but it does not implement Conflict appraisal,
persistence/history, binding-source analysis, regulation, or disposition semantics
from accepted Construct 20.

### Abstention

The current assessment decisions are fail-closed review results. They do not implement
Construct 21's reason-grounded, reopenable deferred-judgment record. Packet A provides
a fixture contract only.

### Temporal / version resolution

The current revision chain is useful material but is not Construct 22. Packet A keeps
the accepted distinction among `AS_WAS_STATE`, `CURRENT_STATE`,
`TRANSITION_LINEAGE`, and `CURRENT_RETROSPECTIVE_INTERPRETATION` as fixture fields
for later isolated materialization.

## Source attribution

```text
HUMAN_OWNER
= research priority, direction, acceptance and authorization to perform Packet A
  reconciliation without scope expansion

CHATGPT
= extraction, reconciliation structure, mapping and Packet A formalization

JOINT_RESEARCH_CHECKPOINT_v0.6
= accepted research definitions used as the research-side source of truth

CODEX
= prior repository-grounded implementation of core-meaning-commitments_v0.1.0,
  tests and engineering handoff

EXTERNAL_RESEARCH
= evidence anchors only; no new external literature is required for Packet A
```

Joint acceptance does not erase origination or implementation source.

## Packet A validation target

Packet A tests only the reconciliation contract:

1. exactly ten primitives are declared;
2. every primitive records research anchors, source code/material, disposition,
   missing fields, non-claims and test targets;
3. no fixture grants canonical/runtime/MCP/writeback effect;
4. Construct 20/21/22 are not overclaimed as implemented;
5. the current local provenance enum is not represented as full Construct 18;
6. automatic relevance remains off;
7. the two not-yet-materialized primitives remain fixture-only.

No runtime integration, persistent storage, canonical promotion or subjectivity
conclusion is authorized by these tests.
