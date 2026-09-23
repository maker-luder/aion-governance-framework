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
from aion_human_ai_longitudinal.epistemic_revision import (
    ConceptualRevisionTrace,
    EpistemicChallengeType,
    EpistemicRevisionAudit,
    RevisionDisposition,
    audit_ccts_epistemic_revision_loop,
)
from aion_human_ai_longitudinal.harness import AdmissionDisposition, StudyError


def h(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()


PROBLEM = "synthetic problem representation"
CLAIM_CEILING = "structural revision trace only; no human-learning or subjectivity claim"
REJECTED = "rejected branch register for the synthetic CCTS challenge profile"

BYPASS_PRIOR = "generic resource availability is the primary bottleneck"
BYPASS_CHALLENGE = (
    "test whether substitution, decomposition, or trust-network paths bypass "
    "the claimed bottleneck"
)
BYPASS_REVISED = "specialized expertise plus trust and verification remain residual constraints"

GROUNDING_PRIOR = (
    "experimental grounding requires a naturally isomorphic biological referent"
)
GROUNDING_CHALLENGE = (
    "test whether engineered and sensorimotor controls can ground "
    "non-innate morphology research"
)
GROUNDING_REVISED = (
    "biological isomorphism is one grounding route; engineered, experimental, "
    "and sensorimotor bindings may also support bounded study designs"
)


def manifest() -> CoConstructedThinkingSpaceManifest:
    return CoConstructedThinkingSpaceManifest(
        space_id="synthetic-ccts-epistemic-revision",
        profile=ThinkingSpaceProfile.CORE_INTERACTION,
        problem_representation_sha256=h(PROBLEM),
        grounding_checkpoint=GroundingCheckpoint(
            problem_representation_sha256=h(PROBLEM),
            human_contribution_id="human-prior-grounding",
            ai_contribution_id="ai-prior-bypass",
            disposition=GroundingDisposition.SUFFICIENT_FOR_CURRENT_PURPOSE,
            unresolved_mismatch=False,
        ),
        contributions=(
            EpistemicContribution(
                contribution_id="human-challenge-bypass",
                role=ContributionRole.HUMAN_OWNER,
                payload_sha256=h(BYPASS_CHALLENGE),
            ),
            EpistemicContribution(
                contribution_id="ai-prior-bypass",
                role=ContributionRole.AI_COLLABORATOR,
                payload_sha256=h(BYPASS_PRIOR),
            ),
            EpistemicContribution(
                contribution_id="ai-revised-bypass",
                role=ContributionRole.AI_COLLABORATOR,
                payload_sha256=h(BYPASS_REVISED),
            ),
            EpistemicContribution(
                contribution_id="ai-challenge-grounding",
                role=ContributionRole.AI_COLLABORATOR,
                payload_sha256=h(GROUNDING_CHALLENGE),
            ),
            EpistemicContribution(
                contribution_id="human-prior-grounding",
                role=ContributionRole.HUMAN_OWNER,
                payload_sha256=h(GROUNDING_PRIOR),
            ),
            EpistemicContribution(
                contribution_id="human-revised-grounding",
                role=ContributionRole.HUMAN_OWNER,
                payload_sha256=h(GROUNDING_REVISED),
            ),
        ),
        revision_edges=(
            RevisionEdge(
                source_id="human-challenge-bypass",
                target_id="ai-prior-bypass",
                relation=RevisionRelation.CHALLENGES,
            ),
            RevisionEdge(
                source_id="ai-prior-bypass",
                target_id="ai-revised-bypass",
                relation=RevisionRelation.REVISES,
            ),
            RevisionEdge(
                source_id="ai-revised-bypass",
                target_id="ai-challenge-grounding",
                relation=RevisionRelation.CLARIFIES,
            ),
            RevisionEdge(
                source_id="ai-challenge-grounding",
                target_id="human-prior-grounding",
                relation=RevisionRelation.CHALLENGES,
            ),
            RevisionEdge(
                source_id="human-prior-grounding",
                target_id="human-revised-grounding",
                relation=RevisionRelation.REVISES,
            ),
        ),
        provenance_manifest_sha256=h("provenance manifest"),
        claim_boundary_sha256=h(CLAIM_CEILING),
        authority_policy_sha256=h("authority policy"),
        rejected_branch_manifest_sha256=h(REJECTED),
    )

def trace(
    *,
    trace_id: str,
    source: str,
    target: str,
    revised_contribution_id: str,
    challenge_types: frozenset[EpistemicChallengeType],
    disposition: RevisionDisposition,
    prior: str,
    challenge: str,
    revised: str,
    evidence: tuple[str, ...] = (),
) -> ConceptualRevisionTrace:
    surviving = f"surviving claims:{trace_id}"
    alternatives = f"unresolved alternatives:{trace_id}"
    return ConceptualRevisionTrace(
        trace_id=trace_id,
        ccts_space_id="synthetic-ccts-epistemic-revision",
        problem_representation_sha256=h(PROBLEM),
        source_contribution_id=source,
        target_contribution_id=target,
        revised_contribution_id=revised_contribution_id,
        challenge_types=challenge_types,
        disposition=disposition,
        prior_model_text=prior,
        prior_model_sha256=h(prior),
        challenge_text=challenge,
        challenge_sha256=h(challenge),
        revised_model_text=revised,
        revised_model_sha256=h(revised),
        surviving_claims_text=surviving,
        surviving_claims_sha256=h(surviving),
        rejected_branches_text=REJECTED,
        rejected_branches_sha256=h(REJECTED),
        unresolved_alternatives_text=alternatives,
        unresolved_alternatives_sha256=h(alternatives),
        claim_ceiling_text=CLAIM_CEILING,
        claim_ceiling_sha256=h(CLAIM_CEILING),
        anomalous_evidence_sha256s=evidence,
    )


def revision_loop() -> tuple[ConceptualRevisionTrace, ...]:
    bypass = trace(
        trace_id="constraint-bypass",
        source="human-challenge-bypass",
        target="ai-prior-bypass",
        revised_contribution_id="ai-revised-bypass",
        challenge_types=frozenset(
            {
                EpistemicChallengeType.HIDDEN_ASSUMPTION,
                EpistemicChallengeType.BYPASS_ANALYSIS,
                EpistemicChallengeType.ALTERNATIVE_EXPLANATION,
            }
        ),
        disposition=RevisionDisposition.NARROW,
        prior=BYPASS_PRIOR,
        challenge=BYPASS_CHALLENGE,
        revised=BYPASS_REVISED,
    )
    grounding = trace(
        trace_id="synthetic-morphology-grounding",
        source="ai-challenge-grounding",
        target="human-prior-grounding",
        revised_contribution_id="human-revised-grounding",
        challenge_types=frozenset(
            {
                EpistemicChallengeType.COUNTEREVIDENCE,
                EpistemicChallengeType.GROUNDING_CHALLENGE,
                EpistemicChallengeType.RESEARCH_NECESSITY,
            }
        ),
        disposition=RevisionDisposition.REVISE,
        prior=GROUNDING_PRIOR,
        challenge=GROUNDING_CHALLENGE,
        revised=GROUNDING_REVISED,
        evidence=(
            h("synthetic evidence binding: supernumerary robotic limb study"),
            h("synthetic evidence binding: non-human virtual ear study"),
        ),
    )
    return (bypass, grounding)


def test_revision_loop_binds_reciprocal_challenge_without_psychology_claim() -> None:
    audit = audit_ccts_epistemic_revision_loop(manifest(), revision_loop())

    assert audit.trace_count == 2
    assert audit.reciprocal_challenge_bound is True
    assert audit.challenge_edges_bound is True
    assert audit.revision_edges_bound is True
    assert audit.graph_content_bound is True
    assert audit.adversarial_challenge_present is True
    assert audit.grounding_or_scope_challenge_present is True
    assert audit.conceptual_revision_trace_present is True
    assert audit.rejected_branch_content_bound is True
    assert audit.claim_ceiling_content_bound is True
    assert audit.unresolved_alternatives_explicit is True
    assert audit.human_conceptual_change == "NOT_ESTABLISHED"
    assert audit.cognitive_conflict == "NOT_ESTABLISHED"
    assert audit.schema_accommodation == "NOT_ESTABLISHED"
    assert audit.transformative_learning == "NOT_ESTABLISHED"
    assert audit.threshold_concept == "NOT_ESTABLISHED"
    assert audit.human_learning == "NOT_ESTABLISHED"
    assert audit.ccts_causal_effect == "NOT_ESTABLISHED"
    assert audit.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert audit.consciousness_conclusion == "NOT_ESTABLISHED"
    assert audit.phenomenal_experience_conclusion == "NOT_ESTABLISHED"
    assert audit.scientific_disposition is AdmissionDisposition.HOLD
    assert audit.canonical_effect == "NONE"
    assert audit.deployment is False


def test_trace_must_bind_existing_ccts_challenge_edge() -> None:
    items = list(revision_loop())
    items[0] = replace(
        items[0],
        source_contribution_id="human-challenge-bypass",
        target_contribution_id="ai-challenge-grounding",
    )
    with pytest.raises(StudyError, match="CHALLENGES revision edge"):
        audit_ccts_epistemic_revision_loop(manifest(), tuple(items))


def test_trace_must_bind_existing_target_to_revised_edge() -> None:
    items = list(revision_loop())
    items[0] = replace(
        items[0],
        revised_contribution_id="human-revised-grounding",
    )
    with pytest.raises(StudyError, match="target-to-revised CCTS REVISES edge"):
        audit_ccts_epistemic_revision_loop(manifest(), tuple(items))


def test_graph_content_binding_rejects_payload_alias() -> None:
    current = manifest()
    contributions = tuple(
        replace(item, payload_sha256=h("wrong challenge"))
        if item.contribution_id == "human-challenge-bypass"
        else item
        for item in current.contributions
    )
    with pytest.raises(StudyError, match="challenge content"):
        audit_ccts_epistemic_revision_loop(
            replace(current, contributions=contributions),
            revision_loop(),
        )


def test_evidence_bound_challenge_requires_evidence_binding() -> None:
    with pytest.raises(StudyError, match="require anomalous evidence"):
        replace(revision_loop()[1], anomalous_evidence_sha256s=())


def test_model_change_disposition_requires_distinct_revised_model() -> None:
    item = revision_loop()[0]
    with pytest.raises(StudyError, match="content-distinct revised model"):
        replace(
            item,
            revised_model_text=item.prior_model_text,
            revised_model_sha256=item.prior_model_sha256,
        )


def test_retain_requires_unchanged_model() -> None:
    item = revision_loop()[0]
    with pytest.raises(StudyError, match="RETAIN requires identical"):
        replace(item, disposition=RevisionDisposition.RETAIN)


def test_verified_content_addresses_fail_closed() -> None:
    with pytest.raises(StudyError, match="prior_model_sha256 must match"):
        replace(revision_loop()[0], prior_model_sha256="0" * 64)


def test_claim_ceiling_and_rejected_branch_must_bind_ccts_manifest() -> None:
    items = list(revision_loop())
    wrong_ceiling = "different claim ceiling"
    items[0] = replace(
        items[0],
        claim_ceiling_text=wrong_ceiling,
        claim_ceiling_sha256=h(wrong_ceiling),
    )
    with pytest.raises(StudyError, match="claim-ceiling content"):
        audit_ccts_epistemic_revision_loop(manifest(), tuple(items))

    items = list(revision_loop())
    wrong_rejected = "different rejected branch register"
    items[0] = replace(
        items[0],
        rejected_branches_text=wrong_rejected,
        rejected_branches_sha256=h(wrong_rejected),
    )
    with pytest.raises(StudyError, match="rejected-branch content"):
        audit_ccts_epistemic_revision_loop(manifest(), tuple(items))


def test_private_identity_and_empirical_observation_flags_fail_closed() -> None:
    item = revision_loop()[0]
    for field, value, match in (
        ("synthetic", False, "synthetic revision traces only"),
        ("model_invoked", True, "cannot contain model or human observations"),
        ("human_participant_observed", True, "cannot contain model or human observations"),
        ("contains_human_identity", True, "human identity"),
        ("contains_private_material", True, "private material"),
    ):
        with pytest.raises(StudyError, match=match):
            replace(item, **{field: value})


def test_challenge_type_and_disposition_reject_raw_strings() -> None:
    item = revision_loop()[0]
    with pytest.raises(StudyError, match="exact EpistemicChallengeType"):
        replace(item, challenge_types=frozenset({"BYPASS_ANALYSIS"}))
    with pytest.raises(StudyError, match="exact RevisionDisposition"):
        replace(item, disposition="REVISE")

def test_audit_receipt_fails_closed_on_forged_boundary_state() -> None:
    audit = audit_ccts_epistemic_revision_loop(manifest(), revision_loop())

    with pytest.raises(StudyError, match="structural audit flags"):
        replace(audit, reciprocal_challenge_bound=False)
    with pytest.raises(StudyError, match="scientific_disposition"):
        replace(audit, scientific_disposition=AdmissionDisposition.ADMIT)
    with pytest.raises(StudyError, match="canonical_effect"):
        replace(audit, canonical_effect="PROMOTE")
    with pytest.raises(StudyError, match="deployment"):
        replace(audit, deployment=True)

    with pytest.raises(StudyError, match="trace_count"):
        EpistemicRevisionAudit(
            trace_count=0,
            reciprocal_challenge_bound=True,
            challenge_edges_bound=True,
            revision_edges_bound=True,
            graph_content_bound=True,
            adversarial_challenge_present=True,
            grounding_or_scope_challenge_present=True,
            conceptual_revision_trace_present=True,
            rejected_branch_content_bound=True,
            claim_ceiling_content_bound=True,
            unresolved_alternatives_explicit=True,
        )
