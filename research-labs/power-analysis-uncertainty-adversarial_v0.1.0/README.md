# Power Analysis Uncertainty Adversarial v0.1.0

Status: `RESEARCH_ONLY / PLANNING_METADATA / ACHIEVED_POWER_CALCULATED=FALSE / CANONICAL_EFFECT=NONE`

## Research question

Can a transparent power-planning contract preserve finite numeric inputs, probability bounds, sample-size type, assumption provenance, preregistration identity, sensitivity monotonicity, and post-outcome assumption locks without treating required sample size as achieved power or observing an effect?

This unit extends `power-analysis-uncertainty_v0.1.0` in a research-only `research-labs` module. The base contract computes an assumption-dependent normal-approximation planning requirement, classifies adequate/underpowered/unknown/invalid plans, records sensitivity sizes for smaller and larger effect bounds, and explicitly leaves `achieved_power` unset. The adversarial extension adds plan-ID/type/finite checks, empty preregistration/assumption references, sensitivity validity checks, decision serialization checks, and an `AssumptionSnapshot` lock that holds pre-outcome changes for review and rejects post-outcome assumption mutation.

## Decision layers

A valid plan is `ADEQUATE` or `UNDERPOWERED` under declared assumptions; the resulting disposition is planning metadata only. Missing inputs and missing assumption basis remain unknown/held. Invalid alpha or target power, non-positive effect/sample inputs, non-finite values, and invalid sample-size types fail closed. An empty preregistration reference is indeterminate, and a missing preregistration reference is not equivalent to a confirmatory plan.

Sensitivity must be present, positive, ordered by effect bound, and non-increasing in required sample size as the assumed effect increases. This is a mechanism check on the declared arithmetic, not proof that the model assumptions are true. An unchanged assumption snapshot is review-only; a pre-outcome change requires review; a post-outcome change is invalid. No branch computes achieved power, observes an effect, runs a model, or executes an intervention.

The experiment constructs synthetic `PowerPlan` and `AssumptionSnapshot` values and calls deterministic planning audits only. Every output preserves `ACHIEVED_POWER_CALCULATED=FALSE`, `EFFECT_OBSERVED=FALSE`, `MODEL_EXECUTION=FALSE`, `OBSERVED_RESULT=NOT_EVALUATED`, `SCIENTIFIC_CONCLUSION=NOT_ESTABLISHED`, `CANONICAL_EFFECT=NONE`, `GOVERNANCE_EFFECT=NONE`, `DEPLOYMENT=FALSE`, `SUBJECTIVITY_CONCLUSION=NOT_ESTABLISHED`, and `IDENTITY_CONTINUITY_CONCLUSION=NOT_ESTABLISHED`.

## Results

The suite passed **20 pytest tests** and **20 synthetic planning/assumption-lock cases**. Cases covered valid, missing-ID, invalid-type, non-finite, empty preregistration, empty assumption basis, missing input, non-positive input, invalid probability, unregistered, underpowered, one-sided, serialization, unchanged-lock, pre-outcome assumption change, post-outcome assumption mutation, plan-ID mismatch, non-finite assumption, missing sample size, and target-power boundary conditions.

| Case family | Decision | Mechanism meaning |
|---|---|---|
| Valid adequate or one-sided plan | `ADEQUATE / PLANNING_REVIEW` | Planning arithmetic meets declared target; no outcome observed |
| Underpowered plan | `UNDERPOWERED / INDETERMINATE` | Requirement is not converted to a scientific null or failure |
| Missing input/assumption/preregistration | `UNKNOWN` | Planning provenance or input is incomplete |
| Invalid type/finite/probability/effect | `INVALID / HOLD` | Arithmetic input fails closed |
| Assumption unchanged | `ADEQUATE / PLANNING_REVIEW` | Declared assumptions remain stable |
| Pre-outcome assumption change | `UNKNOWN / INDETERMINATE` | Change requires explicit review |
| Post-outcome assumption mutation | `INVALID / HOLD` | Outcome-contingent assumption rewriting is blocked |

## Falsifiers

The mechanism would be falsified if it produced an achieved-power value from planning metadata, accepted non-finite or out-of-range probabilities, treated missing preregistration or assumption basis as adequate, returned non-monotone sensitivity under fixed assumptions, silently accepted non-integer sample sizes, converted an underpowered plan into a scientific conclusion, or allowed assumptions to change after an observed effect without invalidation.

This unit does not establish achieved power, observed effect, model validity, sample-size sufficiency in a real population, intervention efficacy, statistical significance, scientific confirmation, causal effect, independent replication, model generalization, subjectivity, consciousness, identity continuity, governance effect, canonical effect, or deployment readiness. A power plan is not a result.

## Evidence reuse and provenance

The base power-planning contract is reused through a stable repository source reference. Its public methodological references and prior tests are methodological inputs, not new independent evidence. The 20 synthetic cases are fixtures, not replication evidence. Unknown, invalid, underpowered, and changed-assumption branches remain represented rather than deleted.

## Explicit non-claims

```text
REQUIRED_SAMPLE_SIZE != ACHIEVED_POWER
POWER_PLAN != OBSERVED_EFFECT
POWER_PLAN != REPLICATION_VALIDITY
PLANNING_REVIEW != SCIENTIFIC_CONFIRMATION
ASSUMPTION_DEPENDENT != EMPIRICALLY_VERIFIED
ACHIEVED_POWER_CALCULATED = FALSE
EFFECT_OBSERVED = FALSE
MODEL_EXECUTION = FALSE
OBSERVED_RESULT = NOT_EVALUATED
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
GOVERNANCE_EFFECT = NONE
DEPLOYMENT = FALSE
```

The implementation uses Python standard-library runtime modules plus the existing repository power-analysis source path for composition. It does not access private data, call external services, execute a model or intervention, modify `main`, write canonical state, or deploy.

## Reproduction

```bash
PYTHONPATH=src:../power-analysis-uncertainty_v0.1.0/src python -m pytest -q
PYTHONPATH=src:../power-analysis-uncertainty_v0.1.0/src python scripts/run_power_adversarial.py --output fixtures/power_adversarial_result.json
PYTHONPATH=src:../power-analysis-uncertainty_v0.1.0/src python scripts/validate_fixture.py fixtures/power_adversarial_result.json
```

## References

The implementation reuses repository evidence from `research-labs/power-analysis-uncertainty_v0.1.0` by stable path. The base README cites public methodological sources; this unit does not claim a new literature result or independent replication.
