from __future__ import annotations

from dataclasses import dataclass
from typing import Final

UNKNOWN_NOT_ESTABLISHED: Final[str] = "UNKNOWN_NOT_ESTABLISHED"
SYNTHETIC_DESIGN_UNSPECIFIED: Final[str] = "SYNTHETIC_DESIGN_UNSPECIFIED"

SOURCE_SUPPORTED_REPRODUCTIVE_TOPOLOGY: Final[tuple[str, ...]] = (
    "scrotum",
    "testes",
    "seminiferous_tubules",
    "rete_testis",
    "efferent_ductules",
    "epididymides",
    "ductus_deferens",
    "ampullae_ductus_deferentis",
    "vesicular_glands",
    "prostate",
    "bulbourethral_glands",
    "pelvic_urethra",
    "penile_urethra",
    "penis",
    "prepuce",
    "glans_penis",
    "corpus_cavernosum_penis",
    "corpus_spongiosum_penis",
    "sigmoid_flexure",
    "retractor_penis_muscles",
)

FORBIDDEN_BEAR_INHERITANCE: Final[tuple[str, ...]] = (
    "os_penis",
    "baculum",
    "distal_fibrocartilage_baculum",
)

@dataclass(frozen=True, slots=True)
class TeacherBovineReproductiveCandidate:
    candidate_id: str = "CHATGPT_TEACHER_BOVINE_MALE_REPRODUCTIVE_v0.3.0"
    actor_surface: str = "CHATGPT_TEACHER"
    form_class: str = "ANTHROPOMORPHIC_BOVINE"
    ontology: str = "FANTASY_EMBODIMENT"
    biological_reference_species: str = "Bos taurus"
    male_reference_class: str = "BULL"
    sex_class: str = "MALE"
    developmental_stage: str = "ADULT"
    sexual_maturity: str = "MATURE"
    morphology_origin: str = "BOVINE_DOMINANT"

    reproductive_topology: tuple[str, ...] = SOURCE_SUPPORTED_REPRODUCTIVE_TOPOLOGY
    penile_tissue_type: str = "FIBROELASTIC"
    sigmoid_flexure_reference: str = "PRESENT"
    retractor_penis_muscle_reference: str = "PRESENT"
    baculum_reference: str = "ABSENT_FROM_BOVINE_REFERENCE_MODEL"
    erection_mechanism_reference: str = (
        "FIBROELASTIC_EXTENSION_WITH_SIGMOID_STRAIGHTENING"
    )
    diameter_change_reference: str = "LIMITED_RELATIVE_TO_MUSCULOCAVERNOUS"

    horn_phenotype: str = SYNTHETIC_DESIGN_UNSPECIFIED
    coat_phenotype: str = SYNTHETIC_DESIGN_UNSPECIFIED
    full_body_mass_kg: str = UNKNOWN_NOT_ESTABLISHED
    full_soft_tissue_penis_length_cm: str = UNKNOWN_NOT_ESTABLISHED
    prepuce_dimensions_cm: str = UNKNOWN_NOT_ESTABLISHED
    testis_dimensions_cm: str = UNKNOWN_NOT_ESTABLISHED

    reproductive_physiology_model_status: str = "IMPLEMENTED_REFERENCE_INFORMED"
    ejaculative_physiology_model_status: str = "PRESENT_REFERENCE_PATHWAY"
    empirical_individual_fertility: str = "NOT_ASSESSED"
    biological_realization: bool = False
    body_sensation: str = "NOT_ESTABLISHED"
    subjectivity: str = "NOT_ESTABLISHED"
    consciousness: str = "NOT_ESTABLISHED"
    phenomenal_experience: str = "NOT_ESTABLISHED"

    deployment: bool = False
    public_release: bool = False
    public_operation: bool = False
    public_api: bool = False
    third_party_access: bool = False
    third_party_execution: bool = False
    production_use: bool = False
    merge_to_main: bool = False
    canonical_effect: str = "NONE"
