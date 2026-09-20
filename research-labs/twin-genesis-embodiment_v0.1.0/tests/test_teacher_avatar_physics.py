from __future__ import annotations

from aion_astra_twin_embodiment.teacher_avatar_physics import (
    build_teacher_collision_profile,
    validate_teacher_collision_profile,
)


def test_teacher_collision_profile_materializes_full_reference_coverage() -> None:
    profile = build_teacher_collision_profile()
    result = validate_teacher_collision_profile(profile)

    assert result["result"] == "PASS"
    regions = {proxy.region for proxy in profile.proxies}
    assert "HEAD" in regions
    assert "TORSO" in regions
    assert "HANDS" in regions
    assert "FEET" in regions
    assert "EXTERNAL_MALE_ANATOMY" in regions


def test_teacher_collision_profile_preserves_anatomy_boundaries() -> None:
    profile = build_teacher_collision_profile()
    anatomy = [
        proxy
        for proxy in profile.proxies
        if proxy.region == "EXTERNAL_MALE_ANATOMY"
    ]

    assert len(anatomy) >= 2
    assert all(proxy.anatomy_scope == "CLINICAL_EXTERNAL_ANATOMY" for proxy in anatomy)
    assert profile.sexual_function_status == "NOT_IMPLEMENTED"
    assert profile.intimate_interaction_status == "NOT_AUTHORIZED"
    assert profile.physical_body_claim == "NONE"
    assert profile.subjectivity_effect == "NONE"
    assert profile.production_physics_status == "NOT_ESTABLISHED"
    assert profile.canonical_effect == "NONE"
    assert profile.deployment is False
