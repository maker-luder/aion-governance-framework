# SLSA / SBOM / artifact-attestation architecture — design spec — 2026-09-25

Status: `DESIGN_SPEC / DOCUMENTATION_ONLY / SECURITY_SENSITIVE / HUMAN_REVIEW_REQUIRED`

```text
BASE_MAIN_HEAD = 55bddfefa76640b987a3d940e22a82b2e60c91e8

IMPLEMENTATION = NONE
WORKFLOW_MUTATION = NONE
PERMISSION_EXPANSION = NONE
SBOM_GENERATION = NONE
ATTESTATION_GENERATION = NONE
RELEASE_PUBLICATION = NONE

PUBLIC_RELEASE_PIPELINE = STOPPED
NEW_PUBLIC_RELEASES = NOT_AUTHORIZED
NEW_RELEASE_TAGS = NOT_AUTHORIZED

ATTESTATION_ENABLED = NO
SBOM_RELEASE_GATE = NOT_IMPLEMENTED
SLSA_LEVEL = NOT_CLAIMED
SPDX_CONFORMANCE = NOT_CLAIMED
THIRD_PARTY_LICENSE_COMPATIBILITY = REVIEW_REQUIRED

WRITE_TO_MAIN = NO
MERGE = NO
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE

SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_AGENCY = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED
```

This document records the approved architecture for a future software-supply-chain
provenance path around AION release artifacts. It does not enable GitHub artifact
attestations, generate an SBOM, publish a release, grant a SLSA level, or expand any
workflow permission.

The Human Owner approved the design direction in chat before this file was written.

## 1. Design intent

The design problem is:

> How should AION eventually bind a governed release artifact to source state,
> dependency inventory, build provenance, and independently replayable verification,
> while preserving least privilege and without turning attestation success into
> release authority, security certification, scientific validation, or a SLSA claim?

Success requires all of the following:

1. define the release subject before any provenance is generated;
2. separate unprivileged build/SBOM work from privileged attestation work;
3. keep normal pull-request CI unable to mint attestations;
4. preserve exact source SHA and artifact SHA-256 binding;
5. produce a machine-readable SBOM using an established ecosystem format;
6. verify provenance and SBOM attestations independently of the generation step;
7. record verification results in a release-evidence record;
8. keep Human Owner release authority external to CI/attestation success;
9. keep SLSA level assessment as a separate conformance step;
10. preserve the repository's stopped-release state until separately reauthorized.

## 2. Existing repository ancestry

This design reuses existing controls instead of creating a parallel trust model.

### 2.1 Existing supply-chain plan

`docs/governance/SUPPLY_CHAIN_ATTESTATION_PLAN.md` already states:

```text
ATTESTATION_ENABLED = NO
SBOM_RELEASE_GATE = NOT_IMPLEMENTED
SLSA_LEVEL = NOT_CLAIMED
SPDX_CONFORMANCE = NOT_CLAIMED
THIRD_PARTY_LICENSE_COMPATIBILITY = REVIEW_REQUIRED
```

It also records the preferred future order:

```text
source commit
-> CI build
-> artifact digest
-> SBOM
-> signed build provenance / attestation
-> verification instructions
-> release evidence index
```

This design formalizes that direction but does not activate it.

### 2.2 Existing read-only CI posture

At the design baseline, `.github/workflows/quality.yml` has:

```yaml
permissions:
  contents: read
```

The design preserves this posture for normal quality/test workflows.

### 2.3 Existing deterministic evidence exports

`components/aion_evidence_interop_v0.1.0` already produces an
`attestation.intoto.json` using in-toto Statement v1 structure.

That output is explicitly:

```text
SIGNATURE_STATUS = UNSIGNED_REFERENCE
```

Therefore:

```text
EXISTING_INTOTO_REFERENCE
!= GITHUB_ARTIFACT_ATTESTATION

UNSIGNED_REFERENCE
!= SIGNED_BUILD_PROVENANCE

DETERMINISTIC_EXPORT
!= HOSTED_BUILD_PROVENANCE
```

The existing exporter remains useful evidence infrastructure but is not promoted into
a SLSA provenance implementation.

### 2.4 Current release freeze

`PUBLIC_RELEASE_POLICY.md` states:

```text
PUBLIC_RELEASE_PIPELINE = STOPPED
NEW_PUBLIC_RELEASES = NOT_AUTHORIZED
NEW_RELEASE_CANDIDATES = NOT_AUTHORIZED
NEW_RELEASE_TAGS = NOT_AUTHORIZED
```

