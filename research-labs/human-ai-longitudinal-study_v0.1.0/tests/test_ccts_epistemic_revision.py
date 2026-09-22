from __future__ import annotations

from dataclasses import replace
from hashlib import sha256

import pytest

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
from aion_human_ai_longitudinal.ccts_epistemic_revision import (
    CCTSEpistemicChallengeTrace,
    ContentAddressedText,
    EpistemicChallengeType,
    EpistemicRevisionDisposition,
    audit_ccts_epistemic_revision_loop,
)
from aion_human_ai_longitudinal.harness import AdmissionDisposition, StudyError


def bound(text: str) -> ContentAddressedText:
    return ContentAddressedText(
        text=text,
        sha256_hex=sha256(text.encode("utf-8")).hexdigest(),
    )


def digest(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()


def manifest(space_id: str = "synthetic-ccts-revision") -> CoConstructedThinkingSpaceManifest:
    problem = digest(f"{space_id}:problem")
    return CoConstructedThinkingSpaceManifest(
        space_id=space_id,
        profile=ThinkingSpaceProfile.CORE_INTERACTION,
        problem_representation_sha256=problem,
        grounding_checkpoint=GroundingCheckpoint(
            problem_representation_sha256=problem,
            human_contribution_id="human",
            ai_contribution_id="ai",
            disposition=GroundingDisposition.SUFFICIENT_FOR_CURRENT_PURPOSE,
            unresolved_mismatch=False,
        ),
        contributions=(
            EpistemicContribution(
                contribution_id="human",
                role=ContributionRole.HUMAN_OWNER,
                payload_sha256=digest(f"{space_id}:human"),
            ),
            EpistemicContribution(
                contribution_id="ai",
                role=ContributionRole.AI_COLLABORATOR,
                payload_sha256=digest(f"{space_id}:ai"),
            ),
        ),
        revision_edges=(
            RevisionEdge(
                source_id="human",
                target_id="ai",
                relation=RevisionRelation.CHALLENGES,
            ),
            RevisionEdge(
                source_id="ai",
                target_id="human",
                relation=RevisionRelation.REVISES,
            ),
        ),
        provenance_manifest_sha256=digest(f"{space_id}:provenance"),
        claim_boundary_sha256=digest(f"{space_id}:claim"),
        authority_policy_sha256=digest(f"{space_id}:authority"),
        rejected_branch_manifest_sha256=digest(f"{space_id}:rejected"),
    )


def trace(
    *,
    trace_id: str,
    challenger: ContributionRole,
    target: ContributionRole,
    challenge_type: EpistemicChallengeType,
    disposition: EpistemicRevisionDisposition,
    ccts_manifest: CoConstructedThinkingSpaceManifest | None = None,
    prior: str = "initial working model",
    revised: str = "revised working model",
    rejected_branch: bool = True,
    alternative: bool = False,
    bypass: bool = False,
    falsifier: bool = False,
) -> CCTSEpistemicChallengeTrace:
    if disposition is EpistemicRevisionDisposition.RETAIN:
        revised = prior
    return CCTSEpistemicChallengeTrace(
        trace_id=trace_id,
        ccts_manifest=ccts_manifest or manifest(),
        challenger_role=challenger,
        target_role=target,
        challenge_type=challenge_type,
        prior_model=bound(prior),
        challenge=bound(f"challenge:{trace_id}"),
        attack_artifact=bound(f"attack-artifact:{trace_id}"),
        disposition=disposition,
        revised_model=bound(revised),
        residual_uncertainty=bound(f"residual-uncertainty:{trace_id}"),
        claim_ceiling=bound(f"claim-ceiling:{trace_id}"),
        rejected_branch=(
            bound(f"rejected-branch:{trace_id}") if rejected_branch else None
        ),
        alternative_explanation=(
            bound(f"alternative-explanation:{trace_id}") if alternative else None
        ),
        bypass_path=bound(f"bypass-path:{trace_id}") if bypass else None,
        falsifier=bound(f"falsifier:{trace_id}") if falsifier else None,
    )


def bypass_oriented_fixture() -> tuple[CCTSEpistemicChallengeTrace, ...]:
    shared = manifest("synthetic-bypass-case")
    return (
        trace(
            trace_id="human-bypass",
            challenger=ContributionRole.HUMAN_OWNER,
            target=ContributionRole.AI_COLLABORATOR,
            challenge_type=EpistemicChallengeType.BYPASS_PATH,
            disposition=EpistemicRevisionDisposition.NARROW,
            ccts_manifest=shared,
            prior="a scalable resource is treated as the primary constraint",
            revised="the surviving constraint is narrower than raw resource volume",
            bypass=True,
        ),
        trace(
            trace_id="ai-alternative",
            challenger=ContributionRole.AI_COLLABORATOR,
            target=ContributionRole.HUMAN_OWNER,
            challenge_type=EpistemicChallengeType.ALTERNATIVE_EXPLANATION,
            disposition=EpistemicRevisionDisposition.REVISE,
            ccts_manifest=shared,
            prior="the remaining constraint is treated as singular",
            revised="multiple interacting constraints remain plausible",
            alternative=True,
        ),
    )


def grounding_revision_fixture() -> tuple[CCTSEpistemicChallengeTrace, ...]:
    shared = manifest("synthetic-grounding-case")
    return (
        trace(
            trace_id="human-grounding",
            challenger=ContributionRole.HUMAN_OWNER,
            target=ContributionRole.AI_COLLABORATOR,
            challenge_type=EpistemicChallengeType.GROUNDING_CHALLENGE,
            disposition=EpistemicRevisionDisposition.REVISE,
            ccts_manifest=shared,
            prior="grounding requires one natural isomorphic reference",
            revised="grounding may be operationalized through explicit experimental mappings",
        ),
        trace(
            trace_id="ai-counterexample",
            challenger=ContributionRole.AI_COLLABORATOR,
            target=ContributionRole.HUMAN_OWNER,
            challenge_type=EpistemicChallengeType.COUNTEREXAMPLE,
            disposition=EpistemicRevisionDisposition.NARROW,
            ccts_manifest=shared,
            prior="absence of a natural isomorph rules out a grounded study object",
            revised="absence of a natural isomorph limits one grounding route but not every route",
        ),
    )


def test_bypass_fixture_is_structural_only_and_preserves_nonclaims() -> None:
    audit = audit_ccts_epistemic_revision_loop(bypass_oriented_fixture())

    assert audit.trace_count == 2
    assert audit.reciprocal_human_ai_challenge is True
    assert audit.ccts_contract_bound is True
    assert audit.verified_content_addressing is True
    assert audit.rejected_branch_preserved is True
    assert audit.substantive_revision_present is True
    assert EpistemicChallengeType.BYPASS_PATH in audit.challenge_types_present
    assert EpistemicChallengeType.ALTERNATIVE_EXPLANATION in audit.challenge_types_present
    assert audit.empirical_data_collected is False
    assert audit.evidence_admissibility == "STRUCTURAL_QA_ONLY"
    assert audit.adversarial_thinking_effect == "NOT_ESTABLISHED"
    assert audit.conceptual_change == "NOT_ESTABLISHED"
    assert audit.cognitive_conflict == "NOT_ESTABLISHED"
    assert audit.transformative_learning == "NOT_ESTABLISHED"
    assert audit.human_learning == "NOT_ESTABLISHED"
    assert audit.revision_correctness == "NOT_ESTABLISHED"
    assert audit.causal_effect == "NOT_ESTABLISHED"
    assert audit.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert audit.consciousness_conclusion == "NOT_ESTABLISHED"
    assert audit.phenomenal_experience_conclusion == "NOT_ESTABLISHED"
    assert audit.scientific_disposition is AdmissionDisposition.HOLD
    assert audit.canonical_effect == "NONE"
    assert audit.deployment is False


def test_grounding_fixture_records_model_revision_without_psychological_claim() -> None:
    audit = audit_ccts_epistemic_revision_loop(grounding_revision_fixture())

    assert audit.reciprocal_human_ai_challenge is True
    assert EpistemicChallengeType.GROUNDING_CHALLENGE in audit.challenge_types_present
    assert EpistemicChallengeType.COUNTEREXAMPLE in audit.challenge_types_present
    assert audit.substantive_revision_present is True
    assert audit.conceptual_change == "NOT_ESTABLISHED"
    assert audit.human_learning == "NOT_ESTABLISHED"


def test_one_way_challenge_does_not_satisfy_epistemic_revision_loop() -> None:
    with pytest.raises(StudyError, match="reciprocal Human<->AI"):
        audit_ccts_epistemic_revision_loop((bypass_oriented_fixture()[0],))


def test_mixed_ccts_spaces_fail_closed() -> None:
    first = bypass_oriented_fixture()[0]
    second = replace(
        bypass_oriented_fixture()[1],
        ccts_manifest=manifest("different-space"),
    )
    with pytest.raises(StudyError, match="one CCTS space_id"):
        audit_ccts_epistemic_revision_loop((first, second))


@pytest.mark.parametrize(
    "challenge_type,field,match",
    [
        (
            EpistemicChallengeType.BYPASS_PATH,
            "bypass_path",
            "BYPASS_PATH requires",
        ),
        (
            EpistemicChallengeType.ALTERNATIVE_EXPLANATION,
            "alternative_explanation",
            "ALTERNATIVE_EXPLANATION requires",
        ),
        (
            EpistemicChallengeType.FALSIFIER,
            "falsifier",
            "FALSIFIER requires",
        ),
    ],
)
def test_typed_challenges_require_typed_artifacts(
    challenge_type: EpistemicChallengeType,
    field: str,
    match: str,
) -> None:
    kwargs = {
        "trace_id": f"typed:{challenge_type.value}",
        "challenger": ContributionRole.HUMAN_OWNER,
        "target": ContributionRole.AI_COLLABORATOR,
        "challenge_type": challenge_type,
        "disposition": EpistemicRevisionDisposition.REVISE,
        "alternative": challenge_type is EpistemicChallengeType.ALTERNATIVE_EXPLANATION,
        "bypass": challenge_type is EpistemicChallengeType.BYPASS_PATH,
        "falsifier": challenge_type is EpistemicChallengeType.FALSIFIER,
    }
    item = trace(**kwargs)
    with pytest.raises(StudyError, match=match):
        replace(item, **{field: None})


def test_content_address_is_verified_from_text_not_shape_only() -> None:
    with pytest.raises(StudyError, match="must match"):
        ContentAddressedText(text="payload", sha256_hex="a" * 64)


def test_substantive_revision_requires_changed_model_and_rejected_branch() -> None:
    item = trace(
        trace_id="revision",
        challenger=ContributionRole.HUMAN_OWNER,
        target=ContributionRole.AI_COLLABORATOR,
        challenge_type=EpistemicChallengeType.COUNTEREXAMPLE,
        disposition=EpistemicRevisionDisposition.REVISE,
    )
    with pytest.raises(StudyError, match="content-distinct"):
        replace(item, revised_model=item.prior_model)
    with pytest.raises(StudyError, match="rejected-branch"):
        replace(item, rejected_branch=None)


def test_retain_cannot_silently_mutate_the_working_model() -> None:
    item = trace(
        trace_id="retain",
        challenger=ContributionRole.HUMAN_OWNER,
        target=ContributionRole.AI_COLLABORATOR,
        challenge_type=EpistemicChallengeType.EVIDENCE_SUFFICIENCY,
        disposition=EpistemicRevisionDisposition.RETAIN,
    )
    with pytest.raises(StudyError, match="RETAIN requires"):
        replace(item, revised_model=bound("silently changed model"))


@pytest.mark.parametrize(
    "field,value,match",
    [
        ("synthetic", False, "synthetic only"),
        ("model_invoked", True, "cannot contain model or human observations"),
        ("human_participant_observed", True, "cannot contain model or human observations"),
        ("contains_human_identity", True, "human identity"),
        ("contains_private_material", True, "private material"),
    ],
)
def test_empirical_and_privacy_boundaries_fail_closed(
    field: str,
    value: object,
    match: str,
) -> None:
    with pytest.raises(StudyError, match=match):
        replace(bypass_oriented_fixture()[0], **{field: value})


def test_raw_string_roles_types_and_dispositions_fail_closed() -> None:
    item = bypass_oriented_fixture()[0]
    with pytest.raises(StudyError, match="challenger_role"):
        replace(item, challenger_role="HUMAN_OWNER")
    with pytest.raises(StudyError, match="challenge_type"):
        replace(item, challenge_type="BYPASS_PATH")
    with pytest.raises(StudyError, match="disposition"):
        replace(item, disposition="REVISE")
