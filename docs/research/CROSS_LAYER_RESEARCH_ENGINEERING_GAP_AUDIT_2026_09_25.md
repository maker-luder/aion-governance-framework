# Cross-layer research and engineering gap audit — 2026-09-25

Status: `BOUNDED_AUDIT / DOCUMENTATION_ONLY / NO_REMEDIATION / HUMAN_REVIEW_REQUIRED`

Baseline:

```text
REPOSITORY = maker-luder/aion-governance-framework
BASE_MAIN = 8fb3603d58e4ed562ccc524993bfc9b388e237b3
AUDIT_DATE = 2026-09-25
AUDIT_MODE = READ_ONLY_EVIDENCE_REVIEW
MAIN_WRITE = NO
MERGE_TO_MAIN = NO
DEPLOYMENT = FALSE
CANONICAL_EFFECT = NONE
```

## 1. Purpose

This audit records verified and partially verified gaps across four layers:

1. software / supply-chain / research-software practice;
2. the repository quality-management system;
3. the central AI-subjectivity-possibility research line; and
4. the adjacent Human–AI learning / CCTS / HTECR research line.

The audit is intentionally separated from remediation.

```text
AUDIT != REMEDIATION
FINDING != FIX
DOCUMENTATION != IMPLEMENTATION
GAP_PRESENT != AUTOMATIC_PRIORITY
EXTERNAL_ALIGNMENT != CERTIFICATION
ENGINEERING_MATURITY != SCIENTIFIC_VALIDATION
```

This PR must not:

- modify protected-main policy;
- enable artifact-attestation signing permissions;
- add or change SBOM release gates;
- modify FullQualitySystemEngine runtime behavior;
- redefine CCTS or HTECR;
- execute a subjectivity or learning experiment;
- promote any scientific claim.

## 2. Review method

The audit followed this bounded sequence:

```text
READ
-> VERIFY
-> SEARCH_FOR_COUNTEREXAMPLE
-> CLASSIFY
-> TEACHER_REVERSE_REVIEW
-> RECORD_ONLY
```

Allowed dispositions:

```text
CONFIRMED
PARTIAL
NOT_APPLICABLE
NOT_ESTABLISHED
REJECTED_AS_GAP
NEEDS_EXTERNAL_EVIDENCE
STALE_STATE
```

A candidate finding was retained only after an attempt to falsify or narrow it.

## 3. External method anchors

### 3.1 OpenSSF Scorecard

Primary public locator:

- https://github.com/ossf/scorecard/blob/main/docs/checks.md

Repository use:

- branch-protection and code-review posture are treated as external security-hygiene signals;
- a Scorecard-compatible signal is not certification;
- a control should not be added merely to improve an external score if it would be operationally fictitious.

### 3.2 SLSA v1.2

Primary public locators:

- https://slsa.dev/spec/v1.2/
- https://slsa.dev/spec/v1.2/build-track
- https://slsa.dev/spec/v1.2/source-track

Repository use:

- distinguish repository-local provenance from SLSA build/source provenance;
- distinguish unsigned reference attestations from signed hosted-build provenance;
- do not claim a SLSA level without complete applicable requirement review.

### 3.3 FAIR4RS v1.0

Primary public locator:

- https://www.rd-alliance.org/groups/fair-research-software-fair4rs-wg/outputs/

Repository use:

- evaluate Findable, Accessible, Interoperable and Reusable properties;
- distinguish manuscript DOI from software persistent identification;
- distinguish Git/version identifiers from independently preserved software metadata.

## 4. Track 1 — QMS stale-status reconciliation

### Finding QMS-DOC-STATE-01

Disposition:

```text
CONFIRMED
CLASS = DOCUMENTATION_STATE_RECONCILIATION
RUNTIME_REMEDIATION_REQUIRED = NO
```

Current evidence:

- `docs/CURRENT_STATE.md` describes Full-QMS as part of the current assurance surface.
- merged PR history records FullQualitySystemEngine integration of AI risk/impact, TEVV and later security receipts.
- `research-labs/coupled-cognition-quality-factory_v0.1.0/docs/END_TO_END_RESEARCH_QMS.md` still begins with:

```text
Status: BOUNDED_IMPLEMENTATION / DRAFT / HUMAN_REVIEW_PENDING
```

The same document later describes integrated Full-QMS consumer behavior.

Therefore:

