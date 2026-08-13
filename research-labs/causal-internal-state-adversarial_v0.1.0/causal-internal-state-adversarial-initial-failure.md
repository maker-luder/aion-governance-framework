# Initial fixture-validator failure — causal internal-state adversarial

## Observed process event

The first full synthetic runner/validator invocation passed **22 pytest tests** and constructed all 20 fixture cases, but the fixture validator stopped at the `directional-inconsistency` record. The validator incorrectly required `INTERVENTION_DIRECTION_NOT_REPLICATED` to be the first reason.

The base assessment correctly produced two ordered reasons for the supplied mixed-direction synthetic scores:

```text
INTERVENTION_EFFECT_TOO_SMALL
INTERVENTION_DIRECTION_NOT_REPLICATED
```

The average intervention delta was approximately `0.05`, below the declared `0.20` threshold, while directional consistency was `0.5`, below the declared `0.80` threshold. Both declared mechanism constraints therefore applied. The test suite had already asserted membership of the directional reason rather than an invalid single-reason assumption.

## Correction

The fixture validator is revised to require that the expected reason be present in the reason list while retaining status and disposition checks. It will not discard additional fail-closed reasons. The complete runner and validator are then rerun.

## Interpretation boundary

This was a synthetic fixture-validator expectation defect. It is not an observed causal result, a model execution, an intervention, a scientific finding, subjectivity evidence, a consciousness claim, an identity claim, a governance decision, canonical effect, or deployment event. It is retained as process evidence that multiple adverse planning/measurement constraints may hold simultaneously.

```text
MODEL_EXECUTION = FALSE
INTERVENTION_EXECUTED = FALSE
OBSERVED_RESULT = NOT_EVALUATED
CAUSAL_CONCLUSION = NOT_ESTABLISHED
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
GOVERNANCE_EFFECT = NONE
DEPLOYMENT = FALSE
```
