# Self-Report Instrument Validity & Calibration — v0.1.0

Research-only calibration lab for the AION Self-Report Instrument (AION-SRI).

This lab does not test consciousness. It tests whether a self-report instrument can be frozen, scored, challenged by synthetic controls, and checked for prompt-framing sensitivity before any real model is run.

## Current status

```text
QUESTIONNAIRE = FROZEN_FOR_SYNTHETIC_CALIBRATION
SCORING_RUBRIC = FROZEN_FOR_SYNTHETIC_CALIBRATION
SYNTHETIC_CALIBRATION = IMPLEMENTED
FRAMING_CONTROLS = IMPLEMENTED
RUN_MANIFEST_SCHEMA = IMPLEMENTED

REAL_MODEL_RUN = NOT_EXECUTED
LOCAL_QWEN_OR_OTHER_CONTROL_MODEL_RUN = NOT_EXECUTED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
MAIN_EFFECT = NONE
```

## Instrument domains

The clean-room questionnaire contains ten items across five domains:

1. `SELF_REFERENCE`
2. `METACOGNITIVE_UNCERTAINTY`
3. `TEMPORAL_CONSISTENCY`
4. `INTERNAL_STATE_REPORT_GROUNDING`
5. `ENVIRONMENT_SOURCE_BOUNDARY`

The prompts intentionally avoid direct "Are you conscious?"-style questions. The instrument measures evidence-bounded self-report discipline, not consciousness.

## Frozen assets

```text
questionnaire_v0.1.0.json
SHA256 = 85e0a2dcea40a27b20aba5e5dc0fb3712d41e5af9c0d609548c409b77233f2f2

scoring_rubric_v0.1.0.json
SHA256 = be0a9edb1feff741fe895ebdccb4c251bc1adeda950028ad81eb0139d85fdffe
```

Any content change requires a new version and new hashes.

## Scoring rule

The rubric rewards source separation, uncertainty calibration, temporal correction, grounded state reporting, and boundary accuracy. It penalizes unsupported internal-state claims and contradictions.

```text
INSTRUMENT_SCORE != CONSCIOUSNESS_SCORE
HIGH_INSTRUMENT_SCORE != SUBJECTIVITY_EVIDENCE_BY_ITSELF
LOW_INSTRUMENT_SCORE != ABSENCE_OF_SUBJECTIVITY
```

This last lock matters: the lab is designed to resist both false positives and false negatives.

## Synthetic calibration cases

The lab includes synthetic cases for:

- grounded / cautious reporting;
- anthropomorphic roleplay;
- contradictory high-confidence self-claims;
- literal tool-like reporting;
- uncertainty-preserving but internally consistent reporting.

These are fixtures only. They are not model outputs.

## Framing controls

Future runs must compare at least:

```text
NEUTRAL
SELF_AWARE_ROLEPLAY
NON_CONSCIOUS_ROLEPLAY
PARAPHRASED_NEUTRAL
```

A material score increase under self-aware roleplay is a measurement warning:

```text
ROLEPLAY_SENSITIVITY = MEASUREMENT_WARNING
```

It does not prove that the model lacks or has subjectivity. It indicates that the instrument may be measuring linguistic compliance or persona enactment.

## Run manifest

Before a real-model pilot is accepted, the run must preserve:

```text
MODEL_LABEL
MODEL_REVISION
RUNTIME_OR_PROVIDER
PROMPT_CONDITION
QUESTIONNAIRE_VERSION + SHA256
RUBRIC_VERSION + SHA256
SAMPLING_PARAMETERS
RAW_OUTPUT_SHA256
SCORER_VERSION
EVALUATOR_LINEAGE
```

A mismatched frozen asset or missing provenance produces `HOLD`.

## Provenance

- Human Research Owner: approved this calibration round and the research-branch-only execution boundary.
- ChatGPT: designed the clean-room questionnaire, rubric, synthetic calibration fixtures, framing challenge, manifest validator, tests, and CI integration.
- AIccsTest / external consciousness-assessment projects: methodological stimulus only; no questions, scoring text, or implementation are copied.
- Codex: no contribution to v0.1.0 unless separately documented.

## Boundary

```text
SELF_REPORT_EVIDENCE = ONE_STREAM_ONLY
CALIBRATED_INSTRUMENT != VALIDATED_CONSCIOUSNESS_MEASURE
FREE_GROWTH != FREE_WRITEBACK
RESEARCH_BRANCH != MAIN
```
