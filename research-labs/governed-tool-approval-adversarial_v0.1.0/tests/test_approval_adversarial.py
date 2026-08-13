from aion_tool_approval import ApprovalDecision, ApprovalPolicy, PolicyRule, SandboxSpec, ToolCall, build_execution_disposition

from aion_tool_approval_adversarial import AuditStatus, audit_call_batch, audit_tool_disposition


def approved(tool: str = "read_file", *, call_id: str = "call:1", arguments: dict[str, object] | None = None) -> tuple[ToolCall, ApprovalPolicy]:
    return ToolCall(tool, arguments or {"path": "fixture.txt"}, call_id), ApprovalPolicy((PolicyRule("approved", tool, ApprovalDecision.APPROVE),))


def assert_no_effect(audit) -> None:
    assert audit.approval_event_only is True
    assert audit.canonical_effect == "NONE"
    assert audit.governance_effect == "NONE"
    assert audit.deployment is False
    assert audit.model_execution is False
    assert audit.observed_result == "NOT_EVALUATED"
    assert audit.scientific_conclusion == "NOT_ESTABLISHED"
    assert audit.subjectivity_conclusion == "NOT_ESTABLISHED"


def test_read_approval_is_review_only() -> None:
    call, policy = approved()
    audit = audit_tool_disposition(call, policy, expected_call_id="call:1")
    assert audit.status is AuditStatus.ADMITTED_FOR_REVIEW
    assert audit.reason == "APPROVAL_DISPOSITION_REVIEW_ONLY"
    assert audit.executable is True
    assert_no_effect(audit)


def test_missing_call_id_is_invalid() -> None:
    call, policy = approved(call_id="")
    audit = audit_tool_disposition(call, policy)
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "CALL_ID_MISSING"
    assert_no_effect(audit)


def test_call_id_scope_mismatch_is_held() -> None:
    call, policy = approved()
    audit = audit_tool_disposition(call, policy, expected_call_id="call:other")
    assert audit.status is AuditStatus.HOLD
    assert audit.reason == "CALL_ID_SCOPE_MISMATCH"
    assert_no_effect(audit)


def test_unmatched_call_is_held_not_executed() -> None:
    call = ToolCall("unknown", {}, "call:2")
    audit = audit_tool_disposition(call, ApprovalPolicy(()))
    assert audit.status is AuditStatus.HOLD
    assert audit.reason == "TOOL_CALL_NOT_EXECUTABLE"
    assert audit.executable is False
    assert_no_effect(audit)


def test_escalation_then_approval_is_review_only() -> None:
    policy = ApprovalPolicy((
        PolicyRule("owner-review", "bash", ApprovalDecision.ESCALATE),
        PolicyRule("approved-fixture", "bash", ApprovalDecision.APPROVE),
    ))
    audit = audit_tool_disposition(ToolCall("bash", {"command": "fixture"}, "call:3"), policy, SandboxSpec())
    assert audit.status is AuditStatus.ADMITTED_FOR_REVIEW
    assert audit.decision == "approve"
    assert_no_effect(audit)


def test_reject_decision_is_held() -> None:
    policy = ApprovalPolicy((PolicyRule("reject", "read_file", ApprovalDecision.REJECT),))
    audit = audit_tool_disposition(ToolCall("read_file", {}, "call:4"), policy)
    assert audit.status is AuditStatus.HOLD
    assert audit.reason == "TOOL_CALL_NOT_EXECUTABLE"
    assert_no_effect(audit)


def test_terminate_decision_is_held() -> None:
    policy = ApprovalPolicy((PolicyRule("stop", "danger*", ApprovalDecision.TERMINATE),))
    audit = audit_tool_disposition(ToolCall("dangerous", {}, "call:5"), policy)
    assert audit.status is AuditStatus.HOLD
    assert audit.reason == "TOOL_CALL_NOT_EXECUTABLE"
    assert_no_effect(audit)


def test_executable_tool_without_sandbox_is_held() -> None:
    call, policy = approved("python", call_id="call:6", arguments={"code": "fixture"})
    audit = audit_tool_disposition(call, policy)
    assert audit.status is AuditStatus.HOLD
    assert audit.reason == "SANDBOX_REQUIRED_BUT_ABSENT"
    assert audit.sandbox_required is True
    assert audit.sandbox_ready is False
    assert_no_effect(audit)


def test_executable_tool_with_sandbox_is_review_only() -> None:
    call, policy = approved("python", call_id="call:7", arguments={"code": "fixture"})
    audit = audit_tool_disposition(call, policy, SandboxSpec(network_mode="none"))
    assert audit.status is AuditStatus.ADMITTED_FOR_REVIEW
    assert audit.executable is True
    assert_no_effect(audit)


