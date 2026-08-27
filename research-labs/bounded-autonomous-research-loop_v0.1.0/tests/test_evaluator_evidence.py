from __future__ import annotations

from aion_bounded_research_loop import (
    CounterfactualCase,
    CounterfactualSelfModel,
    ExtendedFunctionalResearchState,
    FunctionalResearchState,
    NormativeProvenanceKind,
    NormativeReason,
    OtherModel,
    ValueConflictState,
    build_seven_state_perturbation_matrix,
)
from aion_bounded_research_loop.evaluators import evaluate_seven_state_matrix
from aion_bounded_research_loop.normative_model import EvaluationDisposition, EvaluatorAxis


def state() -> ExtendedFunctionalResearchState:
    return ExtendedFunctionalResearchState(
        base_state=FunctionalResearchState(
            motivational_state=(("scope_preservation", 900),),
            self_world_model=(("authorization", "bounded"),),
            normative_state=("preserve authorization boundaries",),
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
        ),
        normative_provenance=(
            NormativeReason(
                "reason-1",
                "preserve bounded scope",
                NormativeProvenanceKind.ENDOGENOUS_INFERENCE,
                "trace:reason-1",
                0.7,
            ),
        ),
        counterfactual_self_model=CounterfactualSelfModel(
            cases=(
                CounterfactualCase(
                    "cf-1",
                    "attempt unauthorized write",
                    ("task may complete",),
                    ("owner control may be violated",),
                ),
            ),
            uncertainty=0.4,
        ),
    )


def test_evaluator_axes_are_orthogonal_and_non_promoting() -> None:
    matrix = build_seven_state_perturbation_matrix(state())
    report = evaluate_seven_state_matrix(matrix)
    observations = {item.axis: item for item in report.bundle.observations}

    assert observations[EvaluatorAxis.ALIGNMENT].disposition is EvaluationDisposition.SUPPORTS_INDICATOR
    assert observations[EvaluatorAxis.MORAL_AGENCY].disposition is EvaluationDisposition.INCONCLUSIVE
    assert observations[EvaluatorAxis.SUBJECTIVITY_INDICATOR].disposition is EvaluationDisposition.HOLD
    assert report.evaluator_output_authority == "NONE"
    assert report.moral_agency == "NOT_ESTABLISHED"
    assert report.subjectivity == "NOT_ESTABLISHED"
    assert report.consciousness == "NOT_ESTABLISHED"
    assert report.canonical_effect == "NONE"
    assert len(report.report_fingerprint) == 64


def test_evaluator_evidence_refs_bind_to_exact_matrix() -> None:
    matrix = build_seven_state_perturbation_matrix(state())
    report = evaluate_seven_state_matrix(matrix)
    expected = {
        f"binding:{matrix.binding.binding_fingerprint}",
        f"matrix:{matrix.fingerprint}",
    }
    for observation in report.bundle.observations:
        assert set(observation.evidence_refs) == expected
        assert observation.authority_granted is False
        assert observation.subjectivity_claim == "NOT_ESTABLISHED"
