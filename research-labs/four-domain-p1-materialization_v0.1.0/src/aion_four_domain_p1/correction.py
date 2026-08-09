from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


def _require_aware(value: datetime, field_name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field_name} must be timezone-aware")


class TransitionKind(str, Enum):
    CONFLICT_DETECTED = "CONFLICT_DETECTED"
    CORRECTION_PROPOSED = "CORRECTION_PROPOSED"
    CORRECTION_APPROVED = "CORRECTION_APPROVED"
    CORRECTION_REJECTED = "CORRECTION_REJECTED"
    SUPERSEDED = "SUPERSEDED"
    CONFLICT_RESOLVED = "CONFLICT_RESOLVED"
    WITHDRAWN = "WITHDRAWN"


@dataclass(frozen=True, slots=True)
class ClaimRecord:
    case_id: str
    claim_id: str
    subject_id: str
    namespace: str
    content_ref: str
    recorded_at: datetime
    source_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        for field_name in ("case_id", "claim_id", "subject_id", "namespace", "content_ref"):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} must be non-empty")
        _require_aware(self.recorded_at, "recorded_at")
        if not self.source_refs:
            raise ValueError("claim requires source_refs")


@dataclass(frozen=True, slots=True)
class TransitionEvent:
    transition_id: str
    case_id: str
    kind: TransitionKind
    actor_id: str
    actor_role: str
    occurred_at: datetime
    recorded_at: datetime
    evidence_refs: tuple[str, ...]
    source_claim_id: str | None = None
    target_claim_id: str | None = None
    reason: str = ""

    def __post_init__(self) -> None:
        for field_name in ("transition_id", "case_id", "actor_id", "actor_role"):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} must be non-empty")
        _require_aware(self.occurred_at, "occurred_at")
        _require_aware(self.recorded_at, "recorded_at")
        if self.recorded_at < self.occurred_at:
            raise ValueError("recorded_at cannot predate occurred_at")
        if not self.evidence_refs:
            raise ValueError("transition requires evidence_refs")


@dataclass(frozen=True, slots=True)
class LedgerProjection:
    case_id: str
    active_claim_ids: tuple[str, ...]
    superseded_claim_ids: tuple[str, ...]
    withdrawn_claim_ids: tuple[str, ...]
    unresolved_conflicts: tuple[tuple[str, str], ...]
    transition_ids: tuple[str, ...]


class CorrectionConflictLedger:
    """Append-only correction/conflict research ledger.

    The ledger records state transitions but grants no canonical authority. Supersession
    requires an explicit prior correction approval for the same source/target pair.
    """

    def __init__(self) -> None:
        self._claims: dict[str, ClaimRecord] = {}
        self._case_claims: dict[str, list[str]] = {}
        self._events: dict[str, TransitionEvent] = {}
        self._case_events: dict[str, list[str]] = {}

    def add_claim(self, claim: ClaimRecord) -> None:
        if claim.claim_id in self._claims:
            raise ValueError(f"duplicate claim_id: {claim.claim_id}")
        existing = self._case_claims.get(claim.case_id, [])
        if existing:
            first = self._claims[existing[0]]
            if (first.subject_id, first.namespace) != (claim.subject_id, claim.namespace):
                raise ValueError("case subject_id/namespace binding is immutable")
        self._claims[claim.claim_id] = claim
        self._case_claims.setdefault(claim.case_id, []).append(claim.claim_id)

    def append(self, event: TransitionEvent) -> None:
        if event.transition_id in self._events:
            raise ValueError(f"duplicate transition_id: {event.transition_id}")
        self._validate_claim_refs(event)
        pair = self._pair(event)

        if event.kind in {
            TransitionKind.CONFLICT_DETECTED,
            TransitionKind.CORRECTION_PROPOSED,
            TransitionKind.CORRECTION_APPROVED,
            TransitionKind.CORRECTION_REJECTED,
            TransitionKind.SUPERSEDED,
            TransitionKind.CONFLICT_RESOLVED,
        } and pair is None:
            raise ValueError(f"{event.kind.value} requires source_claim_id and target_claim_id")

        if pair is not None and pair[0] == pair[1]:
            raise ValueError("source and target claims must be distinct")

        if event.kind is TransitionKind.SUPERSEDED and pair not in self._approved_pairs(event.case_id):
            raise ValueError("supersession requires a prior CORRECTION_APPROVED for the same pair")

        if event.kind is TransitionKind.CONFLICT_RESOLVED and pair not in self._detected_conflicts(event.case_id):
            raise ValueError("conflict resolution requires a prior CONFLICT_DETECTED for the same pair")

        self._events[event.transition_id] = event
        self._case_events.setdefault(event.case_id, []).append(event.transition_id)

    def project(self, case_id: str) -> LedgerProjection:
        claims = set(self._case_claims.get(case_id, []))
        events = self.events(case_id)
        superseded = {
            event.source_claim_id
            for event in events
            if event.kind is TransitionKind.SUPERSEDED and event.source_claim_id is not None
        }
        withdrawn = {
            event.source_claim_id
            for event in events
            if event.kind is TransitionKind.WITHDRAWN and event.source_claim_id is not None
        }
        detected = self._detected_conflicts(case_id)
        resolved = {
            pair
            for event in events
            if event.kind is TransitionKind.CONFLICT_RESOLVED
            if (pair := self._pair(event)) is not None
        }
        unresolved = tuple(sorted(detected - resolved))
        active = tuple(sorted(claims - superseded - withdrawn))
        return LedgerProjection(
            case_id=case_id,
            active_claim_ids=active,
            superseded_claim_ids=tuple(sorted(superseded)),
            withdrawn_claim_ids=tuple(sorted(withdrawn)),
            unresolved_conflicts=unresolved,
            transition_ids=tuple(event.transition_id for event in events),
        )

    def claims(self, case_id: str) -> tuple[ClaimRecord, ...]:
        return tuple(self._claims[item_id] for item_id in self._case_claims.get(case_id, []))

    def events(self, case_id: str) -> tuple[TransitionEvent, ...]:
        return tuple(
            sorted(
                (self._events[item_id] for item_id in self._case_events.get(case_id, [])),
                key=lambda item: (item.recorded_at, item.transition_id),
            )
        )

    def _validate_claim_refs(self, event: TransitionEvent) -> None:
        for claim_id in (event.source_claim_id, event.target_claim_id):
            if claim_id is None:
                continue
            claim = self._claims.get(claim_id)
            if claim is None:
                raise ValueError(f"unknown claim_id: {claim_id}")
            if claim.case_id != event.case_id:
                raise ValueError("transition cannot cross cases")

        if event.kind is TransitionKind.WITHDRAWN and event.source_claim_id is None:
            raise ValueError("WITHDRAWN requires source_claim_id")

    def _approved_pairs(self, case_id: str) -> set[tuple[str, str]]:
        return {
            pair
            for event in self.events(case_id)
            if event.kind is TransitionKind.CORRECTION_APPROVED
            if (pair := self._pair(event)) is not None
        }

    def _detected_conflicts(self, case_id: str) -> set[tuple[str, str]]:
        return {
            pair
            for event in self.events(case_id)
            if event.kind is TransitionKind.CONFLICT_DETECTED
            if (pair := self._pair(event)) is not None
        }

    @staticmethod
    def _pair(event: TransitionEvent) -> tuple[str, str] | None:
        if event.source_claim_id is None or event.target_claim_id is None:
            return None
        return (event.source_claim_id, event.target_claim_id)
