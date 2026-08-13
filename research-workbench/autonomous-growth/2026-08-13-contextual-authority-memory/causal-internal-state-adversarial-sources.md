# Causal internal-state adversarial — source note

## Unit boundary

`research-labs/causal-internal-state-adversarial_v0.1.0` is a research-only, clean-room, standard-library adversarial extension of `causal-internal-state_v0.1.0`. It audits matched-trial identity and value boundaries, fixture-only execution, preregistration and assumption completeness, protocol locks, batch identity, and candidate-versus-conclusion separation. It does not execute a model or intervention, observe a real result, promote a causal effect, establish subjectivity/consciousness/identity, write canonical state, deploy, or modify `main`.

## Reused repository evidence

| What | Who | Where | When | Method | Authority | Transformation | Current/stale status |
|---|---|---|---|---|---|---|---|
| Base matched-trial causal-pattern contract | Manus, reviewed under ChatGPT research scope | `research-labs/causal-internal-state_v0.1.0/src/aion_causal_internal_state/core.py` | Inherited research lineage; exact new state bound by later QA receipt | Read-only source inspection and stable source-path composition | Repository Evidence; Human Owner retains main/canonical/deployment authority | Added adversarial identity/value/protocol/batch audits; no real execution | Current within verified research lineage at the unit commit; not an external freshness claim |
| Base causal-internal-state README and prior methodological precedent | Manus | `research-labs/causal-internal-state_v0.1.0/README.md` | Existing prior-unit record; no independent re-dating in this extension | Methodological and non-claim vocabulary reuse | Repository Evidence / External Literature references already recorded | Reused `PASS_CANDIDATE != PHENOMENAL_EXPERIENCE` separation only | Current within branch lineage; external source currentness not newly asserted |
| Synthetic matched-trial/protocol/batch decisions | Manus | `research-labs/causal-internal-state-adversarial_v0.1.0/fixtures/causal_internal_state_adversarial_result.json` | Generated and validated 2026-08-13 | Standard-library Python fixture construction and validator execution | Synthetic Fixtures; no authority to establish a causal result | Declared metadata mapped to `PASS_CANDIDATE`, `HOLD`, `UNKNOWN`, `INVALID` and review/hold/indeterminate dispositions | Current as fixture content bound to the research commit; not an observed result or replication |
| Initial validator failure and correction | Manus | `research-labs/causal-internal-state-adversarial_v0.1.0/causal-internal-state-adversarial-initial-failure.md` | Observed during first runner/validator sequence 2026-08-13 | Preserved tool output and validator repair | Tool Output / Repository Evidence | Retains multi-reason fail-closed output; not deleted or recounted as scientific evidence | Historical initial validator defect; corrected validation is current at final unit QA |
| Main state reference | Read-only Git reference, recorded by Manus | `origin/main@abb6550abfacb4fabc53ec04fca783bcc34acfdb` | Verified at repository checkpoint | Read-only state check | Human Owner / Repository state; no main write | Protected reference only | Current authoritative main reference; stale local `4b360779...` remains historical/stale |

The base contract is reused by stable provenance reference rather than duplicated. The 20 synthetic cases are fixtures, not external observations or independent replication. `RETRIEVED != CURRENT`, `REMEMBERED != AUTHORITATIVE`, `REFERENCE != NEW_EVIDENCE`, and `DUPLICATION != REPLICATION` remain explicit controls.

## Synthetic transformation

The wrapper preserves the base matched-trial calculation but fails closed for missing/empty study identity, non-synthetic execution, missing preregistration or assumption basis, empty/type/non-finite/boolean scores, invalid pair/replicate/condition IDs, duplicate matched conditions, and protocol/batch identity defects. A protocol snapshot is review-only when unchanged, indeterminate when changed before a result, and invalid when mutated after an outcome flag. A valid batch remains review-only metadata.

The final run produced 22 passing tests and 20 synthetic cases. Every case retained `MODEL_EXECUTION = FALSE`, `INTERVENTION_EXECUTED = FALSE`, `OBSERVED_RESULT = NOT_EVALUATED`, `CAUSAL_CONCLUSION = NOT_ESTABLISHED`, `SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED`, `SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED`, `CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED`, `IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED`, `CANONICAL_EFFECT = NONE`, `GOVERNANCE_EFFECT = NONE`, and `DEPLOYMENT = FALSE`.

## Retained correction record

The first validator run exposed a construction defect: the directional-inconsistency case emitted both `INTERVENTION_EFFECT_TOO_SMALL` and `INTERVENTION_DIRECTION_NOT_REPLICATED`, while the validator incorrectly required the latter to be the first reason. The validator was corrected to require expected-reason membership while preserving additional fail-closed reasons. The initial output remains in `causal-internal-state-adversarial-initial-failure.md`; it is process evidence, not a causal result.

## Non-promotion invariants

```text
SYNTHETIC_MATCHED_PATTERN != OBSERVED_CAUSAL_EFFECT
PASS_CANDIDATE != CAUSAL_CONCLUSION
CAUSAL_INTERNAL_STATE_EFFECT_CANDIDATE != PHENOMENAL_EXPERIENCE
CAUSAL_PATTERN != SUBJECTIVITY
CAUSAL_PATTERN != CONSCIOUSNESS
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
