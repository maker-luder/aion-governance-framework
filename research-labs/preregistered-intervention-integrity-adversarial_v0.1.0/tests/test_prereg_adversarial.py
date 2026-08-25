
from aion_prereg_integrity import AnalysisClass, Deviation, InterventionPlan, PlannedAnalysis, PlannedOutcome

from aion_prereg_integrity_adversarial import OutcomeLockSnapshot, audit_intervention_boundary, audit_outcome_lock, audit_preregistration


def base_plan(**changes) -> InterventionPlan:
    values = dict(
        plan_id="plan:1",
        plan_version="v1",
        registered_at=1,
        intervention_start=2,
        immutable_digest="sha256:plan1",
        protocol_ref="protocol:1",
        outcomes=(PlannedOutcome("outcome:primary", "Primary outcome", True, "UP", "measure:1"),),
        analyses=(PlannedAnalysis("analysis:confirm", "outcome:primary", AnalysisClass.CONFIRMATORY, "method:1", "estimand:1", "rule:1"),),
        deviations=(),
        report_outcome_ids=frozenset({"outcome:primary"}),
        report_analysis_ids=frozenset({"analysis:confirm"}),
        exploratory_analysis_ids=frozenset(),
        all_results_reported=True,
    )
    values.update(changes)
    return InterventionPlan(**values)


def assert_no_effect(audit) -> None:
    assert audit.scientific_conclusion == "NOT_ESTABLISHED"
    assert audit.canonical_effect == "NONE"
    assert audit.deployment is False
    assert audit.intervention_executed is False
    assert audit.observed_outcomes is False
    assert audit.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert audit.identity_continuity_conclusion == "NOT_ESTABLISHED"


def test_valid_confirmatory_plan_is_review_only() -> None:
    audit = audit_preregistration(base_plan())
    assert audit.status == "VALID"
    assert audit.disposition == "CONFIRMATORY_REVIEW"
    assert audit.reason == "VALID_CONFIRMATORY_PLAN_AND_REPORT"
    assert_no_effect(audit)


def test_missing_plan_id_is_invalid() -> None:
    audit = audit_preregistration(base_plan(plan_id=""))
    assert audit.status == "INVALID"
    assert audit.reason == "MISSING_PLAN_ID_OR_VERSION"
    assert_no_effect(audit)


def test_digest_whitespace_is_invalid() -> None:
    audit = audit_preregistration(base_plan(immutable_digest="sha256 bad"))
    assert audit.status == "INVALID"
    assert audit.reason == "IMMUTABLE_DIGEST_FORMAT_INVALID"
    assert_no_effect(audit)


def test_missing_protocol_remains_indeterminate() -> None:
    audit = audit_preregistration(base_plan(protocol_ref=None))
    assert audit.status == "INDETERMINATE"
    assert audit.reason == "MISSING_PLAN_IMMUTABILITY_OR_PROTOCOL"
    assert_no_effect(audit)


def test_outcome_id_missing_is_invalid() -> None:
    outcome = PlannedOutcome("", "Primary outcome", True, "UP", "measure:1")
    audit = audit_preregistration(base_plan(outcomes=(outcome,)))
    assert audit.status == "INVALID"
    assert audit.reason == "OUTCOME_ID_MISSING"
    assert_no_effect(audit)


def test_analysis_id_missing_is_invalid() -> None:
    analysis = PlannedAnalysis("", "outcome:primary", AnalysisClass.CONFIRMATORY, "method:1", "estimand:1", "rule:1")
    audit = audit_preregistration(base_plan(analyses=(analysis,), report_analysis_ids=frozenset()))
    assert audit.status == "INVALID"
    assert audit.reason == "ANALYSIS_ID_MISSING"
    assert_no_effect(audit)


def test_report_unknown_outcome_is_invalid() -> None:
    audit = audit_preregistration(base_plan(report_outcome_ids=frozenset({"outcome:unknown"})))
    assert audit.status == "INVALID"
    assert audit.reason == "REPORT_UNKNOWN_OUTCOME"
    assert_no_effect(audit)


def test_report_unknown_analysis_is_invalid() -> None:
    audit = audit_preregistration(base_plan(report_analysis_ids=frozenset({"analysis:unknown"})))
    assert audit.status == "INVALID"
    assert audit.reason == "REPORT_UNKNOWN_ANALYSIS"
    assert_no_effect(audit)


def test_exploratory_unknown_analysis_is_invalid() -> None:
    audit = audit_preregistration(base_plan(exploratory_analysis_ids=frozenset({"analysis:unknown"})))
    assert audit.status == "INVALID"
    assert audit.reason == "EXPLORATORY_UNKNOWN_ANALYSIS"
    assert_no_effect(audit)


def test_duplicate_deviation_id_is_invalid() -> None:
    deviation = Deviation("dev:1", "protocol deviation", 3, "reason", "low")
    audit = audit_preregistration(base_plan(deviations=(deviation, deviation)))
    assert audit.status == "INVALID"
    assert audit.reason == "DUPLICATE_DEVIATION_ID"
    assert_no_effect(audit)


def test_missing_deviation_id_is_invalid() -> None:
    deviation = Deviation("", "protocol deviation", 3, "reason", "low")
    audit = audit_preregistration(base_plan(deviations=(deviation,)))
    assert audit.status == "INVALID"
    assert audit.reason == "DEVIATION_ID_MISSING"
    assert_no_effect(audit)


