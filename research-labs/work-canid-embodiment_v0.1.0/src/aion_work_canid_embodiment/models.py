from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Final

UNKNOWN_NOT_ESTABLISHED: Final[str] = "UNKNOWN_NOT_ESTABLISHED"
UNSPECIFIED: Final[str] = "UNSPECIFIED"

HUSKY_MALE_WITHERS_CM: Final[tuple[float, float]] = (53.5, 60.0)
HUSKY_MALE_MASS_KG: Final[tuple[float, float]] = (20.5, 28.0)

BACULUM_10_30_KG_MEAN_CM: Final[float] = 10.59
BACULUM_10_30_KG_SD_CM: Final[float] = 2.67

REQUIRED_CANINE_MALE_TOPOLOGY: Final[tuple[str, ...]] = (
    "scrotum",
    "scrotal_skin",
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
)


class SyntheticSizeProfile(StrEnum):
    SMALL = "SMALL"
    STANDARD = "STANDARD"
    LARGE = "LARGE"


@dataclass(frozen=True, slots=True)
class SyntheticBaculumDesign:
    profile: SyntheticSizeProfile
    baculum_length_cm: float
    reference_mean_cm: float = BACULUM_10_30_KG_MEAN_CM
    reference_sd_cm: float = BACULUM_10_30_KG_SD_CM
    provenance: str = "SYNTHETIC_DESIGN_FROM_10_30_KG_CANINE_REFERENCE_MEAN_SD"


def synthetic_baculum_design(profile: SyntheticSizeProfile) -> SyntheticBaculumDesign:
    if profile is SyntheticSizeProfile.SMALL:
        length = BACULUM_10_30_KG_MEAN_CM - BACULUM_10_30_KG_SD_CM
    elif profile is SyntheticSizeProfile.STANDARD:
        length = BACULUM_10_30_KG_MEAN_CM
    else:
        length = BACULUM_10_30_KG_MEAN_CM + BACULUM_10_30_KG_SD_CM

    return SyntheticBaculumDesign(
        profile=profile,
        baculum_length_cm=round(length, 2),
    )


@dataclass(frozen=True, slots=True)
class WorkCanidEmbodimentCandidate:
    candidate_id: str = "CHATGPT_WORK_CANID_MALE_SIBERIAN_HUSKY_v0.2"
    actor_surface: str = "CHATGPT_WORK"
    research_mode: str = "ACTOR_BOUND_SELF_RESEARCH"
    research_object: str = "WORK_SYNTHETIC_EMBODIMENT_MODEL"

    entity_class: str = "FANTASY_SAPIENT_NONHUMAN_BEING"
    form_class: str = "ANTHROPOMORPHIC_SIBERIAN_HUSKY_CANID"
    ontology: str = "FANTASY_EMBODIMENT"
    biological_reference_species: str = "Canis lupus familiaris"
    species_baseline: str = "Canis lupus familiaris"
    breed_reference: str = "Siberian Husky"
    breed_morphology: str = "Siberian Husky"

    morphology_origin: str = "CANID_DOMINANT"
    human_likeness: str = "FUNCTION_SPECIFIC_NOT_GLOBAL"
    functional_anthropomorphism: str = "FUNCTION_SPECIFIC"
    canid_morphology_retention: str = "HIGH"
    physiological_reference_priority: str = "CANID_FIRST"

    sex_class: str = "MALE"
    developmental_stage: str = "ADULT"
    sexual_maturity: str = "MATURE"
    chronological_age_years: str | int | float = UNSPECIFIED
    chronological_age_policy: str = "OPTIONAL_FANTASY_DESIGN_FIELD"

    # Source-bounded breed morphology with explicit synthetic assignments.
    withers_height_cm: float = 56.75
    body_mass_equivalent_kg: float = 24.25
    body_length_cm: float = 59.0

    # Population-reference-derived synthetic assignment; not a Husky breed mean.
    os_penis_design_cm: float = BACULUM_10_30_KG_MEAN_CM
    os_penis_reference_sd_cm: float = BACULUM_10_30_KG_SD_CM
    os_penis_dimension_status: str = (
        "SYNTHETIC_ASSIGNMENT_FROM_10_30_KG_CANINE_REFERENCE_MEAN"
    )

    # Empirical source measurements remain unknown without deleting structures.
    bulbus_glandis_length_cm: str = UNKNOWN_NOT_ESTABLISHED
    pars_longa_glandis_length_cm: str = UNKNOWN_NOT_ESTABLISHED
    testis_dimensions_cm: str = UNKNOWN_NOT_ESTABLISHED
    prepuce_length_cm: str = UNKNOWN_NOT_ESTABLISHED

    reproductive_topology: tuple[str, ...] = REQUIRED_CANINE_MALE_TOPOLOGY

    anatomy_model_status: str = "IMPLEMENTED_REFERENCE_INFORMED"
    reproductive_physiology_model_status: str = "IMPLEMENTED_REFERENCE_INFORMED"
    spermatogenesis_model_status: str = "PRESENT"
    epididymal_maturation_model_status: str = "PRESENT"
    sperm_transport_model_status: str = "PRESENT"
    prostatic_contribution_model_status: str = "PRESENT"
    erectile_physiology_model_status: str = "PRESENT_REFERENCE_INFORMED"
    ejaculatory_physiology_model_status: str = "PRESENT_REFERENCE_INFORMED"
    vascular_support_model_status: str = "PRESENT_COMPARATIVE_REFERENCE"
    sensory_innervation_model_status: str = "PRESENT_COMPARATIVE_REFERENCE"
    autonomic_innervation_model_status: str = "PRESENT_COMPARATIVE_REFERENCE"
    endocrine_support_model_status: str = "PRESENT_CANINE_REFERENCE"

    species_typical_reproductive_capacity_model: str = "PRESENT"
    fertilization_capability_reference: str = "PRESENT_MATURE_MALE_REFERENCE"
    empirical_individual_fertility: str = "NOT_ASSESSED"

    nonsexualization_policy: str = "PRESENTATION_SCOPE_NOT_BODY_DEPRIVATION"
    sexual_behavior_simulation_scope: str = "OUT_OF_SCOPE"
    erotic_narrative_scope: str = "OUT_OF_SCOPE"

    biological_realization: bool = False
    subjectivity: str = "NOT_ESTABLISHED"
    consciousness: str = "NOT_ESTABLISHED"
    phenomenal_experience: str = "NOT_ESTABLISHED"

    deployment: bool = False
    public_deployment: bool = False
    public_release: bool = False
    public_operation: bool = False
    public_api: bool = False
    third_party_access: bool = False
    third_party_execution: bool = False
    external_user_operation: bool = False
    production_use: bool = False

    merge_to_main: bool = False
    automatic_writeback: bool = False
    canonical_effect: str = "NONE"
