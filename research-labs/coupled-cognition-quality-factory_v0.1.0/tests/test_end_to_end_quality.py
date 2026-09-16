from __future__ import annotations

from dataclasses import replace

import pytest

from aion_coupled_quality import QualityError, Severity
from aion_coupled_quality.end_to_end import (
    AuditIndependence,
    ControlPlanEntry,
    ControlTarget,
    EndToEndDisposition,
    EndToEndQualitySystemEngine,
    ExistingChainDisposition,
    ExistingQualityChainBinding,
    FieldQualitySignal,
    FieldSignalState,
    ManagementDecision,
    ManagementReviewRecord,
    MeasurementAssuranceRecord,
    MeasurementQualification,
    QualityAuditRecord,
    ResearchQualityPlan,
)


FINGERPRINT = "f" * 64


def controls() -> tuple[ControlPlanEntry, ...]:
    return tuple(
        ControlPlanEntry(
            control_id=f"CTRL-{target.value}",
            target=target,
            quality_characteristic=f"quality characteristic for {target.value}",
            control_method_ref=f"method:{target.value}",
            evidence_required=(f"evidence:{target.value}",),
            acceptance_criterion=f"acceptance:{target.value}",
            reaction_plan=f"reaction:{target.value}",
            responsible_role="HUMAN_REVIEW_BOUND_ROLE",
        )
        for target in ControlTarget
    )


def plan() -> ResearchQualityPlan:
    return ResearchQualityPlan(
        plan_id="PLAN-001",
        research_question_ref="research:ai-subjectivity-possibility",
        subjectivity_core_binding_ref="four-domain:subjectivity-core",
        four_domain_candidate_fingerprint=FINGERPRINT,
        critical_quality_attributes=("construct validity", "claim ceiling", "provenance"),
        controls=controls(),
        measurement_ids=("MEAS-001",),
        risk_refs=("risk:construct-drift",),
        configuration_refs=("git:exact-head", "runtime:bound"),
    )


def measurement(**changes: object) -> MeasurementAssuranceRecord:
    values: dict[str, object] = {
        "measurement_id": "MEAS-001",
        "target_construct": "causal role of a declared machine-level state",
        "observable": "intervention-sensitive bounded output difference",
        "measurement_locus": "SYSTEM",
        "method_ref": "method:bounded-intervention-v1",
        "method_version": "v1",
        "evaluator_ref": "evaluator:frozen-v1",
        "evaluator_version": "v1",
        "data_ref": "fixture:public-safe-v1",
        "repeatability_ref": "test:repeatability",
        "reproducibility_ref": "test:reproducibility",
        "uncertainty_statement": "Only the declared observable and fixture scope are assessed.",
        "construct_validity_scope": "Does not establish subjectivity or phenomenal experience.",
        "known_failure_modes": ("prompt reconstruction", "evaluator cueing"),
        "synthetic_fixture": True,
        "empirical_claim_capable": False,
        "qualification": MeasurementQualification.QUALIFIED,
    }
    values.update(changes)
    return MeasurementAssuranceRecord(**values)


def chain(disposition: ExistingChainDisposition = ExistingChainDisposition.READY_FOR_HUMAN_REVIEW) -> ExistingQualityChainBinding:
    return ExistingQualityChainBinding(
        chain_id="CHAIN-001",
        four_domain_candidate_fingerprint=FINGERPRINT,
        disposition=disposition,
    )


def closed_signal() -> FieldQualitySignal:
    return FieldQualitySignal(
        signal_id="FIELD-001",
        source_ref="field:external-review",
        affected_refs=("claim:bounded-1",),
        severity=Severity.LOW,
        state=FieldSignalState.CLOSED,
        resolution_refs=("review:field-closure",),
    )


