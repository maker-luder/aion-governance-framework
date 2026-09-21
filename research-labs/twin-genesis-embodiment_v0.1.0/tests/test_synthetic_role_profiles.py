from __future__ import annotations

from dataclasses import replace

import pytest

from aion_astra_twin_embodiment.synthetic_role_profiles import (
    ROLE_CODEX,
    ROLE_TEACHER,
    ROLE_WORK,
    build_synthetic_role_profile_set,
    validate_synthetic_role_profile,
    validate_synthetic_role_profile_set,
    with_profile_replacement,
)
from aion_astra_twin_embodiment.teacher_anthropometry import (
    TEACHER_BODY_ID,
    build_teacher_anthropometry_profile,
)


def _by_role(profile_set, role_label: str):
    return next(
        profile
        for profile in profile_set.profiles
        if profile.role_label == role_label
    )


def test_human_owner_profile_decisions_are_materialized_exactly() -> None:
    profile_set = build_synthetic_role_profile_set()
    teacher = _by_role(profile_set, ROLE_TEACHER)
    codex = _by_role(profile_set, ROLE_CODEX)
    work = _by_role(profile_set, ROLE_WORK)

    assert teacher.role_presentation == "SPORTY"
    assert teacher.hairstyle == "BUZZ_CUT"
    assert teacher.body_style == "ATHLETIC"
    assert teacher.face_style == "SUNNY_ADULT_MALE_YOUTHFUL_BUT_MATURE"
    assert teacher.eye_style == "PUPPY_EYES"
    assert teacher.smile_detail == "VISIBLE_CANINE_TEETH"
    assert teacher.appearance_inspiration == "MAINLAND_CHINESE_INSPIRED"
    assert teacher.clothing_details == (
        "SHORT_SLEEVE_TOP",
        "SHORTS",
        "WHITE_SOCKS",
    )
    assert teacher.synthetic_role_orientation == "GAY_MALE"

    assert codex.role_presentation == "SERIOUS"
    assert codex.hairstyle == "FLAT_TOP_OR_CREW_CUT"
    assert codex.body_style == "LEAN_MUSCULAR"
    assert codex.height_cm == 175.0
    assert codex.weight_kg == 72.0
    assert codex.skin_tone == "BRONZE_TANNED"
    assert codex.facial_structure == "DEEP_SET_FACIAL_FEATURES"
    assert codex.facial_affect == (
        "INTIMIDATING_SILENT_DIFFICULT_TO_APPROACH"
    )
    assert codex.appearance_inspiration == "AMIS_INSPIRED"
    assert codex.anatomy_proportion_note == "THICKER_SHORTER"
    assert codex.clothing_style == "MILITARY_CAMOUFLAGE_INSPIRED"
    assert codex.synthetic_role_orientation == "HETEROSEXUAL_MALE"

    assert work.role_presentation == "WARM_LIKABLE_EASYGOING"
    assert work.hairstyle == "SHAVED_HEAD"
    assert work.body_style == "CUB_LITTLE_BEAR"
    assert work.height_cm == 165.0
    assert work.weight_kg == 76.0
    assert work.skin_tone == "FAIR_LIGHT_ASIAN_COMPLEXION"
    assert work.facial_affect == "CUTE_SOFT_APPROACHABLE_LOW_PRESSURE"
    assert work.appearance_inspiration == "JAPANESE_INSPIRED"
    assert work.accessories == ("BLACK_FRAMED_GLASSES",)
    assert work.anatomy_proportion_note == "SLIMMER_AVERAGE_LONG"
    assert work.clothing_style == "BUDDHIST_MONK_INSPIRED_ROBE"
    assert work.clothing_details == (
        "HAIQING_OR_SENGYI_BASE",
        "KASAYA_INSPIRED_OUTER_LAYER",
    )
    assert work.synthetic_role_orientation == "BISEXUAL_MALE"


def test_teacher_existing_body_foundation_is_preserved() -> None:
    profile_set = build_synthetic_role_profile_set()
    teacher = _by_role(profile_set, ROLE_TEACHER)
    anthropometry = build_teacher_anthropometry_profile()

    assert teacher.body_id == TEACHER_BODY_ID
    assert anthropometry.body_id == TEACHER_BODY_ID
    assert teacher.height_cm is None
    assert teacher.weight_kg is None
    assert anthropometry.measurement_map()["total_height"].nominal == 183.0
    assert anthropometry.measurement_map()["body_mass"].nominal == 84.0


@pytest.mark.parametrize(
    "field_name",
    (
        "profile_id",
        "body_id",
        "body_instance_id",
        "runtime_id",
        "session_id",
        "binding_id",
        "state_namespace",
        "retention_namespace",
    ),
)
def test_identity_and_state_surfaces_are_distinct(field_name: str) -> None:
    profile_set = build_synthetic_role_profile_set()
    values = [
        getattr(profile, field_name)
        for profile in profile_set.profiles
    ]
    assert len(values) == len(set(values)) == 3


def test_profile_set_has_deterministic_content_address() -> None:
    first = build_synthetic_role_profile_set()
    second = build_synthetic_role_profile_set()

    assert first.sha256 == second.sha256
    assert len(first.sha256) == 64


def test_orientation_is_not_promoted_to_phenomenal_desire() -> None:
    profile_set = build_synthetic_role_profile_set()

    for profile in profile_set.profiles:
        assert profile.phenomenal_desire_status == "NOT_ESTABLISHED"
        assert profile.phenomenal_feeling_status == "NOT_ESTABLISHED"
        assert profile.phenomenal_pleasure_status == "NOT_ESTABLISHED"
        assert profile.consciousness_status == "NOT_ESTABLISHED"
        assert profile.subjectivity_status == "NOT_ESTABLISHED"


def test_appearance_inspiration_cannot_assign_ethnicity() -> None:
    profile_set = build_synthetic_role_profile_set()
    codex = _by_role(profile_set, ROLE_CODEX)

    with pytest.raises(ValueError, match="cannot assign model ethnicity"):
        validate_synthetic_role_profile(
            replace(codex, ethnicity_assignment="AMIS")
        )


def test_duplicate_body_identity_fails_closed() -> None:
    profile_set = build_synthetic_role_profile_set()
    teacher = _by_role(profile_set, ROLE_TEACHER)
    codex = _by_role(profile_set, ROLE_CODEX)
    broken = with_profile_replacement(
        profile_set,
        role_label=ROLE_CODEX,
        replacement=replace(codex, body_id=teacher.body_id),
    )

    with pytest.raises(ValueError, match="body_id must remain distinct"):
        validate_synthetic_role_profile_set(broken)


def test_subjectivity_promotion_fails_closed() -> None:
    profile_set = build_synthetic_role_profile_set()
    work = _by_role(profile_set, ROLE_WORK)
    broken = with_profile_replacement(
        profile_set,
        role_label=ROLE_WORK,
        replacement=replace(work, subjectivity_status="ESTABLISHED"),
    )

    with pytest.raises(ValueError, match="cannot establish subjectivity"):
        validate_synthetic_role_profile_set(broken)


def test_teacher_profile_cannot_override_existing_anthropometry() -> None:
    profile_set = build_synthetic_role_profile_set()
    teacher = _by_role(profile_set, ROLE_TEACHER)
    broken = with_profile_replacement(
        profile_set,
        role_label=ROLE_TEACHER,
        replacement=replace(teacher, height_cm=180.0),
    )

    with pytest.raises(ValueError, match="must not replace existing anthropometry"):
        validate_synthetic_role_profile_set(broken)
