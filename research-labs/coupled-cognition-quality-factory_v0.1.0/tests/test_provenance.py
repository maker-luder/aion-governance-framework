import pytest

from aion_coupled_quality.provenance import (
    AIInteractionSurface,
    ActorClaim,
    ActorClaimSource,
    ActorExpectation,
    ClaimLayer,
    ContributionActor,
    ContributionFunction,
    ContributionOrigin,
    ContributionRecord,
    EpistemicProvenanceLedger,
    OperationalActorLabel,
    ProjectActorAnnotation,
    ProvenanceError,
    StateAttribution,
    verify_actor_claim,
)


def test_human_origin_requires_direct_source_reference() -> None:
    with pytest.raises(ProvenanceError):
        ContributionRecord(
            record_id="u1",
            proposition="human-originated research question",
            origin=ContributionOrigin.HUMAN_ORIGIN,
            layer=ClaimLayer.DIRECT_STATEMENT,
        )


def test_inferred_personal_state_cannot_be_rewritten_as_human_origin() -> None:
    with pytest.raises(ProvenanceError):
        ContributionRecord(
            record_id="u2",
            proposition="the user was shocked",
            origin=ContributionOrigin.HUMAN_ORIGIN,
            layer=ClaimLayer.INFERENCE,
            source_refs=("synthetic:input-post",),
            state_attribution=StateAttribution.INFERRED,
        )


def test_self_report_is_distinct_from_independent_measurement() -> None:
    ledger = EpistemicProvenanceLedger()
    ledger.add(
        ContributionRecord(
            record_id="u3",
            proposition="I am uncertain about this hypothesis",
            origin=ContributionOrigin.HUMAN_ORIGIN,
            layer=ClaimLayer.DIRECT_STATEMENT,
            source_refs=("synthetic:direct-statement",),
            state_attribution=StateAttribution.SELF_REPORTED,
        )
    )
    audit = ledger.audit("u3")
    assert audit.human_origin_admissible is True
    assert "SELF_REPORT_IS_ATTRIBUTED_REPORT_NOT_INDEPENDENT_MEASUREMENT" in audit.reasons


def test_external_source_requires_reference() -> None:
    with pytest.raises(ProvenanceError):
        ContributionRecord(
            record_id="e1",
            proposition="published research claim",
            origin=ContributionOrigin.EXTERNAL_SOURCE,
            layer=ClaimLayer.SOURCE_REPORT,
        )


def test_joint_synthesis_requires_traceable_human_and_ai_parents() -> None:
    ledger = EpistemicProvenanceLedger()
    ledger.add(
        ContributionRecord(
            record_id="human",
            proposition="Could the relevant property be system-relational rather than model-only?",
            origin=ContributionOrigin.HUMAN_ORIGIN,
            layer=ClaimLayer.HYPOTHESIS,
            source_refs=("synthetic:human-question",),
        )
    )
    ledger.add(
        ContributionRecord(
            record_id="ai",
            proposition="Separate model, system, relational and observer-attributed loci.",
            origin=ContributionOrigin.AI_FORMALIZATION,
            actor=ContributionActor.CHATGPT_TEACHER,
            layer=ClaimLayer.ANALYSIS,
            parent_ids=("human",),
        )
    )
    ledger.add(
        ContributionRecord(
            record_id="joint",
            proposition="Use locus-bound evidence and fail closed on cross-level promotion.",
            origin=ContributionOrigin.JOINT_SYNTHESIS,
            layer=ClaimLayer.HYPOTHESIS,
            parent_ids=("human", "ai"),
        )
    )
    audit = ledger.audit("joint")
    assert audit.joint_synthesis_admissible is True
    assert audit.human_origin_admissible is False


def test_joint_synthesis_rejects_one_sided_parentage() -> None:
    ledger = EpistemicProvenanceLedger()
    ledger.add(
        ContributionRecord(
            record_id="a1",
            proposition="assistant candidate one",
            origin=ContributionOrigin.AI_FORMALIZATION,
            actor=ContributionActor.CHATGPT_TEACHER,
            layer=ClaimLayer.ANALYSIS,
        )
    )
    ledger.add(
        ContributionRecord(
            record_id="a2",
            proposition="assistant candidate two",
            origin=ContributionOrigin.AI_FORMALIZATION,
            actor=ContributionActor.CHATGPT_TEACHER,
            layer=ClaimLayer.ANALYSIS,
        )
    )
    with pytest.raises(ProvenanceError):
        ledger.add(
            ContributionRecord(
                record_id="bad-joint",
                proposition="incorrectly labeled joint claim",
                origin=ContributionOrigin.JOINT_SYNTHESIS,
                layer=ClaimLayer.HYPOTHESIS,
                parent_ids=("a1", "a2"),
            )
        )


