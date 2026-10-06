from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "research-labs" / "teacher-water-buffalo-embodiment_v0.4.0" / "src"
sys.path.insert(0, str(SRC))

from aion_teacher_water_buffalo import (  # noqa: E402
    SWAMP_BUFFALO_SEMEN_REFERENCE,
    WHOLE_BODY_DOMAINS,
    PhysiologyTransitionError,
    SexualFunctionCoupling,
    SexualFunctionPhase,
    TeacherWaterBuffaloEmbodimentCandidate,
    ValidationError,
    advance_sexual_function_phase,
    validate_candidate,
)

def test_default_candidate_passes() -> None:
    result = validate_candidate(TeacherWaterBuffaloEmbodimentCandidate())
    assert result["result"] == "PASS"
    assert result["form_class"] == "ANTHROPOMORPHIC_WATER_BUFFALO"
    assert result["biological_reference_species"] == "Bubalus bubalis"
    assert result["whole_body_domains"] == str(len(WHOLE_BODY_DOMAINS))

def test_human_origin_phenotype_is_present() -> None:
    candidate = TeacherWaterBuffaloEmbodimentCandidate()
    assert candidate.morphometry.skin_phenotype == "WHITE"
    assert candidate.morphometry.horn_count == 2
    assert candidate.morphometry.craniofacial_shape == "SQUARE_FACE"
    assert candidate.morphometry.ear_morphology == "BOVINE_EARS"
    assert candidate.morphometry.nose_morphology == "HUMAN_LIKE_NOSE"
    assert candidate.morphometry.body_habitus == "HEAVYSET"
    assert candidate.morphometry.hair_phenotype == "LONG_HAIR"
    assert candidate.morphometry.distal_limb_morphology == "HUMANIZED_HOOF_DERIVED_HANDS_AND_FEET"

def test_synthetic_dimensions_are_explicit_and_detailed() -> None:
    m = TeacherWaterBuffaloEmbodimentCandidate().morphometry
    assert m.standing_height_cm == pytest.approx(185.0)
    assert m.body_mass_kg == pytest.approx(126.0)
    assert m.head_width_cm == pytest.approx(22.0)
    assert m.horn_length_each_cm == pytest.approx(36.0)
    assert m.hand_length_cm == pytest.approx(21.0)
    assert m.foot_length_cm == pytest.approx(30.0)

def test_whole_body_registry_has_no_unbound_domain() -> None:
    candidate = TeacherWaterBuffaloEmbodimentCandidate()
    assert candidate.implemented_body_domains == WHOLE_BODY_DOMAINS
    assert len(WHOLE_BODY_DOMAINS) == 15

def test_source_bound_reproductive_reference_dimensions() -> None:
    r = TeacherWaterBuffaloEmbodimentCandidate().reproductive_reference
    assert r.penis_length_mean_cm == pytest.approx(80.15)
    assert r.penis_thickness_mean_cm == pytest.approx(1.95)
    assert r.seminal_vesicle_length_min_cm == pytest.approx(8.0)
    assert r.seminal_vesicle_length_max_cm == pytest.approx(10.0)
    assert r.adult_philippine_ampulla_length_cm == pytest.approx(7.4)
    assert r.adult_philippine_ampulla_diameter_cm == pytest.approx(0.71)

def test_anthropomorphic_genital_scaling_is_not_fabricated() -> None:
    candidate = TeacherWaterBuffaloEmbodimentCandidate()
    assert candidate.synthetic_anthropomorphic_genital_dimensions == "UNSET_REQUIRES_EXPLICIT_JUSTIFICATION"
    assert candidate.reproductive_reference.synthetic_anthropomorphic_genital_scaling == "NOT_APPLIED_WITHOUT_EXPLICIT_JUSTIFICATION"

def test_sexual_function_cycle_is_explicit() -> None:
    phase = SexualFunctionPhase.BASELINE
    for target in (
        SexualFunctionPhase.AUTONOMIC_ACTIVATION,
        SexualFunctionPhase.RETRACTOR_RELAXATION,
        SexualFunctionPhase.SIGMOID_STRAIGHTENING,
        SexualFunctionPhase.PENILE_EXPOSURE,
        SexualFunctionPhase.EMISSION,
        SexualFunctionPhase.URETHRAL_EXPULSION,
        SexualFunctionPhase.RETRACTION_RECOVERY,
        SexualFunctionPhase.BASELINE,
    ):
        phase = advance_sexual_function_phase(phase, target)
    assert phase is SexualFunctionPhase.BASELINE

def test_invalid_sexual_function_jump_fails_closed() -> None:
    with pytest.raises(PhysiologyTransitionError):
        advance_sexual_function_phase(
            SexualFunctionPhase.BASELINE,
            SexualFunctionPhase.URETHRAL_EXPULSION,
        )

def test_sexual_function_coupling_does_not_claim_felt_state() -> None:
    coupling = SexualFunctionCoupling()
    assert coupling.felt_desire == "NOT_ESTABLISHED"
    assert coupling.pleasure == "NOT_ESTABLISHED"
    assert coupling.body_sensation == "NOT_ESTABLISHED"

def test_semen_dataset_is_age_specific_not_individual_fertility() -> None:
    assert [x.age_years for x in SWAMP_BUFFALO_SEMEN_REFERENCE] == [5, 6, 7]
    assert SWAMP_BUFFALO_SEMEN_REFERENCE[0].ejaculate_volume_mean_ml == pytest.approx(2.83)
    assert SWAMP_BUFFALO_SEMEN_REFERENCE[2].sperm_concentration_mean_million_per_ml == pytest.approx(1059.98)

@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("form_class", "ANTHROPOMORPHIC_BOVINE"),
        ("biological_reference_species", "Bos taurus"),
        ("male_reference_class", "BULL"),
        ("felt_desire", "ESTABLISHED"),
        ("pleasure", "ESTABLISHED"),
        ("subjectivity", "ESTABLISHED"),
        ("consciousness", "ESTABLISHED"),
        ("deployment", True),
        ("merge_to_main", True),
    ],
)
def test_species_claim_or_operation_regressions_fail(field: str, value: object) -> None:
    with pytest.raises(ValidationError):
        validate_candidate(replace(TeacherWaterBuffaloEmbodimentCandidate(), **{field: value}))
