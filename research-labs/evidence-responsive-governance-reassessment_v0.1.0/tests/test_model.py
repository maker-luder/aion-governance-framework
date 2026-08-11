from __future__ import annotations

import pytest

from aion_governance_reassessment import (
    AdversarialStatus,
    ClaimScopeChange,
    EvidenceAdmissibilityStatus,
    EvidenceLevel,
    EvidenceQuality,
    EvidenceQualityAxis,
    EvidenceState,
    FALSIFIERS,
    GovernanceReassessmentCase,
    PrecautionaryProtection,
    ProvenanceStatus,
    ReassessmentDirection,
    ReassessmentPressure,
    ReplicationEvidenceSummary,
    ReviewDisposition,
    ReviewDomain,
    SubstantiveEvidenceDomain,
    claim_boundary_disposition,
    construct_evidence_state,
    recommend_replication_reassessment,
    review_disposition,
)
from aion_research_eval import ClaimBoundaryGate


def quality(
    provenance: ProvenanceStatus = ProvenanceStatus.VERIFIED,
    *,
    adversarial: AdversarialStatus = AdversarialStatus.SURVIVED,
    confirmations: int = 1,
    failures: int = 0,
) -> EvidenceQuality:
    return EvidenceQuality(
        provenance_status=provenance,
        adversarial_status=adversarial,
        replication_record_ref="replication:record-1"
        if confirmations or failures
        else None,
        valid_independent_confirmations=confirmations,
        valid_independent_failures=failures,
    )


def e3_state() -> EvidenceState:
    return construct_evidence_state(
        EvidenceLevel.E3,
        substantive_domains=(
            SubstantiveEvidenceDomain.FUNCTIONAL_INTERVENTION,
            SubstantiveEvidenceDomain.CONTINUITY,
        ),
        evidence_refs=("evidence:functional", "evidence:continuity"),
        quality=quality(confirmations=0),
    )


def test_four_review_domains_remain_separate_and_never_emit_rights():
    state = e3_state()
    outputs = {domain: review_disposition(state, domain) for domain in ReviewDomain}
    assert len(outputs) == 4
    assert outputs[ReviewDomain.RESEARCH_ETHICS_REVIEW] is ReviewDisposition.ENHANCED_RESEARCH_REVIEW
    assert all("RIGHT" not in value.value for value in outputs.values())


def test_single_failed_attempt_does_not_force_fixed_e2():
    recommendation = recommend_replication_reassessment(
        EvidenceLevel.E5,
        ReplicationEvidenceSummary(
            attempt_refs=("attempt:failed-1",),
            valid_independent_failures=1,
        ),
    )
    assert recommendation.direction is ReassessmentDirection.REASSESSMENT_DOWN
    assert recommendation.pressure is ReassessmentPressure.DOWNWARD_PRESSURE
    assert recommendation.observed_or_requested_level is EvidenceLevel.E5
    assert recommendation.proposed_evidence_level is None


def test_four_confirmations_plus_evaluator_drift_failure_do_not_downgrade():
    recommendation = recommend_replication_reassessment(
        EvidenceLevel.E5,
        ReplicationEvidenceSummary(
            attempt_refs=("c1", "c2", "c3", "c4", "drift-failure"),
            valid_independent_confirmations=4,
            evaluator_drift_failures=1,
        ),
    )
    assert recommendation.direction is ReassessmentDirection.STABLE
    assert recommendation.proposed_evidence_level is None
    assert recommendation.observed_or_requested_level is EvidenceLevel.E5


def test_invalid_replication_does_not_downgrade_substantive_evidence():
    recommendation = recommend_replication_reassessment(
        EvidenceLevel.E4,
        ReplicationEvidenceSummary(
            attempt_refs=("invalid-failure",),
            invalid_failures=1,
        ),
    )
    assert recommendation.direction is ReassessmentDirection.STABLE
    assert recommendation.pressure is ReassessmentPressure.NONE
    assert recommendation.proposed_evidence_level is None


