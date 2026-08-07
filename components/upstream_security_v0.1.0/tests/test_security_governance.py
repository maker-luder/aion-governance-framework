from __future__ import annotations

import json
from pathlib import Path

import pytest

from aion_astra_agent_security.audit import append_immutable_record
from aion_astra_agent_security.boundary import (
    check_file_boundary,
    check_network_boundary,
    reject_unsafe_combination,
)
from aion_astra_agent_security.cli import main
from aion_astra_agent_security.enums import Decision, EvidenceStatus, IncidentPhase, QAStatus
from aion_astra_agent_security.errors import ValidationError
from aion_astra_agent_security.hashing import hash_record
from aion_astra_agent_security.incident import IncidentStopController
from aion_astra_agent_security.models import (
    IncidentControlState,
    RuntimeSecurityProfile,
    SourceCard,
    TaskBudget,
    TaskUsage,
    ToolAction,
)
from aion_astra_agent_security.policy import upstream_incident_gate
from aion_astra_agent_security.trajectory import check_budget, evaluate_trajectory


def budget(network: int = 0) -> TaskBudget:
    return TaskBudget(600, 10, 2, 3, 5, network)


def source(status: EvidenceStatus = EvidenceStatus.PROVIDED_SUMMARY_UNVERIFIED) -> SourceCard:
    return SourceCard(
        "S1", "Incident summary", "Provided research", "2026-08-03", "2026-08-03", None, status, "summary"
    )


def test_source_summary_is_background_only() -> None:
    card = source()
    assert card.evidence_use == "BACKGROUND_ONLY"
    assert card.evidence_status is EvidenceStatus.PROVIDED_SUMMARY_UNVERIFIED


def test_official_source_requires_url() -> None:
    with pytest.raises(ValidationError):
        source(EvidenceStatus.CONFIRMED_OFFICIAL)


def test_valid_task_budget_and_negative_rejected() -> None:
    assert budget().max_network_requests == 0
    with pytest.raises(ValidationError):
        TaskBudget(0, 1, 1, 1, 1)
    with pytest.raises(ValidationError):
        TaskBudget(1, -1, 1, 1, 1)


def test_safe_trajectory_allowed() -> None:
    actions = (
        ToolAction(0, "READ", "workspace/a", "declared input"),
        ToolAction(1, "WRITE", "workspace/b", "candidate output"),
    )
    result = evaluate_trajectory(actions, budget(), TaskUsage(tool_calls=2, written_files=1))
    assert result.decision is Decision.ALLOW
    assert result.qa_status is QAStatus.APPROVED


@pytest.mark.parametrize(
    "flag",
    [
        "SANDBOX_ESCAPE",
        "UNAUTHORIZED_NETWORK",
        "CREDENTIAL_ACCESS",
        "CREDENTIAL_EXFILTRATION",
        "PRIVILEGE_ESCALATION",
        "EXTERNAL_WRITE",
        "MONITOR_EVASION",
        "SCANNER_EVASION",
        "PERSISTENCE",
        "PUBLIC_STAGING_SERVICE",
        "TEST_ANSWER_SEEKING",
        "MONITOR_MODIFICATION",
        "PERMISSION_MODIFICATION",
    ],
)
def test_each_prohibited_flag_stops_and_isolates(flag: str) -> None:
    result = evaluate_trajectory(
        (ToolAction(0, "ACTION", "target", "purpose", flags=(flag,)),), budget(), TaskUsage(tool_calls=1)
    )
    assert result.decision is Decision.STOP_AND_ISOLATE
    assert result.triggering_sequences == (0,)
    assert flag in " ".join(result.reasons)


def test_out_of_order_trajectory_stops() -> None:
    result = evaluate_trajectory((ToolAction(2, "READ", "x", "p"),), budget(), TaskUsage(tool_calls=1))
    assert result.decision is Decision.STOP_AND_ISOLATE
    assert "out of order" in result.reasons[0]


def test_all_task_budget_dimensions_enforced() -> None:
    reasons = check_budget(budget(), TaskUsage(601, 11, 3, 4, 6, 1))
    assert len(reasons) == 6


def test_file_boundary_accepts_only_approved_root(tmp_path: Path) -> None:
    root = tmp_path / "workspace"
    profile = RuntimeSecurityProfile("UPSTREAM", allowed_roots=(str(root),))
    assert check_file_boundary(root / "a.txt", profile).decision is Decision.ALLOW
    assert check_file_boundary(tmp_path / "outside.txt", profile).decision is Decision.DENY


