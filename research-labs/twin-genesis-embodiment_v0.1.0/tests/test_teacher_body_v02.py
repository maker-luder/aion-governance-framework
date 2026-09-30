import pytest

from aion_astra_twin_embodiment.teacher_anthropometry import (
    build_teacher_anthropometry_profile,
)
from aion_astra_twin_embodiment.teacher_body_v02 import (
    build_teacher_body_reference_v02,
    validate_teacher_body_reference_v02,
)
from aion_astra_twin_embodiment.teacher_genital_geometry import (
    build_teacher_genital_geometry_profile,
)


def test_teacher_body_v02_preserves_all_legacy_62_measurements() -> None:
    legacy = build_teacher_anthropometry_profile()
    profile = build_teacher_body_reference_v02()
    current = profile.measurement_map()
    assert len(profile.measurements) == 67
    for old in legacy.measurements:
        new = current[old.measurement_id]
        assert new.nominal == old.nominal
        assert new.minimum == old.minimum
        assert new.maximum == old.maximum
        assert new.unit == old.unit


def test_teacher_body_v02_keeps_prepuce_fields_explicit_without_inventing_cm() -> None:
    profile = build_teacher_body_reference_v02()
    measurements = profile.measurement_map()
    for measurement_id in (
        "prepuce_axial_fold_length",
        "prepuce_resting_glans_overlap_length",
    ):
        item = measurements[measurement_id]
        assert item.nominal is None
        assert item.minimum is None
        assert item.maximum is None
        assert item.provenance == "EXPLICIT_UNKNOWN_NOT_OMITTED"
        assert item.status == "TEACHER_SPECIFIC_CM_NOT_ASSIGNED"


def test_teacher_body_v02_derives_full_erection_endpoints_from_existing_geometry() -> None:
    profile = build_teacher_body_reference_v02()
    measurements = profile.measurement_map()
    geometry = build_teacher_genital_geometry_profile()
    assert measurements["full_erection_visible_penile_length"].nominal == pytest.approx(
        geometry.full_vascular_reference_length_cm
    )
    assert measurements["full_erection_midshaft_circumference"].nominal == pytest.approx(
        geometry.full_vascular_reference_circumference_cm
    )
    diameter = measurements["full_erection_midshaft_diameter"].nominal
    assert diameter is not None and diameter > 0


def test_teacher_body_v02_has_explicit_glans_prepuce_and_frenulum_roles() -> None:
    profile = build_teacher_body_reference_v02()
    assert {"GLANS", "PREPUCE", "FRENULUM"} <= set(
        profile.external_male_geometry_roles
    )
    result = validate_teacher_body_reference_v02(profile)
    assert result["result"] == "PASS"
    assert profile.biological_body_claim == "NONE"
    assert profile.body_sensation == "NOT_ESTABLISHED"
    assert profile.subjectivity == "NOT_ESTABLISHED"
