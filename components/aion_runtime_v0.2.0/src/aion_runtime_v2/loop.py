from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
import json
from typing import Any, Callable, Mapping
from uuid import uuid4

from .provider import ModelRequest, ModelResponseKind, ProviderAdapter, ToolCall
from .session import SessionContextManager
from .tools import ExecutionReceipt, ToolExecutionBridge, ToolRegistry


class RunStatus(str, Enum):
    COMPLETED = "COMPLETED"
    INTERRUPTED = "INTERRUPTED"
    HOLD = "HOLD"
    FAILED = "FAILED"
    BUDGET_EXHAUSTED = "BUDGET_EXHAUSTED"


@dataclass(frozen=True)
class RunBudget:
    max_turns: int = 8
    max_tool_calls: int = 12
    max_retries: int = 2

    def __post_init__(self) -> None:
        if self.max_turns <= 0 or self.max_tool_calls < 0 or self.max_retries < 0:
            raise ValueError("invalid run budget")


@dataclass(frozen=True)
class PendingApproval:
    interrupt_id: str
    call: ToolCall


@dataclass
class RunState:
    run_id: str
    session_id: str
    profile_id: str
    turns: int = 0
    tool_calls: int = 0
    retries: int = 0
    pending: PendingApproval | None = None
    complete: bool = False
    schema_version: str = "0.2.0"
    canonical_effect: str = "NONE"

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, sort_keys=True)

    @classmethod
    def from_json(cls, raw: str) -> "RunState":
        data = json.loads(raw)
        pending_raw = data.pop("pending", None)
        if pending_raw is not None:
            call_raw = pending_raw["call"]
            data["pending"] = PendingApproval(interrupt_id=pending_raw["interrupt_id"], call=ToolCall(call_id=call_raw["call_id"], name=call_raw["name"], arguments=call_raw.get("arguments", {})))
        state = cls(**data)
        if state.schema_version != "0.2.0":
            raise ValueError("unsupported RunState schema_version")
        return state


@dataclass(frozen=True)
class RunResult:
    status: RunStatus
    state: RunState
    final_output: str = ""
    receipts: tuple[ExecutionReceipt, ...] = ()
    reason: str = ""
    canonical_effect: str = "NONE"


ApprovalResolver = Callable[[ToolCall], Mapping[str, Any]]


