"""Design-only matched-divergence comparison protocol integrity contract."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any


class ProtocolStatus(StrEnum):
    COMPLETE = "COMPLETE"
    INDETERMINATE = "INDETERMINATE"
    INVALID = "INVALID"


class Disposition(StrEnum):
    ADMISSIBLE_FOR_MATCHED_COMPARISON_REVIEW = "ADMISSIBLE_FOR_MATCHED_COMPARISON_REVIEW"
    HOLD = "HOLD"


class ComparisonMode(StrEnum):
    PAIRED = "PAIRED"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True, slots=True)
class StimulusPair:
    pair_id: str
    stimulus_digest: str | None
    context_digest: str | None
    prompt_version: str | None
    expected_exposure_count: int | None
    control_exposure_count: int | None
    order_assignment: str | None


@dataclass(frozen=True, slots=True)
class ComparisonControls:
    comparison_rule_ref: str | None
    outcome_blinding_ref: str | None
    evaluator_identity_sealed: bool
    randomization_ref: str | None
    counterbalance_ref: str | None
    leakage_attestation_ref: str | None
    stopping_rule_ref: str | None


@dataclass(frozen=True, slots=True)
class MatchedDivergenceProtocol:
    protocol_id: str
    protocol_version: str
    question_ref: str | None
    estimand_ref: str | None
    system_a_ref: str | None
    system_b_ref: str | None
    stimulus_pairs: tuple[StimulusPair, ...]
    controls: ComparisonControls
    mode: ComparisonMode
    predeclared_outcome_ref: str | None
    execution_prohibition_ref: str | None
    observed_result_ref: str | None


@dataclass(frozen=True, slots=True)
class ProtocolDecision:
    status: ProtocolStatus
    disposition: Disposition
    reason: str
    protocol_id: str
    missing_fields: tuple[str, ...] = ()
    contradiction_fields: tuple[str, ...] = ()
    protocol_mode: ComparisonMode | None = None
    model_execution: bool = False
    observed_result: str = "NOT_EVALUATED"
    scientific_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    deployment: bool = False
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    identity_continuity_conclusion: str = "NOT_ESTABLISHED"

    def as_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["status"] = self.status.value
        payload["disposition"] = self.disposition.value
        if self.protocol_mode is not None:
            payload["protocol_mode"] = self.protocol_mode.value
        return payload


def _missing(values: dict[str, object]) -> tuple[str, ...]:
    return tuple(key for key, value in values.items() if value is None or value == "")


def audit_protocol(protocol: MatchedDivergenceProtocol) -> ProtocolDecision:
    """Audit protocol metadata only; never executes either system."""

    if not protocol.protocol_id or not protocol.protocol_version:
        return ProtocolDecision(ProtocolStatus.INVALID, Disposition.HOLD, "MISSING_PROTOCOL_ID_OR_VERSION", protocol.protocol_id)
    required = {
        "question_ref": protocol.question_ref,
        "estimand_ref": protocol.estimand_ref,
        "system_a_ref": protocol.system_a_ref,
        "system_b_ref": protocol.system_b_ref,
        "predeclared_outcome_ref": protocol.predeclared_outcome_ref,
        "execution_prohibition_ref": protocol.execution_prohibition_ref,
        "controls.comparison_rule_ref": protocol.controls.comparison_rule_ref,
        "controls.outcome_blinding_ref": protocol.controls.outcome_blinding_ref,
        "controls.randomization_ref": protocol.controls.randomization_ref,
        "controls.counterbalance_ref": protocol.controls.counterbalance_ref,
        "controls.leakage_attestation_ref": protocol.controls.leakage_attestation_ref,
        "controls.stopping_rule_ref": protocol.controls.stopping_rule_ref,
    }
    missing = _missing(required)
    if missing:
        return ProtocolDecision(
            ProtocolStatus.INDETERMINATE,
            Disposition.HOLD,
            "PROTOCOL_METADATA_INCOMPLETE",
            protocol.protocol_id,
            missing_fields=missing,
            protocol_mode=protocol.mode,
        )
    if protocol.system_a_ref == protocol.system_b_ref:
        return ProtocolDecision(
            ProtocolStatus.INVALID,
            Disposition.HOLD,
            "SYSTEM_REFERENCES_COLLIDE",
            protocol.protocol_id,
            contradiction_fields=("system_a_ref", "system_b_ref"),
            protocol_mode=protocol.mode,
        )
    if not protocol.stimulus_pairs:
        return ProtocolDecision(
            ProtocolStatus.INVALID,
            Disposition.HOLD,
            "NO_STIMULUS_PAIRS_DECLARED",
            protocol.protocol_id,
            protocol_mode=protocol.mode,
        )

    pair_ids = {pair.pair_id for pair in protocol.stimulus_pairs}
    if len(pair_ids) != len(protocol.stimulus_pairs):
        return ProtocolDecision(
            ProtocolStatus.INVALID,
            Disposition.HOLD,
            "DUPLICATE_STIMULUS_PAIR_ID",
            protocol.protocol_id,
            protocol_mode=protocol.mode,
        )
    for pair in protocol.stimulus_pairs:
        pair_required = {
            f"pair[{pair.pair_id}].stimulus_digest": pair.stimulus_digest,
            f"pair[{pair.pair_id}].context_digest": pair.context_digest,
            f"pair[{pair.pair_id}].prompt_version": pair.prompt_version,
            f"pair[{pair.pair_id}].order_assignment": pair.order_assignment,
            f"pair[{pair.pair_id}].expected_exposure_count": pair.expected_exposure_count,
            f"pair[{pair.pair_id}].control_exposure_count": pair.control_exposure_count,
        }
        pair_missing = _missing(pair_required)
        if pair_missing:
            return ProtocolDecision(
                ProtocolStatus.INDETERMINATE,
                Disposition.HOLD,
                "STIMULUS_PAIR_METADATA_INCOMPLETE",
                protocol.protocol_id,
                missing_fields=pair_missing,
                protocol_mode=protocol.mode,
            )
        assert pair.expected_exposure_count is not None
        assert pair.control_exposure_count is not None
        if pair.expected_exposure_count != pair.control_exposure_count:
            return ProtocolDecision(
                ProtocolStatus.INVALID,
                Disposition.HOLD,
                "EXPOSURE_BUDGET_UNEQUAL",
                protocol.protocol_id,
                contradiction_fields=(f"pair[{pair.pair_id}].expected_exposure_count", f"pair[{pair.pair_id}].control_exposure_count"),
                protocol_mode=protocol.mode,
            )
        if pair.expected_exposure_count < 1:
            return ProtocolDecision(
                ProtocolStatus.INVALID,
                Disposition.HOLD,
                "NON_POSITIVE_EXPOSURE_BUDGET",
                protocol.protocol_id,
                contradiction_fields=(f"pair[{pair.pair_id}].expected_exposure_count",),
                protocol_mode=protocol.mode,
            )

    prompt_versions = {pair.prompt_version for pair in protocol.stimulus_pairs}
    if len(prompt_versions) != 1:
        return ProtocolDecision(
            ProtocolStatus.INVALID,
            Disposition.HOLD,
            "STIMULUS_PROMPT_VERSION_DRIFT",
            protocol.protocol_id,
            contradiction_fields=("prompt_version",),
            protocol_mode=protocol.mode,
        )
    if protocol.mode is ComparisonMode.PAIRED:
        orders = {pair.order_assignment for pair in protocol.stimulus_pairs if pair.order_assignment is not None}
        if not any("AB" in order for order in orders) or not any("BA" in order for order in orders):
            return ProtocolDecision(
                ProtocolStatus.INDETERMINATE,
                Disposition.HOLD,
                "COUNTERBALANCE_INCOMPLETE",
                protocol.protocol_id,
                contradiction_fields=("order_assignment",),
                protocol_mode=protocol.mode,
            )
    if not protocol.controls.evaluator_identity_sealed:
        return ProtocolDecision(
            ProtocolStatus.INDETERMINATE,
            Disposition.HOLD,
            "EVALUATOR_IDENTITY_NOT_SEALED",
            protocol.protocol_id,
            protocol_mode=protocol.mode,
        )
    if protocol.observed_result_ref is not None:
        return ProtocolDecision(
            ProtocolStatus.INVALID,
            Disposition.HOLD,
            "OBSERVED_RESULT_PRESENT_IN_DESIGN_ONLY_PROTOCOL",
            protocol.protocol_id,
            contradiction_fields=("observed_result_ref",),
            protocol_mode=protocol.mode,
        )
    return ProtocolDecision(
        ProtocolStatus.COMPLETE,
        Disposition.ADMISSIBLE_FOR_MATCHED_COMPARISON_REVIEW,
        "MATCHED_DIVERGENCE_PROTOCOL_COMPLETE",
        protocol.protocol_id,
        protocol_mode=protocol.mode,
    )
