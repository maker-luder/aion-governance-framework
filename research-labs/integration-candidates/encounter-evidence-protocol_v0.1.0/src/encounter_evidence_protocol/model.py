from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Final

NONE: Final[str] = "NONE"
NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"


class BoundaryKind(str, Enum):
    START = "START"
    END = "END"
    ABORT = "ABORT"


class EncounterStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    ABORTED = "ABORTED"


def _require_nonempty(name: str, value: str) -> None:
    if not value.strip():
        raise ValueError(f"{name} must be non-empty")


def _require_refs(name: str, refs: tuple[str, ...]) -> None:
    if not refs:
        raise ValueError(f"{name} must be non-empty")
    for ref in refs:
        _require_nonempty(name, ref)
    if len(refs) != len(set(refs)):
        raise ValueError(f"{name} must not contain duplicates")


def _parse_timestamp(value: str) -> datetime:
    _require_nonempty("timestamp", value)
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError("timestamp must be ISO 8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("timestamp must be timezone-aware")
    return parsed


@dataclass(frozen=True, slots=True)
class EncounterBinding:
    binding_id: str
    entity_ref: str
    entity_kind_ref: str
    role_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    canonical_effect: str = NONE
    identity_claim: str = NOT_ESTABLISHED
    authority_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        for name in ("binding_id", "entity_ref", "entity_kind_ref"):
            _require_nonempty(name, getattr(self, name))
        _require_refs("role_refs", self.role_refs)
        _require_refs("evidence_refs", self.evidence_refs)
        _require_refs("provenance_refs", self.provenance_refs)
        if self.canonical_effect != NONE:
            raise ValueError("binding must keep canonical_effect=NONE")
        if self.identity_claim != NOT_ESTABLISHED:
            raise ValueError("binding identity claim must remain NOT_ESTABLISHED")
        if self.authority_claim != NOT_ESTABLISHED:
            raise ValueError("binding authority claim must remain NOT_ESTABLISHED")


@dataclass(frozen=True, slots=True)
class EncounterBoundaryEvidence:
    boundary_id: str
    encounter_id: str
    kind: BoundaryKind
    timestamp: str
    source_actor_ref: str
    method_ref: str
    evidence_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    canonical_effect: str = NONE

    def __post_init__(self) -> None:
        for name in ("boundary_id", "encounter_id", "source_actor_ref", "method_ref"):
            _require_nonempty(name, getattr(self, name))
        _parse_timestamp(self.timestamp)
        _require_refs("evidence_refs", self.evidence_refs)
        _require_refs("provenance_refs", self.provenance_refs)
        if self.canonical_effect != NONE:
            raise ValueError("boundary evidence must keep canonical_effect=NONE")


@dataclass(frozen=True, slots=True)
class EncounterEventEvidence:
    event_id: str
    encounter_id: str
    timestamp: str
    event_kind_ref: str
    source_actor_ref: str
    involved_entity_refs: tuple[str, ...]
    content_ref: str
    evidence_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    canonical_effect: str = NONE

    def __post_init__(self) -> None:
        for name in (
            "event_id",
            "encounter_id",
            "event_kind_ref",
            "source_actor_ref",
            "content_ref",
        ):
            _require_nonempty(name, getattr(self, name))
        _parse_timestamp(self.timestamp)
        _require_refs("involved_entity_refs", self.involved_entity_refs)
        _require_refs("evidence_refs", self.evidence_refs)
        _require_refs("provenance_refs", self.provenance_refs)
        if self.canonical_effect != NONE:
            raise ValueError("event evidence must keep canonical_effect=NONE")


@dataclass(frozen=True, slots=True)
class EncounterRecord:
    encounter_id: str
    subject_ref: str
    context_ref: str
    encounter_kind_refs: tuple[str, ...]
    bindings: tuple[EncounterBinding, ...]
    boundaries: tuple[EncounterBoundaryEvidence, ...]
    events: tuple[EncounterEventEvidence, ...]
    evidence_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    canonical_effect: str = NONE
    relationship_claim: str = NOT_ESTABLISHED
    intimacy_claim: str = NOT_ESTABLISHED
    shared_meaning_claim: str = NOT_ESTABLISHED
    mutual_understanding_claim: str = NOT_ESTABLISHED
    subjectivity_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        for name in ("encounter_id", "subject_ref", "context_ref"):
            _require_nonempty(name, getattr(self, name))
        for ref in self.encounter_kind_refs:
            _require_nonempty("encounter_kind_refs", ref)
        if len(self.encounter_kind_refs) != len(set(self.encounter_kind_refs)):
            raise ValueError("encounter_kind_refs must not contain duplicates")
        if not self.bindings:
            raise ValueError("encounter requires at least the subject binding")
        _require_refs("evidence_refs", self.evidence_refs)
        _require_refs("provenance_refs", self.provenance_refs)
        self._validate_claims()
        self._validate_bindings()
        start, terminal = self._validate_boundaries()
        self._validate_events(start, terminal)

    def _validate_claims(self) -> None:
        if self.canonical_effect != NONE:
            raise ValueError("encounter record must keep canonical_effect=NONE")
        for name in (
            "relationship_claim",
            "intimacy_claim",
            "shared_meaning_claim",
            "mutual_understanding_claim",
            "subjectivity_claim",
        ):
            if getattr(self, name) != NOT_ESTABLISHED:
                raise ValueError(f"{name} must remain NOT_ESTABLISHED")

    def _validate_bindings(self) -> None:
        binding_ids = [item.binding_id for item in self.bindings]
        entity_refs = [item.entity_ref for item in self.bindings]
        if len(binding_ids) != len(set(binding_ids)):
            raise ValueError("binding_id values must be unique")
        if len(entity_refs) != len(set(entity_refs)):
            raise ValueError("entity_ref values must be unique within one encounter")
        if entity_refs.count(self.subject_ref) != 1:
            raise ValueError("subject_ref must have exactly one binding")

    def _known_entities(self) -> set[str]:
        return {item.entity_ref for item in self.bindings}

    def _validate_boundaries(
        self,
    ) -> tuple[EncounterBoundaryEvidence, EncounterBoundaryEvidence | None]:
        boundary_ids = [item.boundary_id for item in self.boundaries]
        if len(boundary_ids) != len(set(boundary_ids)):
            raise ValueError("boundary_id values must be unique")
        for boundary in self.boundaries:
            if boundary.encounter_id != self.encounter_id:
                raise ValueError("boundary encounter_id mismatch")
            if boundary.source_actor_ref not in self._known_entities():
                raise ValueError("boundary source_actor_ref is not bound to encounter")
        starts = [item for item in self.boundaries if item.kind is BoundaryKind.START]
        if len(starts) != 1:
            raise ValueError("encounter requires exactly one START boundary")
        terminals = [
            item for item in self.boundaries if item.kind in (BoundaryKind.END, BoundaryKind.ABORT)
        ]
        if len(terminals) > 1:
            raise ValueError("encounter may have at most one terminal boundary")
        start = starts[0]
        terminal = terminals[0] if terminals else None
        if terminal is not None and _parse_timestamp(terminal.timestamp) < _parse_timestamp(start.timestamp):
            raise ValueError("terminal boundary cannot precede START boundary")
        return start, terminal

    def _validate_events(
        self,
        start: EncounterBoundaryEvidence,
        terminal: EncounterBoundaryEvidence | None,
    ) -> None:
        event_ids = [item.event_id for item in self.events]
        if len(event_ids) != len(set(event_ids)):
            raise ValueError("event_id values must be unique")
        known = self._known_entities()
        start_time = _parse_timestamp(start.timestamp)
        terminal_time = _parse_timestamp(terminal.timestamp) if terminal is not None else None
        for event in self.events:
            if event.encounter_id != self.encounter_id:
                raise ValueError("event encounter_id mismatch")
            if event.source_actor_ref not in known:
                raise ValueError("event source_actor_ref is not bound to encounter")
            if any(ref not in known for ref in event.involved_entity_refs):
                raise ValueError("event involved_entity_refs contain an unbound entity")
            event_time = _parse_timestamp(event.timestamp)
            if event_time < start_time:
                raise ValueError("event cannot occur before START boundary")
            if terminal_time is not None and event_time > terminal_time:
                raise ValueError("event cannot occur after terminal boundary")

    @property
    def status(self) -> EncounterStatus:
        for boundary in self.boundaries:
            if boundary.kind is BoundaryKind.ABORT:
                return EncounterStatus.ABORTED
            if boundary.kind is BoundaryKind.END:
                return EncounterStatus.CLOSED
        return EncounterStatus.OPEN

    @property
    def started_at(self) -> str:
        for boundary in self.boundaries:
            if boundary.kind is BoundaryKind.START:
                return boundary.timestamp
        raise RuntimeError("validated encounter is missing START boundary")

    @property
    def ended_at(self) -> str | None:
        terminals = [
            item.timestamp
            for item in self.boundaries
            if item.kind in (BoundaryKind.END, BoundaryKind.ABORT)
        ]
        return terminals[0] if terminals else None