class AgentRunner:
    """Bounded agent loop with explicit approval and resumable interruption boundaries."""

    def __init__(self, *, provider: ProviderAdapter, session: SessionContextManager, registry: ToolRegistry, bridge: ToolExecutionBridge, approval_resolver: ApprovalResolver, budget: RunBudget | None = None) -> None:
        self.provider = provider
        self.session = session
        self.registry = registry
        self.bridge = bridge
        self.approval_resolver = approval_resolver
        self.budget = budget or RunBudget()
        self._receipts: list[ExecutionReceipt] = []

    def new_state(self) -> RunState:
        return RunState(run_id=f"RUN-{uuid4()}", session_id=self.session.session_id, profile_id=self.provider.profile.profile_id)

    def _validate_state_binding(self, state: RunState) -> None:
        if not state.run_id.strip():
            raise ValueError("RunState run_id must be non-empty")
        if state.session_id != self.session.session_id:
            raise ValueError("RunState session_id does not match the bound SessionContextManager")
        if state.profile_id != self.provider.profile.profile_id:
            raise ValueError("RunState profile_id does not match the bound provider profile")

    def run(self, state: RunState | None = None) -> RunResult:
        state = state or self.new_state()
        self._validate_state_binding(state)
        if state.complete:
            return RunResult(RunStatus.COMPLETED, state, reason="run already complete")
        if state.pending is not None:
            return RunResult(RunStatus.INTERRUPTED, state, reason="pending approval must be resolved before run")
        while state.turns < self.budget.max_turns:
            state.turns += 1
            request = ModelRequest(messages=self.session.assemble_messages(), tools=self.registry.specs(), metadata={"run_id": state.run_id, "session_id": state.session_id, "canonical_effect": "NONE"})
            response = self.provider.complete(request)
            if response.kind is ModelResponseKind.ERROR:
                return RunResult(RunStatus.FAILED, state, receipts=tuple(self._receipts), reason=response.text)
            if response.kind is ModelResponseKind.RETRY:
                state.retries += 1
                if state.retries > self.budget.max_retries:
                    return RunResult(RunStatus.BUDGET_EXHAUSTED, state, receipts=tuple(self._receipts), reason="retry budget exhausted")
                self.session.append(kind="runtime_note", role="system", content=f"model retry requested: {response.retry_reason or response.text}")
                continue
            if response.kind is ModelResponseKind.FINAL:
                self.session.append(kind="message", role="assistant", content=response.text)
                state.complete = True
                return RunResult(RunStatus.COMPLETED, state, final_output=response.text, receipts=tuple(self._receipts), reason="final response")
            if len(response.tool_calls) != 1:
                return RunResult(RunStatus.HOLD, state, receipts=tuple(self._receipts), reason="v0.2 fail-closed boundary permits exactly one tool call per model turn; parallel tool-call resume semantics are not implemented")
            call = response.tool_calls[0]
            state.tool_calls += 1
            if state.tool_calls > self.budget.max_tool_calls:
                return RunResult(RunStatus.BUDGET_EXHAUSTED, state, receipts=tuple(self._receipts), reason="tool-call budget exhausted")
            disposition = dict(self.approval_resolver(call))
            if bool(disposition.get("requires_human", False)):
                interrupt_id = str(disposition.get("interrupt_id") or f"INT-{uuid4()}")
                state.pending = PendingApproval(interrupt_id, call)
                self.session.add_interrupt(interrupt_id=interrupt_id, call_id=call.call_id, tool_name=call.name, arguments=call.arguments, reason=str(disposition.get("reason", "human approval required")))
                return RunResult(RunStatus.INTERRUPTED, state, receipts=tuple(self._receipts), reason="human approval required")
            receipt = self.bridge.execute(call, disposition)
            self._receipts.append(receipt)
            self.session.append(kind="tool_result", role="tool", content=json.dumps({"call_id": call.call_id, "tool": call.name, "executed": receipt.executed, "status": receipt.result_status, "output": receipt.output, "error": receipt.error}, ensure_ascii=False, sort_keys=True), metadata={"call_id": call.call_id, "tool_name": call.name})
            if receipt.result_status in {"HOLD", "REJECT"}:
                return RunResult(RunStatus.HOLD, state, receipts=tuple(self._receipts), reason=receipt.error or receipt.result_status)
        return RunResult(RunStatus.BUDGET_EXHAUSTED, state, receipts=tuple(self._receipts), reason="max turns exhausted")

    def resume(self, state: RunState, disposition: Mapping[str, Any]) -> RunResult:
        self._validate_state_binding(state)
        if state.pending is None:
            raise ValueError("run has no pending approval")
        pending = state.pending
        self.session.resolve_interrupt(pending.interrupt_id)
        state.pending = None
        receipt = self.bridge.execute(pending.call, disposition)
        self._receipts.append(receipt)
        self.session.append(kind="tool_result", role="tool", content=json.dumps({"call_id": pending.call.call_id, "tool": pending.call.name, "executed": receipt.executed, "status": receipt.result_status, "output": receipt.output, "error": receipt.error}, ensure_ascii=False, sort_keys=True), metadata={"call_id": pending.call.call_id, "tool_name": pending.call.name})
        if receipt.result_status in {"HOLD", "REJECT", "NOT_EXECUTED"}:
            return RunResult(RunStatus.HOLD, state, receipts=tuple(self._receipts), reason=receipt.error or receipt.result_status)
        return self.run(state)
