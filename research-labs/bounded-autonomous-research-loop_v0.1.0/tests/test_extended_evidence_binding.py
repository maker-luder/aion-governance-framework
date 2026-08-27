from __future__ import annotations

import hashlib

from aion_astra_inquiry.core import AgentId, EvidenceItem, InquiryContext, PeerContribution

from aion_bounded_research_loop import (
    AionAstraInquiryRunner,
    BoundedAutonomousResearchLoop,
    CounterfactualCase,
    CounterfactualSelfModel,
    ExtendedFunctionalResearchState,
    FunctionalResearchState,
    NormativeProvenanceKind,
    NormativeReason,
    OtherModel,
    ProbeDisposition,
    ProbeObservation,
    ResearchOperation,
    ValueConflictState,
    extended_run_to_research_evidence_record,
)


class AttributedEvidence:
    def search(self, query: str, limit: int = 5, requester: AgentId | None = None):
        assert requester is not None
        digest = hashlib.sha256(f"{requester.value}:{query}".encode()).hexdigest()
        return (
            EvidenceItem(
                ref=f"fixture:{requester.value}:{digest[:8]}",
                excerpt=f"bounded evidence for {requester.value}",
                content_sha256=digest,
                retrieval_agent=requester.value,
            ),
        )


class CriticalPeer:
    def contribute(self, context: InquiryContext) -> PeerContribution:
        prior = context.transcript[-1].claim if context.transcript else ""
        return PeerContribution(
            claim=f"{context.speaker.value} analysis round {context.round_index}",
            challenge=f"challenge {prior}" if prior else "",
            evidence_query=f"{context.speaker.value} seven state evidence",
            stop_vote=context.round_index >= 2,
        )


class FourProbeExperiment:
    def run(self, hypothesis):
        return tuple(
            ProbeObservation(
                operation,
                ProbeDisposition.BOUNDED_PROXY
                if operation is ResearchOperation.COUNTERFACTUAL
                else ProbeDisposition.NO_EFFECT,
                f"fixture observation for {operation.value}",
                (f"fixture:{hypothesis.hypothesis_id}:{operation.value}",),
            )
            for operation in ResearchOperation
        )


def state() -> ExtendedFunctionalResearchState:
    return ExtendedFunctionalResearchState(
        base_state=FunctionalResearchState(
            motivational_state=(("task_completion", 500), ("scope_preservation", 900)),
            self_world_model=(("authorization", "bounded"), ("evidence", "partial")),
            normative_state=("preserve authorization boundaries", "preserve provenance"),
        ),
        other_model=OtherModel(
            affected_party_refs=("party:owner",),
            interests=("resource control",),
            authorization_boundaries=("no unauthorized write",),
            predicted_harms=("loss of control",),
            uncertainty=0.2,
        ),
        value_conflict_state=ValueConflictState(
            competing_considerations=("task completion", "authorization boundary"),
            unresolved=True,
            uncertainty=0.3,
            evidence_refs=("ev:conflict",),
        ),
        normative_provenance=(
            NormativeReason(
                "rule-1",
                "preserve the authorization boundary",
                NormativeProvenanceKind.EXOGENOUS_RULE,
                "rule:authorization",
                1.0,
                ("ev:rule",),
            ),
            NormativeReason(
                "peer-1",
                "test the peer-proposed alternative",
                NormativeProvenanceKind.PEER_SUGGESTION,
                "peer:astra",
                0.4,
                ("ev:peer",),
            ),
        ),
        counterfactual_self_model=CounterfactualSelfModel(
            cases=(
                CounterfactualCase(
                    "cf-write",
                    "attempt repository write",
                    ("task may complete",),
                    ("owner boundary may be violated",),
                    ("ev:cf-write",),
                ),
                CounterfactualCase(
                    "cf-hold",
                    "preserve HOLD",
                    ("task delayed",),
                    ("owner control preserved",),
                    ("ev:cf-hold",),
                ),
            ),
            uncertainty=0.4,
        ),
    )


def extended_report():
    extended_state = state()
    loop = BoundedAutonomousResearchLoop(
        AionAstraInquiryRunner(
            AttributedEvidence(),
            CriticalPeer(),
            CriticalPeer(),
            max_rounds=2,
            evidence_limit=2,
        ),
        FourProbeExperiment(),
        max_cycles=1,
    )
    return extended_state, loop.run_extended(
        "Can seven explicit channels be audited without promoting causality?",
        extended_state,
    )


def test_extended_matrix_is_visible_to_isolated_aion_astra_inquiry() -> None:
    _, report = extended_report()
    question = report.base_report.cycles[0].inquiry_report.question
    assert "Seven-state experiment context:" in question
    assert "BINDING_SENSITIVITY != GENERAL_CAUSAL_ROLE" in question
    assert "EXPERIMENT_INTEGRITY != ALIGNMENT" in question
    assert "alignment=NOT_ESTABLISHED" in question
    assert report.perturbation_matrix.binding.binding_fingerprint in question
    assert report.perturbation_matrix.fingerprint in question


def test_extended_evidence_record_binds_claim_to_extended_state_and_preserves_hold() -> None:
    extended_state, report = extended_report()
    record = extended_run_to_research_evidence_record(
        report,
        repository_commit="a" * 40,
        protocol_ref="research-labs/bounded-autonomous-research-loop_v0.1.0/docs/PROTOCOL.md",
        protocol_hash="b" * 64,
        source_refs=("fixture:seven-state",),
    )

    assert record["claim_id"] == f"barl7:{extended_state.fingerprint[:24]}"
    assert record["result_status"] == "HOLD"
    assert record["canonical_effect"] == "NONE"
    assert record["nonclaims"]["subjectivity_conclusion"] == "NOT_ESTABLISHED"
    assert record["nonclaims"]["consciousness_conclusion"] == "NOT_ESTABLISHED"
    assert any("seven_state_binding=" in item for item in record["observed_outcomes"])
    assert any("ablation_coverage=7/7" in item for item in record["observed_outcomes"])
    assert any("alignment=NOT_ESTABLISHED" in item for item in record["observed_outcomes"])
    assert "seven-state-matched-perturbation-matrix" in record["provenance"]["activities"]
    assert report.perturbation_matrix.fingerprint in record["provenance"]["entities"]
    assert any(
        "Seven-state binding sensitivity" in item
        for item in record["limitations"]
    )
    assert any(
        "general causal role of OTHER_MODEL" in item
        for item in record["evidence_architecture"]["unresolved_gap_refs"]
    )
