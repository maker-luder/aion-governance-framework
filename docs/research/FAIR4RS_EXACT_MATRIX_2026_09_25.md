# FAIR4RS exact matrix — 2026-09-25

Status: `BOUNDED_CROSSWALK / DOCUMENTATION_ONLY / NO_REMEDIATION / HUMAN_REVIEW_REQUIRED`

## 1. Scope

This document maps the repository-level AION research-software object against the FAIR Principles for Research Software (FAIR4RS) v1.0.

```text
ASSESSMENT_TARGET = AION_REPOSITORY_LEVEL_RESEARCH_SOFTWARE_OBJECT
REPOSITORY = maker-luder/aion-governance-framework
BASE_MAIN = 34741cf9869f668e14ff068464a849a3aa65623c
ASSESSMENT_DATE = 2026-09-25

FAIR4RS_VERSION = 1.0
FAIR4RS_REFERENCE_DOI = 10.15497/RDA00068

FORMAL_FAIR4RS_CONFORMANCE = NOT_CLAIMED
CERTIFICATION = NONE
REMEDIATION_PERFORMED = NO
RUNTIME_CHANGE = NO
WORKFLOW_CHANGE = NO
CANONICAL_RESEARCH_CLAIM_EFFECT = NONE
DEPLOYMENT = FALSE
```

The FAIR4RS Principles v1.0 were produced by the FAIR for Research Software Working Group and endorsed by the Research Data Alliance Council as an official output.

Primary public locators:

- https://doi.org/10.15497/RDA00068
- https://www.rd-alliance.org/groups/fair-research-software-fair4rs-wg/outputs/
- https://www.rd-alliance.org/groups/fair-research-software-fair4rs-wg/activity/

This is an evidence crosswalk, not a certification or self-awarded FAIR score.

## 2. Disposition vocabulary

Each FAIR4RS principle is classified using only:

```text
CONFIRMED
PARTIAL
NOT_APPLICABLE
NOT_ESTABLISHED
```

Interpretation:

- `CONFIRMED` — repository evidence satisfies the principle for the assessed repository-level scope.
- `PARTIAL` — meaningful evidence exists, but an identified part of the principle remains incomplete or unverified.
- `NOT_APPLICABLE` — the principle's conditional requirement is not needed for the current public-access route.
- `NOT_ESTABLISHED` — current repository and external evidence do not establish the requirement.

```text
CONFIRMED != CERTIFIED
PARTIAL != FAIL
NOT_ESTABLISHED != PROVEN_ABSENT
ALIGNMENT != CONFORMANCE
```

## 3. Exact FAIR4RS matrix

