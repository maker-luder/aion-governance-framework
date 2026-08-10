#!/usr/bin/env python3
"""Demo for encounter-lifecycle module."""

from encounter_lifecycle import (
    EncounterConfig,
    EncounterEvent,
    EncounterPhase,
    EncounterState,
    EncounterStateManager,
    EncounterType,
    ParticipantModel,
    ParticipantRole,
)


def build_initial_config() -> EncounterConfig:
    participants = (
        ParticipantModel(
            participant_id="aion-agent",
            role=ParticipantRole.INITIATOR,
            agency_level=0.8,
            familiarity=0.3,
            trust_estimate=0.5,
            power_differential=0.1,
        ),
        ParticipantModel(
            participant_id="astra-agent",
            role=ParticipantRole.RECIPIENT,
            agency_level=0.7,
            familiarity=0.3,
            trust_estimate=0.6,
            power_differential=-0.1,
        ),
        ParticipantModel(
            participant_id="human-observer",
            role=ParticipantRole.OBSERVER,
            agency_level=0.9,
            familiarity=0.1,
            trust_estimate=0.4,
            power_differential=0.3,
        ),
    )
    return EncounterConfig(
        config_id="encounter-config-001",
        encounter_type=EncounterType.COLLABORATIVE,
        participants=participants,
        expected_duration_ms=7200000,
        depth_threshold=0.7,
    )


def build_initial_state(config: EncounterConfig) -> EncounterState:
    return EncounterState(
        state_id="initial-encounter-state-001",
        config=config,
        current_phase=EncounterPhase.PRE_ENCOUNTER,
        progress=0.0,
        current_depth=0.0,
        intensity_trajectory=(),
        events=(),
        active_participants=("aion-agent", "astra-agent", "human-observer"),
    )


