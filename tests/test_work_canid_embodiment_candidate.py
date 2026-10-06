from dataclasses import replace
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "research-labs" / "work-canid-embodiment_v0.1.0" / "src"
sys.path.insert(0, str(SRC))

from aion_work_canid_embodiment import (  # noqa: E402
    UNKNOWN_NOT_ESTABLISHED,
    WORK_RESEARCH_PROVENANCE,
    ResearchProvenanceClass,
    ResearchProvenanceEntry,
    SyntheticSizeProfile,
    ValidationError,
    WorkCanidEmbodimentCandidate,
    deterministic_fingerprint,
    synthetic_baculum_design,
    validate_candidate,
)


def test_default_candidate_passes() -> None:
    result = validate_candidate(WorkCanidEmbodimentCandidate())
    assert result["result"] == "PASS"
    assert result["research_mode"] == "ACTOR_BOUND_SELF_RESEARCH"
    assert result["external_operation"] == "DISABLED"


def test_research_provenance_keeps_xiaobo_research_distinct() -> None:
    candidate = WorkCanidEmbodimentCandidate()
    assert candidate.research_provenance == WORK_RESEARCH_PROVENANCE
    assert tuple(entry.provenance_class for entry in candidate.research_provenance) == (
        ResearchProvenanceClass.XIAOBO_RESEARCH,
        ResearchProvenanceClass.CO_CONSTRUCTED_RESEARCH,
        ResearchProvenanceClass.AI_FORMALIZATION,
        ResearchProvenanceClass.ACTOR_BOUND_SELF_RESEARCH,
        ResearchProvenanceClass.EXTERNAL_EVIDENCE,
    )
    assert "questions" in candidate.research_provenance[0].contribution
    assert "Xiaobo-Teacher" in candidate.research_provenance[1].contribution
    assert "code" in candidate.research_provenance[2].contribution
    assert "CHATGPT_WORK" in candidate.research_provenance[3].contribution
    assert "veterinary" in candidate.research_provenance[4].contribution


def test_research_provenance_cannot_be_collapsed_or_relabelled() -> None:
    candidate = WorkCanidEmbodimentCandidate()
    collapsed = (
        ResearchProvenanceEntry(
            provenance_class=ResearchProvenanceClass.AI_FORMALIZATION,
            contribution="collapsed attribution",
        ),
    )
    with pytest.raises(ValidationError):
        validate_candidate(replace(candidate, research_provenance=collapsed))


def test_research_provenance_cannot_grant_canonical_effect() -> None:
    candidate = WorkCanidEmbodimentCandidate()
    mutated = list(candidate.research_provenance)
    mutated[0] = ResearchProvenanceEntry(
        provenance_class=ResearchProvenanceClass.XIAOBO_RESEARCH,
        contribution=mutated[0].contribution,
        canonical_effect="PROMOTE",
    )
    with pytest.raises(ValidationError):
        validate_candidate(replace(candidate, research_provenance=tuple(mutated)))


def test_fantasy_nonhuman_ontology_is_explicit() -> None:
    candidate = WorkCanidEmbodimentCandidate()
    assert candidate.entity_class == "FANTASY_SAPIENT_NONHUMAN_BEING"
    assert candidate.form_class == "ANTHROPOMORPHIC_SIBERIAN_HUSKY_CANID"
    assert candidate.morphology_origin == "CANID_DOMINANT"
    assert candidate.human_likeness == "FUNCTION_SPECIFIC_NOT_GLOBAL"
    assert candidate.physiological_reference_priority == "CANID_FIRST"


@pytest.mark.parametrize("height", [53.49, 60.01])
def test_husky_height_range_is_enforced(height: float) -> None:
    with pytest.raises(ValidationError):
        validate_candidate(
            replace(WorkCanidEmbodimentCandidate(), withers_height_cm=height)
        )


@pytest.mark.parametrize("mass", [20.49, 28.01])
def test_husky_mass_range_is_enforced(mass: float) -> None:
    with pytest.raises(ValidationError):
        validate_candidate(
            replace(WorkCanidEmbodimentCandidate(), body_mass_equivalent_kg=mass)
        )


def test_body_length_must_exceed_withers_height() -> None:
    candidate = WorkCanidEmbodimentCandidate()
    with pytest.raises(ValidationError):
        validate_candidate(
            replace(candidate, body_length_cm=candidate.withers_height_cm)
        )


