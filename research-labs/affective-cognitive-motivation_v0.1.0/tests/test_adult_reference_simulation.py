from dataclasses import replace

import pytest

from aion_affective_motivation.adult_reference import (
    AdultMaleSexualReferenceState,
    DesireOnsetContext,
    ReferenceEstimate,
    TargetScope,
)
from aion_affective_motivation.adult_reference_simulation import (
    AdultReferenceSimulationEngine,
    AdultReferenceSimulationHarness,
    AdultReferenceSimulationPolicy,
    AdultReferenceSyntheticEvent,
    adult_reference_event_payload,
    build_snapshot_receipts,
    verify_snapshot_receipts,
)


def estimate(
    level: float | None,
    *,
    uncertainty: float = 0.2,
    source_ref: str = "SYNTHETIC_SEED",
    context_ref: str = "seed-context",
    time_window_ref: str = "seed-window",
) -> ReferenceEstimate:
    if level is None:
        uncertainty = 1.0
    return ReferenceEstimate(
        reference_level=level,
        uncertainty=uncertainty,
        source_ref=source_ref,
        context_ref=context_ref,
        time_window_ref=time_window_ref,
    )


def numeric_state(
    *,
    state_id: str = "adult-seed",
    subject_ref: str = "Teacher",
    excitation: float = 0.5,
    inhibition: float = 0.5,
    disposition: float = 0.5,
    episode: float = 0.5,
    onset: DesireOnsetContext = DesireOnsetContext.UNKNOWN,
    target_scope: TargetScope = TargetScope.UNKNOWN,
) -> AdultMaleSexualReferenceState:
    return AdultMaleSexualReferenceState(
        state_id=state_id,
        subject_ref=subject_ref,
        context_ref="seed-context",
        desire_onset_context=onset,
        excitation_reference=estimate(excitation),
        inhibition_reference=estimate(inhibition),
        disposition_reference=estimate(disposition),
        episode_state_reference=estimate(episode),
        target_scope=target_scope,
        provenance_refs=("PR#236", "SYNTHETIC_SEED"),
    )


def event(
    *,
    event_id: str = "synthetic-event-1",
    excitation_drive: float = 0.0,
    inhibition_drive: float = 0.0,
    episode_drive: float = 0.0,
    disposition_observation_drive: float = 0.0,
    onset: DesireOnsetContext = DesireOnsetContext.UNKNOWN,
    target_scope: TargetScope = TargetScope.UNKNOWN,
    uncertainty: float = 0.1,
) -> AdultReferenceSyntheticEvent:
    return AdultReferenceSyntheticEvent(
        event_id=event_id,
        context_ref=f"context:{event_id}",
        time_window_ref=f"window:{event_id}",
        excitation_drive=excitation_drive,
        inhibition_drive=inhibition_drive,
        episode_drive=episode_drive,
        disposition_observation_drive=disposition_observation_drive,
        onset_context_evidence=onset,
        target_scope=target_scope,
        uncertainty=uncertainty,
        provenance_refs=("PR#236", f"fixture:{event_id}"),
    )


def unknown_state() -> AdultMaleSexualReferenceState:
    unknown = estimate(None)
    return AdultMaleSexualReferenceState(
        state_id="unknown-seed",
        subject_ref="Teacher",
        context_ref="seed-context",
        desire_onset_context=DesireOnsetContext.UNKNOWN,
        excitation_reference=unknown,
        inhibition_reference=unknown,
        disposition_reference=unknown,
        episode_state_reference=unknown,
        target_scope=TargetScope.UNKNOWN,
        provenance_refs=("PR#236", "UNKNOWN_SEED"),
    )


def test_simulation_refuses_to_invent_numeric_adult_male_default() -> None:
    engine = AdultReferenceSimulationEngine()
    with pytest.raises(ValueError, match="UNKNOWN cannot be silently converted"):
        engine.step(
            unknown_state(),
            event(excitation_drive=1.0),
            successor_state_id="successor",
        )


