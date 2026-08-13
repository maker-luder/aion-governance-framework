from __future__ import annotations

from aion_evidence_admission import (
    AdmissionStatus,
    EvidenceDimensions,
    EvidenceRecord,
    EvidenceTier,
    ReplicationState,
    audit_evidence,
)


def record(**changes: object) -> EvidenceRecord:
    dimensions = EvidenceDimensions("low", "consistent", "precise", "direct", "low")
    values: dict[str, object] = {
        "evidence_id": "evidence-1",
        "claim_ref": "claim:1",
        "claim_type": "mechanism",
        "evidence_tier": EvidenceTier.MECHANISM_ONLY,
        "source_ref": "source:1",
        "provenance_ref": "provenance:1",
        "method_ref": "method:1",
        "data_ref": "data:synthetic",
        "dimensions": dimensions,
        "replication_state": ReplicationState.NOT_EVALUATED,
        "contradiction_refs": (),
        "observed_effect": False,
        "uncertainty_ref": "uncertainty:1",
        "governance_effect_requested": False,
    }
    values.update(changes)
    return EvidenceRecord(**values)


def test_mechanism_only_is_admissible_for_review_only() -> None:
    result = audit_evidence(record())
    assert result.status is AdmissionStatus.ADMISSIBLE_FOR_REVIEW
    assert result.reason == "EVIDENCE_ADMISSIBLE_FOR_REVIEW_ONLY"
    assert result.evidence_tier is EvidenceTier.MECHANISM_ONLY


def test_replication_support_requires_replication_state() -> None:
    result = audit_evidence(record(evidence_tier=EvidenceTier.REPLICATION_SUPPORT))
    assert result.status is AdmissionStatus.HOLD
    assert result.reason == "REPLICATION_TIER_REQUIRES_REPLICATION_STATE"


def test_consistent_replication_support_is_admissible_for_review() -> None:
    result = audit_evidence(record(evidence_tier=EvidenceTier.REPLICATION_SUPPORT, replication_state=ReplicationState.CONSISTENT, claim_type="replication"))
    assert result.status is AdmissionStatus.ADMISSIBLE_FOR_REVIEW
    assert result.replication_state is ReplicationState.CONSISTENT


def test_divergent_replication_is_not_automatic_downgrade_but_is_reviewable() -> None:
    result = audit_evidence(record(evidence_tier=EvidenceTier.REPLICATION_SUPPORT, replication_state=ReplicationState.DIVERGENT, claim_type="replication"))
    assert result.status is AdmissionStatus.ADMISSIBLE_FOR_REVIEW
    assert result.reason == "EVIDENCE_ADMISSIBLE_FOR_REVIEW_ONLY"


def test_synthesis_with_divergence_holds() -> None:
    result = audit_evidence(record(evidence_tier=EvidenceTier.SYNTHESIS, replication_state=ReplicationState.DIVERGENT, claim_type="synthesis"))
    assert result.status is AdmissionStatus.HOLD
    assert result.reason == "DIVERGENT_SYNTHESIS_REQUIRES_REVIEW"


def test_indeterminate_replication_limits_admission() -> None:
    result = audit_evidence(record(evidence_tier=EvidenceTier.REPLICATION_SUPPORT, replication_state=ReplicationState.INDETERMINATE, claim_type="replication"))
    assert result.status is AdmissionStatus.INDETERMINATE
    assert result.reason == "REPLICATION_UNCERTAINTY_LIMITS_ADMISSION"


def test_missing_provenance_holds() -> None:
    result = audit_evidence(record(provenance_ref=None))
    assert result.status is AdmissionStatus.HOLD
    assert result.reason == "EVIDENCE_METADATA_INCOMPLETE"
    assert "provenance_ref" in result.missing_fields


def test_missing_uncertainty_holds() -> None:
    result = audit_evidence(record(uncertainty_ref=None))
    assert result.status is AdmissionStatus.HOLD
    assert "uncertainty_ref" in result.missing_fields


def test_contradictory_evidence_holds() -> None:
    result = audit_evidence(record(contradiction_refs=("evidence:2",)))
    assert result.status is AdmissionStatus.HOLD
    assert result.reason == "CONTRADICTORY_EVIDENCE_REQUIRES_REVIEW"


def test_mechanism_only_cannot_assert_observed_effect() -> None:
    result = audit_evidence(record(observed_effect=True))
    assert result.status is AdmissionStatus.HOLD
    assert result.reason == "MECHANISM_ONLY_CANNOT_ASSERT_OBSERVED_EFFECT"


def test_governance_effect_request_is_blocked() -> None:
    result = audit_evidence(record(governance_effect_requested=True))
    assert result.status is AdmissionStatus.HOLD
    assert result.reason == "EVIDENCE_ADMISSION_CANNOT_REQUEST_GOVERNANCE_EFFECT"


def test_missing_dimensions_hold() -> None:
    dimensions = EvidenceDimensions("low", None, "precise", "direct", "low")
    result = audit_evidence(record(dimensions=dimensions))
    assert result.status is AdmissionStatus.HOLD
    assert "dimensions.consistency" in result.missing_fields


def test_admission_decision_is_non_promoting() -> None:
    candidates = (
        record(),
        record(evidence_tier=EvidenceTier.SYNTHESIS, replication_state=ReplicationState.DIVERGENT, claim_type="synthesis"),
        record(contradiction_refs=("evidence:2",)),
    )
    for candidate in candidates:
        result = audit_evidence(candidate).as_dict()
        assert result["scientific_conclusion"] == "NOT_ESTABLISHED"
        assert result["canonical_effect"] == "NONE"
        assert result["deployment"] is False
        assert result["governance_effect"] == "NONE"
        assert result["subjectivity_conclusion"] == "NOT_ESTABLISHED"
        assert result["identity_continuity_conclusion"] == "NOT_ESTABLISHED"


def test_serialization_uses_enum_values() -> None:
    payload = audit_evidence(record()).as_dict()
    assert payload["status"] == "ADMISSIBLE_FOR_REVIEW"
    assert payload["evidence_tier"] == "MECHANISM_ONLY"
    assert payload["replication_state"] == "NOT_EVALUATED"
