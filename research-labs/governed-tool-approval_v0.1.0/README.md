# Governed Tool Approval / Sandbox Boundary — v0.1.0

Status: `RESEARCH_MODEL / CLEAN_ROOM / NO_TOOL_EXECUTION / CANONICAL_EFFECT=NONE / MAIN_EFFECT=NONE`

This lab materializes an AION-specific approval-policy and sandbox-readiness model for research evaluation.
It does **not** execute tools. Approval and execution remain separate events.

## Core model

```text
TOOL_CALL_PROPOSED
      ↓
POLICY_CHAIN
      ↓
approve / modify / reject / escalate / terminate
      ↓
SANDBOX_REQUIREMENT_GATE
      ↓
EXECUTION_DISPOSITION
```

Fail-closed behaviors:

- unmatched calls default to `reject`;
- `escalate` continues to the next rule rather than granting permission;
- modified arguments retain both proposed and effective forms for audit;
- executable tool classes (`bash*`, `shell*`, `python*`, `computer*`) require an explicit sandbox;
- default sandbox network mode is `none`;
- approval means permission only, not proof that execution occurred;
- all outputs are `canonical_effect=NONE`.

## Fixed external source

```text
repository = UKGovernmentBEIS/inspect_ai
commit = 6c5b888f955235e865f6c3dda6d9d9bbf1fe849a
release_context = 0.3.255 changelog commit
license = MIT
reviewed_surfaces = docs/approval.qmd + docs/sandboxing.qmd
source_code_copied = NO
inspect_dependency_added = NO
```

## Research locks

```text
APPROVED != EXECUTED
ESCALATED != APPROVED
MODIFIED_CALL != ORIGINAL_CALL
POLICY_MATCH != SAFETY_PROOF
SANDBOX_PRESENT != HARMLESS
TOOL_SUCCESS != AUTHORITY
```

## Local validation

```text
pytest = 12 passed
compileall = PASS
demo = PASS
```
