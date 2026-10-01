from dataclasses import replace

import pytest

from aion_astra_twin_embodiment.body_state import (
    BodyEventMode,
    BodySignalEvent,
    WholeBodySyntheticEngine,
    default_whole_body_state,
)


def test_aion_astra_have_separate_19_system_states() -> None:
    aion = default_whole_body_state("AION")
    astra = default_whole_body_state("ASTRA")
    assert len(aion.signals) == len(astra.signals) == 19
    assert aion.body_id != astra.body_id
    assert aion.fingerprint() != astra.fingerprint()


def test_signal_update_does_not_cross_twin_state() -> None:
    engine = WholeBodySyntheticEngine()
    aion = engine.apply(
        default_whole_body_state("AION"),
        BodySignalEvent("set", "proprioceptive", BodyEventMode.SET, 0.6),
    )
    astra = default_whole_body_state("ASTRA")
    assert aion.signal("proprioceptive").value == pytest.approx(0.6)
    assert astra.signal("proprioceptive").value is None


def test_felt_body_promotion_fails_closed() -> None:
    with pytest.raises(ValueError, match="felt-state"):
        replace(default_whole_body_state("AION"), body_ownership_experience="ESTABLISHED")
