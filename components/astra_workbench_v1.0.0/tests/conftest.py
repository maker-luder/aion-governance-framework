from __future__ import annotations

from pathlib import Path

import pytest

from astra_engineering_workbench.approvals import (
    create_approval_request,
    grant_approval,
)
from astra_engineering_workbench.enums import (
    ApprovalDecision,
    PermissionLevel,
    RiskLevel,
)
from astra_engineering_workbench.workspace import (
    WorkspaceController,
    create_candidate_workspace,
)


@pytest.fixture
def controller(tmp_path: Path) -> WorkspaceController:
    baseline = tmp_path / "baseline"
    baseline.mkdir()
    (baseline / "sample.txt").write_text("alpha\nbeta\n", encoding="utf-8")
    sessions = tmp_path / "sessions"
    sessions.mkdir()
    workspace = create_candidate_workspace(
        task_id="TASK-001",
        baseline_root=baseline,
        sessions_root=sessions,
        created_at="2026-07-30T00:00:00+00:00",
    )
    request = create_approval_request(
        approval_request_id="REQ-001",
        task_id="TASK-001",
        operation_type=PermissionLevel.CANDIDATE_WRITE,
        reason="candidate test",
        affected_paths=("sample.txt",),
        proposed_commands=(),
        expected_effect="candidate only",
        risk_level=RiskLevel.LOW,
        data_exposure="NONE",
        rollback_plan="snapshot",
        requested_at="2026-07-30T00:00:00+00:00",
        expires_at="2026-07-31T00:00:00+00:00",
    )
    grant = grant_approval(
        request,
        grant_id="GRANT-001",
        decision=ApprovalDecision.APPROVED,
        approved_by="OWNER_A",
        approved_at="2026-07-30T00:01:00+00:00",
    )
    return WorkspaceController(
        workspace, request, grant, "2026-07-30T01:00:00+00:00"
    )
