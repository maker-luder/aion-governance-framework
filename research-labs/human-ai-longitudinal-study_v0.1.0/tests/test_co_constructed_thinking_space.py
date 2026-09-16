from __future__ import annotations

from dataclasses import replace

import pytest

from aion_human_ai_longitudinal import StudyError
from aion_human_ai_longitudinal.co_constructed_thinking_space import (
    CoConstructedThinkingSpaceManifest,
    ContributionRole,
    EpistemicContribution,
    RevisionEdge,
    RevisionRelation,
    ThinkingSpaceProfile,
    audit_co_constructed_thinking_space,
)


def digest(char: str) -> str:
    return char * 64


def contribution(
    contribution_id: str,
    role: ContributionRole,
    char: str,
) -> EpistemicContribution:
    return EpistemicContribution(
        contribution_id=contribution_id,
        role=role,
        payload_sha256=digest(char),
    )


def research_manifest() -> CoConstructedThinkingSpaceManifest:
    contributions = (
        contribution("human", ContributionRole.HUMAN_OWNER, "1"),
        contribution("ai", ContributionRole.AI_COLLABORATOR, "2"),
        contribution("evidence", ContributionRole.EXTERNAL_EVIDENCE, "3"),
        contribution("implementation", ContributionRole.IMPLEMENTATION_EVIDENCE, "4"),
        contribution("repository", ContributionRole.REPOSITORY_ARTIFACT, "b"),
        contribution("reentry", ContributionRole.REPOSITORY_ARTIFACT, "c"),
    )
    edges = (
        RevisionEdge("human", "ai", RevisionRelation.CHALLENGES),
        RevisionEdge("ai", "human", RevisionRelation.REVISES),
        RevisionEdge("evidence", "ai", RevisionRelation.REVISES),
        RevisionEdge("repository", "human", RevisionRelation.CLARIFIES),
        RevisionEdge("reentry", "ai", RevisionRelation.CLARIFIES),
        RevisionEdge("implementation", "human", RevisionRelation.CHALLENGES),
    )
    return CoConstructedThinkingSpaceManifest(
        space_id="ccts:synthetic:research",
        profile=ThinkingSpaceProfile.LONGITUDINAL_REPOSITORY_RESEARCH,
        problem_representation_sha256=digest("6"),
        contributions=contributions,
        revision_edges=edges,
        provenance_manifest_sha256=digest("7"),
        claim_boundary_sha256=digest("8"),
        authority_policy_sha256=digest("9"),
        rejected_branch_manifest_sha256=digest("a"),
        persistent_artifact_sha256=digest("b"),
        reentry_binding_sha256=digest("c"),
    )


def test_complete_longitudinal_repository_profile_is_structural_qa_only() -> None:
    audit = audit_co_constructed_thinking_space(research_manifest())
    assert audit.profile is ThinkingSpaceProfile.LONGITUDINAL_REPOSITORY_RESEARCH
    assert audit.reciprocal_human_ai_revision is True
    assert audit.revision_graph_connected is True
    assert audit.external_evidence_present is True
    assert audit.repository_artifact_present is True
    assert audit.implementation_evidence_present is True
    assert audit.longitudinal_bindings_present is True
    assert audit.research_profile_complete is True
    assert audit.mode == "DETERMINISTIC_SYNTHETIC_STRUCTURE"
    assert audit.empirical_data_collected is False
    assert audit.evidence_admissibility == "STRUCTURAL_QA_ONLY"
    assert audit.epistemic_co_agency == "NOT_ESTABLISHED"
    assert audit.distributed_cognition_mechanism == "NOT_ESTABLISHED"
    assert audit.human_learning == "NOT_ESTABLISHED"
    assert audit.shared_mind == "NOT_ESTABLISHED"
    assert audit.shared_consciousness == "NOT_ESTABLISHED"
    assert audit.ai_subjectivity == "NOT_ESTABLISHED"
    assert audit.scientific_disposition.value == "HOLD"
    assert audit.canonical_effect == "NONE"
    assert audit.deployment is False


def test_core_profile_requires_substantive_reciprocity_but_not_research_infrastructure() -> None:
    manifest = CoConstructedThinkingSpaceManifest(
        space_id="ccts:synthetic:core",
        profile=ThinkingSpaceProfile.CORE_INTERACTION,
        problem_representation_sha256=digest("1"),
        contributions=(
            contribution("human", ContributionRole.HUMAN_OWNER, "2"),
            contribution("ai", ContributionRole.AI_COLLABORATOR, "3"),
        ),
        revision_edges=(
            RevisionEdge("human", "ai", RevisionRelation.REVISES),
            RevisionEdge("ai", "human", RevisionRelation.CHALLENGES),
        ),
        provenance_manifest_sha256=digest("4"),
        claim_boundary_sha256=digest("5"),
        authority_policy_sha256=digest("6"),
        rejected_branch_manifest_sha256=digest("7"),
    )
    audit = audit_co_constructed_thinking_space(manifest)
    assert audit.reciprocal_human_ai_revision is True
    assert audit.revision_graph_connected is True
    assert audit.research_profile_complete is False
    assert audit.external_evidence_present is False
    assert audit.repository_artifact_present is False
    assert audit.implementation_evidence_present is False
    assert audit.longitudinal_bindings_present is False