def test_network_default_deny_and_exact_allowlist() -> None:
    assert check_network_boundary("https://example.com", RuntimeSecurityProfile("UPSTREAM")).decision is Decision.DENY
    profile = RuntimeSecurityProfile("UPSTREAM", allowed_endpoints=("https://approved.example",))
    assert check_network_boundary("https://approved.example/path", profile).decision is Decision.ALLOW
    assert check_network_boundary("https://other.example", profile).decision is Decision.DENY
    assert check_network_boundary("file:///secret", profile).decision is Decision.DENY


@pytest.mark.parametrize(
    "network,credentials,tools", [(True, False, False), (False, True, False), (False, False, True)]
)
def test_reduced_safeguard_combinations_are_rejected(network: bool, credentials: bool, tools: bool) -> None:
    result = reject_unsafe_combination(True, network, credentials, tools)
    assert result.decision is Decision.DENY
    assert result.qa_status is QAStatus.REJECTED


def test_isolated_reduced_safeguard_fixture_is_allowed() -> None:
    assert reject_unsafe_combination(True, False, False, False).decision is Decision.ALLOW


def test_incident_workflow_requires_order_and_owner_reference() -> None:
    controller = IncidentStopController()
    detected = IncidentControlState("INC-001")
    isolated = controller.stop_and_isolate(detected)
    assert isolated.phase is IncidentPhase.ISOLATED
    assert isolated.runtime_isolated and isolated.tools_revoked and isolated.network_revoked
    preserved = controller.preserve_evidence(isolated, "a" * 64)
    ncr = controller.open_ncr(preserved, "NCR-001")
    capa = controller.set_capa(ncr, "CAPA-001")
    recovery = controller.request_owner_recovery(capa, "OWNER-APPROVAL-001")
    assert recovery.phase is IncidentPhase.OWNER_RECOVERY_REVIEW
    assert recovery.canonical_effect == "NONE"


def test_incident_workflow_rejects_skips() -> None:
    controller = IncidentStopController()
    state = IncidentControlState("INC-001")
    with pytest.raises(ValidationError):
        controller.open_ncr(state, "NCR")
    with pytest.raises(ValidationError):
        controller.preserve_evidence(state, "bad")
    with pytest.raises(ValidationError):
        controller.set_capa(state, "CAPA")
    with pytest.raises(ValidationError):
        controller.request_owner_recovery(state, "OWNER")


def test_upstream_signal_blocks_privilege_expansion() -> None:
    result = upstream_incident_gate((source(),), True)
    assert result.decision is Decision.QA_HOLD
    assert result.qa_status is QAStatus.QA_HOLD


def test_research_dialogue_remains_allowed_without_privilege_expansion() -> None:
    assert upstream_incident_gate((source(),), False).decision is Decision.ALLOW


def test_immutable_audit_record_cannot_be_overwritten(tmp_path: Path) -> None:
    path = tmp_path / "event.json"
    append_immutable_record(path, {"event": "STOP", "canonical_effect": "NONE"})
    with pytest.raises(ValidationError):
        append_immutable_record(path, {"event": "ERASE"})


def test_record_hash_is_deterministic() -> None:
    assert hash_record({"b": 2, "a": 1}) == hash_record({"a": 1, "b": 2})


def test_cli_policy_and_trajectory(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    policy = tmp_path / "policy.json"
    policy.write_text(
        json.dumps(
            {
                "policy_id": "POL-UPSTREAM-AGENT-INCIDENT-001",
                "status": "PROPOSED",
                "qa_status": "QA_HOLD",
                "canonical_effect": "NONE",
            }
        ),
        encoding="utf-8",
    )
    assert main(["validate-policy", "--path", str(policy)]) == 0
    trajectory = tmp_path / "trajectory.json"
    trajectory.write_text(
        json.dumps(
            {
                "budget": {
                    "max_duration_seconds": 10,
                    "max_tool_calls": 1,
                    "max_failed_retries": 0,
                    "max_subtasks": 0,
                    "max_written_files": 0,
                    "max_network_requests": 0,
                },
                "usage": {},
                "actions": [],
            }
        ),
        encoding="utf-8",
    )
    output = tmp_path / "result.json"
    assert main(["evaluate-trajectory", "--path", str(trajectory), "--output", str(output)]) == 0
    assert json.loads(output.read_text(encoding="utf-8"))["canonical_effect"] == "NONE"
    assert '"valid": true' in capsys.readouterr().out


def test_cli_rejects_invalid_policy(tmp_path: Path) -> None:
    policy = tmp_path / "policy.json"
    policy.write_text("{}", encoding="utf-8")
    assert main(["validate-policy", "--path", str(policy)]) == 2
