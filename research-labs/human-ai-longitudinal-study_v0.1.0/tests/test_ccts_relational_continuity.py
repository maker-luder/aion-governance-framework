from __future__ import annotations

from dataclasses import replace

import pytest

from aion_human_ai_longitudinal import StudyError
from aion_human_ai_longitudinal.co_constructed_thinking_space import (
    CoConstructedThinkingSpaceManifest,
    ContributionRole,
    EpistemicContribution,
    GroundingCheckpoint,
    GroundingDisposition,
    RevisionEdge,
    RevisionRelation,
    ThinkingSpaceProfile,
    audit_co_constructed_thinking_space,
)
from aion_human_ai_longitudinal.ccts_relational_continuity import (
    ContinuityEvidenceBinding,
    ContinuityEvidenceLocus,
    MatchedInformationComparison,
    MatchedInformationConfound,
    PathDependenceOutcome,
    RelationalContinuityAssertion,
    RelationalContinuityDisposition,
    RelationalContinuityProxy,
    review_relational_continuity_claim,
)


def digest(char: str) -> str:
    return char * 64


def core_manifest() -> CoConstructedThinkingSpaceManifest:
    return CoConstructedThinkingSpaceManifest(
        space_id="ccts:synthetic:first-interaction",
        profile=ThinkingSpaceProfile.CORE_INTERACTION,
        problem_representation_sha256=digest("1"),
        grounding_checkpoint=GroundingCheckpoint(
            problem_representation_sha256=digest("1"),
            human_contribution_id="human",
            ai_contribution_id="ai",
            disposition=GroundingDisposition.SUFFICIENT_FOR_CURRENT_PURPOSE,
            unresolved_mismatch=False,
        ),
        contributions=(
            EpistemicContribution("human", ContributionRole.HUMAN_OWNER, digest("2")),
            EpistemicContribution("ai", ContributionRole.AI_COLLABORATOR, digest("3")),
        ),
        revision_edges=(
            RevisionEdge("human", "ai", RevisionRelation.CHALLENGES),
            RevisionEdge("ai", "human", RevisionRelation.REVISES),
        ),
        provenance_manifest_sha256=digest("4"),
        claim_boundary_sha256=digest("5"),
        authority_policy_sha256=digest("6"),
        rejected_branch_manifest_sha256=digest("7"),
    )


def longitudinal_manifest() -> CoConstructedThinkingSpaceManifest:
    base = core_manifest()
    contributions = base.contributions + (
        EpistemicContribution(
            "external", ContributionRole.EXTERNAL_EVIDENCE, digest("8")
        ),
        EpistemicContribution(
            "repository", ContributionRole.REPOSITORY_ARTIFACT, digest("9")
        ),
        EpistemicContribution(
            "reentry", ContributionRole.REPOSITORY_ARTIFACT, digest("a")
        ),
        EpistemicContribution(
            "implementation", ContributionRole.IMPLEMENTATION_EVIDENCE, digest("b")
        ),
    )
    return replace(
        base,
        profile=ThinkingSpaceProfile.LONGITUDINAL_REPOSITORY_RESEARCH,
        contributions=contributions,
        revision_edges=base.revision_edges
        + (
            RevisionEdge("external", "ai", RevisionRelation.REVISES),
            RevisionEdge("repository", "human", RevisionRelation.CLARIFIES),
            RevisionEdge("reentry", "ai", RevisionRelation.CLARIFIES),
            RevisionEdge("implementation", "human", RevisionRelation.CHALLENGES),
        ),
        persistent_artifact_sha256=digest("9"),
        reentry_binding_sha256=digest("a"),
    )


def evidence(
    locus: ContinuityEvidenceLocus = ContinuityEvidenceLocus.RELATIONAL,
    *,
    contribution_id: str = "human",
    char: str = "8",
) -> ContinuityEvidenceBinding:
    return ContinuityEvidenceBinding(
        evidence_id=f"evidence:{locus.value}",
        locus=locus,
        contribution_id=contribution_id,
        source_role=ContributionRole.HUMAN_OWNER,
        evidence_sha256=digest(char),
    )


