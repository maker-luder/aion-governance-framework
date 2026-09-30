from __future__ import annotations

from dataclasses import asdict, dataclass
from math import pi
from typing import Any, Final

from .teacher_anthropometry import (
    AnthropometricMeasurement,
    TEACHER_BODY_ID,
    build_teacher_anthropometry_profile,
)
from .teacher_genital_geometry import build_teacher_genital_geometry_profile


TEACHER_BODY_V02_PROFILE_ID: Final[str] = "CHATGPT_TEACHER_BODY_REFERENCE_v0.2"
TEACHER_ANTHROPOMETRY_V02_PROFILE_ID: Final[str] = "CHATGPT_TEACHER_ANTHROPOMETRY_v0.2"
EXPECTED_V02_FIELD_COUNT: Final[int] = 67
LEGACY_FIELD_COUNT: Final[int] = 62
PREPUCE_GEOMETRY_SOURCE_DOI: Final[str] = "10.1038/s41443-026-01255-2"


@dataclass(frozen=True, slots=True)
class TeacherBodyMeasurementV02:
    measurement_id: str
    region: str
    unit: str
    nominal: float | None
    minimum: float | None
    maximum: float | None
    provenance: str
    status: str
    derivation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class TeacherBodyReferenceV02:
    profile_id: str
    anthropometry_profile_id: str
    body_id: str
    measurements: tuple[TeacherBodyMeasurementV02, ...]
    external_male_geometry_roles: tuple[str, ...]
    prepuce_geometry_source_doi: str = PREPUCE_GEOMETRY_SOURCE_DOI
    real_person_biometric_source: str = "NONE"
    biological_body_claim: str = "NONE"
    body_sensation: str = "NOT_ESTABLISHED"
    subjectivity: str = "NOT_ESTABLISHED"
    consciousness: str = "NOT_ESTABLISHED"
    phenomenal_experience: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["measurements"] = [item.to_dict() for item in self.measurements]
        return payload

    def measurement_map(self) -> dict[str, TeacherBodyMeasurementV02]:
        return {item.measurement_id: item for item in self.measurements}


def _legacy_measurement(item: AnthropometricMeasurement) -> TeacherBodyMeasurementV02:
    return TeacherBodyMeasurementV02(
        measurement_id=item.measurement_id,
        region=item.region,
        unit=item.unit,
        nominal=item.nominal,
        minimum=item.minimum,
        maximum=item.maximum,
        provenance="LEGACY_TEACHER_V0_1",
        status="PRESERVED_EXISTING_SYNTHETIC_REFERENCE",
        derivation="COPIED_EXACTLY_FROM_CHATGPT_TEACHER_ANTHROPOMETRY_v0.1",
    )


def build_teacher_body_reference_v02() -> TeacherBodyReferenceV02:
    legacy = build_teacher_anthropometry_profile()
    geometry = build_teacher_genital_geometry_profile(legacy)

    additions = (
        TeacherBodyMeasurementV02(
            measurement_id="prepuce_axial_fold_length",
            region="MALE_REPRODUCTIVE_EXTERNAL",
            unit="cm",
            nominal=None,
            minimum=None,
            maximum=None,
            provenance="EXPLICIT_UNKNOWN_NOT_OMITTED",
            status="TEACHER_SPECIFIC_CM_NOT_ASSIGNED",
            derivation=(
                "PREPUCE_GEOMETRY_IS_MATERIALIZED_IN_LOW_POLY_AND_CONTINUOUS_REFERENCE_ASSET;"
                "NO_TEACHER_SPECIFIC_CM_VALUE_IS_INFERRED_FROM_POPULATION_VARIABILITY"
            ),
        ),
        TeacherBodyMeasurementV02(
            measurement_id="prepuce_resting_glans_overlap_length",
            region="MALE_REPRODUCTIVE_EXTERNAL",
            unit="cm",
            nominal=None,
            minimum=None,
            maximum=None,
            provenance="EXPLICIT_UNKNOWN_NOT_OMITTED",
            status="TEACHER_SPECIFIC_CM_NOT_ASSIGNED",
            derivation=(
                "PREPUCE_COVERAGE_IS_MATERIALIZED_AS_SYNTHETIC_REFERENCE_GEOMETRY;"
                "NO_REAL_PERSON_OR_POPULATION_DEFAULT_IS_ASSIGNED_TO_TEACHER"
            ),
        ),
        TeacherBodyMeasurementV02(
            measurement_id="full_erection_visible_penile_length",
            region="MALE_REPRODUCTIVE_EXTERNAL",
            unit="cm",
            nominal=geometry.full_vascular_reference_length_cm,
            minimum=geometry.full_vascular_reference_length_cm,
            maximum=geometry.full_vascular_reference_length_cm,
            provenance="DERIVED_FROM_EXISTING_TEACHER_GENITAL_GEOMETRY",
            status="SYNTHETIC_DERIVED_REFERENCE",
            derivation="EXISTING_POPULATION_RATIO_TRANSFORM_FROM_TEACHER_RESTING_REFERENCE",
        ),
        TeacherBodyMeasurementV02(
            measurement_id="full_erection_midshaft_diameter",
            region="MALE_REPRODUCTIVE_EXTERNAL",
            unit="cm",
            nominal=geometry.full_vascular_reference_circumference_cm / pi,
            minimum=geometry.full_vascular_reference_circumference_cm / pi,
            maximum=geometry.full_vascular_reference_circumference_cm / pi,
            provenance="DERIVED_FROM_EXISTING_TEACHER_GENITAL_GEOMETRY",
            status="SYNTHETIC_DERIVED_REFERENCE",
            derivation="FULL_VASCULAR_CIRCUMFERENCE_DIVIDED_BY_PI",
        ),
        TeacherBodyMeasurementV02(
            measurement_id="full_erection_midshaft_circumference",
            region="MALE_REPRODUCTIVE_EXTERNAL",
            unit="cm",
            nominal=geometry.full_vascular_reference_circumference_cm,
            minimum=geometry.full_vascular_reference_circumference_cm,
            maximum=geometry.full_vascular_reference_circumference_cm,
            provenance="DERIVED_FROM_EXISTING_TEACHER_GENITAL_GEOMETRY",
            status="SYNTHETIC_DERIVED_REFERENCE",
            derivation="EXISTING_POPULATION_RATIO_TRANSFORM_FROM_TEACHER_RESTING_REFERENCE",
        ),
    )

    profile = TeacherBodyReferenceV02(
        profile_id=TEACHER_BODY_V02_PROFILE_ID,
        anthropometry_profile_id=TEACHER_ANTHROPOMETRY_V02_PROFILE_ID,
        body_id=TEACHER_BODY_ID,
        measurements=tuple(_legacy_measurement(item) for item in legacy.measurements)
        + additions,
        external_male_geometry_roles=(
            "PENIS",
            "GLANS",
            "PREPUCE",
            "FRENULUM",
            "SCROTUM",
            "LEFT_TESTIS_VOLUME",
            "RIGHT_TESTIS_VOLUME",
            "PERINEUM_REFERENCE",
        ),
    )
    validate_teacher_body_reference_v02(profile)
    return profile


