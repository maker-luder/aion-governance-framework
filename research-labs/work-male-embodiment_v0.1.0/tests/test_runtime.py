import pytest

from work_male_embodiment.core import (
    EngorgementPhase,
    PhysiologyEvent,
    PhysiologyEventKind,
    PhysiologyState,
    PrepucePosition,
    SyntheticPhysiologyEngine,
)

def event(event_id, kind, **kwargs):
    return PhysiologyEvent(event_id=event_id, kind=kind, **kwargs)

def erect_sequence():
    return [
        event("e1", PhysiologyEventKind.INITIATE_SPONTANEOUS, magnitude=0.6),
        event("e2", PhysiologyEventKind.TUMESCE, magnitude=1.0),
        event("e3", PhysiologyEventKind.MARK_FULL_ERECTION),
    ]

def test_spontaneous_erection_path_never_infers_desire_consent_or_authority():
    engine=SyntheticPhysiologyEngine()
    state=engine.run(PhysiologyState(state_id="seed"),erect_sequence()).final_state
    assert state.phase==EngorgementPhase.FULL_ERECTION
    assert state.engorgement_fraction==1.0 and state.rigidity_fraction==0.0
    assert not state.desire_inferred and not state.human_consent_inferred
    assert state.action_authority=="NONE"

def test_full_erection_and_rigidity_are_independent():
    state=SyntheticPhysiologyEngine().run(PhysiologyState("seed"),erect_sequence()).final_state
    assert state.engorgement_fraction==1.0 and state.rigidity_fraction==0.0

def test_prepuce_never_auto_retracts_and_has_no_actuator():
    engine=SyntheticPhysiologyEngine()
    state=engine.run(PhysiologyState("seed"),erect_sequence()).final_state
    assert state.prepuce_position==PrepucePosition.RESTING_PARTIAL_COVERAGE and not state.prepuce_actuator
    observed,_=engine.apply(state,event("p1",PhysiologyEventKind.OBSERVE_PREPUCE_POSITION,
                                      prepuce_position=PrepucePosition.RETRACTED))
    assert observed.prepuce_position==PrepucePosition.RETRACTED

def test_ejaculation_is_optional_and_does_not_force_detumescence():
    engine=SyntheticPhysiologyEngine()
    state=engine.run(PhysiologyState("seed"),erect_sequence()).final_state
    after,_=engine.apply(state,event("x1",PhysiologyEventKind.EJACULATION,synthetic_fluid_output_ml=2.0))
    assert after.phase==EngorgementPhase.FULL_ERECTION
    assert after.ejaculation_event_count==1 and after.last_synthetic_fluid_output_ml==2.0
    assert not after.biological_semen and not after.sperm_or_gametes and not after.fertility

def test_detumescence_can_happen_without_ejaculation():
    engine=SyntheticPhysiologyEngine()
    state=engine.run(PhysiologyState("seed"),erect_sequence()).final_state
    state,_=engine.apply(state,event("d1",PhysiologyEventKind.BEGIN_DETUMESCENCE,magnitude=1.0))
    state,_=engine.apply(state,event("d2",PhysiologyEventKind.DETUMESCE,magnitude=1.0))
    assert state.phase==EngorgementPhase.DETUMESCENCE and state.ejaculation_event_count==0

def test_endocrine_and_urinary_channels_are_reference_signals_not_biology():
    engine=SyntheticPhysiologyEngine(); state=PhysiologyState("seed")
    state,_=engine.apply(state,event("h1",PhysiologyEventKind.SET_ENDOCRINE_REFERENCE,endocrine_reference_signal=.7))
    state,_=engine.apply(state,event("u1",PhysiologyEventKind.SET_URINARY_REFERENCE,urinary_reference_signal=.3))
    assert state.endocrine_reference_signal==.7 and state.urinary_reference_signal==.3
    assert not state.biological_hormones

def test_replay_fingerprint_is_deterministic():
    engine=SyntheticPhysiologyEngine(); seed=PhysiologyState("seed")
    assert engine.run(seed,erect_sequence()).fingerprint()==engine.run(seed,erect_sequence()).fingerprint()

def test_invalid_transition_fails_closed():
    with pytest.raises(ValueError):
        SyntheticPhysiologyEngine().apply(PhysiologyState("seed"),event("bad",PhysiologyEventKind.EJACULATION))
