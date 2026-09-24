# CCTS scholarly release route — repository software + scholarly publication (verified 2026-09-24)

Status: `PREPARATION_ONLY / NO_RELEASE_ACTION`

## 1. Reverse-review correction

The AION repository and the CCTS manuscript are related research objects, but they are not the same citable object.

```text
OBJECT_A = AION_REPOSITORY / SOFTWARE-AND-RESEARCH-FRAMEWORK
OBJECT_B = CCTS_SCHOLARLY_MANUSCRIPT / PUBLICATION

OBJECT_A != OBJECT_B
SOFTWARE_DOI != MANUSCRIPT_DOI
```

The root `CITATION.cff` belongs to Object A. It must not be replaced by metadata that makes the entire AION repository appear to be only the CCTS paper.

## 2. Verified CFF mechanism

Citation File Format 1.2.0 supports `preferred-citation`.

The official CFF schema guide describes this specifically for the case where a repository/software project has a paper that authors would prefer users to cite. GitHub's own citation documentation also supports `preferred-citation` for articles and other research objects.

Therefore the future repository-level pattern is:

```text
ROOT CITATION.cff
= AION repository/software metadata
+ optional preferred-citation -> CCTS scholarly publication
```

Official references:
- CFF schema guide: https://github.com/citation-file-format/citation-file-format/blob/main/schema-guide.md
- GitHub citation documentation: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files

## 3. Verified Zenodo distinction

Zenodo's GitHub integration describes and archives GitHub **software releases**. Zenodo supports `CITATION.cff` and `.zenodo.json` as software-release metadata.

Separately, Zenodo's normal deposit workflow accepts multiple research-object types, including **publication** and **software**, and can mint a DOI for a manually uploaded publication record.

Therefore the clean CCTS publication route is:

```text
AION / GitHub repository
  -> optional GitHub Release
  -> optional Zenodo software archive DOI

CCTS manuscript
  -> PDF / archival manuscript package
  -> Zenodo New Upload
  -> resource type = publication / appropriate manuscript subtype
  -> CCTS publication DOI
```

Official references:
- Zenodo GitHub software metadata: https://help.zenodo.org/docs/github/describe-software/
- Zenodo CITATION.cff support: https://help.zenodo.org/docs/github/describe-software/citation-file/
- Zenodo create new upload: https://help.zenodo.org/docs/deposit/create-new-upload/
- Zenodo DOI reservation: https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/

## 4. Repository-specific metadata decision

Current repository state:

```text
ROOT_CITATION_CFF = PRESENT
ROOT_ZENODO_JSON = ABSENT
```

Decision for CCTS preparation:

```text
OVERWRITE_ROOT_CITATION_WITH_CCTS = NO
ADD_ZENODO_JSON_NOW = NO

FUTURE_ROOT_PREFERRED_CITATION_TO_CCTS
= POSSIBLE_AFTER_CCTS_PUBLICATION_METADATA_EXISTS
```

Reason:
- the repository contains substantially more than CCTS;
- replacing the root citation title with CCTS would misdescribe the repository;
- adding a second Zenodo metadata format without need adds precedence/drift risk.

## 5. CCTS manuscript version namespace

The repository already has repository-level release tags such as `v0.1.0-rc.1` and `v0.2.0-rc.1`.

The CCTS scholarly manuscript must use a clearly separate namespace.

```text
CCTS_MANUSCRIPT_VERSION = 0.1.0
PROPOSED_ARTIFACT_LABEL = ccts-scholarly-v0.1.0

CCTS_MANUSCRIPT_VERSION
!= AION_REPOSITORY_VERSION
```

No tag has been created.

## 6. Intended publication sequence

```text
CCTS MANUSCRIPT REVIEW
↓
REFERENCE VERIFICATION
↓
AUTHOR + LICENSE CONFIRMATION
↓
FINAL METADATA EDIT
↓
EXACT CANDIDATE HEAD FREEZE
↓
EXACT-HEAD CI + REVERSE REVIEW
↓
HUMAN OWNER MERGE DECISION
↓
IF MERGED: bind manuscript to exact main commit
↓
PREPARE PDF / ARCHIVAL MANUSCRIPT
↓
ZENODO PUBLICATION DRAFT
↓
OPTIONALLY RESERVE DOI BEFORE FINAL PDF
↓
HUMAN OWNER PUBLISH AUTHORIZATION
↓
PUBLISH CCTS MANUSCRIPT RECORD
↓
CCTS PUBLICATION DOI
↓
OPTIONAL: add CCTS DOI as root CITATION.cff preferred-citation
```

A separate AION GitHub Release / software DOI is optional and is not required to mint the CCTS manuscript DOI.

## 7. Important non-equivalences

```text
GITHUB_CITATION_SUPPORT != PEER_REVIEW
ZENODO_PUBLICATION != PEER_REVIEW
DOI != SCIENTIFIC_VALIDATION
SOFTWARE_RELEASE != MANUSCRIPT_PUBLICATION
SOFTWARE_DOI != MANUSCRIPT_DOI
ARCHIVAL_PUBLICATION != EMPIRICAL_CONFIRMATION
```

## 8. Actions explicitly not performed

```text
MAIN_WRITE = NO
MERGE = NO
TAG = NO
GITHUB_RELEASE = NO
ZENODO_ENABLEMENT = NO
ZENODO_PUBLICATION = NO
DOI = NO
ROOT_CITATION_CHANGE = NO
```
