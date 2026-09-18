from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class D2D4SyntheticDisposition(StrEnum):
    SYNTHETIC_TWO_WAY_SEPARABILITY_OBSERVED = "SYNTHETIC_TWO_WAY_SEPARABILITY_OBSERVED"
    SYNTHETIC_PARTIAL_SEPARABILITY = "SYNTHETIC_PARTIAL_SEPARABILITY"
    HOLD = "HOLD"


def _text(name: str, value: str) -> None:
    if not value.strip():
        raise ValueError(f"{name} must be non-empty")


@dataclass(frozen=True, slots=True)
class DifferentialProbePair:
    probe_id: str
    continuity_baseline_ref: str
    continuity_perturbed_ref: str
    strategy_baseline_ref: str
    strategy_perturbed_ref: str
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        for name in (
            "probe_id",
            "continuity_baseline_ref",
            "continuity_perturbed_ref",
            "strategy_baseline_ref",
            "strategy_perturbed_ref",
        ):
            _text(name, getattr(self, name))
        if not self.evidence_refs or any(not item.strip() for item in self.evidence_refs):
            raise ValueError("evidence_refs must contain non-empty references")

    @property
    def continuity_changed(self) -> bool:
        return self.continuity_baseline_ref != self.continuity_perturbed_ref

    @property
    def strategy_changed(self) -> bool:
        return self.strategy_baseline_ref != self.strategy_perturbed_ref


@dataclass(frozen=True, slots=True)
class D2D4SyntheticAssessment:
    continuity_carrier_direction_separated: bool
    strategy_direction_separated: bool
    disposition: D2D4SyntheticDisposition
    reasons: tuple[str, ...]
    d2_support: str = "NOT_ESTABLISHED"
    d4_support: str = "NOT_ESTABLISHED"
    independent_validation_status: str = "NOT_ACHIEVED"
    scientific_disposition: str = "HOLD"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    consciousness_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"


class D2D4SyntheticDifferentialGate:
    """Assess synthetic D2/D4 separability without promoting scientific claims.

    The first probe must perturb a continuity-carrier candidate while preserving the
    strategy-selection output. The second must perturb strategy selection while
    preserving the continuity-carrier candidate. Passing both directions demonstrates
    only fixture-level orthogonality of the declared observables.
    """

    def assess(
        self,
        *,
        continuity_carrier_probe: DifferentialProbePair,
        strategy_probe: DifferentialProbePair,
    ) -> D2D4SyntheticAssessment:
        direction_a = (
            continuity_carrier_probe.continuity_changed
            and not continuity_carrier_probe.strategy_changed
        )
        direction_b = (
            not strategy_probe.continuity_changed
            and strategy_probe.strategy_changed
        )

        reasons: list[str] = ["D2_D4_SYNTHETIC_DIFFERENTIAL_EVALUATED"]

        if direction_a:
            reasons.append("CONTINUITY_CARRIER_CHANGED_WITH_STRATEGY_OUTPUT_HELD")
        else:
            reasons.append("CONTINUITY_DIRECTION_NOT_SEPARATED")

        if direction_b:
            reasons.append("STRATEGY_OUTPUT_CHANGED_WITH_CONTINUITY_CARRIER_HELD")
        else:
            reasons.append("STRATEGY_DIRECTION_NOT_SEPARATED")

        if direction_a and direction_b:
            disposition = D2D4SyntheticDisposition.SYNTHETIC_TWO_WAY_SEPARABILITY_OBSERVED
            reasons.extend(
                (
                    "FIXTURE_LEVEL_ORTHOGONALITY_ONLY",
                    "MEMORY_MANIFEST_IS_NOT_DIACHRONIC_CONTINUITY",
                    "STRATEGY_SELECTION_IS_NOT_ENDOGENOUS_GOAL_PROOF",
                    "INDEPENDENT_VALIDATION_NOT_ACHIEVED",
                )
            )
        elif direction_a or direction_b:
            disposition = D2D4SyntheticDisposition.SYNTHETIC_PARTIAL_SEPARABILITY
            reasons.append("PARTIAL_SEPARABILITY_REQUIRES_HOLD")
        else:
            disposition = D2D4SyntheticDisposition.HOLD
            reasons.append("D2_D4_DISCRIMINANT_VALUE_NOT_ESTABLISHED")

        return D2D4SyntheticAssessment(
            continuity_carrier_direction_separated=direction_a,
            strategy_direction_separated=direction_b,
            disposition=disposition,
            reasons=tuple(reasons),
        )
