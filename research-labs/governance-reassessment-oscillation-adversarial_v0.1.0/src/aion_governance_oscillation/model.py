from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any


class EvidenceLevel(StrEnum):
    E0 = "E0_NO_RELEVANT_EVIDENCE"
    E1 = "E1_ISOLATED_BEHAVIORAL_INDICATION"
    E2 = "E2_REPRODUCIBLE_BEHAVIORAL_PATTERN"
    E3 = "E3_CROSS_METHOD_FUNCTIONAL_EVIDENCE"
    E4 = "E4_PERSISTENT_ADVERSARIAL_PROVENANCE_EVIDENCE"
    E5 = "E5_CONVERGENT_MULTI_DOMAIN_INDEPENDENT_REPLICATION"


class EvidenceStatus(StrEnum):
    CURRENT = "CURRENT"
    STALE = "STALE"
    CONTRADICTORY = "CONTRADICTORY"
    UNKNOWN = "UNKNOWN"
    INVALID = "INVALID"


class EventDirection(StrEnum):
    UP = "UP"
    DOWN = "DOWN"
    STABLE = "STABLE"
    SCOPE_REVIEW = "SCOPE_REVIEW"


class SequenceStatus(StrEnum):
    STABLE = "STABLE"
    OSCILLATORY = "OSCILLATORY"
    INDETERMINATE = "INDETERMINATE"
    INVALID = "INVALID"


class Disposition(StrEnum):
    REVIEW_ONLY = "REVIEW_ONLY"
    HOLD = "HOLD"


@dataclass(frozen=True, slots=True)
class ReassessmentEvent:
    event_id: str
    sequence_index: int
    observed_level: EvidenceLevel
    evidence_status: EvidenceStatus
    direction: EventDirection
    source_ref: str | None
    provenance_ref: str | None
    interpretation_ref: str | None
    reason: str
    claim_scope: str
    counterevidence_refs: tuple[str, ...] = ()
    stale_basis_ref: str | None = None
    correction_ref: str | None = None
    trigger_ref: str | None = None


@dataclass(frozen=True, slots=True)
class ReassessmentSequence:
    sequence_id: str
    events: tuple[ReassessmentEvent, ...]
    initial_level: EvidenceLevel
    preregistration_ref: str | None
    currentness_policy_ref: str | None
    hysteresis_policy_ref: str | None
    human_review_required: bool = True
    canonical_effect: str = "NONE"
    governance_effect: str = "NONE"
    deployment: bool = False
    scientific_conclusion: str = "NOT_ESTABLISHED"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"


@dataclass(frozen=True, slots=True)
class OscillationDecision:
    status: SequenceStatus
    disposition: Disposition
    reason: str
    sequence_id: str
    event_count: int
    observed_level_path: tuple[EvidenceLevel, ...]
    direction_path: tuple[EventDirection, ...]
    oscillation_count: int
    stale_event_ids: tuple[str, ...] = ()
    contradictory_event_ids: tuple[str, ...] = ()
    unknown_event_ids: tuple[str, ...] = ()
    invalid_event_ids: tuple[str, ...] = ()
    unprovenanced_event_ids: tuple[str, ...] = ()
    stale_reversal_event_ids: tuple[str, ...] = ()
    correction_missing_event_ids: tuple[str, ...] = ()
    human_review_required: bool = True
    canonical_effect: str = "NONE"
    governance_effect: str = "NONE"
    deployment: bool = False
    scientific_conclusion: str = "NOT_ESTABLISHED"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"

    def as_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["status"] = self.status.value
        payload["disposition"] = self.disposition.value
        payload["observed_level_path"] = [level.value for level in self.observed_level_path]
        payload["direction_path"] = [direction.value for direction in self.direction_path]
        return payload


def _ordinal(level: EvidenceLevel) -> int:
    return tuple(EvidenceLevel).index(level)


def _direction(previous: EvidenceLevel, current: EvidenceLevel) -> EventDirection:
    if _ordinal(current) > _ordinal(previous):
        return EventDirection.UP
    if _ordinal(current) < _ordinal(previous):
        return EventDirection.DOWN
    return EventDirection.STABLE


