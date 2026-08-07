from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from astra_engineering_workbench.approvals import (
    create_approval_request,
    grant_approval,
    validate_grant,
)
from astra_engineering_workbench.audit import AppendOnlyAudit
from astra_engineering_workbench.enums import (
    ApprovalDecision,
    PermissionLevel,
    RiskLevel,
    TaskStatus,
)
from astra_engineering_workbench.errors import (
    ApprovalError,
    StateTransitionError,
    ValidationError,
)
from astra_engineering_workbench.intake import structure_task
from astra_engineering_workbench.scope import validate_scope_lock
from astra_engineering_workbench.state_machine import transition_task


def raw_task() -> dict[str, object]:
    return {
        "task_id": "TASK-001",
        "goal": "candidate",
        "current_state": "baseline",
        "requested_change": "patch",
        "in_scope": ["PROJECT_ALPHA"],
        "out_of_scope": ["deployment"],
        "constraints": ["candidate only"],
        "acceptance_criteria": ["tests pass"],
        "affected_components": ["workbench"],
        "rollback_plan": "snapshot",
        "stop_condition": "owner review",
        "created_at": "2026-07-30T00:00:00+00:00",
    }


def request():
    return create_approval_request(
        approval_request_id="REQ-001",
        task_id="TASK-001",
        operation_type=PermissionLevel.CANDIDATE_WRITE,
        reason="write candidate",
        affected_paths=("sample.txt",),
        proposed_commands=(),
        expected_effect="candidate delta",
        risk_level=RiskLevel.MEDIUM,
        data_exposure="NONE",
        rollback_plan="snapshot",
        requested_at="2026-07-30T00:00:00+00:00",
        expires_at="2026-07-31T00:00:00+00:00",
    )


def grant():
    return grant_approval(
        request(),
        grant_id="GRANT-001",
        decision=ApprovalDecision.APPROVED,
        approved_by="OWNER_A",
        approved_at="2026-07-30T00:01:00+00:00",
    )


def test_TASK_REQUIRES_SCOPE_001() -> None:
    raw = raw_task()
    del raw["goal"]
    with pytest.raises(ValidationError):
        structure_task(raw)


def test_scope_lock_passes() -> None:
    assert validate_scope_lock(structure_task(raw_task())).task_id == "TASK-001"


def test_scope_overlap_rejected() -> None:
    raw = raw_task()
    raw["out_of_scope"] = ["PROJECT_ALPHA"]
    with pytest.raises(ValidationError):
        validate_scope_lock(structure_task(raw))


def test_STALE_APPROVAL_REJECTED_001() -> None:
    with pytest.raises(ApprovalError):
        validate_grant(
            request(),
            grant(),
            task_id="TASK-001",
            required_permission=PermissionLevel.CANDIDATE_WRITE,
            now="2026-08-01T00:00:00+00:00",
        )


def test_APPROVAL_FOR_OTHER_TASK_REJECTED_001() -> None:
    with pytest.raises(ApprovalError):
        validate_grant(
            request(),
            grant(),
            task_id="TASK-OTHER",
            required_permission=PermissionLevel.CANDIDATE_WRITE,
            now="2026-07-30T01:00:00+00:00",
        )


def test_nonapproval_cannot_create_grant() -> None:
    with pytest.raises(ApprovalError):
        grant_approval(
            request(),
            grant_id="X",
            decision=ApprovalDecision.REJECTED,
            approved_by="OWNER_A",
            approved_at="2026-07-30T00:01:00+00:00",
        )


def test_ILLEGAL_STATE_TRANSITION_REJECTED_001(tmp_path: Path) -> None:
    audit = AppendOnlyAudit(tmp_path / "audit.jsonl")
    with pytest.raises(StateTransitionError):
        transition_task(
            structure_task(raw_task()),
            TaskStatus.IMPLEMENTING_CANDIDATE,
            occurred_at="2026-07-30T00:00:01+00:00",
            audit=audit,
        )


