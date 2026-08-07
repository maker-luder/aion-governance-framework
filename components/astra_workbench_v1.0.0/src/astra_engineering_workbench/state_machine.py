"""Fail-closed task state machine with mandatory audit."""

from __future__ import annotations

from dataclasses import replace

from .audit import AppendOnlyAudit
from .enums import TaskStatus
from .errors import StateTransitionError
from .models import EngineeringTask


_TRANSITIONS: dict[TaskStatus, set[TaskStatus]] = {
    TaskStatus.RECEIVED: {
        TaskStatus.READ_ONLY_ANALYSIS,
        TaskStatus.REJECTED,
        TaskStatus.CANCELLED,
    },
    TaskStatus.READ_ONLY_ANALYSIS: {TaskStatus.SCOPE_PROPOSED, TaskStatus.BLOCKED},
    TaskStatus.SCOPE_PROPOSED: {TaskStatus.AWAITING_OWNER_APPROVAL, TaskStatus.BLOCKED},
    TaskStatus.AWAITING_OWNER_APPROVAL: {
        TaskStatus.APPROVED,
        TaskStatus.REJECTED,
        TaskStatus.CANCELLED,
        TaskStatus.BLOCKED,
    },
    TaskStatus.APPROVED: {TaskStatus.WORKSPACE_PREPARING, TaskStatus.CANCELLED},
    TaskStatus.WORKSPACE_PREPARING: {TaskStatus.PLAN_READY, TaskStatus.HOLD},
    TaskStatus.PLAN_READY: {TaskStatus.IMPLEMENTING_CANDIDATE, TaskStatus.BLOCKED},
    TaskStatus.IMPLEMENTING_CANDIDATE: {TaskStatus.VALIDATING, TaskStatus.HOLD},
    TaskStatus.VALIDATING: {
        TaskStatus.PACKAGING,
        TaskStatus.BLOCKED,
        TaskStatus.HOLD,
    },
    TaskStatus.BLOCKED: {TaskStatus.REVIEW_PACKET_READY, TaskStatus.HOLD},
    TaskStatus.REVIEW_PACKET_READY: {TaskStatus.CLOSED, TaskStatus.HOLD},
    TaskStatus.PACKAGING: {TaskStatus.PASS_PENDING_OWNER_REVIEW, TaskStatus.HOLD},
    TaskStatus.PASS_PENDING_OWNER_REVIEW: {TaskStatus.CLOSED},
    TaskStatus.HOLD: {TaskStatus.CLOSED},
    TaskStatus.REJECTED: {TaskStatus.CLOSED},
    TaskStatus.CANCELLED: {TaskStatus.CLOSED},
    TaskStatus.CLOSED: set(),
}


def transition_task(
    task: EngineeringTask,
    requested: TaskStatus,
    *,
    occurred_at: str,
    audit: AppendOnlyAudit,
) -> EngineeringTask:
    if requested not in _TRANSITIONS[task.status]:
        raise StateTransitionError(
            f"illegal task transition: {task.status.value}->{requested.value}"
        )
    audit.append(
        occurred_at=occurred_at,
        task_id=task.task_id,
        action="task.transition",
        details={"from": task.status.value, "to": requested.value},
    )
    return replace(task, status=requested)
