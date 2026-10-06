from __future__ import annotations

from aion_astra_twin_embodiment.body_dimensions import (
    COMMUNITY_DESIGN_REFERENCE,
    DESIGN_TARGET,
    ENGINEERING_DESIGN_CHOICE,
    HUMAN_ANTHROPOMETRY_REFERENCE,
    REFERENCE_OBSERVATION,
    TIGER_CONFIRMED,
    UNKNOWN_SOURCE_NOT_ESTABLISHED,
    build_aion_tiger_full_dimension_preset,
    validate_aion_tiger_dimension_preset,
)


def test_full_dimension_preset_validates():
    preset = build_aion_tiger_full_dimension_preset()
    result = validate_aion_tiger_dimension_preset(preset)
    assert result["result"] == "PASS"
    assert int(result["dimension_count"]) >= 40


def test_global_body_has_concrete_modeling_dimensions():
    m = build_aion_tiger_full_dimension_preset().measurement_map()
    assert m["stature_cm"].value == 190.0
    assert m["shoulder_breadth_cm"].value == 54.0
    assert m["chest_circumference_cm"].value == 118.0
    assert m["tail_length_cm"].value == 105.0
    assert m["hindpaw_length_cm"].value == 31.0


def test_furry_community_is_design_reference_not_biology():
    m = build_aion_tiger_full_dimension_preset().measurement_map()
    item = m["tail_base_diameter_cm"]
    assert COMMUNITY_DESIGN_REFERENCE in item.provenance
    assert ENGINEERING_DESIGN_CHOICE in item.provenance
    assert item.measurement_role == DESIGN_TARGET


def test_human_anthropometry_and_tiger_reference_can_coexist():
    m = build_aion_tiger_full_dimension_preset().measurement_map()
    shoulder = m["shoulder_breadth_cm"]
    assert HUMAN_ANTHROPOMETRY_REFERENCE in shoulder.provenance
    assert TIGER_CONFIRMED in shoulder.provenance


def test_tiger_reproductive_measurements_are_reference_observations():
    m = build_aion_tiger_full_dimension_preset().measurement_map()
    testis = m["tiger_reference_right_testis_length_cm"]
    urethra = m["tiger_reference_penile_urethra_diameter_mm"]
    assert testis.value == 4.42
    assert urethra.value == 1.73
    assert testis.measurement_role == REFERENCE_OBSERVATION
    assert testis.provenance == (TIGER_CONFIRMED,)


def test_missing_direct_genital_dimension_is_not_fabricated():
    m = build_aion_tiger_full_dimension_preset().measurement_map()
    item = m["aion_total_penile_length_cm"]
    assert item.value is None
    assert item.status == UNKNOWN_SOURCE_NOT_ESTABLISHED


def test_semi_realistic_head_ratio_and_tail_constraint():
    m = build_aion_tiger_full_dimension_preset().measurement_map()
    stature = m["stature_cm"].value
    head = m["head_height_cm"].value
    tail = m["tail_length_cm"].value
    assert stature is not None and head is not None and tail is not None
    assert head / stature == 0.2
    assert tail < stature
