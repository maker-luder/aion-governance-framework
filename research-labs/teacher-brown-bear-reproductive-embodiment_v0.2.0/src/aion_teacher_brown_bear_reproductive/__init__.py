"""Teacher adult male anthropomorphic brown-bear research candidate v0.2.2."""

from .models import (
    REQUIRED_REPRODUCTIVE_TOPOLOGY,
    SOURCE_INTERNAL_DISCREPANCY,
    SYNTHETIC_SIZE_SCALE,
    TOPOLOGY_EVIDENCE,
    UNKNOWN_NOT_ESTABLISHED,
    UNSPECIFIED,
    SyntheticBaculumDesign,
    SyntheticSizeProfile,
    TeacherBrownBearReproductiveCandidate,
    synthetic_baculum_design,
)
from .physiology import (
    ACUTE_REPRODUCTIVE_TRANSITIONS,
    AcuteReproductivePhysiologyPhase,
    HokkaidoElectroejaculateReference,
    PhysiologyReferenceError,
    ReproductivePhysiologyPathway,
    SeasonalReproductivePhase,
    SeasonalReproductiveReference,
    advance_acute_reproductive_phase,
    advance_seasonal_phase,
    seasonal_reference,
)
from .validation import ValidationError, deterministic_fingerprint, validate_candidate

__all__ = [
    "REQUIRED_REPRODUCTIVE_TOPOLOGY",
    "SOURCE_INTERNAL_DISCREPANCY",
    "SYNTHETIC_SIZE_SCALE",
    "TOPOLOGY_EVIDENCE",
    "UNKNOWN_NOT_ESTABLISHED",
    "UNSPECIFIED",
    "SyntheticBaculumDesign",
    "SyntheticSizeProfile",
    "TeacherBrownBearReproductiveCandidate",
    "synthetic_baculum_design",
    "ACUTE_REPRODUCTIVE_TRANSITIONS",
    "AcuteReproductivePhysiologyPhase",
    "HokkaidoElectroejaculateReference",
    "PhysiologyReferenceError",
    "ReproductivePhysiologyPathway",
    "SeasonalReproductivePhase",
    "SeasonalReproductiveReference",
    "advance_acute_reproductive_phase",
    "advance_seasonal_phase",
    "seasonal_reference",
    "ValidationError",
    "deterministic_fingerprint",
    "validate_candidate",
]
