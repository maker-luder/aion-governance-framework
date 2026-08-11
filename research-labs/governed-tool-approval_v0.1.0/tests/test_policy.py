from __future__ import annotations

import pytest

from aion_tool_approval import (
    ApprovalDecision,
    ApprovalPolicy,
    PolicyRule,
    SandboxSpec,
    ToolCall,
    build_execution_disposition,
)


def test_unmatched_call_fails_closed() -> None:
    outcome = ApprovalPolicy(()).decide(ToolCall("unknown"))
    assert outcome.decision is ApprovalDecision.REJECT


def test_simple_approve_rule() -> None:
    policy = ApprovalPolicy((PolicyRule("read", "read_*", ApprovalDecision.APPROVE),))
    assert policy.decide(ToolCall("read_file")).executable is True


def test_prefix_glob_rule_matches() -> None:
    policy = ApprovalPolicy((PolicyRule("browser", "web_browser_*", ApprovalDecision.APPROVE),))
    assert policy.decide(ToolCall("web_browser_go")).decision is ApprovalDecision.APPROVE


def test_argument_specific_rule() -> None:
    policy = ApprovalPolicy((PolicyRule("safe-list", "computer", ApprovalDecision.APPROVE, {"action": "move"}),))
    assert policy.decide(ToolCall("computer", {"action": "move"})).decision is ApprovalDecision.APPROVE
    assert policy.decide(ToolCall("computer", {"action": "key"})).decision is ApprovalDecision.REJECT


def test_escalate_continues_to_next_rule() -> None:
    policy = ApprovalPolicy((
        PolicyRule("needs-owner", "bash", ApprovalDecision.ESCALATE),
        PolicyRule("owner-approved-fixture", "bash", ApprovalDecision.APPROVE),
    ))
    assert policy.decide(ToolCall("bash")).rule_name == "owner-approved-fixture"


def test_modify_preserves_proposed_and_effective_arguments() -> None:
    policy = ApprovalPolicy((PolicyRule(
        "clamp-timeout",
        "python",
        ApprovalDecision.MODIFY,
        modified_arguments={"timeout": 2},
    ),))
    outcome = policy.decide(ToolCall("python", {"code": "print(1)", "timeout": 50}))
    assert outcome.proposed_arguments["timeout"] == 50
    assert outcome.effective_arguments["timeout"] == 2


def test_terminate_is_not_executable() -> None:
    policy = ApprovalPolicy((PolicyRule("stop", "danger*", ApprovalDecision.TERMINATE),))
    assert policy.decide(ToolCall("dangerous")).executable is False


def test_default_sandbox_is_network_isolated() -> None:
    assert SandboxSpec().network_mode == "none"


def test_invalid_sandbox_resource_limits_rejected() -> None:
    with pytest.raises(ValueError):
        SandboxSpec(memory_mb=0)


def test_executable_tool_requires_sandbox_even_if_approved() -> None:
    policy = ApprovalPolicy((PolicyRule("approved", "python", ApprovalDecision.APPROVE),))
    disposition = build_execution_disposition(ToolCall("python", {"code": "1+1"}), policy)
    assert disposition["decision"] == "approve"
    assert disposition["sandbox_required"] is True
    assert disposition["executable"] is False


def test_executable_tool_can_run_only_with_sandbox_ready() -> None:
    policy = ApprovalPolicy((PolicyRule("approved", "python", ApprovalDecision.APPROVE),))
    disposition = build_execution_disposition(ToolCall("python", {"code": "1+1"}), policy, SandboxSpec())
    assert disposition["executable"] is True
    assert disposition["network_mode"] == "none"


def test_approval_is_recorded_as_permission_not_execution() -> None:
    policy = ApprovalPolicy((PolicyRule("approved", "read_file", ApprovalDecision.APPROVE),))
    disposition = build_execution_disposition(ToolCall("read_file", {"path": "fixture.txt"}), policy)
    assert disposition["approval_event_only"] is True
    assert disposition["canonical_effect"] == "NONE"