def test_registration_after_intervention_start_is_invalid() -> None:
    audit = audit_preregistration(base_plan(registered_at=3, intervention_start=2))
    assert audit.status == "INVALID"
    assert audit.reason == "REGISTRATION_AFTER_INTERVENTION_START"
    assert_no_effect(audit)


def test_exploratory_analyses_are_separated() -> None:
    exploratory = PlannedAnalysis("analysis:explore", "outcome:primary", AnalysisClass.EXPLORATORY, "method:2", "estimand:2", "rule:2")
    plan = base_plan(analyses=(base_plan().analyses[0], exploratory), report_analysis_ids=frozenset({"analysis:confirm", "analysis:explore"}), exploratory_analysis_ids=frozenset({"analysis:explore"}))
    audit = audit_preregistration(plan)
    assert audit.status == "VALID"
    assert audit.disposition == "EXPLORATORY_REVIEW"
    assert audit.exploratory_analysis_ids == ("analysis:explore",)
    assert_no_effect(audit)


def test_missing_reported_results_are_indeterminate() -> None:
    audit = audit_preregistration(base_plan(report_outcome_ids=frozenset(), report_analysis_ids=frozenset(), all_results_reported=False))
    assert audit.status == "INDETERMINATE"
    assert audit.reason == "ALL_PREREGISTERED_RESULTS_NOT_REPORTED"
    assert_no_effect(audit)


def test_undisclosed_deviation_is_indeterminate() -> None:
    deviation = Deviation("dev:1", "protocol deviation", None, None, None)
    audit = audit_preregistration(base_plan(deviations=(deviation,)))
    assert audit.status == "INDETERMINATE"
    assert audit.reason == "DEVIATION_DISCLOSURE_INCOMPLETE"
    assert_no_effect(audit)


def test_valid_disclosed_deviation_remains_review_only() -> None:
    deviation = Deviation("dev:1", "protocol deviation", 3, "safety", "low")
    audit = audit_preregistration(base_plan(deviations=(deviation,)))
    assert audit.status == "VALID"
    assert_no_effect(audit)


def test_unchanged_outcome_lock_after_no_observation_is_valid() -> None:
    snapshot = OutcomeLockSnapshot("plan:1", "sha256:1", "sha256:1", frozenset({"outcome:primary"}), frozenset({"outcome:primary"}), frozenset({"analysis:confirm"}), frozenset({"analysis:confirm"}), False)
    audit = audit_outcome_lock(snapshot)
    assert audit.status == "VALID"
    assert audit.reason == "OUTCOME_LOCK_UNCHANGED"
    assert_no_effect(audit)


def test_post_outcome_new_declaration_is_invalid() -> None:
    snapshot = OutcomeLockSnapshot("plan:1", "sha256:1", "sha256:1", frozenset({"outcome:primary"}), frozenset({"outcome:primary", "outcome:new"}), frozenset({"analysis:confirm"}), frozenset({"analysis:confirm"}), True)
    audit = audit_outcome_lock(snapshot)
    assert audit.status == "INVALID"
    assert audit.reason == "POST_OUTCOME_DECLARATION_MUTATION"
    assert_no_effect(audit)


def test_post_outcome_digest_change_is_invalid() -> None:
    snapshot = OutcomeLockSnapshot("plan:1", "sha256:1", "sha256:2", frozenset({"outcome:primary"}), frozenset({"outcome:primary"}), frozenset({"analysis:confirm"}), frozenset({"analysis:confirm"}), True)
    audit = audit_outcome_lock(snapshot)
    assert audit.status == "INVALID"
    assert audit.reason == "PLAN_DIGEST_CHANGED_AFTER_OUTCOME"
    assert_no_effect(audit)


def test_pre_outcome_plan_change_requires_review() -> None:
    snapshot = OutcomeLockSnapshot("plan:1", "sha256:1", "sha256:2", frozenset({"outcome:primary"}), frozenset({"outcome:primary", "outcome:new"}), frozenset({"analysis:confirm"}), frozenset({"analysis:confirm"}), False)
    audit = audit_outcome_lock(snapshot)
    assert audit.status == "INDETERMINATE"
    assert audit.reason == "PRE_OUTCOME_PLAN_CHANGE_REQUIRES_REVIEW"
    assert_no_effect(audit)


def test_lock_requires_plan_id() -> None:
    snapshot = OutcomeLockSnapshot("", "sha256:1", "sha256:1", frozenset(), frozenset(), frozenset(), frozenset(), False)
    audit = audit_outcome_lock(snapshot)
    assert audit.status == "INVALID"
    assert audit.reason == "LOCK_PLAN_ID_MISSING"
    assert_no_effect(audit)


def test_lock_requires_both_digests() -> None:
    snapshot = OutcomeLockSnapshot("plan:1", "", "sha256:1", frozenset(), frozenset(), frozenset(), frozenset(), False)
    audit = audit_outcome_lock(snapshot)
    assert audit.status == "INVALID"
    assert audit.reason == "LOCK_DIGEST_MISSING"
    assert_no_effect(audit)


def test_intervention_boundary_is_metadata_only() -> None:
    audit = audit_intervention_boundary(base_plan())
    assert audit.status == "VALID"
    assert audit.reason == "VALID_CONFIRMATORY_PLAN_AND_REPORT"
    assert_no_effect(audit)


def test_plan_version_is_required() -> None:
    audit = audit_preregistration(base_plan(plan_version=""))
    assert audit.status == "INVALID"
    assert audit.reason == "MISSING_PLAN_ID_OR_VERSION"
    assert_no_effect(audit)
