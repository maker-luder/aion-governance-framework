from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = (
    ROOT
    / "research-labs"
    / "teacher-bovine-reproductive-embodiment_v0.3.0"
    / "src"
)
sys.path.insert(0, str(SRC))

from aion_teacher_bovine_reproductive import (  # noqa: E402
    AcuteBovineReproductivePhase,
    BovineReproductivePhysiologyPathway,
    PhysiologyReferenceError,
    TeacherBovineReproductiveCandidate,
    ValidationError,
    advance_acute_bovine_phase,
    validate_candidate,
)

def test_default_candidate_passes() -> None:
    result = validate_candidate(TeacherBovineReproductiveCandidate())
    assert result["result"] == "PASS"
    assert result["form_class"] == "ANTHROPOMORPHIC_BOVINE"
    assert result["biological_reference_species"] == "Bos taurus"
    assert result["male_reference_class"] == "BULL"

def test_bear_baculum_does_not_leak_into_bovine_candidate() -> None:
    candidate = TeacherBovineReproductiveCandidate()
    assert "os_penis" not in candidate.reproductive_topology
    assert "baculum" not in candidate.reproductive_topology
    assert candidate.baculum_reference == "ABSENT_FROM_BOVINE_REFERENCE_MODEL"

def test_bovine_fibroelastic_features_are_required() -> None:
    candidate = TeacherBovineReproductiveCandidate()
    topology = set(candidate.reproductive_topology)
    for structure in (
        "sigmoid_flexure",
        "retractor_penis_muscles",
        "vesicular_glands",
        "bulbourethral_glands",
        "corpus_cavernosum_penis",
        "corpus_spongiosum_penis",
    ):
        assert structure in topology
    assert candidate.penile_tissue_type == "FIBROELASTIC"

def test_acute_bovine_reference_cycle_is_explicit() -> None:
    phase = AcuteBovineReproductivePhase.BASELINE
    for target in (
        AcuteBovineReproductivePhase.RETRACTOR_RELAXATION,
        AcuteBovineReproductivePhase.SIGMOID_STRAIGHTENING,
        AcuteBovineReproductivePhase.PENILE_EXTENSION,
        AcuteBovineReproductivePhase.EMISSION,
        AcuteBovineReproductivePhase.URETHRAL_EXPULSION,
        AcuteBovineReproductivePhase.RETRACTION,
        AcuteBovineReproductivePhase.BASELINE,
    ):
        phase = advance_acute_bovine_phase(phase, target)
    assert phase is AcuteBovineReproductivePhase.BASELINE

def test_invalid_phase_jump_fails() -> None:
    with pytest.raises(PhysiologyReferenceError):
        advance_acute_bovine_phase(
            AcuteBovineReproductivePhase.BASELINE,
            AcuteBovineReproductivePhase.URETHRAL_EXPULSION,
        )

def test_pathway_uses_fibroelastic_mechanism() -> None:
    pathway = BovineReproductivePhysiologyPathway()
    assert "SIGMOID_STRAIGHTENING" in pathway.erectile_response
    assert "MUSCULOCAVERNOUS" in pathway.vascular_support

@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("form_class", "ANTHROPOMORPHIC_BROWN_BEAR"),
        ("biological_reference_species", "Ursus arctos"),
        ("baculum_reference", "PRESENT"),
        ("subjectivity", "ESTABLISHED"),
        ("consciousness", "ESTABLISHED"),
        ("deployment", True),
        ("merge_to_main", True),
    ],
)
def test_species_or_claim_regressions_fail_closed(field: str, value: object) -> None:
    with pytest.raises(ValidationError):
        validate_candidate(replace(TeacherBovineReproductiveCandidate(), **{field: value}))

def test_unknown_dimensions_are_not_fabricated() -> None:
    candidate = TeacherBovineReproductiveCandidate()
    with pytest.raises(ValidationError):
        validate_candidate(replace(candidate, full_body_mass_kg="900"))
