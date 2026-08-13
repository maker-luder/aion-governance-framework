from __future__ import annotations

from aion_prereg_integrity import (
    AnalysisClass,
    AuditStatus,
    Deviation,
    Disposition,
    InterventionPlan,
    PlannedAnalysis,
    PlannedOutcome,
    audit_plan,
)


def base_plan(**changes: object) -> InterventionPlan:
    values: dict[str, object] = {
        "plan_id": "plan-1",
        "plan_version": "v1",
        "registered_at": 1,
        "intervention_start": 10,
        "immutable_digest": "sha256:plan-1",
        "protocol_ref": "protocol:1",
        "outcomes": (
            PlannedOutcome("outcome-primary", "primary outcome", True, "increase", "measure:primary"),
            PlannedOutcome("outcome-secondary", "secondary outcome", False, "increase", "measure:secondary"),
        ),
        "analyses": (
            PlannedAnalysis("analysis-confirmatory", "outcome-primary", AnalysisClass.CONFIRMATORY, "method:t", "estimand:primary", "rule:alpha"),
            PlannedAnalysis("analysis-exploratory", "outcome-secondary", AnalysisClass.EXPLORATORY, "method:descriptive", "estimand:secondary", "rule:describe"),
        ),
        "deviations": (),
        "report_outcome_ids": frozenset({"outcome-primary", "outcome-secondary"}),
        "report_analysis_ids": frozenset({"analysis-confirmatory", "analysis-exploratory"}),
        "exploratory_analysis_ids": frozenset({"analysis-exploratory"}),
        "all_results_reported": True,
    }
    values.update(changes)
    return InterventionPlan(**values)


def test_valid_plan_separates_confirmatory_and_exploratory() -> None:
    result = audit_plan(base_plan())
    assert result.status is AuditStatus.VALID
    assert result.disposition is Disposition.EXPLORATORY_REVIEW
    assert result.confirmatory_analysis_ids == ("analysis-confirmatory",)
    assert result.exploratory_analysis_ids == ("analysis-exploratory",)


def test_confirmatory_only_plan_is_confirmatory_review() -> None:
    analysis = PlannedAnalysis("analysis-confirmatory", "outcome-primary", AnalysisClass.CONFIRMATORY, "method:t", "estimand:primary", "rule:alpha")
    result = audit_plan(base_plan(analyses=(analysis,), report_analysis_ids=frozenset({"analysis-confirmatory"}), exploratory_analysis_ids=frozenset()))
    assert result.status is AuditStatus.VALID
    assert result.disposition is Disposition.CONFIRMATORY_REVIEW


def test_registration_after_intervention_start_is_invalid() -> None:
    result = audit_plan(base_plan(registered_at=11))
    assert result.status is AuditStatus.INVALID
    assert result.disposition is Disposition.HOLD
    assert result.reason == "REGISTRATION_AFTER_INTERVENTION_START"


def test_missing_immutable_digest_holds() -> None:
    result = audit_plan(base_plan(immutable_digest=None))
    assert result.status is AuditStatus.INDETERMINATE
    assert result.reason == "MISSING_PLAN_IMMUTABILITY_OR_PROTOCOL"


def test_missing_primary_outcome_is_invalid() -> None:
    outcomes = (
        PlannedOutcome("outcome-secondary", "secondary", False, "increase", "measure:secondary"),
    )
    result = audit_plan(base_plan(outcomes=outcomes))
    assert result.status is AuditStatus.INVALID
    assert result.reason == "PRIMARY_OUTCOME_CARDINALITY_INVALID"


def test_analysis_outcome_switching_to_unknown_outcome_is_invalid() -> None:
    analysis = PlannedAnalysis("analysis-confirmatory", "outcome-switched", AnalysisClass.CONFIRMATORY, "method:t", "estimand:primary", "rule:alpha")
    result = audit_plan(base_plan(analyses=(analysis,), report_analysis_ids=frozenset({"analysis-confirmatory"}), exploratory_analysis_ids=frozenset()))
    assert result.status is AuditStatus.INVALID
    assert result.reason == "ANALYSIS_REFERENCES_UNKNOWN_OUTCOME"


