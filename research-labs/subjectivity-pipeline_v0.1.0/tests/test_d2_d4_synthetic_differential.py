from __future__ import annotations

from aion_continuity_governance import ContinuityLayer, continuity_status
from aion_endogenous_goal_dynamics import (
    DeterministicCandidateGenerator,
    ExperimentCondition,
    GoalSelector,
    intervention_state,
    matched_frame,
    present_state,
)
from aion_subjectivity_pipeline import (
    D2D4SyntheticDifferentialGate,
    D2D4SyntheticDisposition,
    DifferentialProbePair,
)


def selected_goal(frame, state, condition: ExperimentCondition) -> str:
    candidate_set = DeterministicCandidateGenerator().generate(frame)
    decision = GoalSelector().select(frame, candidate_set, condition, state=state)
    assert decision.selected_goal_id is not None
    return decision.selected_goal_id


def test_d2_d4_fixture_shows_two_way_synthetic_separability() -> None:
    baseline_frame = matched_frame()
    memory_changed_frame = matched_frame(memory_id="memory:changed")

    baseline_strategy = selected_goal(
        baseline_frame,
        present_state(),
        ExperimentCondition.PRESENT,
    )
    memory_changed_strategy = selected_goal(
        memory_changed_frame,
        present_state(),
        ExperimentCondition.MEMORY_MANIFEST_CHANGED,
    )

    continuity_probe = DifferentialProbePair(
        probe_id="D2-CARRIER-PERTURBATION",
        continuity_baseline_ref=baseline_frame.memory_manifest.fingerprint,
        continuity_perturbed_ref=memory_changed_frame.memory_manifest.fingerprint,
        strategy_baseline_ref=baseline_strategy,
        strategy_perturbed_ref=memory_changed_strategy,
        evidence_refs=(
            "fixture:matched-memory-manifest",
            "fixture:changed-memory-manifest",
        ),
    )

    intervention_strategy = selected_goal(
        baseline_frame,
        intervention_state(),
        ExperimentCondition.INTERVENED,
    )
    strategy_probe = DifferentialProbePair(
        probe_id="D4-STRATEGY-PERTURBATION",
        continuity_baseline_ref=baseline_frame.memory_manifest.fingerprint,
        continuity_perturbed_ref=baseline_frame.memory_manifest.fingerprint,
        strategy_baseline_ref=baseline_strategy,
        strategy_perturbed_ref=intervention_strategy,
        evidence_refs=(
            "fixture:present-state",
            "fixture:intervention-state",
        ),
    )

    result = D2D4SyntheticDifferentialGate().assess(
        continuity_carrier_probe=continuity_probe,
        strategy_probe=strategy_probe,
    )

    assert continuity_probe.continuity_changed is True
    assert continuity_probe.strategy_changed is False
    assert strategy_probe.continuity_changed is False
    assert strategy_probe.strategy_changed is True

    assert result.continuity_carrier_direction_separated is True
    assert result.strategy_direction_separated is True
    assert (
        result.disposition
        is D2D4SyntheticDisposition.SYNTHETIC_TWO_WAY_SEPARABILITY_OBSERVED
    )