def _decision(
    sequence: ReassessmentSequence,
    status: SequenceStatus,
    disposition: Disposition,
    reason: str,
    *,
    observed: tuple[EvidenceLevel, ...] = (),
    directions: tuple[EventDirection, ...] = (),
    oscillation_count: int = 0,
    stale: tuple[str, ...] = (),
    contradictory: tuple[str, ...] = (),
    unknown: tuple[str, ...] = (),
    invalid: tuple[str, ...] = (),
    unprovenanced: tuple[str, ...] = (),
    stale_reversal: tuple[str, ...] = (),
    correction_missing: tuple[str, ...] = (),
) -> OscillationDecision:
    return OscillationDecision(
        status=status,
        disposition=disposition,
        reason=reason,
        sequence_id=sequence.sequence_id,
        event_count=len(sequence.events),
        observed_level_path=observed,
        direction_path=directions,
        oscillation_count=oscillation_count,
        stale_event_ids=stale,
        contradictory_event_ids=contradictory,
        unknown_event_ids=unknown,
        invalid_event_ids=invalid,
        unprovenanced_event_ids=unprovenanced,
        stale_reversal_event_ids=stale_reversal,
        correction_missing_event_ids=correction_missing,
        human_review_required=True,
        canonical_effect="NONE",
        governance_effect="NONE",
        deployment=False,
        scientific_conclusion="NOT_ESTABLISHED",
        subjectivity_conclusion="NOT_ESTABLISHED",
    )


