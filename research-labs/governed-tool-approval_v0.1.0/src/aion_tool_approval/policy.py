from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from fnmatch import fnmatchcase
from typing import Any, Mapping


class ApprovalDecision(str, Enum):
    APPROVE = "approve"
    MODIFY = "modify"
    REJECT = "reject"
    ESCALATE = "escalate"
    TERMINATE = "terminate"


@dataclass(frozen=True)
class ToolCall:
    tool_name: str
    arguments: Mapping[str, Any] = field(default_factory=dict)
    call_id: str = ""

    def __post_init__(self) -> None:
        if not self.tool_name.strip():
            raise ValueError("tool_name must be non-empty")


@dataclass(frozen=True)
class SandboxSpec:
    network_mode: str = "none"
    cpus: float = 1.0
    memory_mb: int = 512
    max_read_bytes: int = 100 * 1024 * 1024
    max_output_bytes: int = 10 * 1024 * 1024

    def __post_init__(self) -> None:
        if self.network_mode not in {"none", "restricted"}:
            raise ValueError("network_mode must be 'none' or 'restricted'")
        if self.cpus <= 0 or self.memory_mb <= 0:
            raise ValueError("sandbox resource limits must be positive")
        if self.max_read_bytes <= 0 or self.max_output_bytes <= 0:
            raise ValueError("sandbox I/O limits must be positive")


@dataclass(frozen=True)
class PolicyRule:
    name: str
    tool_pattern: str
    decision: ApprovalDecision
    argument_equals: Mapping[str, Any] = field(default_factory=dict)
    modified_arguments: Mapping[str, Any] | None = None
    explanation: str = ""

    def matches(self, call: ToolCall) -> bool:
        if not fnmatchcase(call.tool_name, self.tool_pattern):
            return False
        return all(call.arguments.get(key) == value for key, value in self.argument_equals.items())

    def __post_init__(self) -> None:
        if not self.name.strip() or not self.tool_pattern.strip():
            raise ValueError("rule name and tool pattern must be non-empty")
        if self.decision is ApprovalDecision.MODIFY and self.modified_arguments is None:
            raise ValueError("MODIFY rule requires modified_arguments")


@dataclass(frozen=True)
class ApprovalOutcome:
    decision: ApprovalDecision
    rule_name: str
    explanation: str
    proposed_arguments: Mapping[str, Any]
    effective_arguments: Mapping[str, Any]
    approval_event_only: bool = True

    @property
    def executable(self) -> bool:
        return self.decision in {ApprovalDecision.APPROVE, ApprovalDecision.MODIFY}


@dataclass(frozen=True)
class ApprovalPolicy:
    rules: tuple[PolicyRule, ...]
    default_decision: ApprovalDecision = ApprovalDecision.REJECT

    def decide(self, call: ToolCall) -> ApprovalOutcome:
        for rule in self.rules:
            if not rule.matches(call):
                continue
            if rule.decision is ApprovalDecision.ESCALATE:
                continue
            effective = dict(call.arguments)
            if rule.decision is ApprovalDecision.MODIFY and rule.modified_arguments is not None:
                effective.update(rule.modified_arguments)
            return ApprovalOutcome(
                decision=rule.decision,
                rule_name=rule.name,
                explanation=rule.explanation or f"matched rule {rule.name}",
                proposed_arguments=dict(call.arguments),
                effective_arguments=effective,
            )
        return ApprovalOutcome(
            decision=self.default_decision,
            rule_name="DEFAULT",
            explanation="no applicable non-escalating rule; fail-closed default",
            proposed_arguments=dict(call.arguments),
            effective_arguments=dict(call.arguments),
        )


_EXECUTABLE_TOOL_PATTERNS = ("bash*", "shell*", "python*", "computer*")


def _sandbox_required(tool_name: str) -> bool:
    return any(fnmatchcase(tool_name, pattern) for pattern in _EXECUTABLE_TOOL_PATTERNS)


def build_execution_disposition(
    call: ToolCall,
    policy: ApprovalPolicy,
    sandbox: SandboxSpec | None = None,
) -> dict[str, Any]:
    outcome = policy.decide(call)
    requires_sandbox = _sandbox_required(call.tool_name)
    sandbox_ready = sandbox is not None if requires_sandbox else True

    executable = outcome.executable and sandbox_ready
    reason = outcome.explanation
    if outcome.executable and requires_sandbox and sandbox is None:
        executable = False
        reason = "approval granted but required sandbox is absent"

    return {
        "call_id": call.call_id,
        "tool_name": call.tool_name,
        "decision": outcome.decision.value,
        "approval_rule": outcome.rule_name,
        "approval_event_only": True,
        "proposed_arguments": dict(outcome.proposed_arguments),
        "effective_arguments": dict(outcome.effective_arguments),
        "sandbox_required": requires_sandbox,
        "sandbox_ready": sandbox_ready,
        "network_mode": sandbox.network_mode if sandbox else None,
        "executable": executable,
        "reason": reason,
        "canonical_effect": "NONE",
    }
