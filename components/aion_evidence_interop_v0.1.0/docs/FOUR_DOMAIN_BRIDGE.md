# Four-Domain → AION Evidence Bridge v0.1.0

Status: `BOUNDED / READ_ONLY / INSPECTION_ONLY`

This bridge connects one exact preserved Four-Domain research checkpoint to the existing AION research-evidence and interoperability pipeline without restarting research, merging the research branch, promoting a scientific conclusion, or creating runtime authority.

## Frozen source binding

```text
SOURCE_REPOSITORY = maker-luder/aion-governance-framework
SOURCE_BRANCH = review/four-domain-research-materialization
SOURCE_HEAD = f654b5032ebc45058a64e81d409149ee7ea4bfbe
SOURCE_STATE = INDEFINITE_FROZEN_CHECKPOINT
SOURCE_ARTIFACT = research-workbench/four-domain-materialization/2026-08-09/FOUR_DOMAIN_REPOSITORY_CROSSWALK.md
SOURCE_GIT_BLOB_SHA1 = 7e55741b85b27d383b4b721b834b1744c6c03fb9
```

The bridge is pinned to the exact commit and Git blob above. It does not resolve the live branch tip, fetch remote content, or infer that a later branch state is equivalent.

## Flow

```text
frozen Four-Domain crosswalk
        |
        | exact commit + blob reference
        v
Four-Domain bridge descriptor
        |
        | deterministic materialization
        v
AION research_evidence_record_v0.2.0
        |
        | existing AION validator
        v
AION Evidence Interop Profile v0.1.0
        |
        +--> W3C PROV
        +--> RO-Crate
        +--> unsigned in-toto Statement v1
        +--> OPA / Rego
        +--> Inspect-compatible static dataset/task metadata
        +--> OpenSSF Scorecard-aligned repository hygiene crosswalk
```

The materialized evidence record uses `result_status = HOLD`. The bridge records a historical repository mapping; it does not claim a newly executed experiment or a fresh scientific result. The record's `code_commit` is therefore the frozen Four-Domain source head, while the existing AION validator remains free to require exact inspected-head binding for completed records.

## Semantics preserved

The source crosswalk remains authoritative for its row-level content. v0.1.0 materializes the crosswalk as one bounded evidence unit and preserves the following distinctions:

```text
OBSERVATION != MECHANISM != INTERPRETATION
ENGINEERING_ANALOGUE != BIOLOGICAL_EQUIVALENCE
ENGINEERING_CONTINUITY != ONTOLOGICAL_IDENTITY_CONTINUITY
RUNTIME_EVENT_STREAM != RECOLLECTIVE_EXPERIENCE
DESIGN_GAP = PRESERVE_AS_GAP
RESEARCH_DEFINITION_REQUIRED = PRESERVE_AS_UNRESOLVED
```

The bridge must not convert a repository mapping, implementation status, test result, provenance record, or engineering analogue into evidence of subjectivity, consciousness, phenomenal affect, identity continuity, moral status, or canonical authority.

## Governance boundaries

```text
FOUR_DOMAIN_SOURCE != MAIN_CANONICAL_STATE
DERIVATION != MERGE
REFERENCE != PROMOTION
INTEROP_EXPORT != RESEARCH_RESTART

PROJECT_RESTART = NO
RESEARCH_EXECUTION = FALSE
MODEL_EXECUTION = FALSE
NETWORK_ACCESS = FALSE
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
INDEPENDENT_IVV = NOT_ACHIEVED
```

No change to `review/four-domain-research-materialization` is required or authorized by this bridge.

## Source verification model

v0.1.0 stores the exact source repository, branch label, commit SHA-1, artifact path, and Git blob SHA-1 in a closed descriptor. The implementation validates those pinned values locally and constructs an exact-commit GitHub URL as an opaque provenance reference. It does not make a network request and does not claim to re-verify hosted GitHub state at runtime.

The source artifact was previously inspected and preserved on the research branch. This bridge records that exact historical identity; it is not an independent archive service or IV&V system.

## Attribution

```text
BRIDGE_DESIGN_SOURCE = ChatGPT
BRIDGE_IMPLEMENTATION_SOURCE = ChatGPT
CURRENT_IMPLEMENTATION_REQUEST = USER_GIVEN
FOUR_DOMAIN_SOURCE_ATTRIBUTION = PRESERVED_FROM_SOURCE_ARTIFACT
MAIN_MERGE_AUTHORITY = NOT_GRANTED_BY_THIS_BRIDGE
CANONICAL_EFFECT = NONE
```
