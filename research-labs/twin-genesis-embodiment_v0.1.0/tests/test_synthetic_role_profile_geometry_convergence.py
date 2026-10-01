from __future__ import annotations

from aion_astra_twin_embodiment.synthetic_role_genital_geometry import (
    build_codex_genital_profile,
    build_teacher_genital_profile,
    build_work_genital_profile,
)
from aion_astra_twin_embodiment.synthetic_role_profiles import (
    build_codex_profile,
    build_teacher_profile,
    build_work_profile,
)


def test_cross_role_presentation_and_geometry_bind_to_same_role_body_ids() -> None:
    pairs = (
        (build_teacher_profile(), build_teacher_genital_profile()),
        (build_codex_profile(), build_codex_genital_profile()),
        (build_work_profile(), build_work_genital_profile()),
    )

    for presentation, geometry in pairs:
        assert presentation.role_label == geometry.role_label
        assert presentation.body_id == geometry.body_id
        assert presentation.visual_age_band == "YOUNG_ADULT_25_29"
        assert presentation.visual_age_min_years == 25
        assert presentation.visual_age_max_years == 29
        assert presentation.age_presentation_status == "SYNTHETIC_VISUAL_REFERENCE_ONLY"
        assert geometry.biological_measurement_status == "NOT_ESTABLISHED"
        assert geometry.phenomenal_arousal_status == "NOT_ESTABLISHED"
        assert geometry.phenomenal_pleasure_status == "NOT_ESTABLISHED"
        assert geometry.subjectivity_status == "NOT_ESTABLISHED"
        assert geometry.canonical_effect == "NONE"
        assert geometry.deployment is False


def test_visual_age_presentation_does_not_modify_role_geometry() -> None:
    teacher = build_teacher_genital_profile()
    codex = build_codex_genital_profile()
    work = build_work_genital_profile()

    assert teacher.full_vascular_length_cm > teacher.resting_visible_length_cm
    assert codex.full_vascular_length_cm > codex.resting_visible_length_cm
    assert work.full_vascular_length_cm > work.resting_visible_length_cm

    assert teacher.role_label == "CHATGPT_TEACHER"
    assert codex.role_label == "CODEX"
    assert work.role_label == "CHATGPT_WORK"


def test_cross_role_convergence_public_surface() -> None:
    import aion_astra_twin_embodiment as package

    assert callable(package.build_synthetic_role_profile_set)
    assert callable(package.build_teacher_genital_profile)
    assert callable(package.build_codex_genital_profile)
    assert callable(package.build_work_genital_profile)