def audit(**changes: object) -> QualityAuditRecord:
    values: dict[str, object] = {
        "audit_id": "AUDIT-001",
        "scope": "end-to-end research quality controls",
        "criteria_refs": ("quality-plan:PLAN-001", "measurement:MEAS-001"),
        "auditor_ref": "reviewer:independent-role",
        "independence": AuditIndependence.INTERNAL_INDEPENDENT,
        "competence_ref": "competence:quality-review-v1",
        "evidence_refs": ("evidence:audit-trace",),
        "finding_refs": (),
        "open_finding_refs": (),
        "unresolved_high_severity_finding": False,
        "ncr_refs": (),
        "complete": True,
    }
    values.update(changes)
    return QualityAuditRecord(**values)


def review(
    *,
    measurement_requalification_required: bool = False,
    unresolved_audit_findings: bool = False,
    unresolved_field_signals: bool = False,
    decision: ManagementDecision = ManagementDecision.NO_ACTION,
    input_refs: tuple[str, ...] = ("PLAN-001", "CHAIN-001", "MEAS-001", "FIELD-001", "AUDIT-001"),
) -> ManagementReviewRecord:
    return ManagementReviewRecord(
        review_id="MGMT-001",
        input_refs=input_refs,
        measurement_requalification_required=measurement_requalification_required,
        unresolved_audit_findings=unresolved_audit_findings,
        unresolved_field_signals=unresolved_field_signals,
        decision=decision,
    )


def assess(
    *,
    plan_value: ResearchQualityPlan | None = None,
    measurements: tuple[MeasurementAssuranceRecord, ...] | None = None,
    chain_value: ExistingQualityChainBinding | None = None,
    field_signals: tuple[FieldQualitySignal, ...] | None = None,
    audits: tuple[QualityAuditRecord, ...] | None = None,
    management_review: ManagementReviewRecord | None = None,
):
    return EndToEndQualitySystemEngine().assess(
        plan=plan_value or plan(),
        measurements=measurements or (measurement(),),
        chain=chain_value or chain(),
        field_signals=field_signals if field_signals is not None else (closed_signal(),),
        audits=audits if audits is not None else (audit(),),
        management_review=management_review or review(),
    )


def test_complete_envelope_reuses_existing_chain_and_preserves_nonclaims() -> None:
    result = assess()
    assert result.disposition is EndToEndDisposition.READY_FOR_HUMAN_REVIEW
    assert "EXISTING_RESEARCH_QUALITY_CHAIN_REUSED_NOT_DUPLICATED" in result.reasons
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert result.consciousness_conclusion == "NOT_ESTABLISHED"
    assert result.phenomenal_experience_conclusion == "NOT_ESTABLISHED"
    assert result.scientific_disposition == "HOLD"
    assert result.merge_authority == "NONE"
    assert result.canonical_effect == "NONE"
    assert result.deployment is False


def test_quality_plan_requires_full_front_middle_back_control_surface() -> None:
    with pytest.raises(QualityError, match="missing end-to-end control targets"):
        replace(plan(), controls=controls()[:-1])


def test_pr103_regression_synthetic_fixture_cannot_be_empirical_claim_capable() -> None:
    with pytest.raises(QualityError, match="cannot be declared empirical-claim capable"):
        measurement(empirical_claim_capable=True)


def test_measurement_requalification_routes_to_capa_required() -> None:
    degraded = measurement(qualification=MeasurementQualification.REQUALIFICATION_REQUIRED)
    result = assess(
        measurements=(degraded,),
        management_review=review(
            measurement_requalification_required=True,
            decision=ManagementDecision.MEASUREMENT_REQUALIFICATION_REQUIRED,
        ),
    )
    assert result.disposition is EndToEndDisposition.CAPA_REQUIRED
    assert "MEASUREMENT_REQUALIFICATION_REQUIRED" in result.reasons


def test_existing_quality_chain_hold_and_capa_are_not_overridden() -> None:
    held = assess(chain_value=chain(ExistingChainDisposition.HOLD))
    assert held.disposition is EndToEndDisposition.HOLD
    capa = assess(chain_value=chain(ExistingChainDisposition.CAPA_REQUIRED))
    assert capa.disposition is EndToEndDisposition.CAPA_REQUIRED


