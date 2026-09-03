"""Inspection-only adapter to the existing agenda, not a new scheduler.

Pending requests require the memory-recall component when this adapter is used.
The campaign's synthetic mechanism probes do not adjudicate arbitrary claims.
Producing this agenda never runs a campaign or resolves a claim.
"""
from __future__ import annotations

from .agenda import _SCORE_BY_KIND
from .models import AgendaEntry, AgendaKind
from aion_triadic_state import canonical_hash


def build_revision_agenda(requests: tuple, *, limit: int = 3) -> tuple[AgendaEntry, ...]:
    from aion_memory_recall.revision import ClaimStatus, RevisionRequest

    if type(limit) is not int or not 1 <= limit <= 20:
        raise ValueError("revision agenda limit must be an integer between 1 and 20")
    if not isinstance(requests, tuple) or len(requests) > 64:
        raise ValueError("expected at most 64 pending requests")
    entries = {}
    for request in requests:
        if not isinstance(request, RevisionRequest) or request.status not in {ClaimStatus.CHALLENGED, ClaimStatus.DEPENDENCY_HOLD}:
            raise ValueError("agenda requires pending typed revision requests")
        if request.memory_id in entries:
            raise ValueError("duplicate pending memory version")
        entries[request.memory_id] = AgendaEntry(
            question_id="REV-" + canonical_hash(request)[:24],
            question=f"Recheck claim {request.claim_id} version {request.version}: {request.status.value}; preserve scope and counterevidence.",
            kind=AgendaKind.CONTRADICTION,
            score=_SCORE_BY_KIND[AgendaKind.CONTRADICTION],
            source_refs=(f"memory:{request.memory_id}", f"revision-head:{request.expected_event_hash}")
                + tuple(f"evidence:{ref}" for ref in request.evidence_refs)
                + tuple(f"premise:{ref}" for ref in request.dependency_refs),
        )
    return tuple(sorted(entries.values(), key=lambda entry: entry.question_id)[:limit])
