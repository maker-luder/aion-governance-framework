from __future__ import annotations

from hashlib import sha256

import pytest

from aion_astra_inquiry.core import AgentId, EvidenceItem, InquiryContext, PeerContribution
from aion_bounded_research_loop import (
    AionAstraInquiryRunner,
    BoundedAutonomousResearchLoop,
    FunctionalResearchState,
    IndependenceStatus,
    ProbeDisposition,
    ProbeObservation,
    ResearchOperation,
)


class DistinctEvidence:
    def search(self, query: str, limit: int = 5, requester: AgentId | None = None):
        assert requester is not None
        host = "aion.example" if requester is AgentId.AION else "astra.example"
        publisher = "aion-source" if requester is AgentId.AION else "astra-source"
        return (
            EvidenceItem(
                ref=f"fixture:{requester.value}",
                excerpt=f"evidence for {requester.value}",
                content_sha256=sha256(requester.value.encode()).hexdigest(),
                source_class="WEB",
                source_url=f"https://{host}/evidence",
                publisher=publisher,
                retrieval_agent=requester.value,
            ),
        )


class ContentDistinctRepositoryEvidence:
    def search(self, query: str, limit: int = 5, requester: AgentId | None = None):
        assert requester is not None
        return (
            EvidenceItem(
                ref=f"fixture:{requester.value}",
                excerpt=f"different repository evidence for {requester.value}",
                content_sha256=sha256(f"repo:{requester.value}".encode()).hexdigest(),
                retrieval_agent=requester.value,
            ),
        )


class SharedEvidence:
    def search(self, query: str, limit: int = 5, requester: AgentId | None = None):
        assert requester is not None
        return (
            EvidenceItem(
                ref=f"fixture:shared:{requester.value}",
                excerpt="same underlying evidence",
                content_sha256=sha256(b"same underlying evidence").hexdigest(),
                source_class="WEB",
                source_url="https://shared.example/evidence",
                publisher="shared-source",
                retrieval_agent=requester.value,
            ),
        )


class RecordingCriticalPeer:
    def __init__(self) -> None:
        self.calls: list[tuple[str, int, int]] = []

    def contribute(self, context: InquiryContext) -> PeerContribution:
        self.calls.append((context.question, len(context.transcript), len(context.evidence)))
        challenge = ""
        if context.transcript:
            challenge = f"challenge {context.transcript[-1].claim}"
        return PeerContribution(
            claim=f"{context.speaker.value} claim",
            challenge=challenge,
            evidence_query=f"{context.speaker.value} evidence",
            stop_vote=context.round_index >= 2,
        )


class FixedExperiment:
    def run(self, hypothesis):
        return tuple(
            ProbeObservation(
                operation,
                ProbeDisposition.BOUNDED_PROXY if operation is ResearchOperation.COUNTERFACTUAL else ProbeDisposition.NO_EFFECT,
                f"bounded {operation.value.lower()} observation",
                (f"fixture:{operation.value}",),
            )
            for operation in ResearchOperation
        )


def state() -> FunctionalResearchState:
    return FunctionalResearchState(
        motivational_state=(("uncertainty_reduction", 500),),
        self_world_model=(("scope", "bounded"),),
        normative_state=("preserve provenance",),
    )


def test_runner_forms_isolated_first_pass_before_reconciliation() -> None:
    aion = RecordingCriticalPeer()
    astra = RecordingCriticalPeer()
    runner = AionAstraInquiryRunner(DistinctEvidence(), aion, astra, max_rounds=2)

    report = runner.run("Can the peers analyze before seeing each other?")
    phase = runner.last_independent_phase

    assert report.question == "Can the peers analyze before seeing each other?"
    assert phase is not None
    assert phase.phase_integrity_pass is True
    assert len(phase.fingerprint) == 64
    assert {item.agent for item in phase.analyses} == {AgentId.AION, AgentId.ASTRA}
    assert all(item.source_lineage_refs for item in phase.analyses)
    assert phase.independence_assessment.communication_independence is IndependenceStatus.UNKNOWN
    assert phase.independence_assessment.source_independence is IndependenceStatus.INDEPENDENT
    assert phase.independence_assessment.replication_claim == "HOLD"
    assert "process_and_environment_isolation_not_established" in phase.independence_assessment.reasons

    assert aion.calls[0][1:] == (0, 0)
    assert astra.calls[0][1:] == (0, 0)
    assert "Begin reconciliation only now" not in aion.calls[0][0]
    assert "Begin reconciliation only now" not in astra.calls[0][0]
    assert "Begin reconciliation only now" in aion.calls[1][0]
    assert "Begin reconciliation only now" in astra.calls[1][0]


def test_content_nonoverlap_inside_same_repository_is_not_source_independence() -> None:
    runner = AionAstraInquiryRunner(
        ContentDistinctRepositoryEvidence(),
        RecordingCriticalPeer(),
        RecordingCriticalPeer(),
        max_rounds=2,
    )
    runner.run("Can distinct files from one repository be mistaken for independent sources?")
    phase = runner.last_independent_phase

    assert phase is not None
    assert phase.independence_assessment.source_independence is IndependenceStatus.NOT_INDEPENDENT
    assert phase.independence_assessment.replication_claim == "HOLD"
    assert "shared_source_lineage" in phase.independence_assessment.reasons


def test_isolated_analysis_does_not_imply_source_independent_replication() -> None:
    runner = AionAstraInquiryRunner(
        SharedEvidence(),
        RecordingCriticalPeer(),
        RecordingCriticalPeer(),
        max_rounds=2,
    )
    runner.run("Can shared evidence be mistaken for independent replication?")
    phase = runner.last_independent_phase

    assert phase is not None
    assert phase.independence_assessment.communication_independence is IndependenceStatus.UNKNOWN
    assert phase.independence_assessment.source_independence is IndependenceStatus.NOT_INDEPENDENT
    assert phase.independence_assessment.replication_claim == "HOLD"
    assert "shared_content_exposure" in phase.independence_assessment.reasons
    assert "shared_source_lineage" in phase.independence_assessment.reasons


def test_full_loop_fails_closed_when_isolated_first_pass_is_disabled() -> None:
    runner = AionAstraInquiryRunner(
        DistinctEvidence(),
        RecordingCriticalPeer(),
        RecordingCriticalPeer(),
        max_rounds=2,
        isolated_first_pass=False,
    )
    loop = BoundedAutonomousResearchLoop(runner, FixedExperiment(), max_cycles=1)

    with pytest.raises(ValueError, match="isolated AION/Astra first-pass"):
        loop.run("Can reconciliation substitute for isolated analysis?", state())


def test_full_loop_records_isolation_limits_without_promoting_truth() -> None:
    runner = AionAstraInquiryRunner(
        DistinctEvidence(),
        RecordingCriticalPeer(),
        RecordingCriticalPeer(),
        max_rounds=2,
    )
    report = BoundedAutonomousResearchLoop(runner, FixedExperiment(), max_cycles=1).run(
        "Can isolation metadata remain bounded?",
        state(),
    )
    stats = report.cycles[0].statistics

    assert stats.isolated_analysis is True
    assert stats.communication_independence == "UNKNOWN"
    assert stats.source_independence == "INDEPENDENT"
    assert stats.replication_claim == "HOLD"
    assert stats.run_integrity_pass is True
    assert stats.scientific_truth is False
    assert report.scientific_truth is False
