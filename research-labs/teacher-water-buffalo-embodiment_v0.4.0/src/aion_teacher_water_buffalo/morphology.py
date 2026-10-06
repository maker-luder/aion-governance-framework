from __future__ import annotations

from dataclasses import dataclass
from typing import Final

SYNTHETIC_DESIGN: Final[str] = "SYNTHETIC_DESIGN"

@dataclass(frozen=True, slots=True)
class SyntheticMorphometry:
    provenance: str = SYNTHETIC_DESIGN
    standing_height_cm: float = 185.0
    body_mass_kg: float = 126.0
    shoulder_breadth_cm: float = 58.0
    chest_circumference_cm: float = 132.0
    waist_circumference_cm: float = 120.0
    hip_circumference_cm: float = 122.0
    neck_circumference_cm: float = 48.0

    head_height_cm: float = 27.0
    head_width_cm: float = 22.0
    jaw_width_cm: float = 19.5
    face_length_cm: float = 20.0
    human_like_nose_width_cm: float = 4.2
    human_like_nose_projection_cm: float = 2.4

    horn_count: int = 2
    horn_length_each_cm: float = 36.0
    horn_base_diameter_cm: float = 5.8
    horn_tip_to_tip_span_cm: float = 76.0
    bovine_ear_length_cm: float = 19.0
    bovine_ear_width_cm: float = 8.5

    external_hair_length_cm: float = 8.0
    tail_length_cm: float = 70.0

    arm_span_cm: float = 192.0
    upper_arm_length_cm: float = 35.0
    forearm_length_cm: float = 30.0
    hand_length_cm: float = 21.0
    palm_width_cm: float = 10.5
    hand_digit_count: int = 5

    thigh_length_cm: float = 50.0
    lower_leg_length_cm: float = 46.0
    foot_length_cm: float = 30.0
    foot_width_cm: float = 11.5
    foot_digit_count: int = 5

    body_habitus: str = "HEAVYSET"
    skin_phenotype: str = "WHITE"
    craniofacial_shape: str = "SQUARE_FACE"
    ear_morphology: str = "BOVINE_EARS"
    nose_morphology: str = "HUMAN_LIKE_NOSE"
    hair_phenotype: str = "LONG_HAIR"
    distal_limb_morphology: str = "HUMANIZED_HOOF_DERIVED_HANDS_AND_FEET"
    distal_keratin_expression: str = "HOOF_DERIVED_NAIL_PLATES"
