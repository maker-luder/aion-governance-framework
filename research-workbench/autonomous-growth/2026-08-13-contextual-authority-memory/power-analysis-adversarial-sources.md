# Power-analysis uncertainty adversarial — source note

## Unit boundary

`research-labs/power-analysis-uncertainty-adversarial_v0.1.0` is a research-only, clean-room, standard-library adversarial extension of the existing power-planning contract. It audits arithmetic input boundaries, sensitivity ordering, preregistration/assumption identity, assumption mutation, and no-achieved-power serialization. It does not observe data, calculate achieved power, execute a model or intervention, promote an effect, write canonical state, deploy, or modify `main`.

## Reused repository evidence

| What | Who | Where | When | Method | Authority | Transformation | Current/stale status |
|---|---|---|---|---|---|---|---|
| Base power-planning contract and enums | Manus, reviewed under ChatGPT research scope | `research-labs/power-analysis-uncertainty_v0.1.0/src/aion_power_analysis/model.py` | Inherited research lineage; exact new state bound by later QA receipt | Read-only source inspection and stable source-path composition | Repository Evidence; Human Owner retains main/canonical/deployment authority | Added adversarial finite/probability/type/identity/sensitivity/serialization audits; no planning formula promoted to outcome | Current within verified research lineage at the unit commit; not an external freshness claim |
| Base power-planning README and prior methodological references | Manus | `research-labs/power-analysis-uncertainty_v0.1.0/README.md`; `power-analysis-sources.md` | Existing prior-unit record; no independent re-dating in this extension | Methodological vocabulary and non-claim reuse | Repository Evidence / External Literature references already recorded | Reused assumption-dependent planning and `REQUIRED_SAMPLE_SIZE != ACHIEVED_POWER` distinctions only | Current within branch lineage; external source currentness not newly asserted |
| Synthetic planning and assumption-lock decisions | Manus | `research-labs/power-analysis-uncertainty-adversarial_v0.1.0/fixtures/power_adversarial_result.json` | Generated and validated 2026-08-13 | Standard-library Python fixture execution and validator assertions | Synthetic Fixtures; no authority to establish a scientific result | Declared planning metadata mapped to `ADEQUATE`, `UNDERPOWERED`, `UNKNOWN`, `INVALID` and review/hold/indeterminate dispositions | Current as fixture content bound to the research commit; not an observed effect, achieved-power result, or replication |
| Test and validator output | Manus | `research-labs/power-analysis-uncertainty-adversarial_v0.1.0/tests/` and `scripts/validate_fixture.py` | Generated and validated 2026-08-13 | Pytest, compileall, deterministic fixture validation | Tool Output / Repository Evidence | Mechanism tests only; failures would remain process evidence | Current for the recorded unit QA; not scientific evidence |
| Main state reference | Read-only Git reference, recorded by Manus | `origin/main@abb6550abfacb4fabc53ec04fca783bcc34acfdb` | Verified at the repository checkpoint | Read-only state check | Human Owner / Repository state; no main write | Protected reference only | Current authoritative main reference; stale local `4b360779...` remains historical/stale |

Reusing a source reference does not create new evidence. The 20 synthetic cases are not independent replication evidence. `RETRIEVED != CURRENT`, `REMEMBERED != AUTHORITATIVE`, `REFERENCE != NEW_EVIDENCE`, and `DUPLICATION != REPLICATION` remain explicit controls.

## Synthetic transformation

The extension composes `evaluate_plan()` without changing its planning meaning. It adds fail-closed checks for empty plan identifiers, non-integer sample sizes, non-finite values, alpha/target-power boundaries, non-positive effect or standard deviation, missing preregistration and assumption basis, sensitivity monotonicity, assumption identity, and post-outcome assumption mutation. The `AssumptionSnapshot` lock distinguishes unchanged review metadata from pre-outcome changes requiring review and post-outcome mutation requiring hold/invalid handling.

The final run produced 20 passing tests and 20 synthetic cases. Every output retained `ACHIEVED_POWER_CALCULATED = FALSE`, `EFFECT_OBSERVED = FALSE`, `MODEL_EXECUTION = FALSE`, `OBSERVED_RESULT = NOT_EVALUATED`, `SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED`, `SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED`, `IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED`, `CANONICAL_EFFECT = NONE`, `GOVERNANCE_EFFECT = NONE`, and `DEPLOYMENT = FALSE`.

## Retained correction record

No initial test failure or scientific contradiction was encountered in this unit. The final implementation was rerun from a clean cache state with the full test and fixture validator gates. This statement records the observed process state; it does not claim that the contract is complete or that the planning assumptions are empirically true.

## Non-promotion invariants

```text
REQUIRED_SAMPLE_SIZE != ACHIEVED_POWER
POWER_PLAN != OBSERVED_EFFECT
POWER_PLAN != REPLICATION_VALIDITY
PLANNING_REVIEW != SCIENTIFIC_CONFIRMATION
ASSUMPTION_DEPENDENT != EMPIRICALLY_VERIFIED
UNDERPOWERED != SCIENTIFIC_NULL
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
