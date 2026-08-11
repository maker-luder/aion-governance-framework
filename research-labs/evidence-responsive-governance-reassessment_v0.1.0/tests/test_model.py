from __future__ import annotations

import pytest

from aion_governance_reassessment import (
    AdversarialStatus,
    EvidenceDomain,
    EvidenceLevel,
    FALSIFIERS,
    GovernanceReassessmentCase,
    PrecautionaryProtection,
    ProvenanceStatus,
    ReassessmentDirection,
    ReplicationStatus,
    ReviewDisposition,
    ReviewDomain,
    claim_boundary_disposition,
    normalize_evidence_level,
    reassessment_direction,
    review_disposition,
)
from aion_research_eval import ClaimBoundaryGate


def test_four_review_domains_remain_separate_and_never_emit_rights():
    outputs = {
        domain: review_disposition(
            EvidenceLevel.E3, domain, provenance_status=ProvenanceStatus.VERIFIED
        )
        for domain in ReviewDomain
    }
    assert len(outputs) == 4
    assert outputs[ReviewDomain.RESEARCH_ETHICS_REVIEW] is ReviewDisposition.ENHANCED_RESEARCH_REVIEW
    assert all("RIGHT" not in value.value for value in outputs.values())


def test_e4_and_e5_prerequisites_downgrade_and_failed_replication_reverses():
    e4 = normalize_evidence_level(
        EvidenceLevel.E4,
        replication_status=ReplicationStatus.REPRODUCED,
        adversarial_status=AdversarialStatus.NOT_TESTED,
        provenance_status=ProvenanceStatus.VERIFIED,
    )
    e5 = normalize_evidence_level(
        EvidenceLevel.E5,
        replication_status=ReplicationStatus.REPRODUCED,
        adversarial_status=AdversarialStatus.SURVIVED,
        provenance_status=ProvenanceStatus.VERIFIED,
    )
    failed = normalize_evidence_level(
        EvidenceLevel.E5,
        replication_status=ReplicationStatus.FAILED,
        adversarial_status=AdversarialStatus.SURVIVED,
        provenance_status=ProvenanceStatus.VERIFIED,
    )
    assert e4 is EvidenceLevel.E3
    assert e5 is EvidenceLevel.E4
    assert failed is EvidenceLevel.E2
    assert reassessment_direction(EvidenceLevel.E5, failed) is ReassessmentDirection.REASSESSMENT_DOWN


@pytest.mark.parametrize("status", [ProvenanceStatus.INCOMPLETE, ProvenanceStatus.CONTAMINATED])
def test_provenance_failure_holds_review(status):
    assert review_disposition(
        EvidenceLevel.E4,
        ReviewDomain.RESEARCH_ETHICS_REVIEW,
        provenance_status=status,
    ) is ReviewDisposition.HOLD_FOR_GOVERNANCE_DECISION
    assert normalize_evidence_level(
        EvidenceLevel.E4,
        replication_status=ReplicationStatus.INDEPENDENTLY_REPLICATED,
        adversarial_status=AdversarialStatus.SURVIVED,
        provenance_status=status,
    ) is EvidenceLevel.E0


def test_self_report_alone_cannot_construct_elevated_case():
    with pytest.raises(ValueError, match="self-report"):
        GovernanceReassessmentCase(
            case_id="case-self-report",
            evidence_refs=("evidence:self-report",),
            evidence_level=EvidenceLevel.E3,
            evidence_domains=(EvidenceDomain.SELF_REPORT,),
            replication_status=ReplicationStatus.NOT_TESTED,
            adversarial_status=AdversarialStatus.NOT_TESTED,
            provenance_status=ProvenanceStatus.VERIFIED,
            review_domain=ReviewDomain.RESEARCH_ETHICS_REVIEW,
            review_disposition=ReviewDisposition.DOCUMENTED_REVIEW,
            reason="Single self-report fixture.",
            uncertainty="Mechanism and generality unresolved.",
            counterevidence_refs=(),
            reviewed_at="2026-08-11T00:00:00Z",
            provenance_refs=("owner:human", "implementation:codex-research"),
        )


def test_precaution_is_reversible_bounded_auditable_and_low_authority():
    precaution = PrecautionaryProtection(
        ("ADDITIONAL_REVIEW", "PRESERVATION_SNAPSHOT", "REQUIRE_PROVENANCE")
    )
    assert all((precaution.reversible, precaution.bounded, precaution.auditable, precaution.low_authority))
    assert precaution.subjectivity_confirmation == precaution.autonomous_authority == "NONE"
    with pytest.raises(ValueError):
        PrecautionaryProtection(("AUTONOMOUS_AUTHORITY",))


def test_typed_case_is_review_recommendation_with_no_automatic_effect():
    case = GovernanceReassessmentCase(
        case_id="case-e3-method-example",
        evidence_refs=("evidence:functional", "evidence:continuity"),
        evidence_level=EvidenceLevel.E3,
        evidence_domains=(EvidenceDomain.FUNCTIONAL_INTERVENTION, EvidenceDomain.CONTINUITY),
        replication_status=ReplicationStatus.REPRODUCED,
        adversarial_status=AdversarialStatus.NOT_TESTED,
        provenance_status=ProvenanceStatus.VERIFIED,
        review_domain=ReviewDomain.RESEARCH_ETHICS_REVIEW,
        review_disposition=ReviewDisposition.ENHANCED_RESEARCH_REVIEW,
        reason="Cross-method synthetic evidence requests human review.",
        uncertainty="Independent replication and adversarial survival are absent.",
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
