from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Final

UNKNOWN_NOT_ESTABLISHED: Final[str] = "UNKNOWN_NOT_ESTABLISHED"
UNSPECIFIED: Final[str] = "UNSPECIFIED"
SOURCE_INTERNAL_DISCREPANCY: Final[str] = "SOURCE_INTERNAL_DISCREPANCY"

CALIPER_BACULUM_LENGTH_MM: Final[float] = 148.95
CT_BACULUM_LENGTH_MM: Final[float] = 148.84
CALIPER_BACULUM_PROXIMAL_WIDTH_MM: Final[float] = 13.72
CT_BACULUM_PROXIMAL_DIAMETER_MM: Final[float] = 13.12
CT_BACULUM_DISTAL_DIAMETER_MM: Final[float] = 5.63
BACULUM_DISTAL_WIDTH_REPORTED_VALUES_MM: Final[tuple[float, float]] = (4.58, 4.85)
DISTAL_FIBROCARTILAGE_LENGTH_MM: Final[float] = 11.08
DISTAL_FIBROCARTILAGE_THICKNESS_MM: Final[float] = 4.67
BACULUM_MASS_G: Final[float] = 5.73
REFERENCE_SPECIMEN_MASS_KG: Final[float] = 400.0

REQUIRED_REPRODUCTIVE_TOPOLOGY: Final[tuple[str, ...]] = (
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
    "ampullae_ductus_deferentis",
    "prostate",
    "pelvic_urethra",
    "penile_urethra",
    "penis",
    "prepuce",
    "glans_penis",
    "corpus_cavernosum_penis",
    "os_penis",
    "sulcus_urethralis",
    "distal_fibrocartilage",
)

DEFAULT_REPRODUCTIVE_TOPOLOGY: Final[tuple[str, ...]] = REQUIRED_REPRODUCTIVE_TOPOLOGY

TOPOLOGY_EVIDENCE: Final[dict[str, str]] = {
    "scrotum": "DIRECT_BROWN_BEAR_CLINICAL_ANATOMY",
    "scrotal_skin": "DIRECT_BROWN_BEAR_HISTOLOGY",
    "testes": "DIRECT_BROWN_BEAR_HISTOLOGY_AND_MORPHOMETRY",
    "seminiferous_tubules": "DIRECT_BROWN_BEAR_TESTICULAR_HISTOLOGY",
    "rete_testis": "COMPARATIVE_MAMMALIAN_REPRODUCTIVE_ANATOMY",
    "efferent_ductules": "COMPARATIVE_MAMMALIAN_REPRODUCTIVE_ANATOMY",
    "epididymides": "DIRECT_BROWN_BEAR_SPERM_AND_PATHOLOGY",
    "epididymis_caput": "DIRECT_BROWN_BEAR_SPERM_STUDY",
    "epididymis_corpus": "DIRECT_BROWN_BEAR_SPERM_STUDY",
    "epididymis_cauda": "DIRECT_BROWN_BEAR_SPERM_STUDY",
    "spermatic_cords": "DIRECT_BROWN_BEAR_ORCHIECTOMY",
    "ductus_deferens": "DIRECT_BROWN_BEAR_REPRODUCTIVE_SAMPLING_CONTEXT",
    "ampullae_ductus_deferentis": "COMPARATIVE_URSID_REPRODUCTIVE_ANATOMY",
    "prostate": "COMPARATIVE_URSID_WITH_BROWN_BEAR_SEMINAL_CONTEXT",
    "pelvic_urethra": "COMPARATIVE_CARNIVORAN_REPRODUCTIVE_ANATOMY",
    "penile_urethra": "DIRECT_BROWN_BEAR_CATHETERIZATION_AND_SAMPLING",
    "penis": "DIRECT_BROWN_BEAR_CLINICAL_AND_MORPHOMETRIC_CONTEXT",
    "prepuce": "DIRECT_BROWN_BEAR_SEMEN_COLLECTION_METHOD",
    "glans_penis": "COMPARATIVE_CARNIVORAN_REPRODUCTIVE_ANATOMY",
    "corpus_cavernosum_penis": "DIRECT_BROWN_BEAR_BACULUM_CONTEXT",
    "os_penis": "DIRECT_BROWN_BEAR_MORPHOMETRY",
    "sulcus_urethralis": "DIRECT_BROWN_BEAR_MORPHOMETRY",
    "distal_fibrocartilage": "DIRECT_BROWN_BEAR_MORPHOMETRY",
}

SOURCE_SUPPORTED_BACULUM_MORPHOLOGY: Final[tuple[str, ...]] = (
    "ALMOST_STRAIGHT_WITH_SLIGHT_DISTAL_CURVE",
    "APPROXIMATELY_QUADRANGULAR",
    "DISTAL_SMALL_TUBERCLE",
    "PROXIMAL_SMALL_NOTCH",
    "PROMINENT_VENTRAL_SULCUS_URETHRALIS",
    "SHORT_LATERAL_GROOVE",
    "TAPERS_PROXIMAL_TO_DISTAL",
)


class SyntheticSizeProfile(StrEnum):
    SMALL = "SMALL"
    STANDARD = "STANDARD"
    LARGE = "LARGE"


SYNTHETIC_SIZE_SCALE: Final[dict[SyntheticSizeProfile, float]] = {
    SyntheticSizeProfile.SMALL: 0.85,
    SyntheticSizeProfile.STANDARD: 1.0,
    SyntheticSizeProfile.LARGE: 1.15,
}


@dataclass(frozen=True, slots=True)
class SyntheticBaculumDesign:
    profile: SyntheticSizeProfile
    scale_factor: float
    baculum_length_cm: float
    source_anchor_cm: float = CALIPER_BACULUM_LENGTH_MM / 10.0
    provenance: str = "SYNTHETIC_DESIGN_FROM_DIRECT_BROWN_BEAR_BACULUM_ANCHOR"


