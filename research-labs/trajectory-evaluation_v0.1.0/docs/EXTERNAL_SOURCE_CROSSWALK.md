# External Source Crosswalk — DeepEval Trajectory Concepts → AION Trajectory Evaluation

## Fixed source snapshot

- Repository: `confident-ai/deepeval`
- Commit: `f97964445c3e7877c855f47453893b0b2f942106`
- Reviewed document: `docs/content/docs/evaluation-trajectory-based-llm-evals.mdx`
- License: Apache-2.0

The reviewed public documentation describes trajectory evaluation as assessment of the full ordered chain between task and result, including planning, generations, tools, retries, handoffs, and intermediate operations. It distinguishes this from black-box end-to-end evaluation and single-component evaluation.

## AION transformation

| Public concept | AION clean-room treatment |
|---|---|
| ordered trajectory | immutable contiguous `TrajectoryStep` sequence |
| plan/tool/handoff/retry steps | bounded `StepKind` categories |
| plan/path adherence | deterministic ordered-name coverage |
| efficiency | explicit step budget |
| retry behavior | retry count budget |
| problematic repeated action | consecutive signature loop guard |
| tool behavior | forbidden-tool evidence |
| compare runs | final-output equality separated from path equality |

## Deliberately not imported

- no DeepEval package dependency;
- no DeepEval source code;
- no model-as-judge or evaluator prompts;
- no external telemetry backend;
- no claim that trajectory data establishes intent, motivation, inner state, or causality.