def test_exploratory_label_mismatch_is_invalid() -> None:
    result = audit_plan(base_plan(exploratory_analysis_ids=frozenset()))
    assert result.status is AuditStatus.INVALID
    assert result.reason == "EXPLORATORY_LABEL_MISMATCH"


def test_undisclosed_deviation_holds() -> None:
    deviation = Deviation("dev-1", "sample shortfall", None, "not recorded", "not recorded")
    result = audit_plan(base_plan(deviations=(deviation,)))
    assert result.status is AuditStatus.INDETERMINATE
    assert result.disposition is Disposition.HOLD
    assert result.reason == "DEVIATION_DISCLOSURE_INCOMPLETE"
    assert result.undisclosed_deviation_ids == ("dev-1",)


def test_disclosed_deviation_can_be_reviewed() -> None:
    deviation = Deviation("dev-1", "sample shortfall", 20, "recruitment ended", "reduced precision")
    result = audit_plan(base_plan(deviations=(deviation,)))
    assert result.status is AuditStatus.VALID
    assert result.reason == "VALID_WITH_EXPLORATORY_ANALYSES_SEPARATED"


def test_unreported_outcome_holds_and_is_named() -> None:
    result = audit_plan(base_plan(report_outcome_ids=frozenset({"outcome-primary"})))
    assert result.status is AuditStatus.INDETERMINATE
    assert result.reason == "ALL_PREREGISTERED_RESULTS_NOT_REPORTED"
    assert result.unreported_outcome_ids == ("outcome-secondary",)


def test_unreported_analysis_holds() -> None:
    result = audit_plan(base_plan(report_analysis_ids=frozenset({"analysis-confirmatory"})))
    assert result.status is AuditStatus.INDETERMINATE
    assert result.unreported_analysis_ids == ("analysis-exploratory",)


def test_all_results_flag_is_required() -> None:
    result = audit_plan(base_plan(all_results_reported=False))
    assert result.status is AuditStatus.INDETERMINATE
    assert result.reason == "ALL_PREREGISTERED_RESULTS_NOT_REPORTED"


def test_missing_measure_or_direction_is_indeterminate() -> None:
    outcome = PlannedOutcome("outcome-primary", "primary", True, None, "measure:primary")
    result = audit_plan(base_plan(outcomes=(outcome,)))
    assert result.status is AuditStatus.INDETERMINATE
    assert result.reason == "OUTCOME_MEASURE_OR_DIRECTION_MISSING"


def test_missing_analysis_specification_holds() -> None:
    analysis = PlannedAnalysis("analysis-confirmatory", "outcome-primary", AnalysisClass.CONFIRMATORY, None, "estimand:primary", "rule:alpha")
    result = audit_plan(base_plan(analyses=(analysis,), report_analysis_ids=frozenset({"analysis-confirmatory"}), exploratory_analysis_ids=frozenset()))
    assert result.status is AuditStatus.INDETERMINATE
    assert result.reason == "ANALYSIS_SPECIFICATION_INCOMPLETE"


def test_decision_boundaries_never_execute_intervention() -> None:
    for candidate in (base_plan(), base_plan(all_results_reported=False), base_plan(registered_at=11)):
        result = audit_plan(candidate)
        assert result.scientific_conclusion == "NOT_ESTABLISHED"
        assert result.canonical_effect == "NONE"
        assert result.deployment is False
        assert result.intervention_executed is False
        assert result.subjectivity_conclusion == "NOT_ESTABLISHED"
        assert result.identity_continuity_conclusion == "NOT_ESTABLISHED"


def test_serialization_uses_enum_values() -> None:
    payload = audit_plan(base_plan()).as_dict()
    assert payload["status"] == "VALID"
    assert payload["disposition"] == "EXPLORATORY_REVIEW"
