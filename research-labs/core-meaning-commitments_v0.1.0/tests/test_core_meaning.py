from __future__ import annotations

import pytest

from aion_core_meaning import (
    AssessmentDecision,
    CoreMeaningWorkbench,
    EvidenceRef,
    JudgmentContext,
    MeaningClaim,
    MeaningEvent,
    MeaningEventKind,
    MeaningKind,
    ProvenanceKind,
    can_derive_authority_from_relationship,
    can_promote_canonical,
    can_transfer_across_namespace,
    governance_status,
)


def evidence(source_id: str = "owner-declaration-1") -> tuple[EvidenceRef, ...]:
    return (
        EvidenceRef(
            source_id=source_id,
            source_kind=ProvenanceKind.HUMAN_OWNER_DECLARATION,
            locator="synthetic-fixture",
        ),
    )


def claim(
    claim_id: str,
    *,
    subject_id: str = "subject-a",
    namespace: str = "meaning-a",
    kind: MeaningKind = MeaningKind.CORE_BELIEF,
    proposition: str = "Evidence should remain distinguishable from interpretation.",
    importance: float = 0.8,
    confidence: float = 0.7,
    revision_of: str | None = None,
) -> MeaningClaim:
    return MeaningClaim(
        claim_id=claim_id,
        subject_id=subject_id,
        namespace=namespace,
        kind=kind,
        proposition=proposition,
        importance=importance,
        confidence=confidence,
        provenance=evidence(),
        recorded_at="2026-08-09T00:00:00Z",
        revision_of=revision_of,
    )


def event_for(item: MeaningClaim, event_id: str) -> MeaningEvent:
    revised = item.revision_of is not None
    return MeaningEvent(
        event_id=event_id,
        subject_id=item.subject_id,
        namespace=item.namespace,
        kind=MeaningEventKind.CLAIM_REVISED if revised else MeaningEventKind.CLAIM_ADDED,
        claim_id=item.claim_id,
        related_claim_ids=(item.revision_of,) if revised else (),
        provenance=evidence(),
        recorded_at="2026-08-09T00:00:01Z",
    )


def test_claim_requires_provenance() -> None:
    with pytest.raises(ValueError, match="provenance"):
        MeaningClaim(
            claim_id="c1",
            subject_id="subject-a",
            namespace="meaning-a",
            kind=MeaningKind.CORE_BELIEF,
            proposition="A candidate proposition",
            importance=0.5,
            confidence=0.5,
            provenance=(),
            recorded_at="2026-08-09T00:00:00Z",
        )


def test_importance_and_confidence_are_separate_bounded_fields() -> None:
    item = claim("c1", importance=0.9, confidence=0.2)
    assert item.importance == 0.9
    assert item.confidence == 0.2
    with pytest.raises(ValueError, match="importance"):
        claim("c2", importance=1.1)
    with pytest.raises(ValueError, match="confidence"):
        claim("c3", confidence=-0.1)


def test_revision_preserves_history_and_projects_successor() -> None:
    ledger = CoreMeaningWorkbench()
    original = claim("c1")
    revised = claim("c2", revision_of="c1", proposition="Evidence and interpretation must remain separate.")
    ledger.add_candidate(original, event_for(original, "e1"))
    ledger.add_candidate(revised, event_for(revised, "e2"))
    projection = ledger.project_current("subject-a", "meaning-a")
    assert projection.superseded_claim_ids == ("c1",)
    assert tuple(item.claim_id for item in projection.current_candidate_claims) == ("c2",)
    assert tuple(item.kind for item in ledger.history("subject-a", "meaning-a")) == (
        MeaningEventKind.CLAIM_ADDED,
        MeaningEventKind.CLAIM_REVISED,
    )


def test_cross_namespace_revision_is_rejected() -> None:
    ledger = CoreMeaningWorkbench()
    original = claim("c1", namespace="meaning-a")
    revised = claim("c2", namespace="meaning-b", revision_of="c1")
    ledger.add_candidate(original, event_for(original, "e1"))
    with pytest.raises(ValueError, match="cross-subject or cross-namespace"):
        ledger.add_candidate(revised, event_for(revised, "e2"))


def test_conflict_requires_review_and_never_decides_judgment() -> None:
    ledger = CoreMeaningWorkbench()
    first = claim("c1", proposition="Preserve established baselines.")
    second = claim("c2", proposition="Replace an established baseline immediately.")
    ledger.add_candidate(first, event_for(first, "e1"))
    ledger.add_candidate(second, event_for(second, "e2"))
    ledger.record_conflict(
        MeaningEvent(
            event_id="e3",
            subject_id="subject-a",
            namespace="meaning-a",
            kind=MeaningEventKind.CONFLICT_RECORDED,
            claim_id="c1",
            related_claim_ids=("c2",),
            provenance=evidence("conflict-review-1"),
            recorded_at="2026-08-09T00:00:02Z",
        )
    )
    result = ledger.assess(
        JudgmentContext(
            judgment_id="j1",
            subject_id="subject-a",
            namespace="meaning-a",
            proposition="How should a baseline change be reviewed?",
            relevant_claim_ids=("c1", "c2"),
            evidence_refs=evidence("judgment-evidence-1"),
        )
    )
    assert result.decision is AssessmentDecision.CONFLICT_REVIEW_REQUIRED
    assert result.final_judgment is None
    assert result.authority_granted is False
    assert result.writeback_authorized is False
    assert result.canonical_effect == "NONE"


def test_caller_must_explicitly_name_relevant_claims() -> None:
    ledger = CoreMeaningWorkbench()
    item = claim("c1")
    ledger.add_candidate(item, event_for(item, "e1"))
    result = ledger.assess(
        JudgmentContext(
            judgment_id="j1",
            subject_id="subject-a",
            namespace="meaning-a",
            proposition=item.proposition,
            relevant_claim_ids=(),
            evidence_refs=evidence("judgment-evidence-1"),
        )
    )
    assert result.decision is AssessmentDecision.NO_APPLICABLE_CLAIM
    assert result.influence_trace == ()


def test_same_text_does_not_merge_subjects() -> None:
    ledger = CoreMeaningWorkbench()
    first = claim("c1", subject_id="subject-a")
    second = claim("c2", subject_id="subject-b")
    ledger.add_candidate(first, event_for(first, "e1"))
    ledger.add_candidate(second, event_for(second, "e2"))
    assert tuple(item.claim_id for item in ledger.project_current("subject-a", "meaning-a").current_candidate_claims) == ("c1",)
    assert tuple(item.claim_id for item in ledger.project_current("subject-b", "meaning-a").current_candidate_claims) == ("c2",)


def test_policy_guards_are_fail_closed() -> None:
    status = governance_status()
    assert can_promote_canonical() is False
    assert can_derive_authority_from_relationship() is False
    assert can_transfer_across_namespace() is False
    assert status["module_status"] == "RESEARCH_CANDIDATE"
    assert status["subjectivity_conclusion"] == "NOT_ESTABLISHED"
    assert status["phenomenal_affect_conclusion"] == "NOT_ESTABLISHED"
    assert status["canonical_effect"] == "NONE"


def test_module_exposes_no_canonicalization_method() -> None:
    ledger = CoreMeaningWorkbench()
    assert not hasattr(ledger, "canonicalize")
    assert not hasattr(ledger, "writeback")
    assert not hasattr(ledger, "transfer_namespace")
