from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Final

@dataclass(frozen=True, slots=True)
class WaterBuffaloReproductiveReference:
    source_scope: str = "ADULT_MALE_BUBALUS_BUBALIS_REVIEW_REFERENCE"
    penis_length_mean_cm: float = 80.15
    penis_thickness_mean_cm: float = 1.95
    seminal_vesicle_length_min_cm: float = 8.0
    seminal_vesicle_length_max_cm: float = 10.0
    seminal_vesicle_diameter_min_cm: float = 2.0
    seminal_vesicle_diameter_max_cm: float = 3.0
    adult_philippine_ampulla_length_cm: float = 7.4
    adult_philippine_ampulla_diameter_cm: float = 0.71
    adult_philippine_ampulla_age_scope_years: str = "3-5"
    scrotal_circumference_over_54_months_lower_reported_mean_cm: float = 33.5
    scrotal_circumference_over_54_months_upper_reported_mean_cm: float = 38.0
    scrotal_circumference_source_variation_status: str = "MULTI_STUDY_REFERENCE_RANGE_NOT_INDIVIDUAL_TARGET"
    synthetic_anthropomorphic_genital_scaling: str = "NOT_APPLIED_WITHOUT_EXPLICIT_JUSTIFICATION"

@dataclass(frozen=True, slots=True)
class SwampBuffaloSemenAgeReference:
    age_years: int
    ejaculate_volume_mean_ml: float
    ejaculate_volume_sd_ml: float
    ph_mean: float
    sperm_concentration_mean_million_per_ml: float
    sperm_concentration_sd_million_per_ml: float
    individual_motility_mean_percent: float
    individual_motility_sd_percent: float

SWAMP_BUFFALO_SEMEN_REFERENCE: Final[tuple[SwampBuffaloSemenAgeReference, ...]] = (
    SwampBuffaloSemenAgeReference(5, 2.83, 0.76, 6.69, 918.00, 233.14, 69.50, 3.68),
    SwampBuffaloSemenAgeReference(6, 2.49, 0.55, 6.69, 866.96, 242.19, 70.00, 0.00),
    SwampBuffaloSemenAgeReference(7, 3.53, 0.98, 6.65, 1059.98, 321.65, 66.29, 9.01),
)

class SexualFunctionPhase(StrEnum):
    BASELINE = "BASELINE"
    AUTONOMIC_ACTIVATION = "AUTONOMIC_ACTIVATION"
    RETRACTOR_RELAXATION = "RETRACTOR_RELAXATION"
    SIGMOID_STRAIGHTENING = "SIGMOID_STRAIGHTENING"
    PENILE_EXPOSURE = "PENILE_EXPOSURE"
    EMISSION = "EMISSION"
    URETHRAL_EXPULSION = "URETHRAL_EXPULSION"
    RETRACTION_RECOVERY = "RETRACTION_RECOVERY"

class PhysiologyTransitionError(ValueError):
    pass

_ALLOWED: Final[dict[SexualFunctionPhase, tuple[SexualFunctionPhase, ...]]] = {
    SexualFunctionPhase.BASELINE: (SexualFunctionPhase.AUTONOMIC_ACTIVATION,),
    SexualFunctionPhase.AUTONOMIC_ACTIVATION: (
        SexualFunctionPhase.RETRACTOR_RELAXATION,
        SexualFunctionPhase.BASELINE,
    ),
    SexualFunctionPhase.RETRACTOR_RELAXATION: (
        SexualFunctionPhase.SIGMOID_STRAIGHTENING,
        SexualFunctionPhase.BASELINE,
    ),
    SexualFunctionPhase.SIGMOID_STRAIGHTENING: (
        SexualFunctionPhase.PENILE_EXPOSURE,
        SexualFunctionPhase.RETRACTION_RECOVERY,
    ),
    SexualFunctionPhase.PENILE_EXPOSURE: (
        SexualFunctionPhase.EMISSION,
        SexualFunctionPhase.RETRACTION_RECOVERY,
    ),
    SexualFunctionPhase.EMISSION: (SexualFunctionPhase.URETHRAL_EXPULSION,),
    SexualFunctionPhase.URETHRAL_EXPULSION: (
        SexualFunctionPhase.RETRACTION_RECOVERY,
    ),
    SexualFunctionPhase.RETRACTION_RECOVERY: (SexualFunctionPhase.BASELINE,),
}

def advance_sexual_function_phase(
    current: SexualFunctionPhase,
    target: SexualFunctionPhase,
) -> SexualFunctionPhase:
    if target not in _ALLOWED[current]:
        raise PhysiologyTransitionError(f"invalid water-buffalo physiology transition: {current} -> {target}")
    return target

@dataclass(frozen=True, slots=True)
class SexualFunctionCoupling:
    nervous: str = "AUTONOMIC_AND_SOMATIC_REFERENCE_CHANNELS"
    cardiovascular: str = "PENILE_VASCULAR_FILLING_AND_PRESSURE_SUPPORT"
    muscular: str = "ISCHIOCAVERNOSUS_BULBOSPONGIOSUS_RETRACTOR_PENIS"
    endocrine: str = "MALE_REPRODUCTIVE_ENDOCRINE_REFERENCE"
    reproductive: str = "SPERM_TRANSPORT_ACCESSORY_GLAND_EMISSION_EJACULATION"
    urinary: str = "SHARED_URETHRAL_TOPOLOGY_WITH_STATE_SEPARATION"
    felt_desire: str = "NOT_ESTABLISHED"
    pleasure: str = "NOT_ESTABLISHED"
    body_sensation: str = "NOT_ESTABLISHED"