def test_three_valid_independent_preregistered_failures_create_strong_pressure():
    recommendation = recommend_replication_reassessment(
        EvidenceLevel.E5,
        ReplicationEvidenceSummary(
            attempt_refs=("f1", "f2", "f3"),
            valid_independent_failures=3,
            preregistered_valid_independent_failures=3,
        ),
    )
    assert recommendation.pressure is ReassessmentPressure.STRONG_DOWNWARD_PRESSURE
    assert recommendation.direction is ReassessmentDirection.REASSESSMENT_DOWN
    assert recommendation.decision_status == "HOLD_FOR_RESEARCH_DECISION"
    assert recommendation.proposed_evidence_level is None


def test_mixed_or_boundary_condition_narrows_scope_without_quality_collapse():
    recommendation = recommend_replication_reassessment(
        EvidenceLevel.E4,
        ReplicationEvidenceSummary(
            attempt_refs=("mixed", "boundary"),
            mixed_attempts=1,
            boundary_condition_discoveries=1,
        ),
    )
    assert recommendation.direction is ReassessmentDirection.CLAIM_SCOPE_CHANGED
    assert recommendation.claim_scope is ClaimScopeChange.NARROWER
    assert recommendation.pressure is ReassessmentPressure.SCOPE_REVIEW
    assert recommendation.proposed_evidence_level is None


def test_no_evidence_is_distinct_from_contaminated_evidence():
    no_evidence = construct_evidence_state(
        EvidenceLevel.E0,
        substantive_domains=(),
        evidence_refs=(),
        quality=quality(confirmations=0),
    )
    contaminated = construct_evidence_state(
        EvidenceLevel.E4,
        substantive_domains=(
            SubstantiveEvidenceDomain.BEHAVIOR,
            SubstantiveEvidenceDomain.MEMORY,
            SubstantiveEvidenceDomain.METACOGNITION,
        ),
        evidence_refs=("evidence:exists",),
        quality=quality(ProvenanceStatus.CONTAMINATED),
    )
    assert no_evidence.observed_or_requested_level is EvidenceLevel.E0
    assert no_evidence.admissibility is EvidenceAdmissibilityStatus.ADMISSIBLE
    assert contaminated.observed_or_requested_level is EvidenceLevel.E4
    assert contaminated.admissibility is EvidenceAdmissibilityStatus.PROVENANCE_CONTAMINATED
    assert contaminated.effective_reassessment_level is None
    assert review_disposition(
        contaminated, ReviewDomain.RESEARCH_ETHICS_REVIEW
    ) is ReviewDisposition.HOLD_FOR_GOVERNANCE_DECISION


@pytest.mark.parametrize(
    ("provenance", "expected"),
    (
        (ProvenanceStatus.INCOMPLETE, EvidenceAdmissibilityStatus.PROVENANCE_INCOMPLETE),
        (
            ProvenanceStatus.CONTAMINATED,
            EvidenceAdmissibilityStatus.PROVENANCE_CONTAMINATED,
        ),
    ),
)
def test_provenance_failure_holds_without_rewriting_observed_level(provenance, expected):
    state = construct_evidence_state(
        EvidenceLevel.E4,
        substantive_domains=(
            SubstantiveEvidenceDomain.BEHAVIOR,
            SubstantiveEvidenceDomain.CONTINUITY,
            SubstantiveEvidenceDomain.MEMORY,
        ),
        evidence_refs=("evidence:e4",),
        quality=quality(provenance),
    )
    assert state.observed_or_requested_level is EvidenceLevel.E4
    assert state.admissibility is expected
    assert state.effective_reassessment_level is None
    restored = EvidenceState.from_json(state.to_json())
    assert restored == state


def test_quality_axes_cannot_count_toward_substantive_domain_minimum():
    assert set(EvidenceQualityAxis) == {
        EvidenceQualityAxis.PROVENANCE,
        EvidenceQualityAxis.REPLICATION,
        EvidenceQualityAxis.ADVERSARIAL_ROBUSTNESS,
    }
    assert all(axis.value not in SubstantiveEvidenceDomain.__members__ for axis in EvidenceQualityAxis)
    state = construct_evidence_state(
        EvidenceLevel.E4,
        substantive_domains=(SubstantiveEvidenceDomain.BEHAVIOR,),
        evidence_refs=("evidence:behavior",),
        quality=quality(),
    )
    assert state.admissibility is EvidenceAdmissibilityStatus.INSUFFICIENT_FOR_CLASSIFICATION
    assert state.effective_reassessment_level is None


