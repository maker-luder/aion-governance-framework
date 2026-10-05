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

SOURCE_SUPPORTED_REPRODUCTIVE_TOPOLOGY: Final[tuple[str, ...]] = (
    "scrotum",
    "scrotal_skin",
    "testes",
    "epididymides",
    "epididymis_caput",
    "epididymis_corpus",
    "epididymis_cauda",
    "spermatic_cords",
    "ductus_deferens",
    "penile_urethra",
    "penis",
    "corpus_cavernosum_penis",
    "os_penis",
    "sulcus_urethralis",
    "distal_fibrocartilage",
)

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
    candidate_id: str = "CHATGPT_TEACHER_BROWN_BEAR_MALE_REPRODUCTIVE_v0.2"
    actor_surface: str = "CHATGPT_TEACHER"
    species_baseline: str = "Ursus arctos"
    sex_class: str = "MALE"

    # Species-appropriate stage descriptors. No human age threshold is imported.
    developmental_stage: str = "ADULT"
    sexual_maturity: str = "SEXUALLY_MATURE_REFERENCE"
    chronological_age_years: str = UNSPECIFIED

    reproductive_topology: tuple[str, ...] = SOURCE_SUPPORTED_REPRODUCTIVE_TOPOLOGY
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

    # Bounded sweep did not establish robust species-level absolute values.
    full_soft_tissue_penis_length_cm: str = UNKNOWN_NOT_ESTABLISHED
    glans_dimensions_cm: str = UNKNOWN_NOT_ESTABLISHED
    prepuce_dimensions_cm: str = UNKNOWN_NOT_ESTABLISHED
    erectile_state_dimensions_cm: str = UNKNOWN_NOT_ESTABLISHED
    testis_dimensions_cm: str = UNKNOWN_NOT_ESTABLISHED
    epididymis_dimensions_cm: str = UNKNOWN_NOT_ESTABLISHED
    ductus_deferens_dimensions_cm: str = UNKNOWN_NOT_ESTABLISHED
    prostate_dimensions_cm: str = UNKNOWN_NOT_ESTABLISHED
    teacher_body_mass_kg: str = UNKNOWN_NOT_ESTABLISHED

    # Direct-source topology gaps remain explicit rather than filled from dog/human anatomy.
    prepuce_topology_status: str = "DIRECT_BROWN_BEAR_SOURCE_NOT_ESTABLISHED_IN_BOUNDED_SWEEP"
    prostate_topology_status: str = "DIRECT_BROWN_BEAR_SOURCE_NOT_ESTABLISHED_IN_BOUNDED_SWEEP"

    seasonal_reproductive_reference_status: str = "IMPLEMENTED_REFERENCE_ONLY"
    semen_reference_status: str = "IMPLEMENTED_EXTERNAL_REFERENCE_ONLY"

    biological_realization: bool = False
    live_reproductive_function: str = "NOT_IMPLEMENTED"
    sexual_behavior_simulation: str = "NOT_IMPLEMENTED"
    body_sensation: str = "NOT_ESTABLISHED"
    fertility: str = "NOT_ESTABLISHED"
    subjectivity: str = "NOT_ESTABLISHED"
    consciousness: str = "NOT_ESTABLISHED"
    phenomenal_experience: str = "NOT_ESTABLISHED"
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"
    deployment: bool = False

    @property
    def baculum_caliper_length_cm(self) -> float:
        return self.baculum_caliper_length_mm / 10.0