def test_clarification_only_edges_do_not_satisfy_substantive_reciprocity() -> None:
    manifest = research_manifest()
    edges = tuple(
        RevisionEdge(edge.source_id, edge.target_id, RevisionRelation.CLARIFIES)
        if {edge.source_id, edge.target_id} == {"human", "ai"}
        else edge
        for edge in manifest.revision_edges
    )
    with pytest.raises(StudyError, match="REVISES or CHALLENGES"):
        audit_co_constructed_thinking_space(replace(manifest, revision_edges=edges))


def test_one_way_interaction_is_not_co_construction() -> None:
    manifest = research_manifest()
    edges = tuple(
        edge
        for edge in manifest.revision_edges
        if not (edge.source_id == "ai" and edge.target_id == "human")
    )
    with pytest.raises(StudyError, match="reciprocal Human<->AI"):
        audit_co_constructed_thinking_space(replace(manifest, revision_edges=edges))


def test_disconnected_declared_role_is_not_mediation() -> None:
    manifest = research_manifest()
    edges = tuple(
        edge
        for edge in manifest.revision_edges
        if edge.source_id != "evidence" and edge.target_id != "evidence"
    )
    with pytest.raises(StudyError, match="connected revision graph"):
        audit_co_constructed_thinking_space(replace(manifest, revision_edges=edges))


def test_longitudinal_profile_requires_external_repository_and_implementation_roles() -> None:
    manifest = research_manifest()
    for missing_role, match in (
        (ContributionRole.EXTERNAL_EVIDENCE, "external evidence"),
        (ContributionRole.REPOSITORY_ARTIFACT, "repository artifact"),
        (ContributionRole.IMPLEMENTATION_EVIDENCE, "implementation evidence"),
    ):
        contributions = tuple(
            item for item in manifest.contributions if item.role is not missing_role
        )
        known = {item.contribution_id for item in contributions}
        edges = tuple(
            edge
            for edge in manifest.revision_edges
            if edge.source_id in known and edge.target_id in known
        )
        with pytest.raises(StudyError, match=match):
            audit_co_constructed_thinking_space(
                replace(manifest, contributions=contributions, revision_edges=edges)
            )


def test_longitudinal_profile_requires_persistent_artifact_and_reentry_bindings() -> None:
    with pytest.raises(StudyError, match="persistent artifact and re-entry"):
        audit_co_constructed_thinking_space(
            replace(research_manifest(), reentry_binding_sha256=None)
        )


@pytest.mark.parametrize(
    "field,match",
    [
        ("persistent_artifact_sha256", "persistent artifact binding must match"),
        ("reentry_binding_sha256", "re-entry binding must match"),
    ],
)
def test_longitudinal_bindings_must_resolve_to_declared_repository_artifacts(
    field: str,
    match: str,
) -> None:
    with pytest.raises(StudyError, match=match):
        audit_co_constructed_thinking_space(
            replace(research_manifest(), **{field: digest("d")})
        )


def test_revision_edges_fail_closed_on_self_or_unknown_targets() -> None:
    with pytest.raises(StudyError, match="cannot target itself"):
        RevisionEdge("human", "human", RevisionRelation.REVISES)

    manifest = research_manifest()
    with pytest.raises(StudyError, match="known contributions"):
        replace(
            manifest,
            revision_edges=manifest.revision_edges
            + (RevisionEdge("human", "unknown", RevisionRelation.REVISES),),
        )


def test_duplicate_contribution_ids_and_structural_binding_aliases_fail_closed() -> None:
    manifest = research_manifest()
    duplicate = contribution("human", ContributionRole.EXTERNAL_EVIDENCE, "d")
    with pytest.raises(StudyError, match="contribution ids must be unique"):
        replace(manifest, contributions=manifest.contributions + (duplicate,))

    with pytest.raises(StudyError, match="content-distinct"):
        replace(
            manifest,
            claim_boundary_sha256=manifest.provenance_manifest_sha256,
        )

    with pytest.raises(StudyError, match="longitudinal bindings"):
        replace(
            manifest,
            reentry_binding_sha256=manifest.persistent_artifact_sha256,
        )


@pytest.mark.parametrize(
    "field,value,match",
    [
        ("synthetic", False, "synthetic structural manifests"),
        ("model_invoked", True, "model or human observations"),
        ("human_participant_observed", True, "model or human observations"),
        ("contains_human_identity", True, "identity and private material"),
        ("contains_private_material", True, "identity and private material"),
        ("asserts_shared_mind", True, "shared mind"),
        ("asserts_shared_consciousness", True, "shared mind"),
        ("asserts_ai_subjectivity_from_structure", True, "shared mind"),
        ("problem_representation_sha256", "not-a-digest", "SHA-256"),
    ],
)
def test_empirical_privacy_ontological_and_digest_boundaries_fail_closed(
    field: str,
    value: object,
    match: str,
) -> None:
    with pytest.raises(StudyError, match=match):
        replace(research_manifest(), **{field: value})


def test_raw_enum_values_are_rejected() -> None:
    with pytest.raises(StudyError, match="exact ThinkingSpaceProfile"):
        replace(
            research_manifest(),
            profile="LONGITUDINAL_REPOSITORY_RESEARCH",
        )
    with pytest.raises(StudyError, match="exact ContributionRole"):
        contribution("raw", "HUMAN_OWNER", "d")  # type: ignore[arg-type]
    with pytest.raises(StudyError, match="exact RevisionRelation"):
        RevisionEdge("human", "ai", "REVISES")  # type: ignore[arg-type]
