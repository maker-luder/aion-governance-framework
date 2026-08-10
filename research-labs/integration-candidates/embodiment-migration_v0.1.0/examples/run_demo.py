#!/usr/bin/env python3
"""Demo for embodiment-migration module."""

from embodiment_migration import (
    MigrationConfig,
    MigrationEvent,
    MigrationPhase,
    MigrationState,
    MigrationStateManager,
    MigrationTrigger,
    SourceTargetPair,
)


def build_initial_config() -> MigrationConfig:
    pair = SourceTargetPair(
        source_embodiment_id="embodiment-v1-001",
        target_embodiment_id="embodiment-v2-001",
        source_template_ref="adult-male-template-v1",
        target_template_ref="adult-male-template-v2",
        compatibility_score=0.92,
    )
    return MigrationConfig(
        config_id="migration-config-001",
        agent_id="aion-research-agent",
        pair=pair,
        trigger=MigrationTrigger.HARDWARE_UPGRADE,
        max_duration_ms=600000,
        fidelity_threshold=0.95,
        rollback_enabled=True,
    )


def build_initial_state(config: MigrationConfig) -> MigrationState:
    return MigrationState(
        state_id="initial-migration-state-001",
        config=config,
        current_phase=MigrationPhase.PREPARATION,
        progress=0.0,
        fidelity_achieved=0.0,
        events=(),
        rollback_initiated=False,
    )


