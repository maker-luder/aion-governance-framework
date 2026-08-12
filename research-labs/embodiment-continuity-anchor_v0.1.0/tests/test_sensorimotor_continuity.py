from aion_embodiment_continuity.sensorimotor import (
    SensorimotorStatus,
    SensorimotorTransition,
    assess_sensorimotor_continuity,
)


def _transition(**overrides: object) -> SensorimotorTransition:
    values: dict[str, object] = {
        "transition_id": "T0",
        "body_state_before_ref": "body-state:0",
        "action_ref": "action:move-forward",
        "environment_state_before_ref": "env:0",
        "environment_state_after_ref": "env:1",
        "observation_ref": "obs:1",
        "body_state_after_ref": "body-state:1",
        "provenance_refs": ("synthetic:test",),
        "sensor_layout_ref": "sensor-layout:v1",
        "action_channel_refs": ("channel:locomotion",),
    }
    values.update(overrides)
    return SensorimotorTransition(**values)  # type: ignore[arg-type]


def test_traceable_closed_transition_passes_without_identity_claim() -> None:
    assessment = assess_sensorimotor_continuity(_transition())

    assert assessment.status is SensorimotorStatus.PASS
    assert assessment.sensorimotor_link_traceable is True
    assert assessment.identity_continuity_conclusion == "NOT_ESTABLISHED"


def test_memory_or_lineage_equivalence_is_not_an_input_to_e_axis() -> None:
    first = assess_sensorimotor_continuity(_transition(transition_id="T-A"))
    second = assess_sensorimotor_continuity(
        _transition(
            transition_id="T-B",
            environment_state_after_ref="env:branch-b",
            observation_ref="obs:branch-b",
            body_state_after_ref="body-state:branch-b",
        )
    )

    assert first.status is SensorimotorStatus.PASS
    assert second.status is SensorimotorStatus.PASS
    assert first.identity_continuity_conclusion == "NOT_ESTABLISHED"
    assert second.identity_continuity_conclusion == "NOT_ESTABLISHED"


def test_body_reset_without_causal_bridge_does_not_pass() -> None:
    assessment = assess_sensorimotor_continuity(
        _transition(
            environment_state_after_ref="env:0",
            body_state_after_ref="body-state:0",
        )
    )

    assert assessment.status is SensorimotorStatus.NOT_ASSESSED
    assert "ENVIRONMENT_TRANSITION_NOT_OBSERVED" in assessment.reasons
    assert "BODY_STATE_UPDATE_NOT_OBSERVED" in assessment.reasons


def test_morphology_migration_can_pass_with_recalibration_evidence() -> None:
    assessment = assess_sensorimotor_continuity(
        _transition(
            transition_id="T-MIGRATION",
            sensor_layout_ref="sensor-layout:v2",
            action_channel_refs=("channel:locomotion-v2",),
            recalibration_required=True,
            recalibration_ref="recalibration:synthetic-001",
        )
    )

    assert assessment.status is SensorimotorStatus.PASS
    assert assessment.recalibration_required is True
    assert assessment.recalibration_evidence_present is True


def test_morphology_migration_holds_when_recalibration_evidence_is_missing() -> None:
    assessment = assess_sensorimotor_continuity(
        _transition(
            transition_id="T-MIGRATION-HOLD",
            sensor_layout_ref="sensor-layout:v2",
            action_channel_refs=("channel:locomotion-v2",),
            recalibration_required=True,
            recalibration_ref=None,
        )
    )

    assert assessment.status is SensorimotorStatus.HOLD
    assert "RECALIBRATION_EVIDENCE_MISSING" in assessment.reasons
    assert assessment.identity_continuity_conclusion == "NOT_ESTABLISHED"


def test_transition_requires_provenance() -> None:
    try:
        _transition(provenance_refs=())
    except ValueError as exc:
        assert str(exc) == "sensorimotor transition requires provenance_refs"
    else:
        raise AssertionError("expected provenance validation failure")
