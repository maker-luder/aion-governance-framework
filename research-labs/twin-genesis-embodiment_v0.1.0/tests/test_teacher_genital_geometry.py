from __future__ import annotations

from dataclasses import replace

import pytest

from aion_astra_twin_embodiment.teacher_body_dynamics import (
    TeacherBodyObservation,
    integrate_teacher_body_state,
)
from aion_astra_twin_embodiment.teacher_body_runtime import (
    bind_teacher_integrated_body_state,
    build_teacher_body_runtime_binding,
)
from aion_astra_twin_embodiment.teacher_genital_geometry import (
    CIRCUMFERENCE_TRANSFORM_RATIO,
    LENGTH_TRANSFORM_RATIO,
    build_teacher_bound_genital_geometry_state,
    build_teacher_genital_geometry_profile,
    validate_teacher_bound_genital_geometry_state,
)


def _state(
    *,
    vascular_fill: float,
    erectile_reflex: float,
    detumescence: float,
    sequence: int = 1,
):
    return integrate_teacher_body_state(
        (
            TeacherBodyObservation("TACTILE_GENERAL", (0.2,), 100),
            TeacherBodyObservation("JOINT_POSITION", (0.1,), 100),
            TeacherBodyObservation(
                "VESTIBULAR_ORIENTATION",
                (1.0, 0.0, 0.0, 0.0),
                100,
            ),
            TeacherBodyObservation("CARDIOVASCULAR_STATE", (0.5,), 100),
            TeacherBodyObservation(
                "GENITAL_VASCULAR_STATE",
                (vascular_fill,),
                100,
            ),
            TeacherBodyObservation(
                "ERECTILE_REFLEX_STATE",
                (erectile_reflex,),
                100,
            ),
            TeacherBodyObservation(
                "DETUMESCENCE_STATE",
                (detumescence,),
                100,
            ),
        ),
        sequence=sequence,
    )


def _bound(state):
    binding = build_teacher_body_runtime_binding(
        "RUNTIME-GEOMETRY",
        "SESSION-GEOMETRY",
    )
    return binding, bind_teacher_integrated_body_state(binding, state)


def test_genital_geometry_profile_derives_synthetic_full_vascular_reference() -> None:
    profile = build_teacher_genital_geometry_profile()

    assert profile.baseline_visible_length_cm == 9.5
    assert profile.baseline_midshaft_circumference_cm == 10.0
    assert profile.length_transform_ratio == pytest.approx(
        13.12 / 9.16
    )
    assert profile.circumference_transform_ratio == pytest.approx(
        11.66 / 9.31
    )
    assert profile.length_transform_ratio == pytest.approx(
        LENGTH_TRANSFORM_RATIO
    )
    assert profile.circumference_transform_ratio == pytest.approx(
        CIRCUMFERENCE_TRANSFORM_RATIO
    )
    assert profile.full_vascular_reference_length_cm == pytest.approx(
        13.606986899563317
    )
    assert profile.full_vascular_reference_circumference_cm == pytest.approx(
        12.524167561761546
    )
    assert profile.population_reference_pmid == "25487360"
    assert profile.transform_basis == "SYNTHETIC_RATIO_FROM_POPULATION_MEANS"
    assert profile.individual_prediction_status == "NOT_ESTABLISHED"
    assert profile.biological_measurement_status == "NOT_ESTABLISHED"
    assert profile.phenomenal_interpretation_status == "NOT_ESTABLISHED"


def test_resting_geometry_matches_static_anthropometry() -> None:
    state = _state(
        vascular_fill=0.0,
        erectile_reflex=0.0,
        detumescence=0.0,
    )
    _, bound = _bound(state)
    geometry = build_teacher_bound_genital_geometry_state(
        bound_body_state=bound,
        body_state=state,
    )

    assert geometry.geometry_state == "RESTING_REFERENCE"
    assert geometry.effective_tumescence_fraction == 0.0
    assert geometry.visible_length_cm == pytest.approx(9.5)
    assert geometry.midshaft_circumference_cm == pytest.approx(10.0)


def test_full_vascular_geometry_reaches_synthetic_reference_target() -> None:
    state = _state(
        vascular_fill=1.0,
        erectile_reflex=1.0,
        detumescence=0.0,
    )
    _, bound = _bound(state)
    geometry = build_teacher_bound_genital_geometry_state(
        bound_body_state=bound,
        body_state=state,
    )

    assert geometry.geometry_state == "ERECT_REFERENCE"
    assert geometry.effective_tumescence_fraction == 1.0
    assert geometry.visible_length_cm == pytest.approx(
        13.606986899563317
    )
    assert geometry.midshaft_circumference_cm == pytest.approx(
        12.524167561761546
    )
    assert geometry.felt_arousal_status == "NOT_ESTABLISHED"
    assert geometry.phenomenal_pleasure_status == "NOT_ESTABLISHED"
    assert geometry.subjectivity_status == "NOT_ESTABLISHED"


def test_detumescence_returns_geometry_toward_resting_reference() -> None:
    state = _state(
        vascular_fill=1.0,
        erectile_reflex=0.5,
        detumescence=0.75,
    )
    _, bound = _bound(state)
    geometry = build_teacher_bound_genital_geometry_state(
        bound_body_state=bound,
        body_state=state,
    )

    assert geometry.geometry_state == "DETUMESCENCE_REFERENCE"
    assert geometry.effective_tumescence_fraction == pytest.approx(0.25)
    assert 9.5 < geometry.visible_length_cm < 13.606986899563317
    assert 10.0 < geometry.midshaft_circumference_cm < 12.524167561761546


def test_geometry_requires_exact_body_instance_and_required_source_channels() -> None:
    state = _state(
        vascular_fill=0.8,
        erectile_reflex=0.8,
        detumescence=0.0,
    )
    _, bound = _bound(state)

    with pytest.raises(ValueError, match="source body-state binding drift"):
        build_teacher_bound_genital_geometry_state(
            bound_body_state=replace(
                bound,
                source_body_state_sha256="0" * 64,
            ),
            body_state=state,
        )

    missing_detumescence = replace(
        state,
        observations=tuple(
            observation
            for observation in state.observations
            if observation.channel_id != "DETUMESCENCE_STATE"
        ),
    )
    with pytest.raises(
        ValueError,
        match="genital geometry requires body observation: DETUMESCENCE_STATE",
    ):
        build_teacher_bound_genital_geometry_state(
            bound_body_state=bound,
            body_state=missing_detumescence,
        )


def test_geometry_validator_rejects_tampered_normalized_state() -> None:
    state = _state(
        vascular_fill=0.8,
        erectile_reflex=0.8,
        detumescence=0.0,
    )
    _, bound = _bound(state)
    geometry = build_teacher_bound_genital_geometry_state(
        bound_body_state=bound,
        body_state=state,
    )

    with pytest.raises(ValueError, match="fractions must be normalized"):
        validate_teacher_bound_genital_geometry_state(
            replace(geometry, vascular_fill_fraction=1.5),
            bound,
            state,
        )
