from __future__ import annotations

from dataclasses import FrozenInstanceError
import pytest

from aion_triadic_state import ConflictStatus, NormativeConstraint, NormativeState, SelfWorldModel, canonical_hash, motivation_view_from_existing
from conftest import make_snapshot


def test_snapshot_is_immutable_and_fingerprint_deterministic() -> None:
    value = make_snapshot()
    assert value.fingerprint == make_snapshot().fingerprint
    with pytest.raises(FrozenInstanceError):
        value.logical_step = 4  # type: ignore[misc]


def test_snapshot_binds_three_channel_fingerprints() -> None:
    value = make_snapshot()
    assert len({value.motivational_fingerprint, value.self_world_fingerprint, value.normative_fingerprint}) == 3
    assert all(len(item) == 64 for item in (value.motivational_fingerprint, value.self_world_fingerprint, value.normative_fingerprint))


def test_cross_subject_snapshot_fails_closed() -> None:
    value = make_snapshot()
    foreign = SelfWorldModel("foreign", "ASTRA", "ctx", (), (), (), 0.5, 0.5)
    with pytest.raises(ValueError, match="same subject"):
        type(value)(value.state_id, value.subject_ref, value.context_ref, value.logical_step, value.predecessor_snapshot_ref, value.motivational_state, foreign, value.normative_state, value.evidence_refs, value.provenance_refs)


def test_normative_constraint_cannot_grant_permission() -> None:
    with pytest.raises(ValueError, match="never grant permission"):
        NormativeConstraint("ALLOW", "bad", "repo", 1, True, ConflictStatus.NONE, 0.0, permission_grant=True)


def test_normative_state_cannot_grant_permission() -> None:
    constraint = NormativeConstraint("NO_WRITE", "policy", "repo", 90, True, ConflictStatus.NONE, 0.0)
    with pytest.raises(ValueError, match="never grants"):
        NormativeState("n", "AION", "ctx", (constraint,), ("p",), permission_grant=True)


def test_self_world_model_uncertainty_bounded() -> None:
    with pytest.raises(ValueError, match="uncertainty"):
        SelfWorldModel("m", "AION", "ctx", (), (), (), 1.1, 0.5)


def test_canonical_hash_recurses_nested_values() -> None:
    value = make_snapshot()
    assert canonical_hash({"items": (value.normative_state.constraints,)}) == canonical_hash({"items": (value.normative_state.constraints,)})


def test_motivation_adapter_reuses_existing_structure_without_authority() -> None:
    class Signal:
        evidence_refs = ("e1", "e2")
        salience = 0.5
    class Existing:
        state_id = "m"; subject_ref = "AION"; context_ref = "ctx"; signals = (Signal(),); canonical_effect = "NONE"; action_authority = "NONE"
    adapted = motivation_view_from_existing(Existing())
    assert adapted.source_model == "aion_affective_motivation.MotivationalState"
    assert adapted.action_authority == "NONE"
    assert adapted.evidence_refs == ("e1", "e2")


def test_motivation_adapter_rejects_authoritative_source() -> None:
    class Existing:
        state_id = "m"; subject_ref = "AION"; context_ref = "ctx"; signals = (1,); canonical_effect = "PROMOTE"; action_authority = "NONE"
    with pytest.raises(ValueError):
        motivation_view_from_existing(Existing())
