from dataclasses import replace

import pytest

from aion_human_ai_longitudinal import (
    AccumulationConditionPacket, AccumulationError, ArtifactCondition,
    DependencyEdge, DependencyGraph, DependencyNode, EdgeType,
    EvidenceReuseFirewall, EvidenceSupportManifest, NodeType, ReuseStatus,
    SupportRelation, audit_accumulation_packets,
)


def manifest(**changes: object) -> EvidenceSupportManifest:
    values = dict(claim_id="claim:new", source_id="source:primary", source_class="PRIMARY",
        source_version_or_date="v2", rechecked_at="2026-09-13", supported_proposition="P",
        requested_proposition="P", source_scope="S", requested_scope="S",
        support_relation=SupportRelation.DIRECT, claim_ceiling="bounded functional claim",
        known_counterevidence=("counterevidence:bounded-search",), canonical_source=True,
        source_current=True, empirical_result_reused=False, reuse_status=ReuseStatus.ALLOWED,
        reuse_reason="exact proposition and scope rechecked")
    values.update(changes)
    return EvidenceSupportManifest(**values)


def packets() -> tuple[AccumulationConditionPacket, ...]:
    return (
        AccumulationConditionPacket(ArtifactCondition.FRESH_TASK_LOCAL, "fresh task", False, False, False, False),
        AccumulationConditionPacket(ArtifactCondition.FLAT_SUMMARY, "flat summary", False, False, False, False),
        AccumulationConditionPacket(ArtifactCondition.VERSIONED_ARTIFACT, "versioned", True, True, True, False),
        AccumulationConditionPacket(ArtifactCondition.VERSIONED_ARTIFACT_PLUS_NAVIGATION, "navigable", True, True, True, True),
    )


def test_exact_rechecked_binding_is_allowed() -> None:
    assert EvidenceReuseFirewall().validate(manifest()) is ReuseStatus.ALLOWED


@pytest.mark.parametrize("change", [
    {"requested_proposition": "different", "reuse_status": ReuseStatus.RECHECK_REQUIRED},
    {"requested_scope": "different", "reuse_status": ReuseStatus.RECHECK_REQUIRED},
    {"source_current": False, "reuse_status": ReuseStatus.RECHECK_REQUIRED},
    {"canonical_source": False, "reuse_status": ReuseStatus.RECHECK_REQUIRED},
    {"empirical_result_reused": True, "reuse_status": ReuseStatus.RECHECK_REQUIRED},
])
def test_changed_binding_requires_recheck(change: dict[str, object]) -> None:
    assert EvidenceReuseFirewall().validate(manifest(**change)) is ReuseStatus.RECHECK_REQUIRED


def test_inflated_allowed_status_fails_closed() -> None:
    with pytest.raises(AccumulationError, match="RECHECK_REQUIRED"):
        EvidenceReuseFirewall().validate(manifest(requested_proposition="different"))


def test_dependency_graph_separates_baseline_from_relations() -> None:
    graph = DependencyGraph("base", (
        DependencyNode("base", NodeType.BASELINE, "git:base"),
        DependencyNode("claim", NodeType.CLAIM, "claim:v1"),
        DependencyNode("source", NodeType.SOURCE, "doi:fixture"),
    ), (DependencyEdge("claim", "source", EdgeType.SUPPORTED_BY),))
    assert graph.edges[0].relation is EdgeType.SUPPORTED_BY
    with pytest.raises(AccumulationError, match="unknown node"):
        replace(graph, edges=(DependencyEdge("claim", "missing", EdgeType.DEPENDS_ON),))


def test_a_to_d_matrix_preserves_nonclaims() -> None:
    result = audit_accumulation_packets(packets())
    assert result["structurally_admissible"] is True
    assert result["empirical_result"] == "SYNTHETIC_FIXTURE_ONLY"
    assert result["mutual_learning"] == "NOT_ESTABLISHED"
    assert result["subjectivity"] == "NOT_ESTABLISHED"
    assert result["canonical_effect"] == "NONE"
    with pytest.raises(AccumulationError, match="exact A-D"):
        audit_accumulation_packets(packets()[:-1])


def test_controls_and_privacy_fail_closed() -> None:
    with pytest.raises(AccumulationError, match="versioned artifact"):
        AccumulationConditionPacket(ArtifactCondition.VERSIONED_ARTIFACT, "x", True, False, True, False)
    with pytest.raises(AccumulationError, match="navigation condition"):
        AccumulationConditionPacket(ArtifactCondition.VERSIONED_ARTIFACT_PLUS_NAVIGATION, "x", True, True, True, False)
    with pytest.raises(AccumulationError, match="private"):
        replace(packets()[0], contains_private_transcript=True)
