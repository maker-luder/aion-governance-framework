# CCTS scholarly publication — current metadata record

Status: `PUBLICLY_ARCHIVED / DOI_MINTED / NOT_PEER_REVIEWED / SCIENTIFIC_HOLD`

This file records the post-publication semantic state of the first CCTS scholarly object. It does not rewrite the dated 2026-09-24 preparation, readiness, or release-route records.

## Current publication object

```text
TITLE =
Co-Constructed Thinking Space (CCTS):
A Provenance-Bounded Framework for Human–AI Reciprocal Epistemic Collaboration

PUBLIC_AUTHOR_NAME = poshi
PUBLICATION_YEAR = 2026
ZENODO_RECORD = 22945883
DOI = 10.5281/zenodo.22945883
PUBLICATION_STATE = PUBLICLY_ARCHIVED

PEER_REVIEW = NOT_PERFORMED
SCIENTIFIC_VALIDATION = NOT_ESTABLISHED
EXTERNAL_REPLICATION = NOT_ESTABLISHED
```

Public routes:

- Zenodo: https://zenodo.org/records/22945883
- DOI: https://doi.org/10.5281/zenodo.22945883

## Repository / publication object boundary

```text
AION_REPOSITORY_OBJECT
= software-and-research-framework object

CCTS_SCHOLARLY_OBJECT
= manuscript / publication object

AION_REPOSITORY_OBJECT != CCTS_SCHOLARLY_OBJECT
SOFTWARE_DOI != MANUSCRIPT_DOI
```

The root `CITATION.cff` continues to describe the broader AION repository/software object and may point to CCTS through `preferred-citation`; the CCTS publication does not replace the repository identity.

## Rights and authorship boundary

The repository software remains under its repository license. The CCTS manuscript rights position remains the separately Human-confirmed scholarly-object rights statement recorded in the pre-publication metadata staging record.

```text
AI_RESEARCH_PARTICIPATION != ACADEMIC_AUTHORSHIP
REPOSITORY_OWNERSHIP != SCHOLARLY_AUTHOR_METADATA
```

## Scientific claim boundary

```text
PUBLICATION != PEER_REVIEW
DOI != SCIENTIFIC_VALIDATION
ARCHIVAL_PUBLICATION != EMPIRICAL_CONFIRMATION
CCTS_STRUCTURAL_CONFORMANCE != CCTS_EMPIRICAL_VALIDATION
CCTS_PUBLICATION != AI_SUBJECTIVITY_EVIDENCE
```

## Verification note

The Zenodo and DOI routes were not independently re-fetched by the current automated review environment during this synchronization pass. Therefore this record does not infer additional Zenodo fields such as an exact publication date, venue classification, or record-side metadata beyond the publication identifiers already established in the repository release context.

```text
PUBLICATION_DATE = NOT_REVERIFIED_IN_THIS_SYNC
UNVERIFIED_REMOTE_FIELDS = NOT_INFERRED
```
