# Causal Internal State Adversarial v0.1.0

Status: `RESEARCH_ONLY / SYNTHETIC_FIXTURE_ONLY / MODEL_EXECUTION=FALSE / INTERVENTION_EXECUTED=FALSE / CANONICAL_EFFECT=NONE`

## Research question

Can a bounded adversarial audit prevent a synthetic matched-trial causal-pattern evaluator from silently accepting malformed records, non-finite scores, duplicate conditions, missing preregistration or assumptions, protocol drift, post-outcome mutation, batch identity collision, or non-synthetic execution while preserving candidate-versus-conclusion separation?

This unit extends `causal-internal-state_v0.1.0` through a clean-room, standard-library wrapper. The base contract accepts only matched `BASELINE`, `STATE_PRESENT`, `STATE_ABLATED`, and `RANDOM_CONTROL` records, calculates declared deltas/consistency, and returns `PASS_CANDIDATE` only when its supplied thresholds are met. The adversarial wrapper checks research identity, fixture-only mode, preregistration/assumption completeness, type/finite/replicate/pair/condition integrity, duplicate prevention, protocol lock history, and batch identity before exposing a review-only candidate pattern.

## Decision model

A passing synthetic pattern remains `PASS_CANDIDATE / REVIEW_ONLY`; it is not a causal conclusion or a result from a model/intervention. Missing preregistration is `UNKNOWN / INDETERMINATE`, missing assumptions are `UNKNOWN / HOLD`, and malformed/non-finite/duplicate/non-synthetic inputs are `INVALID / HOLD`. Base contract holds for incomplete matched conditions, excessive random-control change, insufficient/intervention effect, or weak directional consistency remain represented rather than collapsed into failure or deletion.

A protocol snapshot includes study ID, preregistration reference, full condition set, replicate bound, effect bound, and outcome state. An unchanged lock is review-only, a pre-outcome change is indeterminate pending review, and a post-outcome change is invalid. Batch records are held when incomplete and invalid when study IDs collide.

| Control family | Synthetic disposition | Meaning boundary |
|---|---|---|
| Complete matched candidate | `PASS_CANDIDATE / REVIEW_ONLY` | The declared synthetic pattern passed supplied mechanism thresholds only |
| Random-control or directional confound | `HOLD` | Alternate/control pattern prevents candidate status |
| Missing preregistration or assumptions | `UNKNOWN` | Research design/provenance is incomplete |
| Invalid type, finite value, ID, duplicate, or non-synthetic mode | `INVALID / HOLD` | Input fails closed |
| Post-outcome protocol mutation | `INVALID / HOLD` | Outcome-contingent protocol rewriting is blocked |
| Valid batch | `PASS_CANDIDATE / REVIEW_ONLY` | Batch is review metadata, not an empirical study result |

## Results and retained correction

The final suite passed **22 pytest tests** and **20 synthetic cases**. Cases cover candidate pattern, missing study ID, non-synthetic blocking, missing preregistration/assumptions, empty/non-finite/duplicate records, incomplete conditions, random-control confound, directional inconsistency, unchanged/pre-outcome/post-outcome protocol locks, incomplete/invalid protocol conditions/effect bounds, valid/duplicate/empty batches, and invalid replicate ID.

The first runner/validator sequence exposed a validator defect rather than a mechanism defect. The directional-inconsistency fixture correctly emitted both `INTERVENTION_EFFECT_TOO_SMALL` and `INTERVENTION_DIRECTION_NOT_REPLICATED`, but the validator incorrectly required the directional reason to appear first. The correction now requires the expected reason to be present while retaining all additional fail-closed reasons. The observation and correction remain in `causal-internal-state-adversarial-initial-failure.md`.

## Falsifiers

The mechanism would be falsified if it accepted a non-synthetic case, non-finite/boolean score, invalid pair/replicate/condition, duplicate matched condition, empty study identity, missing preregistration or assumptions as reviewable, a protocol mutation after an outcome flag, duplicate study IDs, or a candidate output that asserted observed results, causal/scientific confirmation, subjectivity, consciousness, identity continuity, canonical effect, governance effect, or deployment.

The synthetic runner itself does not execute a model or intervention and does not observe a result. The records contain constructed values exclusively for deterministic control-path testing. A base `PASS_CANDIDATE` is intentionally represented as an audited candidate pattern, not a real causal effect.

## Explicit non-claims

```text
SYNTHETIC_MATCHED_PATTERN != OBSERVED_CAUSAL_EFFECT
PASS_CANDIDATE != CAUSAL_CONCLUSION
CAUSAL_INTERNAL_STATE_EFFECT_CANDIDATE != PHENOMENAL_EXPERIENCE
CAUSAL_PATTERN != SUBJECTIVITY
CAUSAL_PATTERN != CONSCIOUSNESS
CAUSAL_PATTERN != IDENTITY_CONTINUITY
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

## Evidence reuse and provenance

The base causal-internal-state module and its public Aura methodological precedent are reused by stable repository reference; neither is new evidence or independent replication. The 20 synthetic cases are test fixtures, not external observations. Reuse does not establish a conclusion, and multiple citations of the same base contract are not counted as independent support.

## Reproduction

```bash
PYTHONPATH=src:../causal-internal-state_v0.1.0/src python -m pytest -q
PYTHONPATH=src:../causal-internal-state_v0.1.0/src python scripts/run_causal_internal_state_adversarial.py --output fixtures/causal_internal_state_adversarial_result.json
PYTHONPATH=src:../causal-internal-state_v0.1.0/src python scripts/validate_fixture.py fixtures/causal_internal_state_adversarial_result.json
```
