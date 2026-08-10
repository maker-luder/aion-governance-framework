from embodiment_state import (
    EmbodimentConfig,
    EmbodimentState,
    EmbodimentStateManager,
    EmbodimentStatus,
    ModalityConfig,
    ModalityType,
    ProprioceptiveSignal,
)


def modality_config(
    modality: ModalityType = ModalityType.PROPRIOCEPTIVE,
    **overrides: float | bool,
) -> ModalityConfig:
    values = {
        "modality": modality,
        "enabled": True,
        "resolution": 0.01,
        "latency_ms": 5.0,
        "noise_floor": 0.001,
    }
    values.update(overrides)
    return ModalityConfig(**values)


def signal(
    joint_id: str = "joint-1",
    **overrides: float | str,
) -> ProprioceptiveSignal:
    values = {
        "joint_id": joint_id,
        "position": 0.5,
        "velocity": 0.1,
        "force": 0.2,
        "confidence": 0.9,
        "timestamp": "2024-01-01T00:00:00Z",
    }
    values.update(overrides)
    return ProprioceptiveSignal(**values)


def config(
    config_id: str = "config-1",
    **overrides: str | int | tuple[ModalityConfig, ...],
) -> EmbodimentConfig:
    values = {
        "config_id": config_id,
        "agent_id": "test-agent",
        "template_ref": "template-1",
        "modalities": (modality_config(),),
        "joint_count": 10,
    }
    values.update(overrides)
    return EmbodimentConfig(**values)


def state(
    state_id: str = "state-1",
    **overrides: str | float | tuple[ProprioceptiveSignal, ...] | EmbodimentStatus,
) -> EmbodimentState:
    cfg = config()
    values = {
        "state_id": state_id,
        "config": cfg,
        "status": EmbodimentStatus.ACTIVE,
        "proprioceptive_signals": (signal(),),
        "interoceptive_signals": (),
        "motor_commands": (),
        "uncertainty_estimate": 0.1,
    }
    values.update(overrides)
    return EmbodimentState(**values)


