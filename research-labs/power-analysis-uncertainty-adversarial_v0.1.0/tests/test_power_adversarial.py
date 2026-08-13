import math

from aion_power_analysis import PowerPlan

from aion_power_analysis_adversarial import AssumptionSnapshot, audit_assumption_lock, audit_decision_serialization, audit_power_plan


def plan(**changes) -> PowerPlan:
    values = dict(
        plan_id="power:1",
        standardized_effect_bound=0.5,
        standard_deviation=1.0,
        alpha=0.05,
        target_power=0.8,
        planned_sample_size=100,
        two_sided=True,
        preregistration_ref="prereg:1",
        assumption_basis="prior bounded estimate",
    )
    values.update(changes)
    return PowerPlan(**values)


def assert_no_effect(audit) -> None:
    assert audit.achieved_power is None
    assert audit.effect_observed is False
    assert audit.scientific_conclusion == "NOT_ESTABLISHED"
    assert audit.canonical_effect == "NONE"
    assert audit.deployment is False
    assert audit.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert audit.identity_continuity_conclusion == "NOT_ESTABLISHED"


def test_valid_power_plan_is_planning_review_only() -> None:
    audit = audit_power_plan(plan())
    assert audit.status == "ADEQUATE"
    assert audit.disposition == "PLANNING_REVIEW"
    assert audit.sensitivity_valid is True
    assert_no_effect(audit)


def test_plan_id_is_required() -> None:
    audit = audit_power_plan(plan(plan_id=""))
    assert audit.status == "INVALID"
    assert audit.reason == "PLAN_ID_MISSING"
    assert_no_effect(audit)


def test_sample_size_type_is_checked() -> None:
    audit = audit_power_plan(plan(planned_sample_size=10.5))
    assert audit.status == "INVALID"
    assert audit.reason == "SAMPLE_SIZE_TYPE_INVALID"
    assert_no_effect(audit)


def test_non_finite_input_is_invalid() -> None:
    audit = audit_power_plan(plan(alpha=math.nan))
    assert audit.status == "INVALID"
    assert audit.reason == "NON_FINITE_PLANNING_INPUT"
    assert_no_effect(audit)


def test_empty_preregistration_reference_is_indeterminate() -> None:
    audit = audit_power_plan(plan(preregistration_ref=""))
    assert audit.status == "UNKNOWN"
    assert audit.disposition == "INDETERMINATE"
    assert audit.reason == "PREREGISTRATION_REFERENCE_EMPTY"
    assert_no_effect(audit)


def test_empty_assumption_basis_is_held() -> None:
    audit = audit_power_plan(plan(assumption_basis=" "))
    assert audit.status == "UNKNOWN"
    assert audit.disposition == "HOLD"
    assert audit.reason == "ASSUMPTION_BASIS_EMPTY"
    assert_no_effect(audit)


def test_missing_planning_input_is_unknown() -> None:
    audit = audit_power_plan(plan(standardized_effect_bound=None))
    assert audit.status == "UNKNOWN"
    assert audit.reason == "MISSING_POWER_PLANNING_INPUT"
    assert_no_effect(audit)


def test_non_positive_input_is_invalid() -> None:
    audit = audit_power_plan(plan(standardized_effect_bound=0.0))
    assert audit.status == "INVALID"
    assert audit.reason == "NON_POSITIVE_SAMPLE_OR_EFFECT_INPUT"
    assert_no_effect(audit)


def test_probability_range_is_invalid() -> None:
    audit = audit_power_plan(plan(alpha=1.0))
    assert audit.status == "INVALID"
    assert audit.reason == "ALPHA_OR_TARGET_POWER_OUT_OF_RANGE"
    assert_no_effect(audit)


def test_unregistered_plan_is_unknown_indeterminate() -> None:
    audit = audit_power_plan(plan(preregistration_ref=None))
    assert audit.status == "UNKNOWN"
    assert audit.disposition == "INDETERMINATE"
    assert audit.reason == "POWER_PLAN_NOT_PREREGISTERED"
    assert_no_effect(audit)


def test_underpowered_plan_remains_indeterminate() -> None:
    audit = audit_power_plan(plan(planned_sample_size=1))
    assert audit.status == "UNDERPOWERED"
    assert audit.disposition == "INDETERMINATE"
    assert audit.required_sample_size is not None
    assert_no_effect(audit)


def test_sensitivity_is_monotone_and_valid() -> None:
    audit = audit_power_plan(plan())
    assert audit.sensitivity_valid is True
    assert audit.required_sample_size is not None
    assert_no_effect(audit)


def test_one_sided_plan_is_supported() -> None:
    audit = audit_power_plan(plan(two_sided=False))
    assert audit.status == "ADEQUATE"
    assert audit.sensitivity_valid is True
    assert_no_effect(audit)


def test_decision_serialization_keeps_achieved_power_unset() -> None:
    audit = audit_decision_serialization(plan())
    assert audit.status == "ADEQUATE"
    assert audit.achieved_power is None
    assert_no_effect(audit)


def test_assumption_lock_unchanged_is_review_only() -> None:
    before = AssumptionSnapshot("power:1", 0.5, 1.0, 0.05, 0.8, True)
    audit = audit_assumption_lock(before, before)
    assert audit.status == "ADEQUATE"
    assert audit.reason == "ASSUMPTION_LOCK_UNCHANGED"
    assert_no_effect(audit)


def test_assumption_change_before_outcome_requires_review() -> None:
    before = AssumptionSnapshot("power:1", 0.5, 1.0, 0.05, 0.8, True)
    after = AssumptionSnapshot("power:1", 0.4, 1.0, 0.05, 0.8, True)
    audit = audit_assumption_lock(before, after)
    assert audit.status == "UNKNOWN"
    assert audit.disposition == "INDETERMINATE"
    assert audit.reason == "ASSUMPTION_CHANGE_REQUIRES_REVIEW"
    assert_no_effect(audit)


def test_assumption_change_after_observed_effect_is_invalid() -> None:
    before = AssumptionSnapshot("power:1", 0.5, 1.0, 0.05, 0.8, True)
    after = AssumptionSnapshot("power:1", 0.4, 1.0, 0.05, 0.8, True, observed_effect=True)
    audit = audit_assumption_lock(before, after)
    assert audit.status == "INVALID"
    assert audit.reason == "ASSUMPTION_MUTATION_AFTER_OUTCOME"
    assert_no_effect(audit)


def test_assumption_plan_ids_must_match() -> None:
    before = AssumptionSnapshot("power:1", 0.5, 1.0, 0.05, 0.8, True)
    after = AssumptionSnapshot("power:2", 0.5, 1.0, 0.05, 0.8, True)
    audit = audit_assumption_lock(before, after)
    assert audit.status == "INVALID"
    assert audit.reason == "ASSUMPTION_PLAN_ID_MISMATCH"
    assert_no_effect(audit)


def test_assumption_nan_is_invalid() -> None:
    before = AssumptionSnapshot("power:1", 0.5, 1.0, 0.05, 0.8, True)
    after = AssumptionSnapshot("power:1", math.nan, 1.0, 0.05, 0.8, True)
    audit = audit_assumption_lock(before, after)
    assert audit.status == "INVALID"
    assert audit.reason == "ASSUMPTION_NON_FINITE"
    assert_no_effect(audit)


def test_missing_sample_size_remains_unknown() -> None:
    audit = audit_power_plan(plan(planned_sample_size=None))
    assert audit.status == "UNKNOWN"
    assert audit.reason == "MISSING_POWER_PLANNING_INPUT"
    assert_no_effect(audit)
