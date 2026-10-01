from dataclasses import replace

import pytest

from codex_male_embodiment.body_state import (
    BodyEventMode,
    BodySignalEvent,
    WholeBodySyntheticEngine,
    default_whole_body_state,
)


def test_whole_body_state_contains_19_independent_channels() -> None:
    state = default_whole_body_state()
    assert len(state.signals) == 19
    updated = WholeBodySyntheticEngine().apply(
        state,
        BodySignalEvent("set-proprioception", "proprioceptive", BodyEventMode.SET, 0.7),
    )
    assert updated.signal("proprioceptive").value == pytest.approx(0.7)
    assert updated.signal("thermoregulation").value is None


def test_delta_requires_explicit_known_state() -> None:
    with pytest.raises(ValueError, match="requires SET"):
        WholeBodySyntheticEngine().apply(
            default_whole_body_state(),
            BodySignalEvent("delta", "proprioceptive", BodyEventMode.DELTA, 0.1),
        )


def test_felt_state_promotion_fails_closed() -> None:
    with pytest.raises(ValueError, match="felt-state"):
        replace(default_whole_body_state(), subjectivity="ESTABLISHED")
