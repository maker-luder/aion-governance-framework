# Trajectory Evaluation — v0.1.0

Status: `RESEARCH_MODEL / CLEAN_ROOM / DETERMINISTIC_EVAL / CANONICAL_EFFECT=NONE / MAIN_EFFECT=NONE`

This lab evaluates the recorded ordered path of an agent-like research execution rather than only its final output. It is methodologically informed by public DeepEval trajectory-evaluation documentation, but it does not import DeepEval or use model-as-judge scoring.

## Core question

Two implementations can return the same final output while taking materially different recorded paths.

```text
SAME_OUTPUT != SAME_RECORDED_PATH
RECORDED_PATH != CAUSAL_MECHANISM
TRAJECTORY_SCORE != THEORY_VALIDITY
```

## Implemented deterministic evidence

- contiguous ordered `TrajectoryStep` records;
- explicit step kinds: PLAN, LLM, TOOL, HANDOFF, RETRY, OBSERVE, FINAL;
- expected ordered path coverage using deterministic longest-common-subsequence matching;
- maximum step budget;
- retry budget;
- forbidden-tool detection limited to TOOL steps;
- consecutive identical-step loop guard;
- same-task trajectory comparison that separately reports final-output equality and recorded-path equality;
- every comparison fixes `causal_claim=NOT_ESTABLISHED` and `canonical_effect=NONE`.

## Fixed external source

```text
repository = confident-ai/deepeval
commit = f97964445c3e7877c855f47453893b0b2f942106
reviewed = docs/content/docs/evaluation-trajectory-based-llm-evals.mdx
license = Apache-2.0
source_code_copied = NO
deepeval_dependency_added = NO
model_judge_added = NO
```

## Standing locks

```text
FINAL_OUTPUT != TRAJECTORY
TRAJECTORY != CAUSAL_EXPLANATION
PLAN_ADHERENCE != SUBJECTIVITY
STEP_EFFICIENCY != INTENT
RETRY_PATTERN != MOTIVATION
TRACE_PATH != INNER_STATE
```

## Local validation

```text
pytest = 14 passed
compileall = PASS
demo = PASS
```

The demo intentionally shows `same_final_output=True` and `same_recorded_path=False` for two implementations.
