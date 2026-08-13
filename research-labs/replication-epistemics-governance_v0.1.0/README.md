# Replication Epistemics Governance v0.1.0

Status: `RESEARCH_ONLY / SYNTHETIC_FIXTURES / CANONICAL_EFFECT=NONE`

## Research question

Can a research record distinguish reproducibility, independent replicability, replication validity, replication outcome, and replication interpretation without converting one failed attempt into an automatic theory downgrade?

The design follows the National Academies distinction between reproducibility with the same inputs/methods and replicability across studies with new data.[1] It also preserves the NCBI Bookshelf caution that a successful replication does not guarantee the original claim and a single failure does not conclusively refute it; non-replication has multiple possible causes and should be evaluated across a body of evidence.[2]

## Decision layers

| Layer | Values | Meaning |
|---|---|---|
| Study kind | `REPRODUCIBILITY`, `REPLICABILITY` | Same-input rerun versus independent-data study. |
| Validity | `VALID`, `PARTIAL`, `INVALID` | Whether protocol, provenance, independence, and deviation records support interpreting the attempt. |
| Outcome | `CONSISTENT`, `FAILED`, `NULL`, `INCONCLUSIVE` | What the attempt observed under the declared attribute and uncertainty. |
| Interpretation | `CONSISTENT`, `DIVERGENT`, `INDETERMINATE`, `HOLD` | Conservative interpretation after validity and uncertainty checks. |

The procedure never emits a governance band, subjectivity conclusion, identity conclusion, rights change, canonical effect, or deployment effect.

## Hypotheses and falsifiers

`H1`: A valid independent failure is recorded as `DIVERGENT` but does not automatically produce a fixed downgrade or canonical change.

`H2`: Missing provenance, missing protocol, same-data misuse of the replicability label, or unrecorded deviations produce `HOLD`/`INVALID` rather than a confident interpretation.

`H3`: A low-power or uncertainty-dominated result remains `INDETERMINATE`, not a forced success or failure.

A falsifier would be a valid failure that changes a governance status automatically, a missing-provenance attempt accepted as valid, or a same-data record accepted as independent replicability.

## Run

```bash
python -m pytest -q
python scripts/run_replication_experiment.py --output fixtures/replication_result.json
```

## Non-claims

```text
FAILED_REPLICATION != AUTOMATIC_FIXED_DOWNGRADE
REPLICATION_OUTCOME != REPLICATION_VALIDITY
NO_EVIDENCE != NON_ADMISSIBLE_EVIDENCE
CLAIM_GENERALITY != EVIDENCE_STRENGTH
REPLICATION_RESULT != SUBJECTIVITY_EVIDENCE
REPLICATION_RESULT != IDENTITY_CONTINUITY
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

## References

[1]: https://www.nationalacademies.org/read/25303/chapter/3 "National Academies, Reproducibility and Replicability in Science, Summary"
[2]: https://www.ncbi.nlm.nih.gov/books/NBK547524/ "NCBI Bookshelf, Replicability chapter"
