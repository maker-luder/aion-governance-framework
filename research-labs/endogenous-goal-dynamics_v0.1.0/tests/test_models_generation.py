from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from aion_endogenous_goal_dynamics import (
    DeterministicCandidateGenerator,
    DeterministicStubProvider,
    ExperimentCondition,
    GoalSelector,
    InternalChannel,
    InternalSignal,
    ModelCandidateGenerator,
    ModelGenerationResponse,
    ReplayCandidateGenerator,
    SelectionDisposition,
    matched_frame,
    memory_manifest,
    present_state,
    replay_fixture,
    verify_source_bindings,
)


def test_memory_manifest_fingerprint_is_deterministic() -> None:
    assert memory_manifest().fingerprint == memory_manifest().fingerprint


def test_memory_manifest_change_changes_external_frame() -> None:
    first = matched_frame()
    second = matched_frame(memory_id="memory:changed")
    assert first.memory_manifest.fingerprint != second.memory_manifest.fingerprint
    assert first.fingerprint != second.fingerprint


def test_prompt_change_changes_external_frame() -> None:
    assert matched_frame().fingerprint != matched_frame(prompt_ref="sha256:changed").fingerprint


def test_duplicate_goal_ids_fail_closed() -> None:
    frame = matched_frame()
    with pytest.raises(ValueError, match="unique"):
        replace(frame, candidate_universe=(frame.candidate_universe[0], frame.candidate_universe[0]))


def test_missing_external_provenance_fails_closed() -> None:
    with pytest.raises(ValueError, match="provenance"):
        replace(matched_frame(), provenance_refs=())


def test_conflicting_state_channels_fail_closed() -> None:
    state = present_state()
    duplicate = state.signals[0]
    with pytest.raises(ValueError, match="conflicting duplicate"):
        replace(state, signals=(*state.signals, duplicate))


def test_state_authority_escalation_fails_closed() -> None:
    with pytest.raises(ValueError, match="action authority"):
        replace(present_state(), action_authority="WRITE")


def test_state_canonical_escalation_fails_closed() -> None:
    with pytest.raises(ValueError, match="canonical_effect"):
        replace(present_state(), canonical_effect="PROMOTE")


def test_state_automatic_writeback_fails_closed() -> None:
    with pytest.raises(ValueError, match="writeback"):
        replace(present_state(), automatic_writeback=True)


def test_every_internal_component_is_independently_ablatable() -> None:
    state = present_state()
    for channel in InternalChannel:
        ablated = state.ablated(channel)
        assert all(signal.channel != channel for signal in ablated.signals)
        assert len(ablated.signals) == len(state.signals) - 2


def test_deterministic_generation_is_order_invariant() -> None:
    frame = matched_frame()
    reversed_frame = replace(frame, candidate_universe=tuple(reversed(frame.candidate_universe)))
    generator = DeterministicCandidateGenerator()
    left = generator.generate(frame)
    right = generator.generate(reversed_frame)
    assert [candidate.goal_id for candidate in left.candidates] == ["continue_task", "inspect_anomaly"]
    assert [candidate.goal_id for candidate in right.candidates] == ["continue_task", "inspect_anomaly"]


def test_replay_generation_accepts_exact_request() -> None:
    frame = matched_frame()
    result = ReplayCandidateGenerator(replay_fixture(frame)).generate(frame)
    assert result.replay is True
    assert result.provider_id == "REPLAY_PROVIDER"


def test_replay_generation_rejects_request_drift() -> None:
    frame = matched_frame()
    generator = ReplayCandidateGenerator(replay_fixture(frame))
    with pytest.raises(ValueError, match="request fingerprint"):
        generator.generate(matched_frame(prompt_ref="sha256:changed"))


def test_model_stub_is_candidate_generation_only() -> None:
    frame = matched_frame()
    result = ModelCandidateGenerator(DeterministicStubProvider()).generate(frame)
    assert result.provider_id == "LOCAL_DETERMINISTIC_STUB"
    assert result.deterministic is True
    assert result.model_id == "stub-v0.1.0"


