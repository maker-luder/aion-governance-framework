# Independent Replication Design v0.1.0

Status: `RESEARCH_ONLY / SYNTHETIC_FIXTURES / CANONICAL_EFFECT=NONE`

## Research question

Can a bounded research contract distinguish an **independent replication design** from a same-data rerun or an incomplete study plan, while separating design validity, power metadata, observed outcome, and conservative interpretation?

This prototype is informed by the National Academies and NCBI Bookshelf treatment of replicability as a same-question comparison using new data, where proximity and uncertainty must both be considered.[1] [2] It also uses the Center for Open Science preregistration concept as a design-control vocabulary for fixing confirmatory decisions before observing outcomes.[3]

The implementation is an engineering mechanism test over synthetic records. It does not estimate scientific power for a real experiment, certify a replication, or produce evidence about AION, Astra, subjectivity, consciousness, or identity continuity.

## Decision layers

| Layer | Values | Meaning |
|---|---|---|
| Design validity | `VALID`, `PARTIAL`, `INVALID` | Whether data independence, protocol, preregistration ordering, estimand, analysis plan, provenance, and independence attestations are present. |
| Power status | `ADEQUATE`, `UNDERPOWERED`, `UNKNOWN` | A transparent comparison of planned sample size to a declared synthetic minimum, or an explicit unknown state. |
| Outcome | `CONSISTENT`, `DIVERGENT`, `INDETERMINATE` | The declared synthetic outcome under the predeclared estimand. |
| Interpretation | `CONSISTENT`, `DIVERGENT`, `INDETERMINATE`, `HOLD` | A conservative decision after design and uncertainty checks. |

A divergent result from a valid, adequately specified design is recorded as `DIVERGENT` with no automatic downgrade. An underpowered or uncertainty-incomplete design is not converted into a strong positive or negative conclusion. Same-data records and incomplete preregistered designs produce `HOLD`.

## Hypotheses and falsifiers

`H1`: New-data and explicit independence checks reject a same-data record as an independent replication.

`H2`: Missing preregistration ordering, estimand, analysis plan, protocol, provenance, or independence rationale produces `HOLD` rather than a confident outcome interpretation.

`H3`: An underpowered or uncertainty-incomplete design remains `INDETERMINATE`, not a forced success or failure.

`H4`: A valid divergent outcome remains `DIVERGENT` without automatic governance downgrade, canonical effect, deployment, or subjectivity/identity conclusion.

A falsifier would be a same-data record accepted as independent, a post-outcome preregistration accepted as confirmatory, a missing-design record classified as a strong outcome, or a divergent result changing a governance state automatically.

## Experiment

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/run_design_experiment.py --output fixtures/design_result.json
```

The five synthetic cases are: adequate consistent design, adequate divergent design, underpowered design, missing preregistration, and same-data misuse.

## Non-claims and invariants

```text
DESIGN_VALIDITY != SCIENTIFIC_TRUTH
POWER_METADATA != POWER_GUARANTEE
DIVERGENT_OUTCOME != AUTOMATIC_FIXED_DOWNGRADE
SAME_DATA != INDEPENDENT_REPLICATION
PREREGISTRATION != RESULT_CERTIFICATION
REPLICATION_RESULT != SUBJECTIVITY_EVIDENCE
REPLICATION_RESULT != IDENTITY_CONTINUITY
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

## References

[1]: https://www.nationalacademies.org/read/25303/chapter/8 "National Academies — Chapter 5: Replicability"
[2]: https://www.ncbi.nlm.nih.gov/books/NBK547524/ "NCBI Bookshelf — Replicability"
[3]: https://www.cos.io/initiatives/prereg "Center for Open Science — Preregistration"
