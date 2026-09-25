# CCTS first scholarly release — metadata draft

Status: `METADATA_PREPARED / NOT_RELEASED / EXACT_HEAD_REVIEW_REQUIRED`

## 1. Object separation

```text
AION_REPOSITORY_OBJECT
= repository / software-and-research-framework object

CCTS_SCHOLARLY_OBJECT
= manuscript / publication object

AION_REPOSITORY_OBJECT != CCTS_SCHOLARLY_OBJECT
```

The CCTS scholarly manuscript may cite and bind the repository, but it must not overwrite the repository's identity.

## 2. Fixed CCTS scholarly metadata

```text
TITLE =
Co-Constructed Thinking Space (CCTS):
A Provenance-Bounded Framework for Human–AI Reciprocal Epistemic Collaboration

SHORT_TITLE =
Co-Constructed Thinking Space (CCTS)

SCHOLARLY_OBJECT_TYPE =
CONCEPTUAL_FRAMEWORK
+ RESEARCH_METHOD
+ EXECUTABLE_STRUCTURAL_CONTRACT

CCTS_MANUSCRIPT_VERSION =
0.1.0

PROPOSED_ARTIFACT_LABEL =
ccts-scholarly-v0.1.0

LANGUAGE =
English manuscript with repository-linked bilingual research context

RELATED_REPOSITORY =
maker-luder/aion-governance-framework

REPOSITORY_SOFTWARE_LICENSE =
Apache-2.0

SCIENTIFIC_DISPOSITION =
HOLD

PEER_REVIEW =
NOT_PERFORMED

SCIENTIFIC_VALIDATION =
NOT_ESTABLISHED
```

The CCTS manuscript version is a separate namespace and is not an AION repository semantic-version replacement.

## 3. Proposed keywords

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

## 4. Abstract metadata

Use the manuscript abstract from:

`docs/research/publication/CCTS_PREPRINT_DRAFT_V0_1.md`

The abstract must preserve:

```text
CCTS = REPOSITORY_DEFINED_CONSTRUCT
CCTS != VALIDATED_THEORY
CCTS != AI_SUBJECTIVITY_RESULT
```

## 5. Human-confirmation-required fields

These fields are intentionally not inferred:

```text
PUBLIC_AUTHOR_NAME = poshi
ORCID = OMIT_FROM_FIRST_RELEASE / NOT_PROVIDED
AFFILIATION = OMIT_FROM_FIRST_RELEASE / NOT_PROVIDED
PUBLIC_CONTACT_EMAIL = OMIT_FROM_FIRST_RELEASE / NOT_PROVIDED

MANUSCRIPT_TEXT_LICENSE = ALL RIGHTS RESERVED / CUSTOM RIGHTS STATEMENT

ZENODO_DEFAULT_LICENSE = CC-BY-4.0
ZENODO_LICENSE_DECISION = HUMAN_CONFIRMED_CUSTOM_RIGHTS

PUBLICATION_DATE = NOT_SET
CCTS_PUBLICATION_DOI = NOT_MINTED
```

The GitHub username, repository ownership, account email and any private identity information must not be silently converted into scholarly author metadata.

## 6. Human-confirmed manuscript rights statement

The Human Owner explicitly confirmed the following rights statement for the CCTS scholarly manuscript:

```text
ALL RIGHTS RESERVED

本作品不另行授權重製、改作、散布或商業利用。
引用與節錄僅依適用法律所允許的範圍進行。

No additional rights to reproduce, adapt, redistribute, or commercially exploit this work are granted.
Citation and quotation are permitted only to the extent allowed by applicable law.
```

Interpretation boundary:

```text
CITATION_ALLOWED_BY_LAW != GENERAL_REUSE_LICENSE
NO_ADDITIONAL_REUSE_RIGHTS_GRANTED = YES
CREATIVE_COMMONS_LICENSE = NO
```

This statement is the manuscript/publication rights position and must not be confused with the repository software license (`Apache-2.0`).

## 7. Citation strategy

The root `CITATION.cff` describes the repository/software object.

Correct future pattern:

```text
ROOT_CITATION_CFF
= AION_REPOSITORY_METADATA
+ OPTIONAL preferred-citation -> CCTS_PUBLICATION
```

Incorrect pattern:

```text
ROOT_CITATION_CFF
= REPLACED_BY_CCTS_ONLY
```

A root `preferred-citation` should be considered only after the CCTS publication has stable author metadata and preferably a DOI.

## 8. Zenodo scholarly-record strategy

Zenodo currently requires a license for a deposited record and defaults to Creative Commons Attribution 4.0 International (CC BY 4.0). The default is documented here but is **not** adopted automatically for CCTS.

Official source:
- https://help.zenodo.org/docs/deposit/describe-records/licenses/

```text
ZENODO_LICENSE_FIELD = REQUIRED
ZENODO_DEFAULT = CC-BY-4.0
DEFAULT_PRESENT != HUMAN_LICENSE_CONSENT

ZENODO_LICENSE_SELECTION = CUSTOM
ZENODO_CUSTOM_LICENSE_TITLE = All Rights Reserved — lawful citation and quotation only
ZENODO_CUSTOM_LICENSE_DESCRIPTION = No additional rights to reproduce, adapt, redistribute, or commercially exploit this work are granted. Citation and quotation are permitted only to the extent allowed by applicable law.
```



The CCTS manuscript should use an independent Zenodo publication record if Zenodo is chosen for the first archival publication.

```text
ZENODO_RESOURCE_TYPE
= PUBLICATION / APPROPRIATE MANUSCRIPT SUBTYPE

RELATED_IDENTIFIER
= exact repository / exact commit / optional software archive

CCTS_PUBLICATION_DOI
= manuscript/publication DOI
```

A GitHub-triggered Zenodo software archive is a separate optional object.

## 9. AI assistance disclosure metadata

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

## 10. Privacy / ethics metadata

```text
RAW_PRIVATE_TRANSCRIPTS_PUBLISHED = NO
DIRECT_HUMAN_IDENTIFIERS_PUBLISHED = NO
HUMAN_PARTICIPANT_DATASET_PUBLISHED = NO
SYNTHETIC_STRUCTURAL_FIXTURES = YES
```

This metadata describes the planned first CCTS scholarly object only. Any later empirical Human-participant study requires a separate ethics and consent assessment.

## 11. Release readiness implication

```text
METADATA_STRUCTURE = PREPARED

PUBLIC_AUTHOR_NAME
= CONFIRMED_AS_poshi

MANUSCRIPT_TEXT_LICENSE
= CONFIRMED_CUSTOM_RIGHTS

CCTS_PUBLICATION_DOI
= POST_DRAFT / PREPUBLICATION-RESERVABLE / REGISTERED_ON_PUBLICATION

ROOT_PREFERRED_CITATION
= OPTIONAL_AFTER_CCTS_PUBLICATION_METADATA_EXISTS
```