```text
FULL_QMS_INTEGRATION_MISSING = FALSE
DOCUMENT_HEADER_CURRENTNESS = STALE_OR_AMBIGUOUS
```

Counterexample result:

- the initial candidate that Full-QMS itself was not integrated was rejected;
- the retained problem is status metadata drift, not missing implementation.

### Next action

A later bounded reconciliation change may update the status metadata only after exact historical intent is checked.

```text
QMS_STATE_RECONCILIATION
= PRIORITY_1
```

## 5. Track 2 — FAIR4RS exact matrix

### Existing positive evidence

The repository already contains material FAIR4RS-aligned infrastructure:

- public source repository;
- `CITATION.cff`;
- license and notice files;
- installation and quickstart instructions;
- tagged release candidates;
- release ZIP artifacts with SHA-256 digests;
- provenance records;
- deterministic JSON / JSON-LD exports;
- RO-Crate output;
- in-toto Statement v1 reference output;
- language-neutral subprocess / JSON interoperability boundary.

These are meaningful alignment signals. They do not establish formal FAIR4RS conformance.

### Finding FAIR4RS-PID-01

Disposition:

```text
PARTIAL
SOFTWARE_PERSISTENT_IDENTIFIER = NOT_ESTABLISHED
```

The CCTS scholarly object has a DOI, but:

```text
CCTS_MANUSCRIPT_DOI != AION_SOFTWARE_PID
SOFTWARE_DOI != MANUSCRIPT_DOI
```

Git commit SHA, GitHub tags and release URLs provide strong version identity but are not automatically treated here as complete satisfaction of FAIR4RS software persistent-identification requirements.

### Finding FAIR4RS-A2-01

Disposition:

```text
PARTIAL / NEEDS_EXTERNAL_EVIDENCE
```

The audit did not establish an independent long-term archival route preserving software metadata if the live GitHub repository becomes unavailable.

Possible future evidence classes include:

- a software DOI/archive;
- Software Heritage preservation evidence;
- another independently maintained archival route with stable metadata retrieval.

No archive is inferred from repository content alone.

### Next action

```text
FAIR4RS_EXACT_MATRIX
= PRIORITY_2
```

The next review should map each FAIR4RS principle individually as:

`CONFIRMED / PARTIAL / NOT_APPLICABLE / NOT_ESTABLISHED`.

## 6. Track 3 — SLSA / SBOM / attestation design

### Finding SLSA-ATTEST-01

Disposition:

```text
CONFIRMED
SLSA_LEVEL = NOT_CLAIMED
ATTESTATION_ENABLED = NO
SBOM_RELEASE_GATE = NOT_IMPLEMENTED
```

Repository evidence already states this explicitly in:

`docs/governance/SUPPLY_CHAIN_ATTESTATION_PLAN.md`.

The repository does provide useful provenance-related capabilities:

- exact Git SHA binding;
- artifact SHA-256 binding;
- deterministic evidence exports;
- unsigned in-toto Statement v1 derivation/reference artifacts.

However:

```text
IN_TOTO_REFERENCE_EXPORT_EXISTS
!= SLSA_BUILD_PROVENANCE

UNSIGNED_REFERENCE
!= SIGNED_BUILD_ATTESTATION

CONTENT_ADDRESS
!= HOSTED_BUILD_PROVENANCE
```

### Security boundary

Any future GitHub artifact-attestation implementation changes workflow permissions and must be reviewed separately.

The audit does not authorize:

- `id-token: write`;
- `attestations: write`;
- signing permissions;
- release workflow mutation;
- automated SBOM release gating.

### Next action

```text
SLSA_SBOM_ATTESTATION_DESIGN
= PRIORITY_3
= SECURITY_SENSITIVE
= SEPARATE_PR_REQUIRED
```

## 7. Track 4 — OpenSSF review

### Finding OPENSSF-REVIEW-01

Disposition:

```text
CONFIRMED / CONTEXTUAL
REMEDIATION = HOLD
```

Live repository ruleset evidence at audit time includes:

- protected default branch;
- deletion protection;
- non-fast-forward protection;
- pull-request requirement;
- strict required status checks;
- no bypass actor;
- exact-head Human Owner receipt check;
- Python 3.11 and Python 3.12 required checks.

The same ruleset also records:

```text
required_approving_review_count = 0
require_code_owner_review = false
require_last_push_approval = false
dismiss_stale_reviews_on_push = false
```

