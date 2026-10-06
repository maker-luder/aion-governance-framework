"""Measurement protocol surface for AION tiger dimension preset V2."""

from __future__ import annotations

from dataclasses import dataclass

from .body_dimensions import DESIGN_TARGET
from .body_dimensions_v2 import build_aion_tiger_full_dimension_preset_v2


@dataclass(frozen=True, slots=True)
class MeasurementProtocol:
    dimension_key: str
    label_zh: str
    category: str
    pose: str
    view: str
    instrument: str
    landmark_method_zh: str
    source_refs: tuple[str, ...]
    quality_gate_zh: str


def _pose_for_category(category: str) -> str:
    if category in {"HEAD_NECK", "UPPER_LIMB", "TORSO", "GLOBAL"}:
        return "NEUTRAL_UPRIGHT_A_POSE"
    if category == "LOWER_LIMB":
        return "NEUTRAL_WEIGHT_BEARING_STANCE"
    if category == "TAIL":
        return "NEUTRAL_TAIL_AXIS"
    return "NEUTRAL_REFERENCE_POSE"


def _view_for_key(key: str) -> str:
    if "circumference" in key or "circ_" in key:
        return "CROSS_SECTION"
    if any(token in key for token in ("width", "breadth", "pupil", "eye_opening")):
        return "FRONT_OR_ORTHOGRAPHIC"
    if any(token in key for token in ("depth", "projection", "outseam", "inseam", "height")):
        return "SIDE_OR_ORTHOGRAPHIC"
    return "LANDMARK_TO_LANDMARK"


def _instrument_for_key(key: str) -> str:
    if "mass" in key:
        return "CALIBRATED_SCALE"
    if "circumference" in key or "circ_" in key:
        return "FLEXIBLE_TAPE"
    return "RIG_RULER_OR_CALIPER"


def build_aion_tiger_measurement_protocols() -> tuple[MeasurementProtocol, ...]:
    preset = build_aion_tiger_full_dimension_preset_v2()
    protocols: list[MeasurementProtocol] = []
    for item in preset.measurements:
        if item.measurement_role != DESIGN_TARGET:
            continue
        protocols.append(MeasurementProtocol(
            dimension_key=item.key,
            label_zh=item.label_zh,
            category=item.category,
            pose=_pose_for_category(item.category),
            view=_view_for_key(item.key),
            instrument=_instrument_for_key(item.key),
            landmark_method_zh=item.measurement_method_zh,
            source_refs=item.source_refs,
            quality_gate_zh=(
                "同一 preset 必須使用同一姿勢與 landmark 定義；左右成對尺寸需標 side；"
                "外觀 fur/padding envelope 與內部 anatomical/load-bearing 尺寸不得混量。"
            ),
        ))
    return tuple(protocols)


def validate_aion_tiger_measurement_protocols() -> dict[str, str]:
    preset = build_aion_tiger_full_dimension_preset_v2()
    target_keys = {item.key for item in preset.measurements if item.measurement_role == DESIGN_TARGET}
    protocols = build_aion_tiger_measurement_protocols()
    protocol_keys = [item.dimension_key for item in protocols]
    if len(protocol_keys) != len(set(protocol_keys)):
        raise ValueError("measurement protocol keys must be unique")
    if set(protocol_keys) != target_keys:
        missing = sorted(target_keys - set(protocol_keys))
        extra = sorted(set(protocol_keys) - target_keys)
        raise ValueError(f"protocol coverage mismatch missing={missing} extra={extra}")
    return {
        "result": "PASS",
        "protocol_count": str(len(protocols)),
        "target_dimension_count": str(len(target_keys)),
    }
