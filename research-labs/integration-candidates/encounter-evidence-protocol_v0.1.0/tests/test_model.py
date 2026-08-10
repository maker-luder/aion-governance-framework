import pytest

from encounter_evidence_protocol import (
    BoundaryKind,
    EncounterBinding,
    EncounterBoundaryEvidence,
    EncounterEventEvidence,
    EncounterRecord,
    EncounterStatus,
)


def binding(entity: str = "agent-a", *, roles: tuple[str, ...] = ("SUBJECT",)) -> EncounterBinding:
    return EncounterBinding(
        binding_id=f"binding-{entity}",
        entity_ref=entity,
        entity_kind_ref="AGENT",
        role_refs=roles,
        evidence_refs=(f"evidence-{entity}",),
        provenance_refs=(f"prov-{entity}",),
    )


def boundary(kind: BoundaryKind, when: str, *, actor: str = "agent-a", encounter_id: str = "enc-1") -> EncounterBoundaryEvidence:
    return EncounterBoundaryEvidence(
        boundary_id=f"boundary-{kind.value}-{when}",
        encounter_id=encounter_id,
        kind=kind,
        timestamp=when,
        source_actor_ref=actor,
        method_ref="boundary-method-v1",
        evidence_refs=("boundary-evidence",),
        provenance_refs=("boundary-prov",),
    )


def event(when: str = "2026-08-10T10:05:00Z", *, encounter_id: str = "enc-1", actor: str = "agent-a", involved: tuple[str, ...] = ("agent-a",)) -> EncounterEventEvidence:
    return EncounterEventEvidence(
        event_id=f"event-{when}-{actor}",
        encounter_id=encounter_id,
        timestamp=when,
        event_kind_ref="OBSERVATION",
        source_actor_ref=actor,
        involved_entity_refs=involved,
        content_ref="artifact:event-content",
        evidence_refs=("event-evidence",),
        provenance_refs=("event-prov",),
    )


def record(*, boundaries=None, events=None, bindings=None, kinds=("COLLABORATIVE", "EXPLORATORY"), relationship_claim="NOT_ESTABLISHED") -> EncounterRecord:
    return EncounterRecord(
        encounter_id="enc-1",
        subject_ref="agent-a",
        context_ref="context-1",
        encounter_kind_refs=kinds,
        bindings=bindings or (binding(),),
        boundaries=boundaries or (boundary(BoundaryKind.START, "2026-08-10T10:00:00Z"),),
        events=events or (),
        evidence_refs=("record-evidence",),
        provenance_refs=("record-prov",),
        relationship_claim=relationship_claim,
    )


def test_open_encounter_can_have_only_subject_binding() -> None:
    item = record()
    assert item.status is EncounterStatus.OPEN
    assert item.ended_at is None


def test_closed_encounter() -> None:
    item = record(boundaries=(
        boundary(BoundaryKind.START, "2026-08-10T10:00:00Z"),
        boundary(BoundaryKind.END, "2026-08-10T11:00:00Z"),
    ))
    assert item.status is EncounterStatus.CLOSED
    assert item.ended_at == "2026-08-10T11:00:00Z"


def test_aborted_encounter() -> None:
    item = record(boundaries=(
        boundary(BoundaryKind.START, "2026-08-10T10:00:00Z"),
        boundary(BoundaryKind.ABORT, "2026-08-10T10:30:00Z"),
    ))
    assert item.status is EncounterStatus.ABORTED


def test_exactly_one_start_required() -> None:
    with pytest.raises(ValueError, match="exactly one START"):
        record(boundaries=(boundary(BoundaryKind.END, "2026-08-10T11:00:00Z"),))


def test_multiple_terminal_boundaries_rejected() -> None:
    with pytest.raises(ValueError, match="at most one terminal"):
        record(boundaries=(
            boundary(BoundaryKind.START, "2026-08-10T10:00:00Z"),
            boundary(BoundaryKind.END, "2026-08-10T11:00:00Z"),
            boundary(BoundaryKind.ABORT, "2026-08-10T11:30:00Z"),
        ))


def test_terminal_cannot_precede_start() -> None:
    with pytest.raises(ValueError, match="cannot precede"):
        record(boundaries=(
            boundary(BoundaryKind.START, "2026-08-10T10:00:00Z"),
            boundary(BoundaryKind.END, "2026-08-10T09:00:00Z"),
        ))


def test_event_before_start_rejected() -> None:
    with pytest.raises(ValueError, match="before START"):
        record(events=(event("2026-08-10T09:59:00Z"),))


def test_event_after_terminal_rejected() -> None:
    with pytest.raises(ValueError, match="after terminal"):
        record(
            boundaries=(
                boundary(BoundaryKind.START, "2026-08-10T10:00:00Z"),
                boundary(BoundaryKind.END, "2026-08-10T11:00:00Z"),
            ),
            events=(event("2026-08-10T11:01:00Z"),),
        )


def test_ghost_event_actor_rejected() -> None:
    with pytest.raises(ValueError, match="source_actor_ref"):
        record(events=(event(actor="ghost"),))


def test_ghost_involved_entity_rejected() -> None:
    with pytest.raises(ValueError, match="unbound entity"):
        record(events=(event(involved=("agent-a", "ghost")),))


def test_event_encounter_mismatch_rejected() -> None:
    with pytest.raises(ValueError, match="event encounter_id mismatch"):
        record(events=(event(encounter_id="other"),))


def test_duplicate_binding_entity_rejected() -> None:
    duplicate = EncounterBinding(
        binding_id="binding-2",
        entity_ref="agent-a",
        entity_kind_ref="AGENT",
        role_refs=("OBSERVER",),
        evidence_refs=("e2",),
        provenance_refs=("p2",),
    )
    with pytest.raises(ValueError, match="entity_ref values must be unique"):
        record(bindings=(binding(), duplicate))


def test_multi_role_and_multi_kind_are_allowed() -> None:
    item = record(
        bindings=(binding(roles=("SUBJECT", "OBSERVER")),),
        kinds=("COLLABORATIVE", "EXPLORATORY"),
    )
    assert item.bindings[0].role_refs == ("SUBJECT", "OBSERVER")
    assert item.encounter_kind_refs == ("COLLABORATIVE", "EXPLORATORY")


def test_nonclaims_are_locked() -> None:
    with pytest.raises(ValueError, match="relationship_claim"):
        record(relationship_claim="ESTABLISHED")


def test_timestamp_must_be_timezone_aware() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        boundary(BoundaryKind.START, "2026-08-10T10:00:00")
