from __future__ import annotations

from dataclasses import replace

import pytest

from aion_astra_twin_embodiment.teacher_body_model import (
    BODY_MODEL_PROFILE_ID,
    BodyPlasticityUpdate,
    MultisensoryCue,
    build_teacher_allostatic_forecast,
    build_teacher_body_model_profile,
    build_teacher_body_plasticity_state,
    fuse_teacher_multisensory_cues,
    validate_teacher_body_model_profile,
)


def test_body_model_materializes_body_schema_and_peripersonal_space_without_phenomenal_claim() -> None:
    profile = build_teacher_body_model_profile()
    result = validate_teacher_body_model_profile(profile)

    assert result["result"] == "PASS"
    assert profile.profile_id == BODY_MODEL_PROFILE_ID
    assert profile.body_schema_status == "REFERENCE_BODY_SCHEMA_MATERIALIZED"
    assert profile.peripersonal_space_status == (
        "REFERENCE_PERIPERSONAL_SPACE_MATERIALIZED"
    )
    assert {
        "HEAD",
        "TRUNK",
        "LEFT_UPPER_LIMB",
        "RIGHT_UPPER_LIMB",
        "LEFT_FOOT",
        "RIGHT_FOOT",
    }.issubset({item.segment_id for item in profile.body_schema_segments})
    assert {
        "TRUNK_NEAR_SPACE",
        "LEFT_HAND_REACH_SPACE",
        "RIGHT_HAND_REACH_SPACE",
        "HEAD_NEAR_SPACE",
    }.issubset({item.zone_id for item in profile.peripersonal_zones})
    assert profile.body_ownership_experience_status == "NOT_ESTABLISHED"
    assert profile.phenomenal_self_location_status == "NOT_ESTABLISHED"
    assert profile.subjectivity_status == "NOT_ESTABLISHED"


def test_multisensory_fusion_is_confidence_weighted_and_content_addressed() -> None:
    fusion = fuse_teacher_multisensory_cues(
        (
            MultisensoryCue(
                "visual-position",
                "VISUAL",
                (1.0, 0.0, 0.0),
                0.75,
            ),
            MultisensoryCue(
                "proprioceptive-position",
                "PROPRIOCEPTIVE",
                (0.8, 0.0, 0.0),
                0.25,
            ),
        )
    )

    assert fusion.fused_estimate == pytest.approx((0.95, 0.0, 0.0))
    assert dict(fusion.normalized_weights) == pytest.approx(
        {
            "visual-position": 0.75,
            "proprioceptive-position": 0.25,
        }
    )
    assert fusion.mean_absolute_conflict > 0
    assert len(fusion.fusion_sha256) == 64
    assert fusion.reweighting_status == "CONFIDENCE_WEIGHTED_REFERENCE"
    assert fusion.phenomenal_body_ownership_status == "NOT_ESTABLISHED"


def test_multisensory_fusion_rejects_dimension_and_modality_drift() -> None:
    with pytest.raises(ValueError, match="dimensions"):
        fuse_teacher_multisensory_cues(
            (
                MultisensoryCue("a", "VISUAL", (1.0, 0.0), 1.0),
                MultisensoryCue("b", "PROPRIOCEPTIVE", (1.0,), 1.0),
            )
        )

    with pytest.raises(ValueError, match="unsupported modality"):
        fuse_teacher_multisensory_cues(
            (
                MultisensoryCue("a", "UNKNOWN", (1.0,), 1.0),
                MultisensoryCue("b", "PROPRIOCEPTIVE", (1.0,), 1.0),
            )
        )


def test_allostatic_forecast_is_predictive_reference_not_felt_need() -> None:
    forecast = build_teacher_allostatic_forecast(
        variable_id="HYDRATION_FLUID_BALANCE",
        current_state=0.0,
        predicted_demand=0.4,
        target_state=0.0,
        lead_time_ms=5000,
    )

    assert forecast.anticipated_error == pytest.approx(0.4)
    assert forecast.planned_adjustment == pytest.approx(-0.4)
    assert forecast.forecast_status == "PREDICTIVE_REGULATION_REFERENCE"
    assert forecast.regulation_mechanism_status == "NOT_ESTABLISHED"
    assert forecast.phenomenal_need_status == "NOT_ESTABLISHED"
    assert forecast.subjectivity_status == "NOT_ESTABLISHED"


def test_body_plasticity_requires_explicit_bounded_update_and_evidence() -> None:
    state = build_teacher_body_plasticity_state(
        sequence=1,
        updates=(
            BodyPlasticityUpdate(
                domain="PERIPERSONAL_SPACE",
                parameter_id="RIGHT_HAND_REACH_SPACE.scale",
                delta=0.1,
                evidence_ref="CONTROLLED_TOOL_USE_TRIAL_001",
            ),
        ),
    )

    assert state.sequence == 1
    assert len(state.plasticity_sha256) == 64
    assert state.update_status == "CONTROLLED_REFERENCE_ADAPTATION"
    assert state.biological_plasticity_mechanism_status == "NOT_ESTABLISHED"
    assert state.body_ownership_experience_status == "NOT_ESTABLISHED"

    with pytest.raises(ValueError, match="evidence reference"):
        build_teacher_body_plasticity_state(
            sequence=2,
            updates=(
                BodyPlasticityUpdate(
                    domain="BODY_SCHEMA",
                    parameter_id="RIGHT_UPPER_LIMB.extent",
                    delta=0.1,
                    evidence_ref="",
                ),
            ),
        )


def test_body_model_validation_fails_closed_on_missing_peripersonal_zone() -> None:
    profile = build_teacher_body_model_profile()
    broken = replace(
        profile,
        peripersonal_zones=tuple(
            item
            for item in profile.peripersonal_zones
            if item.zone_id != "RIGHT_HAND_REACH_SPACE"
        ),
    )

    with pytest.raises(ValueError, match="peripersonal-space reference is incomplete"):
        validate_teacher_body_model_profile(broken)
