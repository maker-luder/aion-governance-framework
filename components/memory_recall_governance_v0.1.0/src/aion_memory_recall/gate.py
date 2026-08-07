from __future__ import annotations

from collections.abc import Iterable

from .models import MemoryRecord, RecallDecision, RecallRequest, RecallStatus


def _overlap(left: frozenset[str], right: frozenset[str]) -> int:
    return len({item.casefold() for item in left} & {item.casefold() for item in right})


def decide_recall(request: RecallRequest, record: MemoryRecord) -> RecallDecision:
    if not request.entity_cues and not request.topic_cues:
        return RecallDecision(RecallStatus.NOT_REQUIRED, None, "no cue")
    if record.tombstoned or record.superseded:
        return RecallDecision(RecallStatus.DENIED_PROVENANCE, record.memory_id, "record inactive")
    if request.user_id != record.user_id or request.agent_id != record.agent_id:
        return RecallDecision(RecallStatus.DENIED_IDENTITY, record.memory_id, "identity mismatch")
    if not record.access_scope.issubset(request.requester_scopes):
        return RecallDecision(RecallStatus.DENIED_ACCESS, record.memory_id, "access scope mismatch")
    if not record.provenance_verified:
        return RecallDecision(RecallStatus.DENIED_PROVENANCE, record.memory_id, "provenance incomplete")
    if record.conflict:
        return RecallDecision(RecallStatus.QUARANTINED_CONFLICT, record.memory_id, "unresolved conflict")
    if _overlap(request.entity_cues, record.entities) + _overlap(request.topic_cues, record.topics) == 0:
        return RecallDecision(RecallStatus.NOT_REQUIRED, None, "record not relevant")
    return RecallDecision(RecallStatus.TEMPORARY_ONLY, record.memory_id, "minimum necessary context only")


def rank_candidates(request: RecallRequest, records: Iterable[MemoryRecord]) -> list[MemoryRecord]:
    eligible: list[tuple[int, str, MemoryRecord]] = []
    for record in records:
        decision = decide_recall(request, record)
        if decision.status is RecallStatus.TEMPORARY_ONLY:
            score = 2 * _overlap(request.entity_cues, record.entities) + _overlap(request.topic_cues, record.topics)
            eligible.append((-score, record.memory_id, record))
    return [record for _, _, record in sorted(eligible)]
