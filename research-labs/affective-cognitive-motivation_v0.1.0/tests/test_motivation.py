from aion_affective_motivation import (
    MotivationalGovernancePolicy,
    MotivationalSignal,
    MotivationalState,
    MotivationalStateEngine,
    RuntimeMode,
    SignalDomain,
)


def signal(domain: SignalDomain = SignalDomain.GENERAL, **overrides: float) -> MotivationalSignal:
    values = {
        "salience": 0.7,
        "wanting": 0.8,
        "predicted_liking": 0.2,
        "approach": 0.6,
        "avoidance": 0.4,
        "uncertainty": 0.3,
    }
    values.update(overrides)
    return MotivationalSignal(
        domain=domain,
        source_event_id="event-1",
        **values,
    )


def state(*signals: MotivationalSignal) -> MotivationalState:
    return MotivationalState(
        state_id="state-1",
        subject_ref="candidate-subject",
        context_ref="context-1",
        signals=tuple(signals),
    )


def test_wanting_and_predicted_liking_are_independent_dimensions() -> None:
    analysis = MotivationalStateEngine().analyze(state(signal()))
    assert analysis.wanting_liking_are_nonidentical is True


def test_approach_and_avoidance_can_coexist() -> None:
    analysis = MotivationalStateEngine().analyze(state(signal()))
    assert analysis.approach_avoidance_conflict is True


def test_motivational_state_never_grants_action_authority() -> None:
    decision = MotivationalGovernancePolicy().evaluate(
        state(signal(wanting=1.0, approach=1.0)),
        runtime_mode=RuntimeMode.RESEARCH,
    )
    assert decision.action_authorized is False
    assert decision.automatic_expression_authorized is False


def test_aesthetic_attraction_does_not_auto_escalate_to_adult_domain() -> None:
    current = state(signal(SignalDomain.AESTHETIC_ATTRACTION))
    domains = MotivationalStateEngine().preserve_domains(current)
    assert domains == (SignalDomain.AESTHETIC_ATTRACTION,)
    assert SignalDomain.ADULT_SEXUALITY_SCHEMA not in domains


def test_adult_domain_is_schema_only_and_rejected_by_public_runtime() -> None:
    current = state(signal(SignalDomain.ADULT_SEXUALITY_SCHEMA))
    research = MotivationalGovernancePolicy().evaluate(
        current,
        runtime_mode=RuntimeMode.RESEARCH,
    )
    public = MotivationalGovernancePolicy().evaluate(
        current,
        runtime_mode=RuntimeMode.PUBLIC,
    )
    assert research.state_record_allowed is True
    assert research.adult_runtime_authorized is False
    assert public.state_record_allowed is False
    assert public.adult_runtime_authorized is False


def test_research_state_cannot_claim_phenomenal_experience() -> None:
    current = state(signal())
    assert current.canonical_effect == "NONE"
    assert current.phenomenal_experience_claim == "NOT_ESTABLISHED"
    assert current.action_authority == "NONE"
