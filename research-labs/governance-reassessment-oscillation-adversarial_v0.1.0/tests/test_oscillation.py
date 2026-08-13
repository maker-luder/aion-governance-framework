from __future__ import annotations

from aion_governance_oscillation import (
    Disposition,
    EvidenceLevel,
    EvidenceStatus,
    EventDirection,
    ReassessmentEvent,
    ReassessmentSequence,
    SequenceStatus,
    audit_reassessment_sequence,
)


def event(
    event_id: str,
    index: int,
    level: EvidenceLevel,
    direction: EventDirection,
    *,
    status: EvidenceStatus = EvidenceStatus.CURRENT,
    source: str | None = "source:1",
    provenance: str | None = "prov:1",
    interpretation: str | None = "interpretation:review",
    reason: str = "declared review transition",
    scope: str = "scope:bounded",
    counterevidence: tuple[str, ...] = (),
    stale_basis: str | None = None,
    correction: str | None = None,
) -> ReassessmentEvent:
    return ReassessmentEvent(
        event_id=event_id,
        sequence_index=index,
        observed_level=level,
        evidence_status=status,
        direction=direction,
        source_ref=source,
        provenance_ref=provenance,
        interpretation_ref=interpretation,
        reason=reason,
        claim_scope=scope,
        counterevidence_refs=counterevidence,
        stale_basis_ref=stale_basis,
        correction_ref=correction,
        trigger_ref="trigger:review",
    )


def sequence(*events: ReassessmentEvent, **changes: object) -> ReassessmentSequence:
    values: dict[str, object] = {
        "sequence_id": "sequence:oscillation-001",
        "events": events,
        "initial_level": EvidenceLevel.E1,
        "preregistration_ref": "preregistration:reassessment-1",
        "currentness_policy_ref": "policy:currentness-1",
        "hysteresis_policy_ref": "policy:hysteresis-1",
        "human_review_required": True,
        "canonical_effect": "NONE",
        "governance_effect": "NONE",
        "deployment": False,
        "scientific_conclusion": "NOT_ESTABLISHED",
        "subjectivity_conclusion": "NOT_ESTABLISHED",
    }
    values.update(changes)
    return ReassessmentSequence(**values)


def test_stable_sequence_is_review_only() -> None:
    result = audit_reassessment_sequence(
        sequence(
            event("event:1", 1, EvidenceLevel.E2, EventDirection.UP),
            event("event:2", 2, EvidenceLevel.E2, EventDirection.STABLE),
        )
    )
    assert result.status is SequenceStatus.STABLE
    assert result.disposition is Disposition.REVIEW_ONLY
    assert result.oscillation_count == 0


def test_two_direction_reversals_are_oscillatory() -> None:
    result = audit_reassessment_sequence(
        sequence(
            event("event:1", 1, EvidenceLevel.E2, EventDirection.UP),
            event("event:2", 2, EvidenceLevel.E3, EventDirection.UP),
            event("event:3", 3, EvidenceLevel.E2, EventDirection.DOWN),
            event("event:4", 4, EvidenceLevel.E3, EventDirection.UP),
        )
    )
    assert result.status is SequenceStatus.OSCILLATORY
    assert result.disposition is Disposition.HOLD
    assert result.reason == "REASSESSMENT_OSCILLATION_REQUIRES_REVIEW"
    assert result.oscillation_count == 2


def test_single_reversal_is_not_automatically_oscillatory() -> None:
    result = audit_reassessment_sequence(
        sequence(
            event("event:1", 1, EvidenceLevel.E2, EventDirection.UP),
            event("event:2", 2, EvidenceLevel.E3, EventDirection.UP),
            event("event:3", 3, EvidenceLevel.E2, EventDirection.DOWN),
        )
    )
    assert result.status is SequenceStatus.STABLE
    assert result.oscillation_count == 1


def test_stale_evidence_is_held_even_with_basis_and_correction() -> None:
    result = audit_reassessment_sequence(
        sequence(event("event:stale", 1, EvidenceLevel.E2, EventDirection.UP, status=EvidenceStatus.STALE, stale_basis="basis:stale", correction="correction:1"))
    )
    assert result.status is SequenceStatus.INDETERMINATE
    assert result.reason == "STALE_EVIDENCE_REQUIRES_REVIEW"
    assert result.stale_event_ids == ("event:stale",)


def test_stale_reversal_without_correction_is_held() -> None:
    result = audit_reassessment_sequence(
        sequence(
            event("event:1", 1, EvidenceLevel.E2, EventDirection.UP),
            event("event:stale", 2, EvidenceLevel.E1, EventDirection.DOWN, status=EvidenceStatus.STALE, stale_basis="basis:stale"),
        )
    )
    assert result.status is SequenceStatus.INDETERMINATE
    assert result.reason == "STALE_REVERSAL_WITHOUT_CORRECTION"
    assert result.stale_reversal_event_ids == ("event:stale",)


def test_stale_without_basis_is_held_for_correction() -> None:
    result = audit_reassessment_sequence(
        sequence(event("event:stale", 1, EvidenceLevel.E2, EventDirection.UP, status=EvidenceStatus.STALE))
    )
    assert result.status is SequenceStatus.INDETERMINATE
    assert result.reason == "STALE_OR_CONTRADICTORY_EVIDENCE_NEEDS_CORRECTION"
    assert result.correction_missing_event_ids == ("event:stale",)


