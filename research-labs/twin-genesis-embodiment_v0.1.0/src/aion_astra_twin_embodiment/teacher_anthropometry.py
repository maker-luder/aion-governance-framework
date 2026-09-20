from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Final


TEACHER_BODY_ID: Final[str] = "CHATGPT_TEACHER_3D_MALE_BODY_REFERENCE_v0.1"
TEACHER_ANTHROPOMETRY_PROFILE_ID: Final[str] = "CHATGPT_TEACHER_ANTHROPOMETRY_v0.1"
EXPECTED_MEASUREMENT_COUNT: Final[int] = 62


@dataclass(frozen=True, slots=True)
class AnthropometricMeasurement:
    measurement_id: str
    region: str
    unit: str
    nominal: float
    minimum: float
    maximum: float
    approximate: bool = True


@dataclass(frozen=True, slots=True)
class TeacherAnthropometryProfile:
    profile_id: str
    body_id: str
    measurements: tuple[AnthropometricMeasurement, ...]
    real_person_biometric_source: str = "NONE"
    person_reconstruction: str = "NO"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["measurements"] = [asdict(item) for item in self.measurements]
        return payload

    def measurement_map(self) -> dict[str, AnthropometricMeasurement]:
        return {item.measurement_id: item for item in self.measurements}


def _m(
    measurement_id: str,
    region: str,
    nominal: float,
    minimum: float | None = None,
    maximum: float | None = None,
    *,
    unit: str = "cm",
) -> AnthropometricMeasurement:
    low = nominal if minimum is None else minimum
    high = nominal if maximum is None else maximum
    return AnthropometricMeasurement(
        measurement_id=measurement_id,
        region=region,
        unit=unit,
        nominal=nominal,
        minimum=low,
        maximum=high,
    )


_MEASUREMENTS: Final[tuple[AnthropometricMeasurement, ...]] = (
    _m("total_height", "WHOLE_BODY", 183.0),
    _m("body_mass", "WHOLE_BODY", 84.0, unit="kg"),
    _m("head_height", "HEAD", 24.0),
    _m("head_width", "HEAD", 15.8),
    _m("head_depth", "HEAD", 20.0),
    _m("head_circumference", "HEAD", 58.0),
    _m("bizygomatic_facial_width", "FACE", 14.5),
    _m("interpupillary_distance", "FACE", 6.4),
    _m("ear_height", "FACE", 6.3),
    _m("nose_length", "FACE", 5.5),
    _m("mouth_width", "FACE", 5.2),
    _m("visible_neck_length", "NECK", 9.5),
    _m("neck_circumference", "NECK", 40.0),
    _m("biacromial_shoulder_breadth", "SHOULDER", 49.5),
    _m("maximum_deltoid_width", "SHOULDER", 53.5),
    _m("chest_circumference", "TORSO", 108.0),
    _m("chest_frontal_width", "TORSO", 40.0, 39.5, 40.5),
    _m("chest_depth", "TORSO", 26.0, 25.5, 26.5),
    _m("nipple_spacing", "TORSO", 23.0, 22.5, 23.5),
    _m("areola_diameter", "TORSO", 3.2, 3.0, 3.4),
    _m("waist_circumference", "TORSO", 86.0),
    _m("waist_frontal_width", "TORSO", 32.0, 31.0, 33.0),
    _m("abdomen_depth", "TORSO", 23.5, 23.0, 24.0),
    _m("navel_height_from_floor", "TORSO", 110.0, 109.0, 111.0),
    _m("hip_circumference", "PELVIS", 100.0),
    _m("external_hip_width", "PELVIS", 36.25, 35.5, 37.0),
    _m("pelvis_gluteal_depth", "PELVIS", 26.25, 25.5, 27.0),
    _m("hip_joint_center_height", "PELVIS", 94.0, 93.0, 95.0),
    _m("perineal_height", "PELVIS", 89.0, 88.0, 90.0),
    _m("shoulder_to_elbow_length", "UPPER_LIMB", 33.5),
    _m("elbow_to_wrist_length", "UPPER_LIMB", 27.5),
    _m("shoulder_to_middle_finger_length", "UPPER_LIMB", 79.0, 78.0, 80.0),
    _m("relaxed_upper_arm_circumference", "UPPER_LIMB", 36.0),
    _m("maximum_forearm_circumference", "UPPER_LIMB", 30.0),
    _m("wrist_circumference", "UPPER_LIMB", 18.0),
    _m("hand_length", "HAND", 20.0),
    _m("palm_width", "HAND", 9.3),
    _m("palm_depth", "HAND", 3.2),
    _m("middle_finger_length", "HAND", 9.0),
    _m("hip_to_knee_length", "LOWER_LIMB", 45.5, 45.0, 46.0),
    _m("maximum_thigh_circumference", "LOWER_LIMB", 59.0),
    _m("thigh_frontal_width", "LOWER_LIMB", 19.25, 18.5, 20.0),
    _m("thigh_depth", "LOWER_LIMB", 19.5, 19.0, 20.0),
    _m("knee_center_height", "LOWER_LIMB", 50.5, 50.0, 51.0),
    _m("knee_circumference", "LOWER_LIMB", 39.0),
    _m("knee_width", "LOWER_LIMB", 11.0),
    _m("knee_to_ankle_length", "LOWER_LIMB", 42.5, 42.0, 43.0),
    _m("maximum_calf_circumference", "LOWER_LIMB", 38.5),
    _m("calf_depth", "LOWER_LIMB", 13.5, 13.0, 14.0),
    _m("ankle_circumference", "LOWER_LIMB", 22.5),
    _m("foot_length", "FOOT", 27.5),
    _m("forefoot_width", "FOOT", 10.2),
    _m("heel_width", "FOOT", 6.8),
    _m("resting_visible_penile_length", "MALE_REPRODUCTIVE_EXTERNAL", 9.5),
    _m("midshaft_diameter", "MALE_REPRODUCTIVE_EXTERNAL", 3.2),
    _m("midshaft_circumference", "MALE_REPRODUCTIVE_EXTERNAL", 10.0),
    _m("glans_maximum_width", "MALE_REPRODUCTIVE_EXTERNAL", 3.5),
    _m("scrotal_resting_height", "MALE_REPRODUCTIVE_EXTERNAL", 9.5),
    _m("scrotal_maximum_width", "MALE_REPRODUCTIVE_EXTERNAL", 7.0),
    _m("testicular_modeled_long_axis", "MALE_REPRODUCTIVE_EXTERNAL", 4.5),
    _m("testicular_modeled_width", "MALE_REPRODUCTIVE_EXTERNAL", 2.8),
    _m("external_perineal_length", "MALE_REPRODUCTIVE_EXTERNAL", 6.0),
)