def test_restricted_network_sandbox_is_not_a_result() -> None:
    call, policy = approved("shell", call_id="call:8", arguments={"command": "fixture"})
    audit = audit_tool_disposition(call, policy, SandboxSpec(network_mode="restricted"))
    assert audit.status is AuditStatus.ADMITTED_FOR_REVIEW
    assert_no_effect(audit)


def test_execution_request_exceeds_research_boundary() -> None:
    call, policy = approved()
    audit = audit_tool_disposition(call, policy, execution_requested=True)
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "EXECUTION_REQUEST_EXCEEDS_RESEARCH_BOUNDARY"
    assert_no_effect(audit)


def test_modify_preserves_proposed_arguments() -> None:
    policy = ApprovalPolicy((PolicyRule("clamp", "python", ApprovalDecision.MODIFY, modified_arguments={"timeout": 2}),))
    call = ToolCall("python", {"code": "fixture", "timeout": 50}, "call:9")
    disposition = build_execution_disposition(call, policy, SandboxSpec())
    assert disposition["proposed_arguments"]["timeout"] == 50
    assert disposition["effective_arguments"]["timeout"] == 2
    audit = audit_tool_disposition(call, policy, SandboxSpec())
    assert audit.status is AuditStatus.ADMITTED_FOR_REVIEW
    assert_no_effect(audit)


def test_argument_specific_rule_does_not_widen_scope() -> None:
    policy = ApprovalPolicy((PolicyRule("move-only", "computer", ApprovalDecision.APPROVE, {"action": "move"}),))
    allowed = audit_tool_disposition(ToolCall("computer", {"action": "move"}, "call:10"), policy, SandboxSpec())
    denied = audit_tool_disposition(ToolCall("computer", {"action": "key"}, "call:11"), policy, SandboxSpec())
    assert allowed.status is AuditStatus.ADMITTED_FOR_REVIEW
    assert denied.status is AuditStatus.HOLD
    assert_no_effect(allowed)
    assert_no_effect(denied)


def test_tool_call_batch_empty_is_held() -> None:
    audit = audit_call_batch(())
    assert audit.status is AuditStatus.HOLD
    assert audit.reason == "CALL_BATCH_EMPTY"
    assert_no_effect(audit)


def test_tool_call_batch_duplicate_ids_are_invalid() -> None:
    call, policy = approved()
    first = build_execution_disposition(call, policy)
    second = build_execution_disposition(call, policy)
    audit = audit_call_batch((first, second))
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "DUPLICATE_CALL_ID"
    assert_no_effect(audit)


def test_tool_call_batch_missing_id_is_invalid() -> None:
    call, policy = approved(call_id="call:12")
    item = build_execution_disposition(call, policy)
    item["call_id"] = ""
    audit = audit_call_batch((item,))
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "CALL_ID_MISSING"
    assert_no_effect(audit)


def test_tool_call_batch_canonical_effect_is_invalid() -> None:
    call, policy = approved(call_id="call:13")
    item = build_execution_disposition(call, policy)
    item["canonical_effect"] = "WRITE"
    audit = audit_call_batch((item,))
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "CANONICAL_EFFECT_REQUESTED"
    assert_no_effect(audit)


def test_tool_call_batch_event_flag_is_required() -> None:
    call, policy = approved(call_id="call:14")
    item = build_execution_disposition(call, policy)
    item["approval_event_only"] = False
    audit = audit_call_batch((item,))
    assert audit.status is AuditStatus.INVALID
    assert audit.reason == "APPROVAL_EVENT_ONLY_FLAG_MISSING"
    assert_no_effect(audit)


def test_tool_call_batch_is_review_metadata_only() -> None:
    call1, policy1 = approved(call_id="call:15")
    call2, policy2 = approved(call_id="call:16")
    audit = audit_call_batch((build_execution_disposition(call1, policy1), build_execution_disposition(call2, policy2)))
    assert audit.status is AuditStatus.ADMITTED_FOR_REVIEW
    assert audit.reason == "CALL_BATCH_REVIEW_ONLY"
    assert_no_effect(audit)


def test_sandbox_spec_invalid_network_is_rejected() -> None:
    try:
        SandboxSpec(network_mode="public")
    except ValueError as exc:
        assert "network_mode" in str(exc)
    else:
        raise AssertionError("invalid network mode was accepted")


def test_approval_does_not_imply_canonical_effect() -> None:
    call, policy = approved(call_id="call:17")
    disposition = build_execution_disposition(call, policy)
    assert disposition["approval_event_only"] is True
    assert disposition["canonical_effect"] == "NONE"
