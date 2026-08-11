# External Module Intake — DeepEval Trajectory Evaluation — 2026-08-11

Status: `RESEARCH_INTAKE / SOURCE_FIXED / CLEAN_ROOM_SELECTED / MAIN_EFFECT=NONE / CANONICAL_EFFECT=NONE`

```text
REPOSITORY = confident-ai/deepeval
COMMIT = f97964445c3e7877c855f47453893b0b2f942106
LICENSE = Apache-2.0
TARGET = docs/content/docs/evaluation-trajectory-based-llm-evals.mdx
WHOLE_FRAMEWORK_VENDORING = NO
MODEL_JUDGE_IMPORT = NO
```

## IQC disposition

AION already evaluates outputs, isolated mechanisms, ablations and causal-validity boundaries. The useful gap is an explicit deterministic representation and evaluation of the full recorded execution path.

```text
ORDERED_TRAJECTORY = USEFUL
SAME_OUTPUT_DIFFERENT_PATH_COMPARISON = USEFUL
DETERMINISTIC_METRICS = SELECTED
EXTERNAL_MODEL_SCORING = NOT_SELECTED
CLEAN_ROOM_RECONSTRUCTION = SELECTED
```

## Materialized output

`research-labs/trajectory-evaluation_v0.1.0/`

The module evaluates recorded path properties only. It explicitly refuses to treat trajectory differences as evidence of intent, motivation, inner state, or causal mechanism.

## Local validation

```text
pytest = 14 passed
compileall = PASS
demo = PASS
```