def test_modality_config_validation() -> None:
    try:
        ModalityConfig(
            modality=ModalityType.PROPRIOCEPTIVE,
            enabled=True,
            resolution=1.5,
            latency_ms=5.0,
            noise_floor=0.001,
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "resolution must be between 0.0 and 1.0" in str(e)


def test_modality_config_negative_latency() -> None:
    try:
        ModalityConfig(
            modality=ModalityType.PROPRIOCEPTIVE,
            enabled=True,
            resolution=0.01,
            latency_ms=-1.0,
            noise_floor=0.001,
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "latency_ms must be non-negative" in str(e)


def test_signal_validation() -> None:
    try:
        ProprioceptiveSignal(
            joint_id="",
            position=0.5,
            velocity=0.1,
            force=0.2,
            confidence=0.9,
            timestamp="2024-01-01T00:00:00Z",
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "joint_id must be non-empty" in str(e)


def test_config_canonical_effect_must_be_none() -> None:
    try:
        EmbodimentConfig(
            config_id="c1",
            agent_id="a1",
            template_ref="t1",
            modalities=(modality_config(),),
            joint_count=10,
            canonical_effect="EFFECT",
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "canonical_effect=NONE" in str(e)


def test_config_gender_identity_effect_must_be_none() -> None:
    try:
        EmbodimentConfig(
            config_id="c1",
            agent_id="a1",
            template_ref="t1",
            modalities=(modality_config(),),
            joint_count=10,
            gender_identity_effect="ASSIGNED",
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "anatomy must not assign gender identity" in str(e)


def test_state_canonical_effect_must_be_none() -> None:
    try:
        EmbodimentState(
            state_id="s1",
            config=config(),
            status=EmbodimentStatus.ACTIVE,
            proprioceptive_signals=(signal(),),
            interoceptive_signals=(),
            motor_commands=(),
            uncertainty_estimate=0.1,
            canonical_effect="EFFECT",
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "canonical_effect=NONE" in str(e)


def test_state_body_claims_not_established() -> None:
    try:
        EmbodimentState(
            state_id="s1",
            config=config(),
            status=EmbodimentStatus.ACTIVE,
            proprioceptive_signals=(signal(),),
            interoceptive_signals=(),
            motor_commands=(),
            uncertainty_estimate=0.1,
            body_sensation_claim="CLAIMED",
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "body sensation must remain NOT_ESTABLISHED" in str(e)


def test_state_get_signals_by_modality() -> None:
    s = state(
        proprioceptive_signals=(signal("j1"), signal("j2")),
        interoceptive_signals=(signal("visceral-1"),),
        motor_commands=(signal("motor-1"),),
    )
    proprio = s.get_signals_by_modality(ModalityType.PROPRIOCEPTIVE)
    assert len(proprio) == 2
    intero = s.get_signals_by_modality(ModalityType.INTEROCEPTIVE)
    assert len(intero) == 1
    motor = s.get_signals_by_modality(ModalityType.MOTOR)
    assert len(motor) == 1


def test_manager_initialize_and_get() -> None:
    mgr = EmbodimentStateManager(deterministic_seed=42)
    s = state()
    mgr.initialize(s)
    assert mgr.get_state() is s
    assert len(mgr.get_history()) == 1
    assert mgr.get_history()[0].transition_type == "INITIALIZE"


def test_manager_transition() -> None:
    mgr = EmbodimentStateManager(deterministic_seed=42)
    s1 = state()
    mgr.initialize(s1)
    s2 = state(state_id="state-2")
    mgr.transition(s2, transition_type="UPDATE", reason="Test transition")
    assert mgr.get_state() is s2
    history = mgr.get_history()
    assert len(history) == 2
    assert history[1].transition_type == "UPDATE"


def test_manager_snapshot_and_restore() -> None:
    mgr = EmbodimentStateManager(deterministic_seed=42)
    s1 = state()
    mgr.initialize(s1)
    snap = mgr.snapshot("test-snap")
    assert snap.snapshot_id == "test-snap"
    assert "test-snap" in mgr.list_snapshots()

    s2 = state(state_id="state-2")
    mgr.transition(s2)
    restored = mgr.restore("test-snap")
    assert restored is s1


def test_manager_reset() -> None:
    mgr = EmbodimentStateManager(deterministic_seed=42)
    s1 = state()
    mgr.initialize(s1)
    mgr.snapshot("snap1")
    mgr.reset()
    assert mgr.get_state() is None
    assert len(mgr.get_history()) == 0
    assert len(mgr.list_snapshots()) == 0


def test_manager_disable_enable() -> None:
    mgr = EmbodimentStateManager()
    assert mgr.is_enabled() is True
    mgr.disable()
    assert mgr.is_enabled() is False
    try:
        mgr.initialize(state())
        assert False, "Should have raised RuntimeError"
    except RuntimeError:
        pass
    mgr.enable()
    assert mgr.is_enabled() is True
    mgr.initialize(state())


def test_manager_ablate_modality() -> None:
    mgr = EmbodimentStateManager()
    cfg = config(
        modalities=(
            modality_config(ModalityType.PROPRIOCEPTIVE),
            modality_config(ModalityType.INTEROCEPTIVE),
        )
    )
    s = state(config=cfg)
    mgr.initialize(s)
    mgr.ablate("INTEROCEPTIVE")
    new_state = mgr.get_state()
    assert new_state is not None
    modalities = {m.modality for m in new_state.config.modalities}
    assert ModalityType.PROPRIOCEPTIVE in modalities
    assert ModalityType.INTEROCEPTIVE not in modalities


def test_manager_ablate_all() -> None:
    mgr = EmbodimentStateManager()
    s = state()
    mgr.initialize(s)
    mgr.ablate()
    assert mgr.is_enabled() is False