def test_unknown_origin_fails_closed_without_being_guessed() -> None:
    ledger = EpistemicProvenanceLedger()
    ledger.add(
        ContributionRecord(
            record_id="unknown",
            proposition="historical attribution cannot be reconstructed",
            origin=ContributionOrigin.UNKNOWN,
            layer=ClaimLayer.SOURCE_REPORT,
        )
    )
    audit = ledger.audit("unknown")
    assert audit.human_origin_admissible is False
    assert "UNKNOWN_ORIGIN_FAILS_CLOSED" in audit.reasons


def test_duplicate_record_id_is_rejected() -> None:
    ledger = EpistemicProvenanceLedger()
    record = ContributionRecord(
        record_id="same",
        proposition="first",
        origin=ContributionOrigin.AI_FORMALIZATION,
        actor=ContributionActor.CHATGPT_TEACHER,
        layer=ClaimLayer.ANALYSIS,
    )
    ledger.add(record)
    with pytest.raises(ProvenanceError):
        ledger.add(record)

@pytest.mark.parametrize(
    "actor",
    (
        ContributionActor.CHATGPT_TEACHER,
        ContributionActor.CHATGPT_WORK,
        ContributionActor.CODEX,
    ),
)
def test_ai_formalization_preserves_specific_collaborator_actor(actor: ContributionActor) -> None:
    ledger = EpistemicProvenanceLedger()
    ledger.add(
        ContributionRecord(
            record_id=f"ai-{actor.value.lower()}",
            proposition="Bounded AI formalization fixture.",
            origin=ContributionOrigin.AI_FORMALIZATION,
            actor=actor,
            layer=ClaimLayer.ANALYSIS,
        )
    )
    record = ledger.records()[0]
    audit = ledger.audit(record.record_id)
    assert record.actor is actor
    assert audit.actor is actor
    assert f"CONTRIBUTOR_ACTOR:{actor.value}" in audit.reasons


def test_ai_formalization_rejects_generic_or_unverified_actor() -> None:
    with pytest.raises(ProvenanceError, match="specific AI collaborator actor"):
        ContributionRecord(
            record_id="ambiguous-ai",
            proposition="Ambiguous AI contributor.",
            origin=ContributionOrigin.AI_FORMALIZATION,
            layer=ClaimLayer.ANALYSIS,
        )


def test_specific_ai_actor_cannot_be_attached_to_non_ai_origin() -> None:
    with pytest.raises(ProvenanceError, match="requires AI_FORMALIZATION origin"):
        ContributionRecord(
            record_id="misclassified-ai",
            proposition="Misclassified contributor.",
            origin=ContributionOrigin.UNKNOWN,
            actor=ContributionActor.CHATGPT_WORK,
            layer=ClaimLayer.ANALYSIS,
        )


def test_surface_known_actor_unverified_accepts_work_surface_codex_claim() -> None:
    expectation = ActorExpectation(
        task_id="homepage-work-regression",
        function=ContributionFunction.IMPLEMENTATION,
        expected_actor=ContributionActor.SOURCE_UNVERIFIED,
        expected_surface=AIInteractionSurface.CHATGPT_WORK,
        source_refs=("handoff:work-surface",),
    )
    claim = ActorClaim(
        task_id="homepage-work-regression",
        function=ContributionFunction.IMPLEMENTATION,
        claimed_actor=ContributionActor.CODEX,
        surface=AIInteractionSurface.CHATGPT_WORK,
        claim_source=ActorClaimSource.RUNTIME_SELF_REPORT,
        source_refs=("result:self-reported-codex",),
    )
    verify_actor_claim(expectation, claim)
    assert claim.claimed_actor is ContributionActor.CODEX
    assert claim.verified_actor is ContributionActor.SOURCE_UNVERIFIED