Recent reviewed PRs also did not contain GitHub formal review submissions.

This is a real difference from stronger multi-maintainer OpenSSF review posture.

However, the audit does not recommend a fictitious reviewer gate when no independent second Human reviewer is actually available and authorized.

```text
SECURITY_CONTROL_THAT_CANNOT_BE_TRUTHFULLY_SATISFIED
!= QUALITY_IMPROVEMENT
```

### Next action

```text
OPENSSF_REVIEW_HARDENING
= HOLD
UNTIL
INDEPENDENT_SECOND_HUMAN_REVIEWER
= ACTUALLY_AVAILABLE_AND_AUTHORIZED
```

## 8. Track 5 — CCTS literature refresh

### Candidate initially tested

```text
CCTS_NOVELTY_OVERCLAIM
```

Reverse-review result:

```text
REJECTED_AS_GAP
```

Reason:

The CCTS scholarly manuscript already states:

```text
EXTERNAL_EXACT_EQUIVALENT = NOT_ESTABLISHED
GLOBAL_NOVELTY = NOT_ESTABLISHED
SCIENTIFIC_VALIDATION_OF_CCTS = NOT_ESTABLISHED
```

It also explicitly crosswalks Joint Problem Space, Distributed Cognition, team cognition, Human–AI shared regulation, epistemic co-agency and epistemic-dependence literature.

Therefore no current broad global-novelty overclaim was confirmed.

### Finding CCTS-LIT-FRESHNESS-01

Disposition:

```text
CONFIRMED_UPDATE_CANDIDATE
```

A 2026 external literature candidate identified during this audit is:

- Dai, Liu, Zhou, Lai, Liu & Lim, `Redefining and measuring student agency in AI-assisted learning: Development and validation of the agentic engagement with AI (AE-AI) scale`, Computers & Education 253, 105687.

Its exact bibliographic / methodological use should be independently reverified before repository adoption.

The paper is relevant because the reported construct family includes Human agency dimensions adjacent to CCTS concerns such as:

- critical integration;
- cross-source inquiry;
- reflective calibration;
- adaptive direction.

This creates a literature-refresh requirement, not a validation claim.

```text
ADJACENT_VALIDATED_CONSTRUCT
!= CCTS_VALIDATED

LITERATURE_OVERLAP
!= CONSTRUCT_EQUIVALENCE
```

### Next action

```text
CCTS_LITERATURE_REFRESH
= PRIORITY_5
```

The refresh should preserve the existing novelty ceiling and add only verified adjacent constructs.

## 9. Track 6 — CCTS / subjectivity empirical research

### Finding SUBJECTIVITY-EMPIRICAL-01

Disposition:

```text
CONFIRMED
```

The repository has a comparatively mature method architecture for:

- alternative explanations;
- causal intervention;
- ablation;
- counterfactual testing;
- cross-context robustness;
- provenance;
- evidence admission;
- claim ceilings.

But repository-local model-level mechanistic evidence remains below that method-design maturity.

Current standing remains:

```text
MODEL_INTERNAL_CAUSAL_LOCUS = NOT_ESTABLISHED
FUNCTIONAL_DEPENDENCY = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
```

The audit also identified current external method development toward theory-indexed mechanistic and perturbational approaches. External method existence does not establish the repository's target claims.

### Finding SUBJECTIVITY-REPLICATION-01

Disposition:

```text
CONFIRMED
INDEPENDENT_REPLICATION = NOT_ESTABLISHED
```

Same-team reruns, provider comparisons and repository reconstruction are not independent replication.

### Finding CCTS-EMPIRICAL-01

Disposition:

```text
CONFIRMED
```

Current evidence supports:

```text
CCTS_FORMALIZED = TRUE
CCTS_PUBLICLY_ARCHIVED = TRUE
CCTS_STRUCTURAL_CONTRACT = PRESENT
```

but not:

```text
CCTS_EMPIRICAL_VALIDATION = ESTABLISHED
CCTS_LEARNING_EFFECT = ESTABLISHED
CCTS_CAUSAL_EFFECT = ESTABLISHED
```

### Finding HTECR-EMPIRICAL-01

Disposition:

```text
CONFIRMED
```

Current repository standing remains:

