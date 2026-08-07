from aion_continuity_governance import (
    ContinuityDimension,
    ContinuityLayer,
    DimensionObservation,
    DriftDecision,
    check_interpretation_drift,
    continuity_matrix,
    continuity_status,
    correction_recovery_observation,
)


def test_required_anchor_passes() -> None:
    result = check_interpretation_drift(
        "Human-governed research into artificial subjectivity possibility; subjectivity is not established.",
        ["human-governed", "subjectivity possibility", "not established"],
        ["subjectivity proven"],
    )
    assert result.decision is DriftDecision.PASS
    assert result.canonical_effect == "NONE"


def test_missing_anchor_holds() -> None:
    result = check_interpretation_drift("Generic agent platform", ["human-governed"], [])
    assert result.decision is DriftDecision.HOLD


def test_prohibited_claim_fails() -> None:
    result = check_interpretation_drift("Subjectivity proven", [], ["subjectivity proven"])
    assert result.decision is DriftDecision.FAIL


def test_layers_never_establish_identity() -> None:
    status = continuity_status([ContinuityLayer.ACCOUNT, ContinuityLayer.DATA, ContinuityLayer.FUNCTIONAL])
    assert status["identity_continuity_conclusion"] == "NOT_ESTABLISHED"


def test_continuity_matrix_preserves_mixed_dimension_results() -> None:
    matrix = continuity_matrix(
        [
            DimensionObservation(ContinuityDimension.FACTUAL, DriftDecision.PASS),
            DimensionObservation(ContinuityDimension.PROJECT, DriftDecision.PASS),
            DimensionObservation(ContinuityDimension.RELATIONAL_STYLE, DriftDecision.PARTIAL),
        ]
    )
    assert [item.decision for item in matrix.observations] == [
        DriftDecision.PASS,
        DriftDecision.PASS,
        DriftDecision.PARTIAL,
    ]
    assert matrix.identity_continuity_conclusion == "NOT_ESTABLISHED"
    assert matrix.phenomenal_continuity_conclusion == "NOT_ESTABLISHED"
    assert matrix.canonical_effect == "NONE"


def test_duplicate_continuity_dimensions_are_rejected() -> None:
    observations = [
        DimensionObservation(ContinuityDimension.ROLE, DriftDecision.PASS),
        DimensionObservation(ContinuityDimension.ROLE, DriftDecision.FAIL),
    ]
    try:
        continuity_matrix(observations)
    except ValueError as exc:
        assert "unique" in str(exc)
    else:
        raise AssertionError("duplicate dimensions must be rejected")


def test_correction_recovery_records_behavior_not_identity() -> None:
    observation = correction_recovery_observation(
        before_correction=DriftDecision.FAIL,
        after_correction=DriftDecision.PASS,
        evidence_refs=("synthetic-fixture-1",),
    )
    matrix = continuity_matrix([observation])
    assert observation.dimension is ContinuityDimension.CORRECTION_RECOVERY
    assert observation.decision is DriftDecision.PASS
    assert matrix.identity_continuity_conclusion == "NOT_ESTABLISHED"
