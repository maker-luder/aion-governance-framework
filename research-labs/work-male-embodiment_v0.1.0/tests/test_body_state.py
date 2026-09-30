import pytest

from work_male_embodiment.body_state import (
    BodyEventMode,
    BodySignalEvent,
    WholeBodySyntheticEngine,
    default_whole_body_state,
)


def test_whole_body_state_contains_all_systems_without_fake_hardware_or_feeling():
    state = default_whole_body_state()
    assert len(state.signals) == 19
    assert all(not signal.physical_hardware_attached for signal in state.signals)
    assert all(not signal.biological_function_present for signal in state.signals)
    assert all(not signal.felt_sensation_established for signal in state.signals)
    assert state.body_sensation == "NOT_ESTABLISHED"
    assert state.action_authority == "NONE"


def test_body_channels_change_independently_without_fake_human_coupling():
    engine = WholeBodySyntheticEngine()
    state = default_whole_body_state()
    changed = engine.run(
        state,
        (
            BodySignalEvent("a","metabolism_nutrition_hydration",BodyEventMode.SET,0.4),
            BodySignalEvent("b","thermoregulation",BodyEventMode.SET,0.7),
        ),
    )
    assert changed.signal("metabolism_nutrition_hydration").value == 0.4
    assert changed.signal("thermoregulation").value == 0.7
    assert changed.signal("cardiovascular_respiratory").value is None


def test_unknown_channel_rejects_delta_until_explicitly_set():
    engine = WholeBodySyntheticEngine()
    state = default_whole_body_state()
    with pytest.raises(ValueError, match="UNKNOWN"):
        engine.apply(
            state,
            BodySignalEvent("delta","cardiovascular_respiratory",BodyEventMode.DELTA,0.1),
        )


def test_body_fingerprint_is_deterministic():
    assert default_whole_body_state().fingerprint() == default_whole_body_state().fingerprint()