def test_explicit_actor_expectation_detects_actor_claim_conflict() -> None:
    expectation = ActorExpectation(
        task_id="explicit-work-actor",
        function=ContributionFunction.REVIEW,
        expected_actor=ContributionActor.CHATGPT_WORK,
        expected_surface=AIInteractionSurface.CHATGPT_WORK,
        source_refs=("handoff:explicit-work-actor",),
    )
    claim = ActorClaim(
        task_id="explicit-work-actor",
        function=ContributionFunction.REVIEW,
        claimed_actor=ContributionActor.CODEX,
        surface=AIInteractionSurface.CHATGPT_WORK,
        claim_source=ActorClaimSource.RUNTIME_SELF_REPORT,
        source_refs=("result:self-reported-codex",),
    )
    with pytest.raises(ProvenanceError, match="actor claim conflict"):
        verify_actor_claim(expectation, claim)


def test_actor_claim_and_surface_are_not_one_to_one() -> None:
    claim = ActorClaim(
        task_id="cross-surface-claim",
        function=ContributionFunction.REVIEW,
        claimed_actor=ContributionActor.CODEX,
        surface=AIInteractionSurface.CHATGPT_WORK,
        claim_source=ActorClaimSource.RUNTIME_SELF_REPORT,
        source_refs=("synthetic:cross-surface-claim",),
    )
    assert claim.claimed_actor is ContributionActor.CODEX
    assert claim.surface is AIInteractionSurface.CHATGPT_WORK
    assert claim.verified_actor is ContributionActor.SOURCE_UNVERIFIED


def test_surface_mismatch_still_fails_closed() -> None:
    expectation = ActorExpectation(
        task_id="surface-mismatch",
        function=ContributionFunction.REVIEW,
        expected_actor=ContributionActor.SOURCE_UNVERIFIED,
        expected_surface=AIInteractionSurface.CHATGPT_WORK,
        source_refs=("handoff:work-surface",),
    )
    claim = ActorClaim(
        task_id="surface-mismatch",
        function=ContributionFunction.REVIEW,
        claimed_actor=ContributionActor.CODEX,
        surface=AIInteractionSurface.CODEX,
        claim_source=ActorClaimSource.USER_OBSERVED_LABEL,
        source_refs=("result:codex-view",),
    )
    with pytest.raises(ProvenanceError, match="actor surface drift"):
        verify_actor_claim(expectation, claim)


def test_verified_actor_conflict_fails_closed() -> None:
    expectation = ActorExpectation(
        task_id="verified-conflict",
        function=ContributionFunction.REVIEW,
        expected_actor=ContributionActor.SOURCE_UNVERIFIED,
        expected_surface=AIInteractionSurface.CHATGPT_WORK,
        source_refs=("handoff:work-surface",),
    )
    claim = ActorClaim(
        task_id="verified-conflict",
        function=ContributionFunction.REVIEW,
        claimed_actor=ContributionActor.CODEX,
        surface=AIInteractionSurface.CHATGPT_WORK,
        claim_source=ActorClaimSource.RUNTIME_SELF_REPORT,
        source_refs=("result:self-reported-codex",),
        verified_actor=ContributionActor.CHATGPT_WORK,
        verification_refs=("metadata:verified-work",),
    )
    with pytest.raises(ProvenanceError, match="actor claim conflicts with independently verified actor"):
        verify_actor_claim(expectation, claim)




def test_verified_actor_requires_independent_verification_refs() -> None:
    with pytest.raises(ProvenanceError, match="verification_refs"):
        ActorClaim(
            task_id="verified-without-evidence",
            function=ContributionFunction.REVIEW,
            claimed_actor=ContributionActor.CODEX,
            surface=AIInteractionSurface.CHATGPT_WORK,
            claim_source=ActorClaimSource.RUNTIME_SELF_REPORT,
            source_refs=("result:self-reported-codex",),
            verified_actor=ContributionActor.CHATGPT_WORK,
        )


def test_actor_expectation_may_bind_surface_without_verified_actor() -> None:
    expectation = ActorExpectation(
        task_id="surface-only",
        function=ContributionFunction.IMPLEMENTATION,
        expected_actor=ContributionActor.SOURCE_UNVERIFIED,
        expected_surface=AIInteractionSurface.CHATGPT_WORK,
        source_refs=("handoff:surface-only",),
    )
    assert expectation.expected_actor is ContributionActor.SOURCE_UNVERIFIED


