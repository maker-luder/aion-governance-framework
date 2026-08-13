# Governed Tool Approval Adversarial — Source Notes

## Unit boundary

`governed-tool-approval-adversarial_v0.1.0` is a research-only approval/disposition metadata audit. It does not invoke any tool, execute a command, run a browser/computer action, use a network, or alter canonical state.

## Reused repository evidence

| Source item | Stable reference | Source kind | Status | Transformation |
|---|---|---|---|---|
| Existing approval policy model | `repo:research-labs/governed-tool-approval_v0.1.0/src/aion_tool_approval/policy.py` | Repository Evidence | Current within verified research lineage at the unit commit; exact state bounded by QA receipt | Reused ApprovalDecision, ToolCall, SandboxSpec, PolicyRule, ApprovalPolicy, disposition and approval-event-only semantics; no tool execution was repeated or counted as new evidence |
| Existing governed-tool README/crosswalk | `repo:research-labs/governed-tool-approval_v0.1.0/README.md` and `docs/EXTERNAL_SOURCE_CROSSWALK.md` | Repository Evidence | Current within branch lineage; external methodological source currentness not newly asserted | Added call identity, rule/sandbox, argument mutation, execution-request, batch, and canonical-boundary adversarial checks |
| Current remote main reference | `git:origin/main@abb6550abfacb4fabc53ec04fca783bcc34acfdb` | Tool Output / Repository Evidence | Independently verified by read-only fetch at the latest successful checkpoint | Read-only branch-state reference; no main content or authority modified |

## Synthetic transformation

The audit maps declared call/disposition metadata to `ADMITTED_FOR_REVIEW`, `HOLD`, or `INVALID`. An approval or executable disposition remains an approval event only; it is not evidence that a tool ran. The 20 synthetic cases are fixtures, not external evidence and not replication evidence.

## Provenance vocabulary

```text
APPROVAL != EXECUTION
EXECUTABLE_DISPOSITION != OBSERVED_RESULT
SANDBOX_READY != TOOL_RUN
MODIFIED_ARGUMENTS != EXECUTED_ARGUMENTS
BATCH_REVIEW != COMPLETED_RUN
EVIDENCE_REFERENCE != NEW_EVIDENCE
```

## Non-promotion invariants

```text
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
