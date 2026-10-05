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
    ReproductivePhysiologyPathway,
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
    assert result["anatomy_model"] == "IMPLEMENTED_SPECIES_REFERENCE"
    assert result["reproductive_physiology_model"] == "IMPLEMENTED_SPECIES_REFERENCE"


def test_animal_stage_does_not_require_human_age_threshold() -> None:
    candidate = TeacherBrownBearReproductiveCandidate()
    assert candidate.developmental_stage == "ADULT"
    assert candidate.sexual_maturity == "SEXUALLY_MATURE_REFERENCE"
    assert candidate.chronological_age_years == UNSPECIFIED


def test_required_anatomy_is_present_including_prepuce_and_prostate() -> None:
    topology = set(TeacherBrownBearReproductiveCandidate().reproductive_topology)
    for structure in (
        "scrotum",
        "testes",
        "epididymides",
        "ductus_deferens",
        "ampullae_ductus_deferentis",
        "prostate",
        "penile_urethra",
        "penis",
        "prepuce",
        "glans_penis",
        "corpus_cavernosum_penis",
        "os_penis",
    ):
        assert structure in topology


def test_topology_is_extensible_not_closed_world() -> None:
    candidate = TeacherBrownBearReproductiveCandidate()
    extended = replace(
        candidate,
        reproductive_topology=candidate.reproductive_topology + ("future_sourced_structure",),
    )
    assert validate_candidate(extended)["result"] == "PASS"


def test_required_structure_cannot_be_deleted() -> None:
    candidate = TeacherBrownBearReproductiveCandidate()
    reduced = tuple(x for x in candidate.reproductive_topology if x != "prepuce")
    with pytest.raises(ValidationError):
        validate_candidate(replace(candidate, reproductive_topology=reduced))


def test_unknown_dimension_does_not_remove_structure() -> None:
    candidate = TeacherBrownBearReproductiveCandidate()
    topology = set(candidate.reproductive_topology)
    assert "prepuce" in topology
    assert candidate.prepuce_dimensions_cm == UNKNOWN_NOT_ESTABLISHED
    assert "prostate" in topology
    assert candidate.prostate_dimensions_cm == UNKNOWN_NOT_ESTABLISHED


def test_reproductive_physiology_pathway_is_implemented_as_reference() -> None:
    pathway = ReproductivePhysiologyPathway()
    assert "TESTES" in pathway.spermatogenesis
    assert "CAUDA" in pathway.sperm_transport
    assert "ERECTION" in pathway.erectile_response
    assert "EJACULATORY" in pathway.ejaculation
    assert "ACCESSORY_GLAND" in pathway.seminal_plasma


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


def test_peak_function_is_a_positive_physiology_reference() -> None:
    ref = seasonal_reference(SeasonalReproductivePhase.PEAK_FUNCTIONAL)
    candidate = TeacherBrownBearReproductiveCandidate()
    assert ref.spermatogenesis_state == "ACTIVE_REFERENCE"
    assert candidate.reproductive_physiology_model_status == "IMPLEMENTED_SPECIES_REFERENCE"
    assert candidate.ejaculatory_physiology_model_status == "IMPLEMENTED_REFERENCE"


def test_hokkaido_semen_values_are_reference_not_species_mean() -> None:
    ref = HokkaidoElectroejaculateReference()
    assert ref.trials == 21
    assert ref.motile_sperm_ejaculate_trials == 14
    assert ref.volume_mean_ml == pytest.approx(2.7)
    assert ref.sperm_concentration_mean_million_per_ml == pytest.approx(471.6)
    assert ref.motility_mean_percent == pytest.approx(80.2)
    assert ref.ph_mean == pytest.approx(7.4)
    assert ref.population_mean_claim is False
    assert ref.fertility_inference == "NOT_ESTABLISHED_FROM_THIS_DATASET"


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
def test_only_unsupported_numbers_fail_closed(field: str) -> None:
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
        ("fertility", "ESTABLISHED"),
        ("subjectivity", "ESTABLISHED"),
        ("consciousness", "ESTABLISHED"),
        ("canonical_effect", "PROMOTE"),
        ("deployment", True),
    ],
)
def test_only_epistemic_or_identity_boundary_promotions_fail_closed(
    field: str,
    value: object,
) -> None:
    with pytest.raises(ValidationError):
        validate_candidate(
            replace(TeacherBrownBearReproductiveCandidate(), **{field: value})
        )
