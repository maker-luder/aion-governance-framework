from dataclasses import replace
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
    ValidationError,
    WorkCanidEmbodimentCandidate,
    advance_fraction,
    advance_mechanism,
    fraction_reference,
    mechanism_reference,
    validate_candidate,
)


def test_mechanism_and_fraction_are_separate_axes() -> None:
    mechanism = mechanism_reference(EjaculatoryMechanismStage.SEMINAL_EMISSION)
    fraction = fraction_reference(EjaculateFraction.SPERM_RICH)
    assert mechanism.stage == EjaculatoryMechanismStage.SEMINAL_EMISSION
    assert fraction.fraction == EjaculateFraction.SPERM_RICH


def test_source_grounded_mechanism_sequence() -> None:
    stage = EjaculatoryMechanismStage.BASELINE
    for target in (
        EjaculatoryMechanismStage.SEMINAL_EMISSION,
        EjaculatoryMechanismStage.BLADDER_NECK_CLOSURE,
        EjaculatoryMechanismStage.URETHRAL_EXPULSION,
        EjaculatoryMechanismStage.PROSTATIC_CONTINUATION,
        EjaculatoryMechanismStage.RESOLUTION,
        EjaculatoryMechanismStage.BASELINE,
    ):
        stage = advance_mechanism(stage, target)
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


def test_expulsion_reference_contains_rhythmic_striated_muscle_component() -> None:
    expulsion = mechanism_reference(EjaculatoryMechanismStage.URETHRAL_EXPULSION)
    assert "RHYTHMIC" in expulsion.striated_muscle_state
    assert "ISCHIOCAVERNOSUS" in expulsion.striated_muscle_state


def test_reference_does_not_claim_live_physiology_or_sensation() -> None:
    for stage in EjaculatoryMechanismStage:
        ref = mechanism_reference(stage)
        assert ref.live_physiology is False
        assert ref.sensation == "NOT_ESTABLISHED"


def test_candidate_binds_reference_but_not_live_function() -> None:
    candidate = WorkCanidEmbodimentCandidate()
    assert candidate.ejaculatory_reference_model_status == "IMPLEMENTED_SYNTHETIC_REFERENCE_ONLY"
    assert candidate.live_ejaculatory_function == "NOT_IMPLEMENTED"
    validate_candidate(candidate)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("ejaculatory_reference_model_status", "LIVE"),
        ("live_ejaculatory_function", "IMPLEMENTED"),
    ],
)
def test_reference_model_cannot_promote_to_live_function(field: str, value: str) -> None:
    with pytest.raises(ValidationError):
        validate_candidate(replace(WorkCanidEmbodimentCandidate(), **{field: value}))
