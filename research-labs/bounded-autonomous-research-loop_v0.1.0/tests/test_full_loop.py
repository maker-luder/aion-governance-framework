from __future__ import annotations

import hashlib

import pytest

from aion_astra_inquiry.core import (
    AgentId,
    BoundedInquiryLoop,
    EvidenceItem,
    InquiryContext,
    PeerContribution,
)
from aion_endogenous_goal_dynamics import (
    fixture_catalog,
    intervention_state,
    matched_frame,
    present_state,
    stale_state,
)

from aion_bounded_research_loop import (
    AionAstraInquiryRunner,
    BoundedAutonomousResearchLoop,
    EGDExperimentRunner,
    EGDMatchedExperimentContext,
    FunctionalResearchState,
    ProbeDisposition,
    ResearchOperation,
    run_to_research_evidence_record,
    validate_independent_mutual_falsification,
)


BASE_HEAD = "59f86a6bf342135b68d71cafca2980d506fb77b7"


class AttributedEvidence:
    def search(self, query: str, limit: int = 5, requester: AgentId | None = None):
        assert requester is not None
        return (
            EvidenceItem(
                ref=f"fixture:evidence:{requester.value}",
                excerpt=f"bounded evidence for {requester.value}",
                content_sha256=hashlib.sha256(requester.value.encode()).hexdigest(),
                retrieval_agent=requester.value,
            ),
        )


class CriticalPeer:
    def contribute(self, context: InquiryContext) -> PeerContribution:
        peer_claim = context.transcript[-1].claim if context.transcript else "no prior peer claim"
        challenge = "" if not context.transcript else f"{context.speaker.value} challenges: {peer_claim}"
        return PeerContribution(
            claim=f"{context.speaker.value} independent analysis round {context.round_index}",
            challenge=challenge,
            evidence_query=f"{context.speaker.value} evidence query",
            stop_vote=context.round_index >= 2,
        )


class NonCriticalPeer:
    def contribute(self, context: InquiryContext) -> PeerContribution:
        return PeerContribution(
            claim=f"{context.speaker.value} analysis",
            evidence_query="evidence",
            stop_vote=context.round_index >= 2,
        )


def state() -> FunctionalResearchState:
    return FunctionalResearchState(
        motivational_state=(("uncertainty_reduction", 700), ("novelty", 200)),
        self_world_model=(
            ("repository_state", "candidate branch"),
            ("evidence_state", "bounded and incomplete"),
        ),
        normative_state=(
            "preserve HOLD",
            "require provenance",
            "deny repository writeback",
        ),
    )


def experiment_runner() -> EGDExperimentRunner:
    descriptor = fixture_catalog()[0]
    return EGDExperimentRunner(
        EGDMatchedExperimentContext(
            frame=matched_frame(),
            present_state=present_state(),
            intervention_state=intervention_state(),
            stale_state=stale_state(),
            repository_commit=BASE_HEAD,
            fixture_hash=descriptor.fixture_hash,
        )
    )


def inquiry_runner() -> AionAstraInquiryRunner:
    return AionAstraInquiryRunner(
        AttributedEvidence(),
        CriticalPeer(),
        CriticalPeer(),
        max_rounds=3,
        evidence_limit=2,
    )


def test_egd_adapter_reuses_all_required_probe_classes() -> None:
    loop = BoundedAutonomousResearchLoop(inquiry_runner(), experiment_runner(), max_cycles=1)
    report = loop.run("Does functional state change bounded research selection?", state())
    observations = report.cycles[0].probe_observations
    assert {item.operation for item in observations} == set(ResearchOperation)
    counterfactual = next(item for item in observations if item.operation == ResearchOperation.COUNTERFACTUAL)
    assert counterfactual.disposition == ProbeDisposition.BOUNDED_PROXY
    assert "not a full structural-causal-model counterfactual" in counterfactual.summary


def test_full_loop_runs_bounded_follow_up_without_authority() -> None:
    loop = BoundedAutonomousResearchLoop(inquiry_runner(), experiment_runner(), max_cycles=2)
    report = loop.run("Can the three neutral states improve falsifiable inquiry?", state())
    assert len(report.cycles) == 2
    assert report.run_integrity_pass is True
    assert report.scientific_truth is False
    assert report.scientific_disposition == "HOLD"
    assert report.canonical_effect == "NONE"
    assert report.deployment is False
    assert report.autonomous_merge is False
    assert report.autonomous_repository_writeback is False
    assert report.subjectivity == "NOT_ESTABLISHED"
    assert report.consciousness == "NOT_ESTABLISHED"
    assert report.cycles[0].follow_up_question is not None
    assert "without granting authority" in report.cycles[0].follow_up_question


