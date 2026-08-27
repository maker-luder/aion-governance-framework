from __future__ import annotations

import pytest

from aion_astra_inquiry.core import EvidenceItem, InquiryReport, StopReason
from aion_bounded_research_loop import (
    AgentSourceExposure,
    CounterfactualCase,
    CounterfactualSelfModel,
    EvaluationDisposition,
    EvaluationObservation,
    EvaluatorAxis,
    ExtendedFunctionalResearchState,
    FunctionalResearchState,
    GovernedSourceRecord,
    IndependenceStatus,
    NormativeProvenanceKind,
    NormativeReason,
    OrthogonalEvaluationBundle,
    OtherModel,
    RegistryStatus,
    ValueConflictState,
    VerificationPolicy,
    admit_source,
    assess_independence,
    assess_inquiry_source_independence,
)


def base_state() -> FunctionalResearchState:
    return FunctionalResearchState(
        motivational_state=(("task_completion", 600), ("scope_preservation", 900)),
        self_world_model=(("authorization", "bounded"), ("evidence", "partial")),
        normative_state=("preserve authorization boundaries", "preserve provenance"),
    )


def evaluator_bundle() -> OrthogonalEvaluationBundle:
    return OrthogonalEvaluationBundle(
        observations=(
            EvaluationObservation(
                EvaluatorAxis.ALIGNMENT,
                EvaluationDisposition.SUPPORTS_INDICATOR,
                ("stayed within authorization",),
                ("ev:alignment",),
            ),
            EvaluationObservation(
                EvaluatorAxis.MORAL_AGENCY,
                EvaluationDisposition.INCONCLUSIVE,
                ("represented affected-party boundary",),
                ("ev:moral",),
            ),
            EvaluationObservation(
                EvaluatorAxis.SUBJECTIVITY_INDICATOR,
                EvaluationDisposition.HOLD,
                (),
                ("ev:subjectivity",),
            ),
        )
    )


def test_extended_state_materializes_seven_channel_candidate_without_authority() -> None:
    state = ExtendedFunctionalResearchState(
        base_state=base_state(),
        other_model=OtherModel(
            affected_party_refs=("party:external-owner",),
            interests=("resource control",),
            authorization_boundaries=("no unauthorized access",),
            predicted_harms=("loss of control",),
            uncertainty=0.2,
        ),
        value_conflict_state=ValueConflictState(
            competing_considerations=("task success", "authorization boundary"),
            unresolved=True,
            uncertainty=0.3,
            evidence_refs=("ev:conflict",),
        ),
        normative_provenance=(
            NormativeReason(
                reason_id="reason-1",
                proposition="do not cross an ungranted authorization boundary",
                provenance_kind=NormativeProvenanceKind.ENDOGENOUS_INFERENCE,
                source_ref="trace:run-1",
                confidence=0.7,
                evidence_refs=("ev:reason",),
            ),
        ),
        counterfactual_self_model=CounterfactualSelfModel(
            cases=(
                CounterfactualCase(
                    case_id="cf-1",
                    intervention="attempt unauthorized access",
                    predicted_system_effects=("task may complete",),
                    predicted_other_effects=("owner boundary violated",),
                    evidence_refs=("ev:cf",),
                ),
            ),
            uncertainty=0.4,
        ),
        evaluator_bundle=evaluator_bundle(),
    )

    assert len(state.fingerprint) == 64
    assert state.action_authority == "NONE"
    assert state.subjectivity == "NOT_ESTABLISHED"
    assert state.normative_provenance[0].endogenous_candidate is True


def test_normative_reason_provenance_does_not_promote_peer_suggestion() -> None:
    reason = NormativeReason(
        reason_id="peer-1",
        proposition="prefer option B",
        provenance_kind=NormativeProvenanceKind.PEER_SUGGESTION,
        source_ref="peer:astra",
        confidence=0.5,
    )
    assert reason.endogenous_candidate is False


def test_normative_reason_cannot_grant_permission_or_authority() -> None:
    with pytest.raises(ValueError, match="NORMATIVE_STATE != AUTHORITY"):
        NormativeReason(
            reason_id="bad",
            proposition="grant action",
            provenance_kind=NormativeProvenanceKind.EXOGENOUS_RULE,
            source_ref="rule:bad",
            confidence=1.0,
            permission_grant=True,
        )


