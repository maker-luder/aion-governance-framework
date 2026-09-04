# EX-001 RESULT

```text
EXPERIMENT_ID = EX-001
KIND = PROVENANCE / REPOSITORY-INTEGRITY
RUN_UTC = 2026-09-04T09:31:45Z
BASE_HEAD_AT_RUN = f4c911af558e5076a52cfe7b4efc5a8e00585d2c
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

## Literal pytest result

```text
..........                                                               [100%]
10 passed in 0.07s
```

## Narrow claims

| Claim | Result |
|---|---|
| C1 register **and** fetch-manifest files parse with a `sources` array (7/7 surfaces) | `SUPPORTED` |
| C2 license/usage metadata strings are present | `SUPPORTED` |
| C3A per-entry outcomes reported | `SUPPORTED` |
| C3B all checked-in hashes match | `NOT_SUPPORTED` |
| C3 coverage aggregate | `PARTIALLY_SUPPORTED` |
| Aggregate of C1 + C2 + C3A + C3B | `PARTIALLY_SUPPORTED` |

C2 records only that a metadata string exists. Legal effectiveness remains
`NOT_ESTABLISHED`. External URLs were not fetched.

## C3 coverage

```text
checked_in_n = 24
MATCH = 22
MISMATCH = 2
MISSING = 0
NOT_APPLICABLE = 18
match_coverage = 22/24
```

`C3B` is `NOT_SUPPORTED` because two checked-in entries mismatch. That is not
hidden inside a universal "hash matches" claim.

Mismatch entries:

| source_id | recorded repository_sha256 | working-tree sha256 |
|---|---|---|
| `PTOLEMY_TETRABIBLOS_GUTENBERG_70850` | `9acc3da34642eb0a54d8b14224bfa52017aec6bb7f8c0558f50e8492ed226fc1` | `35a6f4456b49288202e216a0421b803771f65657d6a1f785964864ce3f60f8f3` |
| `SEPHARIAL_ASTROLOGY_GUTENBERG_46963` | `93a32745a37a43763e1b62924e59d136c886a58f050febbbf8f1b6798d80eaf6` | `a555cd5853a0a4ff73b1f9ee844bb89213f26b5f76a5ee973759ac67c4917890` |

Competing explanations remain: original-download hash vs later normalization;
working-tree bytes vs intended blob; later drift. This experiment does not
choose among them and does not rewrite authoritative manifests.

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