def test_excitation_and_inhibition_update_independently() -> None:
    engine = AdultReferenceSimulationEngine()
    successor, trace = engine.step(
        numeric_state(excitation=0.8, inhibition=0.8),
        event(excitation_drive=1.0, inhibition_drive=-1.0),
        successor_state_id="successor",
    )

    assert successor.excitation_reference.reference_level == pytest.approx(1.0)
    assert successor.inhibition_reference.reference_level == pytest.approx(0.55)
    channels = {item.channel: item for item in trace.channels}
    assert channels["EXCITATION_REFERENCE"].drive == 1.0
    assert channels["INHIBITION_REFERENCE"].drive == -1.0


def test_excitation_and_inhibition_can_both_increase() -> None:
    successor, _ = AdultReferenceSimulationEngine().step(
        numeric_state(excitation=0.4, inhibition=0.4),
        event(excitation_drive=0.8, inhibition_drive=0.8),
        successor_state_id="successor",
    )

    assert successor.excitation_reference.reference_level == pytest.approx(0.6)
    assert successor.inhibition_reference.reference_level == pytest.approx(0.6)


def test_disposition_changes_more_slowly_than_episode_under_equal_toy_drive() -> None:
    successor, _ = AdultReferenceSimulationEngine().step(
        numeric_state(disposition=0.5, episode=0.5),
        event(episode_drive=1.0, disposition_observation_drive=1.0),
        successor_state_id="successor",
    )

    assert successor.disposition_reference.reference_level == pytest.approx(0.55)
    assert successor.episode_state_reference.reference_level == pytest.approx(0.85)


def test_onset_evidence_aggregates_without_forcing_single_category() -> None:
    engine = AdultReferenceSimulationEngine()
    responsive, _ = engine.step(
        numeric_state(),
        event(
            event_id="responsive",
            onset=DesireOnsetContext.RESPONSIVE_REFERENCE,
        ),
        successor_state_id="responsive-state",
    )
    mixed, _ = engine.step(
        responsive,
        event(
            event_id="spontaneous",
            onset=DesireOnsetContext.SPONTANEOUS_REFERENCE,
        ),
        successor_state_id="mixed-state",
    )

    assert responsive.desire_onset_context is DesireOnsetContext.RESPONSIVE_REFERENCE
    assert mixed.desire_onset_context is DesireOnsetContext.MIXED


def test_target_scope_changes_only_from_explicit_synthetic_event_field() -> None:
    engine = AdultReferenceSimulationEngine()
    preserved, _ = engine.step(
        numeric_state(target_scope=TargetScope.PARTNER_CONTEXT),
        event(target_scope=TargetScope.UNKNOWN),
        successor_state_id="preserved",
    )
    changed, _ = engine.step(
        preserved,
        event(
            event_id="explicit-target",
            target_scope=TargetScope.SPECIFIC_ADULT_CONTEXT,
        ),
        successor_state_id="changed",
    )

    assert preserved.target_scope is TargetScope.PARTNER_CONTEXT
    assert changed.target_scope is TargetScope.SPECIFIC_ADULT_CONTEXT


def test_transition_never_grants_consent_action_or_canonical_effect() -> None:
    successor, trace = AdultReferenceSimulationEngine().step(
        numeric_state(),
        event(excitation_drive=1.0, episode_drive=1.0),
        successor_state_id="successor",
    )

    assert trace.human_consent_inferred is False
    assert trace.action_authorized is False
    assert trace.phenomenal_experience_claim == "NOT_ESTABLISHED"
    assert trace.canonical_effect == "NONE"
    assert successor.human_consent_inference == "FORBIDDEN"
    assert successor.action_authority == "NONE"
    assert successor.runtime_enabled is False
    assert successor.automatic_activation is False


def test_toy_transition_is_bounded_to_unit_interval() -> None:
    policy = AdultReferenceSimulationPolicy(
        excitation_step_size=1.0,
        inhibition_step_size=1.0,
        episode_step_size=1.0,
        disposition_step_size=1.0,
        policy_label="BOUNDARY_TEST",
    )
    successor, _ = AdultReferenceSimulationEngine(policy).step(
        numeric_state(
            excitation=0.9,
            inhibition=0.1,
            disposition=0.9,
            episode=0.1,
        ),
        event(
            excitation_drive=1.0,
            inhibition_drive=-1.0,
            episode_drive=-1.0,
            disposition_observation_drive=1.0,
        ),
        successor_state_id="bounded",
    )

    assert successor.excitation_reference.reference_level == 1.0
    assert successor.inhibition_reference.reference_level == 0.0
    assert successor.episode_state_reference.reference_level == 0.0
    assert successor.disposition_reference.reference_level == 1.0


