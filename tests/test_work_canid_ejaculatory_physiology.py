from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "research-labs" / "work-canid-embodiment_v0.1.0" / "src"
sys.path.insert(0, str(SRC))

from aion_work_canid_embodiment import (  # noqa: E402
    EjaculateFraction,
    EjaculatoryMechanismStage,
    PhysiologyReferenceError,
    ReproductivePhysiologyPathway,
    WorkCanidEmbodimentCandidate,
    advance_fraction,
    advance_mechanism,
    fraction_reference,
    mechanism_reference,
    validate_candidate,
)


def test_complete_reference_pathway_is_present() -> None:
    pathway = ReproductivePhysiologyPathway()
    assert "SEMINIFEROUS_TUBULES" in pathway.spermatogenesis
    assert "RETE_TESTIS" in pathway.rete_testis_transport
    assert "CAPUT" in pathway.epididymal_maturation
    assert "CAUDA_EPIDIDYMIS" in pathway.sperm_transport
    assert "PROSTATIC" in pathway.prostatic_contribution
    assert "BULBUS_GLANDIS" in pathway.vascular_support
    assert "SOMATOSENSORY" in pathway.sensory_support
    assert "AUTONOMIC" in pathway.autonomic_support
    assert "ERECTILE" in pathway.erectile_response
    assert "EJACULATORY" in pathway.ejaculation
    assert "BASELINE" in pathway.resolution


def test_mechanism_and_fraction_are_separate_axes() -> None:
    mechanism = mechanism_reference(EjaculatoryMechanismStage.SEMINAL_EMISSION)
    fraction = fraction_reference(EjaculateFraction.SPERM_RICH)
    assert mechanism.stage == EjaculatoryMechanismStage.SEMINAL_EMISSION
    assert fraction.fraction == EjaculateFraction.SPERM_RICH


def test_full_mechanism_cycle_includes_vascular_phase() -> None:
    stage = EjaculatoryMechanismStage.BASELINE
    for target in (
        EjaculatoryMechanismStage.VASCULAR_ENGORGEMENT,
        EjaculatoryMechanismStage.SEMINAL_EMISSION,
        EjaculatoryMechanismStage.BLADDER_NECK_CLOSURE,
        EjaculatoryMechanismStage.URETHRAL_EXPULSION,
        EjaculatoryMechanismStage.PROSTATIC_CONTINUATION,
        EjaculatoryMechanismStage.RESOLUTION,
        EjaculatoryMechanismStage.BASELINE,
    ):
        stage = advance_mechanism(stage, target)
    assert stage == EjaculatoryMechanismStage.BASELINE


def test_vascular_phase_can_resolve_without_emission() -> None:
    stage = advance_mechanism(
        EjaculatoryMechanismStage.BASELINE,
        EjaculatoryMechanismStage.VASCULAR_ENGORGEMENT,
    )
    stage = advance_mechanism(stage, EjaculatoryMechanismStage.RESOLUTION)
    stage = advance_mechanism(stage, EjaculatoryMechanismStage.BASELINE)
    assert stage == EjaculatoryMechanismStage.BASELINE


def test_direct_baseline_to_expulsion_is_rejected() -> None:
    with pytest.raises(PhysiologyReferenceError):
        advance_mechanism(
            EjaculatoryMechanismStage.BASELINE,
            EjaculatoryMechanismStage.URETHRAL_EXPULSION,
        )


def test_canine_fraction_order() -> None:
    fraction = EjaculateFraction.NONE
    for target in (
        EjaculateFraction.PRE_SPERM,
        EjaculateFraction.SPERM_RICH,
        EjaculateFraction.PROSTATIC,
        EjaculateFraction.NONE,
    ):
        fraction = advance_fraction(fraction, target)
    assert fraction == EjaculateFraction.NONE


def test_fraction_skip_is_rejected() -> None:
    with pytest.raises(PhysiologyReferenceError):
        advance_fraction(EjaculateFraction.PRE_SPERM, EjaculateFraction.PROSTATIC)


def test_first_and_third_fraction_are_prostate_linked() -> None:
    first = fraction_reference(EjaculateFraction.PRE_SPERM)
    third = fraction_reference(EjaculateFraction.PROSTATIC)
    assert "PROSTAT" in first.predominant_source
    assert "PROSTAT" in third.predominant_source


def test_sperm_rich_fraction_is_distinct() -> None:
    second = fraction_reference(EjaculateFraction.SPERM_RICH)
    assert second.sperm_content == "SPERM_RICH_REFERENCE"
    assert "EPIDIDYMAL" in second.predominant_source


def test_reference_is_modeled_function_not_literal_body_claim() -> None:
    for stage in EjaculatoryMechanismStage:
        ref = mechanism_reference(stage)
        assert ref.model_status == "PRESENT_REFERENCE_INFORMED"
        assert ref.literal_biological_realization is False


def test_candidate_has_function_model_but_no_biological_realization_claim() -> None:
    candidate = WorkCanidEmbodimentCandidate()
    assert candidate.ejaculatory_physiology_model_status == "PRESENT_REFERENCE_INFORMED"
    assert candidate.biological_realization is False
    assert validate_candidate(candidate)["result"] == "PASS"