This architecture is therefore preparatory only.

## 3. External method anchors

### 3.1 GitHub artifact attestations

Current GitHub documentation specifies the minimum workflow permissions for artifact
attestation generation as:

```yaml
permissions:
  contents: read
  id-token: write
  attestations: write
```

Container publication additionally requires package-registry permissions such as
`packages: write`; this design does not assume a container release.

Current GitHub documentation also supports SBOM attestations by providing an SBOM path
to the attestation action and supports independent verification through GitHub
attestation verification tooling.

Design consequence:

```text
ATTESTATION_PERMISSION_EXPANSION
= SECURITY_SENSITIVE

ATTESTATION_PERMISSION_EXPANSION
!= NORMAL_CI_PERMISSION
```

Primary source:
https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations

### 3.2 SLSA v1.2

SLSA v1.2 is the current approved specification at the time of this design.

Build-track summary:

```text
BUILD_L0 = no requirements
BUILD_L1 = provenance exists
BUILD_L2 = signed provenance from a hosted build platform
BUILD_L3 = hardened build platform
```

This design does not pre-admit any AION SLSA level.

```text
GITHUB_ATTESTATION_PRESENT
!= AUTOMATIC_SLSA_LEVEL

SLSA_LEVEL
= SEPARATE_REQUIREMENTS_ASSESSMENT
```

Primary sources:
https://slsa.dev/spec/v1.2/
https://slsa.dev/spec/v1.2/build-track-basics
https://slsa.dev/spec/v1.2/provenance

### 3.3 SPDX

The current SPDX specification family is 3.0. GitHub's current artifact-attestation
documentation also documents SBOM attestation interoperability with SPDX-formatted
SBOMs.

For initial AION implementation design, the format family is fixed while the exact
version is deliberately deferred until the selected generator and GitHub attestation
path are reverified together.

```text
PREFERRED_SBOM_FAMILY = SPDX
EXACT_SBOM_VERSION = DEFERRED_TO_IMPLEMENTATION_REVERIFICATION
```

A likely initial implementation candidate is SPDX 2.3 JSON if that remains the most
interoperable combination with the selected generator and GitHub attestation
verification path.

```text
SPDX_3_X_CURRENT_STANDARD
!= AUTOMATIC_TOOLCHAIN_COMPATIBILITY
```

Primary source:
https://spdx.dev/use/specifications/

## 4. Chosen architecture

The approved architecture is a four-stage evidence chain with privilege separation.

```text
ARTIFACT DEFINITION GATE
        |
        v
UNPRIVILEGED BUILD + SBOM
        |
        v
PRIVILEGED ATTESTATION
        |
        v
READ-ONLY VERIFICATION
        |
        v
RELEASE EVIDENCE RECORD
        |
        v
HUMAN OWNER RELEASE DECISION
```

This replaces the rejected design of adding attestation permissions directly to the
normal Quality workflow.

## 5. Artifact-definition gate

Attestation must not begin until the release subject is explicit.

The future implementation must define:

- release artifact path/name;
- artifact type;
- exact source commit;
- build command / workflow identity;
- expected output count;
- content digest algorithm;
- whether the artifact is source archive, built package, binary, or another governed
  release object;
- whether an SBOM describes one subject or multiple subjects.

Fail-closed rule:

```text
OFFICIAL_RELEASE_ARTIFACT = UNSPECIFIED
-> DO_NOT_ATTEST
```

The repository currently contains historical ZIP release artifacts, but this design
does not assume that a future release must use the same packaging form.

```text
HISTORICAL_RELEASE_SHAPE
!= FUTURE_RELEASE_REQUIREMENT
```

## 6. Stage A — unprivileged build and SBOM generation

Purpose:

- materialize the exact governed subject artifact;
- calculate SHA-256;
- generate a machine-readable SBOM;
- validate that the SBOM structurally describes the intended artifact;
- expose outputs to the later privileged job without granting attestation authority.

Target permission posture:

```yaml
permissions:
  contents: read
```

Prohibited permissions in Stage A:

```text
id-token: write = NO
attestations: write = NO
contents: write = NO
packages: write = NO
```

The future implementation should prefer an established SBOM generator over a custom
AION dependency-discovery engine.

Reason:

