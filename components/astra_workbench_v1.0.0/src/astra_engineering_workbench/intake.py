"""Convert Owner input into an explicit EngineeringTask."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .enums import RiskLevel, SourceType, TaskStatus
from .errors import ValidationError
from .models import (
    AcceptanceCriterion,
    EngineeringTask,
    OwnerConstraint,
    RiskClassification,
    TaskScope,
)


def _string_tuple(value: object, name: str) -> tuple[str, ...]:
    if not isinstance(value, (list, tuple)) or not all(
        isinstance(item, str) and item for item in value
    ):
        raise ValidationError(f"{name} must be a non-empty string collection")
    return tuple(value)


def structure_task(raw: Mapping[str, Any]) -> EngineeringTask:
    required = {
        "task_id",
        "goal",
        "current_state",
        "requested_change",
        "in_scope",
        "out_of_scope",
        "constraints",
        "acceptance_criteria",
        "affected_components",
        "rollback_plan",
        "stop_condition",
        "created_at",
    }
    if missing := required - set(raw):
        raise ValidationError(f"task input missing fields: {sorted(missing)}")
    constraints = tuple(
        OwnerConstraint(f"OC-{index:03}", text, SourceType.OWNER_STATEMENT)
        for index, text in enumerate(
            _string_tuple(raw["constraints"], "constraints"), start=1
        )
    )
    criteria = tuple(
        AcceptanceCriterion(f"AC-{index:03}", text)
        for index, text in enumerate(
            _string_tuple(raw["acceptance_criteria"], "acceptance_criteria"), start=1
        )
    )
    scope = TaskScope(
        goal=str(raw["goal"]),
        current_state=str(raw["current_state"]),
        requested_change=str(raw["requested_change"]),
        in_scope=_string_tuple(raw["in_scope"], "in_scope"),
        out_of_scope=_string_tuple(raw["out_of_scope"], "out_of_scope"),
        constraints=constraints,
        assumptions=tuple(str(item) for item in raw.get("assumptions", ())),
        unresolved_questions=tuple(
            str(item) for item in raw.get("unresolved_questions", ())
        ),
        acceptance_criteria=criteria,
        blocking_conditions=tuple(
            str(item) for item in raw.get("blocking_conditions", ())
        ),
        affected_components=_string_tuple(
            raw["affected_components"], "affected_components"
        ),
        revalidation_scope=tuple(
            str(item) for item in raw.get("revalidation_scope", ())
        ),
        rollback_plan=str(raw["rollback_plan"]),
        stop_condition=str(raw["stop_condition"]),
    )
    if not all((scope.goal, scope.requested_change, scope.rollback_plan, scope.stop_condition)):
        raise ValidationError("task scope cannot contain blank controlling statements")
    return EngineeringTask(
        task_id=str(raw["task_id"]),
        scope=scope,
        risk=RiskClassification(
            RiskLevel(str(raw.get("risk_level", RiskLevel.MEDIUM.value))),
            tuple(str(item) for item in raw.get("risk_reasons", ())),
        ),
        status=TaskStatus.RECEIVED,
        created_at=str(raw["created_at"]),
    )