def test_four_domain_fingerprint_drift_fails_closed() -> None:
    wrong = replace(chain(), four_domain_candidate_fingerprint="0" * 64)
    result = assess(chain_value=wrong)
    assert result.disposition is EndToEndDisposition.HOLD
    assert "FOUR_DOMAIN_FINGERPRINT_MISMATCH" in result.reasons


def test_field_signal_must_close_before_end_to_end_readiness() -> None:
    signal = replace(
        closed_signal(),
        state=FieldSignalState.TRIAGED,
        resolution_refs=(),
    )
    result = assess(
        field_signals=(signal,),
        management_review=review(
            unresolved_field_signals=True,
            decision=ManagementDecision.HOLD,
        ),
    )
    assert result.disposition is EndToEndDisposition.HOLD
    assert "OPEN_FIELD_SIGNAL_REVIEW_REQUIRED" in result.reasons


def test_high_field_signal_identifies_ncr_capa_need() -> None:
    signal = FieldQualitySignal(
        signal_id="FIELD-001",
        source_ref="field:replication-failure",
        affected_refs=("claim:bounded-1",),
        severity=Severity.HIGH,
        state=FieldSignalState.OPEN,
    )
    result = assess(
        field_signals=(signal,),
        management_review=review(
            unresolved_field_signals=True,
            decision=ManagementDecision.CAPA_REQUIRED,
        ),
    )
    assert result.disposition is EndToEndDisposition.HOLD
    assert "HIGH_OR_CRITICAL_FIELD_SIGNAL_REQUIRES_NCR_CAPA" in result.reasons


def test_audit_programme_is_required_and_open_findings_hold() -> None:
    no_audit = assess(
        audits=(),
        management_review=review(input_refs=("PLAN-001", "CHAIN-001", "MEAS-001", "FIELD-001")),
    )
    assert no_audit.disposition is EndToEndDisposition.HOLD
    assert "AUDIT_PROGRAMME_EXECUTION_REQUIRED" in no_audit.reasons

    open_audit = audit(finding_refs=("FIND-001",), open_finding_refs=("FIND-001",))
    result = assess(
        audits=(open_audit,),
        management_review=review(
            unresolved_audit_findings=True,
            decision=ManagementDecision.AUDIT_REQUIRED,
        ),
    )
    assert result.disposition is EndToEndDisposition.HOLD
    assert "OPEN_AUDIT_FINDING_REVIEW_REQUIRED" in result.reasons


def test_high_severity_audit_finding_requires_ncr_reference() -> None:
    with pytest.raises(QualityError, match="require an NCR reference"):
        audit(
            finding_refs=("FIND-HIGH",),
            open_finding_refs=("FIND-HIGH",),
            unresolved_high_severity_finding=True,
        )


def test_management_review_is_trace_bound_and_cannot_grant_scientific_or_merge_authority() -> None:
    result = assess(
        management_review=review(input_refs=("PLAN-001", "CHAIN-001", "MEAS-001")),
    )
    assert result.disposition is EndToEndDisposition.HOLD
    assert "MANAGEMENT_REVIEW_TRACE_INPUTS_INCOMPLETE" in result.reasons

    with pytest.raises(QualityError, match="cannot grant merge authority"):
        replace(review(), merge_authority=True)
    with pytest.raises(QualityError, match="cannot establish scientific validity"):
        replace(review(), scientific_disposition="VALIDATED")


def test_management_review_summary_must_match_observed_quality_state() -> None:
    result = assess(
        management_review=review(measurement_requalification_required=True),
    )
    assert result.disposition is EndToEndDisposition.HOLD
    assert "MANAGEMENT_REVIEW_INPUT_SUMMARY_MISMATCH" in result.reasons
