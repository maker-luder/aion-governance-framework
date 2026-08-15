# POL-UPSTREAM-SUPPLIER-TRUST-001 — QA Evidence Index — 2026-08-08

- `STATUS = BRANCH_CANDIDATE_QA_INDEX`
- `REVIEWED_BASELINE = main@121d01e12adb7fd7c7a1da1233571773610feb33`
- `IMPLEMENTATION = NONE`
- `ACTIVE_ENFORCEMENT = NOT_ENABLED`
- `FROZEN_RELEASE_MANIFEST_MUTATION = NONE`

## Package integrity

This policy package uses package-specific integrity references without modifying the frozen release manifest.

For unchanged files from the first branch candidate, the previously recorded SHA-256 remains valid. For files changed by NCR-SUP-003 / NCR-SUP-004 / NCR-SUP-005 CAPA, the exact current Git blob object ID is recorded for the branch candidate and supersedes the earlier package entry for review purposes.

| Path | Integrity reference | Status |
|---|---|---|
| `docs/governance/POL_UPSTREAM_SUPPLIER_TRUST_001.md` | `git-blob:66bb3ec3dd287187852183edfffd05fe07c79cf5` | CURRENT_AFTER_NCR_SUP_003 |
| `docs/evidence/standards/POL_UPSTREAM_SUPPLIER_TRUST_001_CROSSWALK_2026-08-08.md` | `git-blob:d02f9c92119a45a48ec2878cbf94675ce364818c` | CURRENT_AFTER_NCR_SUP_003 |
| `docs/history/reconciliation/POL_UPSTREAM_SUPPLIER_TRUST_001_FREEZE_AND_CHANGE_CONTROL_2026-08-08.md` | `git-blob:a42f958f06dada1d7d14213cb3a26d941aaf81df` | CURRENT_AFTER_NCR_SUP_003_004_005 |
| `docs/history/reconciliation/POL_UPSTREAM_SUPPLIER_TRUST_001_IMPLEMENTATION_ACCEPTANCE_v0.1_FROZEN_2026-08-08.md` | `sha256:c09c40a04209db3c3d8cd8b9edd7559d537f6045f99983a5c220bbdc353ab3b1` | UNCHANGED |
| `docs/history/reconciliation/POL_UPSTREAM_SUPPLIER_TRUST_001_POLICY_ACCEPTANCE_2026-08-08.md` | `sha256:d195b4233cecb638be5dba4174374f14828aa2a0bf0f29515c0df789e9e00937` | UNCHANGED |
| `docs/evidence/verification/POL_UPSTREAM_SUPPLIER_TRUST_001_VALIDATION_RECORD_2026-08-08.md` | `git-blob:09b91ad113cdc2c426945b4d5ae3528e8c492359` | CURRENT_AFTER_NCR_SUP_004 |
| `qa/POL_UPSTREAM_SUPPLIER_TRUST_001_OWNER_REVIEW_RECORD_2026-08-08.md` | `sha256:3658c05bbeb80d8a0ba2db1ab9fa62de533b63fdf53d33d0b6d302beb5c582a0` | UNCHANGED |

The QA index itself is not self-hashed inside its own content.

## Policy canonicalization criteria

| Criterion | Candidate evidence | Status |
|---|---|---|
| PC-01 | Normative policy contains no hard-coded vendor branch | PASS |
| PC-02 | Evidence class / strength separated; Anthropic enum drift corrected by NCR-SUP-004 | PASS |
| PC-03 | Default scope propagation denied | PASS |
| PC-04 | Owner context cannot rewrite evidence | PASS |
| PC-05 | No permanent immunity / automatic condemnation | PASS |
| PC-06 | Methodological incompatibility separated from security failure | PASS |
| PC-07 | Supplier risk separated from project impact | PASS |
| PC-08 | Disposition states declared non-linear | PASS |
| PC-09 | Relational continuity separated from authority | PASS |
| PC-10 | Remediation separated from incident erasure | PASS |
| PC-11 | Public package excludes private Owner deliberation detail | PASS |
| PC-12 | Named vendors isolated in validation record | PASS |
| PC-13 | Crosswalk contains explicit non-certification boundaries | PASS |
| PC-14 | Existing upstream security and writeback gates remain authoritative layers | PASS |
| PC-15 | `IMPLEMENTATION = NONE`; `ACTIVE_ENFORCEMENT = NOT_ENABLED` | PASS |
| PC-16 | Provenance uses role-specific `POLICY_FORMALIZED_BY`, `CROSSWALK_SYNTHESIZED_BY`, `PRE_PROMOTION_QA_BY`; executable implementation remains NONE | PASS_AFTER_NCR_SUP_003 |
| PC-17 | Owner review scope accurately bounded | PASS |
| PC-18 | Package-specific integrity references recorded; frozen release manifest untouched | PASS_CANDIDATE |

## Pre-merge CAPA status

```text
NCR-SUP-003 = CAPA_ACCEPTED_AND_APPLIED
NCR-SUP-004 = CAPA_ACCEPTED_AND_APPLIED
NCR-SUP-005 = CAPA_ACCEPTED_AND_APPLIED
NORMATIVE_POLICY_CORE_CHANGE = NO
```

## GitHub-side evidence rule

Historical CI runs may be cited as historical evidence, but the live merge decision must evaluate the GitHub Actions Quality result attached to the **latest PR head**.

The QA index intentionally does not self-attest the post-commit CI status of the commit that contains this file. Copying a successful run number into this document would itself create a new commit and a new CI requirement.

Therefore:

```text
FINAL_GITHUB_CI_STATUS = EXTERNAL_PR_CHECK_EVIDENCE
QA_INDEX != SELF_ATTESTATION_OF_ITS_OWN_POST_COMMIT_CI
```

Before merge, external PR evidence must establish:

1. the exact latest PR head SHA;
2. a successful GitHub Actions Quality result on that exact head;
3. successful public-tree / obvious-secret scan on that exact head;
4. changed-file diff inspection for the final CAPA changes;
5. completed Human Owner final branch/PR review.

The live CI result is external GitHub evidence and is not copied back into this file merely to attest its own commit.

```text
POLICY_CANONICALIZATION_GATE = CANDIDATE_PASS_SUBJECT_TO_LATEST_PR_HEAD_CHECKS_AND_OWNER_FINAL_REVIEW
CANONICAL_PROMOTION = NOT_YET_PERFORMED
```

## Non-claims

No external certification, independent IV&V, executable enforcement, deployment, vendor guilt/innocence beyond cited evidence, subjectivity or consciousness is claimed.
