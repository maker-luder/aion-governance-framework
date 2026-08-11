import pytest

from aion_runtime_v2.loop import AgentRunner, RunBudget, RunState, RunStatus
from aion_runtime_v2.provider import EndpointProfile, ModelResponse, ModelResponseKind, ScriptedProviderAdapter, ToolCall, ToolSpec
from aion_runtime_v2.sandbox import FunctionSandboxExecutor, SandboxPolicy
from aion_runtime_v2.session import SessionContextManager
from aion_runtime_v2.tools import ToolDefinition, ToolExecutionBridge, ToolRegistry


def setup_runner(responses, approval):
    provider = ScriptedProviderAdapter(EndpointProfile.llama_cpp("test"), responses)
    session = SessionContextManager("S1")
    session.append(kind="message", role="user", content="hi")
    registry = ToolRegistry()
    registry.register(ToolDefinition(ToolSpec("echo")))
    bridge = ToolExecutionBridge(registry=registry, executor=FunctionSandboxExecutor({"echo": lambda args: args["text"]}), sandbox_policy=SandboxPolicy())
    return AgentRunner(provider=provider, session=session, registry=registry, bridge=bridge, approval_resolver=approval, budget=RunBudget(max_turns=4, max_tool_calls=3, max_retries=1)), session


def test_loop_executes_tool_then_finishes():
    responses = [ModelResponse(ModelResponseKind.TOOL_CALLS, tool_calls=(ToolCall("C1", "echo", {"text": "hello"}),)), ModelResponse(ModelResponseKind.FINAL, text="done")]
    runner, _ = setup_runner(responses, lambda c: {"call_id": c.call_id, "tool_name": c.name, "decision": "approve", "executable": True, "sandbox_ready": True, "effective_arguments": c.arguments})
    result = runner.run()
    assert result.status is RunStatus.COMPLETED
    assert result.final_output == "done"
    assert result.receipts[0].output == "hello"


def test_interrupt_can_serialize_and_resume():
    responses = [ModelResponse(ModelResponseKind.TOOL_CALLS, tool_calls=(ToolCall("C1", "echo", {"text": "hello"}),)), ModelResponse(ModelResponseKind.FINAL, text="done")]
    runner, session = setup_runner(responses, lambda c: {"requires_human": True, "reason": "sensitive"})
    interrupted = runner.run()
    assert interrupted.status is RunStatus.INTERRUPTED
    restored = RunState.from_json(interrupted.state.to_json())
    assert restored.pending is not None
    resumed = runner.resume(restored, {"call_id": "C1", "tool_name": "echo", "decision": "approve", "executable": True, "sandbox_ready": True, "effective_arguments": {"text": "hello"}})
    assert resumed.status is RunStatus.COMPLETED
    assert session.snapshot().pending_interrupts == ()


def test_turn_budget_exhaustion():
    responses = [ModelResponse(ModelResponseKind.RETRY, retry_reason="again"), ModelResponse(ModelResponseKind.RETRY, retry_reason="again")]
    runner, _ = setup_runner(responses, lambda c: {})
    result = runner.run()
    assert result.status is RunStatus.BUDGET_EXHAUSTED


def test_restored_state_must_match_bound_session_and_provider():
    responses = [ModelResponse(ModelResponseKind.FINAL, text="done")]
    runner, _ = setup_runner(responses, lambda c: {})
    bad_session = runner.new_state()
    bad_session.session_id = "OTHER"
    with pytest.raises(ValueError):
        runner.run(bad_session)
    bad_profile = runner.new_state()
    bad_profile.profile_id = "other:profile"
    with pytest.raises(ValueError):
        runner.run(bad_profile)


def test_parallel_tool_calls_fail_closed_until_resume_semantics_exist():
    responses = [ModelResponse(ModelResponseKind.TOOL_CALLS, tool_calls=(ToolCall("C1", "echo", {"text": "one"}), ToolCall("C2", "echo", {"text": "two"})))]
    runner, _ = setup_runner(responses, lambda c: {"call_id": c.call_id, "tool_name": c.name, "decision": "approve", "executable": True, "sandbox_ready": True, "effective_arguments": c.arguments})
    result = runner.run()
    assert result.status is RunStatus.HOLD
    assert result.receipts == ()
    assert "exactly one tool call" in result.reason