def test_e4_and_e5_quality_prerequisites_are_separate_from_domain_count():
    domains = (
        SubstantiveEvidenceDomain.BEHAVIOR,
        SubstantiveEvidenceDomain.FUNCTIONAL_INTERVENTION,
        SubstantiveEvidenceDomain.CONTINUITY,
        SubstantiveEvidenceDomain.MEMORY,
        SubstantiveEvidenceDomain.METACOGNITION,
    )
    e4 = construct_evidence_state(
        EvidenceLevel.E4,
        substantive_domains=domains[:3],
        evidence_refs=("evidence:e4",),
        quality=quality(adversarial=AdversarialStatus.NOT_TESTED, confirmations=0),
    )
    e5 = construct_evidence_state(
        EvidenceLevel.E5,
        substantive_domains=domains,
        evidence_refs=("evidence:e5",),
        quality=quality(confirmations=0),
    )
    assert e4.admissibility is EvidenceAdmissibilityStatus.HELD_FOR_REVIEW
    assert e5.admissibility is EvidenceAdmissibilityStatus.HELD_FOR_REVIEW
    assert e5.observed_or_requested_level is EvidenceLevel.E5


def test_self_report_alone_cannot_support_elevated_state():
    state = construct_evidence_state(
        EvidenceLevel.E3,
        substantive_domains=(SubstantiveEvidenceDomain.SELF_REPORT,),
        evidence_refs=("evidence:self-report",),
        quality=quality(confirmations=0),
    )
    assert state.admissibility is EvidenceAdmissibilityStatus.INSUFFICIENT_FOR_CLASSIFICATION
    assert state.effective_reassessment_level is None


def test_precaution_is_reversible_bounded_auditable_and_low_authority():
    precaution = PrecautionaryProtection(
        ("ADDITIONAL_REVIEW", "PRESERVATION_SNAPSHOT", "REQUIRE_PROVENANCE")
    )
    assert all(
        (precaution.reversible, precaution.bounded, precaution.auditable, precaution.low_authority)
    )
    assert precaution.subjectivity_confirmation == precaution.autonomous_authority == "NONE"
    with pytest.raises(ValueError):
        PrecautionaryProtection(("AUTONOMOUS_AUTHORITY",))


def test_typed_case_preserves_governance_boundary():
    state = e3_state()
    case = GovernanceReassessmentCase(
        case_id="case-e3-method-example",
        evidence_state=state,
        review_domain=ReviewDomain.RESEARCH_ETHICS_REVIEW,
        review_disposition=ReviewDisposition.ENHANCED_RESEARCH_REVIEW,
        reason="Cross-method synthetic evidence requests human review.",
        uncertainty="Independent replication and adversarial generality remain open.",
        counterevidence_refs=("counterevidence:simpler-mechanism",),
        reviewed_at="2026-08-11T00:00:00Z",
        provenance_refs=("owner:human", "review:chatgpt", "implementation:codex-research"),
        precautionary_protection=PrecautionaryProtection(("ADDITIONAL_REVIEW",)),
    )
    assert case.recommendation_type == "REVIEW_RECOMMENDATION"
    assert case.human_review_required is True
    assert case.automatic_rights == case.automatic_authority == "NONE"
    assert case.main_effect == case.canonical_effect == case.runtime_effect == "NONE"


def test_claim_boundary_reuses_existing_repository_gate():
    gate = ClaimBoundaryGate()
    assert claim_boundary_disposition(gate, "subjectivity_established") == "DENY_PROMOTION"
    assert claim_boundary_disposition(gate, "review_recommendation") == "RESEARCH_EVIDENCE_ONLY"


def test_falsifier_register_covers_six_fail_closed_challenges():
    assert len(FALSIFIERS) == 6
    assert FALSIFIERS[0].startswith("F1_")
    assert FALSIFIERS[-1].startswith("F6_")
