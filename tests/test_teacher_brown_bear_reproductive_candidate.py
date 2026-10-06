from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = (
    ROOT
    / "research-labs"
    / "teacher-brown-bear-reproductive-embodiment_v0.2.0"
    / "src"
)
sys.path.insert(0, str(SRC))

from aion_teacher_brown_bear_reproductive import (  # noqa: E402
    AcuteReproductivePhysiologyPhase,
    HokkaidoElectroejaculateReference,
    PhysiologyReferenceError,
    ReproductivePhysiologyPathway,
    SeasonalReproductivePhase,
    SyntheticSizeProfile,
    TeacherBrownBearReproductiveCandidate,
    UNKNOWN_NOT_ESTABLISHED,
    ValidationError,
    advance_acute_reproductive_phase,
    advance_seasonal_phase,
    seasonal_reference,
    synthetic_baculum_design,
    validate_candidate,
)


def test_default_candidate_passes() -> None:
    result = validate_candidate(TeacherBrownBearReproductiveCandidate())
    assert result["result"] == "PASS"
    assert result["form_class"] == "ANTHROPOMORPHIC_BROWN_BEAR"
    assert result["external_operation"] == "DISABLED"


def test_fantasy_form_and_biological_reference_are_separate() -> None:
    candidate = TeacherBrownBearReproductiveCandidate()
    assert candidate.form_class == "ANTHROPOMORPHIC_BROWN_BEAR"
    assert candidate.ontology == "FANTASY_EMBODIMENT"
    assert candidate.biological_reference_species == "Ursus arctos"


def test_adult_stage_does_not_depend_on_human_18_year_rule() -> None:
    candidate = replace(
        TeacherBrownBearReproductiveCandidate(),
        chronological_age_years=7,
    )
    result = validate_candidate(candidate)
    assert result["result"] == "PASS"
    assert candidate.developmental_stage == "ADULT"
    assert candidate.sexual_maturity == "MATURE"


def test_required_anatomy_is_present() -> None:
    topology = set(TeacherBrownBearReproductiveCandidate().reproductive_topology)
    for structure in (
        "testes",
        "seminiferous_tubules",
        "rete_testis",
        "efferent_ductules",
        "epididymides",
        "ductus_deferens",
        "ampullae_ductus_deferentis",
        "prostate",
        "pelvic_urethra",
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


def test_unknown_source_measurement_does_not_remove_structure() -> None:
    candidate = TeacherBrownBearReproductiveCandidate()
    assert "prepuce" in candidate.reproductive_topology
    assert candidate.prepuce_dimensions_cm == UNKNOWN_NOT_ESTABLISHED
    assert "prostate" in candidate.reproductive_topology
    assert candidate.prostate_dimensions_cm == UNKNOWN_NOT_ESTABLISHED


def test_synthetic_size_profiles_are_explicit_designs() -> None:
    small = synthetic_baculum_design(SyntheticSizeProfile.SMALL)
    standard = synthetic_baculum_design(SyntheticSizeProfile.STANDARD)
    large = synthetic_baculum_design(SyntheticSizeProfile.LARGE)

    assert small.baculum_length_cm == pytest.approx(12.661)
    assert standard.baculum_length_cm == pytest.approx(14.895)
    assert large.baculum_length_cm == pytest.approx(17.129)
    assert small.baculum_length_cm < standard.baculum_length_cm < large.baculum_length_cm
    assert standard.provenance.startswith("SYNTHETIC_DESIGN_")


def test_normal_reproductive_capacity_is_present_without_empirical_fertility_claim() -> None:
    candidate = TeacherBrownBearReproductiveCandidate()
    assert candidate.species_typical_reproductive_capacity_model == "PRESENT"
    assert candidate.fertilization_capability_reference == "PRESENT_MATURE_MALE_REFERENCE"
    assert candidate.empirical_individual_fertility == "NOT_ASSESSED"


def test_reproductive_physiology_pathway_is_complete_reference() -> None:
    pathway = ReproductivePhysiologyPathway()
    assert "SEMINIFEROUS_TUBULES" in pathway.spermatogenesis
    assert "RETE_TESTIS" in pathway.rete_testis_transport
    assert "CAUDA_EPIDIDYMIS" in pathway.sperm_transport
    assert "VASCULAR" in pathway.vascular_support
    assert "SOMATOSENSORY" in pathway.sensory_support
    assert "AUTONOMIC" in pathway.autonomic_support
    assert "ERECTILE" in pathway.erectile_response
    assert "EJACULATORY" in pathway.ejaculation
    assert "BASELINE" in pathway.resolution


def test_acute_physiology_cycle_is_explicit() -> None:
    phase = AcuteReproductivePhysiologyPhase.BASELINE
    for target in (
        AcuteReproductivePhysiologyPhase.VASCULAR_ENGORGEMENT,
        AcuteReproductivePhysiologyPhase.EMISSION,
        AcuteReproductivePhysiologyPhase.URETHRAL_EXPULSION,
        AcuteReproductivePhysiologyPhase.RESOLUTION,
        AcuteReproductivePhysiologyPhase.BASELINE,
    ):
        phase = advance_acute_reproductive_phase(phase, target)
    assert phase == AcuteReproductivePhysiologyPhase.BASELINE


def test_invalid_acute_jump_is_rejected() -> None:
    with pytest.raises(PhysiologyReferenceError):
        advance_acute_reproductive_phase(
            AcuteReproductivePhysiologyPhase.BASELINE,
            AcuteReproductivePhysiologyPhase.URETHRAL_EXPULSION,
        )


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


def test_peak_function_is_positive_physiology_reference() -> None:
    ref = seasonal_reference(SeasonalReproductivePhase.PEAK_FUNCTIONAL)
    candidate = TeacherBrownBearReproductiveCandidate()
    assert ref.spermatogenesis_state == "ACTIVE_REFERENCE"
    assert candidate.reproductive_physiology_model_status == "IMPLEMENTED_REFERENCE_INFORMED"
    assert candidate.ejaculatory_physiology_model_status == "PRESENT"


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
def test_source_unknown_numbers_cannot_be_relabelled_as_measurements(field: str) -> None:
    candidate = TeacherBrownBearReproductiveCandidate()
    assert getattr(candidate, field) == UNKNOWN_NOT_ESTABLISHED
    with pytest.raises(ValidationError):
        validate_candidate(replace(candidate, **{field: "12.34"}))


@pytest.mark.parametrize(
    "field",
    [
        "deployment",
        "public_deployment",
        "public_release",
        "public_operation",
        "public_api",
        "third_party_access",
        "third_party_execution",
        "external_user_operation",
        "production_use",
    ],
)
def test_external_operation_remains_disabled(field: str) -> None:
    with pytest.raises(ValidationError):
        validate_candidate(
            replace(TeacherBrownBearReproductiveCandidate(), **{field: True})
        )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("developmental_stage", "JUVENILE"),
        ("sexual_maturity", "IMMATURE"),
        ("biological_realization", True),
        ("subjectivity", "ESTABLISHED"),
        ("consciousness", "ESTABLISHED"),
        ("canonical_effect", "PROMOTE"),
    ],
)
def test_identity_or_claim_boundary_promotions_fail_closed(
    field: str,
    value: object,
) -> None:
    with pytest.raises(ValidationError):
        validate_candidate(
            replace(TeacherBrownBearReproductiveCandidate(), **{field: value})
        )