| Principle | FAIR4RS requirement, abbreviated | Disposition | Repository evidence | Limitation / reason |
|---|---|---|---|---|
| F1 | Software is assigned a globally unique and persistent identifier. | `NOT_ESTABLISHED` | Git repository URL, commit SHA, tags and release URLs identify source states and releases. | No AION software DOI, Software Heritage identifier or other independent globally unique persistent software identifier was established by this review. The CCTS manuscript DOI identifies a scholarly article, not the AION software object. |
| F1.1 | Software components representing levels of granularity have distinct identifiers. | `PARTIAL` | Components use distinct repository paths, package names and component versions; many contain local `pyproject.toml` metadata. | Component-level persistent identifiers were not established. Distinct path/package identity is weaker than persistent identification. |
| F1.2 | Different versions of the software have distinct identifiers. | `PARTIAL` | Git commit SHAs, tags `v0.1.0-rc.1` and `v0.2.0-rc.1`, and distinct GitHub release URLs identify versions. | Repository release identifiers are not independently established as persistent identifiers for FAIR4RS F1. The `v0.2.0-rc.1` tag also contains stale `CITATION.cff` version metadata stating `0.1.0-rc.1`. |
| F2 | Software is described with rich metadata. | `CONFIRMED` | Root `CITATION.cff`, README, installation, API, interoperability, versioning, provenance, license and current-state documentation describe the software and its boundaries. | This disposition does not imply that every component has equally rich standalone metadata. |
| F3 | Metadata clearly and explicitly include the identifier of the software they describe. | `PARTIAL` | `CITATION.cff` explicitly contains `repository-code` for the AION repository. Release/tag metadata provide additional version identity. | Because a FAIR4RS F1 persistent software identifier is not established, the metadata cannot yet bind an established F1 identifier. |
| F4 | Metadata are FAIR, searchable and indexable. | `PARTIAL` | Public GitHub repository metadata, `CITATION.cff`, README and documentation are machine- and human-searchable through the repository platform. | F1 and A2 remain unresolved; therefore the metadata are not represented here as fully FAIR or independently persistent. |
| A1 | Software is retrievable by its identifier using a standardized communications protocol. | `PARTIAL` | Public GitHub repository, commit, tag and release URLs are retrievable over HTTPS. Release assets are directly downloadable. | Retrieval currently depends on repository/platform identifiers rather than an established FAIR4RS F1 persistent software identifier. |
| A1.1 | The protocol is open, free and universally implementable. | `CONFIRMED` | Public repository and release retrieval use HTTPS. | Platform availability is distinct from protocol openness. |
| A1.2 | The protocol supports authentication and authorization where necessary. | `NOT_APPLICABLE` | The assessed public source/release retrieval path does not require authentication. | This does not assess private administrative or maintainer operations. |
| A2 | Metadata remain accessible even when the software is no longer available. | `NOT_ESTABLISHED` | Current metadata are accessible while the live GitHub repository is available. | No independent long-term archival route preserving AION software metadata after loss of the live repository was established. Public searches did not establish a Software Heritage preservation record or an AION software archive/DOI; absence is not asserted. |
| I1 | Software reads, writes and exchanges data in ways meeting domain-relevant community standards. | `PARTIAL` | The repository exposes deterministic JSON, JSON-LD, JSONL, RO-Crate, in-toto Statement v1 reference output, OPA input and a language-neutral subprocess/JSON boundary. | Repository-wide domain-standard interoperability across all components is not established. Some outputs are reference integrations rather than certified implementations. |
| I2 | Software includes qualified references to other objects. | `PARTIAL` | Provenance records, source references, configuration references, exact Git bindings, manifests, citation metadata and content digests provide typed or contextual references to related objects. | A repository-wide qualified-reference model using persistent identifiers for all external objects is not established. |
| R1 | Software is described with a plurality of accurate and relevant attributes. | `CONFIRMED` | README, `CITATION.cff`, API, installation, quickstart, interoperability, versioning, provenance, current-state and non-claim documentation describe purpose, scope, interfaces and limitations. | Accuracy is bounded to current documented repository evidence and does not imply external validation. |
| R1.1 | Software has a clear and accessible license. | `CONFIRMED` | Root `LICENSE` is Apache-2.0; `NOTICE` and `THIRD_PARTY_NOTICES.md` identify separately licensed material. The optional Swiss Ephemeris example is explicitly AGPL-3.0-only. | The repository must not be described as uniformly Apache-only because of the explicitly separated optional AGPL example. |
| R1.2 | Software is associated with detailed provenance. | `CONFIRMED` | `docs/PROVENANCE.md`, Git history, exact-head controls, SHA-256 manifests, source-role records, evidence manifests and release hashes provide detailed provenance. | Provenance does not establish identity, authorship beyond recorded evidence, scientific truth or independent IV&V. |
| R2 | Software includes qualified references to other software. | `PARTIAL` | Dependency metadata, `THIRD_PARTY_NOTICES.md`, `DEPENDENCY_LICENSE_REPORT.json`, component `pyproject.toml` files and pinned external revisions identify software dependencies and related software. | Not every software relationship is represented by a persistent, qualified machine-readable reference. |
| R3 | Software meets domain-relevant community standards. | `PARTIAL` | The repository uses common research-software practices including structured citation metadata, explicit licensing, versioning, provenance, reproducible commands, public APIs, checksums and interoperable evidence formats. | Complete conformance to all domain-relevant community standards is not established and is intentionally not claimed. |

## 4. Overall disposition

The repository shows substantial FAIR4RS-aligned infrastructure, especially in metadata richness, licensing, provenance, reproducibility documentation and interoperable evidence export.

The strongest bounded conclusion is:

```text
FAIR4RS_OVERALL = PARTIAL / SUBSTANTIAL_ALIGNMENT
FAIR4RS_CONFORMANCE = NOT_ESTABLISHED

FINDABLE = PARTIAL
ACCESSIBLE = PARTIAL
INTEROPERABLE = PARTIAL
REUSABLE = STRONG_PARTIAL
```

This summary is descriptive. It is not a FAIR score, certification, ranking or external endorsement.

## 5. Persistent-identifier gap

### FAIR4RS-PID-01

```text
DISPOSITION = CONFIRMED_GAP
SOFTWARE_PERSISTENT_IDENTIFIER = NOT_ESTABLISHED

CCTS_MANUSCRIPT_DOI = 10.5281/zenodo.22945883
CCTS_MANUSCRIPT_DOI != AION_SOFTWARE_PID
SOFTWARE_DOI != MANUSCRIPT_DOI
GIT_COMMIT_SHA != AUTOMATIC_FAIR4RS_SOFTWARE_PID
GITHUB_RELEASE_URL != AUTOMATIC_FAIR4RS_SOFTWARE_PID
```

The repository has strong source-state identity through Git, but this review did not establish an independently maintained persistent identifier for the repository-level software object.

## 6. Metadata-persistence gap

### FAIR4RS-A2-01

