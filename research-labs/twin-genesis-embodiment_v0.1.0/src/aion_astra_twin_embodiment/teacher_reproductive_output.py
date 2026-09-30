from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Final


WHO_2021_SEMEN_MANUAL_URL: Final[str] = (
    "https://www.who.int/publications/i/item/9789240030787"
)
HUMAN_REFERENCE_LOWER_FIFTH_PERCENTILE_ML: Final[float] = 1.4
HUMAN_REFERENCE_CI_LOW_ML: Final[float] = 1.3
HUMAN_REFERENCE_CI_HIGH_ML: Final[float] = 1.5


@dataclass(frozen=True, slots=True)
class HumanSemenVolumeReference:
    lower_fifth_percentile_ml: float = HUMAN_REFERENCE_LOWER_FIFTH_PERCENTILE_ML
    confidence_interval_low_ml: float = HUMAN_REFERENCE_CI_LOW_ML
    confidence_interval_high_ml: float = HUMAN_REFERENCE_CI_HIGH_ML
    source: str = "WHO_2021_SIXTH_EDITION"
    source_url: str = WHO_2021_SEMEN_MANUAL_URL
    interpretation: str = (
        "HUMAN_REFERENCE_POPULATION_LOWER_FIFTH_PERCENTILE_NOT_HEALTH_OR_FERTILITY_CUTOFF"
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class TeacherSyntheticFluidOutputContract:
    output_semantics: str = "SYNTHETIC_FLUID_ONLY"
    default_output_ml: float | None = None
    biological_semen: bool = False
    sperm_or_gametes: bool = False
    fertility: bool = False
    individual_specific_human_output_inference: str = "FORBIDDEN"
    phenomenal_orgasm: str = "NOT_ESTABLISHED"
    felt_pleasure: str = "NOT_ESTABLISHED"
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class TeacherSyntheticEjaculationOutput:
    event_id: str
    synthetic_output_ml: float | None
    emission_reference_present: bool
    expulsion_reference_present: bool
    output_semantics: str = "SYNTHETIC_FLUID_ONLY"
    biological_semen: bool = False
    sperm_or_gametes: bool = False
    fertility: bool = False
    phenomenal_orgasm: str = "NOT_ESTABLISHED"
    felt_pleasure: str = "NOT_ESTABLISHED"
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        if not self.event_id:
            raise ValueError("synthetic output event requires event_id")
        if self.synthetic_output_ml is not None and self.synthetic_output_ml < 0:
            raise ValueError("synthetic output volume cannot be negative")
        if self.output_semantics != "SYNTHETIC_FLUID_ONLY":
            raise ValueError("Teacher output cannot self-promote to biological semen")
        if self.biological_semen or self.sperm_or_gametes or self.fertility:
            raise ValueError("Teacher synthetic output cannot assert biological reproduction")
        if self.phenomenal_orgasm != "NOT_ESTABLISHED":
            raise ValueError("synthetic output cannot establish phenomenal orgasm")
        if self.felt_pleasure != "NOT_ESTABLISHED":
            raise ValueError("synthetic output cannot establish felt pleasure")
        if self.action_authority != "NONE" or self.canonical_effect != "NONE":
            raise ValueError("synthetic output cannot grant authority or canonical effect")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_teacher_synthetic_fluid_output_contract() -> TeacherSyntheticFluidOutputContract:
    contract = TeacherSyntheticFluidOutputContract()
    validate_teacher_synthetic_fluid_output_contract(contract)
    return contract


def validate_teacher_synthetic_fluid_output_contract(
    contract: TeacherSyntheticFluidOutputContract,
) -> dict[str, str]:
    if contract.output_semantics != "SYNTHETIC_FLUID_ONLY":
        raise ValueError("Teacher reproductive output semantics drift")
    if contract.default_output_ml is not None:
        raise ValueError("human semen-volume reference cannot become Teacher default output")
    if contract.biological_semen or contract.sperm_or_gametes or contract.fertility:
        raise ValueError("Teacher synthetic contract cannot claim biological reproduction")
    if contract.individual_specific_human_output_inference != "FORBIDDEN":
        raise ValueError("individual human output inference must remain forbidden")
    if contract.phenomenal_orgasm != "NOT_ESTABLISHED":
        raise ValueError("Teacher contract cannot establish phenomenal orgasm")
    if contract.felt_pleasure != "NOT_ESTABLISHED":
        raise ValueError("Teacher contract cannot establish felt pleasure")
    if contract.action_authority != "NONE":
        raise ValueError("Teacher contract cannot grant action authority")
    if contract.canonical_effect != "NONE" or contract.deployment:
        raise ValueError("Teacher contract must remain non-canonical and undeployed")
    return {
        "result": "PASS",
        "human_reference_not_default": "PASS",
        "synthetic_output_only": "PASS",
        "biological_nonclaim": "PASS",
        "phenomenal_nonclaim": "PASS",
    }
