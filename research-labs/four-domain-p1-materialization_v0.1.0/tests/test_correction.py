from datetime import datetime, timezone

import pytest

from aion_four_domain_p1 import ClaimRecord, CorrectionConflictLedger, TransitionEvent, TransitionKind

UTC = timezone.utc


def dt(hour: int) -> datetime:
    return datetime(2026, 8, 9, hour, tzinfo=UTC)


def claim(claim_id: str) -> ClaimRecord:
    return ClaimRecord(
        case_id="case-1",
        claim_id=claim_id,
        subject_id="subject-a",
        namespace="AION",
        content_ref=f"content:{claim_id}",
        recorded_at=dt(1),
        source_refs=(f"source:{claim_id}",),
    )


def event(event_id: str, kind: TransitionKind, source: str, target: str | None = None, hour: int = 2) -> TransitionEvent:
    return TransitionEvent(
        transition_id=event_id,
        case_id="case-1",
        kind=kind,
        actor_id="reviewer-1",
        actor_role="RESEARCH_REVIEWER",
        occurred_at=dt(hour),
        recorded_at=dt(hour),
        evidence_refs=(f"evidence:{event_id}",),
        source_claim_id=source,
        target_claim_id=target,
        reason="synthetic fixture",
    )


def test_supersession_requires_explicit_approval() -> None:
    ledger = CorrectionConflictLedger()
    ledger.add_claim(claim("old"))
    ledger.add_claim(claim("new"))

    with pytest.raises(ValueError, match="prior CORRECTION_APPROVED"):
        ledger.append(event("t1", TransitionKind.SUPERSEDED, "old", "new"))

    ledger.append(event("t2", TransitionKind.CORRECTION_PROPOSED, "old", "new"))
    ledger.append(event("t3", TransitionKind.CORRECTION_APPROVED, "old", "new", hour=3))
    ledger.append(event("t4", TransitionKind.SUPERSEDED, "old", "new", hour=4))

    projection = ledger.project("case-1")
    assert projection.active_claim_ids == ("new",)
    assert projection.superseded_claim_ids == ("old",)


def test_conflict_remains_visible_until_explicit_resolution() -> None:
    ledger = CorrectionConflictLedger()
    ledger.add_claim(claim("a"))
    ledger.add_claim(claim("b"))
    ledger.append(event("c1", TransitionKind.CONFLICT_DETECTED, "a", "b"))
    assert ledger.project("case-1").unresolved_conflicts == (("a", "b"),)

    ledger.append(event("c2", TransitionKind.CONFLICT_RESOLVED, "a", "b", hour=3))
    assert ledger.project("case-1").unresolved_conflicts == ()


def test_missing_evidence_fails_closed() -> None:
    with pytest.raises(ValueError, match="evidence_refs"):
        TransitionEvent(
            transition_id="x",
            case_id="case-1",
            kind=TransitionKind.WITHDRAWN,
            actor_id="actor",
            actor_role="reviewer",
            occurred_at=dt(1),
            recorded_at=dt(1),
            evidence_refs=(),
            source_claim_id="a",
        )
