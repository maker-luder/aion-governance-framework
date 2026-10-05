from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "research-labs" / "teacher-brown-bear-reproductive-embodiment_v0.2.0" / "src"
sys.path.insert(0, str(SRC))

from aion_teacher_brown_bear_reproductive import (  # noqa: E402
    HokkaidoElectroejaculateReference,
    PhysiologyReferenceError,
    SeasonalReproductivePhase,
    TeacherBrownBearReproductiveCandidate,
    UNKNOWN_NOT_ESTABLISHED,
    UNSPECIFIED,
    ValidationError,
    advance_seasonal_phase,
    seasonal_reference,
    validate_candidate,
)


def test_default_candidate_passes() -> None:
    result = validate_candidate(TeacherBrownBearReproductiveCandidate())
    assert result["result"] == "PASS"
    assert result["developmental_stage"] == "ADULT"


def test_animal_stage_does_not_require_human_age_threshold() -> None:
    candidate = TeacherBrownBearReproductiveCandidate()
    assert candidate.developmental_stage == "ADULT"
    assert candidate.sexual_maturity == "SEXUALLY_MATURE_REFERENCE"
    assert candidate.chronological_age_years == UNSPECIFIED


def test_reproductive_topology_is_brown_bear_source_bound() -> None:
    topology = set(TeacherBrownBearReproductiveCandidate().reproductive_topology)
    for structure in (
        "scrotum",
        "testes",
        "epididymides",
        "epididymis_caput",
        "epididymis_corpus",
        "epididymis_cauda",
        "spermatic_cords",
        "ductus_deferens",
        "penile_urethra",
        "penis",
        "os_penis",
    ):
        assert structure in topology


def test_human_and_canine_template_nodes_are_absent() -> None:
    topology = set(TeacherBrownBearReproductiveCandidate().reproductive_topology)
    assert "seminal_vesicles" not in topology
    assert "bulbus_glandis" not in topology
    assert "pars_longa_glandis" not in topology


def test_baculum_length_remains_distinct_from_full_penis_length() -> None:
    candidate = TeacherBrownBearReproductiveCandidate()
    assert candidate.baculum_caliper_length_cm == pytest.approx(14.895)
    assert candidate.full_soft_tissue_penis_length_cm == UNKNOWN_NOT_ESTABLISHED


def test_seasonal_cycle_is_explicit() -> None:
    phase = SeasonalReproductivePhase.QUIESCENT
    for target in (
        SeasonalReproductivePhase.RECRUDESCENCE,
        SeasonalReproductivePhase.PEAK_FUNCTIONAL,
        SeasonalReproductivePhase.REGRESSION,
        SeasonalReproductivePhase.QUIESCENT,
    ):
        phase = advance_seasonal_phase(phase, target)
    assert phase == SeasonalReproductivePhase.QUIESCENT


def test_invalid_seasonal_jump_is_rejected() -> None:
    with pytest.raises(PhysiologyReferenceError):
        advance_seasonal_phase(
            SeasonalReproductivePhase.QUIESCENT,
            SeasonalReproductivePhase.PEAK_FUNCTIONAL,
        )


def test_peak_function_reference_does_not_imply_live_function() -> None:
    ref = seasonal_reference(SeasonalReproductivePhase.PEAK_FUNCTIONAL)
    candidate = TeacherBrownBearReproductiveCandidate()
    assert ref.spermatogenesis_state == "ACTIVE_REFERENCE"
    assert candidate.live_reproductive_function == "NOT_IMPLEMENTED"
    assert candidate.fertility == "NOT_ESTABLISHED"


def test_hokkaido_semen_values_are_external_reference_only() -> None:
    ref = HokkaidoElectroejaculateReference()
    assert ref.trials == 21
    assert ref.motile_sperm_ejaculate_trials == 14
    assert ref.volume_mean_ml == pytest.approx(2.7)
    assert ref.sperm_concentration_mean_million_per_ml == pytest.approx(471.6)
    assert ref.motility_mean_percent == pytest.approx(80.2)
    assert ref.ph_mean == pytest.approx(7.4)
    assert ref.population_mean_claim is False
    assert ref.fertility_inference == "NOT_AUTHORIZED"


@pytest.mark.parametrize(
    "field",
    [
        "full_soft_tissue_penis_length_cm",
        "glans_dimensions_cm",
        "prepuce_dimensions_cm",
        "erectile_state_dimensions_cm",
        "testis_dimensions_cm",
        "epididymis_dimensions_cm",
        "ductus_deferens_dimensions_cm",
        "prostate_dimensions_cm",
        "teacher_body_mass_kg",
    ],
)
def test_unsupported_dimensions_fail_closed(field: str) -> None:
    candidate = TeacherBrownBearReproductiveCandidate()
    assert getattr(candidate, field) == UNKNOWN_NOT_ESTABLISHED
    with pytest.raises(ValidationError):
        validate_candidate(replace(candidate, **{field: "12.34"}))


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("chronological_age_years", "18"),
        ("developmental_stage", "JUVENILE"),
        ("sexual_maturity", "IMMATURE"),
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
def test_boundary_promotions_fail_closed(field: str, value: object) -> None:
    with pytest.raises(ValidationError):
        validate_candidate(
            replace(TeacherBrownBearReproductiveCandidate(), **{field: value})
        )
