from __future__ import annotations

from dataclasses import replace
from hashlib import sha256

import pytest

from aion_human_ai_longitudinal import StudyError
from aion_human_ai_longitudinal.ccts_epistemic_challenge import (
    ConceptualRevisionTrace,
    EpistemicChallengeProfile,
    EpistemicChallengeRecord,
    EpistemicChallengeType,
    RevisionDisposition,
    audit_ccts_epistemic_challenge,
)
from aion_human_ai_longitudinal.co_constructed_thinking_space import (
    CoConstructedThinkingSpaceManifest,
    ContributionRole,
    EpistemicContribution,
    GroundingCheckpoint,
    GroundingDisposition,
    RevisionEdge,
    RevisionRelation,
    ThinkingSpaceProfile,
)
from aion_human_ai_longitudinal.task_selection_exposure import BoundArtifact


def artifact(artifact_id: str, text: str) -> BoundArtifact:
    return BoundArtifact(
        artifact_id=artifact_id,
        content_utf8=text,
        sha256_digest=sha256(text.encode("utf-8")).hexdigest(),
    )


def contribution(
    contribution_id: str,
    role: ContributionRole,
    item: BoundArtifact,
) -> EpistemicContribution:
    return EpistemicContribution(
        contribution_id=contribution_id,
        role=role,
        payload_sha256=item.sha256_digest,
    )


def research_manifest() -> tuple[
    CoConstructedThinkingSpaceManifest,
    dict[str, BoundArtifact],
]:
    items = {
        "problem": artifact("problem", "synthetic prior problem representation"),
        "human": artifact("human", "synthetic Human contribution"),
        "ai": artifact("ai", "synthetic AI contribution"),
        "evidence": artifact("evidence", "synthetic external evidence"),
        "implementation": artifact(
            "implementation", "synthetic implementation evidence"
        ),
        "repository": artifact("repository", "synthetic persistent repository artifact"),
        "reentry": artifact("reentry", "synthetic re-entry repository artifact"),
        "provenance": artifact("provenance", "synthetic provenance manifest"),
        "claim": artifact("claim", "synthetic claim ceiling"),
        "authority": artifact("authority", "synthetic authority policy"),
        "rejected": artifact("rejected", "synthetic rejected branches"),
    }
    contributions = (
        contribution("human", ContributionRole.HUMAN_OWNER, items["human"]),
        contribution("ai", ContributionRole.AI_COLLABORATOR, items["ai"]),
        contribution(
            "evidence", ContributionRole.EXTERNAL_EVIDENCE, items["evidence"]
        ),
        contribution(
            "implementation",
            ContributionRole.IMPLEMENTATION_EVIDENCE,
            items["implementation"],
        ),
        contribution(
            "repository", ContributionRole.REPOSITORY_ARTIFACT, items["repository"]
        ),
        contribution("reentry", ContributionRole.REPOSITORY_ARTIFACT, items["reentry"]),
    )
    manifest = CoConstructedThinkingSpaceManifest(
        space_id="ccts:synthetic:adversarial-review",
        profile=ThinkingSpaceProfile.LONGITUDINAL_REPOSITORY_RESEARCH,
        problem_representation_sha256=items["problem"].sha256_digest,
        grounding_checkpoint=GroundingCheckpoint(
            problem_representation_sha256=items["problem"].sha256_digest,
            human_contribution_id="human",
            ai_contribution_id="ai",
            disposition=GroundingDisposition.SUFFICIENT_FOR_CURRENT_PURPOSE,
            unresolved_mismatch=False,
        ),
        contributions=contributions,
        revision_edges=(
            RevisionEdge("human", "ai", RevisionRelation.CHALLENGES),
            RevisionEdge("ai", "human", RevisionRelation.CHALLENGES),
            RevisionEdge("evidence", "ai", RevisionRelation.REVISES),
            RevisionEdge("repository", "human", RevisionRelation.CLARIFIES),
            RevisionEdge("reentry", "ai", RevisionRelation.CLARIFIES),
            RevisionEdge("implementation", "human", RevisionRelation.CHALLENGES),
        ),
        provenance_manifest_sha256=items["provenance"].sha256_digest,
        claim_boundary_sha256=items["claim"].sha256_digest,
        authority_policy_sha256=items["authority"].sha256_digest,
        rejected_branch_manifest_sha256=items["rejected"].sha256_digest,
        persistent_artifact_sha256=items["repository"].sha256_digest,
        reentry_binding_sha256=items["reentry"].sha256_digest,
    )
    return manifest, items