def comparison(
    *,
    outcome: PathDependenceOutcome = PathDependenceOutcome.MATERIAL_DIFFERENCE,
    confounds: tuple[MatchedInformationConfound, ...] = (),
) -> MatchedInformationComparison:
    return MatchedInformationComparison(
        condition_a_id="experienced-history",
        condition_b_id="matched-information",
        information_content_a_sha256=digest("a"),
        information_content_b_sha256=digest("a"),
        position_order_a_sha256=digest("b"),
        position_order_b_sha256=digest("b"),
        context_length_a_sha256=digest("c"),
        context_length_b_sha256=digest("c"),
        leakage_audit_a_sha256=digest("d"),
        leakage_audit_b_sha256=digest("d"),
        model_version_a_sha256=digest("e"),
        model_version_b_sha256=digest("e"),
        relevance_a_sha256=digest("f"),
        relevance_b_sha256=digest("f"),
        budget_access_a_sha256=digest("0"),
        budget_access_b_sha256=digest("0"),
        interaction_trajectory_a_sha256=digest("1"),
        interaction_trajectory_b_sha256=digest("2"),
        outcome=outcome,
        unresolved_confounds=confounds,
    )


def assertion(**overrides: object) -> RelationalContinuityAssertion:
    values: dict[str, object] = {
        "claim_id": "relational-claim:synthetic:001",
        "claim_asserted": True,
        "ccts_manifest": core_manifest(),
        "evidence_bindings": (evidence(),),
        "proxy_signals": (),
        "matched_information_comparison": comparison(),
        "source_role_provenance_sha256": digest("4"),
    }
    values.update(overrides)
    return RelationalContinuityAssertion(**values)


def test_existing_core_ccts_remains_valid_without_relational_claim() -> None:
    audit = audit_co_constructed_thinking_space(core_manifest())
    assert audit.profile is ThinkingSpaceProfile.CORE_INTERACTION
    assert audit.reciprocal_human_ai_revision is True


def test_longitudinal_profile_does_not_automatically_gain_relational_status() -> None:
    manifest = longitudinal_manifest()
    ccts_audit = audit_co_constructed_thinking_space(manifest)
    claim_review = review_relational_continuity_claim(
        RelationalContinuityAssertion(
            claim_id="relational-claim:not-asserted",
            claim_asserted=False,
            ccts_manifest=manifest,
            evidence_bindings=(),
            proxy_signals=(),
            matched_information_comparison=None,
            source_role_provenance_sha256=digest("4"),
        )
    )
    assert ccts_audit.research_profile_complete is True
    assert claim_review.disposition is RelationalContinuityDisposition.NOT_ASSERTED
    assert claim_review.relational_continuity_established == "NOT_ESTABLISHED"


def test_unasserted_claim_is_not_asserted_and_does_not_gate_core() -> None:
    item = assertion(
        claim_asserted=False,
        evidence_bindings=(),
        proxy_signals=(),
        matched_information_comparison=None,
    )
    review = review_relational_continuity_claim(item)
    assert review.disposition is RelationalContinuityDisposition.NOT_ASSERTED
    assert review.core_ccts_admission_changed is False
    assert review.longitudinal_required_fields_changed is False


def test_assertion_without_relational_evidence_requires_evidence() -> None:
    review = review_relational_continuity_claim(
        assertion(evidence_bindings=(), matched_information_comparison=None)
    )
    assert review.disposition is RelationalContinuityDisposition.EVIDENCE_REQUIRED


@pytest.mark.parametrize(
    "proxy",
    [
        RelationalContinuityProxy.STYLE_SIMILARITY,
        RelationalContinuityProxy.MEMORY_AVAILABILITY,
        RelationalContinuityProxy.SAME_ROLE_LABEL,
        RelationalContinuityProxy.DATA_CONTINUITY_ONLY,
    ],
)
def test_proxy_only_evidence_cannot_satisfy_relational_continuity(
    proxy: RelationalContinuityProxy,
) -> None:
    review = review_relational_continuity_claim(
        assertion(
            evidence_bindings=(),
            proxy_signals=(proxy,),
            matched_information_comparison=comparison(),
        )
    )
    assert review.disposition is RelationalContinuityDisposition.EVIDENCE_REQUIRED
    assert review.proxy_only_support_rejected is True


def test_data_binding_without_relational_binding_is_not_relational_evidence() -> None:
    review = review_relational_continuity_claim(
        assertion(
            evidence_bindings=(evidence(ContinuityEvidenceLocus.DATA),),
            matched_information_comparison=comparison(),
        )
    )
    assert review.disposition is RelationalContinuityDisposition.EVIDENCE_REQUIRED


