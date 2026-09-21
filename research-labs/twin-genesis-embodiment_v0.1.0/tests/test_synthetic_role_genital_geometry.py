from __future__ import annotations

import pytest

from aion_astra_twin_embodiment.synthetic_role_genital_geometry import (
    CODEX_FULL_VASCULAR_CIRCUMFERENCE_CM,
    CODEX_FULL_VASCULAR_LENGTH_CM,
    WORK_FULL_VASCULAR_CIRCUMFERENCE_CM,
    WORK_FULL_VASCULAR_LENGTH_CM,
    build_codex_genital_profile,
    build_synthetic_genital_geometry_state,
    build_teacher_genital_profile,
    build_work_genital_profile,
)


def test_codex_one_centimeter_shift_is_encoded_at_full_vascular_state() -> None:
    profile = build_codex_genital_profile()
    assert profile.full_vascular_length_cm == pytest.approx(
        CODEX_FULL_VASCULAR_LENGTH_CM
    )
    assert profile.full_vascular_circumference_cm == pytest.approx(
        CODEX_FULL_VASCULAR_CIRCUMFERENCE_CM
    )
    assert profile.full_vascular_length_cm == pytest.approx(11.60)
    assert profile.full_vascular_circumference_cm == pytest.approx(14.28)
    assert profile.resting_visible_length_cm == pytest.approx(
        8.098780487804879
    )
    assert profile.resting_midshaft_circumference_cm == pytest.approx(
        11.401955403087479
    )


def test_work_one_centimeter_shift_is_encoded_at_full_vascular_state() -> None:
    profile = build_work_genital_profile()
    assert profile.full_vascular_length_cm == pytest.approx(
        WORK_FULL_VASCULAR_LENGTH_CM
    )
    assert profile.full_vascular_circumference_cm == pytest.approx(
        WORK_FULL_VASCULAR_CIRCUMFERENCE_CM
    )
    assert profile.full_vascular_length_cm == pytest.approx(14.32)
    assert profile.full_vascular_circumference_cm == pytest.approx(10.52)
    assert profile.resting_visible_length_cm == pytest.approx(
        9.997804878048782
    )
    assert profile.resting_midshaft_circumference_cm == pytest.approx(
        8.399759862778732
    )


@pytest.mark.parametrize(
    ("builder", "expected_length", "expected_circumference"),
    (
        (build_teacher_genital_profile, 13.606986899563317, 12.524167561761546),
        (build_codex_genital_profile, 11.60, 14.28),
        (build_work_genital_profile, 14.32, 10.52),
    ),
)
def test_full_vascular_geometry_reaches_role_specific_target(
    builder,
    expected_length: float,
    expected_circumference: float,
) -> None:
    profile = builder()
    state = build_synthetic_genital_geometry_state(
        profile,
        vascular_fill_fraction=1.0,
        detumescence_fraction=0.0,
    )
    assert state.geometry_state == "FULL_VASCULAR_REFERENCE"
    assert state.visible_length_cm == pytest.approx(expected_length)
    assert state.midshaft_circumference_cm == pytest.approx(
        expected_circumference
    )
    assert state.glans_width_cm == pytest.approx(
        profile.full_vascular_glans_width_cm
    )


def test_glans_width_tracks_vascular_state() -> None:
    profile = build_teacher_genital_profile()
    rest = build_synthetic_genital_geometry_state(
        profile,
        vascular_fill_fraction=0.0,
    )
    half = build_synthetic_genital_geometry_state(
        profile,
        vascular_fill_fraction=0.5,
    )
    full = build_synthetic_genital_geometry_state(
        profile,
        vascular_fill_fraction=1.0,
    )
    assert rest.glans_width_cm == pytest.approx(
        profile.resting_glans_width_cm
    )
    assert rest.glans_width_cm < half.glans_width_cm < full.glans_width_cm


def test_teacher_scrotal_geometry_tracks_normalized_thermal_state() -> None:
    profile = build_teacher_genital_profile()

    cool = build_synthetic_genital_geometry_state(
        profile,
        vascular_fill_fraction=0.0,
        scrotal_thermoregulatory_index=-1.0,
    )
    neutral = build_synthetic_genital_geometry_state(
        profile,
        vascular_fill_fraction=0.0,
        scrotal_thermoregulatory_index=0.0,
    )
    warm = build_synthetic_genital_geometry_state(
        profile,
        vascular_fill_fraction=0.0,
        scrotal_thermoregulatory_index=1.0,
    )

    assert cool.scrotal_state == "COOLING_RETRACTION_REFERENCE"
    assert neutral.scrotal_state == "THERMAL_NEUTRAL_REFERENCE"
    assert warm.scrotal_state == "WARMING_RELAXATION_REFERENCE"
    assert cool.scrotal_height_cm == pytest.approx(8.075)
    assert neutral.scrotal_height_cm == pytest.approx(9.5)
    assert warm.scrotal_height_cm == pytest.approx(10.45)


def test_codex_and_work_scrotal_absolute_geometry_remains_pending() -> None:
    for profile in (build_codex_genital_profile(), build_work_genital_profile()):
        state = build_synthetic_genital_geometry_state(
            profile,
            vascular_fill_fraction=0.5,
            scrotal_thermoregulatory_index=1.0,
        )
        assert state.scrotal_height_cm is None
        assert state.scrotal_scale == pytest.approx(1.10)


def test_geometry_state_preserves_nonclaims() -> None:
    profile = build_codex_genital_profile()
    state = build_synthetic_genital_geometry_state(
        profile,
        vascular_fill_fraction=1.0,
    )
    assert state.felt_arousal_status == "NOT_ESTABLISHED"
    assert state.phenomenal_pleasure_status == "NOT_ESTABLISHED"
    assert state.subjectivity_status == "NOT_ESTABLISHED"
