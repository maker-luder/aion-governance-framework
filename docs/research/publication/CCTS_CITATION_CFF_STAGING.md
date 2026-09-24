# Proposed repository CITATION.cff strategy for CCTS — staging only

This file is a human-readable staging note. It is **not** the repository root `CITATION.cff`.

## 1. Correct object model

The repository root citation file describes the AION repository/software object.

The CCTS scholarly manuscript is a separate publication object.

CFF 1.2.0 provides `preferred-citation` specifically for the case where software/repository metadata remains at the root while a paper or other work is the preferred scholarly citation.

```text
ROOT_OBJECT = AION_REPOSITORY
PREFERRED_SCHOLARLY_OBJECT = CCTS_PUBLICATION

ROOT_OBJECT != PREFERRED_SCHOLARLY_OBJECT
```

## 2. Future root pattern — schematic, not release-valid

The future root file should preserve actual repository metadata and may add a CCTS preferred citation after Human-controlled metadata is confirmed.

```yaml
cff-version: 1.2.0
message: >-
  Please cite the AION repository/software using the repository metadata below.
  For the CCTS scholarly framework, use the preferred-citation once published.

title: "AION Governance Framework"
type: software

authors:
  - name: "<REPOSITORY_AUTHOR_METADATA_REVIEW_REQUIRED>"

repository-code: "https://github.com/maker-luder/aion-governance-framework"
license: "Apache-2.0"

# Repository version/date/commit must reflect the exact repository release
# being described and must not be copied from a stale historical release.

preferred-citation:
  type: article
  title: >-
    Co-Constructed Thinking Space (CCTS):
    A Provenance-Bounded Framework for Human–AI Reciprocal Epistemic Collaboration
  authors:
    - name: "<PUBLIC_AUTHOR_NAME_REQUIRES_HUMAN_CONFIRMATION>"
  year: "<SET_WHEN_PUBLICATION_EXISTS>"
  doi: "<SET_AFTER_CCTS_PUBLICATION_DOI_EXISTS>"
```

## 3. Why this replaces the earlier staging plan

Earlier staging considered replacing the root citation object with CCTS metadata. Reverse review rejected that approach because the repository contains a broader AION research framework.

```text
OVERWRITE_AION_ROOT_IDENTITY_WITH_CCTS = REJECTED
CFF_PREFERRED_CITATION_PATTERN = ACCEPTED_FOR_FUTURE_REVIEW
```

## 4. Zenodo boundary

Zenodo's GitHub integration consumes repository metadata for software archiving.

The CCTS manuscript should instead be deposited as its own scholarly publication record if a publication DOI is desired.

```text
GITHUB_ZENODO_SOFTWARE_RECORD
!=
CCTS_ZENODO_PUBLICATION_RECORD
```

## 5. Validation boundary

No root citation change is authorized by this staging note.

Before any future root `CITATION.cff` update:

1. review the current repository-level citation metadata independently;
2. confirm the Human public author name for CCTS;
3. confirm manuscript license;
4. freeze the CCTS manuscript publication metadata;
5. obtain or reserve the CCTS publication DOI if desired;
6. validate the final CFF syntax;
7. obtain explicit Human Owner authorization for the root metadata change.

```text
STAGING_NOTE_EXISTS != ROOT_CITATION_UPDATED
PREFERRED_CITATION_PROPOSED != PUBLICATION_EXISTS
```
