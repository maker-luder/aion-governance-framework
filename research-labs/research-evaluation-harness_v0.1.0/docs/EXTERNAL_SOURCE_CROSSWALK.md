# External Source Crosswalk — Pydantic Evals → AION Research Evaluation Harness

## Fixed source snapshot

- Repository: `pydantic/pydantic-ai`
- Commit: `d995cfee9fa4243e3a6f5d8e6762b841f7fde839`
- Commit message: `Add repository-owned unified docs navigation (#7361)`
- Commit timestamp: `2026-08-10T23:40:50Z`
- License at fixed commit: MIT
- Acquisition path: GitHub connector / Contents API because the execution container had no direct GitHub DNS access.

## Reviewed concepts

The public Pydantic Evals documentation separates:

```text
Dataset / Case / Evaluator / Experiment / EvaluationReport
```

and explicitly supports applying the same dataset to different implementations for comparison over time.

## AION transformation

| External concept | AION clean-room counterpart | Transformation |
|---|---|---|
| Dataset | `ResearchDataset` | Narrowed to research-only cases/evaluators |
| Case | `ResearchCase` | Adds stable `case_id` and metadata preservation |
| Evaluator | evaluator protocol + `EvidenceResult` | Evidence is explicit and reason-bearing |
| Experiment | `evaluate_dataset()` | Binds results to `implementation_id` |
| EvaluationReport | `ExperimentReport` | Adds `research_only=True`, `canonical_effect=NONE` |
| Compare implementations | `compare_reports()` | Requires same dataset; output remains research evidence |
| No direct counterpart | `ClaimBoundaryGate` | AION-specific fail-closed promotion boundary |

## Deliberately not imported

- no `pydantic_evals` package dependency;
- no Pydantic Evals source files copied;
- no external telemetry backend;
- no external evaluator prompts or model-based scorers;
- no claim that this reproduces Pydantic Evals behavior or benchmark results.

## Clean-room statement

The implementation was written from AION research requirements after reviewing public concepts and documentation. External source ownership and license remain attributed to their original project. This module is an independent research artifact, not a fork or vendored copy.
