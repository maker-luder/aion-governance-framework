#!/usr/bin/env python3
"""Demo for embodiment-state module."""

from embodiment_state import (
    EmbodimentConfig,
    EmbodimentState,
    EmbodimentStateManager,
    EmbodimentStatus,
    ModalityConfig,
    ModalityType,
    ProprioceptiveSignal,
)


def build_initial_config() -> EmbodimentConfig:
    modalities = (
        ModalityConfig(
            modality=ModalityType.PROPRIOCEPTIVE,
            enabled=True,
            resolution=0.001,
            latency_ms=2.0,
            noise_floor=0.0005,
        ),
        ModalityConfig(
            modality=ModalityType.INTEROCEPTIVE,
            enabled=True,
            resolution=0.01,
            latency_ms=50.0,
            noise_floor=0.01,
        ),
        ModalityConfig(
            modality=ModalityType.TACTILE,
            enabled=True,
            resolution=0.005,
            latency_ms=10.0,
            noise_floor=0.002,
        ),
        ModalityConfig(
            modality=ModalityType.VESTIBULAR,
            enabled=True,
            resolution=0.001,
            latency_ms=5.0,
            noise_floor=0.001,
        ),
        ModalityConfig(
            modality=ModalityType.MOTOR,
            enabled=True,
            resolution=0.001,
            latency_ms=1.0,
            noise_floor=0.0005,
        ),
    )
    return EmbodimentConfig(
        config_id="embodiment-config-001",
        agent_id="aion-research-agent",
        template_ref="adult-male-template-001",
        modalities=modalities,
        joint_count=27,
    )


def build_initial_state(config: EmbodimentConfig) -> EmbodimentState:
    proprioceptive = tuple(
        ProprioceptiveSignal(
            joint_id=f"joint-{i:02d}",
            position=0.0,
            velocity=0.0,
            force=0.0,
            confidence=0.95,
            timestamp="2024-01-01T00:00:00Z",
        )
        for i in range(config.joint_count)
    )
    interoceptive = (
        ProprioceptiveSignal(
            joint_id="heart-rate",
            position=72.0,
            velocity=0.0,
            force=0.0,
            confidence=0.9,
            timestamp="2024-01-01T00:00:00Z",
        ),
        ProprioceptiveSignal(
            joint_id="respiration",
            position=16.0,
            velocity=0.0,
            force=0.0,
            confidence=0.85,
            timestamp="2024-01-01T00:00:00Z",
        ),
    )
    return EmbodimentState(
        state_id="initial-embodiment-state-001",
        config=config,
        status=EmbodimentStatus.ACTIVE,
        proprioceptive_signals=proprioceptive,
        interoceptive_signals=interoceptive,
        motor_commands=(),
        uncertainty_estimate=0.05,
    )


def demo() -> None:
    print("=" * 60)
    print("EMBODIMENT STATE DEMO")
    print("=" * 60)

    mgr = EmbodimentStateManager(deterministic_seed=12345)

    print("\n1. Building configuration...")
    config = build_initial_config()
    print(f"   Config ID: {config.config_id}")
    print(f"   Agent ID: {config.agent_id}")
    print(f"   Template: {config.template_ref}")
    print(f"   Joint count: {config.joint_count}")
    print(f"   Modalities: {[m.modality.value for m in config.modalities]}")

    print("\n2. Initializing state...")
    initial = build_initial_state(config)
    mgr.initialize(initial)
    print(f"   State ID: {mgr.get_state().state_id}")
    print(f"   Status: {mgr.get_state().status}")
    print(f"   Proprioceptive signals: {len(mgr.get_state().proprioceptive_signals)}")
    print(f"   Interoceptive signals: {len(mgr.get_state().interoceptive_signals)}")
    print(f"   Uncertainty: {mgr.get_state().uncertainty_estimate}")

    print("\n3. Creating snapshot...")
    snap = mgr.snapshot("demo-snapshot-1")
    print(f"   Snapshot ID: {snap.snapshot_id}")

    print("\n4. Simulating movement (transition)...")
    moved_proprioceptive = tuple(
        ProprioceptiveSignal(
            joint_id=sig.joint_id,
            position=sig.position + 0.1,
            velocity=0.5,
            force=0.2,
            confidence=0.9,
            timestamp="2024-01-01T00:00:01Z",
        )
        for sig in initial.proprioceptive_signals
    )
    motor_commands = tuple(
        ProprioceptiveSignal(
            joint_id=sig.joint_id,
            position=sig.position + 0.15,
            velocity=0.6,
            force=0.3,
            confidence=0.85,
            timestamp="2024-01-01T00:00:01Z",
        )
        for sig in initial.proprioceptive_signals[:5]  # First 5 joints actuated
    )
    moved_state = EmbodimentState(
        state_id="moved-embodiment-state-002",
        config=config,
        status=EmbodimentStatus.ACTIVE,
        proprioceptive_signals=moved_proprioceptive,
        interoceptive_signals=initial.interoceptive_signals,
        motor_commands=motor_commands,
        uncertainty_estimate=0.08,
    )
    mgr.transition(moved_state, transition_type="MOVEMENT", reason="Simulated reaching movement")
    print(f"   New state ID: {mgr.get_state().state_id}")
    print(f"   Motor commands: {len(mgr.get_state().motor_commands)}")
    print(f"   Uncertainty: {mgr.get_state().uncertainty_estimate}")

    print("\n5. History trace:")
    for i, t in enumerate(mgr.get_history()):
        print(f"   {i}: {t.transition_type} | {t.from_state_id} -> {t.to_state_id} | {t.reason}")

    print("\n6. Restoring from snapshot...")
    restored = mgr.restore("demo-snapshot-1")
    print(f"   Restored state ID: {restored.state_id}")
    print(f"   Proprioceptive signals: {len(restored.proprioceptive_signals)}")
    print(f"   Motor commands: {len(restored.motor_commands)}")

    print("\n7. Ablating TACTILE modality...")
    mgr.ablate("TACTILE")
    ablated = mgr.get_state()
    modalities = {m.modality for m in ablated.config.modalities}
    print(f"   Remaining modalities: {[m.value for m in modalities]}")
    assert ModalityType.TACTILE not in modalities

    print("\n8. Disabling module...")
    mgr.disable()
    print(f"   Enabled: {mgr.is_enabled()}")
    try:
        mgr.initialize(build_initial_state(build_initial_config()))
    except RuntimeError as e:
        print(f"   Expected error: {e}")

    print("\n9. Re-enabling and final reset...")
    mgr.enable()
    mgr.reset()
    print(f"   State after reset: {mgr.get_state()}")
    print(f"   History length: {len(mgr.get_history())}")

    print("\n" + "=" * 60)
    print("DEMO COMPLETE - Module operates in isolation")
    print("Canonical effect: NONE")
    print("Body sensation claim: NOT_ESTABLISHED")
    print("Body ownership claim: NOT_ESTABLISHED")
    print("Gender identity claim: NOT_ESTABLISHED")
    print("Subjectivity claim: NOT_ESTABLISHED")
    print("=" * 60)


if __name__ == "__main__":
    demo()