"""Scope-lock validation helpers."""

from __future__ import annotations

from .errors import ValidationError
from .models import EngineeringTask


def validate_scope_lock(task: EngineeringTask) -> EngineeringTask:
    scope = task.scope
    overlap = set(scope.in_scope) & set(scope.out_of_scope)
    if overlap:
        raise ValidationError(f"in-scope/out-of-scope overlap: {sorted(overlap)}")
    if scope.unresolved_questions:
        raise ValidationError("unresolved Owner questions require BLOCKED status")
    if not scope.acceptance_criteria or not scope.stop_condition:
        raise ValidationError("scope lock requires acceptance and stop conditions")
    return task
