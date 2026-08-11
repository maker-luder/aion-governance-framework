from aion_runtime_v2 import AIONRuntimeV2Candidate, DeploymentEventType, EndpointProfile, FunctionSandboxExecutor, ModelResponse, ModelResponseKind, SandboxPolicy, ScriptedProviderAdapter, ToolCall, ToolDefinition, ToolExecutionBridge, ToolRegistry, ToolSpec


def main() -> None:
    profile = EndpointProfile.llama_cpp("synthetic-local-model")
    provider = ScriptedProviderAdapter(profile, [ModelResponse(ModelResponseKind.TOOL_CALLS, tool_calls=(ToolCall("C1", "echo", {"text": "hello"}),)), ModelResponse(ModelResponseKind.FINAL, text="done")])
    registry = ToolRegistry()
    registry.register(ToolDefinition(ToolSpec("echo", "echo text")))
    executor = FunctionSandboxExecutor({"echo": lambda args: args["text"]})
    bridge = ToolExecutionBridge(registry=registry, executor=executor, sandbox_policy=SandboxPolicy())
    def approve(call: ToolCall) -> dict[str, object]:
        return {"call_id": call.call_id, "tool_name": call.name, "decision": "approve", "approval_event_only": True, "effective_arguments": dict(call.arguments), "sandbox_ready": True, "executable": True}
    runtime = AIONRuntimeV2Candidate(provider=provider, registry=registry, bridge=bridge, approval_resolver=approve)
    runtime.start_service()
    runtime.record_deployment(event_type=DeploymentEventType.FIRST_INSTANTIATION, deployment_id="DEPLOY-DEMO", runtime_instance_id="AION-I-DEMO", lineage_id="AION-LINEAGE-DEMO")
    result = runtime.run_turn(session_id="S-DEMO", user_input="echo hello")
    print(runtime.status().to_dict())
    print(result.status.value, result.final_output, runtime.deployments.verify_chain())


if __name__ == "__main__":
    main()
