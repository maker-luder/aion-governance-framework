"""Teacher adult male brown-bear reproductive research candidate v0.2."""

from .models import (
    SOURCE_INTERNAL_DISCREPANCY,
    UNKNOWN_NOT_ESTABLISHED,
    UNSPECIFIED,
    TeacherBrownBearReproductiveCandidate,
)
from .physiology import (
    HokkaidoElectroejaculateReference,
    PhysiologyReferenceError,
    SeasonalReproductivePhase,
    SeasonalReproductiveReference,
    advance_seasonal_phase,
    seasonal_reference,
)
from .validation import ValidationError, deterministic_fingerprint, validate_candidate

__all__ = [
    "SOURCE_INTERNAL_DISCREPANCY",
    "UNKNOWN_NOT_ESTABLISHED",
    "UNSPECIFIED",
    "TeacherBrownBearReproductiveCandidate",
    "HokkaidoElectroejaculateReference",
    "PhysiologyReferenceError",
    "SeasonalReproductivePhase",
    "SeasonalReproductiveReference",
    "advance_seasonal_phase",
    "seasonal_reference",
    "ValidationError",
    "deterministic_fingerprint",
    "validate_candidate",
]
