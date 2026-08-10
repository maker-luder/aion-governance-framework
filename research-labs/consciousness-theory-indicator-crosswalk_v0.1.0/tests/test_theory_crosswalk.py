from aion_theory_crosswalk import IndicatorRecord, TheoryStatus, assess_indicator

def record(**overrides):
    values = dict(
        theory="GNW",
        prediction="information becomes globally available after competition",
        engineered_indicator="bounded broadcast workspace",
        observation="selected item is broadcast to registered consumers",
        alternative_explanation="ordinary routing can produce similar availability",
        source_ref="external://theory-and-project-review",
    )
    values.update(overrides)
    return IndicatorRecord(**values)

def test_complete_crosswalk_is_indicator_only():
    result = assess_indicator(record())
    assert result.status is TheoryStatus.INDICATOR_ONLY
    assert result.theory_confirmed is False
    assert result.consciousness_conclusion == "NOT_ESTABLISHED"

def test_missing_alternative_explanation_holds():
    result = assess_indicator(record(alternative_explanation=""))
    assert result.status is TheoryStatus.HOLD

def test_engineering_indicator_never_confirms_theory():
    result = assess_indicator(record(theory="IIT"))
    assert "LIKE_MECHANISM_EVIDENCE" in result.mechanism_evidence
    assert result.theory_confirmed is False
