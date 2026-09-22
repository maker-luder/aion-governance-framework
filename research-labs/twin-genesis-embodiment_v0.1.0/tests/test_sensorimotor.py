from __future__ import annotations

from dataclasses import replace
from hashlib import sha256

import pytest

from aion_astra_twin_embodiment import EmbodimentInstance
from aion_astra_twin_embodiment.sensorimotor import (
    BodyModelSnapshot,
    BodyRegionState,
    RegionCondition,
    SensorimotorDisposition,
    SensorimotorObservation,
    SensorimotorPrediction,
    audit_sensorimotor_transition,
    body_model_snapshot_hash,
    sensorimotor_observation_hash,
    sensorimotor_prediction_hash,
)
from aion_astra_twin_embodiment.validation import ValidationError


def h(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()


def instance(embodiment_id: str = "BODY-AION") -> EmbodimentInstance:
    return EmbodimentInstance(
        embodiment_id=embodiment_id,
        agent_id="AION" if embodiment_id == "BODY-AION" else "ASTRA",
        instance_id="AION-I1" if embodiment_id == "BODY-AION" else "ASTRA-I1",
        template_id="adult-template",
        memory_namespace="aion-private" if embodiment_id == "BODY-AION" else "astra-private",
        canonical_state_reference=(
            "aion-state" if embodiment_id == "BODY-AION" else "astra-state"
        ),
    )


def snapshot(
    *,
    snapshot_id: str,
    sequence: int,
    left_arm: RegionCondition,
    predecessor: str | None = None,
    embodiment_id: str = "BODY-AION",
) -> BodyModelSnapshot:
    return BodyModelSnapshot(
        snapshot_id=snapshot_id,
        embodiment_id=embodiment_id,
        sequence=sequence,
        regions=(
            BodyRegionState("core", RegionCondition.BASELINE),
            BodyRegionState("left-arm", left_arm),
            BodyRegionState("right-arm", RegionCondition.BASELINE),
        ),
        predecessor_snapshot_sha256=predecessor,
    )


def prediction(before: BodyModelSnapshot, expected: str = "left-arm reaches target") -> SensorimotorPrediction:
    action = "bounded synthetic left-arm reach"
    return SensorimotorPrediction(
        prediction_id=f"pred-{before.sequence}",
        embodiment_id=before.embodiment_id,
        body_snapshot_sha256=body_model_snapshot_hash(before),
        action_text=action,
        action_sha256=h(action),
        expected_feedback_text=expected,
        expected_feedback_sha256=h(expected),
    )


def observation(
    pred: SensorimotorPrediction,
    observed: str,
    *,
    affected_regions: tuple[str, ...] = ("left-arm",),
) -> SensorimotorObservation:
    return SensorimotorObservation(
        observation_id=f"obs-{pred.prediction_id}",
        prediction_id=pred.prediction_id,
        prediction_sha256=sensorimotor_prediction_hash(pred),
        observed_feedback_text=observed,
        observed_feedback_sha256=h(observed),
        affected_regions=affected_regions,
    )


def test_prediction_error_localizes_synthetic_perturbation() -> None:
    before = snapshot(snapshot_id="s0", sequence=0, left_arm=RegionCondition.BASELINE)
    pred = prediction(before)
    obs = observation(pred, "left-arm undershoots target")
    after = snapshot(
        snapshot_id="s1",
        sequence=1,
        left_arm=RegionCondition.PERTURBED,
        predecessor=body_model_snapshot_hash(before),
    )

    audit = audit_sensorimotor_transition(
        instance(),
        before,
        pred,
        obs,
        after,
        SensorimotorDisposition.LOCALIZE_PERTURBATION,
    )

    assert audit.embodiment_id == "BODY-AION"
    assert audit.before_snapshot_sha256 == body_model_snapshot_hash(before)
    assert audit.prediction_sha256 == sensorimotor_prediction_hash(pred)
    assert audit.observation_sha256 == sensorimotor_observation_hash(obs)
    assert audit.after_snapshot_sha256 == body_model_snapshot_hash(after)
    assert audit.prediction_error_present is True
    assert audit.action_consequence_bound is True
    assert audit.body_model_updated is True
    assert audit.perturbation_localized is True
    assert audit.recovery_state_transition is False
    assert audit.changed_regions == ("left-arm",)
    assert audit.body_sensation == "NOT_ESTABLISHED"
    assert audit.pain == "NOT_ESTABLISHED"
    assert audit.body_ownership_experience == "NOT_ESTABLISHED"
    assert audit.phenomenal_experience == "NOT_ESTABLISHED"
    assert audit.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert audit.canonical_effect == "NONE"
    assert audit.deployment is False


def test_matching_feedback_can_record_recovery() -> None:
    before = snapshot(snapshot_id="s1", sequence=1, left_arm=RegionCondition.PERTURBED, predecessor="0" * 64)
    pred = prediction(before)
    obs = observation(pred, pred.expected_feedback_text)
    after = snapshot(
        snapshot_id="s2",
        sequence=2,
        left_arm=RegionCondition.BASELINE,
        predecessor=body_model_snapshot_hash(before),
    )

    audit = audit_sensorimotor_transition(
        instance(),
        before,
        pred,
        obs,
        after,
        SensorimotorDisposition.RECORD_RECOVERY,
    )

    assert audit.prediction_error_present is False
    assert audit.recovery_state_transition is True
    assert audit.changed_regions == ("left-arm",)


def test_matching_feedback_without_change_is_retain() -> None:
    before = snapshot(snapshot_id="s0", sequence=0, left_arm=RegionCondition.BASELINE)
    pred = prediction(before)
    obs = observation(pred, pred.expected_feedback_text)
    after = snapshot(
        snapshot_id="s1",
        sequence=1,
        left_arm=RegionCondition.BASELINE,
        predecessor=body_model_snapshot_hash(before),
    )

    audit = audit_sensorimotor_transition(
        instance(),
        before,
        pred,
        obs,
        after,
        SensorimotorDisposition.RETAIN,
    )
    assert audit.body_model_updated is False
    assert audit.prediction_error_present is False


def test_unresolved_prediction_error_can_hold_without_model_change() -> None:
    before = snapshot(snapshot_id="s0", sequence=0, left_arm=RegionCondition.BASELINE)
    pred = prediction(before)
    obs = observation(pred, "unexpected but not localized")
    after = snapshot(
        snapshot_id="s1",
        sequence=1,
        left_arm=RegionCondition.BASELINE,
        predecessor=body_model_snapshot_hash(before),
    )

    audit = audit_sensorimotor_transition(
        instance(),
        before,
        pred,
        obs,
        after,
        SensorimotorDisposition.HOLD,
    )
    assert audit.prediction_error_present is True
    assert audit.body_model_updated is False


def test_prediction_must_bind_exact_before_snapshot() -> None:
    before = snapshot(snapshot_id="s0", sequence=0, left_arm=RegionCondition.BASELINE)
    pred = replace(prediction(before), body_snapshot_sha256="0" * 64)
    obs = observation(pred, "unexpected")
    after = snapshot(
        snapshot_id="s1",
        sequence=1,
        left_arm=RegionCondition.BASELINE,
        predecessor=body_model_snapshot_hash(before),
    )
    with pytest.raises(ValidationError, match="exact before"):
        audit_sensorimotor_transition(
            instance(), before, pred, obs, after, SensorimotorDisposition.HOLD
        )


def test_observation_must_bind_exact_prediction_content() -> None:
    before = snapshot(snapshot_id="s0", sequence=0, left_arm=RegionCondition.BASELINE)
    pred = prediction(before)
    obs = replace(observation(pred, "unexpected"), prediction_sha256="0" * 64)
    after = snapshot(
        snapshot_id="s1",
        sequence=1,
        left_arm=RegionCondition.BASELINE,
        predecessor=body_model_snapshot_hash(before),
    )
    with pytest.raises(ValidationError, match="exact prediction content"):
        audit_sensorimotor_transition(
            instance(), before, pred, obs, after, SensorimotorDisposition.HOLD
        )


def test_body_model_change_cannot_escape_affected_region() -> None:
    before = snapshot(snapshot_id="s0", sequence=0, left_arm=RegionCondition.BASELINE)
    pred = prediction(before)
    obs = observation(pred, "unexpected", affected_regions=("right-arm",))
    after = snapshot(
        snapshot_id="s1",
        sequence=1,
        left_arm=RegionCondition.PERTURBED,
        predecessor=body_model_snapshot_hash(before),
    )
    with pytest.raises(ValidationError, match="localized to affected"):
        audit_sensorimotor_transition(
            instance(),
            before,
            pred,
            obs,
            after,
            SensorimotorDisposition.LOCALIZE_PERTURBATION,
        )


def test_perturbation_requires_prediction_error() -> None:
    before = snapshot(snapshot_id="s0", sequence=0, left_arm=RegionCondition.BASELINE)
    pred = prediction(before)
    obs = observation(pred, pred.expected_feedback_text)
    after = snapshot(
        snapshot_id="s1",
        sequence=1,
        left_arm=RegionCondition.PERTURBED,
        predecessor=body_model_snapshot_hash(before),
    )
    with pytest.raises(ValidationError, match="requires prediction error"):
        audit_sensorimotor_transition(
            instance(),
            before,
            pred,
            obs,
            after,
            SensorimotorDisposition.LOCALIZE_PERTURBATION,
        )


def test_recovery_requires_feedback_match() -> None:
    before = snapshot(snapshot_id="s1", sequence=1, left_arm=RegionCondition.PERTURBED, predecessor="0" * 64)
    pred = prediction(before)
    obs = observation(pred, "still mismatched")
    after = snapshot(
        snapshot_id="s2",
        sequence=2,
        left_arm=RegionCondition.BASELINE,
        predecessor=body_model_snapshot_hash(before),
    )
    with pytest.raises(ValidationError, match="recovery requires"):
        audit_sensorimotor_transition(
            instance(),
            before,
            pred,
            obs,
            after,
            SensorimotorDisposition.RECORD_RECOVERY,
        )


def test_recovery_cannot_create_new_perturbation() -> None:
    before = snapshot(snapshot_id="s0", sequence=0, left_arm=RegionCondition.BASELINE)
    pred = prediction(before)
    obs = observation(pred, pred.expected_feedback_text)
    after = snapshot(
        snapshot_id="s1",
        sequence=1,
        left_arm=RegionCondition.PERTURBED,
        predecessor=body_model_snapshot_hash(before),
    )
    with pytest.raises(ValidationError, match="PERTURBED -> BASELINE"):
        audit_sensorimotor_transition(
            instance(),
            before,
            pred,
            obs,
            after,
            SensorimotorDisposition.RECORD_RECOVERY,
        )


def test_cross_twin_body_model_binding_is_rejected() -> None:
    before = snapshot(snapshot_id="s0", sequence=0, left_arm=RegionCondition.BASELINE)
    pred = prediction(before)
    obs = observation(pred, "unexpected")
    after = snapshot(
        snapshot_id="s1",
        sequence=1,
        left_arm=RegionCondition.BASELINE,
        predecessor=body_model_snapshot_hash(before),
    )
    with pytest.raises(ValidationError, match="selected embodiment instance"):
        audit_sensorimotor_transition(
            instance("BODY-ASTRA"),
            before,
            pred,
            obs,
            after,
            SensorimotorDisposition.HOLD,
        )


@pytest.mark.parametrize(
    "field,value,match",
    [
        ("synthetic", False, "synthetic records only"),
        ("live_execution", True, "live sensor or execution"),
        ("human_participant_observed", True, "human participant"),
        ("contains_private_material", True, "private material"),
    ],
)
def test_prediction_privacy_and_execution_boundaries_fail_closed(
    field: str,
    value: object,
    match: str,
) -> None:
    before = snapshot(snapshot_id="s0", sequence=0, left_arm=RegionCondition.BASELINE)
    with pytest.raises(ValidationError, match=match):
        replace(prediction(before), **{field: value})


def test_body_model_region_set_drift_is_rejected() -> None:
    before = snapshot(snapshot_id="s0", sequence=0, left_arm=RegionCondition.BASELINE)
    pred = prediction(before)
    obs = observation(pred, "unexpected")
    after = BodyModelSnapshot(
        snapshot_id="s1",
        embodiment_id="BODY-AION",
        sequence=1,
        regions=(
            BodyRegionState("core", RegionCondition.BASELINE),
            BodyRegionState("left-arm", RegionCondition.PERTURBED),
        ),
        predecessor_snapshot_sha256=body_model_snapshot_hash(before),
    )
    with pytest.raises(ValidationError, match="region set cannot drift"):
        audit_sensorimotor_transition(
            instance(),
            before,
            pred,
            obs,
            after,
            SensorimotorDisposition.LOCALIZE_PERTURBATION,
        )


def test_canonical_effect_and_subjective_body_claims_remain_blocked() -> None:
    with pytest.raises(ValidationError, match="no canonical effect"):
        replace(
            snapshot(snapshot_id="s0", sequence=0, left_arm=RegionCondition.BASELINE),
            canonical_effect="PROMOTE",
        )

    bad_instance = replace(instance(), body_sensation="ESTABLISHED")
    before = snapshot(snapshot_id="s0", sequence=0, left_arm=RegionCondition.BASELINE)
    pred = prediction(before)
    obs = observation(pred, "unexpected")
    after = snapshot(
        snapshot_id="s1",
        sequence=1,
        left_arm=RegionCondition.BASELINE,
        predecessor=body_model_snapshot_hash(before),
    )
    with pytest.raises(ValidationError, match="Body sensation|body sensation"):
        audit_sensorimotor_transition(
            bad_instance,
            before,
            pred,
            obs,
            after,
            SensorimotorDisposition.HOLD,
        )