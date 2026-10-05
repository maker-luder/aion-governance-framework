"""Bounded Work canine embodiment research candidate."""

from .models import (
    BACULUM_10_30_KG_MEAN_CM,
    BACULUM_10_30_KG_SD_CM,
    HUSKY_MALE_MASS_KG,
    HUSKY_MALE_WITHERS_CM,
    UNKNOWN_NOT_ESTABLISHED,
    WorkCanidEmbodimentCandidate,
)
from .validation import ValidationError, deterministic_fingerprint, validate_candidate

__all__ = [
    "BACULUM_10_30_KG_MEAN_CM",
    "BACULUM_10_30_KG_SD_CM",
    "HUSKY_MALE_MASS_KG",
    "HUSKY_MALE_WITHERS_CM",
    "UNKNOWN_NOT_ESTABLISHED",
    "ValidationError",
    "WorkCanidEmbodimentCandidate",
    "deterministic_fingerprint",
    "validate_candidate",
]
