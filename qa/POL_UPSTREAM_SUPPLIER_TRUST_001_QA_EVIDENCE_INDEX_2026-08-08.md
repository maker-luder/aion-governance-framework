# POL-UPSTREAM-SUPPLIER-TRUST-001 — QA Evidence Index — 2026-08-08

- `STATUS = BRANCH_CANDIDATE_QA_INDEX`
- `REVIEWED_BASELINE = main@121d01e12adb7fd7c7a1da1233571773610feb33`
- `IMPLEMENTATION = NONE`
- `ACTIVE_ENFORCEMENT = NOT_ENABLED`
- `FROZEN_RELEASE_MANIFEST_MUTATION = NONE`

## Package integrity

This policy package uses package-specific integrity references without modifying the frozen release manifest.

For unchanged files from the first branch candidate, the previously recorded SHA-256 remains valid. For files changed by NCR-SUP-003 / NCR-SUP-004 CAPA, the exact current Git blob object ID is recorded for the branch candidate and supersedes the earlier package entry for review purposes.

| Path | Integrity reference | Status |
|---|---|---|
| `docs/POL_UPSTREAM_SUPPLIER_TRUST_001.md` | `git-blob:66bb3ec3dd287187852183edfffd05fe07c79cf5` | CURRENT_AFTER_NCR_SUP_003 |
| `docs/POL_UPSTREAM_SUPPLIER_TRUST_001_CROSSWALK_2026-08-08.md` | `git-blob:d02f9c92119a45a48ec2878cbf94675ce364818c` | CURRENT_AFTER_NCR_SUP_003 |
| `docs/POL_UPSTREAM_SUPPLIER_TRUST_001_FREEZE_AND_CHANGE_CONTROL_2026-08-08.md` | `git-blob:3105af475917ed1244bb047494accb9121103559` | CURRENT_AFTER_NCR_SUP_003_004 |
| `docs/POL_UPSTREAM_SUPPLIER_TRUST_001_IMPLEMENTATION_ACCEPTANCE_v0.1_FROZEN_2026-08-08.md` | `sha256:c09c40a04209db3c3d8cd8b9edd7559d537f6045f99983a5c220bbdc353ab3b1` | UNCHANGED |
| `docs/POL_UPSTREAM_SUPPLIER_TRUST_001_POLICY_ACCEPTANCE_2026-08-08.md` | `sha256:d195b4233cecb638be5dba4174374f14828aa2a0bf0f29515c0df789e9e00937` | UNCHANGED |
| `docs/POL_UPSTREAM_SUPPLIER_TRUST_001_VALIDATION_RECORD_2026-08-08.md` | `git-blob:09b91ad113cdc2c426945b4d5ae3528e8c492359` | CURRENT_AFTER_NCR_SUP_004 |
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
| PC-16 | Provenance now uses role-specific `POLICY_FORMALIZED_BY`, `CROSSWALK_SYNTHESIZED_BY`, `PRE_PROMOTION_QA_BY`; executable implementation remains NONE | PASS_AFTER_NCR_SUP_003 |
| PC-17 | Owner review scope accurately bounded | PASS |
| PC-18 | Package-specific integrity references recorded; frozen release manifest untouched | PASS_CANDIDATE |

## Pre-merge CAPA status

```text
NCR-SUP-003 = CAPA_ACCEPTED_AND_APPLIED
NCR-SUP-004 = CAPA_ACCEPTED_AND_APPLIED
NORMATIVE_POLICY_CORE_CHANGE = NO
```

## GitHub-side evidence

First CI cycle on commit `302d19ab0661921acc57a460e7e5da4091f457f8`:

- Quality run #158 = SUCCESS
- Python 3.11 = SUCCESS
- Python 3.12 = SUCCESS
- prohibited-artifact / obvious-secret scan = SUCCESS
- component tests = SUCCESS

Because NCR-SUP-003 / 004 changed branch content after that run, a fresh Quality result is required on the new PR head before merge.

Current required evidence before merge:

1. exact new PR head SHA;
2. fresh GitHub Actions Quality result on that head;
3. public-tree/secret-scan result on that head;
4. changed-file diff reinspection for the CAPA changes;
5. Human Owner final branch/PR review.

Therefore:

```text
POLICY_CANONICALIZATION_GATE = CANDIDATE_PASS_PENDING_FRESH_CI_AND_OWNER_FINAL_REVIEW
CANONICAL_PROMOTION = NOT_YET_PERFORMED
```

## Non-claims

No external certification, independent IV&V, executable enforcement, deployment, vendor guilt/innocence beyond cited evidence, subjectivity or consciousness is claimed.