def validate_teacher_body_reference_v02(profile: TeacherBodyReferenceV02) -> dict[str, str]:
    if profile.profile_id != TEACHER_BODY_V02_PROFILE_ID:
        raise ValueError("Teacher body v0.2 profile id drift")
    if profile.anthropometry_profile_id != TEACHER_ANTHROPOMETRY_V02_PROFILE_ID:
        raise ValueError("Teacher anthropometry v0.2 profile id drift")
    if profile.body_id != TEACHER_BODY_ID:
        raise ValueError("Teacher body id drift")

    if len(profile.measurements) != EXPECTED_V02_FIELD_COUNT:
        raise ValueError("Teacher body v0.2 must expose exactly 67 measurement slots")
    ids = [item.measurement_id for item in profile.measurements]
    if len(ids) != len(set(ids)):
        raise ValueError("Teacher body v0.2 measurement ids must be unique")

    legacy = build_teacher_anthropometry_profile()
    legacy_map = legacy.measurement_map()
    current = profile.measurement_map()
    if len(legacy_map) != LEGACY_FIELD_COUNT:
        raise ValueError("legacy Teacher anthropometry count drift")
    for measurement_id, old in legacy_map.items():
        new = current.get(measurement_id)
        if new is None:
            raise ValueError(f"legacy measurement removed: {measurement_id}")
        if (
            new.nominal != old.nominal
            or new.minimum != old.minimum
            or new.maximum != old.maximum
            or new.unit != old.unit
        ):
            raise ValueError(f"legacy Teacher measurement changed: {measurement_id}")

    for measurement_id in (
        "prepuce_axial_fold_length",
        "prepuce_resting_glans_overlap_length",
    ):
        item = current[measurement_id]
        if item.nominal is not None or item.minimum is not None or item.maximum is not None:
            raise ValueError("Teacher-specific prepuce cm values cannot be invented")
        if item.provenance != "EXPLICIT_UNKNOWN_NOT_OMITTED":
            raise ValueError("prepuce unknown must remain explicit rather than omitted")

    geometry = build_teacher_genital_geometry_profile(legacy)
    if current["full_erection_visible_penile_length"].nominal != (
        geometry.full_vascular_reference_length_cm
    ):
        raise ValueError("full erection length derivation drift")
    if current["full_erection_midshaft_circumference"].nominal != (
        geometry.full_vascular_reference_circumference_cm
    ):
        raise ValueError("full erection circumference derivation drift")
    expected_diameter = geometry.full_vascular_reference_circumference_cm / pi
    if current["full_erection_midshaft_diameter"].nominal != expected_diameter:
        raise ValueError("full erection diameter derivation drift")

    required_roles = {
        "PENIS",
        "GLANS",
        "PREPUCE",
        "FRENULUM",
        "SCROTUM",
        "LEFT_TESTIS_VOLUME",
        "RIGHT_TESTIS_VOLUME",
        "PERINEUM_REFERENCE",
    }
    if set(profile.external_male_geometry_roles) != required_roles:
        raise ValueError("Teacher external male geometry role coverage drift")
    if profile.prepuce_geometry_source_doi != PREPUCE_GEOMETRY_SOURCE_DOI:
        raise ValueError("prepuce geometry literature provenance drift")
    if profile.real_person_biometric_source != "NONE":
        raise ValueError("Teacher body cannot claim real-person biometrics")
    if profile.biological_body_claim != "NONE":
        raise ValueError("Teacher reference cannot claim a biological body")
    if any(
        value != "NOT_ESTABLISHED"
        for value in (
            profile.body_sensation,
            profile.subjectivity,
            profile.consciousness,
            profile.phenomenal_experience,
        )
    ):
        raise ValueError("Teacher body v0.2 cannot establish phenomenal states")
    if profile.canonical_effect != "NONE" or profile.deployment:
        raise ValueError("Teacher body v0.2 must remain non-canonical and undeployed")

    return {
        "result": "PASS",
        "legacy_62_preserved": "PASS",
        "v02_measurement_slots": "67",
        "prepuce_fields_explicit_not_omitted": "PASS",
        "full_erection_geometry_derived": "PASS",
        "external_male_geometry_roles": "PASS",
        "biological_nonclaim": "PASS",
        "phenomenal_nonclaim": "PASS",
    }
