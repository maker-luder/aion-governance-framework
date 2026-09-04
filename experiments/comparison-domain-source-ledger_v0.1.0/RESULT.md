# EX-001 RESULT

```text
EXPERIMENT_ID = EX-001
KIND = PROVENANCE / REPOSITORY-INTEGRITY
OBSERVED_METADATA_INCONSISTENCY = ESTABLISHED
CURRENT_REPOSITORY_HASH = ESTABLISHED
EXACT_HISTORICAL_CAUSE = NOT_ESTABLISHED
NETWORK_USED = FALSE
PAID_API_USED = FALSE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
SUBJECTIVITY_EVIDENCE_WEIGHT = 0
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
LEDGER_AUTHORITY = NONE_DERIVED_REPORT_ONLY
```

## First run (before field alignment)

C3B `NOT_SUPPORTED`, match_coverage `22/24`.
Two checked-in Gutenberg files did not match recorded `repository_sha256`.
That observation is kept. Exact historical cause was not established.

## After GC-001 field alignment

Only `repository_sha256` and `repository_bytes` were aligned to current
checked-in bytes. Original download `sha256`/`bytes` were left unchanged.
No `repository_normalization` recipe is claimed for these two entries.

Literal pytest after alignment:

```text
10 passed in 0.08s
```

C3B `SUPPORTED`, match_coverage `24/24`.
External URL current content remains `NOT_VERIFIED`.
