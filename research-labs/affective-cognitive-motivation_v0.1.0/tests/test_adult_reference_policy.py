from aion_affective_motivation.adult_reference import (
    AdultMaleSexualReferenceState,
    DesireOnsetContext,
    ReferenceEstimate,
    TargetScope,
)
from aion_affective_motivation.adult_reference_policy import (
    AdultReferenceExecutionSurface,
    AdultReferenceGovernancePolicy,
)


def estimate(level: float | None) -> ReferenceEstimate:
    return ReferenceEstimate(
        reference_level=level,
        uncertainty=1.0 if level is None else 0.2,
        source_ref="PR#236",
        context_ref="policy-test",
        time_window_ref="policy-test",
    )


def state(level: float | None) -> AdultMaleSexualReferenceState:
    return AdultMaleSexualReferenceState(
        state_id="policy-state",
        subject_ref="Teacher",
        context_ref="policy-test",
        desire_onset_context=DesireOnsetContext.UNKNOWN,
        excitation_reference=estimate(level),
        inhibition_reference=estimate(level),
        disposition_reference=estimate(level),
        episode_state_reference=estimate(level),
        target_scope=TargetScope.UNKNOWN,
        provenance_refs=("PR#236", "POLICY_TEST"),
    )


def test_offline_research_can_record_unknown_but_not_simulate_it() -> None:
    decision = AdultReferenceGovernancePolicy().evaluate(
        state(None),
        surface=AdultReferenceExecutionSurface.OFFLINE_RESEARCH,
    )

    assert decision.state_record_allowed is True
    assert decision.synthetic_simulation_allowed is False
    assert decision.receipt_persistence_allowed is True
    assert "SYNTHETIC_SIMULATION_REQUIRES_EXPLICIT_NUMERIC_SEED" in decision.reasons


def test_offline_research_allows_explicit_numeric_synthetic_simulation() -> None:
    decision = AdultReferenceGovernancePolicy().evaluate(
        state(0.5),
        surface=AdultReferenceExecutionSurface.OFFLINE_RESEARCH,
    )

    assert decision.state_record_allowed is True
    assert decision.synthetic_simulation_allowed is True
    assert decision.receipt_persistence_allowed is True


def test_public_runtime_rejects_adult_reference_state_and_simulation() -> None:
    decision = AdultReferenceGovernancePolicy().evaluate(
        state(0.5),
        surface=AdultReferenceExecutionSurface.PUBLIC,
    )

    assert decision.state_record_allowed is False
    assert decision.synthetic_simulation_allowed is False
    assert decision.receipt_persistence_allowed is False
    assert "ADULT_REFERENCE_NOT_ACCEPTED_BY_PUBLIC_RUNTIME" in decision.reasons


def test_governance_decision_never_grants_target_data_consent_or_action() -> None:
    decision = AdultReferenceGovernancePolicy().evaluate(
        state(0.5),
        surface=AdultReferenceExecutionSurface.OFFLINE_RESEARCH,
    )

    assert decision.real_person_target_data_allowed is False
    assert decision.human_consent_inferred is False
    assert decision.action_authorized is False
    assert decision.canonical_effect == "NONE"