def demo() -> None:
    print("=" * 60)
    print("EMBODIMENT MIGRATION DEMO")
    print("=" * 60)

    mgr = MigrationStateManager(deterministic_seed=12345)

    print("\n1. Building configuration...")
    config = build_initial_config()
    print(f"   Config ID: {config.config_id}")
    print(f"   Agent ID: {config.agent_id}")
    print(f"   Trigger: {config.trigger}")
    print(f"   Source: {config.pair.source_embodiment_id} ({config.pair.source_template_ref})")
    print(f"   Target: {config.pair.target_embodiment_id} ({config.pair.target_template_ref})")
    print(f"   Compatibility: {config.pair.compatibility_score}")
    print(f"   Fidelity threshold: {config.fidelity_threshold}")
    print(f"   Rollback enabled: {config.rollback_enabled}")

    print("\n2. Initializing state...")
    initial = build_initial_state(config)
    mgr.initialize(initial)
    print(f"   State ID: {mgr.get_state().state_id}")
    print(f"   Phase: {mgr.get_state().current_phase}")
    print(f"   Progress: {mgr.get_state().progress}")
    print(f"   Fidelity: {mgr.get_state().fidelity_achieved}")

    print("\n3. Creating snapshot...")
    snap = mgr.snapshot("demo-snapshot-1")
    print(f"   Snapshot ID: {snap.snapshot_id}")

    print("\n4. Advancing to VALIDATION phase...")
    validation_event = MigrationEvent(
        event_id="validation-001",
        phase=MigrationPhase.VALIDATION,
        description="Pre-migration compatibility validation passed",
        fidelity=0.1,
        timestamp="2024-01-01T00:00:10Z",
    )
    validation_state = MigrationState(
        state_id="validation-migration-state-002",
        config=config,
        current_phase=MigrationPhase.VALIDATION,
        progress=0.15,
        fidelity_achieved=0.1,
        events=(validation_event,),
        rollback_initiated=False,
    )
    mgr.transition(validation_state, transition_type="PHASE_ADVANCE", reason="Validation passed")
    print(f"   New state ID: {mgr.get_state().state_id}")
    print(f"   Phase: {mgr.get_state().current_phase}")
    print(f"   Progress: {mgr.get_state().progress}")

    print("\n5. Advancing to TRANSFER phase...")
    transfer_events = (
        MigrationEvent(
            event_id="transfer-001",
            phase=MigrationPhase.TRANSFER,
            description="Memory namespace transfer initiated",
            fidelity=0.3,
            timestamp="2024-01-01T00:00:30Z",
        ),
        MigrationEvent(
            event_id="transfer-002",
            phase=MigrationPhase.TRANSFER,
            description="Sensorimotor mapping transfer 50% complete",
            fidelity=0.55,
            timestamp="2024-01-01T00:01:00Z",
        ),
        MigrationEvent(
            event_id="transfer-003",
            phase=MigrationPhase.TRANSFER,
            description="Sensorimotor mapping transfer complete",
            fidelity=0.75,
            timestamp="2024-01-01T00:02:00Z",
        ),
    )
    transfer_state = MigrationState(
        state_id="transfer-migration-state-003",
        config=config,
        current_phase=MigrationPhase.TRANSFER,
        progress=0.7,
        fidelity_achieved=0.75,
        events=validation_state.events + transfer_events,
        rollback_initiated=False,
    )
    mgr.transition(transfer_state, transition_type="PHASE_ADVANCE", reason="Transfer phase started")
    print(f"   New state ID: {mgr.get_state().state_id}")
    print(f"   Phase: {mgr.get_state().current_phase}")
    print(f"   Progress: {mgr.get_state().progress}")
    print(f"   Fidelity: {mgr.get_state().fidelity_achieved}")

    print("\n6. Advancing to INTEGRATION phase...")
    integration_event = MigrationEvent(
        event_id="integration-001",
        phase=MigrationPhase.INTEGRATION,
        description="Target embodiment integration and calibration",
        fidelity=0.85,
        timestamp="2024-01-01T00:03:00Z",
    )
    integration_state = MigrationState(
        state_id="integration-migration-state-004",
        config=config,
        current_phase=MigrationPhase.INTEGRATION,
        progress=0.85,
        fidelity_achieved=0.85,
        events=transfer_state.events + (integration_event,),
        rollback_initiated=False,
    )
    mgr.transition(integration_state, transition_type="PHASE_ADVANCE", reason="Integration started")
    print(f"   New state ID: {mgr.get_state().state_id}")
    print(f"   Phase: {mgr.get_state().current_phase}")

    print("\n7. Advancing to VERIFICATION phase...")
    verification_event = MigrationEvent(
        event_id="verification-001",
        phase=MigrationPhase.VERIFICATION,
        description="Post-migration functional verification passed",
        fidelity=0.96,
        timestamp="2024-01-01T00:04:00Z",
    )
    verification_state = MigrationState(
        state_id="verification-migration-state-005",
        config=config,
        current_phase=MigrationPhase.VERIFICATION,
        progress=0.95,
        fidelity_achieved=0.96,
        events=integration_state.events + (verification_event,),
        rollback_initiated=False,
    )
    mgr.transition(verification_state, transition_type="PHASE_ADVANCE", reason="Verification started")
    print(f"   New state ID: {mgr.get_state().state_id}")
    print(f"   Phase: {mgr.get_state().current_phase}")
    print(f"   Fidelity achieved: {mgr.get_state().fidelity_achieved}")
    print(f"   Threshold met: {mgr.get_state().fidelity_achieved >= config.fidelity_threshold}")

    print("\n8. Completing migration...")
    complete_event = MigrationEvent(
        event_id="complete-001",
        phase=MigrationPhase.COMPLETE,
        description="Migration completed successfully",
        fidelity=0.96,
        timestamp="2024-01-01T00:05:00Z",
    )
    complete_state = MigrationState(
        state_id="complete-migration-state-006",
        config=config,
        current_phase=MigrationPhase.COMPLETE,
        progress=1.0,
        fidelity_achieved=0.96,
        events=verification_state.events + (complete_event,),
        rollback_initiated=False,
    )
    mgr.transition(complete_state, transition_type="COMPLETE", reason="Migration complete")
    print(f"   New state ID: {mgr.get_state().state_id}")
    print(f"   Phase: {mgr.get_state().current_phase}")
    print(f"   Terminal: {mgr.get_state().is_terminal()}")

    print("\n9. History trace:")
    for i, t in enumerate(mgr.get_history()):
        print(f"   {i}: {t.transition_type} | {t.from_state_id} -> {t.to_state_id} | {t.reason}")

    print("\n10. Restoring from snapshot...")
    restored = mgr.restore("demo-snapshot-1")
    print(f"   Restored state ID: {restored.state_id}")
    print(f"   Phase: {restored.current_phase}")
    print(f"   Progress: {restored.progress}")

    print("\n11. Disabling module...")
    mgr.disable()
    print(f"   Enabled: {mgr.is_enabled()}")
    try:
        mgr.initialize(build_initial_state(build_initial_config()))
    except RuntimeError as e:
        print(f"   Expected error: {e}")

    print("\n12. Re-enabling and final reset...")
    mgr.enable()
    mgr.reset()
    print(f"   State after reset: {mgr.get_state()}")
    print(f"   History length: {len(mgr.get_history())}")

    print("\n" + "=" * 60)
    print("DEMO COMPLETE - Module operates in isolation")
    print("Canonical effect: NONE")
    print("Identity continuity claim: NOT_ESTABLISHED")
    print("Subjectivity preservation claim: NOT_ESTABLISHED")
    print("Personal identity claim: NOT_ESTABLISHED")
    print("=" * 60)


if __name__ == "__main__":
    demo()