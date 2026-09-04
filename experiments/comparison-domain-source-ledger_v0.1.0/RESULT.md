# EX-001 RESULT

```text
EXPERIMENT_ID = EX-001
KIND = PROVENANCE / REPOSITORY-INTEGRITY
RUN_UTC = 2026-09-04T09:22:50Z
BASE_HEAD = c3403b15f231eda052c6d0ac3138dc47e07b70d2
NETWORK_USED = FALSE
PAID_API_USED = FALSE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
SUBJECTIVITY_EVIDENCE_WEIGHT = 0
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
LEDGER_AUTHORITY = NONE_DERIVED_REPORT_ONLY
```

## Commands

```bash
python experiments/comparison-domain-source-ledger_v0.1.0/run_experiment.py --write-derived
python -m pytest -q experiments/comparison-domain-source-ledger_v0.1.0/tests
```

## Literal pytest result

```text
...                                                                      [100%]
3 passed in 0.03s
```

## Narrow claims

| Claim | Result |
|---|---|
| C1 listed register/manifest files exist and parse with a `sources` array | `SUPPORTED` |
| C2 fetch-manifest `license_or_terms` and calendar-register `license` strings are present | `SUPPORTED` |
| C3 checked-in `repository_path` SHA-256 matches recorded `repository_sha256` | `PARTIALLY_SUPPORTED` |
| Aggregate of the three narrow claims | `PARTIALLY_SUPPORTED` |

C2 records only that a metadata string exists. It does not establish that a license is legally effective.

C3 compared working-tree bytes to the existing fetch-manifest `repository_sha256`. External URLs were not fetched.

## C3 detail

Checked-in files hashed: 24  
Match: 22  
Mismatch: 2  
HASH_ONLY / no local path: 18 (`NOT_APPLICABLE`, not treated as C3 failures)

Mismatches:

| source_id | recorded repository_sha256 | working-tree sha256 | recorded bytes | working-tree bytes |
|---|---|---|---:|---:|
| `PTOLEMY_TETRABIBLOS_GUTENBERG_70850` | `9acc3da34642eb0a54d8b14224bfa52017aec6bb7f8c0558f50e8492ed226fc1` | `35a6f4456b49288202e216a0421b803771f65657d6a1f785964864ce3f60f8f3` | 552667 | 542633 |
| `SEPHARIAL_ASTROLOGY_GUTENBERG_46963` | `93a32745a37a43763e1b62924e59d136c886a58f050febbbf8f1b6798d80eaf6` | `a555cd5853a0a4ff73b1f9ee844bb89213f26b5f76a5ee973759ac67c4917890` | 235778 | 231411 |

## Competing explanations for C3 mismatches

1. The fetch-manifest hash is the original download hash, while the checked-in file was later normalized (line endings / trailing whitespace) without updating `repository_sha256`.
2. The working tree used for this run is not byte-identical to the blob intended by the manifest.
3. The file contents drifted after the manifest was written.

This experiment does not choose among those explanations and does not rewrite the authoritative manifests.

## Alternative explanations that are out of scope

- Comparison-domain texts being empirically true
- External URLs still serving the recorded bytes
- License strings being sufficient legal clearance

## Falsifiers

- C1 becomes `NOT_SUPPORTED` if a listed register cannot be parsed or loses `sources`.
- C2 becomes `NOT_SUPPORTED` if a fetch-manifest entry lacks `license_or_terms`.
- C3 becomes `NOT_SUPPORTED` if every checked-in path mismatches or is missing.
- C3 becomes `SUPPORTED` only if every checked-in `repository_sha256` matches.

## Non-claims

```text
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
EXTERNAL_URL_CURRENT_CONTENT = NOT_VERIFIED
LICENSE_LEGAL_EFFECTIVENESS = NOT_ESTABLISHED
COMPARISON_DOMAIN_CAUSAL_VALIDITY = NOT_ESTABLISHED
```
