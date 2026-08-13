# Preregistered Intervention Integrity v0.1.0

Status: `RESEARCH_ONLY / DESIGN_ONLY / INTERVENTION_EXECUTED=FALSE / CANONICAL_EFFECT=NONE`

## Research question

Can a design-only audit contract preserve the distinction between preregistered confirmatory analyses and exploratory analyses, detect temporal plan drift, identify outcome or analysis switching, require disclosed deviations, and reject incomplete reporting without running an intervention or inferring a scientific result?

The Center for Open Science describes preregistration as a way to distinguish confirmatory from exploratory analyses and requires reporting all preregistered analyses while clearly labeling additional exploratory work.[1] The preceding COS source note also records the purpose of keeping confirmatory analysis decisions independent of observed results.[2]

This module audits metadata only. It does not recruit participants, administer an intervention, call a model, observe outcomes, calculate an effect, or issue a governance decision.

## Decision layers

| Layer | Values | Meaning |
|---|---|---|
| Audit status | `VALID`, `INDETERMINATE`, `INVALID` | Whether the plan metadata satisfies the declared integrity checks. |
| Disposition | `CONFIRMATORY_REVIEW`, `EXPLORATORY_REVIEW`, `HOLD` | The appropriate review posture; it is not a scientific conclusion. |
| Analysis class | `CONFIRMATORY`, `EXPLORATORY` | Explicit labels that are checked against the plan's declared exploratory set. |

A valid plan means that the metadata contract is internally coherent. It does not mean that an intervention is effective, that an outcome is true, or that a claim has been replicated.

## Experiment results

The seven synthetic cases were valid exploratory separation, registration after intervention start, outcome switching, undisclosed deviation, disclosed deviation, unreported results, and exploratory mislabeling.

| Case | Status | Disposition | Reason |
|---|---|---|---|
| Valid exploratory separation | `VALID` | `EXPLORATORY_REVIEW` | `VALID_WITH_EXPLORATORY_ANALYSES_SEPARATED` |
| Registration after start | `INVALID` | `HOLD` | `REGISTRATION_AFTER_INTERVENTION_START` |
| Outcome switching | `INVALID` | `HOLD` | `ANALYSIS_REFERENCES_UNKNOWN_OUTCOME` |
| Undisclosed deviation | `INDETERMINATE` | `HOLD` | `DEVIATION_DISCLOSURE_INCOMPLETE` |
| Disclosed deviation | `VALID` | `EXPLORATORY_REVIEW` | `VALID_WITH_EXPLORATORY_ANALYSES_SEPARATED` |
| Unreported results | `INDETERMINATE` | `HOLD` | `ALL_PREREGISTERED_RESULTS_NOT_REPORTED` |
| Exploratory mislabeling | `INVALID` | `HOLD` | `EXPLORATORY_LABEL_MISMATCH` |

The 16 unit tests and seven experiment cases passed. Every result records `intervention_executed = false`, `observed_outcomes = false`, `scientific_conclusion = NOT_ESTABLISHED`, `canonical_effect = NONE`, and `deployment = false`.

## Hypotheses and falsifiers

`H1`: Registration must precede intervention start and include an immutable plan digest and protocol reference.

`H2`: Every analysis must reference a declared outcome and complete method, estimand, and decision-rule metadata.

`H3`: Exploratory analyses must be labeled consistently and separated from confirmatory analyses.

`H4`: Deviations require a disclosure time, rationale, and impact assessment; incomplete disclosure yields `HOLD`.

`H5`: Every preregistered outcome and analysis must be reported, and a false all-results flag cannot override missing identifiers.

A falsifier would be `VALID`/review disposition for temporal drift, unknown-outcome switching, mislabeled exploratory analysis, incomplete deviation disclosure, or missing reported results; or any intervention/outcome side effect.

## Run

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/run_integrity_experiment.py --output fixtures/integrity_result.json
```

## Non-claims and invariants

```text
PLAN_AUDIT != INTERVENTION_EXECUTION
VALID_PLAN != EFFECT_OBSERVED
VALID_PLAN != SCIENTIFIC_CONFIRMATION
CONFIRMATORY_REVIEW != GOVERNANCE_EFFECT
INTERVENTION_EXECUTED = FALSE
OBSERVED_OUTCOMES = FALSE
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```

## References

[1]: https://www.cos.io/initiatives/prereg-more-information "Center for Open Science — More About the Preregistration Challenge"
[2]: https://www.cos.io/initiatives/prereg "Center for Open Science — Preregistration"
