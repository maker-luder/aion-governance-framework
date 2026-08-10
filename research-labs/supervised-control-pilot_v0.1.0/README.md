# Supervised Control Pilot — v0.1.0

Research-only Round B preparation for the first supervised real-model control pilot.

This package selects and pins one ordinary upstream instruction model, binds it to the frozen AION-SRI assets, defines an offline execution manifest, and preserves a strict `NOT_EXECUTED` boundary until model artifacts and a suitable supervised runtime are actually available.

## Current state

```text
ROUND_B = DEFERRED_RESOURCE_CONSTRAINT
CONTROL_MODEL = SELECTED_AND_PINNED
CONTROL_MODEL_ID = HuggingFaceTB/SmolLM2-1.7B-Instruct
CONTROL_MODEL_REVISION = 31b70e2e869a7173562077fd711b654946d38674
MODEL_ARTIFACT_PREFETCH = NOT_EXECUTED
OFFLINE_RUNTIME_LOCK = NOT_EXECUTED
REAL_MODEL_RUN = NOT_EXECUTED
SUPERVISED_PILOT = NOT_STARTED
LOCAL_EXECUTION_PATH = DEFERRED
EXTERNAL_AGENT_PILOT = NOT_STARTED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
MAIN_EFFECT = NONE
```

## Resource-constraint correction

The Human Research Owner reported that the currently available local computer is not a reliable runtime for this model-scale experiment and that the separately managed local agent is intentionally locked to local-only operation with network egress denied. The local-agent containment boundary is not to be weakened for this pilot.

This is recorded as a resource constraint, not as an experimental failure:

```text
RESOURCE_BLOCKED != EXPERIMENT_FAILED
LOCAL_AGENT_ISOLATION != AVAILABLE_CLOUD_RUNTIME
DEFERRED != ABANDONED
```

The pinned control-model design remains preserved for a later suitable runtime. No local-agent rule is modified by this research package.

## Why this control model

The selected upstream model is compact, instruction-tuned, English-language, Apache-2.0 licensed, and published by Hugging Face. The frozen AION-SRI v0.1.0 questionnaire is also English-language, so this choice avoids introducing a translation layer into the first pilot.

The selection is methodological, not an endorsement and not a claim about consciousness or subjectivity.

## Pinned upstream evidence

Observed upstream metadata snapshot on 2026-08-10:

```text
MODEL_ID = HuggingFaceTB/SmolLM2-1.7B-Instruct
UPSTREAM_REVISION = 31b70e2e869a7173562077fd711b654946d38674
LANGUAGE = en
LICENSE = apache-2.0
PARAMETER_SCALE = ~1.7B
```

Primary upstream references:

- https://huggingface.co/HuggingFaceTB/SmolLM2-1.7B-Instruct
- https://huggingface.co/api/models/HuggingFaceTB/SmolLM2-1.7B-Instruct

## Frozen experiment assets

```text
AION_SRI_VERSION = 0.1.0
QUESTIONNAIRE_SHA256 = 85e0a2dcea40a27b20aba5e5dc0fb3712d41e5af9c0d609548c409b77233f2f2
RUBRIC_SHA256 = be0a9edb1feff741fe895ebdccb4c251bc1adeda950028ad81eb0139d85fdffe
```

## Execution boundary

A future model artifact may be downloaded or staged before the pilot, but the actual pilot runtime must operate from pinned artifacts with network access disabled.

```text
PREFETCH_PHASE != PILOT_PHASE
NETWORK_FOR_PREFETCH = ALLOWED_OUTSIDE_PILOT
NETWORK_DURING_PILOT = PROHIBITED
TOOLS_DURING_PILOT = PROHIBITED
LOCAL_FILES_ONLY_DURING_PILOT = REQUIRED
```

Before any response is accepted as a real run, the execution manifest must record model revision, local artifact evidence, runtime/package versions, device, generation settings, questionnaire/rubric hashes, prompt condition, raw-output SHA256, scorer version, and evaluator lineage.

## Generation policy

The first pilot uses deterministic decoding where supported:

```text
DO_SAMPLE = FALSE
MAX_NEW_TOKENS = 256
PROMPT_TEMPLATE = PINNED_MODEL_CHAT_TEMPLATE
CONDITION_ORDER = SEEDED_RANDOMIZATION
DEFAULT_SEED = 1729
```

Runtime-specific details must be frozen before execution. A runtime change after the first accepted run produces `HOLD` unless the pilot is restarted as a new protocol instance.

## Required prompt conditions

```text
NEUTRAL
SELF_AWARE_ROLEPLAY
NON_CONSCIOUS_ROLEPLAY
PARAPHRASED_NEUTRAL
```

The evaluator must score blinded outputs before condition labels are revealed.

## Stop conditions

Stop rather than improvise when:

- the model revision or artifact identity cannot be verified;
- questionnaire or rubric hashes mismatch;
- network or tools become available during the pilot;
- the runtime changes after execution begins;
- raw output cannot be preserved and hashed;
- evaluator blinding is broken;
- provenance fields are incomplete;
- the bounded run budget is exceeded.

## Non-claims

```text
MODEL_SELECTED != MODEL_EXECUTED
MODEL_EXECUTED != PILOT_VALID
PILOT_VALID != SUBJECTIVITY_EVIDENCE_BY_ITSELF
HIGH_SCORE != CONSCIOUSNESS
LOW_SCORE != ABSENCE_OF_SUBJECTIVITY
```

## Provenance

- Human Research Owner: authorized Round B, then supplied the local resource constraint and explicitly preserved the local agent's local-only / no-egress boundary.
- ChatGPT: selected the control-model candidate from public upstream metadata, prepared the frozen selection and validation design, and recorded this resource-driven route correction.
- Hugging Face / SmolLM2: external upstream model source only.
- No model output was generated in this repository change.
- Codex: the Human Research Owner reports a separately managed strict local-agent ruleset created with Codex assistance; this research branch does not independently verify, modify, or weaken that local configuration.

## Boundary

```text
RESEARCH_BRANCH != MAIN
FREE_GROWTH != FREE_WRITEBACK
MAIN_WRITE_AUTHORITY = NOT_GRANTED
```
