from __future__ import annotations

import pytest

from aion_power_analysis import (
    Disposition,
    PlanningStatus,
    PowerPlan,
    evaluate_plan,
    required_sample_size,
)


def plan(**changes: object) -> PowerPlan:
    values: dict[str, object] = {
        "plan_id": "power-1",
        "standardized_effect_bound": 0.30,
        "standard_deviation": 1.0,
        "alpha": 0.05,
        "target_power": 0.80,
        "planned_sample_size": 200,
        "two_sided": True,
        "preregistration_ref": "prereg:power-1",
        "assumption_basis": "bounded pilot estimate, deliberately conservative",
    }
    values.update(changes)
    return PowerPlan(**values)


def test_required_sample_size_is_deterministic_positive_integer() -> None:
    result = required_sample_size(0.30, 1.0, 0.05, 0.80)
    assert result == required_sample_size(0.30, 1.0, 0.05, 0.80)
    assert isinstance(result, int)
    assert result > 0


def test_adequate_preregistered_plan_is_planning_review_only() -> None:
    result = evaluate_plan(plan())
    assert result.planning_status is PlanningStatus.ADEQUATE
    assert result.disposition is Disposition.PLANNING_REVIEW
    assert result.required_sample_size is not None
    assert result.planned_sample_size >= result.required_sample_size
    assert result.achieved_power is None
    assert result.scientific_conclusion == "NOT_ESTABLISHED"


def test_underpowered_plan_is_indeterminate() -> None:
    result = evaluate_plan(plan(planned_sample_size=10))
    assert result.planning_status is PlanningStatus.UNDERPOWERED
    assert result.disposition is Disposition.INDETERMINATE
    assert result.reason == "PLANNED_SAMPLE_BELOW_ASSUMPTION_DEPENDENT_REQUIREMENT"


def test_missing_preregistration_is_indeterminate_not_adequate() -> None:
    result = evaluate_plan(plan(preregistration_ref=None))
    assert result.planning_status is PlanningStatus.UNKNOWN
    assert result.disposition is Disposition.INDETERMINATE
    assert result.reason == "POWER_PLAN_NOT_PREREGISTERED"


def test_missing_effect_size_basis_holds() -> None:
    result = evaluate_plan(plan(assumption_basis=None))
    assert result.planning_status is PlanningStatus.UNKNOWN
    assert result.disposition is Disposition.HOLD
    assert result.reason == "MISSING_EFFECT_SIZE_ASSUMPTION_BASIS"


def test_missing_input_is_unknown_and_holds() -> None:
    result = evaluate_plan(plan(standardized_effect_bound=None))
    assert result.planning_status is PlanningStatus.UNKNOWN
    assert result.disposition is Disposition.HOLD
    assert result.reason == "MISSING_POWER_PLANNING_INPUT"


def test_invalid_probability_is_invalid_and_holds() -> None:
    result = evaluate_plan(plan(alpha=1.0))
    assert result.planning_status is PlanningStatus.INVALID
    assert result.disposition is Disposition.HOLD
    assert result.reason == "ALPHA_OR_TARGET_POWER_OUT_OF_RANGE"


def test_non_positive_sample_or_effect_is_invalid() -> None:
    result = evaluate_plan(plan(planned_sample_size=0))
    assert result.planning_status is PlanningStatus.INVALID
    assert result.reason == "NON_POSITIVE_SAMPLE_OR_EFFECT_INPUT"


def test_sensitivity_requires_more_samples_for_smaller_effect() -> None:
    result = evaluate_plan(plan())
    values = dict(result.sensitivity_required_sample_sizes)
    assert values[0.15] > values[0.30] > values[0.45]


def test_one_sided_plan_is_supported_as_explicit_assumption() -> None:
    result = evaluate_plan(plan(two_sided=False))
    assert result.required_sample_size is not None
    assert result.planning_status is PlanningStatus.ADEQUATE


def test_invalid_formula_inputs_raise() -> None:
    with pytest.raises(ValueError):
        required_sample_size(0.0, 1.0, 0.05, 0.80)
    with pytest.raises(ValueError):
        required_sample_size(0.30, 1.0, 0.0, 0.80)


def test_serialization_and_boundaries_are_non_promoting() -> None:
    payload = evaluate_plan(plan()).as_dict()
    assert payload["planning_status"] == "ADEQUATE"
    assert payload["disposition"] == "PLANNING_REVIEW"
    assert payload["achieved_power"] is None
    assert payload["canonical_effect"] == "NONE"
    assert payload["deployment"] is False
    assert payload["subjectivity_conclusion"] == "NOT_ESTABLISHED"
    assert payload["identity_continuity_conclusion"] == "NOT_ESTABLISHED"
