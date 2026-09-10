from aion_subjectivity_pipeline.locus import (
    AdmissionDisposition,
    ClaimTarget,
    EvidenceLocus,
    LocusAdmissionEngine,
    LocusBridgeHypothesis,
    LocusEvidence,
)


def evidence(locus: EvidenceLocus) -> LocusEvidence:
    return LocusEvidence(
        evidence_id=f"e-{locus.value.lower()}",
        locus=locus,
        description="synthetic bounded observation",
        source_refs=("synthetic:fixture",),
    )


def test_model_evidence_cannot_silently_become_system_evidence() -> None:
    result = LocusAdmissionEngine().assess(
        evidence(EvidenceLocus.MODEL),
        target=ClaimTarget.SYSTEM_PROPERTY,
    )
    assert result.disposition is AdmissionDisposition.HOLD
    assert result.direct_locus_match is False
    assert "CROSS_LOCUS_PROMOTION_REQUIRES_EXPLICIT_BRIDGE_HYPOTHESIS" in result.reasons


def test_system_evidence_can_support_bounded_system_engineering_claim() -> None:
    result = LocusAdmissionEngine().assess(
        evidence(EvidenceLocus.SYSTEM),
        target=ClaimTarget.SYSTEM_PROPERTY,
    )
    assert result.disposition is AdmissionDisposition.ADMISSIBLE_FOR_ENGINEERING_CLAIM
    assert result.direct_locus_match is True
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"


def test_relational_pattern_does_not_establish_subjectivity() -> None:
    result = LocusAdmissionEngine().assess(
        evidence(EvidenceLocus.RELATIONAL),
        target=ClaimTarget.SUBJECTIVITY,
    )
    assert result.disposition is AdmissionDisposition.HOLD
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert result.phenomenal_experience_conclusion == "NOT_ESTABLISHED"


def test_observer_attribution_is_not_internal_property_evidence() -> None:
    result = LocusAdmissionEngine().assess(
        evidence(EvidenceLocus.OBSERVER_ATTRIBUTION),
        target=ClaimTarget.MODEL_PROPERTY,
    )
    assert result.disposition is AdmissionDisposition.HOLD
    assert "OBSERVER_ATTRIBUTION_IS_NOT_INTERNAL_PROPERTY_EVIDENCE" in result.reasons


def test_unknown_locus_fails_closed() -> None:
    result = LocusAdmissionEngine().assess(
        evidence(EvidenceLocus.UNKNOWN),
        target=ClaimTarget.RELATIONAL_PROPERTY,
    )
    assert result.disposition is AdmissionDisposition.HOLD
    assert "UNKNOWN_LOCUS_FAILS_CLOSED" in result.reasons


def test_explicit_bridge_is_candidate_not_cross_level_proof() -> None:
    bridge = LocusBridgeHypothesis(
        bridge_id="b1",
        from_locus=EvidenceLocus.MODEL,
        to_locus=EvidenceLocus.SYSTEM,
        mechanism="a declared scaffold repeatedly propagates a model-level state into system-level selection",
        falsifier="matched ablation of the scaffold removes the system-level effect",
        preregistration_ref="synthetic:preregistered-bridge",
    )
    result = LocusAdmissionEngine().assess(
        evidence(EvidenceLocus.MODEL),
        target=ClaimTarget.SYSTEM_PROPERTY,
        bridge=bridge,
    )
    assert result.disposition is AdmissionDisposition.RESEARCH_CANDIDATE
    assert result.bridge_used is True
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert "BRIDGE_IS_RESEARCH_CANDIDATE_NOT_LEVEL_EQUIVALENCE" in result.reasons


def test_wrong_bridge_fails_closed() -> None:
    bridge = LocusBridgeHypothesis(
        bridge_id="b2",
        from_locus=EvidenceLocus.SCAFFOLD,
        to_locus=EvidenceLocus.RELATIONAL,
        mechanism="synthetic mismatch",
        falsifier="synthetic mismatch falsifier",
        preregistration_ref="synthetic:wrong-bridge",
    )
    result = LocusAdmissionEngine().assess(
        evidence(EvidenceLocus.MODEL),
        target=ClaimTarget.SYSTEM_PROPERTY,
        bridge=bridge,
    )
    assert result.disposition is AdmissionDisposition.HOLD
    assert "BRIDGE_LOCUS_MISMATCH" in result.reasons