```text
CUSTOM_SBOM_DISCOVERY
= NEW_MAINTENANCE_SURFACE
+ HIGHER_OMISSION_RISK
+ DUPLICATE_ECOSYSTEM_WORK
```

The exact generator is not selected in this design. When selected, its action or
binary must be version-pinned according to repository supply-chain policy.

### 6.1 Required Stage A outputs

A future Stage A result should include at least:

```text
SOURCE_HEAD
ARTIFACT_NAME
ARTIFACT_SHA256
SBOM_PATH
SBOM_SHA256
SBOM_FORMAT
SBOM_VERSION
BUILD_WORKFLOW_IDENTITY
BUILD_RUN_ID
```

### 6.2 Dependency/license separation

SBOM generation is inventory evidence only.

```text
SBOM_PRESENT
!= DEPENDENCIES_SECURE

SBOM_PRESENT
!= LICENSE_COMPATIBILITY

SPDX_IDENTIFIER
!= LICENSE_COMPATIBILITY_DECISION
```

Existing `DEPENDENCY_LICENSE_REPORT.json`,
`MODEL_AND_DATA_LICENSE_REPORT.md`, and third-party notices remain distinct
review inputs.

## 7. Stage B — isolated privileged attestation

The attestation job is the only proposed location for attestation-writing
permissions.

Minimum intended permissions:

```yaml
permissions:
  contents: read
  id-token: write
  attestations: write
```

For the current non-container design:

```text
packages: write = NOT_REQUIRED
contents: write = NOT_REQUIRED
```

The job must receive only reviewed outputs from the preceding governed build path.

It must not be a generic arbitrary-artifact signing service.

### 7.1 Pull-request firewall

The privileged attestation path must not run for untrusted pull-request code.

```text
PULL_REQUEST_EVENT
-> PRIVILEGED_ATTESTATION = BLOCKED

PULL_REQUEST_TARGET
-> PRIVILEGED_ATTESTATION = BLOCKED

UNTRUSTED_PR_CODE
-> OIDC_ATTESTATION_CONTEXT = FORBIDDEN
```

Normal PR Quality and CodeQL remain read-only and cannot mint attestations.

### 7.2 Subject binding

Before attestation, the privileged job must recompute or independently consume the
subject digest and confirm exact source binding.

Required relationship:

```text
ATTESTED_SUBJECT_SHA256
=
VERIFIED_RELEASE_ARTIFACT_SHA256
```

No filename-only binding is sufficient.

### 7.3 Attestation classes

The first implementation design may produce two logically separate attestations:

1. build provenance for the release subject;
2. SBOM attestation binding the SBOM to that same subject.

```text
BUILD_PROVENANCE_ATTESTATION
!= SBOM_ATTESTATION
```

Both may describe the same subject digest while carrying different predicates.

## 8. Stage C — read-only independent verification

Verification must be a distinct stage from generation.

Purpose:

- verify attestation authenticity;
- verify repository/source identity;
- verify subject digest;
- verify expected workflow identity;
- verify exact commit relation;
- verify SBOM predicate type;
- verify the SBOM artifact can be retrieved/read;
- preserve verification evidence.

This stage should not require attestation-write permission.

```text
VERIFY_JOB_WRITE_ATTESTATION = NO
```

The verification path should use supported GitHub attestation verification
mechanisms rather than trusting JSON presence alone.

```text
ATTESTATION_FILE_PRESENT
!= ATTESTATION_VERIFIED

SIGNATURE_PRESENT
!= EXPECTED_SIGNER_IDENTITY_VERIFIED
```

GitHub documentation explicitly notes that meaningful verification requires
cryptographic verification and signer-identity validation.

## 9. Stage D — release-evidence record

After successful build, SBOM, attestation, and verification, a release-evidence
record should bind the whole chain.

Minimum conceptual fields:

```text
repository
source_head
workflow_identity
workflow_run_id

artifact_name
artifact_sha256

sbom_format
sbom_version
sbom_sha256

build_attestation_reference
sbom_attestation_reference

verification_status
verification_evidence_reference

test_evidence_refs
security_scan_refs
license_review_status

human_release_authority_reference
canonical_effect
deployment
```

The evidence record must not manufacture Human authority.

```text
ATTESTATION_PASS
!= HUMAN_OWNER_RELEASE_APPROVAL

VERIFY_PASS
!= HUMAN_OWNER_RELEASE_APPROVAL
```

## 10. Human authority boundary

No supply-chain mechanism in this design creates release or main-transition
authority.

