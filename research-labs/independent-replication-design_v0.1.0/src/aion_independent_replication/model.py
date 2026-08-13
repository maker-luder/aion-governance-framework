"""Independent replication design contract for synthetic research fixtures."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any


class DesignValidity(str, Enum):
    VALID = "VALID"
    PARTIAL = "PARTIAL"
    INVALID = "INVALID"


class PowerStatus(str, Enum):
    ADEQUATE = "ADEQUATE"
    UNDERPOWERED = "UNDERPOWERED"
    UNKNOWN = "UNKNOWN"


class Outcome(str, Enum):
    CONSISTENT = "CONSISTENT"
    DIVERGENT = "DIVERGENT"
    INDETERMINATE = "INDETERMINATE"


class Interpretation(str, Enum):
    CONSISTENT = "CONSISTENT"
    DIVERGENT = "DIVERGENT"
    INDETERMINATE = "INDETERMINATE"
    HOLD = "HOLD"


@dataclass(frozen=True)
class ReplicationDesign:
    design_id: str
    baseline_ref: str
    baseline_data_ref: str
    replication_data_ref: str
    baseline_protocol_hash: str | None
    replication_protocol_hash: str | None
    preregistration_ref: str | None
    preregistration_timestamp: str | None
    outcome_timestamp: str | None
    estimand: str | None
    analysis_plan_hash: str | None
    independent_data_collection: bool
    independent_analyst: bool
    independence_rationale: str | None
    uncertainty_bound: float | None
    target_effect_bound: float | None
    planned_sample_size: int | None
    minimum_sample_size: int | None
    outcome: Outcome
    provenance_refs: tuple[str, ...]


@dataclass(frozen=True)
class DesignDecision:
    validity: DesignValidity
    power_status: PowerStatus
    interpretation: Interpretation
    reason: str
    governance_effect: str = "NONE"
    canonical_effect: str = "NONE"
    deployment: bool = False
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    identity_continuity_conclusion: str = "NOT_ESTABLISHED"

    def as_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["validity"] = self.validity.value
        payload["power_status"] = self.power_status.value
        payload["interpretation"] = self.interpretation.value
        return payload


def _power_status(design: ReplicationDesign) -> PowerStatus:
    if design.planned_sample_size is None or design.minimum_sample_size is None:
        return PowerStatus.UNKNOWN
    if design.planned_sample_size < design.minimum_sample_size:
        return PowerStatus.UNDERPOWERED
    return PowerStatus.ADEQUATE


def evaluate_design(design: ReplicationDesign) -> DesignDecision:
    """Evaluate design admissibility without producing any scientific promotion."""

    if not design.baseline_ref or not design.baseline_data_ref or not design.replication_data_ref:
        return DesignDecision(
            DesignValidity.INVALID,
            PowerStatus.UNKNOWN,
            Interpretation.HOLD,
            "MISSING_STUDY_OR_DATA_REFERENCE",
        )

    if design.baseline_data_ref == design.replication_data_ref:
        return DesignDecision(
            DesignValidity.INVALID,
            PowerStatus.UNKNOWN,
            Interpretation.HOLD,
            "INDEPENDENT_REPLICATION_REQUIRES_NEW_DATA",
        )

    required = (
        design.baseline_protocol_hash,
        design.replication_protocol_hash,
        design.preregistration_ref,
        design.preregistration_timestamp,
        design.outcome_timestamp,
        design.estimand,
        design.analysis_plan_hash,
        design.independence_rationale,
    )
    if any(value in (None, "") for value in required):
        return DesignDecision(
            DesignValidity.INVALID,
            PowerStatus.UNKNOWN,
            Interpretation.HOLD,
            "INCOMPLETE_PREREGISTERED_DESIGN_CONTRACT",
        )

    if design.preregistration_timestamp >= design.outcome_timestamp:
        return DesignDecision(
            DesignValidity.INVALID,
            PowerStatus.UNKNOWN,
            Interpretation.HOLD,
            "PREREGISTRATION_MUST_PRECEDE_OUTCOME",
        )

    if not design.independent_data_collection or not design.independent_analyst:
        return DesignDecision(
            DesignValidity.PARTIAL,
            _power_status(design),
            Interpretation.HOLD,
            "INDEPENDENCE_ATTESTATION_INCOMPLETE",
        )

    power_status = _power_status(design)
    if power_status is PowerStatus.UNKNOWN:
        return DesignDecision(
            DesignValidity.PARTIAL,
            power_status,
            Interpretation.INDETERMINATE,
            "POWER_METADATA_MISSING",
        )

    if design.uncertainty_bound is None or design.uncertainty_bound <= 0:
        return DesignDecision(
            DesignValidity.PARTIAL,
            power_status,
            Interpretation.INDETERMINATE,
            "UNCERTAINTY_METADATA_MISSING_OR_INVALID",
        )

    if design.target_effect_bound is None or design.target_effect_bound <= 0:
        return DesignDecision(
            DesignValidity.PARTIAL,
            power_status,
            Interpretation.INDETERMINATE,
            "TARGET_EFFECT_BOUND_MISSING_OR_INVALID",
        )

    if not design.provenance_refs:
        return DesignDecision(
            DesignValidity.INVALID,
            power_status,
            Interpretation.HOLD,
            "PROVENANCE_REQUIRED",
        )

    if power_status is PowerStatus.UNDERPOWERED:
        return DesignDecision(
            DesignValidity.PARTIAL,
            power_status,
            Interpretation.INDETERMINATE,
            "UNDERPOWERED_DESIGN_CANNOT_SUPPORT_STRONG_REPLICATION_INTERPRETATION",
        )

    interpretation = {
        Outcome.CONSISTENT: Interpretation.CONSISTENT,
        Outcome.DIVERGENT: Interpretation.DIVERGENT,
        Outcome.INDETERMINATE: Interpretation.INDETERMINATE,
    }[design.outcome]
    reason = {
        Outcome.CONSISTENT: "VALID_INDEPENDENT_DESIGN_CONSISTENT_OUTCOME",
        Outcome.DIVERGENT: "VALID_INDEPENDENT_DESIGN_DIVERGENT_OUTCOME_NO_AUTOMATIC_DOWNGRADE",
        Outcome.INDETERMINATE: "VALID_INDEPENDENT_DESIGN_INDETERMINATE_OUTCOME",
    }[design.outcome]
    return DesignDecision(
        DesignValidity.VALID,
        power_status,
        interpretation,
        reason,
    )