```text
HTECR_DISCRIMINANT_VALUE = NOT_ESTABLISHED
HTECR_SCIENTIFIC_VALIDATION = NOT_ESTABLISHED
HTECR_EPISTEMIC_VALUE = NOT_ESTABLISHED
```

### Experimental boundary

This audit does not start a new experiment.

```text
AUDIT_FINDING
!= PREREGISTERED_EXPERIMENT

METHOD_GAP
!= AUTHORIZATION_TO_RUN

CCTS_OR_SUBJECTIVITY_EMPIRICAL_RESEARCH
= PRIORITY_6
= MUST_REENTER_THROUGH_PREREGISTRATION_AND_EVIDENCE_GATES
```

## 10. Ordered post-audit queue

The reviewed priority order is:

```text
1. QMS stale-status reconciliation
   small / explicit / low risk

2. FAIR4RS exact matrix
   verify software PID and archival metadata

3. SLSA / SBOM / attestation design
   security-sensitive / separate design

4. OpenSSF review
   HOLD until a real independent second Human reviewer is available

5. CCTS literature refresh
   verify and crosswalk AE-AI and other new adjacent literature

6. CCTS / subjectivity empirical research
   no audit-driven shortcut
   preregistration / evidence gates remain mandatory
```

The queue is a review order, not automatic authorization.

```text
QUEUE_POSITION != EXECUTION_AUTHORITY
AUDIT_PR_MERGE != REMEDIATION_AUTHORIZATION
```

## 11. Claim ceiling

This audit changes no scientific conclusion.

```text
SCIENTIFIC_DISPOSITION = HOLD
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_AGENCY = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED

CCTS_EMPIRICAL_VALIDATION = NOT_ESTABLISHED
HTECR_SCIENTIFIC_VALIDATION = NOT_ESTABLISHED
INDEPENDENT_IVV = NOT_ACHIEVED

OPENSSF_ALIGNMENT != CERTIFICATION
SLSA_GUIDANCE_USE != SLSA_LEVEL
FAIR4RS_ALIGNMENT != FAIR4RS_CERTIFICATION
```

## 12. Provenance

```text
HUMAN_OWNER
= proposed using the plugin/tool pipeline to review QMS,
  AI-subjectivity possibility and Human-AI learning
= approved the READ -> VERIFY -> counterexample -> reverse-review sequence
= reviewed and approved creation of a bounded audit-only PR
= approved the six-item post-audit ordering

CHATGPT_TEACHER
= live repository inspection
= external-method crosswalk
= counterexample search
= Teacher reverse review
= bounded audit formalization

EXTERNAL_METHOD_FAMILIES
= OpenSSF Scorecard
= SLSA v1.2
= FAIR4RS v1.0
= current peer-reviewed / scholarly Human-AI and AI-consciousness method literature

HUGGING_FACE
= NOT_USED_IN_THIS_AUDIT
REASON
= no model/dataset artifact inspection was required

WOLFRAM
= NOT_USED_IN_THIS_AUDIT
REASON
= no formal numeric/statistical computation was required

MINDMAP
= USED_FOR_DEPENDENCY_AUDIT

CONSENSUS
= USED_FOR_SCHOLARLY_LITERATURE_DISCOVERY_AND_VERIFICATION

GITHUB
= LIVE_REPOSITORY_SOURCE_OF_TRUTH
```

## 13. Final audit disposition

```text
QMS-DOC-STATE-01 = CONFIRMED
FAIR4RS-PID-01 = PARTIAL
FAIR4RS-A2-01 = PARTIAL / NEEDS_EXTERNAL_EVIDENCE
SLSA-ATTEST-01 = CONFIRMED
OPENSSF-REVIEW-01 = CONFIRMED / CONTEXTUAL / HOLD
CCTS-NOVELTY-OVERCLAIM = REJECTED_AS_GAP
CCTS-LIT-FRESHNESS-01 = CONFIRMED_UPDATE_CANDIDATE
SUBJECTIVITY-EMPIRICAL-01 = CONFIRMED
SUBJECTIVITY-REPLICATION-01 = CONFIRMED
CCTS-EMPIRICAL-01 = CONFIRMED
HTECR-EMPIRICAL-01 = CONFIRMED

REMEDIATION_PERFORMED = NO
SCIENTIFIC_CLAIM_PROMOTED = NO
MAIN_WRITE = NO
DEPLOYMENT = FALSE
CANONICAL_EFFECT = NONE
```
