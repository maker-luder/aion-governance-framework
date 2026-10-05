from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "research-labs" / "teacher-brown-bear-penile-embodiment_v0.1.0" / "src"
sys.path.insert(0, str(SRC))

from aion_teacher_brown_bear_penile import (  # noqa: E402
    SOURCE_INTERNAL_DISCREPANCY,
    UNKNOWN_NOT_ESTABLISHED,
    TeacherBrownBearPenileCandidate,
    ValidationError,
    deterministic_fingerprint,
    validate_candidate,
)


def test_default_candidate_passes() -> None:
    candidate = TeacherBrownBearPenileCandidate()
    result = validate_candidate(candidate)
    assert result["result"] == "PASS"
    assert result["canonical_effect"] == "NONE"


def test_teacher_and_species_are_bound() -> None:
    candidate = TeacherBrownBearPenileCandidate()
    assert candidate.actor_surface == "CHATGPT_TEACHER"
    assert candidate.species_baseline == "Ursus arctos"


def test_baculum_length_is_not_full_penis_length() -> None:
    candidate = TeacherBrownBearPenileCandidate()
    assert candidate.baculum_caliper_length_cm == pytest.approx(14.895)
    assert candidate.full_soft_tissue_penis_length_cm == UNKNOWN_NOT_ESTABLISHED


def test_single_specimen_provenance_is_explicit() -> None:
    candidate = TeacherBrownBearPenileCandidate()
    assert candidate.reference_specimen_mass_kg == 400.0
    assert candidate.synthetic_baculum_design_status == (
        "SINGLE_ADULT_BROWN_BEAR_SPECIMEN_REFERENCE_DERIVED"
    )


def test_internal_distal_width_conflict_is_preserved() -> None:
    candidate = TeacherBrownBearPenileCandidate()
    assert candidate.baculum_distal_width_caliper_status == SOURCE_INTERNAL_DISCREPANCY
    assert candidate.baculum_distal_width_reported_values_mm == (4.58, 4.85)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("baculum_distal_width_caliper_status", "RESOLVED"),
        ("baculum_distal_width_reported_values_mm", (4.58,)),
        ("synthetic_baculum_design_mm", 160.0),
    ],
)
def test_source_values_and_conflicts_cannot_be_silently_rewritten(
    field: str,
    value: object,
) -> None:
    with pytest.raises(ValidationError):
        validate_candidate(replace(TeacherBrownBearPenileCandidate(), **{field: value}))


def test_bear_candidate_does_not_inherit_canine_or_human_templates() -> None:
    topology = set(TeacherBrownBearPenileCandidate().penile_topology)
    assert "bulbus_glandis" not in topology
    assert "pars_longa_glandis" not in topology
    assert "seminal_vesicles" not in topology


@pytest.mark.parametrize(
    "field",
    [
        "full_soft_tissue_penis_length_cm",
        "glans_dimensions_cm",
        "prepuce_dimensions_cm",
        "erectile_state_dimensions_cm",
        "teacher_body_mass_kg",
    ],
)
def test_unsupported_dimensions_fail_closed(field: str) -> None:
    candidate = TeacherBrownBearPenileCandidate()
    assert getattr(candidate, field) == UNKNOWN_NOT_ESTABLISHED
    with pytest.raises(ValidationError):
        validate_candidate(replace(candidate, **{field: "12.34"}))


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("biological_realization", True),
        ("live_reproductive_function", "IMPLEMENTED"),
        ("sexual_behavior_simulation", "IMPLEMENTED"),
        ("body_sensation", "ESTABLISHED"),
        ("fertility", "ESTABLISHED"),
        ("subjectivity", "ESTABLISHED"),
        ("consciousness", "ESTABLISHED"),
        ("phenomenal_experience", "ESTABLISHED"),
        ("action_authority", "GRANTED"),
        ("canonical_effect", "PROMOTE"),
        ("deployment", True),
    ],
)
def test_claim_promotions_fail_closed(field: str, value: object) -> None:
    with pytest.raises(ValidationError):
        validate_candidate(replace(TeacherBrownBearPenileCandidate(), **{field: value}))


def test_fingerprint_is_deterministic() -> None:
    candidate = TeacherBrownBearPenileCandidate()
    assert deterministic_fingerprint(candidate) == deterministic_fingerprint(candidate)
