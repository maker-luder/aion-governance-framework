# Power Analysis Uncertainty v0.1.0

Status: `RESEARCH_ONLY / SYNTHETIC_FIXTURES / ACHIEVED_POWER=NOT_CALCULATED / CANONICAL_EFFECT=NONE`

## Research question

Can a transparent planning contract expose how sample-size requirements depend on effect-size and variance assumptions, while distinguishing planning adequacy from achieved power, observed effects, replication validity, and scientific conclusions?

Power planning depends on the test model, alpha, expected effect size, and planned sample size.[1] Effect size is an assumption used before data collection rather than an observed fact, and statistical significance alone does not establish practical importance.[1] The National Academies also emphasize that effect-size variation and limited numbers of studies constrain confidence in synthesis and replication interpretation.[2]

This prototype uses a normal approximation for a one-sample mean as an explicit planning model. It reports an assumption-dependent required sample size and a three-point effect-size sensitivity range. It does **not** calculate achieved power, observe an effect, fit a model, or establish a scientific conclusion.

## Decision layers

| Layer | Values | Meaning |
|---|---|---|
| Planning status | `ADEQUATE`, `UNDERPOWERED`, `UNKNOWN`, `INVALID` | Whether the declared sample meets the assumption-dependent required size, or whether inputs are missing/invalid. |
| Disposition | `PLANNING_REVIEW`, `INDETERMINATE`, `HOLD` | Whether the plan is structurally reviewable, assumption-sensitive/underpowered, or blocked by missing/invalid inputs. |
| Output | Required sample size and sensitivity table | A planning calculation conditional on declared assumptions, not an achieved result. |

## Experiment results

The six synthetic cases were adequate, underpowered, smaller-effect sensitivity, missing input, invalid alpha, and unregistered.

| Case | Planning status | Disposition | Required sample size | Interpretation |
|---|---|---|---:|---|
| Adequate | `ADEQUATE` | `PLANNING_REVIEW` | 88 | Meets the declared normal-approximation target under stated assumptions. |
| Underpowered | `UNDERPOWERED` | `INDETERMINATE` | 88 | Planned sample is below the assumption-dependent requirement. |
| Smaller effect | `UNDERPOWERED` | `INDETERMINATE` | 349 | Smaller assumed effect materially increases the planning requirement. |
| Missing input | `UNKNOWN` | `HOLD` | — | No effect bound was supplied. |
| Invalid alpha | `INVALID` | `HOLD` | — | Alpha is outside the valid probability range. |
| Unregistered | `UNKNOWN` | `INDETERMINATE` | 88 | Calculation exists, but confirmatory planning provenance is incomplete. |

The 12 unit tests and six experiment cases passed. The output explicitly records `achieved_power_calculated = false` and `effect_observed = false`.

## Hypotheses and falsifiers

`H1`: Required sample size increases as the assumed effect bound decreases, holding the other declared assumptions fixed.

`H2`: Missing or invalid planning inputs produce `UNKNOWN`/`INVALID` with `HOLD`, rather than an invented power result.

`H3`: A plan below the assumption-dependent requirement remains `INDETERMINATE`, not a forced null or negative scientific conclusion.

`H4`: A non-preregistered plan is not treated as equivalent to a confirmatory plan even when its arithmetic is computable.

A falsifier would be non-monotonic sensitivity under fixed assumptions, an invented achieved-power value, a scientific conclusion from planning metadata alone, or `PLANNING_REVIEW` for an invalid/missing input.

## Run

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/run_power_experiment.py --output fixtures/power_result.json
```

## Non-claims and invariants

```text
REQUIRED_SAMPLE_SIZE != ACHIEVED_POWER
POWER_PLAN != OBSERVED_EFFECT
POWER_PLAN != REPLICATION_VALIDITY
PLANNING_REVIEW != SCIENTIFIC_CONFIRMATION
ACHIEVED_POWER_CALCULATED = FALSE
EFFECT_OBSERVED = FALSE
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```

## References

[1]: https://meera.seas.umich.edu/power-analysis-statistical-significance-effect-size.html "University of Michigan Meera — Power Analysis, Statistical Significance, and Effect Size"
[2]: https://www.nationalacademies.org/read/25303/chapter/10 "National Academies — Chapter 7: Confidence in Science"