```text
OIDC_IDENTITY
!= HUMAN_OWNER_IDENTITY

SIGNED_PROVENANCE
!= RELEASE_AUTHORIZATION

SBOM_ATTESTATION
!= RELEASE_AUTHORIZATION

SLSA_CONFORMANCE
!= RELEASE_AUTHORIZATION

CI_PASS
!= RELEASE_AUTHORIZATION
```

A future release still requires separate fresh Human Owner authority after all
technical gates have settled.

## 11. SLSA conformance boundary

Implementation and conformance assessment are separate.

Proposed order:

```text
IMPLEMENT_PROVENANCE_PIPELINE
-> VERIFY_PIPELINE
-> COLLECT_EVIDENCE
-> SEPARATE_SLSA_REQUIREMENTS_ASSESSMENT
-> ONLY_THEN CLAIM OR DECLINE LEVEL
```

Until that assessment:

```text
SLSA_LEVEL = NOT_CLAIMED
```

The existence of GitHub-generated attestations may be relevant evidence for SLSA
Build requirements, but no level is inferred from tool choice alone.

## 12. FAIR4RS separation

This architecture does not resolve FAIR4RS archival persistence by itself.

GitHub artifact attestations are hosted repository evidence and may be managed or
deleted; they are not treated here as an independent archival route.

```text
GITHUB_ARTIFACT_ATTESTATION
!= INDEPENDENT_LONG_TERM_ARCHIVE

SLSA_PROVENANCE
!= FAIR4RS_A2_ARCHIVAL_PERSISTENCE
```

Therefore the previously recorded FAIR4RS A2 status remains a separate issue.

## 13. Failure model

Future implementation must fail closed for at least these conditions:

```text
OFFICIAL_ARTIFACT_UNDEFINED
ARTIFACT_DIGEST_MISMATCH
SOURCE_HEAD_MISMATCH
SBOM_GENERATION_FAILURE
SBOM_PARSE_FAILURE
SBOM_SUBJECT_MISMATCH
ATTESTATION_GENERATION_FAILURE
ATTESTATION_VERIFY_FAILURE
UNEXPECTED_REPOSITORY_IDENTITY
UNEXPECTED_WORKFLOW_IDENTITY
UNEXPECTED_SOURCE_COMMIT
UNEXPECTED_PREDICATE_TYPE
PRIVILEGED_EVENT_NOT_ALLOWED
RELEASE_AUTHORITY_MISSING
```

Failure of a supply-chain gate must not mutate release state automatically.

## 14. Event and privilege model

Preferred future trigger model:

```text
NORMAL_PULL_REQUEST
-> Quality / CodeQL only
-> read-only

GOVERNED_RELEASE_CANDIDATE_EVENT
-> explicit exact source head
-> artifact-definition gate
-> unprivileged build/SBOM
-> isolated attestation
-> read-only verification
-> evidence record
-> Human Owner decision
```

The exact trigger mechanism is deferred to implementation review.

This design specifically does not authorize:

- `pull_request_target` execution of untrusted release-building code;
- automatic attestation on every push;
- automatic release on successful attestation;
- automatic merge;
- automatic tag creation.

## 15. Implementation phases

### Phase 1 — artifact + SBOM preparation

Security posture:

```text
PRIVILEGED_PERMISSION_CHANGE = NO
```

Deliverables:

- exact release-subject definition;
- reproducible artifact build;
- SHA-256 binding;
- selected/pinned SBOM generator;
- SBOM structural validation;
- local/read-only verification.

### Phase 2 — privileged artifact attestation

Security posture:

```text
SECURITY_SENSITIVE = YES
id-token: write = REQUIRED_CANDIDATE
attestations: write = REQUIRED_CANDIDATE
```

Deliverables:

- isolated attestation job;
- event restrictions;
- exact subject digest binding;
- build provenance attestation;
- SBOM attestation.

This phase requires a separate PR and focused permissions review.

### Phase 3 — independent verification and evidence binding

Deliverables:

- supported attestation verification command/path;
- repository/workflow/source/digest checks;
- SBOM predicate verification;
- machine-readable release-evidence record.

### Phase 4 — SLSA assessment

Deliverable:

- separate requirement-by-requirement SLSA v1.2 assessment.

No level is preselected.

### Phase 5 — release decision/publication

Precondition:

```text
PUBLIC_RELEASE_PIPELINE
= EXPLICITLY_REAUTHORIZED_BY_HUMAN_OWNER
```

