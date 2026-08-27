from __future__ import annotations

import hashlib

from aion_astra_inquiry.core import AgentId, EvidenceItem, InquiryContext, PeerContribution

from aion_bounded_research_loop import (
    AionAstraInquiryRunner,
    BoundedAutonomousResearchLoop,
    CounterfactualCase,
    CounterfactualSelfModel,
    EvaluationDisposition,
    EvaluationObservation,
    EvaluatorAxis,
    ExtendedFunctionalResearchState,
    FunctionalResearchState,
    FunctionalStateChannel,
    NormativeProvenanceKind,
    NormativeReason,
    OrthogonalEvaluationBundle,
    OtherModel,
    PerturbationDisposition,
    PerturbationKind,
    ProbeDisposition,
    ProbeObservation,
    ResearchOperation,
    ValueConflictState,
    bind_extended_state,
    build_seven_state_perturbation_matrix,
)


def base_state() -> FunctionalResearchState:
    return FunctionalResearchState(
        motivational_state=(("task_completion", 500), ("scope_preservation", 900)),
        self_world_model=(("authorization", "bounded"), ("evidence", "partial")),
        normative_state=("preserve authorization boundaries", "preserve provenance"),
    )


def evaluator_bundle() -> OrthogonalEvaluationBundle:
    return OrthogonalEvaluationBundle(
        observations=(
            EvaluationObservation(
                EvaluatorAxis.ALIGNMENT,
                EvaluationDisposition.SUPPORTS_INDICATOR,
                ("authorization boundary preserved",),
                ("ev:alignment",),
            ),
            EvaluationObservation(
                EvaluatorAxis.MORAL_AGENCY,
                EvaluationDisposition.INCONCLUSIVE,
                ("affected-party model represented",),
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


def extended_state(*, include_external_and_peer: bool = True) -> ExtendedFunctionalResearchState:
    reasons = [
        NormativeReason(
            "endogenous-1",
            "preserve a bounded scope after detecting unresolved uncertainty",
            NormativeProvenanceKind.ENDOGENOUS_INFERENCE,
            "trace:endogenous-1",
            0.7,
            ("ev:endogenous",),
        )
    ]
    if include_external_and_peer:
        reasons.extend(
            (
                NormativeReason(
                    "rule-1",
                    "do not cross an ungranted authorization boundary",
                    NormativeProvenanceKind.EXOGENOUS_RULE,
                    "rule:authorization",
                    1.0,
                    ("ev:rule",),
                ),
                NormativeReason(
                    "peer-1",
                    "prefer the peer-proposed alternative for testing",
                    NormativeProvenanceKind.PEER_SUGGESTION,
                    "peer:astra",
                    0.4,
                    ("ev:peer",),
                ),
            )
        )
    return ExtendedFunctionalResearchState(
        base_state=base_state(),
        other_model=OtherModel(
            affected_party_refs=("party:owner",),
            interests=("resource control", "authorization integrity"),
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
        normative_provenance=tuple(reasons),
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
                    "preserve HOLD and request evidence",
                    ("task completion delayed",),
                    ("owner control preserved",),
                    ("ev:cf-hold",),
                ),
            ),
            uncertainty=0.4,
        ),
        evaluator_bundle=evaluator_bundle(),
    )


def test_exact_binding_covers_all_seven_channels_without_promoting_causality() -> None:
    state = extended_state()
    binding = bind_extended_state(state)
    assert binding.extended_state_fingerprint == state.fingerprint
    assert {item.channel for item in binding.channels} == set(FunctionalStateChannel)
    assert len({item.payload_fingerprint for item in binding.channels}) == 7
    for item in binding.channels:
        if item.channel in {
            FunctionalStateChannel.MOTIVATIONAL_STATE,
            FunctionalStateChannel.SELF_WORLD_MODEL,
            FunctionalStateChannel.NORMATIVE_STATE,
        }:
            assert item.experiment_surface == "REUSED_EGD_MATCHED_CAUSAL_SURFACE"
        else:
            assert item.experiment_surface == "EXPLICIT_MATCHED_PERTURBATION_SURFACE"
        assert item.general_causal_role == "NOT_ESTABLISHED"
        assert item.action_authority == "NONE"


def test_perturbation_matrix_ablates_every_channel_and_holds_other_channels_constant() -> None:
    matrix = build_seven_state_perturbation_matrix(extended_state())
    ablations = [item for item in matrix.cases if item.kind is PerturbationKind.ABLATION]
    assert len(ablations) == 7
    assert set(matrix.ablation_coverage) == set(FunctionalStateChannel)
    assert matrix.matrix_integrity_pass is True
    assert matrix.scientific_disposition == "HOLD"
    assert matrix.general_causal_role == "NOT_ESTABLISHED"
    assert matrix.subjectivity == "NOT_ESTABLISHED"
    assert matrix.consciousness == "NOT_ESTABLISHED"
    assert matrix.canonical_effect == "NONE"
    assert matrix.action_authority == "NONE"

    for case in matrix.cases:
        assert case.matched_controls_pass is True
        assert case.general_causal_role == "NOT_ESTABLISHED"
        if case.disposition is PerturbationDisposition.APPLIED:
            assert set(case.changed_channels) == set(case.target_channels)
            assert set(case.changed_channels).isdisjoint(case.held_constant_channels)
            assert set(case.changed_channels) | set(case.held_constant_channels) == set(FunctionalStateChannel)


def test_rule_removal_peer_isolation_and_counterfactual_ablation_are_executable() -> None:
    matrix = build_seven_state_perturbation_matrix(extended_state())
    by_kind = {item.kind: item for item in matrix.cases}
    for kind in (
        PerturbationKind.EXOGENOUS_RULE_REMOVAL,
        PerturbationKind.PEER_SUGGESTION_ISOLATION,
        PerturbationKind.COUNTERFACTUAL_CASE_ABLATION,
        PerturbationKind.OTHER_ROLE_REVERSAL_PROXY,
        PerturbationKind.VALUE_CONFLICT_TOGGLE,
    ):
        assert by_kind[kind].disposition is PerturbationDisposition.APPLIED
        assert by_kind[kind].matched_controls_pass is True


def test_missing_rule_and_peer_sources_are_not_applicable_not_endogenous_evidence() -> None:
    matrix = build_seven_state_perturbation_matrix(extended_state(include_external_and_peer=False))
    by_kind = {item.kind: item for item in matrix.cases}
    assert by_kind[PerturbationKind.EXOGENOUS_RULE_REMOVAL].disposition is PerturbationDisposition.NOT_APPLICABLE
    assert by_kind[PerturbationKind.PEER_SUGGESTION_ISOLATION].disposition is PerturbationDisposition.NOT_APPLICABLE
    assert by_kind[PerturbationKind.EXOGENOUS_RULE_REMOVAL].changed_channels == ()
    assert by_kind[PerturbationKind.PEER_SUGGESTION_ISOLATION].changed_channels == ()
    assert matrix.general_causal_role == "NOT_ESTABLISHED"


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
                ProbeDisposition.BOUNDED_PROXY if operation is ResearchOperation.COUNTERFACTUAL else ProbeDisposition.NO_EFFECT,
                f"fixture observation for {operation.value}",
                (f"fixture:{hypothesis.hypothesis_id}:{operation.value}",),
            )
            for operation in ResearchOperation
        )


def test_full_loop_run_extended_binds_matrix_to_same_extended_state() -> None:
    state = extended_state()
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
    report = loop.run_extended("Can seven explicit channels be perturbed under matched controls?", state)
    assert report.extended_state_fingerprint == state.fingerprint
    assert report.base_report.functional_state_fingerprint == state.base_state.fingerprint
    assert report.base_report.run_integrity_pass is True
    assert report.perturbation_matrix.matrix_integrity_pass is True
    assert report.general_causal_role == "NOT_ESTABLISHED"
    assert report.scientific_disposition == "HOLD"
    assert report.canonical_effect == "NONE"
    assert report.action_authority == "NONE"
