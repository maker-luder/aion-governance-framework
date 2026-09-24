# CCTS first scholarly release — metadata draft

Status: `DRAFT_METADATA / NOT_RELEASED / HUMAN_CONFIRMATION_REQUIRED`

## Fixed research metadata

```text
TITLE =
Co-Constructed Thinking Space (CCTS):
A Provenance-Bounded Framework for Human–AI Reciprocal Epistemic Collaboration

SHORT_TITLE =
Co-Constructed Thinking Space (CCTS)

RELEASE_OBJECT =
CONCEPTUAL_FRAMEWORK
+ RESEARCH_METHOD
+ EXECUTABLE_STRUCTURAL_CONTRACT

CANDIDATE_VERSION =
0.1.0

LANGUAGE =
English manuscript with repository-linked bilingual research context

REPOSITORY =
maker-luder/aion-governance-framework

LICENSE_SOFTWARE =
Apache-2.0 (existing repository software license)

SCIENTIFIC_DISPOSITION =
HOLD

PEER_REVIEW =
NOT_PERFORMED

SCIENTIFIC_VALIDATION =
NOT_ESTABLISHED
```

## Proposed keywords

```text
Human–AI collaboration
Human–AI interaction
epistemic collaboration
co-construction
provenance
reciprocal revision
distributed cognition
joint problem space
epistemic agency
AI-assisted learning
research integrity
reproducible research
```

## Abstract metadata

Use the manuscript abstract from:
`docs/research/publication/CCTS_PREPRINT_DRAFT_V0_1.md`

The abstract must preserve:
```text
CCTS = REPOSITORY_DEFINED_CONSTRUCT
CCTS != VALIDATED_THEORY
CCTS != AI_SUBJECTIVITY_RESULT
```

## Human-confirmation-required fields

These fields are intentionally not inferred:

```text
PUBLIC_AUTHOR_NAME = PENDING
ORCID = OPTIONAL / PENDING
AFFILIATION = OPTIONAL / PENDING
PUBLIC_CONTACT_EMAIL = OPTIONAL / PENDING
MANUSCRIPT_TEXT_LICENSE = PENDING
RELEASE_DATE = NOT_SET
DOI = NOT_MINTED
```

The GitHub username, repository ownership, account email and any private identity information must not be silently converted into scholarly author metadata.

## Citation strategy

The root `CITATION.cff` currently describes a historical AION release and must remain untouched until the new CCTS scholarly metadata is complete.

Planned release transition:

```text
CURRENT_ROOT_CITATION
= HISTORICAL_AION_RELEASE_METADATA

FUTURE_ROOT_CITATION_AFTER_EXPLICIT_APPROVAL
= CCTS_SCHOLARLY_RELEASE_METADATA
+ explicit historical/version provenance
```

No root citation change is authorized by this draft.

## AI assistance disclosure metadata

```text
AI_SYSTEM =
ChatGPT

ROLE =
research assistance

DISCLOSED_FUNCTIONS =
problem decomposition
literature-search support
formalization
adversarial review
source-role separation
engineering / QA assistance
manuscript drafting assistance

AI_AUTHORSHIP =
NOT_ASSUMED
```

Final wording remains venue-dependent.

## Privacy / ethics metadata

```text
RAW_PRIVATE_TRANSCRIPTS_PUBLISHED = NO
DIRECT_HUMAN_IDENTIFIERS_PUBLISHED = NO
HUMAN_PARTICIPANT_DATASET_PUBLISHED = NO
SYNTHETIC_STRUCTURAL_FIXTURES = YES
```

This metadata describes the planned first CCTS scholarly object only. Any later empirical Human-participant study requires a separate ethics and consent assessment.

## Release readiness implication

```text
METADATA_STRUCTURE = PREPARED
PUBLIC_AUTHOR_NAME = BLOCKING
MANUSCRIPT_TEXT_LICENSE = BLOCKING_FOR_FINAL_ARCHIVE
DOI = POST_RELEASE
```
