from aion_runtime_v2 import AIONRuntimeV2Candidate, DeploymentEventType, EndpointProfile, FunctionSandboxExecutor, ModelResponse, ModelResponseKind, SandboxPolicy, ScriptedProviderAdapter, ToolCall, ToolDefinition, ToolExecutionBridge, ToolRegistry, ToolSpec


def test_runtime_v2_full_synthetic_turn():
    provider = ScriptedProviderAdapter(EndpointProfile.vllm("synthetic"), [ModelResponse(ModelResponseKind.TOOL_CALLS, tool_calls=(ToolCall("C1", "echo", {"text": "x"}),)), ModelResponse(ModelResponseKind.FINAL, text="finished")])
    registry = ToolRegistry()
    registry.register(ToolDefinition(ToolSpec("echo")))
    bridge = ToolExecutionBridge(registry=registry, executor=FunctionSandboxExecutor({"echo": lambda args: args["text"]}), sandbox_policy=SandboxPolicy())
    def approve(call):
        return {"call_id": call.call_id, "tool_name": call.name, "decision": "approve", "executable": True, "sandbox_ready": True, "effective_arguments": call.arguments}
    runtime = AIONRuntimeV2Candidate(provider=provider, registry=registry, bridge=bridge, approval_resolver=approve)
    runtime.start_service()
    runtime.record_deployment(event_type=DeploymentEventType.FIRST_INSTANTIATION, deployment_id="D1", runtime_instance_id="R1", lineage_id="L1")
    result = runtime.run_turn(session_id="S1", user_input="go")
    assert result.final_output == "finished"
    assert runtime.deployments.verify_chain()
    assert runtime.status().canonical_effect == "NONE"
    assert runtime.status().deployment == "FALSE"