def challenge(
    challenge_id: str,
    challenge_type: EpistemicChallengeType,
    *,
    source: str = "human",
    target: str = "ai",
) -> EpistemicChallengeRecord:
    return EpistemicChallengeRecord(
        challenge_id=challenge_id,
        source_contribution_id=source,
        target_contribution_id=target,
        challenge_type=challenge_type,
        challenge_artifact=artifact(
            f"challenge:{challenge_id}",
            f"synthetic {challenge_type.value} challenge {challenge_id}",
        ),
        linked_evidence_artifact=artifact(
            f"evidence:{challenge_id}",
            f"synthetic linked evidence for {challenge_id}",
        ),
    )


def high_rigor_trace() -> ConceptualRevisionTrace:
    manifest, items = research_manifest()
    return ConceptualRevisionTrace(
        trace_id="trace:synthetic:challenge",
        profile=EpistemicChallengeProfile.RESEARCH_ADVERSARIAL_REVIEW,
        ccts_manifest=manifest,
        prior_problem_model=items["problem"],
        challenges=(
            challenge("counter", EpistemicChallengeType.COUNTEREVIDENCE),
            challenge("assumption", EpistemicChallengeType.HIDDEN_ASSUMPTION),
            challenge(
                "alternative",
                EpistemicChallengeType.ALTERNATIVE_EXPLANATION,
                source="ai",
                target="human",
            ),
            challenge(
                "falsifier",
                EpistemicChallengeType.FALSIFIER,
                source="ai",
                target="human",
            ),
            challenge("grounding", EpistemicChallengeType.GROUNDING_CHALLENGE),
            challenge("bypass", EpistemicChallengeType.BYPASS_ANALYSIS),
        ),
        disposition=RevisionDisposition.REVISE,
        revised_problem_model=artifact(
            "revised-model", "synthetic revised problem representation"
        ),
        anomalous_evidence=artifact(
            "anomaly", "synthetic anomalous evidence that challenges the prior model"
        ),
        conflict_acknowledged=True,
        surviving_claims=artifact(
            "surviving", "synthetic claims that survived adversarial review"
        ),
        rejected_branches=items["rejected"],
        unresolved_alternatives=artifact(
            "unresolved", "synthetic unresolved alternative explanations"
        ),
        claim_ceiling=items["claim"],
    )


def test_high_rigor_trace_binds_challenge_and_revision_without_scientific_promotion() -> None:
    audit = audit_ccts_epistemic_challenge(high_rigor_trace())

    assert audit.profile is EpistemicChallengeProfile.RESEARCH_ADVERSARIAL_REVIEW
    assert audit.challenge_count == 6
    assert audit.challenge_edges_bound is True
    assert audit.bidirectional_human_ai_challenge is True
    assert audit.evidence_attack_present is True
    assert audit.assumption_attack_present is True
    assert audit.alternative_model_present is True
    assert audit.falsifier_present is True
    assert audit.grounding_or_scope_challenge_present is True
    assert audit.conceptual_revision_bound is True
    assert audit.rejected_branch_bound is True
    assert audit.unresolved_alternatives_bound is True
    assert audit.claim_ceiling_bound is True
    assert audit.mode == "DETERMINISTIC_SYNTHETIC_STRUCTURE"
    assert audit.empirical_data_collected is False
    assert audit.conceptual_change_mechanism == "NOT_ESTABLISHED"
    assert audit.cognitive_conflict_state == "NOT_ESTABLISHED"
    assert audit.transformative_learning == "NOT_ESTABLISHED"
    assert audit.human_learning == "NOT_ESTABLISHED"
    assert audit.ccts_causal_effect == "NOT_ESTABLISHED"
    assert audit.ai_subjectivity == "NOT_ESTABLISHED"
    assert audit.scientific_disposition.value == "HOLD"
    assert audit.canonical_effect == "NONE"
    assert audit.deployment is False


