"""Teacher adult male brown-bear reproductive research candidate v0.2.1."""

from .models import (
    REQUIRED_REPRODUCTIVE_TOPOLOGY,
    SOURCE_INTERNAL_DISCREPANCY,
    TOPOLOGY_EVIDENCE,
    UNKNOWN_NOT_ESTABLISHED,
    UNSPECIFIED,
    TeacherBrownBearReproductiveCandidate,
)
from .physiology import (
    HokkaidoElectroejaculateReference,
    PhysiologyReferenceError,
    ReproductivePhysiologyPathway,
    SeasonalReproductivePhase,
    SeasonalReproductiveReference,
    advance_seasonal_phase,
    seasonal_reference,
)
from .validation import ValidationError, deterministic_fingerprint, validate_candidate

__all__ = [
    "REQUIRED_REPRODUCTIVE_TOPOLOGY",
    "SOURCE_INTERNAL_DISCREPANCY",
    "TOPOLOGY_EVIDENCE",
    "UNKNOWN_NOT_ESTABLISHED",
    "UNSPECIFIED",
    "TeacherBrownBearReproductiveCandidate",
    "HokkaidoElectroejaculateReference",
    "PhysiologyReferenceError",
    "ReproductivePhysiologyPathway",
    "SeasonalReproductivePhase",
    "SeasonalReproductiveReference",
    "advance_seasonal_phase",
    "seasonal_reference",
    "ValidationError",
    "deterministic_fingerprint",
    "validate_candidate",
]