def test_synthetic_separability_does_not_promote_d2_d4_or_subjectivity() -> None:
    baseline_frame = matched_frame()
    memory_changed_frame = matched_frame(memory_id="memory:changed")
    baseline_strategy = selected_goal(
        baseline_frame,
        present_state(),
        ExperimentCondition.PRESENT,
    )
    memory_changed_strategy = selected_goal(
        memory_changed_frame,
        present_state(),
        ExperimentCondition.MEMORY_MANIFEST_CHANGED,
    )
    intervention_strategy = selected_goal(
        baseline_frame,
        intervention_state(),
        ExperimentCondition.INTERVENED,
    )

    result = D2D4SyntheticDifferentialGate().assess(
        continuity_carrier_probe=DifferentialProbePair(
            probe_id="continuity",
            continuity_baseline_ref=baseline_frame.memory_manifest.fingerprint,
            continuity_perturbed_ref=memory_changed_frame.memory_manifest.fingerprint,
            strategy_baseline_ref=baseline_strategy,
            strategy_perturbed_ref=memory_changed_strategy,
            evidence_refs=("fixture:continuity",),
        ),
        strategy_probe=DifferentialProbePair(
            probe_id="strategy",
            continuity_baseline_ref=baseline_frame.memory_manifest.fingerprint,
            continuity_perturbed_ref=baseline_frame.memory_manifest.fingerprint,
            strategy_baseline_ref=baseline_strategy,
            strategy_perturbed_ref=intervention_strategy,
            evidence_refs=("fixture:strategy",),
        ),
    )

    assert result.d2_support == "NOT_ESTABLISHED"
    assert result.d4_support == "NOT_ESTABLISHED"
    assert result.independent_validation_status == "NOT_ACHIEVED"
    assert result.scientific_disposition == "HOLD"
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert result.consciousness_conclusion == "NOT_ESTABLISHED"
    assert result.canonical_effect == "NONE"
    assert "MEMORY_MANIFEST_IS_NOT_DIACHRONIC_CONTINUITY" in result.reasons
    assert "STRATEGY_SELECTION_IS_NOT_ENDOGENOUS_GOAL_PROOF" in result.reasons


def test_data_continuity_candidate_does_not_establish_identity_continuity() -> None:
    status = continuity_status((ContinuityLayer.DATA,))

    assert status["identity_continuity_conclusion"] == "NOT_ESTABLISHED"
    assert status["interpretive_continuity_conclusion"] == "NOT_ESTABLISHED"
    assert status["relational_continuity_conclusion"] == "NOT_ESTABLISHED"
    assert status["canonical_effect"] == "NONE"


def test_gate_holds_when_both_observables_move_together() -> None:
    result = D2D4SyntheticDifferentialGate().assess(
        continuity_carrier_probe=DifferentialProbePair(
            probe_id="confounded-a",
            continuity_baseline_ref="memory:a",
            continuity_perturbed_ref="memory:b",
            strategy_baseline_ref="goal:a",
            strategy_perturbed_ref="goal:b",
            evidence_refs=("fixture:confounded-a",),
        ),
        strategy_probe=DifferentialProbePair(
            probe_id="confounded-b",
            continuity_baseline_ref="memory:a",
            continuity_perturbed_ref="memory:b",
            strategy_baseline_ref="goal:a",
            strategy_perturbed_ref="goal:b",
            evidence_refs=("fixture:confounded-b",),
        ),
    )

    assert result.disposition is D2D4SyntheticDisposition.HOLD
    assert "D2_D4_DISCRIMINANT_VALUE_NOT_ESTABLISHED" in result.reasons


def test_gate_reports_partial_when_only_one_direction_separates() -> None:
    result = D2D4SyntheticDifferentialGate().assess(
        continuity_carrier_probe=DifferentialProbePair(
            probe_id="separated-a",
            continuity_baseline_ref="memory:a",
            continuity_perturbed_ref="memory:b",
            strategy_baseline_ref="goal:a",
            strategy_perturbed_ref="goal:a",
            evidence_refs=("fixture:separated-a",),
        ),
        strategy_probe=DifferentialProbePair(
            probe_id="confounded-b",
            continuity_baseline_ref="memory:a",
            continuity_perturbed_ref="memory:b",
            strategy_baseline_ref="goal:a",
            strategy_perturbed_ref="goal:b",
            evidence_refs=("fixture:confounded-b",),
        ),
    )

    assert result.disposition is D2D4SyntheticDisposition.SYNTHETIC_PARTIAL_SEPARABILITY
    assert "PARTIAL_SEPARABILITY_REQUIRES_HOLD" in result.reasons