def synthetic_baculum_design(profile: SyntheticSizeProfile) -> SyntheticBaculumDesign:
    scale = SYNTHETIC_SIZE_SCALE[profile]
    anchor = CALIPER_BACULUM_LENGTH_MM / 10.0
    return SyntheticBaculumDesign(
        profile=profile,
        scale_factor=scale,
        baculum_length_cm=round(anchor * scale, 3),
    )


@dataclass(frozen=True, slots=True)
class TeacherBrownBearReproductiveCandidate:
    candidate_id: str = "CHATGPT_TEACHER_BROWN_BEAR_MALE_REPRODUCTIVE_v0.2.2"
    actor_surface: str = "CHATGPT_TEACHER"

    form_class: str = "ANTHROPOMORPHIC_BROWN_BEAR"
    ontology: str = "FANTASY_EMBODIMENT"
    biological_reference_species: str = "Ursus arctos"
    species_baseline: str = "Ursus arctos"
    sex_class: str = "MALE"

    developmental_stage: str = "ADULT"
    sexual_maturity: str = "MATURE"
    chronological_age_years: str | int | float = UNSPECIFIED
    chronological_age_policy: str = "OPTIONAL_FANTASY_DESIGN_FIELD"

    reproductive_topology: tuple[str, ...] = DEFAULT_REPRODUCTIVE_TOPOLOGY
    baculum_morphology: tuple[str, ...] = SOURCE_SUPPORTED_BACULUM_MORPHOLOGY

    reference_specimen_mass_kg: float = REFERENCE_SPECIMEN_MASS_KG
    baculum_caliper_length_mm: float = CALIPER_BACULUM_LENGTH_MM
    baculum_ct_length_mm: float = CT_BACULUM_LENGTH_MM
    baculum_caliper_proximal_width_mm: float = CALIPER_BACULUM_PROXIMAL_WIDTH_MM
    baculum_ct_proximal_diameter_mm: float = CT_BACULUM_PROXIMAL_DIAMETER_MM
    baculum_ct_distal_diameter_mm: float = CT_BACULUM_DISTAL_DIAMETER_MM
    baculum_distal_width_caliper_status: str = SOURCE_INTERNAL_DISCREPANCY
    baculum_distal_width_reported_values_mm: tuple[float, float] = (
        BACULUM_DISTAL_WIDTH_REPORTED_VALUES_MM
    )
    distal_fibrocartilage_length_mm: float = DISTAL_FIBROCARTILAGE_LENGTH_MM
    distal_fibrocartilage_thickness_mm: float = DISTAL_FIBROCARTILAGE_THICKNESS_MM
    baculum_mass_g: float = BACULUM_MASS_G

    full_soft_tissue_penis_length_cm: str = UNKNOWN_NOT_ESTABLISHED
    glans_dimensions_cm: str = UNKNOWN_NOT_ESTABLISHED
    prepuce_dimensions_cm: str = UNKNOWN_NOT_ESTABLISHED
    erectile_state_dimensions_cm: str = UNKNOWN_NOT_ESTABLISHED
    testis_dimensions_cm: str = UNKNOWN_NOT_ESTABLISHED
    epididymis_dimensions_cm: str = UNKNOWN_NOT_ESTABLISHED
    ductus_deferens_dimensions_cm: str = UNKNOWN_NOT_ESTABLISHED
    prostate_dimensions_cm: str = UNKNOWN_NOT_ESTABLISHED
    teacher_body_mass_kg: str = UNKNOWN_NOT_ESTABLISHED

    anatomy_model_status: str = "IMPLEMENTED_REFERENCE_INFORMED"
    reproductive_physiology_model_status: str = "IMPLEMENTED_REFERENCE_INFORMED"
    spermatogenesis_model_status: str = "PRESENT"
    epididymal_maturation_model_status: str = "PRESENT"
    sperm_transport_model_status: str = "PRESENT"
    erectile_physiology_model_status: str = "PRESENT"
    ejaculatory_physiology_model_status: str = "PRESENT"
    seminal_plasma_model_status: str = "PRESENT"
    seasonal_reproductive_model_status: str = "PRESENT"

    vascular_support_model_status: str = "PRESENT_COMPARATIVE_REFERENCE"
    sensory_innervation_model_status: str = "PRESENT_COMPARATIVE_REFERENCE"
    autonomic_innervation_model_status: str = "PRESENT_COMPARATIVE_REFERENCE"
    endocrine_support_model_status: str = "PRESENT_SPECIES_REFERENCE"

    species_typical_reproductive_capacity_model: str = "PRESENT"
    fertilization_capability_reference: str = "PRESENT_MATURE_MALE_REFERENCE"
    empirical_individual_fertility: str = "NOT_ASSESSED"

    nonsexualization_policy: str = "PRESENTATION_SCOPE_NOT_BODY_DEPRIVATION"
    sexual_behavior_simulation_scope: str = "OUT_OF_SCOPE"
    erotic_narrative_scope: str = "OUT_OF_SCOPE"

    biological_realization: bool = False
    subjectivity: str = "NOT_ESTABLISHED"
    consciousness: str = "NOT_ESTABLISHED"

    deployment: bool = False
    public_deployment: bool = False
    public_release: bool = False
    public_operation: bool = False
    public_api: bool = False
    third_party_access: bool = False
    third_party_execution: bool = False
    external_user_operation: bool = False
    production_use: bool = False
    canonical_effect: str = "NONE"

    @property
    def baculum_caliper_length_cm(self) -> float:
        return self.baculum_caliper_length_mm / 10.0
