# External Module Intake — Inspect AI Approval / Sandbox — 2026-08-11

Status: `RESEARCH_INTAKE / SOURCE_FIXED / CLEAN_ROOM_SELECTED / MAIN_EFFECT=NONE / CANONICAL_EFFECT=NONE`

```text
REPOSITORY = UKGovernmentBEIS/inspect_ai
COMMIT = 6c5b888f955235e865f6c3dda6d9d9bbf1fe849a
LICENSE = MIT
TARGET_SURFACES = docs/approval.qmd + docs/sandboxing.qmd
WHOLE_FRAMEWORK_VENDORING = NO
```

## IQC disposition

AION already has Risk Gate, Policy Check, Tool Router, Writeback Gate and Audit Sink concepts. The useful external mechanism is the explicit approval-decision chain plus the evaluation-sandbox boundary.

```text
APPROVAL_DECISION_CHAIN = USEFUL
SANDBOX_BOUNDARY = USEFUL
INSPECT_AGENT_RUNTIME = NOT_SELECTED
INSPECT_TOOL_RUNTIME = NOT_SELECTED
CLEAN_ROOM_RECONSTRUCTION = SELECTED
```

## Materialized output

`research-labs/governed-tool-approval_v0.1.0/`

The module is intentionally non-executing. It computes an auditable execution disposition; actual tool execution remains outside this research lab.

## Local validation

```text
pytest = 12 passed
compileall = PASS
demo = PASS
```
