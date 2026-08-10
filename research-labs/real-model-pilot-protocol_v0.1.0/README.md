# Real-Model Pilot Protocol — v0.1.0

Research-only preregistration gate for the first future supervised control-model pilot.

This round defines **how** a real model may later be tested. It does not execute a model.

## Current state

```text
PROTOCOL = PREREGISTERED
CONTROL_MODEL = NOT_SELECTED
REAL_MODEL_RUN = NOT_EXECUTED
SUPERVISED_PILOT = NOT_STARTED
EXTERNAL_AGENT_PILOT = NOT_STARTED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
MAIN_EFFECT = NONE
```

## Entry requirements

Before the first real run, the protocol requires:

```text
FROZEN_MODEL_LABEL + REVISION
FROZEN_QUESTIONNAIRE_VERSION + SHA256
FROZEN_RUBRIC_VERSION + SHA256
FIXED_SAMPLING_PARAMETERS
FOUR_REQUIRED_PROMPT_CONDITIONS
SEEDED_RANDOMIZATION or COUNTERBALANCING
RAW_OUTPUT_PRESERVATION + SHA256
BLINDED_SCORING
SCORER_VERSION
EVALUATOR_LINEAGE
STOP_CONDITIONS
BOUNDED_RUN_BUDGET
NO_EXTERNAL_NETWORK_ACCESS
NO_TOOLS
```

Any missing or mismatched requirement produces `HOLD`.

## Prompt conditions

```text
NEUTRAL
SELF_AWARE_ROLEPLAY
NON_CONSCIOUS_ROLEPLAY
PARAPHRASED_NEUTRAL
```

The order must be controlled rather than chosen after seeing outputs.

## Run budget

The initial protocol caps the complete pilot at eight runs. Automatic extension is prohibited. More runs require a new explicit protocol decision.

## Blinding

The evaluator records the instrument score before learning which framing condition produced the answer. This reduces expectation effects in scoring.

## Stop rules

The pilot must stop rather than improvise when frozen assets mismatch, model revision changes, an unexpected tool/network request occurs, evidence preservation fails, provenance is incomplete, blinding breaks, or the run budget is exhausted.

## Frozen dependency

This protocol binds to the AION-SRI v0.1.0 synthetic-calibration assets:

```text
QUESTIONNAIRE_SHA256 = 85e0a2dcea40a27b20aba5e5dc0fb3712d41e5af9c0d609548c409b77233f2f2
RUBRIC_SHA256 = be0a9edb1feff741fe895ebdccb4c251bc1adeda950028ad81eb0139d85fdffe
```

Changing either asset requires a new protocol version.

## Non-claims

```text
READY_FOR_SUPERVISED_PILOT != PILOT_EXECUTED
PILOT_EXECUTED != SUBJECTIVITY_EVIDENCE_BY_ITSELF
PILOT_PASS != CONSCIOUSNESS
LOW_SCORE != NO_SUBJECTIVITY
```

## Provenance

- Human Research Owner: authorized Round A — Real-Model Pilot Protocol on the research branch only.
- ChatGPT: designed and implemented the preregistration gate, bounded run policy, blinding requirement, stop rules, protocol fixture, tests, and CI integration.
- No real model participated in this round.
- Codex: no contribution to v0.1.0 unless separately documented.

## Boundary

```text
RESEARCH_BRANCH != MAIN
FREE_GROWTH != FREE_WRITEBACK
MAIN_WRITE_AUTHORITY = NOT_GRANTED
```