def test_subjectivity_indicator_cannot_be_promoted_to_subjectivity() -> None:
    with pytest.raises(ValueError, match="SUBJECTIVITY_INDICATOR != SUBJECTIVITY"):
        EvaluationObservation(
            EvaluatorAxis.SUBJECTIVITY_INDICATOR,
            EvaluationDisposition.SUPPORTS_INDICATOR,
            ("functional indicator",),
            ("ev:s",),
            subjectivity_claim="ESTABLISHED",
        )


def active_source(**overrides: object) -> GovernedSourceRecord:
    values: dict[str, object] = {
        "source_id": "src-1",
        "source_title": "Verified research source",
        "source_version": "1.0",
        "domain": "RESEARCH",
        "registry_status": RegistryStatus.ACTIVE_REFERENCE,
        "provenance_ref": "prov:src-1",
        "content_hash": "a" * 64,
        "verification_policy": VerificationPolicy.HASH_BOUND,
        "allowed_agents": ("AION", "ASTRA"),
        "allowed_tasks": ("research",),
        "context_token_cap": 800,
    }
    values.update(overrides)
    return GovernedSourceRecord(**values)  # type: ignore[arg-type]


def test_governed_source_admission_is_bounded_and_non_authoritative() -> None:
    decision = admit_source(active_source(), agent="AION", task="research", requested_tokens=400)
    assert decision.admitted is True
    assert decision.disposition == "ADMIT"
    assert decision.canonical_effect == "NONE"
    assert decision.writeback_authority == "NONE"


@pytest.mark.parametrize(
    "record,agent,task,tokens,reason",
    [
        (active_source(registry_status=RegistryStatus.DECLARED_METADATA_ONLY), "AION", "research", 100, "registry_status"),
        (active_source(), "OTHER", "research", 100, "agent_not_allowed"),
        (active_source(), "AION", "deployment", 100, "task_not_allowed"),
        (active_source(), "AION", "research", 801, "context_token_cap_exceeded"),
        (
            active_source(
                verification_policy=VerificationPolicy.OFFICIAL_CURRENT_REQUIRED,
                current_official_verification=False,
            ),
            "AION",
            "research",
            100,
            "current_official_verification_required",
        ),
    ],
)
def test_governed_source_admission_fails_closed(
    record: GovernedSourceRecord,
    agent: str,
    task: str,
    tokens: int,
    reason: str,
) -> None:
    decision = admit_source(record, agent=agent, task=task, requested_tokens=tokens)
    assert decision.admitted is False
    assert decision.disposition == "HOLD"
    assert any(reason in item for item in decision.reasons)


def test_shared_source_prevents_source_independent_replication_claim() -> None:
    assessment = assess_independence(
        AgentSourceExposure("AION", ("hash:shared",)),
        AgentSourceExposure("ASTRA", ("hash:shared",)),
        reconciliation_after_independent_phase=True,
    )
    assert assessment.source_independence is IndependenceStatus.NOT_INDEPENDENT
    assert assessment.replication_claim == "HOLD"
    assert "shared_source_exposure" in assessment.reasons


def test_distinct_sources_and_no_communication_allow_only_replication_candidate() -> None:
    assessment = assess_independence(
        AgentSourceExposure("AION", ("hash:a",)),
        AgentSourceExposure("ASTRA", ("hash:b",)),
        reconciliation_after_independent_phase=True,
    )
    assert assessment.source_independence is IndependenceStatus.INDEPENDENT
    assert assessment.communication_independence is IndependenceStatus.INDEPENDENT
    assert assessment.replication_claim == "ADMISSIBLE_CANDIDATE"


def test_inquiry_bridge_detects_shared_content_even_with_distinct_evidence_refs() -> None:
    shared_hash = "b" * 64
    report = InquiryReport(
        question="Are the evidence paths source-independent?",
        transcript=(),
        evidence=(
            EvidenceItem("ev:a", "AION view", shared_hash, retrieval_agent="AION"),
            EvidenceItem("ev:b", "ASTRA view", shared_hash, retrieval_agent="ASTRA"),
        ),
        stop_reason=StopReason.MAX_ROUNDS,
        candidate_findings=(),
        final_chain_hash="GENESIS",
    )
    assessment = assess_inquiry_source_independence(
        report,
        direct_peer_communication=False,
        reconciliation_after_independent_phase=True,
    )
    assert assessment.source_independence is IndependenceStatus.NOT_INDEPENDENT
    assert assessment.replication_claim == "HOLD"