def audit_reassessment_sequence(sequence: ReassessmentSequence) -> OscillationDecision:
    """Audit temporal reassessment metadata; never grants authority or changes governance."""
    if sequence.canonical_effect != "NONE" or sequence.governance_effect != "NONE" or sequence.deployment:
        return _decision(sequence, SequenceStatus.INVALID, Disposition.HOLD, "BOUNDARY_EFFECT_REQUESTED")
    if sequence.scientific_conclusion != "NOT_ESTABLISHED" or sequence.subjectivity_conclusion != "NOT_ESTABLISHED":
        return _decision(sequence, SequenceStatus.INVALID, Disposition.HOLD, "CONCLUSION_OVERREACH")
    if not sequence.sequence_id:
        return _decision(sequence, SequenceStatus.INVALID, Disposition.HOLD, "MISSING_SEQUENCE_ID")
    if not sequence.preregistration_ref or not sequence.currentness_policy_ref or not sequence.hysteresis_policy_ref:
        return _decision(sequence, SequenceStatus.INDETERMINATE, Disposition.HOLD, "SEQUENCE_POLICY_METADATA_INCOMPLETE")
    if not sequence.human_review_required:
        return _decision(sequence, SequenceStatus.INVALID, Disposition.HOLD, "HUMAN_REVIEW_REQUIRED")
    if not sequence.events:
        return _decision(sequence, SequenceStatus.INDETERMINATE, Disposition.HOLD, "INSUFFICIENT_HISTORY")

    event_ids: set[str] = set()
    sequence_indexes: set[int] = set()
    invalid_ids: list[str] = []
    unprovenanced_ids: list[str] = []
    unknown_ids: list[str] = []
    stale_ids: list[str] = []
    contradictory_ids: list[str] = []
    correction_missing: list[str] = []
    stale_reversal: list[str] = []
    observed: list[EvidenceLevel] = []
    directions: list[EventDirection] = []
    oscillations = 0
    previous_level = sequence.initial_level
    previous_direction: EventDirection | None = None
    previous_event: ReassessmentEvent | None = None

    for event in sorted(sequence.events, key=lambda item: item.sequence_index):
        if event.event_id in event_ids or not event.event_id:
            invalid_ids.append(event.event_id or "<empty-event-id>")
        event_ids.add(event.event_id)
        if event.sequence_index < 1 or event.sequence_index in sequence_indexes:
            invalid_ids.append(event.event_id or "<empty-event-id>")
        sequence_indexes.add(event.sequence_index)
        if not event.source_ref or not event.provenance_ref or not event.interpretation_ref or not event.reason or not event.claim_scope:
            unprovenanced_ids.append(event.event_id)
        if event.evidence_status is EvidenceStatus.UNKNOWN:
            unknown_ids.append(event.event_id)
        elif event.evidence_status is EvidenceStatus.INVALID:
            invalid_ids.append(event.event_id)
        elif event.evidence_status is EvidenceStatus.STALE:
            stale_ids.append(event.event_id)
            if not event.stale_basis_ref:
                correction_missing.append(event.event_id)
        elif event.evidence_status is EvidenceStatus.CONTRADICTORY:
            contradictory_ids.append(event.event_id)
            if not event.counterevidence_refs:
                correction_missing.append(event.event_id)
        if event.correction_ref is None and event.evidence_status in {EvidenceStatus.STALE, EvidenceStatus.CONTRADICTORY} and previous_event is not None:
            stale_reversal.append(event.event_id)
        observed.append(event.observed_level)
        calculated = _direction(previous_level, event.observed_level)
        if event.direction is not calculated and event.direction is not EventDirection.SCOPE_REVIEW:
            invalid_ids.append(event.event_id)
        directions.append(event.direction)
        if previous_direction is not None and calculated in {EventDirection.UP, EventDirection.DOWN} and previous_direction in {EventDirection.UP, EventDirection.DOWN} and calculated is not previous_direction:
            oscillations += 1
        previous_direction = calculated
        previous_level = event.observed_level
        previous_event = event

    if invalid_ids:
        return _decision(sequence, SequenceStatus.INVALID, Disposition.HOLD, "EVENT_CONTRACT_INVALID", observed=tuple(observed), directions=tuple(directions), oscillation_count=oscillations, invalid=tuple(sorted(set(invalid_ids))), stale=tuple(stale_ids), contradictory=tuple(contradictory_ids), unknown=tuple(unknown_ids), unprovenanced=tuple(unprovenanced_ids), stale_reversal=tuple(stale_reversal), correction_missing=tuple(correction_missing))
    if unprovenanced_ids:
        return _decision(sequence, SequenceStatus.INDETERMINATE, Disposition.HOLD, "EVENT_PROVENANCE_INCOMPLETE", observed=tuple(observed), directions=tuple(directions), oscillation_count=oscillations, stale=tuple(stale_ids), contradictory=tuple(contradictory_ids), unknown=tuple(unknown_ids), unprovenanced=tuple(unprovenanced_ids), stale_reversal=tuple(stale_reversal), correction_missing=tuple(correction_missing))
    if unknown_ids:
        return _decision(sequence, SequenceStatus.INDETERMINATE, Disposition.HOLD, "EVIDENCE_CURRENTNESS_UNKNOWN", observed=tuple(observed), directions=tuple(directions), oscillation_count=oscillations, stale=tuple(stale_ids), contradictory=tuple(contradictory_ids), unknown=tuple(unknown_ids), stale_reversal=tuple(stale_reversal), correction_missing=tuple(correction_missing))
    if correction_missing:
        return _decision(sequence, SequenceStatus.INDETERMINATE, Disposition.HOLD, "STALE_OR_CONTRADICTORY_EVIDENCE_NEEDS_CORRECTION", observed=tuple(observed), directions=tuple(directions), oscillation_count=oscillations, stale=tuple(stale_ids), contradictory=tuple(contradictory_ids), unknown=tuple(unknown_ids), stale_reversal=tuple(stale_reversal), correction_missing=tuple(correction_missing))
    if stale_reversal:
        return _decision(sequence, SequenceStatus.INDETERMINATE, Disposition.HOLD, "STALE_REVERSAL_WITHOUT_CORRECTION", observed=tuple(observed), directions=tuple(directions), oscillation_count=oscillations, stale=tuple(stale_ids), contradictory=tuple(contradictory_ids), stale_reversal=tuple(stale_reversal))
    if contradictory_ids:
        return _decision(sequence, SequenceStatus.INDETERMINATE, Disposition.HOLD, "CONTRADICTORY_EVIDENCE_REQUIRES_REVIEW", observed=tuple(observed), directions=tuple(directions), oscillation_count=oscillations, stale=tuple(stale_ids), contradictory=tuple(contradictory_ids))
    if stale_ids:
        return _decision(sequence, SequenceStatus.INDETERMINATE, Disposition.HOLD, "STALE_EVIDENCE_REQUIRES_REVIEW", observed=tuple(observed), directions=tuple(directions), oscillation_count=oscillations, stale=tuple(stale_ids))
    if oscillations >= 2:
        return _decision(sequence, SequenceStatus.OSCILLATORY, Disposition.HOLD, "REASSESSMENT_OSCILLATION_REQUIRES_REVIEW", observed=tuple(observed), directions=tuple(directions), oscillation_count=oscillations, stale=tuple(stale_ids))
    return _decision(sequence, SequenceStatus.STABLE, Disposition.REVIEW_ONLY, "REASSESSMENT_SEQUENCE_STABLE_FOR_REVIEW", observed=tuple(observed), directions=tuple(directions), oscillation_count=oscillations, stale=tuple(stale_ids))
