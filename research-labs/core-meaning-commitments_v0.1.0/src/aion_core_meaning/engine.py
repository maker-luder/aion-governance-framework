from __future__ import annotations

from .models import (
    AssessmentDecision,
    InfluenceTrace,
    JudgmentContext,
    MeaningAssessment,
    MeaningClaim,
    MeaningEvent,
    MeaningEventKind,
    MeaningProjection,
)


class CoreMeaningWorkbench:
    """In-memory candidate ledger with no canonical or runtime write path."""

    def __init__(self) -> None:
        self._claims: dict[str, MeaningClaim] = {}
        self._events: list[MeaningEvent] = []

    def add_candidate(self, claim: MeaningClaim, event: MeaningEvent) -> None:
        if claim.claim_id in self._claims:
            raise ValueError("claim_id must be unique")
        expected_kind = MeaningEventKind.CLAIM_REVISED if claim.revision_of else MeaningEventKind.CLAIM_ADDED
        if event.kind is not expected_kind:
            raise ValueError(f"event kind must be {expected_kind.value}")
        self._validate_event_binding(claim, event)
        if claim.revision_of:
            previous = self._require_claim(claim.revision_of)
            self._require_same_scope(claim.subject_id, claim.namespace, previous)
            if event.related_claim_ids != (claim.revision_of,):
                raise ValueError("revision event must identify exactly the revised claim")
        elif event.related_claim_ids:
            raise ValueError("new-claim event must not include related claims")
        self._claims[claim.claim_id] = claim
        self._events.append(event)

    def record_conflict(self, event: MeaningEvent) -> None:
        if event.kind is not MeaningEventKind.CONFLICT_RECORDED:
            raise ValueError("conflict event kind is required")
        if len(event.related_claim_ids) != 1:
            raise ValueError("conflict event must identify exactly one other claim")
        first = self._require_claim(event.claim_id)
        second = self._require_claim(event.related_claim_ids[0])
        self._require_same_scope(event.subject_id, event.namespace, first)
        self._require_same_scope(event.subject_id, event.namespace, second)
        if first.claim_id == second.claim_id:
            raise ValueError("a claim cannot conflict with itself")
        self._events.append(event)

    def withdraw_candidate(self, event: MeaningEvent) -> None:
        if event.kind is not MeaningEventKind.CLAIM_WITHDRAWN:
            raise ValueError("withdrawal event kind is required")
        claim = self._require_claim(event.claim_id)
        self._require_same_scope(event.subject_id, event.namespace, claim)
        if event.related_claim_ids:
            raise ValueError("withdrawal event must not include related claims")
        self._events.append(event)

    def history(self, subject_id: str, namespace: str) -> tuple[MeaningEvent, ...]:
        return tuple(
            event
            for event in self._events
            if event.subject_id == subject_id and event.namespace == namespace
        )

    def project_current(self, subject_id: str, namespace: str) -> MeaningProjection:
        scoped_claims = tuple(
            claim
            for claim in self._claims.values()
            if claim.subject_id == subject_id and claim.namespace == namespace
        )
        superseded = {claim.revision_of for claim in scoped_claims if claim.revision_of is not None}
        scoped_events = self.history(subject_id, namespace)
        withdrawn = {
            event.claim_id
            for event in scoped_events
            if event.kind is MeaningEventKind.CLAIM_WITHDRAWN
        }
        conflict_pairs = {
            tuple(sorted((event.claim_id, event.related_claim_ids[0])))
            for event in scoped_events
            if event.kind is MeaningEventKind.CONFLICT_RECORDED
        }
        current = tuple(
            claim
            for claim in scoped_claims
            if claim.claim_id not in superseded and claim.claim_id not in withdrawn
        )
        return MeaningProjection(
            subject_id=subject_id,
            namespace=namespace,
            current_candidate_claims=current,
            superseded_claim_ids=tuple(sorted(superseded)),
            withdrawn_claim_ids=tuple(sorted(withdrawn)),
            conflict_pairs=tuple(sorted(conflict_pairs)),
        )

    def assess(self, context: JudgmentContext) -> MeaningAssessment:
        projection = self.project_current(context.subject_id, context.namespace)
        current = {claim.claim_id: claim for claim in projection.current_candidate_claims}
        requested = tuple(dict.fromkeys(context.relevant_claim_ids))
        applicable = tuple(claim_id for claim_id in requested if claim_id in current)
        unavailable = tuple(claim_id for claim_id in requested if claim_id not in current)
        applicable_set = set(applicable)
        conflicts = tuple(
            pair
            for pair in projection.conflict_pairs
            if pair[0] in applicable_set and pair[1] in applicable_set
        )
        trace = tuple(
            InfluenceTrace(
                claim_id=claim.claim_id,
                kind=claim.kind,
                importance=claim.importance,
                confidence=claim.confidence,
            )
            for claim in (current[claim_id] for claim_id in applicable)
        )
        if conflicts:
            decision = AssessmentDecision.CONFLICT_REVIEW_REQUIRED
        elif applicable:
            decision = AssessmentDecision.REVIEW_REQUIRED
        else:
            decision = AssessmentDecision.NO_APPLICABLE_CLAIM
        return MeaningAssessment(
            decision=decision,
            applicable_claim_ids=applicable,
            unavailable_claim_ids=unavailable,
            conflict_pairs=conflicts,
            influence_trace=trace,
        )

    def _validate_event_binding(self, claim: MeaningClaim, event: MeaningEvent) -> None:
        if event.claim_id != claim.claim_id:
            raise ValueError("event claim_id must match claim")
        if event.subject_id != claim.subject_id or event.namespace != claim.namespace:
            raise ValueError("event and claim must share subject and namespace")

    def _require_claim(self, claim_id: str) -> MeaningClaim:
        try:
            return self._claims[claim_id]
        except KeyError as exc:
            raise ValueError(f"unknown claim: {claim_id}") from exc

    @staticmethod
    def _require_same_scope(subject_id: str, namespace: str, claim: MeaningClaim) -> None:
        if claim.subject_id != subject_id or claim.namespace != namespace:
            raise ValueError("cross-subject or cross-namespace operation is prohibited")
