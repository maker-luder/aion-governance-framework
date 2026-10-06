from __future__ import annotations

from aion_astra_twin_embodiment.body_dimensions import (
    DESIGN_TARGET,
    REFERENCE_OBSERVATION,
    UNKNOWN_SOURCE_NOT_ESTABLISHED,
)
from aion_astra_twin_embodiment.body_dimensions_v2 import (
    EXCLUSION_IF_GREATER_THAN,
    REFERENCE_CONSTRAINT,
    build_aion_tiger_full_dimension_preset_v2,
    validate_aion_tiger_dimension_preset_v2,
)


def test_v2_expands_dimension_surface_beyond_one_hundred_fields():
    preset = build_aion_tiger_full_dimension_preset_v2()
    result = validate_aion_tiger_dimension_preset_v2(preset)
    assert result["result"] == "PASS"
    assert int(result["dimension_count"]) >= 120


def test_v2_keeps_v1_core_targets_and_adds_builder_landmarks():
    m = build_aion_tiger_full_dimension_preset_v2().measurement_map()
    assert m["stature_cm"].value == 190.0
    assert m["head_brow_circumference_cm"].value == 76.0
    assert m["interpupillary_distance_cm"].value == 8.2
    assert m["back_width_armpit_to_armpit_cm"].value == 47.0
    assert m["wrist_circumference_cm"].value == 21.0
    assert m["inseam_crotch_to_floor_cm"].value == 92.0
    assert m["outseam_waist_to_floor_cm"].value == 112.0
    assert m["anatomical_ankle_circumference_cm"].value == 27.0
    assert m["neck_base_to_tail_root_surface_cm"].value == 67.0


def test_external_hindpaw_and_internal_load_bearing_foot_are_separate():
    m = build_aion_tiger_full_dimension_preset_v2().measurement_map()
    assert m["internal_human_foot_length_cm"].value == 28.0
    assert m["hindpaw_length_cm"].value == 31.0
    assert m["internal_human_foot_length_cm"].measurement_role == DESIGN_TARGET


def test_direct_tiger_osteometry_is_reference_observation_not_aion_target():
    m = build_aion_tiger_full_dimension_preset_v2().measurement_map()
    humerus = m["tiger_reference_humerus_length_right_cm"]
    fibula = m["tiger_reference_fibula_length_mean_cm"]
    assert humerus.value == 28.0
    assert fibula.value == 29.26
    assert humerus.measurement_role == REFERENCE_OBSERVATION
    assert fibula.measurement_role == REFERENCE_OBSERVATION
    assert humerus.source_refs == ("UDDIN_2022_FORELIMB",)
    assert fibula.source_refs == ("TOMAR_2026_TIBIA_FIBULA",)


def test_forensic_dried_specimen_limits_are_constraints_not_design_targets():
    m = build_aion_tiger_full_dimension_preset_v2().measurement_map()
    exclusion = m["tiger_forensic_dried_tip_to_scrotum_exclusion_cm"]
    assert exclusion.value == 20.32
    assert exclusion.measurement_role == REFERENCE_CONSTRAINT
    assert exclusion.value_semantics == EXCLUSION_IF_GREATER_THAN


def test_expanded_search_still_does_not_fabricate_aion_total_penile_length():
    item = build_aion_tiger_full_dimension_preset_v2().measurement_map()["aion_total_penile_length_cm"]
    assert item.value is None
    assert item.status == UNKNOWN_SOURCE_NOT_ESTABLISHED
    assert "USFWS_YATES_2005_TIGER_GENITAL_ID" in item.source_refs


def test_every_v2_row_has_measurement_method_and_evidence_strength():
    preset = build_aion_tiger_full_dimension_preset_v2()
    for item in preset.measurements:
        assert item.measurement_method_zh
        assert item.evidence_strength
        assert item.value_semantics