```text
DISPOSITION = NOT_ESTABLISHED
INDEPENDENT_ARCHIVAL_METADATA_PERSISTENCE = NOT_ESTABLISHED
SOFTWARE_HERITAGE_PRESERVATION = NOT_ESTABLISHED
AION_SOFTWARE_DOI = NOT_ESTABLISHED
```

The review did not establish that software metadata remain independently retrievable if the live GitHub repository disappears.

Possible future evidence classes include:

- an archival software DOI;
- a verified Software Heritage preservation record and persistent identifier;
- another independently maintained archive preserving software metadata and version identity.

```text
SEARCH_NO_RESULT != PROOF_OF_ABSENCE
ARCHIVE_CLAIM_REQUIRES_POSITIVE_EVIDENCE
```

## 7. Release-metadata drift

### FAIR4RS-RELEASE-METADATA-01

The repository has two GitHub prereleases with downloadable ZIP assets and SHA-256 sidecars:

```text
v0.1.0-rc.1
v0.2.0-rc.1
```

However, the `v0.2.0-rc.1` tag's retained root `CITATION.cff` contains:

```text
version: "0.1.0-rc.1"
date-released: "2026-08-07"
```

Therefore:

```text
FAIR4RS-RELEASE-METADATA-01 = CONFIRMED
RELEASE_TAG_VERSION = v0.2.0-rc.1
CITATION_VERSION_METADATA = 0.1.0-rc.1
RELEASE_TAG_VERSION != CITATION_VERSION_METADATA
```

This is recorded as historical release-metadata drift. This PR does not retag or rewrite the historical release.

```text
HISTORICAL_TAG_MUTATION = NO
RELEASE_REWRITE = NO
```

## 8. Existing positive evidence inventory

Current evidence supporting FAIR4RS alignment includes:

- public source repository;
- root `CITATION.cff`;
- Apache-2.0 core license and explicit optional AGPL scope;
- `NOTICE` and third-party notices;
- installation and quickstart instructions;
- API and interoperability documentation;
- component-local package metadata;
- Git commit and tag version identity;
- GitHub prerelease assets;
- SHA-256 release sidecars;
- provenance records;
- file and package manifests;
- deterministic JSON / JSON-LD / JSONL exports;
- RO-Crate metadata output;
- in-toto Statement v1 reference output;
- language-neutral subprocess / JSON interoperability;
- exact-head validation and content-addressed evidence bindings.

These support the individual dispositions above; they do not establish formal FAIR4RS certification.

## 9. Scope boundary

This matrix records evidence only.

It does not perform:

```text
NO_SOFTWARE_DOI_MINTING
NO_ZENODO_SOFTWARE_RELEASE
NO_SOFTWARE_HERITAGE_CLAIM_WITHOUT_EVIDENCE
NO_RELEASE_RETAGGING
NO_HISTORICAL_RELEASE_REWRITE
NO_CITATION_CFF_REMEDIATION
NO_RUNTIME_CHANGE
NO_WORKFLOW_CHANGE
NO_DEPENDENCY_CHANGE
NO_FAIR4RS_CERTIFICATION_CLAIM
```

The following separations remain mandatory:

```text
AUDIT_MATRIX != REMEDIATION
ALIGNMENT != CONFORMANCE
MANUSCRIPT_DOI != SOFTWARE_PID
GIT_TAG != AUTOMATIC_PERSISTENT_IDENTIFIER
REPOSITORY_URL != AUTOMATIC_PERSISTENT_IDENTIFIER
RELEASE_ASSET_HASH != ARCHIVAL_PERSISTENCE
```

## 10. Scientific and authority boundaries

FAIR4RS evaluates research-software findability, accessibility, interoperability and reusability. It does not evaluate whether the repository's scientific hypotheses are true.

```text
FAIR4RS_ALIGNMENT != SCIENTIFIC_VALIDATION
FAIR4RS_ALIGNMENT != SUBJECTIVITY_EVIDENCE
METADATA_QUALITY != CLAIM_TRUTH
REUSABILITY != INDEPENDENT_REPLICATION

SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_AGENCY = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED

CI_PASS != MERGE_AUTHORITY
AI_REVIEW != HUMAN_OWNER_APPROVAL
```

## 11. Provenance

```text
HUMAN_OWNER
= authorized proceeding to the FAIR4RS exact-matrix remediation-record step
= approved the bounded design before repository write

CHATGPT_TEACHER
= read current repository evidence
= cross-checked FAIR4RS v1.0 against official RDA sources
= formalized the 17-principle exact matrix
= performed external searches for archive/PID evidence without converting no-result searches into absence claims

EXTERNAL_SOURCE
= Research Data Alliance FAIR4RS v1.0
= DOI 10.15497/RDA00068

REMEDIATION_PERFORMED = NO
MERGE_TO_MAIN = NO
DEPLOYMENT = FALSE
CANONICAL_EFFECT = NONE
```
