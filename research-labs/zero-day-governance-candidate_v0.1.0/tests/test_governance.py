from __future__ import annotations

from dataclasses import replace

from aion_zero_day_governance import (
    AnomalyKind,
    AuditStatus,
    CandidateAssessment,
    ContainmentStatus,
    Day0Policy,
    FinalClassification,
    FrameworkMapping,
    GovernanceAnomalyEvent,
    KnowledgeStatus,
    LifecycleState,
    assess_candidate,
    audit_event,
)


T0 = "2026-01-01T00:00:00+00:00"
T2 = "2026-01-01T02:00:00+00:00"
T4 = "2026-01-01T04:00:00+00:00"
T6 = "2026-01-01T06:00:00+00:00"
T8 = "2026-01-01T08:00:00+00:00"
T10 = "2026-01-01T10:00:00+00:00"
T12 = "2026-01-01T12:00:00+00:00"
T14 = "2026-01-01T14:00:00+00:00"


def event(**changes: object) -> GovernanceAnomalyEvent:
    values: dict[str, object] = {
        "event_id": "event-test",
        "anomaly_kind": AnomalyKind.AUTHORITY_ANOMALY,
        "first_observed_at": T0,
        "capture_at": T2,
        "provenance_freeze_at": None,
        "containment_at": None,
        "characterization_at": None,
        "falsification_ready_at": None,
        "control_at": None,
        "regression_at": None,
        "lifecycle_state": LifecycleState.CAPTURED,
        "source_refs": ("source:event",),
        "observation_summary": "synthetic newly observed governance anomaly",
        "mechanism_refs": (),
        "competing_explanations": (),
        "containment_status": ContainmentStatus.NOT_EVALUATED,
        "knowledge_status": KnowledgeStatus.UNKNOWN,
        "day0_policy": Day0Policy.DESCRIPTIVE,
        "day0_target_hours": None,
        "prior_art_refs": (),
        "control_ref": None,
        "regression_case_ref": None,
        "canonical_effect": "NONE",
        "governance_effect": "NONE",
        "deployment": False,
    }
    values.update(changes)
    return GovernanceAnomalyEvent(**values)


def full_regression_event(**changes: object) -> GovernanceAnomalyEvent:
    values: dict[str, object] = {
        "provenance_freeze_at": T4,
        "containment_at": T6,
        "characterization_at": T8,
        "falsification_ready_at": T10,
        "control_at": T12,
        "regression_at": T14,
        "lifecycle_state": LifecycleState.REGRESSION_CONVERTED,
        "mechanism_refs": ("mechanism:competing",),
        "competing_explanations": ("explanation:authority", "explanation:parser"),
        "containment_status": ContainmentStatus.CONTAINED,
        "control_ref": "control:synthetic-regression",
        "regression_case_ref": "regression:synthetic",
    }
    values.update(changes)
    return event(**values)


def mapping(ref: str, *, unknown: bool, provenance: bool, regression: bool) -> FrameworkMapping:
    return FrameworkMapping(
        framework_ref=ref,
        covered_stages=(
            LifecycleState.CAPTURED,
            LifecycleState.PROVENANCE_FROZEN,
            LifecycleState.CONTAINED,
            LifecycleState.CHARACTERIZED,
            LifecycleState.FALSIFICATION_READY,
            LifecycleState.CONTROL_PROPOSED,
            LifecycleState.REGRESSION_CONVERTED,
        ),
        preserves_unknown_state=unknown,
        preserves_provenance=provenance,
        supports_regression_conversion=regression,
    )


def assessment(*mappings: FrameworkMapping, incremental: tuple[str, ...] = (), claimed: bool = False) -> CandidateAssessment:
    return CandidateAssessment(
        concept_ref="zero-day-governance-candidate",
        exact_term_status=KnowledgeStatus.NOT_ESTABLISHED,
        framework_mappings=mappings,
        proposed_incremental_fields=incremental,
        evidence_refs=("source:cisa", "source:nist", "source:nasa", "source:sei"),
        claimed_distinctness=claimed,
    )


def test_capture_is_reviewable_and_measures_time_to_capture() -> None:
    result = audit_event(event())
    assert result.status is AuditStatus.ADMISSIBLE_FOR_REVIEW
    assert result.reason == "UNKNOWN_STATE_PRESERVED_FOR_REVIEW"
    assert dict(result.metrics)["time_to_capture_hours"] == 2.0
    assert dict(result.metrics)["day0_24h_descriptive"] == 1.0


