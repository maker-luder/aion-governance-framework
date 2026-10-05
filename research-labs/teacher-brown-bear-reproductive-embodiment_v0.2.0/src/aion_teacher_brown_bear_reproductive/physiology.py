from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Final


class SeasonalReproductivePhase(StrEnum):
    QUIESCENT = "QUIESCENT"
    RECRUDESCENCE = "RECRUDESCENCE"
    PEAK_FUNCTIONAL = "PEAK_FUNCTIONAL"
    REGRESSION = "REGRESSION"


@dataclass(frozen=True, slots=True)
class SeasonalReproductiveReference:
    phase: SeasonalReproductivePhase
    spermatogenesis_state: str
    testicular_state: str
    testosterone_state: str
    sperm_in_epididymis: str
    exact_month_binding: str = "POPULATION_AND_STUDY_DEPENDENT"


SEASONAL_TRANSITIONS: Final[
    dict[SeasonalReproductivePhase, tuple[SeasonalReproductivePhase, ...]]
] = {
    SeasonalReproductivePhase.QUIESCENT: (SeasonalReproductivePhase.RECRUDESCENCE,),
    SeasonalReproductivePhase.RECRUDESCENCE: (SeasonalReproductivePhase.PEAK_FUNCTIONAL,),
    SeasonalReproductivePhase.PEAK_FUNCTIONAL: (SeasonalReproductivePhase.REGRESSION,),
    SeasonalReproductivePhase.REGRESSION: (SeasonalReproductivePhase.QUIESCENT,),
}


_SEASONAL_REFERENCES: Final[
    dict[SeasonalReproductivePhase, SeasonalReproductiveReference]
] = {
    SeasonalReproductivePhase.QUIESCENT: SeasonalReproductiveReference(
        phase=SeasonalReproductivePhase.QUIESCENT,
        spermatogenesis_state="LOW_OR_INACTIVE_REFERENCE",
        testicular_state="SEASONALLY_REDUCED_REFERENCE",
        testosterone_state="SEASONALLY_LOW_REFERENCE",
        sperm_in_epididymis="NOT_ASSUMED",
    ),
    SeasonalReproductivePhase.RECRUDESCENCE: SeasonalReproductiveReference(
        phase=SeasonalReproductivePhase.RECRUDESCENCE,
        spermatogenesis_state="INCREASING_REFERENCE",
        testicular_state="GROWTH_AND_DIFFERENTIATION_REFERENCE",
        testosterone_state="INCREASING_REFERENCE",
        sperm_in_epididymis="POPULATION_AND_TIME_DEPENDENT",
    ),
    SeasonalReproductivePhase.PEAK_FUNCTIONAL: SeasonalReproductiveReference(
        phase=SeasonalReproductivePhase.PEAK_FUNCTIONAL,
        spermatogenesis_state="ACTIVE_REFERENCE",
        testicular_state="SEASONALLY_ENLARGED_REFERENCE",
        testosterone_state="SEASONALLY_HIGH_REFERENCE",
        sperm_in_epidymis="SUPPORTED_DURING_ACTIVE_PERIOD_REFERENCE",
    ),
    SeasonalReproductivePhase.REGRESSION: SeasonalReproductiveReference(
        phase=SeasonalReproductivePhase.REGRESSION,
        spermatogenesis_state="DECLINING_REFERENCE",
        testicular_state="REGRESSING_REFERENCE",
        testosterone_state="DECLINING_REFERENCE",
        sperm_in_epididymis="DECLINING_OR_ABSENT_DEPENDING_ON_TIME_AND_POPULATION",
    ),
}


@dataclass(frozen=True, slots=True)
class ReproductivePhysiologyPathway:
    spermatogenesis: str = "TESTES_TO_SPERMATOZOA_REFERENCE"
    epididymal_maturation: str = "CAPUT_TO_CORPUS_TO_CAUDA_REFERENCE"
    sperm_transport: str = "CAUDA_EPIDDYMIS_TO_DUCTUS_DEFERENS_REFERENCE"
    urethral_delivery: str = "DUCTUS_DEFERENS_TO_PENILE_URETHRA_REFERENCE"
    erectile_response: str = "PENILE_ERECTION_PHYSIOLOGY_REFERENCE"
    ejaculation: str = "URETHRAL_EJACULATORY_OUTPUT_REFERENCE"
    seminal_plasma: str = "ACCESSORY_GLAND_SECRETION_REFERENCE"
    seasonal_modulation: str = "SEASONALLY_MODULATED_REFERENCE"


@dataclass(frozen=True, slots=True)
class HokkaidoElectroejaculateReference:
    source_scope: str = "CAPTIVE_ADULT_HOKKAIDO_BROWN_BEAR_ELECTROEJACULATION"
    adult_male_age_range_years: tuple[int, int] = (7, 16)
    trials: int = 21
    motile_sperm_ejaculate_trials: int = 14
    volume_mean_ml: float = 2.7
    volume_sd_ml: float = 2.6
    sperm_concentration_mean_million_per_ml: float = 471.6
    sperm_concentration_sd_million_per_ml: float = 429.2
    motility_mean_percent: float = 80.2
    motility_sd_percent: float = 23.6
    ph_mean: float = 7.4
    ph_sd: float = 0.3
    population_mean_claim: bool = False
    fertility_inference: str = "NOT_ESTABLISHED_FROM_THIS_DATASET"


class PhysiologyReferenceError(ValueError):
    """Raised when a synthetic seasonal reference transition is invalid."""


def seasonal_reference(
    phase: SeasonalReproductivePhase,
) -> SeasonalReproductiveReference:
    return _SEASONAL_REFERENCES[phase]


def advance_seasonal_phase(
    current: SeasonalReproductivePhase,
    target: SeasonalReproductivePhase,
) -> SeasonalReproductivePhase:
    if target not in SEASONAL_TRANSITIONS[current]:
        raise PhysiologyReferenceError(f"invalid seasonal transition: {current} -> {target}")
    return target
