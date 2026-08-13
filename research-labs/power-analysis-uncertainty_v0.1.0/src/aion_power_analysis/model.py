"""Transparent, assumption-dependent power planning contract."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from math import ceil, isfinite
from statistics import NormalDist
from typing import Any


class PlanningStatus(StrEnum):
    ADEQUATE = "ADEQUATE"
    UNDERPOWERED = "UNDERPOWERED"
    UNKNOWN = "UNKNOWN"
    INVALID = "INVALID"


class Disposition(StrEnum):
    PLANNING_REVIEW = "PLANNING_REVIEW"
    INDETERMINATE = "INDETERMINATE"
    HOLD = "HOLD"


@dataclass(frozen=True, slots=True)
class PowerPlan:
    plan_id: str
    standardized_effect_bound: float | None
    standard_deviation: float | None
    alpha: float | None
    target_power: float | None
    planned_sample_size: int | None
    two_sided: bool = True
    preregistration_ref: str | None = None
    assumption_basis: str | None = None


@dataclass(frozen=True, slots=True)
class PowerDecision:
    planning_status: PlanningStatus
    disposition: Disposition
    required_sample_size: int | None
    planned_sample_size: int | None
    effect_bound: float | None
    sensitivity_required_sample_sizes: tuple[tuple[float, int], ...]
    reason: str
    achieved_power: None = None
    scientific_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    deployment: bool = False
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    identity_continuity_conclusion: str = "NOT_ESTABLISHED"

    def as_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        for key in ("planning_status", "disposition"):
            payload[key] = getattr(self, key).value
        return payload


def _valid_probability(value: float | None) -> bool:
    return value is not None and isfinite(value) and 0.0 < value < 1.0


def required_sample_size(
    effect_bound: float,
    standard_deviation: float,
    alpha: float,
    target_power: float,
    two_sided: bool = True,
) -> int:
    """Normal-approximation planning size for a one-sample mean.

    This is a planning approximation conditional on the supplied model inputs;
    it is not an achieved-power estimator or a scientific conclusion.
    """

    if not all(isfinite(value) for value in (effect_bound, standard_deviation, alpha, target_power)):
        raise ValueError("planning inputs must be finite")
    if effect_bound <= 0 or standard_deviation <= 0:
        raise ValueError("effect_bound and standard_deviation must be positive")
    if not _valid_probability(alpha) or not _valid_probability(target_power):
        raise ValueError("alpha and target_power must be between zero and one")
    if two_sided:
        critical = NormalDist().inv_cdf(1.0 - alpha / 2.0)
    else:
        critical = NormalDist().inv_cdf(1.0 - alpha)
    power_quantile = NormalDist().inv_cdf(target_power)
    return ceil(((critical + power_quantile) * standard_deviation / effect_bound) ** 2)


def evaluate_plan(plan: PowerPlan) -> PowerDecision:
    """Evaluate planning metadata without claiming achieved power or effect."""

    fields = (
        plan.standardized_effect_bound,
        plan.standard_deviation,
        plan.alpha,
        plan.target_power,
        plan.planned_sample_size,
    )
    if any(value is None for value in fields):
        return PowerDecision(
            PlanningStatus.UNKNOWN,
            Disposition.HOLD,
            None,
            plan.planned_sample_size,
            plan.standardized_effect_bound,
            (),
            "MISSING_POWER_PLANNING_INPUT",
        )
    assert plan.standardized_effect_bound is not None
    assert plan.standard_deviation is not None
    assert plan.alpha is not None
    assert plan.target_power is not None
    assert plan.planned_sample_size is not None
    if plan.planned_sample_size < 1 or plan.standardized_effect_bound <= 0 or plan.standard_deviation <= 0:
        return PowerDecision(
            PlanningStatus.INVALID,
            Disposition.HOLD,
            None,
            plan.planned_sample_size,
            plan.standardized_effect_bound,
            (),
            "NON_POSITIVE_SAMPLE_OR_EFFECT_INPUT",
        )
    if not _valid_probability(plan.alpha) or not _valid_probability(plan.target_power):
        return PowerDecision(
            PlanningStatus.INVALID,
            Disposition.HOLD,
            None,
            plan.planned_sample_size,
            plan.standardized_effect_bound,
            (),
            "ALPHA_OR_TARGET_POWER_OUT_OF_RANGE",
        )
    if plan.assumption_basis is None or not plan.assumption_basis.strip():
        return PowerDecision(
            PlanningStatus.UNKNOWN,
            Disposition.HOLD,
            None,
            plan.planned_sample_size,
            plan.standardized_effect_bound,
            (),
            "MISSING_EFFECT_SIZE_ASSUMPTION_BASIS",
        )

    required = required_sample_size(
        plan.standardized_effect_bound,
        plan.standard_deviation,
        plan.alpha,
        plan.target_power,
        plan.two_sided,
    )
    sensitivity_bounds = tuple(
        sorted(
            {
                plan.standardized_effect_bound * 0.5,
                plan.standardized_effect_bound,
                plan.standardized_effect_bound * 1.5,
            }
        )
    )
    sensitivity = tuple(
        (
            round(effect, 8),
            required_sample_size(
                effect,
                plan.standard_deviation,
                plan.alpha,
                plan.target_power,
                plan.two_sided,
            ),
        )
        for effect in sensitivity_bounds
    )
    if plan.preregistration_ref is None:
        return PowerDecision(
            PlanningStatus.UNKNOWN,
            Disposition.INDETERMINATE,
            required,
            plan.planned_sample_size,
            plan.standardized_effect_bound,
            sensitivity,
            "POWER_PLAN_NOT_PREREGISTERED",
        )
    if plan.planned_sample_size < required:
        return PowerDecision(
            PlanningStatus.UNDERPOWERED,
            Disposition.INDETERMINATE,
            required,
            plan.planned_sample_size,
            plan.standardized_effect_bound,
            sensitivity,
            "PLANNED_SAMPLE_BELOW_ASSUMPTION_DEPENDENT_REQUIREMENT",
        )
    return PowerDecision(
        PlanningStatus.ADEQUATE,
        Disposition.PLANNING_REVIEW,
        required,
        plan.planned_sample_size,
        plan.standardized_effect_bound,
        sensitivity,
        "ASSUMPTION_DEPENDENT_PLAN_MEETS_DECLARED_TARGET",
    )
