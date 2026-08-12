import pytest

from motivational_signal_primitives import MotivationalSignalPrimitive, MotivationalSignalSet


def signal(**overrides):
    values = {
        "signal_id": "sig-1",
        "subject_ref": "subject-1",
        "context_ref": "context-1",
        "source_event_id": "event-1",
        "signal_kind": "research-signal",
        "intensity": 0.7,
        "approach_bias": 0.8,
        "avoidance_bias": 0.2,
        "uncertainty": 0.1,
        "evidence_refs": ("evidence-1",),
        "provenance_refs": ("provenance-1",),
    }
    values.update(overrides)
    return MotivationalSignalPrimitive(**values)


def test_signal_requires_evidence_and_provenance():
    with pytest.raises(ValueError):
        signal(evidence_refs=())
    with pytest.raises(ValueError):
        signal(provenance_refs=())


def test_signal_bounds():
    with pytest.raises(ValueError):
        signal(intensity=1.1)
    with pytest.raises(ValueError):
        signal(avoidance_bias=-0.1)


def test_signal_nonclaims_are_locked():
    with pytest.raises(ValueError):
        signal(felt_experience_claim="ESTABLISHED")
    with pytest.raises(ValueError):
        signal(motivational_authority_claim="ESTABLISHED")


def test_signed_bias_preserves_direction():
    assert signal(approach_bias=0.8, avoidance_bias=0.2).signed_action_bias == pytest.approx(0.6)
    assert signal(approach_bias=0.2, avoidance_bias=0.8).signed_action_bias == pytest.approx(-0.6)


def test_coactivation_does_not_assert_conflict():
    assert signal(approach_bias=0.99, avoidance_bias=0.01).coactivation == pytest.approx(0.01)


def test_signal_set_rejects_duplicate_ids():
    first = signal()
    second = signal()
    with pytest.raises(ValueError):
        MotivationalSignalSet("set-1", "subject-1", "context-1", (first, second))


def test_signal_set_enforces_subject_and_context_binding():
    with pytest.raises(ValueError):
        MotivationalSignalSet("set-1", "subject-2", "context-1", (signal(),))
    with pytest.raises(ValueError):
        MotivationalSignalSet("set-1", "subject-1", "context-2", (signal(),))


def test_empty_signal_set_is_valid_for_control_conditions():
    state = MotivationalSignalSet("set-1", "subject-1", "context-1", ())
    assert state.total_approach_bias() == 0.0
    assert state.total_avoidance_bias() == 0.0
    assert state.signed_action_bias() == 0.0


def test_signal_set_aggregates_without_stale_summary_fields():
    first = signal(signal_id="a", approach_bias=0.8, avoidance_bias=0.1)
    second = signal(signal_id="b", approach_bias=0.2, avoidance_bias=0.6)
    state = MotivationalSignalSet("set-1", "subject-1", "context-1", (first, second))
    assert state.total_approach_bias() == pytest.approx(1.0)
    assert state.total_avoidance_bias() == pytest.approx(0.7)
    assert state.signed_action_bias() == pytest.approx(0.3)
