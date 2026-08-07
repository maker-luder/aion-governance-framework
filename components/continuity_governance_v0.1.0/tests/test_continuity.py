from aion_continuity_governance import ContinuityLayer, DriftDecision, check_interpretation_drift, continuity_status


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
