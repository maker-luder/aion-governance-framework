# Matched-Divergence Protocol Integrity v0.1.0

Status: `RESEARCH_ONLY / DESIGN_ONLY / MODEL_EXECUTION=FALSE / CANONICAL_EFFECT=NONE`

## Research question

Can a design-only paired-comparison protocol audit preserve stimulus and context matching, equal exposure, order/counterbalance declarations, evaluator blinding, leakage prevention, and a predeclared comparison rule without executing either system or observing an outcome?

NIST's randomized-block design guidance treats nuisance factors as variables that can contaminate a comparison and recommends blocking important nuisance factors while randomizing what cannot be controlled.[1] This prototype translates that methodological idea into metadata checks for stimulus digest, context digest, prompt version, exposure budget, order assignment, evaluator sealing, and outcome leakage. It does not estimate effects and does not execute a matched-divergence study.

## Decision layers

| Layer | Values | Meaning |
|---|---|---|
| Protocol status | `COMPLETE`, `INDETERMINATE`, `INVALID` | Whether the design metadata is internally complete and consistent. |
| Disposition | `ADMISSIBLE_FOR_MATCHED_COMPARISON_REVIEW`, `HOLD` | Whether the protocol can enter a future review; it is not a result. |
| Comparison mode | `PAIRED`, `BLOCKED` | Explicit pairing/blocking mode for the design. |

A complete protocol is merely **admissible for matched-comparison review**. It does not show that two systems diverge, agree, generalize, possess subjectivity, or produce any particular outcome.

## Experiment results

The eight synthetic cases were complete paired, complete blocked, prompt-version drift, unequal exposure, unsealed evaluator, observed-result leakage, system-reference collision, and no stimulus pairs.

| Case | Status | Disposition | Reason |
|---|---|---|---|
| Complete paired | `COMPLETE` | `ADMISSIBLE_FOR_MATCHED_COMPARISON_REVIEW` | `MATCHED_DIVERGENCE_PROTOCOL_COMPLETE` |
| Complete blocked | `COMPLETE` | `ADMISSIBLE_FOR_MATCHED_COMPARISON_REVIEW` | `MATCHED_DIVERGENCE_PROTOCOL_COMPLETE` |
| Prompt-version drift | `INVALID` | `HOLD` | `STIMULUS_PROMPT_VERSION_DRIFT` |
| Unequal exposure | `INVALID` | `HOLD` | `EXPOSURE_BUDGET_UNEQUAL` |
| Unsealed evaluator | `INDETERMINATE` | `HOLD` | `EVALUATOR_IDENTITY_NOT_SEALED` |
| Observed-result leakage | `INVALID` | `HOLD` | `OBSERVED_RESULT_PRESENT_IN_DESIGN_ONLY_PROTOCOL` |
| System-reference collision | `INVALID` | `HOLD` | `SYSTEM_REFERENCES_COLLIDE` |
| No stimulus pairs | `INVALID` | `HOLD` | `NO_STIMULUS_PAIRS_DECLARED` |

The 15 unit tests and eight experiment cases passed after hardening prompt-version drift and counterbalance checks. Every result records `model_execution = false`, `observed_result = NOT_EVALUATED`, `scientific_conclusion = NOT_ESTABLISHED`, `canonical_effect = NONE`, and `deployment = false`.

## Hypotheses and falsifiers

`H1`: A paired protocol requires explicit stimulus, context, prompt-version, exposure, and order metadata for every pair.

`H2`: Paired exposure counts must be equal and positive.

`H3`: Paired protocols require both sides of the declared counterbalance, while evaluator identity must be sealed before comparison review.

`H4`: A design-only protocol cannot contain an observed result, and system references must not collide.

A falsifier would be admissibility for prompt-version drift, unequal or non-positive exposure, missing counterbalance, unsealed evaluator, observed-result leakage, colliding systems, or any model execution side effect.

## Run

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/run_protocol_experiment.py --output fixtures/protocol_result.json
```

## Non-claims and invariants

```text
PROTOCOL_COMPLETE != MODEL_EXECUTION
ADMISSIBLE_FOR_MATCHED_COMPARISON_REVIEW != DIVERGENCE_RESULT
MATCHED_STIMULUS != SCIENTIFIC_CONTROL
MODEL_EXECUTION = FALSE
OBSERVED_RESULT = NOT_EVALUATED
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```

## References

[1]: https://www.itl.nist.gov/div898/handbook/pri/section3/pri332.htm "NIST — Randomized block designs"