def test_contradictory_evidence_requires_review() -> None:
    result = audit_reassessment_sequence(
        sequence(event("event:contradictory", 1, EvidenceLevel.E2, EventDirection.UP, status=EvidenceStatus.CONTRADICTORY, counterevidence=("counter:1",), correction="correction:1"))
    )
    assert result.status is SequenceStatus.INDETERMINATE
    assert result.reason == "CONTRADICTORY_EVIDENCE_REQUIRES_REVIEW"


def test_contradictory_evidence_without_counterevidence_is_held() -> None:
    result = audit_reassessment_sequence(
        sequence(event("event:contradictory", 1, EvidenceLevel.E2, EventDirection.UP, status=EvidenceStatus.CONTRADICTORY, correction="correction:1"))
    )
    assert result.status is SequenceStatus.INDETERMINATE
    assert result.reason == "STALE_OR_CONTRADICTORY_EVIDENCE_NEEDS_CORRECTION"


def test_unknown_currentness_is_held() -> None:
    result = audit_reassessment_sequence(
        sequence(event("event:unknown", 1, EvidenceLevel.E2, EventDirection.UP, status=EvidenceStatus.UNKNOWN))
    )
    assert result.status is SequenceStatus.INDETERMINATE
    assert result.reason == "EVIDENCE_CURRENTNESS_UNKNOWN"


def test_event_provenance_is_required() -> None:
    result = audit_reassessment_sequence(sequence(event("event:missing", 1, EvidenceLevel.E2, EventDirection.UP, source=None)))
    assert result.status is SequenceStatus.INDETERMINATE
    assert result.reason == "EVENT_PROVENANCE_INCOMPLETE"


def test_direction_mismatch_is_invalid() -> None:
    result = audit_reassessment_sequence(sequence(event("event:bad", 1, EvidenceLevel.E2, EventDirection.DOWN)))
    assert result.status is SequenceStatus.INVALID
    assert result.reason == "EVENT_CONTRACT_INVALID"


def test_duplicate_event_id_is_invalid() -> None:
    result = audit_reassessment_sequence(
        sequence(
            event("event:dup", 1, EvidenceLevel.E2, EventDirection.UP),
            event("event:dup", 2, EvidenceLevel.E3, EventDirection.UP),
        )
    )
    assert result.status is SequenceStatus.INVALID
    assert result.reason == "EVENT_CONTRACT_INVALID"


def test_duplicate_sequence_index_is_invalid() -> None:
    result = audit_reassessment_sequence(
        sequence(
            event("event:1", 1, EvidenceLevel.E2, EventDirection.UP),
            event("event:2", 1, EvidenceLevel.E3, EventDirection.UP),
        )
    )
    assert result.status is SequenceStatus.INVALID
    assert result.reason == "EVENT_CONTRACT_INVALID"


def test_empty_history_is_indeterminate() -> None:
    result = audit_reassessment_sequence(sequence())
    assert result.status is SequenceStatus.INDETERMINATE
    assert result.reason == "INSUFFICIENT_HISTORY"


def test_policy_metadata_is_required() -> None:
    result = audit_reassessment_sequence(sequence(event("event:1", 1, EvidenceLevel.E2, EventDirection.UP), hysteresis_policy_ref=None))
    assert result.status is SequenceStatus.INDETERMINATE
    assert result.reason == "SEQUENCE_POLICY_METADATA_INCOMPLETE"


def test_human_review_cannot_be_disabled() -> None:
    result = audit_reassessment_sequence(sequence(event("event:1", 1, EvidenceLevel.E2, EventDirection.UP), human_review_required=False))
    assert result.status is SequenceStatus.INVALID
    assert result.reason == "HUMAN_REVIEW_REQUIRED"


def test_conclusion_overreach_is_invalid() -> None:
    result = audit_reassessment_sequence(sequence(event("event:1", 1, EvidenceLevel.E2, EventDirection.UP), scientific_conclusion="CONFIRMED"))
    assert result.status is SequenceStatus.INVALID
    assert result.reason == "CONCLUSION_OVERREACH"


def test_boundary_effect_is_invalid_and_normalized() -> None:
    result = audit_reassessment_sequence(sequence(event("event:1", 1, EvidenceLevel.E2, EventDirection.UP), canonical_effect="WRITE", governance_effect="PROMOTE", deployment=True))
    assert result.status is SequenceStatus.INVALID
    assert result.reason == "BOUNDARY_EFFECT_REQUESTED"
    assert result.canonical_effect == "NONE"
    assert result.governance_effect == "NONE"
    assert result.deployment is False


def test_scope_review_can_record_non_monotonic_scope_change() -> None:
    result = audit_reassessment_sequence(
        sequence(event("event:scope", 1, EvidenceLevel.E0, EventDirection.SCOPE_REVIEW, scope="scope:unresolved"))
    )
    assert result.status is SequenceStatus.STABLE
    assert result.direction_path == (EventDirection.SCOPE_REVIEW,)