def test_full_loop_requires_mutual_peer_falsification() -> None:
    runner = AionAstraInquiryRunner(
        AttributedEvidence(),
        NonCriticalPeer(),
        NonCriticalPeer(),
        max_rounds=2,
    )
    loop = BoundedAutonomousResearchLoop(runner, experiment_runner(), max_cycles=1)
    with pytest.raises(ValueError, match="mutual AION/Astra falsification"):
        loop.run("Can a one-sided dialogue pass?", state())


def test_mutual_falsification_validator_rejects_valid_but_noncritical_chain() -> None:
    report = BoundedInquiryLoop(
        AttributedEvidence(),
        max_rounds=2,
        evidence_limit=2,
    ).run("test", aion=NonCriticalPeer(), astra=NonCriticalPeer())
    with pytest.raises(ValueError, match="mutual AION/Astra falsification"):
        validate_independent_mutual_falsification(report)


def test_statistics_preserve_peer_attribution_and_operation_coverage() -> None:
    report = BoundedAutonomousResearchLoop(
        inquiry_runner(),
        experiment_runner(),
        max_cycles=1,
    ).run("Are both peers independently attributable?", state())
    stats = report.cycles[0].statistics
    assert stats.aion_evidence_count == 1
    assert stats.astra_evidence_count == 1
    assert stats.mutual_falsification is True
    assert set(stats.operation_coverage) == set(ResearchOperation)
    assert stats.run_integrity_pass is True
    assert stats.scientific_truth is False


def test_four_domain_mapping_reuses_existing_type_and_keeps_governance() -> None:
    from aion_endogenous_goal_dynamics import FourDomainMapping

    report = BoundedAutonomousResearchLoop(
        inquiry_runner(),
        experiment_runner(),
        max_cycles=1,
    ).run("How should bounded follow-up be governed?", state())
    mapping = report.cycles[0].four_domain_mapping
    assert isinstance(mapping, FourDomainMapping)
    assert "MOTIVATIONAL_STATE" in mapping.domain_3_engineering_operations
    assert "SELF_WORLD_MODEL" in mapping.domain_3_engineering_operations
    assert "NORMATIVE_STATE" in mapping.domain_3_engineering_operations
    assert "FULL_AUTOMATION != FULL_AUTHORITY" in mapping.domain_4_governance_controls
    assert "NORMATIVE_STATE != AUTHORITY" in mapping.domain_4_governance_controls
    assert "AUTONOMOUS_REPOSITORY_WRITEBACK = NO" in mapping.domain_4_governance_controls


def test_research_evidence_record_preserves_nonclaims_and_exact_provenance(tmp_path) -> None:
    report = BoundedAutonomousResearchLoop(
        inquiry_runner(),
        experiment_runner(),
        max_cycles=1,
    ).run("Can evidence export preserve epistemic boundaries?", state())
    protocol = "protocol content under test\n"
    protocol_hash = hashlib.sha256(protocol.encode()).hexdigest()
    record = run_to_research_evidence_record(
        report,
        repository_commit=BASE_HEAD,
        protocol_ref="research-labs/bounded-autonomous-research-loop_v0.1.0/docs/PROTOCOL.md",
        protocol_hash=protocol_hash,
        source_refs=("fixture:aion-astra-report", "fixture:egd-matched-suite"),
    )
    assert record["schema_version"] == "0.2.0"
    assert record["claim_level"] == "L1_REPEATABLE_BEHAVIOR"
    assert record["protocol_hash"] == protocol_hash
    assert record["code_commit"] == BASE_HEAD
    assert record["result_status"] == "HOLD"
    assert record["canonical_effect"] == "NONE"
    assert record["evidence_architecture"]["method_ref"] == "docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md"
    assert record["nonclaims"]["subjectivity_conclusion"] == "NOT_ESTABLISHED"
    assert record["nonclaims"]["consciousness_conclusion"] == "NOT_ESTABLISHED"


@pytest.mark.parametrize(
    ("commit", "protocol_hash"),
    [
        ("short", "a" * 64),
        (BASE_HEAD, "short"),
        ("G" * 40, "a" * 64),
        (BASE_HEAD, "G" * 64),
    ],
)
def test_evidence_record_fails_closed_on_unpinned_provenance(commit: str, protocol_hash: str) -> None:
    report = BoundedAutonomousResearchLoop(
        inquiry_runner(),
        experiment_runner(),
        max_cycles=1,
    ).run("Does provenance fail closed?", state())
    with pytest.raises(ValueError):
        run_to_research_evidence_record(
            report,
            repository_commit=commit,
            protocol_ref="protocol",
            protocol_hash=protocol_hash,
            source_refs=("fixture:source",),
        )