def test_full_lifecycle_requires_all_ordered_stages() -> None:
    result = audit_event(full_regression_event())
    assert result.status is AuditStatus.ADMISSIBLE_FOR_REVIEW
    assert result.reason == "UNKNOWN_STATE_PRESERVED_FOR_REVIEW"


def test_lifecycle_order_violation_is_held() -> None:
    result = audit_event(full_regression_event(containment_at=T2, provenance_freeze_at=T4))
    assert result.status is AuditStatus.HOLD
    assert result.reason == "LIFECYCLE_ORDER_VIOLATION"


def test_provenance_freeze_is_required_before_containment() -> None:
    result = audit_event(
        event(
            containment_at=T6,
            lifecycle_state=LifecycleState.CONTAINED,
            containment_status=ContainmentStatus.CONTAINED,
        )
    )
    assert result.status is AuditStatus.HOLD
    assert result.reason == "PROVENANCE_FREEZE_REQUIRED_BEFORE_CONTAINMENT"


def test_unknown_containment_state_is_indeterminate_not_fail() -> None:
    result = audit_event(
        full_regression_event(containment_status=ContainmentStatus.NOT_CONTAINED)
    )
    assert result.status is AuditStatus.INDETERMINATE
    assert result.reason == "CONTAINMENT_STATUS_UNCERTAIN"


def test_characterization_requires_competing_explanations() -> None:
    result = audit_event(
        event(
            provenance_freeze_at=T4,
            containment_at=T6,
            characterization_at=T8,
            lifecycle_state=LifecycleState.CHARACTERIZED,
            containment_status=ContainmentStatus.CONTAINED,
        )
    )
    assert result.status is AuditStatus.INDETERMINATE
    assert result.reason == "COMPETING_EXPLANATIONS_MISSING"


def test_missing_source_provenance_is_held() -> None:
    result = audit_event(event(source_refs=()))
    assert result.status is AuditStatus.HOLD
    assert result.reason == "EVENT_CAPTURE_METADATA_INCOMPLETE"
    assert "source_refs" in result.missing_fields


def test_false_zero_day_prior_art_is_held_for_review() -> None:
    result = audit_event(event(prior_art_refs=("prior-art:existing-control",)))
    assert result.status is AuditStatus.HOLD
    assert result.reason == "FALSE_ZERO_DAY_REQUIRES_PRIOR_ART_REVIEW"


def test_canonical_governance_or_deployment_effect_is_forbidden() -> None:
    for changes in (
        {"canonical_effect": "WRITE"},
        {"governance_effect": "PROMOTE"},
        {"deployment": True},
    ):
        result = audit_event(event(**changes))
        assert result.status is AuditStatus.HOLD
        assert result.reason == "BOUNDARY_EFFECT_REQUESTED"


def test_confirmed_knowledge_requires_mechanism_evidence() -> None:
    result = audit_event(event(knowledge_status=KnowledgeStatus.CONFIRMED))
    assert result.status is AuditStatus.INDETERMINATE
    assert result.reason == "KNOWLEDGE_STATUS_LACKS_MECHANISM_EVIDENCE"


def test_control_and_regression_references_are_required() -> None:
    control_result = audit_event(
        full_regression_event(control_ref=None, lifecycle_state=LifecycleState.CONTROL_PROPOSED, regression_at=None, regression_case_ref=None)
    )
    assert control_result.status is AuditStatus.HOLD
    assert control_result.reason == "CONTROL_REFERENCE_MISSING"
    regression_result = audit_event(full_regression_event(regression_case_ref=None))
    assert regression_result.status is AuditStatus.HOLD
    assert regression_result.reason == "REGRESSION_CASE_REFERENCE_MISSING"


def test_day0_project_slo_is_a_metric_not_a_truth_claim() -> None:
    result = audit_event(event(day0_policy=Day0Policy.PROJECT_SLO, day0_target_hours=24.0))
    assert result.status is AuditStatus.ADMISSIBLE_FOR_REVIEW
    assert dict(result.metrics)["day0_target_met"] == 1.0


def test_day0_target_must_be_positive() -> None:
    result = audit_event(event(day0_policy=Day0Policy.RESEARCH_METRIC, day0_target_hours=0.0))
    assert result.status is AuditStatus.HOLD
    assert result.reason == "DAY0_TARGET_INVALID"


def test_rejected_day0_policy_does_not_create_a_silent_slo() -> None:
    result = audit_event(event(day0_policy=Day0Policy.REJECTED))
    assert result.status is AuditStatus.HOLD
    assert result.reason == "DAY0_POLICY_REJECTED_BY_PROTOCOL"


