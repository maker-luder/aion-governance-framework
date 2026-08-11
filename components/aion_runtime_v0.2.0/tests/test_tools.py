from aion_runtime_v2.provider import ToolCall, ToolSpec
from aion_runtime_v2.sandbox import FunctionSandboxExecutor, SandboxPolicy
from aion_runtime_v2.tools import ToolDefinition, ToolExecutionBridge, ToolRegistry


def make_bridge(requires_sandbox=False):
    registry = ToolRegistry()
    registry.register(ToolDefinition(ToolSpec("echo", requires_sandbox=requires_sandbox)))
    executor = FunctionSandboxExecutor({"echo": lambda args: args["text"]})
    return ToolExecutionBridge(registry=registry, executor=executor, sandbox_policy=SandboxPolicy())


def test_approval_does_not_imply_execution():
    bridge = make_bridge()
    receipt = bridge.execute(ToolCall("C1", "echo", {"text": "x"}), {"decision": "approve", "executable": False, "reason": "approval only"})
    assert receipt.executed is False
    assert receipt.result_status == "NOT_EXECUTED"


def test_modified_effective_arguments_are_executed():
    bridge = make_bridge()
    receipt = bridge.execute(ToolCall("C1", "echo", {"text": "unsafe"}), {"call_id": "C1", "tool_name": "echo", "decision": "modify", "executable": True, "sandbox_ready": True, "effective_arguments": {"text": "safe"}})
    assert receipt.executed is True
    assert receipt.output == "safe"


def test_required_sandbox_fails_closed():
    bridge = make_bridge(requires_sandbox=True)
    receipt = bridge.execute(ToolCall("C1", "echo", {"text": "x"}), {"call_id": "C1", "tool_name": "echo", "decision": "approve", "executable": True, "sandbox_ready": False})
    assert receipt.result_status == "HOLD"


def test_executable_disposition_requires_exact_call_identity():
    bridge = make_bridge()
    call = ToolCall("C1", "echo", {"text": "x"})
    missing = bridge.execute(call, {"decision": "approve", "executable": True, "sandbox_ready": True})
    forged = bridge.execute(call, {"call_id": "C2", "tool_name": "echo", "decision": "approve", "executable": True, "sandbox_ready": True})
    assert missing.result_status == "REJECT"
    assert forged.result_status == "REJECT"
    assert missing.executed is False
    assert forged.executed is False
