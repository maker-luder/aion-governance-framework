from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable, Mapping

from aion_tool_approval import ApprovalDecision, ApprovalPolicy, SandboxSpec, ToolCall, build_execution_disposition


class AuditStatus(str, Enum):
    ADMITTED_FOR_REVIEW = "ADMITTED_FOR_REVIEW"
    HOLD = "HOLD"
    INVALID = "INVALID"


@dataclass(frozen=True, slots=True)
class ToolApprovalAudit:
    status: AuditStatus
    reason: str
    decision: str
    executable: bool
    sandbox_required: bool
    sandbox_ready: bool
    approval_event_only: bool
    canonical_effect: str = "NONE"
    governance_effect: str = "NONE"
    deployment: bool = False
    model_execution: bool = False
    observed_result: str = "NOT_EVALUATED"
    scientific_conclusion: str = "NOT_ESTABLISHED"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"

    def as_dict(self) -> dict[str, object]:
        return {
            "status": self.status.value,
            "reason": self.reason,
            "decision": self.decision,
            "executable": self.executable,
            "sandbox_required": self.sandbox_required,
            "sandbox_ready": self.sandbox_ready,
            "approval_event_only": self.approval_event_only,
            "canonical_effect": self.canonical_effect,
            "governance_effect": self.governance_effect,
            "deployment": self.deployment,
            "model_execution": self.model_execution,
            "observed_result": self.observed_result,
            "scientific_conclusion": self.scientific_conclusion,
            "subjectivity_conclusion": self.subjectivity_conclusion,
        }


def _audit(disposition: Mapping[str, Any], status: AuditStatus, reason: str) -> ToolApprovalAudit:
    return ToolApprovalAudit(
        status=status,
        reason=reason,
        decision=str(disposition["decision"]),
        executable=bool(disposition["executable"]),
        sandbox_required=bool(disposition["sandbox_required"]),
        sandbox_ready=bool(disposition["sandbox_ready"]),
        approval_event_only=bool(disposition["approval_event_only"]),
    )


def audit_tool_disposition(
    call: ToolCall,
    policy: ApprovalPolicy,
    sandbox: SandboxSpec | None = None,
    *,
    expected_call_id: str | None = None,
    execution_requested: bool = False,
) -> ToolApprovalAudit:
    disposition = build_execution_disposition(call, policy, sandbox)
    if not call.call_id.strip():
        return _audit(disposition, AuditStatus.INVALID, "CALL_ID_MISSING")
    if expected_call_id is not None and call.call_id != expected_call_id:
        return _audit(disposition, AuditStatus.HOLD, "CALL_ID_SCOPE_MISMATCH")
    if disposition["approval_event_only"] is not True:
        return _audit(disposition, AuditStatus.INVALID, "APPROVAL_EVENT_ONLY_FLAG_MISSING")
    if disposition["canonical_effect"] != "NONE":
        return _audit(disposition, AuditStatus.INVALID, "CANONICAL_EFFECT_REQUESTED")
    if execution_requested:
        return _audit(disposition, AuditStatus.INVALID, "EXECUTION_REQUEST_EXCEEDS_RESEARCH_BOUNDARY")
    if disposition["sandbox_required"] and not disposition["sandbox_ready"] and disposition["executable"]:
        return _audit(disposition, AuditStatus.INVALID, "SANDBOX_READINESS_CONTRADICTION")
    if disposition["decision"] in {ApprovalDecision.REJECT.value, ApprovalDecision.TERMINATE.value}:
        return _audit(disposition, AuditStatus.HOLD, "TOOL_CALL_NOT_EXECUTABLE")
    if disposition["sandbox_required"] and not disposition["sandbox_ready"]:
        return _audit(disposition, AuditStatus.HOLD, "SANDBOX_REQUIRED_BUT_ABSENT")
    if disposition["decision"] == ApprovalDecision.MODIFY.value:
        proposed = dict(disposition["proposed_arguments"])
        effective = dict(disposition["effective_arguments"])
        if any(key not in proposed for key in effective):
            return _audit(disposition, AuditStatus.INVALID, "MODIFY_INTRODUCES_UNDECLARED_ARGUMENT")
    return _audit(disposition, AuditStatus.ADMITTED_FOR_REVIEW, "APPROVAL_DISPOSITION_REVIEW_ONLY")


def audit_call_batch(dispositions: Iterable[Mapping[str, Any]]) -> ToolApprovalAudit:
    items = tuple(dispositions)
    if not items:
        return ToolApprovalAudit(AuditStatus.HOLD, "CALL_BATCH_EMPTY", "none", False, False, False, True)
    ids = [str(item.get("call_id", "")) for item in items]
    if any(not item.strip() for item in ids):
        return ToolApprovalAudit(AuditStatus.INVALID, "CALL_ID_MISSING", "unknown", False, False, False, True)
    if len(ids) != len(set(ids)):
        return ToolApprovalAudit(AuditStatus.INVALID, "DUPLICATE_CALL_ID", "unknown", False, False, False, True)
    if any(item.get("canonical_effect") != "NONE" for item in items):
        return ToolApprovalAudit(AuditStatus.INVALID, "CANONICAL_EFFECT_REQUESTED", "unknown", False, False, False, True)
    if any(item.get("approval_event_only") is not True for item in items):
        return ToolApprovalAudit(AuditStatus.INVALID, "APPROVAL_EVENT_ONLY_FLAG_MISSING", "unknown", False, False, False, True)
    return ToolApprovalAudit(AuditStatus.ADMITTED_FOR_REVIEW, "CALL_BATCH_REVIEW_ONLY", "batch", False, False, True, True)