@pytest.mark.parametrize(
    "missing_type,match",
    [
        (EpistemicChallengeType.COUNTEREVIDENCE, "evidence attack"),
        (EpistemicChallengeType.HIDDEN_ASSUMPTION, "assumption attack"),
        (EpistemicChallengeType.ALTERNATIVE_EXPLANATION, "alternative explanation"),
        (EpistemicChallengeType.FALSIFIER, "falsifier"),
        (EpistemicChallengeType.GROUNDING_CHALLENGE, "grounding/research-necessity"),
    ],
)
def test_high_rigor_profile_fails_closed_when_required_challenge_family_is_missing(
    missing_type: EpistemicChallengeType,
    match: str,
) -> None:
    trace = high_rigor_trace()
    challenges = tuple(
        item
        for item in trace.challenges
        if item.challenge_type is not missing_type
        and not (
            missing_type is EpistemicChallengeType.ALTERNATIVE_EXPLANATION
            and item.challenge_type is EpistemicChallengeType.BYPASS_ANALYSIS
        )
    )
    with pytest.raises(StudyError, match=match):
        audit_ccts_epistemic_challenge(replace(trace, challenges=challenges))


def test_high_rigor_profile_requires_bidirectional_human_ai_challenge() -> None:
    trace = high_rigor_trace()
    one_way = tuple(
        replace(item, source_contribution_id="human", target_contribution_id="ai")
        for item in trace.challenges
    )
    with pytest.raises(StudyError, match="bidirectional"):
        audit_ccts_epistemic_challenge(replace(trace, challenges=one_way))


def test_challenge_record_must_bind_exact_ccts_challenges_edge() -> None:
    trace = high_rigor_trace()
    unbound = replace(
        trace.challenges[0],
        source_contribution_id="evidence",
        target_contribution_id="ai",
    )
    with pytest.raises(StudyError, match="exact CCTS CHALLENGES edge"):
        audit_ccts_epistemic_challenge(
            replace(trace, challenges=(unbound,) + trace.challenges[1:])
        )


def test_revision_disposition_requires_acknowledged_conflict_and_new_problem_model() -> None:
    trace = high_rigor_trace()

    with pytest.raises(StudyError, match="acknowledged conflict"):
        replace(trace, conflict_acknowledged=False)

    with pytest.raises(StudyError, match="require a revised problem model"):
        replace(trace, revised_problem_model=None)

    with pytest.raises(StudyError, match="content-distinct"):
        replace(trace, revised_problem_model=trace.prior_problem_model)


def test_retain_and_hold_cannot_claim_structural_revision() -> None:
    trace = high_rigor_trace()
    with pytest.raises(StudyError, match="RETAIN/HOLD"):
        replace(trace, disposition=RevisionDisposition.HOLD)

    retained = replace(
        trace,
        disposition=RevisionDisposition.RETAIN,
        revised_problem_model=None,
        conflict_acknowledged=False,
    )
    audit = audit_ccts_epistemic_challenge(retained)
    assert audit.conceptual_revision_bound is False


def test_problem_rejected_branch_and_claim_ceiling_bindings_fail_closed() -> None:
    trace = high_rigor_trace()

    with pytest.raises(StudyError, match="prior problem model"):
        replace(trace, prior_problem_model=artifact("other-problem", "different problem"))

    with pytest.raises(StudyError, match="rejected branches"):
        replace(
            trace,
            rejected_branches=artifact("other-rejected", "different rejected branches"),
        )

    with pytest.raises(StudyError, match="claim ceiling"):
        replace(trace, claim_ceiling=artifact("other-claim", "different claim ceiling"))


def test_privacy_empirical_and_raw_enum_boundaries_fail_closed() -> None:
    trace = high_rigor_trace()

    with pytest.raises(StudyError, match="synthetic"):
        replace(trace, synthetic=False)

    with pytest.raises(StudyError, match="model or human observations"):
        replace(trace, human_participant_observed=True)

    with pytest.raises(StudyError, match="identity and private material"):
        replace(trace, contains_private_material=True)

    with pytest.raises(StudyError, match="exact EpistemicChallengeProfile"):
        replace(trace, profile="RESEARCH_ADVERSARIAL_REVIEW")  # type: ignore[arg-type]

    with pytest.raises(StudyError, match="exact RevisionDisposition"):
        replace(trace, disposition="REVISE")  # type: ignore[arg-type]

    with pytest.raises(StudyError, match="exact EpistemicChallengeType"):
        replace(
            trace.challenges[0],
            challenge_type="COUNTEREVIDENCE",  # type: ignore[arg-type]
        )
