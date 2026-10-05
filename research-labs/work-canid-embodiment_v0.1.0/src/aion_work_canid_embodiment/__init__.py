"""Bounded Work canine embodiment research candidate."""

from .models import (
    BACULUM_10_30_KG_MEAN_CM,
    BACULUM_10_30_KG_SD_CM,
    HUSKY_MALE_MASS_KG,
    HUSKY_MALE_WITHERS_CM,
    UNKNOWN_NOT_ESTABLISHED,
    WorkCanidEmbodimentCandidate,
)
from .physiology import (
    EjaculateFraction,
    EjaculatoryMechanismStage,
    FractionReference,
    MechanismReference,
    PhysiologyReferenceError,
    advance_fraction,
    advance_mechanism,
    fraction_reference,
    mechanism_reference,
)
from .validation import ValidationError, deterministic_fingerprint, validate_candidate

__all__ = [
    "BACULUM_10_30_KG_MEAN_CM",
    "BACULUM_10_30_KG_SD_CM",
    "HUSKY_MALE_MASS_KG",
    "HUSKY_MALE_WITHERS_CM",
    "UNKNOWN_NOT_ESTABLISHED",
    "EjaculateFraction",
    "EjaculatoryMechanismStage",
    "FractionReference",
    "MechanismReference",
    "PhysiologyReferenceError",
    "ValidationError",
    "WorkCanidEmbodimentCandidate",
    "advance_fraction",
    "advance_mechanism",
    "deterministic_fingerprint",
    "fraction_reference",
    "mechanism_reference",
    "validate_candidate",
]