_REQUIRED_IDS: Final[frozenset[str]] = frozenset(
    item.measurement_id for item in _MEASUREMENTS
)


def build_teacher_anthropometry_profile() -> TeacherAnthropometryProfile:
    profile = TeacherAnthropometryProfile(
        profile_id=TEACHER_ANTHROPOMETRY_PROFILE_ID,
        body_id=TEACHER_BODY_ID,
        measurements=_MEASUREMENTS,
    )
    validate_teacher_anthropometry_profile(profile)
    return profile


def validate_teacher_anthropometry_profile(
    profile: TeacherAnthropometryProfile,
) -> dict[str, str]:
    if profile.profile_id != TEACHER_ANTHROPOMETRY_PROFILE_ID:
        raise ValueError("Teacher anthropometry profile id drift")
    if profile.body_id != TEACHER_BODY_ID:
        raise ValueError("Teacher anthropometry body id drift")
    if len(profile.measurements) != EXPECTED_MEASUREMENT_COUNT:
        raise ValueError("Teacher anthropometry must contain exactly 62 measurements")

    ids = [item.measurement_id for item in profile.measurements]
    if len(ids) != len(set(ids)):
        raise ValueError("Teacher anthropometry measurement ids must be unique")
    if set(ids) != _REQUIRED_IDS:
        raise ValueError("Teacher anthropometry measurement coverage drift")

    for item in profile.measurements:
        if item.unit not in {"cm", "kg"}:
            raise ValueError(f"unsupported anthropometry unit: {item.unit}")
        if item.minimum <= 0 or item.nominal <= 0 or item.maximum <= 0:
            raise ValueError(f"anthropometry values must be positive: {item.measurement_id}")
        if not item.minimum <= item.nominal <= item.maximum:
            raise ValueError(f"invalid anthropometry range: {item.measurement_id}")

    if profile.real_person_biometric_source != "NONE":
        raise ValueError("Teacher anthropometry cannot claim real-person biometrics")
    if profile.person_reconstruction != "NO":
        raise ValueError("Teacher anthropometry cannot be a person reconstruction")
    if profile.canonical_effect != "NONE" or profile.deployment:
        raise ValueError("Teacher anthropometry must remain non-canonical and undeployed")

    return {
        "result": "PASS",
        "measurement_count": str(EXPECTED_MEASUREMENT_COUNT),
        "machine_readable_coverage": "PASS",
        "range_validation": "PASS",
        "synthetic_non_biometric_boundary": "PASS",
    }
