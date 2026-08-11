# External Module Intake — Pydantic Evals — 2026-08-11

Status: `RESEARCH_INTAKE / SOURCE_FIXED / CLEAN_ROOM_SELECTED / MAIN_EFFECT=NONE / CANONICAL_EFFECT=NONE`

## Human direction

The Human Research Owner approved a sequential workflow: retrieve public GitHub repositories, then transform and process suitable mechanisms one at a time for the research branch.

## Source fixed for this cycle

```text
REPOSITORY = pydantic/pydantic-ai
COMMIT = d995cfee9fa4243e3a6f5d8e6762b841f7fde839
COMMIT_TIME = 2026-08-10T23:40:50Z
LICENSE = MIT
TARGET_SURFACE = pydantic_evals
ACQUISITION = GITHUB_CONNECTOR_CONTENTS_API
WHOLE_REPOSITORY_VENDORING = NO
```

The execution container could not directly resolve `github.com`, so source retrieval was performed through the connected GitHub API rather than `git clone`. This does not change the fixed source identity.

## IQC disposition

### Useful mechanism

The external project provides a clear separation between static evaluation definitions, execution, per-case evaluators, experiment reports, and repeated comparison of implementations.

### Existing overlap

AION already has individual experiment fixtures, regression tests, ablations, P1–P5 research flows, evidence gates, and claim-boundary rules. Importing an entire external eval framework would add unnecessary dependency and semantic coupling.

### Gap selected for reconstruction

```text
COMMON_RESEARCH_EVAL_HARNESS = MISSING / USEFUL
EXTERNAL_RUNTIME_DEPENDENCY = NOT_REQUIRED
CLEAN_ROOM_RECONSTRUCTION = SELECTED
```

## Materialized output

`research-labs/research-evaluation-harness_v0.1.0/`

The AION version adds a project-specific `ClaimBoundaryGate` and hard-coded research-only/canonical-none report semantics. It does not copy Pydantic Evals source code and does not claim behavioral equivalence.

## Local validation

```text
pytest = 11 passed
compileall = PASS
demo = PASS
```

## Authority / provenance

- Human Research Owner: authorized the public-repository intake and sequential processing workflow.
- ChatGPT: selected Pydantic Evals as the first conversion target, fixed the source snapshot, performed IQC/overlap analysis, and authored the clean-room materialization.
- Pydantic authors: external source authors only; no project authority is transferred.
- Canonical promotion: not authorized.
