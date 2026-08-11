# External Source Crosswalk — Inspect AI → AION Governed Tool Approval / Sandbox Boundary

## Fixed source snapshot

- Repository: `UKGovernmentBEIS/inspect_ai`
- Commit: `6c5b888f955235e865f6c3dda6d9d9bbf1fe849a`
- License: MIT
- Reviewed documentation: `docs/approval.qmd`, `docs/sandboxing.qmd`

## Mechanism extraction

Public Inspect AI documentation describes chained tool approval decisions and evaluation sandboxes. AION reconstructs only the general mechanisms needed to test its own governance pipeline.

| Public mechanism | AION clean-room treatment |
|---|---|
| approve / modify / reject / escalate / terminate | `ApprovalDecision` enum |
| ordered approval rules | `ApprovalPolicy` with fail-closed default |
| argument-aware approval | `PolicyRule.argument_equals` |
| modified tool call | proposed/effective argument audit pair |
| sandbox binding | `SandboxSpec` readiness gate |
| network isolation | default `network_mode="none"` |
| resource limits | positive CPU/memory/read/output bounds |

No Inspect AI source code, agent bridge, tool implementation, or sandbox runtime is copied.
