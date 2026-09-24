# Proposed repository CITATION.cff strategy for CCTS — staging only

This file is a human-readable staging note for the future CCTS `preferred-citation`. The preparation branch now also contains a separate root `CITATION.cff` cleanup that removes stale August release-bound version/date metadata while preserving the AION repository/software identity.

## 1. Correct object model

The repository root citation file describes the AION repository/software object.

The CCTS scholarly manuscript is a separate publication object.

CFF 1.2.0 provides `preferred-citation` specifically for the case where software/repository metadata remains at the root while a paper or other work is the preferred scholarly citation.

```text
ROOT_OBJECT = AION_REPOSITORY
PREFERRED_SCHOLARLY_OBJECT = CCTS_PUBLICATION

ROOT_OBJECT != PREFERRED_SCHOLARLY_OBJECT
```

## 2. Current preparation-branch root state

The root file now preserves AION repository/software metadata without claiming the historical August release as the live repository version.

```text
ROOT_OBJECT = AION_REPOSITORY
STALE_AUGUST_VERSION_DATE_BINDING = REMOVED_ON_PREPARATION_BRANCH
CCTS_PREFERRED_CITATION = NOT_ADDED
```

## 3. Future preferred-citation pattern — schematic, not release-valid

After Human-controlled CCTS publication metadata is confirmed, the root file may add a CCTS preferred citation while keeping the AION repository identity.

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
    - name: "poshi"
  year: "<SET_WHEN_PUBLICATION_EXISTS>"
  doi: "<SET_AFTER_CCTS_PUBLICATION_DOI_EXISTS>"
```

## 4. Why this replaces the earlier staging plan

Earlier staging considered replacing the root citation object with CCTS metadata. Reverse review rejected that approach because the repository contains a broader AION research framework.

```text
OVERWRITE_AION_ROOT_IDENTITY_WITH_CCTS = REJECTED
CFF_PREFERRED_CITATION_PATTERN = ACCEPTED_FOR_FUTURE_REVIEW
```

## 5. Zenodo boundary

Zenodo's GitHub integration consumes repository metadata for software archiving.

The CCTS manuscript should instead be deposited as its own scholarly publication record if a publication DOI is desired.

```text
GITHUB_ZENODO_SOFTWARE_RECORD
!=
CCTS_ZENODO_PUBLICATION_RECORD
```

## 6. Validation boundary

The stale live-repository release binding has already been corrected on the preparation branch. This staging note does **not** authorize adding a CCTS `preferred-citation`.

Before any future CCTS `preferred-citation` update:

1. preserve the confirmed public author name `poshi`;
2. preserve the confirmed All Rights Reserved manuscript rights statement;
3. freeze the CCTS manuscript publication metadata;
4. obtain or reserve the CCTS publication DOI if desired;
5. set the publication year/date when the publication exists;
6. validate the final CFF syntax;
7. obtain explicit Human Owner authorization for the preferred-citation transition.

```text
ROOT_CITATION_CLEANUP_EXISTS = YES_ON_PREPARATION_BRANCH
STAGING_NOTE_EXISTS != PREFERRED_CITATION_ADDED
PREFERRED_CITATION_PROPOSED != PUBLICATION_EXISTS
```