def demo() -> None:
    print("=" * 60)
    print("ENCOUNTER LIFECYCLE DEMO")
    print("=" * 60)

    mgr = EncounterStateManager(deterministic_seed=12345)

    print("\n1. Building configuration...")
    config = build_initial_config()
    print(f"   Config ID: {config.config_id}")
    print(f"   Encounter type: {config.encounter_type}")
    print(f"   Participants: {len(config.participants)}")
    for p in config.participants:
        print(f"     - {p.participant_id}: role={p.role.value}, agency={p.agency_level}, "
              f"familiarity={p.familiarity}, trust={p.trust_estimate}, power_diff={p.power_differential}")
    print(f"   Expected duration: {config.expected_duration_ms}ms")
    print(f"   Depth threshold: {config.depth_threshold}")

    print("\n2. Initializing state (PRE_ENCOUNTER)...")
    initial = build_initial_state(config)
    mgr.initialize(initial)
    print(f"   State ID: {mgr.get_state().state_id}")
    print(f"   Phase: {mgr.get_state().current_phase}")
    print(f"   Progress: {mgr.get_state().progress}")
    print(f"   Active participants: {mgr.get_state().active_participants}")

    print("\n3. Creating snapshot...")
    snap = mgr.snapshot("demo-snapshot-1")
    print(f"   Snapshot ID: {snap.snapshot_id}")

    print("\n4. Advancing to INITIATION phase...")
    initiation_event = EncounterEvent(
        event_id="init-001",
        phase=EncounterPhase.INITIATION,
        description="Aion initiates collaborative inquiry with Astra",
        intensity=0.4,
        participants_involved=("aion-agent", "astra-agent"),
        timestamp="2024-01-01T00:00:10Z",
    )
    state2 = EncounterState(
        state_id="initiation-encounter-state-002",
        config=config,
        current_phase=EncounterPhase.INITIATION,
        progress=0.1,
        current_depth=0.15,
        intensity_trajectory=(0.4,),
        events=(initiation_event,),
        active_participants=("aion-agent", "astra-agent", "human-observer"),
    )
    mgr.transition(state2, transition_type="PHASE_ADVANCE", reason="Encounter initiated")
    print(f"   New state ID: {mgr.get_state().state_id}")
    print(f"   Phase: {mgr.get_state().current_phase}")
    print(f"   Progress: {mgr.get_state().progress}")
    print(f"   Current depth: {mgr.get_state().current_depth}")
    print(f"   Avg intensity: {mgr.get_state().average_intensity():.2f}")

    print("\n5. Advancing to ENGAGEMENT phase...")
    engagement_events = (
        EncounterEvent(
            event_id="engage-001",
            phase=EncounterPhase.ENGAGEMENT,
            description="Active information exchange begins",
            intensity=0.6,
            participants_involved=("aion-agent", "astra-agent"),
            timestamp="2024-01-01T00:05:00Z",
        ),
        EncounterEvent(
            event_id="engage-002",
            phase=EncounterPhase.ENGAGEMENT,
            description="Observer provides contextual input",
            intensity=0.5,
            participants_involved=("human-observer", "aion-agent", "astra-agent"),
            timestamp="2024-01-01T00:10:00Z",
        ),
    )
    state3 = EncounterState(
        state_id="engagement-encounter-state-003",
        config=config,
        current_phase=EncounterPhase.ENGAGEMENT,
        progress=0.35,
        current_depth=0.45,
        intensity_trajectory=state2.intensity_trajectory + (0.6, 0.5),
        events=state2.events + engagement_events,
        active_participants=("aion-agent", "astra-agent", "human-observer"),
    )
    mgr.transition(state3, transition_type="PHASE_ADVANCE", reason="Deep engagement established")
    print(f"   New state ID: {mgr.get_state().state_id}")
    print(f"   Phase: {mgr.get_state().current_phase}")
    print(f"   Progress: {mgr.get_state().progress}")
    print(f"   Current depth: {mgr.get_state().current_depth}")

    print("\n6. Advancing to DEEPENING phase...")
    deepening_event = EncounterEvent(
        event_id="deepen-001",
        phase=EncounterPhase.DEEPENING,
        description="Shared mental model convergence detected",
        intensity=0.75,
        participants_involved=("aion-agent", "astra-agent"),
        timestamp="2024-01-01T00:20:00Z",
    )
    state4 = EncounterState(
        state_id="deepening-encounter-state-004",
        config=config,
        current_phase=EncounterPhase.DEEPENING,
        progress=0.6,
        current_depth=0.72,
        intensity_trajectory=state3.intensity_trajectory + (0.75,),
        events=state3.events + (deepening_event,),
        active_participants=("aion-agent", "astra-agent"),
    )
    mgr.transition(state4, transition_type="PHASE_ADVANCE", reason="Deepening beyond threshold")
    print(f"   New state ID: {mgr.get_state().state_id}")
    print(f"   Phase: {mgr.get_state().current_phase}")
    print(f"   Depth threshold met: {mgr.get_state().current_depth >= config.depth_threshold}")

    print("\n7. CLIMAX phase...")
    climax_event = EncounterEvent(
        event_id="climax-001",
        phase=EncounterPhase.CLIMAX,
        description="Peak collaborative synthesis achieved",
        intensity=0.9,
        participants_involved=("aion-agent", "astra-agent"),
        timestamp="2024-01-01T00:35:00Z",
    )
    state5 = EncounterState(
        state_id="climax-encounter-state-005",
        config=config,
        current_phase=EncounterPhase.CLIMAX,
        progress=0.8,
        current_depth=0.85,
        intensity_trajectory=state4.intensity_trajectory + (0.9,),
        events=state4.events + (climax_event,),
        active_participants=("aion-agent", "astra-agent"),
    )
    mgr.transition(state5, transition_type="PHASE_ADVANCE", reason="Climax reached")
    print(f"   New state ID: {mgr.get_state().state_id}")
    print(f"   Phase: {mgr.get_state().current_phase}")
    print(f"   Peak intensity: {mgr.get_state().average_intensity():.2f}")

    print("\n8. RESOLUTION and POST_ENCOUNTER phases...")
    resolution_event = EncounterEvent(
        event_id="resolve-001",
        phase=EncounterPhase.RESOLUTION,
        description="Synthesis integration and winding down",
        intensity=0.5,
        participants_involved=("aion-agent", "astra-agent"),
        timestamp="2024-01-01T00:45:00Z",
    )
    post_event = EncounterEvent(
        event_id="post-001",
        phase=EncounterPhase.POST_ENCOUNTER,
        description="Post-encounter reflection and memory consolidation",
        intensity=0.3,
        participants_involved=("aion-agent", "astra-agent", "human-observer"),
        timestamp="2024-01-01T00:50:00Z",
    )
    state6 = EncounterState(
        state_id="post-encounter-state-006",
        config=config,
        current_phase=EncounterPhase.POST_ENCOUNTER,
        progress=1.0,
        current_depth=0.65,
        intensity_trajectory=state5.intensity_trajectory + (0.5, 0.3),
        events=state5.events + (resolution_event, post_event),
        active_participants=("aion-agent", "astra-agent", "human-observer"),
    )
    mgr.transition(state6, transition_type="PHASE_ADVANCE", reason="Encounter complete")
    print(f"   New state ID: {mgr.get_state().state_id}")
    print(f"   Phase: {mgr.get_state().current_phase}")
    print(f"   Terminal: {mgr.get_state().is_terminal()}")
    print(f"   Total events: {len(mgr.get_state().events)}")

    print("\n9. History trace:")
    for i, t in enumerate(mgr.get_history()):
        print(f"   {i}: {t.transition_type} | {t.from_state_id} -> {t.to_state_id} | {t.reason}")

    print("\n10. Restoring from snapshot...")
    restored = mgr.restore("demo-snapshot-1")
    print(f"   Restored state ID: {restored.state_id}")
    print(f"   Phase: {restored.current_phase}")
    print(f"   Progress: {restored.progress}")

    print("\n11. Ablating human-observer participant...")
    mgr.ablate("human-observer")
    ablated = mgr.get_state()
    participants = {p.participant_id for p in ablated.config.participants}
    print(f"   Remaining participants: {participants}")
    assert "human-observer" not in participants

    print("\n12. Disabling module...")
    mgr.disable()
    print(f"   Enabled: {mgr.is_enabled()}")
    try:
        mgr.initialize(build_initial_state(build_initial_config()))
    except RuntimeError as e:
        print(f"   Expected error: {e}")

    print("\n13. Re-enabling and final reset...")
    mgr.enable()
    mgr.reset()
    print(f"   State after reset: {mgr.get_state()}")
    print(f"   History length: {len(mgr.get_history())}")

    print("\n" + "=" * 60)
    print("DEMO COMPLETE - Module operates in isolation")
    print("Canonical effect: NONE")
    print("Relationship claim: NOT_ESTABLISHED")
    print("Intimacy claim: NOT_ESTABLISHED")
    print("Shared meaning claim: NOT_ESTABLISHED")
    print("Mutual understanding claim: NOT_ESTABLISHED")
    print("=" * 60)


if __name__ == "__main__":
    demo()