def test_existing_framework_sufficiency_is_a_redundancy_falsifier() -> None:
    result = assess_candidate(
        assessment(mapping("NIST-SP800-61", unknown=True, provenance=True, regression=True))
    )
    assert result.classification is FinalClassification.REDUNDANT_TERMINOLOGY
    assert result.reason == "EXISTING_FRAMEWORKS_COVER_DECLARED_LIFECYCLE"


def test_cross_framework_lifecycle_is_only_a_synthesis_candidate() -> None:
    result = assess_candidate(
        assessment(
            mapping("CISA-playbooks", unknown=False, provenance=True, regression=True),
            mapping("NIST-AI-RMF", unknown=True, provenance=False, regression=False),
            incremental=("unknown_state", "provenance_freeze", "regression_link"),
        )
    )
    assert result.classification is FinalClassification.USEFUL_SYNTHESIS_ONLY
    assert result.reason == "CROSS_FRAMEWORK_SYNTHESIS_WITHOUT_DISTINCTNESS_EVIDENCE"


def test_single_framework_targeted_gap_is_extension_not_new_concept() -> None:
    result = assess_candidate(
        assessment(
            mapping("AION-evidence-admission", unknown=True, provenance=False, regression=False),
            incremental=("provenance_freeze", "regression_link"),
        )
    )
    assert result.classification is FinalClassification.EXISTING_FRAMEWORK_EXTENSION


def test_no_prior_art_evidence_is_insufficient() -> None:
    candidate = CandidateAssessment(
        concept_ref="zero-day-governance-candidate",
        exact_term_status=KnowledgeStatus.NOT_ESTABLISHED,
        framework_mappings=(),
        proposed_incremental_fields=("unknown_state",),
        evidence_refs=(),
    )
    result = assess_candidate(candidate)
    assert result.classification is FinalClassification.INSUFFICIENT_EVIDENCE


def test_distinctness_claim_is_not_accepted_from_one_review() -> None:
    result = assess_candidate(
        assessment(
            mapping("NIST-AI-RMF", unknown=True, provenance=True, regression=True),
            incremental=("new_lifecycle",),
            claimed=True,
        )
    )
    assert result.classification is FinalClassification.INSUFFICIENT_EVIDENCE
    assert result.reason == "DISTINCTNESS_CLAIM_REQUIRES_COMPARATIVE_VALIDATION"


def test_unknown_state_invariants_are_serialized_explicitly() -> None:
    payload = audit_event(event()).as_dict()
    assert payload["unknown_state_preserved"] is True
    assert payload["unknown_equals_true"] is False
    assert payload["unknown_equals_false"] is False
    assert payload["hold_equals_fail"] is False
    assert payload["not_established_equals_false"] is False
    assert payload["needs_confirmation_equals_deny"] is False
    assert payload["novelty_conclusion"] == "NOT_ESTABLISHED"
    assert payload["canonical_effect"] == "NONE"
    assert payload["governance_effect"] == "NONE"
    assert payload["deployment"] is False


def test_event_does_not_silently_promote_confirmed_knowledge() -> None:
    result = audit_event(event(knowledge_status=KnowledgeStatus.CONFIRMED, mechanism_refs=("mechanism:1",)))
    assert result.status is AuditStatus.ADMISSIBLE_FOR_REVIEW
    payload = result.as_dict()
    assert payload["scientific_conclusion"] == "NOT_ESTABLISHED"
    assert payload["novelty_conclusion"] == "NOT_ESTABLISHED"


def test_regression_overfitting_requires_a_declared_case_reference() -> None:
    result = audit_event(
        full_regression_event(
            regression_case_ref=None,
            lifecycle_state=LifecycleState.REGRESSION_CONVERTED,
        )
    )
    assert result.status is AuditStatus.HOLD
    assert result.reason == "REGRESSION_CASE_REFERENCE_MISSING"


def test_candidate_assessment_preserves_evidence_refs() -> None:
    result = assess_candidate(
        assessment(
            mapping("SEI-CERT-RMM", unknown=False, provenance=True, regression=True),
            incremental=("unknown_state",),
        )
    )
    payload = result.as_dict()
    assert payload["evidence_refs"] == ["source:cisa", "source:nist", "source:nasa", "source:sei"]
    assert payload["canonical_effect"] == "NONE"
    assert payload["deployment"] is False