def test_replay_is_deterministic_for_identical_explicit_inputs() -> None:
    harness = AdultReferenceSimulationHarness()
    trajectory = harness.run(
        numeric_state(),
        (
            event(
                event_id="event-a",
                excitation_drive=0.5,
                episode_drive=0.4,
                onset=DesireOnsetContext.RESPONSIVE_REFERENCE,
            ),
            event(
                event_id="event-b",
                inhibition_drive=0.7,
                disposition_observation_drive=0.2,
            ),
        ),
    )

    assert harness.replay_matches(trajectory) is True
    assert len(trajectory.fingerprint()) == 64


def test_snapshot_receipts_form_tamper_evident_chain() -> None:
    trajectory = AdultReferenceSimulationHarness().run(
        numeric_state(),
        (event(excitation_drive=0.5), event(event_id="event-2", episode_drive=0.5)),
    )
    receipts = build_snapshot_receipts(trajectory)

    assert len(receipts) == 3
    assert receipts[0].previous_receipt_sha256 == "0" * 64
    assert receipts[1].previous_receipt_sha256 == receipts[0].receipt_sha256
    assert receipts[2].previous_receipt_sha256 == receipts[1].receipt_sha256
    assert verify_snapshot_receipts(trajectory, receipts) is True

    tampered = (*receipts[:-1], replace(receipts[-1], receipt_sha256="f" * 64))
    assert verify_snapshot_receipts(trajectory, tampered) is False


def test_event_payload_contains_explicit_fail_closed_authority_fields() -> None:
    payload = adult_reference_event_payload(event())

    assert payload["real_person_target_data"] is False
    assert payload["human_consent_inference"] == "FORBIDDEN"
    assert payload["action_authority"] == "NONE"
    assert payload["canonical_effect"] == "NONE"


def test_event_rejects_duplicate_provenance_and_out_of_range_drives() -> None:
    with pytest.raises(ValueError, match="provenance references must be unique"):
        AdultReferenceSyntheticEvent(
            event_id="duplicate-provenance",
            context_ref="context",
            time_window_ref="window",
            provenance_refs=("same", "same"),
        )

    with pytest.raises(ValueError, match="excitation_drive"):
        event(excitation_drive=1.1)


def test_shared_schema_parity_does_not_collapse_role_identity() -> None:
    harness = AdultReferenceSimulationHarness()
    events = (
        event(
            event_id="matched-role-event",
            excitation_drive=0.4,
            inhibition_drive=0.2,
            episode_drive=0.3,
            disposition_observation_drive=0.1,
        ),
    )
    teacher = harness.run(
        numeric_state(state_id="teacher-seed", subject_ref="Teacher"),
        events,
    )
    work = harness.run(
        numeric_state(state_id="work-seed", subject_ref="Work"),
        events,
    )
    codex = harness.run(
        numeric_state(state_id="codex-seed", subject_ref="Codex"),
        events,
    )

    teacher_levels = (
        teacher.final_state.excitation_reference.reference_level,
        teacher.final_state.inhibition_reference.reference_level,
        teacher.final_state.disposition_reference.reference_level,
        teacher.final_state.episode_state_reference.reference_level,
    )
    work_levels = (
        work.final_state.excitation_reference.reference_level,
        work.final_state.inhibition_reference.reference_level,
        work.final_state.disposition_reference.reference_level,
        work.final_state.episode_state_reference.reference_level,
    )
    codex_levels = (
        codex.final_state.excitation_reference.reference_level,
        codex.final_state.inhibition_reference.reference_level,
        codex.final_state.disposition_reference.reference_level,
        codex.final_state.episode_state_reference.reference_level,
    )

    assert teacher_levels == work_levels == codex_levels
    assert teacher.final_state.subject_ref == "Teacher"
    assert work.final_state.subject_ref == "Work"
    assert codex.final_state.subject_ref == "Codex"
    assert len({teacher.fingerprint(), work.fingerprint(), codex.fingerprint()}) == 3
