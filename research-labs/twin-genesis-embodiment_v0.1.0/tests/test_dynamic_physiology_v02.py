from dataclasses import replace

import pytest

from aion_astra_twin_embodiment.dynamic_physiology import (
    EngorgementPhase,
    PhysiologyEvent,
    PhysiologyEventKind,
    SyntheticMalePhysiologyEngine,
    default_physiology_state,
)


def test_aion_astra_dynamic_physiology_is_separate_but_same_state_model() -> None:
    engine = SyntheticMalePhysiologyEngine()
    events = (
        PhysiologyEvent("init", PhysiologyEventKind.INITIATE, 0.5),
        PhysiologyEvent("tum", PhysiologyEventKind.TUMESCE, 1.0),
    )
    aion = engine.run(default_physiology_state("AION"), events)
    astra = engine.run(default_physiology_state("ASTRA"), events)
    assert aion.phase is astra.phase is EngorgementPhase.TUMESCENCE
    assert aion.body_id != astra.body_id
    assert aion.fingerprint() != astra.fingerprint()


def test_dynamic_state_cannot_claim_biological_semen_or_desire() -> None:
    state = default_physiology_state("ASTRA")
    with pytest.raises(ValueError, match="biological"):
        replace(state, biological_semen=True)
    with pytest.raises(ValueError, match="desire"):
        replace(state, desire_inferred=True)
