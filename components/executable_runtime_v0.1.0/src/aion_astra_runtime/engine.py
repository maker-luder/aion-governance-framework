"""Executable AION/Astra candidate agent loop."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from aion_governance_kernel.pipeline import run_pipeline
from astra_engineering_workbench.approvals import create_approval_request, grant_approval
from astra_engineering_workbench.audit import AppendOnlyAudit
from astra_engineering_workbench.enums import ApprovalDecision, KernelDecision, PermissionLevel, RiskLevel
from astra_engineering_workbench.governance_adapter import GovernanceKernelAdapter
from astra_engineering_workbench.workspace import WorkspaceController, create_candidate_workspace

from .errors import PlannerFailure, PolicyDenied, RuntimeCandidateError
from .models import Observation, RunResult, RunStatus, TaskSpec
from .planner import DeterministicInventoryPlanner, Planner
from .policy import validate_task_paths
from .tools import RuntimeTools


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class AstraRuntime:
    def __init__(self, planner: Planner | None = None) -> None:
        self.planner = planner or DeterministicInventoryPlanner()

    def run(self, task: TaskSpec, *, baseline_root: Path, sessions_root: Path, kill_switch: Path | None = None) -> RunResult:
        validate_task_paths(task)
        baseline = baseline_root.resolve(strict=True)
        sessions = sessions_root.resolve(strict=True)
        workspace = create_candidate_workspace(task_id=task.task_id, baseline_root=baseline, sessions_root=sessions, created_at=_now())
        audit_path = Path(workspace.output_root) / "runtime_audit.jsonl"
        audit = AppendOnlyAudit(audit_path)
        governance_db = str(Path(workspace.output_root) / "governance_audit.sqlite3")
        governance = GovernanceKernelAdapter(run_pipeline, governance_db)
        evaluation = governance.evaluate(task_id=task.task_id, operation="MODIFY_PROJECT", target=task.output_path, approved=True)
        if evaluation.decision is not KernelDecision.ALLOW:
            return self._hold(task, workspace.candidate_root, workspace.output_root, audit, 0, f"governance: {evaluation.decision.value}")

        requested_at = datetime.now(timezone.utc)
        expires_at = requested_at + timedelta(hours=2)
        request = create_approval_request(
            approval_request_id=f"AR-{task.task_id}",
            task_id=task.task_id,
            operation_type=PermissionLevel.CANDIDATE_WRITE,
            reason=task.objective,
            affected_paths=(task.output_path,),
            proposed_commands=(),
            expected_effect="create one candidate derivative",
            risk_level=RiskLevel.LOW,
            data_exposure="LOCAL_CANDIDATE_ONLY",
            rollback_plan="discard isolated candidate workspace",
            requested_at=requested_at.isoformat(),
            expires_at=expires_at.isoformat(),
        )
        grant = grant_approval(
            request,
            grant_id=f"AG-{task.task_id}",
            decision=ApprovalDecision.APPROVED,
            approved_by=task.approved_by,
            approved_at=requested_at.isoformat(),
            conditions=("candidate-only", "canonical-effect-none"),
        )
        controller = WorkspaceController(workspace, request, grant, requested_at.isoformat())
        tools = RuntimeTools(controller, task)
        observations: list[Observation] = []
        audit.append(occurred_at=_now(), task_id=task.task_id, action="runtime.started", details={"profile": task.profile, "canonical_effect": "NONE", "network_policy": task.network_policy.value})

        try:
            for step in range(1, task.max_steps + 1):
                if kill_switch is not None and kill_switch.exists():
                    return self._hold(task, workspace.candidate_root, workspace.output_root, audit, step - 1, "kill switch active", controller.baseline_unchanged())
                action = self.planner.next_action(task, tuple(observations))
                audit.append(occurred_at=_now(), task_id=task.task_id, action="planner.decision", details={"step": step, "tool": action.tool, "argument_keys": sorted(action.arguments)})
                observation = tools.execute(action)
                observations.append(observation)
                audit.append(occurred_at=_now(), task_id=task.task_id, action="tool.completed", details={"step": step, "tool": action.tool, "status": observation.status, **tools.audit_payload(observation)})
                if action.tool == "complete":
                    digest = next((str(item.payload["sha256"]) for item in reversed(observations) if item.tool == "sha256_candidate"), None)
                    baseline_unchanged = controller.baseline_unchanged()
                    status = RunStatus.PASS_PENDING_OWNER_REVIEW if digest and baseline_unchanged else RunStatus.HOLD
                    result = RunResult(task.task_id, status, step, workspace.candidate_root, workspace.output_root, task.output_path, digest, str(audit_path), audit.verify(), baseline_unchanged, failure_reason=None if status is RunStatus.PASS_PENDING_OWNER_REVIEW else "acceptance evidence incomplete")
                    self._write_result(result)
                    return result
        except (RuntimeCandidateError, OSError, UnicodeError, KeyError, ValueError) as exc:
            return self._hold(task, workspace.candidate_root, workspace.output_root, audit, len(observations), f"{type(exc).__name__}: {exc}", controller.baseline_unchanged())
        return self._hold(task, workspace.candidate_root, workspace.output_root, audit, task.max_steps, "maximum step budget exhausted", controller.baseline_unchanged())

    def _hold(self, task: TaskSpec, candidate_root: str, output_root: str, audit: AppendOnlyAudit, steps: int, reason: str, baseline_unchanged: bool = True) -> RunResult:
        audit.append(occurred_at=_now(), task_id=task.task_id, action="runtime.hold", details={"reason": reason, "steps": steps})
        result = RunResult(task.task_id, RunStatus.HOLD, steps, candidate_root, output_root, task.output_path, None, str(audit.path), audit.verify(), baseline_unchanged, failure_reason=reason)
        self._write_result(result)
        return result

    @staticmethod
    def _write_result(result: RunResult) -> None:
        path = Path(result.output_root) / "RUN_RESULT.json"
        path.write_text(json.dumps(result.to_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

