from __future__ import annotations

from dataclasses import replace
import pytest

from aion_triadic_state import SelfWorldModel, StateChannel, TriadicDelta, apply_transition, apply_transition_batch, verify_transition_chain
from conftest import make_snapshot


def test_single_channel_transition_preserves_predecessor() -> None:
    before = make_snapshot()
    replacement = replace(before.self_world_model, model_id="sw-1", uncertainty=0.1)
    result = apply_transition(before, TriadicDelta(StateChannel.SELF_WORLD_MODEL, replacement, "correction", ("e:new",)), transition_id="t1", sequence=1, event_ref="event:1", outcome_ref="outcome:1", correction_ref="correction:1", provenance_refs=("prov:1",))
    assert result.snapshot.predecessor_snapshot_ref == before.fingerprint
    assert result.snapshot.motivational_state == before.motivational_state
    assert result.snapshot.normative_state == before.normative_state
    assert result.event.changed_channel is StateChannel.SELF_WORLD_MODEL
    assert result.event.action_authority == "NONE"


def test_transition_rejects_cross_subject_substitution() -> None:
    before = make_snapshot(); replacement = SelfWorldModel("x", "ASTRA", "ctx", (), (), (), 0.2, 0.8)
    with pytest.raises(ValueError, match="cross-subject"):
        apply_transition(before, TriadicDelta(StateChannel.SELF_WORLD_MODEL, replacement, "bad"), transition_id="t", sequence=1, event_ref="e", outcome_ref="o", correction_ref="", provenance_refs=())


def test_transition_rejects_cross_context_substitution() -> None:
    before = make_snapshot(); replacement = SelfWorldModel("x", "AION", "other", (), (), (), 0.2, 0.8)
    with pytest.raises(ValueError, match="cross-context"):
        apply_transition(before, TriadicDelta(StateChannel.SELF_WORLD_MODEL, replacement, "bad"), transition_id="t", sequence=1, event_ref="e", outcome_ref="o", correction_ref="", provenance_refs=())


def test_transition_rejects_declared_channel_type_mismatch() -> None:
    before = make_snapshot()
    with pytest.raises(TypeError, match="declared channel"):
        apply_transition(before, TriadicDelta(StateChannel.NORMATIVE_STATE, before.self_world_model, "bad"), transition_id="t", sequence=1, event_ref="e", outcome_ref="o", correction_ref="", provenance_refs=())


def test_batch_rejects_duplicate_and_multi_channel_deltas() -> None:
    before = make_snapshot(); replacement = replace(before.self_world_model, model_id="new"); delta = TriadicDelta(StateChannel.SELF_WORLD_MODEL, replacement, "one")
    with pytest.raises(ValueError, match="duplicate"):
        apply_transition_batch(before, (delta, delta), transition_id="t", sequence=1, event_ref="e", outcome_ref="o", correction_ref="", provenance_refs=())
    other = TriadicDelta(StateChannel.MOTIVATIONAL_STATE, replace(before.motivational_state, state_id="new"), "two")
    with pytest.raises(ValueError, match="exactly one"):
        apply_transition_batch(before, (delta, other), transition_id="t", sequence=1, event_ref="e", outcome_ref="o", correction_ref="", provenance_refs=())


def test_transition_chain_verifies_and_tamper_breaks() -> None:
    before = make_snapshot()
    first = apply_transition(before, TriadicDelta(StateChannel.SELF_WORLD_MODEL, replace(before.self_world_model, model_id="s1"), "r1"), transition_id="t1", sequence=1, event_ref="e1", outcome_ref="o1", correction_ref="", provenance_refs=())
    second = apply_transition(first.snapshot, TriadicDelta(StateChannel.MOTIVATIONAL_STATE, replace(first.snapshot.motivational_state, state_id="m1"), "r2"), transition_id="t2", sequence=2, event_ref="e2", outcome_ref="o2", correction_ref="", provenance_refs=(), previous_event_hash=first.event.event_hash)
    assert verify_transition_chain((first.event, second.event))
    assert not verify_transition_chain((replace(first.event, event_hash="0" * 64), second.event))