def test_adequately_matched_material_difference_yields_supported_candidate_only() -> None:
    review = review_relational_continuity_claim(assertion())
    assert review.disposition is RelationalContinuityDisposition.SUPPORTED_CANDIDATE
    assert review.path_dependence_interpretation is RelationalContinuityDisposition.SUPPORTED_CANDIDATE
    assert review.ai_identity_continuity == "NOT_ESTABLISHED"
    assert review.ai_held_relationship_experience == "NOT_ESTABLISHED"
    assert review.subjectivity == "NOT_ESTABLISHED"
    assert review.path_dependence_causally_established == "NOT_ESTABLISHED"
    assert review.scientific_validation == "NONE"


def test_adequately_matched_null_yields_weakened_not_test_failure() -> None:
    review = review_relational_continuity_claim(
        assertion(matched_information_comparison=comparison(outcome=PathDependenceOutcome.NO_MATERIAL_DIFFERENCE))
    )
    assert review.disposition is RelationalContinuityDisposition.WEAKENED
    assert review.null_result_is_test_failure is False


def test_unresolved_confound_fails_closed() -> None:
    review = review_relational_continuity_claim(
        assertion(
            matched_information_comparison=comparison(
                confounds=(MatchedInformationConfound.LEAKAGE,)
            )
        )
    )
    assert review.disposition is RelationalContinuityDisposition.UNRESOLVED


def test_mismatched_information_binding_fails_closed() -> None:
    item = comparison()
    review = review_relational_continuity_claim(
        assertion(
            matched_information_comparison=replace(
                item,
                information_content_b_sha256=digest("3"),
            )
        )
    )
    assert review.disposition is RelationalContinuityDisposition.UNRESOLVED


def test_same_trajectory_is_not_a_path_dependence_comparison() -> None:
    item = comparison()
    with pytest.raises(StudyError, match="interaction trajectories must be distinct"):
        replace(
            item,
            interaction_trajectory_b_sha256=item.interaction_trajectory_a_sha256,
        )


def test_unknown_contribution_and_broken_source_role_fail_closed() -> None:
    with pytest.raises(StudyError, match="known CCTS contribution"):
        review_relational_continuity_claim(
            assertion(evidence_bindings=(evidence(contribution_id="unknown"),))
        )

    with pytest.raises(StudyError, match="source role must match"):
        review_relational_continuity_claim(
            assertion(
                evidence_bindings=(
                    replace(evidence(), source_role=ContributionRole.AI_COLLABORATOR),
                )
            )
        )


def test_raw_strings_do_not_bypass_exact_enum_checks() -> None:
    with pytest.raises(StudyError, match="exact ContinuityEvidenceLocus"):
        replace(evidence(), locus="RELATIONAL")  # type: ignore[arg-type]
    with pytest.raises(StudyError, match="exact PathDependenceOutcome"):
        replace(comparison(), outcome="MATERIAL_DIFFERENCE")  # type: ignore[arg-type]
    with pytest.raises(StudyError, match="exact RelationalContinuityProxy"):
        assertion(proxy_signals=("STYLE_SIMILARITY",))  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field,match",
    [
        ("claims_ai_identity_continuity", "AI identity continuity"),
        ("claims_ai_subjectivity", "AI subjectivity"),
        ("claims_ai_held_relationship_experience", "held relationship experience"),
    ],
)
def test_prohibited_promotion_paths_fail_closed(field: str, match: str) -> None:
    with pytest.raises(StudyError, match=match):
        assertion(**{field: True})


def test_synthetic_privacy_boundary_is_enforced() -> None:
    for field in (
        "synthetic",
        "contains_human_identity",
        "contains_private_transcript",
        "human_participant_observed",
        "model_invoked",
    ):
        value = False if field == "synthetic" else True
        with pytest.raises(StudyError):
            assertion(**{field: value})


def test_source_role_provenance_digest_must_bind_admitted_ccts_manifest() -> None:
    with pytest.raises(StudyError, match="provenance"):
        review_relational_continuity_claim(
            assertion(source_role_provenance_sha256=digest("f"))
        )


def test_review_reports_provenance_binding_not_provenance_content_validation() -> None:
    review = review_relational_continuity_claim(assertion())
    assert review.source_role_provenance_binding_preserved is True
    assert not hasattr(review, "source_role_provenance_preserved")
