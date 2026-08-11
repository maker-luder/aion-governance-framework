from aion_tool_approval import ApprovalDecision, ApprovalPolicy, PolicyRule, SandboxSpec, ToolCall, build_execution_disposition

policy = ApprovalPolicy((
    PolicyRule("safe-read", "read_*", ApprovalDecision.APPROVE),
    PolicyRule("python-review", "python", ApprovalDecision.ESCALATE),
    PolicyRule("owner-fixture", "python", ApprovalDecision.MODIFY, modified_arguments={"timeout": 2}),
))

print(build_execution_disposition(ToolCall("read_file", {"path": "fixture.txt"}, "c1"), policy))
print(build_execution_disposition(ToolCall("python", {"code": "print(1)", "timeout": 60}, "c2"), policy, SandboxSpec()))
