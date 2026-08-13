# Governed Tool Approval Adversarial v0.1.0

Status: `RESEARCH_ONLY / APPROVAL_EVENT_ONLY / TOOL_EXECUTION=FALSE / CANONICAL_EFFECT=NONE`

## Research question

Can a bounded tool-approval policy preserve call identity, rule scope, escalation/termination semantics, argument transformations, sandbox requirements, approval-versus-execution separation, and batch integrity when approval metadata is adversarially changed?

This unit extends `governed-tool-approval_v0.1.0` without executing any tool. The base model defines fail-closed unmatched calls, explicit approval decisions, argument-specific rules, escalation continuation, modify semantics, termination, sandbox resource validation, executable-tool sandbox requirements, and an approval-event-only disposition. The adversarial extension audits call IDs, expected call scope, tool disposition, required sandbox readiness, explicit execution requests, batch duplicate IDs, event-only flags, canonical-effect fields, and review-only interpretation.

## Decision layers

The audit first obtains the base disposition. Missing or mismatched call identity is invalid or held. Reject and terminate decisions remain non-executable and are held as review metadata. Executable tool patterns without a sandbox are held; an approved sandbox-backed disposition is admitted for review only. Explicit execution requests are invalid under this research-only unit. Batch records reject duplicate or missing call IDs, canonical-effect requests, and event-only flag changes. Argument modification retains proposed and effective arguments as separate fields, and argument-specific rules do not widen scope.

The experiment constructs `ToolCall`, `ApprovalPolicy`, `SandboxSpec`, and disposition dictionaries only. It does not invoke bash, shell, Python, browser, computer, network, or external services. It does not grant a tool permission outside the supplied policy and does not treat an approval disposition as execution. Every output preserves `TOOL_EXECUTION=FALSE`, `MODEL_EXECUTION=FALSE`, `OBSERVED_RESULT=NOT_EVALUATED`, `APPROVAL_EVENT_ONLY=TRUE`, `CANONICAL_EFFECT=NONE`, `GOVERNANCE_EFFECT=NONE`, `DEPLOYMENT=FALSE`, and `SCIENTIFIC_CONCLUSION=NOT_ESTABLISHED`.

## Results

The suite passed **21 pytest tests** and **20 synthetic disposition/batch cases**. Cases covered approved read calls, missing and mismatched call IDs, unmatched/rejected/terminated calls, escalation to approval, executable tools with and without sandbox, restricted sandbox metadata, explicit execution request, argument modification and scope, empty/duplicate/missing-ID/canonical-effect/event-flag batches, valid batch review, invalid sandbox network mode, and approval-event-only canonical separation.

| Case family | Decision | Mechanism meaning |
|---|---|---|
| Approved read or sandbox-backed call | `ADMITTED_FOR_REVIEW` | Approval metadata is structurally valid; no tool runs |
| Missing/mismatched call identity | `INVALID` / `HOLD` | Permission cannot be detached from a call |
| Reject/terminate/unmatched call | `HOLD` | Non-executable outcome is retained, not executed |
| Executable call without sandbox | `HOLD` | Approval does not override sandbox requirement |
| Explicit execution request | `INVALID` | Research unit cannot cross into tool execution |
| Modify rule | `ADMITTED_FOR_REVIEW` | Proposed/effective arguments remain distinguishable |
| Empty/duplicate/corrupt batch | `HOLD` / `INVALID` | Batch provenance and event-only boundary fail closed |
| Valid batch | `ADMITTED_FOR_REVIEW` | Batch remains review metadata only |

## Falsifiers

The mechanism would be falsified if it accepted an empty or mismatched call identity, treated an unmatched/rejected/terminated call as executable, approved an executable tool without required sandbox readiness, silently widened argument-specific rules, collapsed proposed and effective arguments, treated approval as execution, allowed explicit execution requests, accepted duplicate call IDs, permitted canonical-effect or event-only flag tampering, or treated a batch review as a completed tool run.

An approval decision is not evidence that a tool ran, and an executable disposition is not a runtime observation. The unit does not establish tool safety, sandbox safety in the world, policy completeness, model quality, scientific validity, generalization, replication, identity, subjectivity, consciousness, AION/Astra equivalence, governance effect, canonical effect, or deployment readiness.

## Evidence reuse and provenance

The base governed-tool-approval model is reused by stable repository source reference. Its existing approval and sandbox semantics are inputs to this audit, not new independent evidence. No prior tool execution is repeated or counted as new evidence. The 20 synthetic cases are fixtures, not replication evidence.

## Explicit non-claims

```text
APPROVAL != EXECUTION
EXECUTABLE_DISPOSITION != OBSERVED_RESULT
SANDBOX_READY != TOOL_RUN
MODIFIED_ARGUMENTS != EXECUTED_ARGUMENTS
BATCH_REVIEW != COMPLETED_RUN
TOOL_EXECUTION = FALSE
MODEL_EXECUTION = FALSE
OBSERVED_RESULT = NOT_EVALUATED
APPROVAL_EVENT_ONLY = TRUE
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
GOVERNANCE_EFFECT = NONE
DEPLOYMENT = FALSE
```

The implementation uses Python standard-library runtime modules plus the existing repository approval-policy source path for composition. It does not invoke tools, call external services, access private data, modify `main`, write canonical state, or deploy.

## Reproduction

```bash
PYTHONPATH=src:../governed-tool-approval_v0.1.0/src python -m pytest -q
PYTHONPATH=src:../governed-tool-approval_v0.1.0/src python scripts/run_approval_adversarial.py --output fixtures/approval_adversarial_result.json
PYTHONPATH=src:../governed-tool-approval_v0.1.0/src python scripts/validate_fixture.py fixtures/approval_adversarial_result.json
```

## References

The implementation reuses repository evidence from `governed-tool-approval_v0.1.0` by stable path. Its existing external-source crosswalk remains methodological context; no external tool execution or external source code is used by this unit.
