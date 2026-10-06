from __future__ import annotations

from aion_astra_twin_embodiment.body_dimensions import DESIGN_TARGET
from aion_astra_twin_embodiment.body_dimensions_v2 import build_aion_tiger_full_dimension_preset_v2
from aion_astra_twin_embodiment.measurement_protocols import (
    build_aion_tiger_measurement_protocols,
    validate_aion_tiger_measurement_protocols,
)


def test_protocol_surface_covers_every_design_target():
    result = validate_aion_tiger_measurement_protocols()
    assert result["result"] == "PASS"
    assert int(result["protocol_count"]) >= 90


def test_reference_observations_do_not_become_model_measurement_protocols():
    preset = build_aion_tiger_full_dimension_preset_v2()
    target_keys = {item.key for item in preset.measurements if item.measurement_role == DESIGN_TARGET}
    protocol_keys = {item.dimension_key for item in build_aion_tiger_measurement_protocols()}
    assert protocol_keys == target_keys
    assert "tiger_reference_humerus_length_right_cm" not in protocol_keys


def test_protocol_distinguishes_fur_padding_from_internal_anatomy():
    protocols = {item.dimension_key: item for item in build_aion_tiger_measurement_protocols()}
    fur = protocols["tail_fur_visual_depth_cm"]
    foot = protocols["internal_human_foot_length_cm"]
    assert "fur/padding" in fur.quality_gate_zh
    assert foot.pose == "NEUTRAL_WEIGHT_BEARING_STANCE"