def test_BLOCKED_TASK_CANNOT_SELF_RESUME_001(tmp_path: Path) -> None:
    audit = AppendOnlyAudit(tmp_path / "audit.jsonl")
    task = replace(structure_task(raw_task()), status=TaskStatus.BLOCKED)
    with pytest.raises(StateTransitionError):
        transition_task(
            task,
            TaskStatus.IMPLEMENTING_CANDIDATE,
            occurred_at="2026-07-30T00:00:01+00:00",
            audit=audit,
        )


def test_VALIDATION_PASS_NOT_CANONICAL_001(tmp_path: Path) -> None:
    audit = AppendOnlyAudit(tmp_path / "audit.jsonl")
    task = replace(structure_task(raw_task()), status=TaskStatus.VALIDATING)
    packaged = transition_task(
        task,
        TaskStatus.PACKAGING,
        occurred_at="2026-07-30T00:00:01+00:00",
        audit=audit,
    )
    assert packaged.status is TaskStatus.PACKAGING


def test_PACKAGE_NOT_DEPLOYMENT_001(tmp_path: Path) -> None:
    audit = AppendOnlyAudit(tmp_path / "audit.jsonl")
    task = replace(structure_task(raw_task()), status=TaskStatus.PACKAGING)
    result = transition_task(
        task,
        TaskStatus.PASS_PENDING_OWNER_REVIEW,
        occurred_at="2026-07-30T00:00:01+00:00",
        audit=audit,
    )
    assert result.status.value == "PASS_PENDING_OWNER_REVIEW"


def test_STOP_CONDITION_CLOSES_TASK_001(tmp_path: Path) -> None:
    audit = AppendOnlyAudit(tmp_path / "audit.jsonl")
    task = replace(structure_task(raw_task()), status=TaskStatus.PASS_PENDING_OWNER_REVIEW)
    assert transition_task(
        task,
        TaskStatus.CLOSED,
        occurred_at="2026-07-30T00:00:01+00:00",
        audit=audit,
    ).status is TaskStatus.CLOSED


def test_AUDIT_APPEND_ONLY_001(tmp_path: Path) -> None:
    audit = AppendOnlyAudit(tmp_path / "audit.jsonl")
    audit.append(occurred_at="t1", task_id="T", action="a", details={})
    audit.append(occurred_at="t2", task_id="T", action="b", details={})
    assert audit.verify()
    text = audit.path.read_text(encoding="utf-8").replace('"action":"a"', '"action":"x"')
    audit.path.write_text(text, encoding="utf-8")
    assert not audit.verify()


def test_invalid_approval_timestamps() -> None:
    with pytest.raises(ApprovalError):
        create_approval_request(
            approval_request_id="R", task_id="T",
            operation_type=PermissionLevel.CANDIDATE_WRITE,
            reason="x", affected_paths=(), proposed_commands=(),
            expected_effect="x", risk_level=RiskLevel.LOW,
            data_exposure="NONE", rollback_plan="x",
            requested_at="bad", expires_at="also-bad",
        )


def test_expired_request_cannot_be_granted() -> None:
    with pytest.raises(ApprovalError):
        grant_approval(
            request(), grant_id="G", decision=ApprovalDecision.APPROVED,
            approved_by="OWNER_A", approved_at="2026-08-01T00:00:00+00:00",
        )


def test_scope_unresolved_and_missing_acceptance() -> None:
    raw = raw_task()
    raw["unresolved_questions"] = ["owner decision"]
    with pytest.raises(ValidationError):
        validate_scope_lock(structure_task(raw))
    raw = raw_task()
    raw["acceptance_criteria"] = []
    with pytest.raises(ValidationError):
        validate_scope_lock(structure_task(raw))


def test_audit_corrupt_json_rejected(tmp_path: Path) -> None:
    from astra_engineering_workbench.errors import AuditError

    path = tmp_path / "a.jsonl"
    path.write_text("{bad", encoding="utf-8")
    with pytest.raises(AuditError):
        AppendOnlyAudit(path).events()
