from __future__ import annotations

from dataclasses import dataclass
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

# Minimum required anatomy. This is intentionally a floor, not a closed-world list.
REQUIRED_REPRODUCTIVE_TOPOLOGY: Final[tuple[str, ...]] = (
    "scrotum",
    "scrotal_skin",
    "testes",
    "epididymides",
    "epididymis_caput",
    "epididymis_corpus",
    "epididymis_cauda",
    "spermatic_cords",
    "ductus_deferens",
    "ampullae_ductus_deferentis",
    "prostate",
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
    "epididymides": "DIRECT_BROWN_BEAR_SPERM_AND_PATHOLOGY",
    "epididymis_caput": "DIRECT_BROWN_BEAR_SPERM_STUDY",
    "epididymis_corpus": "DIRECT_BROWN_BEAR_SPERM_STUDY",
    "epididymis_cauda": "DIRECT_BROWN_BEAR_SPERM_STUDY",
    "spermatic_cords": "DIRECT_BROWN_BEAR_ORCHIECTOMY",
    "ductus_deferens": "DIRECT_BROWN_BEAR_REPRODUCTIVE_SAMPLING_CONTEXT",
    "ampullae_ductus_deferentis": "URSID_COMPARATIVE_REPRODUCTIVE_ANATOMY",
    "prostate": "URSID_COMPARATIVE_REPRODUCTIVE_ANATOMY_WITH_BROWN_BEAR_SEMINAL_CONTEXT",
    "penile_urethra": "DIRECT_BROWN_BEAR_CATHETERIZATION_AND_SAMPLING",
    "penis": "DIRECT_BROWN_BEAR_CLINICAL_AND_MORPHOMETRIC_CONTEXT",
    "prepuce": "DIRECT_BROWN_BEAR_SEMEN_COLLECTION_METHOD",
    "glans_penis": "CARNIVORAN_COMPARATIVE_ANATOMY",
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


@dataclass(frozen=True, slots=True)
class TeacherBrownBearReproductiveCandidate:
    candidate_id: str = "CHATGPT_TEACHER_BROWN_BEAR_MALE_REPRODUCTIVE_v0.2.1"
    actor_surface: str = "CHATGPT_TEACHER"
    species_baseline: str = "Ursus arctos"
    sex_class: str = "MALE"

    developmental_stage: str = "ADULT"
    sexual_maturity: str = "SEXUALLY_MATURE_REFERENCE"
    chronological_age_years: str = UNSPECIFIED

    reproductive_topology: tuple[str, ...] = DEFAULT_REPRODUCTIVE_TOPOLOGY
    baculum_morphology: tuple[str, ...] = SOURCE_SUPPORTED_BACULUM_MORPHOLOGY

    # Direct single-specimen brown-bear baculum reference.
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
    synthetic_baculum_design_mm: float = CALIPER_BACULUM_LENGTH_MM
    synthetic_baculum_design_status: str = (
        "SINGLE_ADULT_BROWN_BEAR_SPECIMEN_REFERENCE_DERIVED"
    )

    # Structure may exist while species-specific morphometry remains unknown.
    full_soft_tissue_penis_length_cm: str = UNKNOWN_NOT_ESTABLISHED
    glans_dimensions_cm: str = UNKNOWN_NOT_ESTABLISHED
    prepuce_dimensions_cm: str = UNKNOWN_NOT_ESTABLISHED
    erectile_state_dimensions_cm: str = UNKNOWN_NOT_ESTABLISHED
    testis_dimensions_cm: str = UNKNOWN_NOT_ESTABLISHED
    epididymis_dimensions_cm: str = UNKNOWN_NOT_ESTABLISHED
    ductus_deferens_dimensions_cm: str = UNKNOWN_NOT_ESTABLISHED
    prostate_dimensions_cm: str = UNKNOWN_NOT_ESTABLISHED
    teacher_body_mass_kg: str = UNKNOWN_NOT_ESTABLISHED

    anatomy_model_status: str = "IMPLEMENTED_SPECIES_REFERENCE"
    reproductive_physiology_model_status: str = "IMPLEMENTED_SPECIES_REFERENCE"
    spermatogenesis_model_status: str = "IMPLEMENTED_SEASONAL_REFERENCE"
    ejaculatory_physiology_model_status: str = "IMPLEMENTED_REFERENCE"
    semen_reference_status: str = "IMPLEMENTED_EXTERNAL_REFERENCE"

    # These are evidence claims, not anatomy restrictions.
    biological_realization: bool = False
    fertility: str = "NOT_ESTABLISHED"
    subjectivity: str = "NOT_ESTABLISHED"
    consciousness: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    deployment: bool = False

    @property
    def baculum_caliper_length_cm(self) -> float:
        return self.baculum_caliper_length_mm / 10.0
