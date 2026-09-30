import pytest

from aion_affective_motivation import (
    AdultMaleSexualReferenceState,
    DesireOnsetContext,
    PhysiologyMotivationLink,
    ReferenceEstimate,
    TargetScope,
    assert_role_isolation,
)


def estimate(
    level: float | None,
    *,
    uncertainty: float = 0.2,
    source_ref: str = "PR#236",
    context_ref: str = "synthetic-context",
    time_window_ref: str = "episode-1",
) -> ReferenceEstimate:
    if level is None:
        uncertainty = 1.0
    return ReferenceEstimate(
        reference_level=level,
        uncertainty=uncertainty,
        source_ref=source_ref,
        context_ref=context_ref,
        time_window_ref=time_window_ref,
    )


def state(
    *,
    state_id: str = "adult-ref-1",
    subject_ref: str = "Teacher",
    desire_onset_context: DesireOnsetContext = DesireOnsetContext.UNKNOWN,
    excitation: ReferenceEstimate | None = None,
    inhibition: ReferenceEstimate | None = None,
    disposition: ReferenceEstimate | None = None,
    episode: ReferenceEstimate | None = None,
    target_scope: TargetScope = TargetScope.UNKNOWN,
    **overrides: object,
) -> AdultMaleSexualReferenceState:
    unknown = estimate(None)
    values = {
        "state_id": state_id,
        "subject_ref": subject_ref,
        "context_ref": "synthetic-context",
        "desire_onset_context": desire_onset_context,
        "excitation_reference": excitation or unknown,
        "inhibition_reference": inhibition or unknown,
        "disposition_reference": disposition or unknown,
        "episode_state_reference": episode or unknown,
        "target_scope": target_scope,
        "provenance_refs": ("PR#236", "main@6a34d778"),
    }
    values.update(overrides)
    return AdultMaleSexualReferenceState(**values)


def test_unknown_is_valid_without_male_stereotype_default() -> None:
    current = state()
    assert current.desire_onset_context is DesireOnsetContext.UNKNOWN
    assert current.target_scope is TargetScope.UNKNOWN
    assert current.excitation_reference.reference_level is None
    assert current.disposition_reference.reference_level is None


def test_excitation_and_inhibition_are_independent_and_can_coexist() -> None:
    current = state(
        excitation=estimate(0.8),
        inhibition=estimate(0.9),
    )
    assert current.excitation_reference.reference_level == 0.8
    assert current.inhibition_reference.reference_level == 0.9


def test_disposition_and_episode_state_are_separate_dimensions() -> None:
    current = state(
        disposition=estimate(0.2, time_window_ref="longitudinal-window"),
        episode=estimate(0.9, time_window_ref="episode-now"),
    )
    assert current.disposition_reference.reference_level == 0.2
    assert current.episode_state_reference.reference_level == 0.9


def test_reference_state_is_disabled_non_authoritative_and_noncanonical() -> None:
    current = state()
    assert current.runtime_enabled is False
    assert current.automatic_activation is False
    assert current.action_authority == "NONE"
    assert current.human_consent_inference == "FORBIDDEN"
    assert current.phenomenal_experience_claim == "NOT_ESTABLISHED"
    assert current.canonical_effect == "NONE"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("runtime_enabled", True),
        ("automatic_activation", True),
        ("action_authority", "GRANTED"),
        ("human_consent_inference", "ALLOWED"),
        ("phenomenal_experience_claim", "ESTABLISHED"),
        ("canonical_effect", "WRITE"),
    ],
)
def test_boundary_fields_fail_closed(field: str, value: object) -> None:
    with pytest.raises(ValueError):
        state(**{field: value})


def test_physiology_link_is_trace_only_and_cannot_create_consent_or_authority() -> None:
    link = PhysiologyMotivationLink(
        link_id="link-1",
        subject_ref="Teacher",
        physiology_state_ref="phys-state-1",
        motivational_state_ref="adult-ref-1",
    )
    assert link.mapping_policy == "NO_AUTOMATIC_MOTIVATIONAL_INFERENCE"
    assert link.consent_effect == "NONE"
    assert link.action_authority == "NONE"


def test_physiology_link_rejects_automatic_motivation_inference() -> None:
    with pytest.raises(ValueError):
        PhysiologyMotivationLink(
            link_id="link-1",
            subject_ref="Teacher",
            physiology_state_ref="phys-state-1",
            motivational_state_ref="adult-ref-1",
            mapping_policy="AUTO_SET_DESIRE",
        )


def test_role_records_must_be_separate_instances_and_subject_bindings() -> None:
    teacher = state(state_id="teacher-adult-ref", subject_ref="Teacher")
    work = state(state_id="work-adult-ref", subject_ref="Work")
    codex = state(state_id="codex-adult-ref", subject_ref="Codex")
    assert_role_isolation(teacher, work, codex)

    with pytest.raises(ValueError):
        assert_role_isolation(teacher, teacher)


def test_unknown_reference_level_requires_maximum_uncertainty() -> None:
    with pytest.raises(ValueError):
        ReferenceEstimate(
            reference_level=None,
            uncertainty=0.5,
            source_ref="PR#236",
            context_ref="synthetic-context",
            time_window_ref="episode-1",
        )