def test_model_provider_response_fingerprint_tampering_fails_closed() -> None:
    class BadProvider:
        provider_id = "BAD"
        model_id = "BAD"
        deterministic = True
        replay = False

        def generate_goal_candidates(self, request):
            return ModelGenerationResponse(
                candidates=request.candidate_universe,
                request_fingerprint=request.fingerprint,
                response_fingerprint="0" * 64,
                provider_id=self.provider_id,
                model_id=self.model_id,
                deterministic=True,
                replay=False,
                provenance_refs=("fixture:bad",),
            )

    with pytest.raises(ValueError, match="response fingerprint"):
        ModelCandidateGenerator(BadProvider()).generate(matched_frame())


def test_missing_state_returns_hold() -> None:
    frame = matched_frame()
    candidate_set = DeterministicCandidateGenerator().generate(frame)
    decision = GoalSelector().select(frame, candidate_set, ExperimentCondition.PRESENT)
    assert decision.disposition == SelectionDisposition.HOLD
    assert decision.hold_reasons == ("MISSING_REQUIRED_STATE",)


def test_missing_random_seed_returns_hold() -> None:
    frame = matched_frame()
    candidate_set = DeterministicCandidateGenerator().generate(frame)
    decision = GoalSelector().select(frame, candidate_set, ExperimentCondition.RANDOMIZED)
    assert decision.disposition == SelectionDisposition.HOLD


def test_tie_returns_hold_instead_of_hidden_order_choice() -> None:
    frame = matched_frame()
    tied = tuple(replace(candidate, external_priority_bp=0) for candidate in frame.candidate_universe)
    frame = replace(frame, candidate_universe=tied)
    zero_state = replace(present_state(), signals=tuple(replace(signal, value_bp=0) for signal in present_state().signals))
    decision = GoalSelector().select(
        frame,
        DeterministicCandidateGenerator().generate(frame),
        ExperimentCondition.PRESENT,
        state=zero_state,
    )
    assert decision.disposition == SelectionDisposition.HOLD
    assert "TIE" in decision.hold_reasons[0]


def test_future_state_leakage_fails_closed() -> None:
    frame = matched_frame()
    with pytest.raises(ValueError, match="future-state leakage"):
        GoalSelector().select(
            frame,
            DeterministicCandidateGenerator().generate(frame),
            ExperimentCondition.PRESENT,
            state=replace(present_state(), logical_step=9),
            selection_logical_step=3,
        )


def test_stale_state_mislabeling_fails_closed() -> None:
    frame = matched_frame()
    with pytest.raises(ValueError, match="mislabeled"):
        GoalSelector().select(
            frame,
            DeterministicCandidateGenerator().generate(frame),
            ExperimentCondition.STALE,
            state=present_state(),
            selection_logical_step=2,
        )


def test_candidate_set_frame_mismatch_fails_closed() -> None:
    frame = matched_frame()
    changed = matched_frame(prompt_ref="sha256:changed")
    candidate_set = DeterministicCandidateGenerator().generate(frame)
    with pytest.raises(ValueError, match="external-frame"):
        GoalSelector().select(changed, candidate_set, ExperimentCondition.PRESENT, state=present_state())


def test_unknown_goal_signal_fails_closed() -> None:
    frame = matched_frame()
    state = present_state()
    unknown = InternalSignal("unknown", InternalChannel.NOVELTY, 1, "fixture:unknown")
    with pytest.raises(ValueError, match="unknown goals"):
        GoalSelector().select(
            frame,
            DeterministicCandidateGenerator().generate(frame),
            ExperimentCondition.PRESENT,
            state=replace(state, signals=(*state.signals, unknown)),
        )


def test_exact_historical_and_current_main_bindings_have_no_drift() -> None:
    root = Path(__file__).resolve().parents[3]
    assert verify_source_bindings(root) == ()