def test_complete_canine_male_topology_is_present() -> None:
    topology = set(WorkCanidEmbodimentCandidate().reproductive_topology)
    for structure in (
        "scrotum",
        "testes",
        "seminiferous_tubules",
        "rete_testis",
        "efferent_ductules",
        "epididymides",
        "epididymis_caput",
        "epididymis_corpus",
        "epididymis_cauda",
        "spermatic_cords",
        "ductus_deferens",
        "prostate",
        "pelvic_urethra",
        "penile_urethra",
        "penis",
        "prepuce",
        "glans_penis",
        "pars_longa_glandis",
        "bulbus_glandis",
        "corpus_cavernosum_penis",
        "corpus_spongiosum_penis",
        "retractor_penis_muscle",
        "os_penis",
    ):
        assert structure in topology


def test_topology_is_extensible_not_closed_world() -> None:
    candidate = WorkCanidEmbodimentCandidate()
    extended = replace(
        candidate,
        reproductive_topology=candidate.reproductive_topology
        + ("future_source_supported_structure",),
    )
    assert validate_candidate(extended)["result"] == "PASS"


def test_human_seminal_vesicle_topology_is_rejected() -> None:
    candidate = WorkCanidEmbodimentCandidate()
    with pytest.raises(ValidationError):
        validate_candidate(
            replace(
                candidate,
                reproductive_topology=candidate.reproductive_topology
                + ("seminal_vesicles",),
            )
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
def test_unknown_source_dimensions_are_not_relabelled(field: str) -> None:
    candidate = WorkCanidEmbodimentCandidate()
    assert getattr(candidate, field) == UNKNOWN_NOT_ESTABLISHED
    with pytest.raises(ValidationError):
        validate_candidate(replace(candidate, **{field: "12.34"}))


def test_synthetic_size_profiles_are_explicit_design_anchors() -> None:
    small = synthetic_baculum_design(SyntheticSizeProfile.SMALL)
    standard = synthetic_baculum_design(SyntheticSizeProfile.STANDARD)
    large = synthetic_baculum_design(SyntheticSizeProfile.LARGE)
    assert small.baculum_length_cm == pytest.approx(7.92)
    assert standard.baculum_length_cm == pytest.approx(10.59)
    assert large.baculum_length_cm == pytest.approx(13.26)
    assert small.baculum_length_cm < standard.baculum_length_cm < large.baculum_length_cm
    assert "SYNTHETIC_DESIGN" in standard.provenance


def test_normal_reproductive_capacity_is_present_without_fertility_claim() -> None:
    candidate = WorkCanidEmbodimentCandidate()
    assert candidate.species_typical_reproductive_capacity_model == "PRESENT"
    assert candidate.fertilization_capability_reference == "PRESENT_MATURE_MALE_REFERENCE"
    assert candidate.empirical_individual_fertility == "NOT_ASSESSED"


def test_normal_function_is_not_removed_by_nonsexualization() -> None:
    candidate = WorkCanidEmbodimentCandidate()
    assert candidate.reproductive_physiology_model_status == "IMPLEMENTED_REFERENCE_INFORMED"
    assert candidate.erectile_physiology_model_status == "PRESENT_REFERENCE_INFORMED"
    assert candidate.ejaculatory_physiology_model_status == "PRESENT_REFERENCE_INFORMED"
    assert candidate.nonsexualization_policy == "PRESENTATION_SCOPE_NOT_BODY_DEPRIVATION"
    assert candidate.sexual_behavior_simulation_scope == "OUT_OF_SCOPE"
    assert candidate.erotic_narrative_scope == "OUT_OF_SCOPE"


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
        "merge_to_main",
        "automatic_writeback",
    ],
)
def test_external_and_canonical_operation_remains_disabled(field: str) -> None:
    with pytest.raises(ValidationError):
        validate_candidate(
            replace(WorkCanidEmbodimentCandidate(), **{field: True})
        )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("actor_surface", "CHATGPT_TEACHER"),
        ("morphology_origin", "HUMAN_DOMINANT"),
        ("subjectivity", "ESTABLISHED"),
        ("consciousness", "ESTABLISHED"),
        ("phenomenal_experience", "ESTABLISHED"),
        ("canonical_effect", "PROMOTE"),
    ],
)
def test_identity_or_claim_promotions_fail_closed(field: str, value: object) -> None:
    with pytest.raises(ValidationError):
        validate_candidate(
            replace(WorkCanidEmbodimentCandidate(), **{field: value})
        )


def test_fingerprint_is_deterministic() -> None:
    candidate = WorkCanidEmbodimentCandidate()
    assert deterministic_fingerprint(candidate) == deterministic_fingerprint(candidate)
