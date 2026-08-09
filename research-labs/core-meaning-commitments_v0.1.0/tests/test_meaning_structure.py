from __future__ import annotations

import pytest

from aion_core_meaning import (
    EvidenceRef,
    MeaningClaim,
    MeaningKind,
    MeaningProjection,
    MeaningRelation,
    MeaningRelationKind,
    MeaningStructureAnalyzer,
    ProvenanceKind,
)


def evidence() -> tuple[EvidenceRef, ...]:
    return (
        EvidenceRef(
            source_id="synthetic-source",
            source_kind=ProvenanceKind.REPOSITORY_EVIDENCE,
            locator="core-meaning-structure-fixture",
        ),
    )


def claim(claim_id: str, proposition: str, *, subject_id: str = "subject-a", namespace: str = "meaning-a") -> MeaningClaim:
    return MeaningClaim(
        claim_id=claim_id,
        subject_id=subject_id,
        namespace=namespace,
        kind=MeaningKind.ORGANIZING_COMMITMENT,
        proposition=proposition,
        importance=0.8,
        confidence=0.7,
        provenance=evidence(),
        recorded_at="2026-08-09T00:00:00Z",
    )


def projection(*claims: MeaningClaim, subject_id: str = "subject-a", namespace: str = "meaning-a") -> MeaningProjection:
    return MeaningProjection(
        subject_id=subject_id,
        namespace=namespace,
        current_candidate_claims=claims,
        superseded_claim_ids=(),
        withdrawn_claim_ids=(),
        conflict_pairs=(),
    )


def relation(relation_id: str = "r1", *, source: str = "c1", target: str = "c2", subject_id: str = "subject-a", namespace: str = "meaning-a", confidence: float = 0.8) -> MeaningRelation:
    return MeaningRelation(
        relation_id=relation_id,
        subject_id=subject_id,
        namespace=namespace,
        source_claim_id=source,
        target_claim_id=target,
        kind=MeaningRelationKind.SUPPORTS,
        provenance_refs=("synthetic-relation-evidence",),
        confidence=confidence,
    )


def test_fingerprint_is_deterministic_across_input_order() -> None:
    analyzer = MeaningStructureAnalyzer()
    c1, c2 = claim("c1", "Preserve provenance."), claim("c2", "Keep changes inspectable.")
    first = analyzer.snapshot(projection(c1, c2), (relation(),))
    second = analyzer.snapshot(projection(c2, c1), (relation(),))
    assert first.structure_fingerprint == second.structure_fingerprint


def test_relation_target_must_exist() -> None:
    analyzer = MeaningStructureAnalyzer()
    with pytest.raises(ValueError, match="endpoints"):
        analyzer.snapshot(projection(claim("c1", "A")), (relation(target="missing"),))


def test_relation_scope_must_match_projection() -> None:
    analyzer = MeaningStructureAnalyzer()
    c1, c2 = claim("c1", "A"), claim("c2", "B")
    with pytest.raises(ValueError, match="subject and namespace"):
        analyzer.snapshot(projection(c1, c2), (relation(namespace="other"),))


def test_drift_detects_claim_and_relation_changes() -> None:
    analyzer = MeaningStructureAnalyzer()
    c1, c2 = claim("c1", "A"), claim("c2", "B")
    before = analyzer.snapshot(projection(c1, c2), (relation(),))
    c2_changed = claim("c2", "B revised")
    c3 = claim("c3", "C")
    after = analyzer.snapshot(
        projection(c1, c2_changed, c3),
        (
            relation("r1", confidence=0.5),
            relation("r2", source="c2", target="c3"),
        ),
    )
    drift = analyzer.compare(before, after)
    assert drift.changed is True
    assert drift.added_claim_ids == ("c3",)
    assert drift.changed_claim_ids == ("c2",)
    assert drift.added_relation_ids == ("r2",)
    assert drift.changed_relation_ids == ("r1",)


def test_cross_scope_snapshots_cannot_be_compared() -> None:
    analyzer = MeaningStructureAnalyzer()
    first = analyzer.snapshot(projection(claim("c1", "A")))
    other_claim = claim("c1", "A", namespace="meaning-b")
    second = analyzer.snapshot(projection(other_claim, namespace="meaning-b"))
    with pytest.raises(ValueError, match="cross-subject or cross-namespace"):
        analyzer.compare(first, second)


def test_fingerprint_changes_when_semantics_change() -> None:
    analyzer = MeaningStructureAnalyzer()
    first = analyzer.snapshot(projection(claim("c1", "A")))
    second = analyzer.snapshot(projection(claim("c1", "A revised")))
    assert first.structure_fingerprint != second.structure_fingerprint


def test_epistemic_locks_are_preserved() -> None:
    analyzer = MeaningStructureAnalyzer()
    snap = analyzer.snapshot(projection(claim("c1", "A")))
    assert snap.canonical_effect == "NONE"
    assert snap.runtime_effect == "NONE"
    assert snap.identity_conclusion == "NOT_ESTABLISHED"
    assert snap.subjectivity_conclusion == "NOT_ESTABLISHED"


def test_duplicate_relation_id_is_rejected() -> None:
    analyzer = MeaningStructureAnalyzer()
    c1, c2 = claim("c1", "A"), claim("c2", "B")
    with pytest.raises(ValueError, match="duplicate relation_id"):
        analyzer.snapshot(projection(c1, c2), (relation("r1"), relation("r1")))


def test_duplicate_claim_id_is_rejected() -> None:
    analyzer = MeaningStructureAnalyzer()
    with pytest.raises(ValueError, match="duplicate claim_id"):
        analyzer.snapshot(projection(claim("c1", "A"), claim("c1", "B")))


def test_relation_provenance_and_confidence_are_bounded() -> None:
    with pytest.raises(ValueError, match="provenance_refs"):
        MeaningRelation(
            relation_id="r-empty",
            subject_id="subject-a",
            namespace="meaning-a",
            source_claim_id="c1",
            target_claim_id="c2",
            kind=MeaningRelationKind.SUPPORTS,
            provenance_refs=(),
        )
    with pytest.raises(ValueError, match="confidence"):
        relation("r-high", confidence=1.1)


def test_self_relation_is_rejected() -> None:
    with pytest.raises(ValueError, match="cannot target itself"):
        relation("r-self", source="c1", target="c1")
