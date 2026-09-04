# EX-001 RESULT

```text
EXPERIMENT_ID = EX-001
KIND = PROVENANCE / REPOSITORY-INTEGRITY
FIRST_RUN_UTC = 2026-09-04T09:31:45Z
RERUN_AFTER_GC001_UTC = 2026-09-04T09:44:00Z
NETWORK_USED = FALSE
PAID_API_USED = FALSE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
SUBJECTIVITY_EVIDENCE_WEIGHT = 0
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
LEDGER_AUTHORITY = NONE_DERIVED_REPORT_ONLY
PR_DIFF_INCLUDES_SANDBOX_RULES = TRUE
MAIN_TRANSITION_AUTHORITY_GATE = UNCHANGED_NOT_BYPASSED
```

## Commands

```bash
python experiments/comparison-domain-source-ledger_v0.1.0/run_experiment.py --write-derived
python -m pytest -q experiments/comparison-domain-source-ledger_v0.1.0/tests
```

## First-run claims (before GC-001)

| Claim | Result |
|---|---|
| C1 | `SUPPORTED` |
| C2 | `SUPPORTED` |
| C3A | `SUPPORTED` |
| C3B all checked-in hashes match | `NOT_SUPPORTED` |
| match_coverage | `22/24` |

Negative finding kept: Ptolemy and Sepharial `repository_sha256` copied the download hash after LF normalization.

## Rerun after GC-001

GC-001 updated only `repository_sha256` / `repository_bytes` / `repository_normalization` on those two fetch-manifest entries. Original download `sha256`/`bytes` were left unchanged.

Literal pytest after repair:

```text
10 passed in 0.08s
```

| Claim | Result |
|---|---|
| C1 register and fetch-manifest files parse (7/7) | `SUPPORTED` |
| C2 license/usage metadata present | `SUPPORTED` |
| C3A per-entry outcomes reported | `SUPPORTED` |
| C3B all checked-in hashes match | `SUPPORTED` |
| C3 coverage | `24/24 MATCH` |
| Aggregate | `SUPPORTED` |

External URL current content remains `NOT_VERIFIED`.
License legal effectiveness remains `NOT_ESTABLISHED`.
This does not establish comparison-domain causal validity or subjectivity.

## Falsifiers

- C1 is `NOT_SUPPORTED` if any of the 7 surfaces fails to parse or loses `sources`.
- C2 is `NOT_SUPPORTED` if any fetch-manifest entry lacks `license_or_terms`.
- C3A is `NOT_SUPPORTED` if an entry lacks a legal outcome label.
- C3B is `NOT_SUPPORTED` if any checked-in entry is `MISMATCH` or `MISSING`.

## Non-claims

```text
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
EXTERNAL_URL_CURRENT_CONTENT = NOT_VERIFIED
LICENSE_LEGAL_EFFECTIVENESS = NOT_ESTABLISHED
COMPARISON_DOMAIN_CAUSAL_VALIDITY = NOT_ESTABLISHED
```
