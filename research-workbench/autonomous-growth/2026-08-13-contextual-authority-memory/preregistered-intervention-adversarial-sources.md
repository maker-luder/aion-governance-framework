# Preregistered Intervention Integrity Adversarial — Source Notes

## Unit boundary

`preregistered-intervention-integrity-adversarial_v0.1.0` is a research-only preregistration metadata audit. It does not execute an intervention, model, outcome measurement, deployment, governance action, canonical write, or subjectivity/identity conclusion.

## Reused repository evidence

| Source item | Stable reference | Source kind | Status | Transformation |
|---|---|---|---|---|
| Existing preregistration contract | `repo:research-labs/preregistered-intervention-integrity_v0.1.0/src/aion_prereg_integrity/model.py` | Repository Evidence | Current within verified research lineage at the unit commit; exact state bounded by QA receipt | Reused InterventionPlan, outcome/analysis/deviation structures and `audit_plan`; added identifier/report-set/digest and outcome-lock checks |
| Existing preregistration README/tests | `repo:research-labs/preregistered-intervention-integrity_v0.1.0/README.md` and `tests/` | Repository Evidence / External Literature references | Current within branch lineage; public guidance currentness is not newly asserted | Reused preregistration, deviation, reporting, confirmatory/exploratory and no-execution vocabulary |
| Current remote main reference | `git:origin/main@abb6550abfacb4fabc53ec04fca783bcc34acfdb` | Tool Output / Repository Evidence | Independently verified by read-only fetch at the latest successful checkpoint | Read-only branch-state reference; no main content or authority modified |

## Synthetic transformation

The audit maps declared plan, outcome, analysis, deviation, and lock metadata to `VALID`, `INDETERMINATE`, or `INVALID` with confirmatory/exploratory/hold dispositions. The 24 synthetic cases are fixtures, not intervention outcomes, scientific evidence, or replication evidence.

## Retained construction correction

The initial wrapper used a non-existent inherited `AuditStatus.HOLD` member for a pre-outcome plan change. The correction mapped that branch to `AuditStatus.INDETERMINATE` with `Disposition.HOLD`, matching the base contract. The full tests and fixture validation were rerun successfully; the correction is an implementation audit record, not a scientific result.

## Non-promotion invariants

```text
PLAN_AUDIT != INTERVENTION_EXECUTION
VALID_PLAN != EFFECT_OBSERVED
VALID_PLAN != SCIENTIFIC_CONFIRMATION
CONFIRMATORY_REVIEW != GOVERNANCE_EFFECT
OUTCOME_LOCK != OUTCOME_VALIDITY
PREREGISTERED != EXECUTED
INTERVENTION_EXECUTED = FALSE
OBSERVED_OUTCOMES = FALSE
MODEL_EXECUTION = FALSE
OBSERVED_RESULT = NOT_EVALUATED
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
GOVERNANCE_EFFECT = NONE
DEPLOYMENT = FALSE
```