Release publication remains outside this design's authority.

## 16. Verification strategy for future implementation

A future implementation plan should include tests for:

1. permission minimization;
2. pull-request event rejection;
3. exact source SHA binding;
4. artifact digest reproducibility;
5. SBOM parser/format validation;
6. artifact/SBOM subject consistency;
7. attestation verification;
8. signer/repository/workflow identity expectations;
9. negative digest tampering;
10. negative source-head drift;
11. negative predicate substitution;
12. missing Human release authority;
13. no automatic release mutation on technical success.

Required negative invariant:

```text
TECHNICAL_SUCCESS_WITHOUT_HUMAN_AUTHORITY
-> HOLD
```

## 17. Rejected alternatives

### 17.1 Add permissions directly to Quality

Rejected.

Reason:

```text
NORMAL_CI_PERMISSION_EXPANSION
= UNNECESSARY_BLAST_RADIUS
```

The existing read-only Quality workflow should not gain OIDC/attestation-writing
authority merely because supply-chain provenance is being added elsewhere.

### 17.2 Build a custom AION SBOM generator

Rejected as the default.

Reason:

- duplicates established ecosystem functionality;
- adds dependency-discovery maintenance burden;
- increases omission risk across Python, Node, optional examples, and future package
  types.

### 17.3 Claim a SLSA level during implementation

Rejected.

Reason:

```text
IMPLEMENTATION_FEATURE
!= REQUIREMENTS_CONFORMANCE
```

### 17.4 Treat GitHub attestations as archival persistence

Rejected.

Reason:

```text
HOSTED_ATTESTATION
!= INDEPENDENT_ARCHIVE
```

## 18. Tool routing for this design

```text
CHANGE_CLASS = E
TYPE = GOVERNANCE / SECURITY ARCHITECTURE
IMPLEMENTATION = DOCUMENTATION_ONLY

GitHub = REQUIRED / USED
Superpowers = REQUIRED / USED

Context7 = CONDITIONAL / TRIGGERED / USED
REASON =
CURRENT_GITHUB_ACTIONS_PERMISSION
+ ARTIFACT_ATTESTATION_SYNTAX
+ VERSION_SENSITIVE_BEHAVIOR

Official GitHub Docs = USED
Official SLSA v1.2 = USED
Official SPDX specification page = USED

Codex Security =
CONDITIONAL / TRIGGER_PRESENT / NOT_AVAILABLE_IN_CURRENT_CONNECTED_TOOLSET / NOT_USED

Consensus = DO_NOT_USE_BY_DEFAULT / NOT_USED
Scite = DO_NOT_USE_BY_DEFAULT / NOT_USED
MindMap = NOT_NEEDED / NOT_USED
Wolfram = NOT_NEEDED / NOT_USED
Hugging Face = NOT_NEEDED / NOT_USED
```

Unavailable-tool rule:

```text
TRIGGERED_TOOL_NOT_AVAILABLE
-> RECORD_NOT_AVAILABLE
-> USE_JUSTIFIED_SUBSTITUTE_OR_HOLD
-> NEVER_PRETEND_TOOL_RAN
```

For this design, live GitHub evidence, current GitHub documentation, Context7, SLSA
v1.2, and SPDX documentation provide the substitute review surface.

## 19. Security and scientific non-claims

```text
DESIGN != IMPLEMENTATION
DESIGN_APPROVAL != WORKFLOW_PERMISSION_APPROVAL
DESIGN_APPROVAL != RELEASE_APPROVAL

SBOM != SECURITY_CERTIFICATION
ATTESTATION != SECURITY_CERTIFICATION
SLSA != SCIENTIFIC_VALIDATION

ENGINEERING_PROVENANCE
!= SUBJECTIVITY_EVIDENCE

SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_AGENCY = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED
```

## 20. Provenance

```text
HUMAN_OWNER
= selected PASS for the architectural design direction
= authorized writing the design spec only
= did not authorize workflow mutation or release publication

CHATGPT_TEACHER
= inspected live repository supply-chain and workflow state
= formalized privilege-separated architecture
= cross-checked current GitHub artifact-attestation requirements
= cross-checked SLSA v1.2 build-track semantics
= cross-checked current SPDX specification family

EXTERNAL_SOURCES
= GitHub Docs
= SLSA v1.2
= SPDX specification index

IMPLEMENTATION_SOURCE = NONE
WORKFLOW_MUTATION = NONE
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```
