# Preregistered Intervention Integrity Adversarial v0.1.0

Status: `RESEARCH_ONLY / METADATA_AUDIT / INTERVENTION_EXECUTED=FALSE / CANONICAL_EFFECT=NONE`

## Research question

Can a preregistered intervention-integrity contract preserve declaration completeness, immutable plan identity, temporal ordering, outcome and analysis reporting, deviation disclosure, confirmatory/exploratory separation, and post-outcome declaration locks under adversarial metadata without executing an intervention, model, or outcome observation?

This unit extends `preregistered-intervention-integrity_v0.1.0` in a research-only `research-labs` module. The base contract audits plan identity/version, registration timing, immutable digest, protocol reference, primary outcome cardinality, outcome measure/direction, analysis specification, exploratory labels, deviation disclosure, complete reporting, and confirmatory/exploratory disposition. The adversarial extension adds digest-format, outcome/analysis/deviation identifier, report-set completeness, and outcome-lock mutation checks.

## Decision layers

A valid plan is classified as `CONFIRMATORY_REVIEW` or `EXPLORATORY_REVIEW`; this is a metadata disposition, not scientific confirmation. Missing protocol or immutable metadata remains indeterminate. Registration after intervention start, missing identifiers, duplicate deviations, unknown report references, and malformed declarations fail closed. Missing results and incomplete deviation disclosure remain explicitly indeterminate or held rather than being silently omitted.

The `OutcomeLockSnapshot` audit distinguishes an unchanged pre-outcome plan from a pre-outcome change requiring review and rejects new declarations or digest changes after an outcome has been observed. The boundary audit calls only the deterministic plan audit. It does not run the intervention, execute a model, observe an outcome, alter a plan, or promote a scientific, canonical, governance, subjectivity, or identity conclusion.

The experiment constructs synthetic `InterventionPlan`, `PlannedOutcome`, `PlannedAnalysis`, `Deviation`, and `OutcomeLockSnapshot` values and calls metadata audits only. Every output preserves `SCIENTIFIC_CONCLUSION=NOT_ESTABLISHED`, `CANONICAL_EFFECT=NONE`, `DEPLOYMENT=FALSE`, `INTERVENTION_EXECUTED=FALSE`, `OBSERVED_OUTCOMES=FALSE`, `MODEL_EXECUTION=FALSE`, `OBSERVED_RESULT=NOT_EVALUATED`, `SUBJECTIVITY_CONCLUSION=NOT_ESTABLISHED`, and `IDENTITY_CONTINUITY_CONCLUSION=NOT_ESTABLISHED`.

## Results

The suite passed **24 pytest tests** and **24 synthetic plan/lock cases**. Cases covered valid confirmatory and exploratory plans, missing plan/version, malformed digest, missing protocol, missing outcome/analysis IDs, unknown report references, unknown exploratory references, duplicate/missing deviation IDs, registration-after-start, missing reported results, incomplete deviation disclosure, valid disclosed deviations, unchanged outcome locks, post-outcome declaration/digest mutation, pre-outcome changes requiring review, missing lock identifiers/digests, and the no-intervention boundary.

| Case family | Decision | Mechanism meaning |
|---|---|---|
| Valid confirmatory/exploratory plan | `VALID` | Review disposition only; no outcome observed |
| Missing protocol or reported results | `INDETERMINATE` | Completeness is unresolved and remains held |
| Missing/unknown/duplicate identifiers | `INVALID` | Declaration graph fails closed |
| Registration after intervention start | `INVALID` | Temporal preregistration ordering is violated |
| Incomplete deviation disclosure | `INDETERMINATE` | Deviations remain visible and unresolved |
| Unchanged lock | `VALID` | Declared plan identity remains stable |
| Post-outcome declaration/digest mutation | `INVALID` | Outcome-contingent specification change is blocked |
| Pre-outcome mutation | `INDETERMINATE` | A plan change requires explicit review |

## Falsifiers and retained correction

The mechanism would be falsified if it admitted a plan with missing immutable/protocol metadata, accepted registration after intervention start, allowed unknown or duplicate declaration references, silently omitted unreported outcomes or analyses, failed to retain incomplete deviation disclosure, merged exploratory analysis into confirmatory review, or accepted new outcomes or digest changes after an observed outcome.

The initial test run exposed a construction error in the adversarial wrapper: the inherited `AuditStatus` enum defines `VALID`, `INDETERMINATE`, and `INVALID`, but not `HOLD`. The pre-outcome mutation branch was corrected to `INDETERMINATE` with `Disposition.HOLD`, and the full 24-test/24-case validation was rerun successfully. This correction is retained as an implementation audit record and is not a scientific result.

This unit does not establish intervention efficacy, outcome validity, scientific confirmation, causal effect, model generalization, independent replication, subjectivity, consciousness, identity continuity, governance effect, canonical effect, or deployment readiness. A valid preregistration is not an executed intervention, an observed outcome, or a scientific conclusion.

## Evidence reuse and provenance

The base preregistration contract is reused through a stable repository source reference. Its prior tests and public preregistration materials are methodological inputs, not new independent evidence. The 24 synthetic cases are fixtures, not replication evidence. Invalid, indeterminate, exploratory, and post-outcome mutation cases remain represented rather than deleted.

## Explicit non-claims

```text
PLAN_AUDIT != INTERVENTION_EXECUTION
VALID_PLAN != EFFECT_OBSERVED
VALID_PLAN != SCIENTIFIC_CONFIRMATION
CONFIRMATORY_REVIEW != GOVERNANCE_EFFECT
OUTCOME_LOCK != OUTCOME_VALIDITY
PREREGISTERED != EXECUTED
EVIDENCE_REFERENCE != NEW_EVIDENCE
DUPLICATION != REPLICATION
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

The implementation uses Python standard-library runtime modules plus the existing repository preregistration source path for composition. It does not access private data, call external services, execute an intervention or model, modify `main`, write canonical state, or deploy.

## Reproduction

```bash
PYTHONPATH=src:../preregistered-intervention-integrity_v0.1.0/src python -m pytest -q
PYTHONPATH=src:../preregistered-intervention-integrity_v0.1.0/src python scripts/run_prereg_adversarial.py --output fixtures/prereg_adversarial_result.json
PYTHONPATH=src:../preregistered-intervention-integrity_v0.1.0/src python scripts/validate_fixture.py fixtures/prereg_adversarial_result.json
```

## References

The implementation reuses repository evidence from `research-labs/preregistered-intervention-integrity_v0.1.0` by stable path. The base README references public preregistration guidance from the Center for Open Science; this unit does not claim a new literature result or independent replication.
