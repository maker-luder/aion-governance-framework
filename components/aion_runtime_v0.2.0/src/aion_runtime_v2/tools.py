from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from .provider import ToolCall, ToolSpec
from .sandbox import ExecutorResult, SandboxExecutor, SandboxPolicy


@dataclass(frozen=True)
class ToolDefinition:
    spec: ToolSpec
    execution_class: str = "function"

    def __post_init__(self) -> None:
        if self.execution_class not in {"function", "filesystem", "process", "network", "computer"}:
            raise ValueError("unsupported execution_class")


@dataclass
class ToolRegistry:
    _definitions: dict[str, ToolDefinition] = field(default_factory=dict)

    def register(self, definition: ToolDefinition) -> None:
        name = definition.spec.name
        if name in self._definitions:
            raise ValueError(f"duplicate tool: {name}")
        self._definitions[name] = definition

    def get(self, name: str) -> ToolDefinition:
        try:
            return self._definitions[name]
        except KeyError as exc:
            raise KeyError(f"unknown tool: {name}") from exc

    def specs(self) -> tuple[ToolSpec, ...]:
        return tuple(item.spec for item in self._definitions.values())


@dataclass(frozen=True)
class ExecutionReceipt:
    call_id: str
    tool_name: str
    approval_decision: str
    executed: bool
    result_status: str
    output: Any = None
    error: str | None = None
    canonical_effect: str = "NONE"
    evidence: Mapping[str, Any] = field(default_factory=dict)


class ToolExecutionBridge:
    """Bridge between a separate approval disposition and a separate executor."""

    def __init__(self, *, registry: ToolRegistry, executor: SandboxExecutor, sandbox_policy: SandboxPolicy) -> None:
        self.registry = registry
        self.executor = executor
        self.sandbox_policy = sandbox_policy

    def execute(self, call: ToolCall, disposition: Mapping[str, Any]) -> ExecutionReceipt:
        definition = self.registry.get(call.name)
        decision = str(disposition.get("decision", "reject"))
        if disposition.get("call_id") not in {None, "", call.call_id}:
            return ExecutionReceipt(call.call_id, call.name, decision, False, "REJECT", error="approval disposition call_id mismatch")
        if str(disposition.get("tool_name", call.name)) != call.name:
            return ExecutionReceipt(call.call_id, call.name, decision, False, "REJECT", error="approval disposition tool_name mismatch")
        if not bool(disposition.get("executable", False)):
            return ExecutionReceipt(call.call_id, call.name, decision, False, "NOT_EXECUTED", error=str(disposition.get("reason", "approval did not grant execution")), evidence={"approval_event_only": bool(disposition.get("approval_event_only", True))})
        requires_sandbox = definition.spec.requires_sandbox or definition.execution_class in {"filesystem", "process", "network", "computer"}
        if requires_sandbox and not bool(disposition.get("sandbox_ready", False)):
            return ExecutionReceipt(call.call_id, call.name, decision, False, "HOLD", error="required sandbox not ready")
        effective_arguments = disposition.get("effective_arguments", call.arguments)
        if not isinstance(effective_arguments, Mapping):
            return ExecutionReceipt(call.call_id, call.name, decision, False, "REJECT", error="effective_arguments must be a mapping")
        result: ExecutorResult = self.executor.execute(call.name, effective_arguments, self.sandbox_policy)
        return ExecutionReceipt(call_id=call.call_id, tool_name=call.name, approval_decision=decision, executed=True, result_status=result.status, output=result.output, error=result.error, evidence={**dict(result.sandbox_evidence), "approval_event_only": bool(disposition.get("approval_event_only", True)), "sandbox_required": requires_sandbox})