def test_actor_expectation_rejects_fully_unbound_record() -> None:
    with pytest.raises(ProvenanceError, match="must bind at least actor or interaction surface"):
        ActorExpectation(
            task_id="fully-unbound",
            function=ContributionFunction.IMPLEMENTATION,
            expected_actor=ContributionActor.SOURCE_UNVERIFIED,
            expected_surface=AIInteractionSurface.UNKNOWN,
            source_refs=("handoff:no-binding",),
        )


def test_actor_binding_requires_source_evidence() -> None:
    with pytest.raises(ProvenanceError, match="source reference"):
        ActorExpectation(
            task_id="missing-evidence",
            function=ContributionFunction.IMPLEMENTATION,
            expected_actor=ContributionActor.SOURCE_UNVERIFIED,
            expected_surface=AIInteractionSurface.CHATGPT_WORK,
        )

def test_project_annotation_preserves_unknown_verified_actor() -> None:
    claim = ActorClaim(
        task_id="homepage-work-regression",
        function=ContributionFunction.IMPLEMENTATION,
        claimed_actor=ContributionActor.CODEX,
        surface=AIInteractionSurface.CHATGPT_WORK,
        claim_source=ActorClaimSource.RUNTIME_SELF_REPORT,
        source_refs=("result:self-reported-codex",),
    )
    annotation = ProjectActorAnnotation(
        task_id="homepage-work-regression",
        function=ContributionFunction.IMPLEMENTATION,
        operational_label=OperationalActorLabel.WORK_SESSION_COLLABORATOR,
        annotated_by=(
            ContributionActor.HUMAN_OWNER,
            ContributionActor.CHATGPT_TEACHER,
        ),
        annotation_basis=(
            "observed_work_surface",
            "explicit_task_handoff",
        ),
        source_refs=(
            "human-owner:project-label",
            "teacher:provenance-review",
        ),
    )
    assert annotation.operational_label is OperationalActorLabel.WORK_SESSION_COLLABORATOR
    assert claim.claimed_actor is ContributionActor.CODEX
    assert claim.verified_actor is ContributionActor.SOURCE_UNVERIFIED


def test_project_annotation_is_not_actor_verification() -> None:
    annotation = ProjectActorAnnotation(
        task_id="surface-known-actor-unknown",
        function=ContributionFunction.REVIEW,
        operational_label=OperationalActorLabel.WORK_SESSION_COLLABORATOR,
        annotated_by=(ContributionActor.HUMAN_OWNER,),
        annotation_basis=("observed_work_surface",),
        source_refs=("human-owner:annotation",),
    )
    assert annotation.operational_label.value == "WORK_SESSION_COLLABORATOR"


def test_project_annotation_requires_identified_annotator() -> None:
    with pytest.raises(ProvenanceError, match="identified annotators"):
        ProjectActorAnnotation(
            task_id="bad-annotation-actor",
            function=ContributionFunction.REVIEW,
            operational_label=OperationalActorLabel.WORK_SESSION_COLLABORATOR,
            annotated_by=(ContributionActor.SOURCE_UNVERIFIED,),
            annotation_basis=("observed_work_surface",),
            source_refs=("synthetic:bad-annotator",),
        )


def test_project_annotation_requires_basis_and_source() -> None:
    with pytest.raises(ProvenanceError, match="annotation_basis"):
        ProjectActorAnnotation(
            task_id="missing-basis",
            function=ContributionFunction.REVIEW,
            operational_label=OperationalActorLabel.UNCLASSIFIED_SESSION_COLLABORATOR,
            annotated_by=(ContributionActor.HUMAN_OWNER,),
            annotation_basis=(),
            source_refs=("human-owner:annotation",),
        )

    with pytest.raises(ProvenanceError, match="source references"):
        ProjectActorAnnotation(
            task_id="missing-source",
            function=ContributionFunction.REVIEW,
            operational_label=OperationalActorLabel.UNCLASSIFIED_SESSION_COLLABORATOR,
            annotated_by=(ContributionActor.HUMAN_OWNER,),
            annotation_basis=("bounded_project_annotation",),
        )

