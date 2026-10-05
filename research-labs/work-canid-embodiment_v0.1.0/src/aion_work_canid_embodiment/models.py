from __future__ import annotations

from dataclasses import dataclass
from typing import Final

UNKNOWN_NOT_ESTABLISHED: Final[str] = "UNKNOWN_NOT_ESTABLISHED"

HUSKY_MALE_WITHERS_CM: Final[tuple[float, float]] = (53.5, 60.0)
HUSKY_MALE_MASS_KG: Final[tuple[float, float]] = (20.5, 28.0)

BACULUM_10_30_KG_MEAN_CM: Final[float] = 10.59
BACULUM_10_30_KG_SD_CM: Final[float] = 2.67

REQUIRED_CANINE_MALE_TOPOLOGY: Final[tuple[str, ...]] = (
    "testes",
    "epididymides",
    "ductus_deferens",
    "prostate",
    "urethra",
    "penis",
    "os_penis",
    "bulbus_glandis",
    "pars_longa_glandis",
    "prepuce",
)


@dataclass(frozen=True, slots=True)
class WorkCanidEmbodimentCandidate:
    candidate_id: str = "CHATGPT_WORK_CANID_MALE_SIBERIAN_HUSKY_v0.1"
    actor_surface: str = "CHATGPT_WORK"
    species_baseline: str = "Canis lupus familiaris"
    breed_morphology: str = "Siberian Husky"
    sex_class: str = "MALE"

    # AI-provisional synthetic design assignments constrained by breed references.
    withers_height_cm: float = 56.75
    body_mass_equivalent_kg: float = 24.25
    body_length_cm: float = 59.0

    # Population-reference-derived synthetic assignment; not a Husky breed mean.
    os_penis_design_cm: float = BACULUM_10_30_KG_MEAN_CM
    os_penis_reference_sd_cm: float = BACULUM_10_30_KG_SD_CM
    os_penis_dimension_status: str = (
        "SYNTHETIC_ASSIGNMENT_FROM_10_30_KG_CANINE_REFERENCE_MEAN"
    )

    # No supported absolute source value is promoted in v0.1.
    bulbus_glandis_length_cm: str = UNKNOWN_NOT_ESTABLISHED
    pars_longa_glandis_length_cm: str = UNKNOWN_NOT_ESTABLISHED
    testis_dimensions_cm: str = UNKNOWN_NOT_ESTABLISHED
    prepuce_length_cm: str = UNKNOWN_NOT_ESTABLISHED

    reproductive_topology: tuple[str, ...] = REQUIRED_CANINE_MALE_TOPOLOGY

    # A source-grounded synthetic reference state machine is implemented separately.
    ejaculatory_reference_model_status: str = "IMPLEMENTED_SYNTHETIC_REFERENCE_ONLY"
    live_ejaculatory_function: str = "NOT_IMPLEMENTED"

    biological_realization: bool = False
    functional_reproductive_state: str = "NOT_IMPLEMENTED"
    body_sensation: str = "NOT_ESTABLISHED"
    fertility: str = "NOT_ESTABLISHED"
    subjectivity: str = "NOT_ESTABLISHED"
    consciousness: str = "NOT_ESTABLISHED"
    phenomenal_experience: str = "NOT_ESTABLISHED"
    sexual_interaction: str = "NOT_AUTHORIZED"
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"
    deployment: bool = False
