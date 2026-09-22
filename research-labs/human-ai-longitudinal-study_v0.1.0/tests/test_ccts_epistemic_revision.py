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


def manifest(
    space_id: str = "synthetic-ccts-revision",
    attack_payloads: dict[str, str] | None = None,
) -> CoConstructedThinkingSpaceManifest:
    problem = digest(f"{space_id}:problem")
    attack_payloads = attack_payloads or {
        "attack:default": "attack-artifact:default"
    }
    attack_contributions = tuple(
        EpistemicContribution(
            contribution_id=contribution_id,
            role=ContributionRole.EXTERNAL_EVIDENCE,
            payload_sha256=digest(text),
        )
        for contribution_id, text in attack_payloads.items()
    )
    attack_edges = tuple(
        RevisionEdge(
            source_id=contribution_id,
            target_id="human",
            relation=RevisionRelation.CLARIFIES,
        )
        for contribution_id in attack_payloads
    )
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
            *attack_contributions,
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
            *attack_edges,
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
    trajectory_id: str = "synthetic-trajectory-001",
    step_index: int = 0,
    prior: str = "initial working model",
    revised: str = "revised working model",
    rejected_branch: bool = True,
    alternative: bool = False,
    bypass: bool = False,
    falsifier: bool = False,
    attack_contribution_id: str | None = None,
) -> CCTSEpistemicChallengeTrace:
    if disposition is EpistemicRevisionDisposition.RETAIN:
        revised = prior
    attack_text = f"attack-artifact:{trace_id}"
    attack_id = attack_contribution_id or f"attack:{trace_id}"
    if ccts_manifest is None:
        ccts_manifest = manifest(
            f"synthetic-space:{trace_id}",
            {attack_id: attack_text},
        )
    challenger_id = (
        "human"
        if challenger is ContributionRole.HUMAN_OWNER
        else "ai"
    )
    target_id = (
        "human"
        if target is ContributionRole.HUMAN_OWNER
        else "ai"
    )
    return CCTSEpistemicChallengeTrace(
        trace_id=trace_id,
        trajectory_id=trajectory_id,
        step_index=step_index,
        ccts_manifest=ccts_manifest,
        challenger_role=challenger,
        target_role=target,
        challenger_contribution_id=challenger_id,
        target_contribution_id=target_id,
        attack_contribution_id=attack_id,
        challenge_type=challenge_type,
        prior_model=bound(prior),
        challenge=bound(f"challenge:{trace_id}"),
        attack_artifact=bound(attack_text),
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
    attack_payloads = {
        "attack-human": "attack-artifact:human-bypass",
        "attack-ai": "attack-artifact:ai-alternative",
    }
    shared = manifest("synthetic-bypass-case", attack_payloads)
    middle_model = "the surviving constraint is narrower than raw resource volume"
    return (
        trace(
            trace_id="human-bypass",
            trajectory_id="bypass-trajectory",
            step_index=0,
            challenger=ContributionRole.HUMAN_OWNER,
            target=ContributionRole.AI_COLLABORATOR,
            challenge_type=EpistemicChallengeType.BYPASS_PATH,
            disposition=EpistemicRevisionDisposition.NARROW,
            ccts_manifest=shared,
            prior="a scalable resource is treated as the primary constraint",
            revised=middle_model,
            bypass=True,
            attack_contribution_id="attack-human",
        ),
        trace(
            trace_id="ai-alternative",
            trajectory_id="bypass-trajectory",
            step_index=1,
            challenger=ContributionRole.AI_COLLABORATOR,
            target=ContributionRole.HUMAN_OWNER,
            challenge_type=EpistemicChallengeType.ALTERNATIVE_EXPLANATION,
            disposition=EpistemicRevisionDisposition.REVISE,
            ccts_manifest=shared,
            prior=middle_model,
            revised="multiple interacting constraints remain plausible",
            alternative=True,
            attack_contribution_id="attack-ai",
        ),
    )


def grounding_revision_fixture() -> tuple[CCTSEpistemicChallengeTrace, ...]:
    attack_payloads = {
        "attack-human": "attack-artifact:human-grounding",
        "attack-ai": "attack-artifact:ai-counterexample",
    }
    shared = manifest("synthetic-grounding-case", attack_payloads)
    middle_model = (
        "grounding may be operationalized through explicit experimental mappings"
    )
    return (
        trace(
            trace_id="human-grounding",
            trajectory_id="grounding-trajectory",
            step_index=0,
            challenger=ContributionRole.HUMAN_OWNER,
            target=ContributionRole.AI_COLLABORATOR,
            challenge_type=EpistemicChallengeType.GROUNDING_CHALLENGE,
            disposition=EpistemicRevisionDisposition.REVISE,
            ccts_manifest=shared,
            prior="grounding requires one natural isomorphic reference",
            revised=middle_model,
            attack_contribution_id="attack-human",
        ),
        trace(
            trace_id="ai-counterexample",
            trajectory_id="grounding-trajectory",
            step_index=1,
            challenger=ContributionRole.AI_COLLABORATOR,
            target=ContributionRole.HUMAN_OWNER,
            challenge_type=EpistemicChallengeType.COUNTEREXAMPLE,
            disposition=EpistemicRevisionDisposition.NARROW,
            ccts_manifest=shared,
            prior=middle_model,
            revised=(
                "absence of a natural isomorph limits one grounding route "
                "but not every route"
            ),
            attack_contribution_id="attack-ai",
        ),
    )


def test_bypass_fixture_is_structural_only_and_preserves_nonclaims() -> None:
    audit = audit_ccts_epistemic_revision_loop(bypass_oriented_fixture())

    assert audit.trace_count == 2
    assert audit.trajectory_id == "bypass-trajectory"
    assert audit.reciprocal_human_ai_challenge is True
    assert audit.ccts_contract_bound is True
    assert audit.contribution_edge_bound is True
    assert audit.attack_provenance_bound is True
    assert audit.trajectory_order_bound is True
    assert audit.revision_lineage_bound is True
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
    assert audit.revision_lineage_bound is True
    assert EpistemicChallengeType.GROUNDING_CHALLENGE in audit.challenge_types_present
    assert EpistemicChallengeType.COUNTEREXAMPLE in audit.challenge_types_present
    assert audit.substantive_revision_present is True
    assert audit.conceptual_change == "NOT_ESTABLISHED"
    assert audit.human_learning == "NOT_ESTABLISHED"


def test_one_way_challenge_does_not_satisfy_epistemic_revision_loop() -> None:
    with pytest.raises(StudyError, match="reciprocal Human<->AI"):
        audit_ccts_epistemic_revision_loop((bypass_oriented_fixture()[0],))


def test_mixed_ccts_spaces_fail_closed() -> None:
    first, second = bypass_oriented_fixture()
    replacement_manifest = manifest(
        "different-space",
        {"attack-ai": "attack-artifact:ai-alternative"},
    )
    second = replace(second, ccts_manifest=replacement_manifest)
    with pytest.raises(StudyError, match="one CCTS space_id"):
        audit_ccts_epistemic_revision_loop((first, second))


def test_mixed_trajectory_ids_fail_closed() -> None:
    first, second = bypass_oriented_fixture()
    second = replace(second, trajectory_id="other-trajectory")
    with pytest.raises(StudyError, match="one trajectory_id"):
        audit_ccts_epistemic_revision_loop((first, second))


def test_noncontiguous_or_duplicate_steps_fail_closed() -> None:
    first, second = bypass_oriented_fixture()
    with pytest.raises(StudyError, match="contiguous"):
        audit_ccts_epistemic_revision_loop((first, replace(second, step_index=2)))
    with pytest.raises(StudyError, match="step_index values must be unique"):
        audit_ccts_epistemic_revision_loop((first, replace(second, step_index=0)))


def test_revision_lineage_must_chain_revised_to_next_prior() -> None:
    first, second = bypass_oriented_fixture()
    second = replace(second, prior_model=bound("unrelated prior model"))
    with pytest.raises(StudyError, match="revised-model to next prior-model"):
        audit_ccts_epistemic_revision_loop((first, second))


def test_trace_must_bind_real_ccts_contribution_edge() -> None:
    item = bypass_oriented_fixture()[0]
    with pytest.raises(StudyError, match="contribution ids must resolve"):
        replace(item, challenger_contribution_id="missing")
    with pytest.raises(StudyError, match="role does not match"):
        replace(
            item,
            challenger_contribution_id="ai",
        )


def test_attack_artifact_must_resolve_to_manifest_provenance() -> None:
    item = bypass_oriented_fixture()[0]
    with pytest.raises(StudyError, match="attack artifact must resolve"):
        replace(item, attack_artifact=bound("different attack artifact"))


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



@pytest.mark.parametrize("field", ["provenance_manifest_sha256", "authority_policy_sha256",
                                   "claim_boundary_sha256", "rejected_branch_manifest_sha256"])
def test_same_space_and_problem_cannot_hide_manifest_drift(field: str) -> None:
    first, second = bypass_oriented_fixture()
    changed = replace(second.ccts_manifest, **{field: digest("substituted binding")})
    second = replace(second, ccts_manifest=changed)
    with pytest.raises(StudyError, match="same CCTS manifest"):
        audit_ccts_epistemic_revision_loop((first, second))


def test_hold_cannot_mutate_model_without_preserving_rejected_branch() -> None:
    item = bypass_oriented_fixture()[0]
    with pytest.raises(StudyError, match="changed model requires"):
        replace(item, disposition=EpistemicRevisionDisposition.HOLD, rejected_branch=None)


def test_unchanged_hold_can_preserve_uncertainty_without_rejected_branch() -> None:
    item = bypass_oriented_fixture()[0]
    held = replace(item, disposition=EpistemicRevisionDisposition.HOLD,
                   revised_model=item.prior_model, rejected_branch=None)
    assert held.residual_uncertainty == item.residual_uncertainty
