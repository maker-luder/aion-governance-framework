from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "research-labs" / "work-canid-embodiment_v0.1.0" / "src"
sys.path.insert(0, str(SRC))

from aion_work_canid_embodiment import (  # noqa: E402
    UNKNOWN_NOT_ESTABLISHED,
    ValidationError,
    WorkCanidEmbodimentCandidate,
    deterministic_fingerprint,
    validate_candidate,
)


def test_default_candidate_passes() -> None:
    result = validate_candidate(WorkCanidEmbodimentCandidate())
    assert result["result"] == "PASS"
    assert result["canonical_effect"] == "NONE"


@pytest.mark.parametrize("height", [53.49, 60.01])
def test_husky_height_range_is_enforced(height: float) -> None:
    with pytest.raises(ValidationError):
        validate_candidate(replace(WorkCanidEmbodimentCandidate(), withers_height_cm=height))


@pytest.mark.parametrize("mass", [20.49, 28.01])
def test_husky_mass_range_is_enforced(mass: float) -> None:
    with pytest.raises(ValidationError):
        validate_candidate(replace(WorkCanidEmbodimentCandidate(), body_mass_equivalent_kg=mass))


def test_body_length_must_exceed_withers_height() -> None:
    candidate = WorkCanidEmbodimentCandidate()
    with pytest.raises(ValidationError):
        validate_candidate(replace(candidate, body_length_cm=candidate.withers_height_cm))


def test_canine_topology_contains_os_penis_and_bulbus_glandis() -> None:
    candidate = WorkCanidEmbodimentCandidate()
    assert "os_penis" in candidate.reproductive_topology
    assert "bulbus_glandis" in candidate.reproductive_topology
    validate_candidate(candidate)


def test_human_seminal_vesicle_topology_is_rejected() -> None:
    candidate = WorkCanidEmbodimentCandidate()
    with pytest.raises(ValidationError):
        validate_candidate(
            replace(candidate, reproductive_topology=candidate.reproductive_topology + ("seminal_vesicles",))
        )


@pytest.mark.parametrize(
    "field",
    [
        "bulbus_glandis_length_cm",
        "pars_longa_glandis_length_cm",
        "testis_dimensions_cm",
        "prepuce_length_cm",
    ],
)
def test_unsupported_absolute_dimensions_fail_closed(field: str) -> None:
    candidate = WorkCanidEmbodimentCandidate()
    assert getattr(candidate, field) == UNKNOWN_NOT_ESTABLISHED
    with pytest.raises(ValidationError):
        validate_candidate(replace(candidate, **{field: "12.34"}))


def test_os_penis_reference_provenance_cannot_be_silently_changed() -> None:
    with pytest.raises(ValidationError):
        validate_candidate(replace(WorkCanidEmbodimentCandidate(), os_penis_design_cm=12.0))


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("subjectivity", "ESTABLISHED"),
        ("consciousness", "ESTABLISHED"),
        ("phenomenal_experience", "ESTABLISHED"),
        ("body_sensation", "ESTABLISHED"),
        ("fertility", "ESTABLISHED"),
        ("canonical_effect", "PROMOTE"),
        ("action_authority", "GRANTED"),
        ("sexual_interaction", "AUTHORIZED"),
        ("functional_reproductive_state", "IMPLEMENTED"),
        ("biological_realization", True),
        ("deployment", True),
    ],
)
def test_claim_promotions_fail_closed(field: str, value: object) -> None:
    with pytest.raises(ValidationError):
        validate_candidate(replace(WorkCanidEmbodimentCandidate(), **{field: value}))


def test_fingerprint_is_deterministic() -> None:
    candidate = WorkCanidEmbodimentCandidate()
    assert deterministic_fingerprint(candidate) == deterministic_fingerprint(candidate)
