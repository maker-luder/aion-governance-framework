# CCTS scholarly release route — GitHub + Zenodo (verified 2026-09-24)

Status: `PREPARATION_ONLY / NO_RELEASE_ACTION`

## 1. Verified publication path

Official GitHub documentation states that a root-level `CITATION.cff` file is used by GitHub's **Cite this repository** feature and can generate APA and BibTeX citation output.

Official Zenodo documentation states that:
- a GitHub repository can be enabled for Zenodo integration;
- after enablement, new GitHub releases can be automatically ingested and archived;
- Zenodo supports `CITATION.cff` metadata for GitHub software releases;
- Zenodo also supports `.zenodo.json`;
- if both are present, Zenodo gives `.zenodo.json` precedence and ignores `CITATION.cff` metadata for GitHub release archiving.

Official references:
- GitHub: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files
- Zenodo GitHub integration: https://help.zenodo.org/docs/github/
- Zenodo repository enablement: https://help.zenodo.org/docs/github/enable-repository/
- Zenodo software metadata: https://help.zenodo.org/docs/github/describe-software/

## 2. Repository-specific decision

Current repository state:

```text
ROOT_CITATION_CFF = PRESENT
ROOT_ZENODO_JSON = ABSENT
```

For the first CCTS scholarly release, the preparation plan is therefore:

```text
USE_CITATION_CFF_AS_PRIMARY_METADATA = YES
ADD_ZENODO_JSON_NOW = NO
```

Reason: adding two competing metadata surfaces without a demonstrated need creates avoidable precedence and drift risk.

## 3. Intended release sequence

```text
CCTS MANUSCRIPT REVIEW
↓
REFERENCE VERIFICATION
↓
AUTHOR METADATA CONFIRMATION
↓
EXACT PUBLICATION COMMIT FREEZE
↓
EXACT-HEAD CI CHECK
↓
UPDATE CITATION.cff FOR NEW SCHOLARLY RELEASE
↓
HUMAN OWNER RELEASE AUTHORIZATION
↓
GITHUB RELEASE
↓
ZENODO ARCHIVE / DOI
↓
POST-RELEASE DOI BACKFILL INTO CITATION METADATA IF NEEDED
```

## 4. Important non-equivalences

```text
GITHUB_CITATION_SUPPORT != PEER_REVIEW
ZENODO_ARCHIVE != PEER_REVIEW
DOI != SCIENTIFIC_VALIDATION
SOFTWARE_RELEASE != EMPIRICAL_CONFIRMATION
```

## 5. Actions explicitly not performed by this preparation branch

```text
MAIN_WRITE = NO
MERGE = NO
TAG = NO
GITHUB_RELEASE = NO
ZENODO_ENABLEMENT = NO
ZENODO_PUBLICATION = NO
DOI = NO
```
