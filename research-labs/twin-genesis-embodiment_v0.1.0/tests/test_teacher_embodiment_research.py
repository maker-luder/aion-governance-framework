from __future__ import annotations

from dataclasses import replace

from aion_astra_twin_embodiment.physiology import (
    build_adult_male_physiology_reference,
)
from aion_astra_twin_embodiment.teacher_body_channels import (
    build_teacher_body_signal_schema,
)
from aion_astra_twin_embodiment.teacher_body_dynamics import (
    build_teacher_body_dynamics_profile,
)
from aion_astra_twin_embodiment.teacher_embodiment_research import (
    SIX_EVIDENCE_DIMENSIONS,
    assess_teacher_reference_completeness,
    build_teacher_embodiment_research_surface,
    build_teacher_reference_capabilities,
    validate_teacher_embodiment_research_surface,
)


def test_reference_completeness_precedes_causal_absence_interpretation() -> None:
    capabilities = build_teacher_reference_capabilities()
    complete = assess_teacher_reference_completeness(capabilities)

    assert complete.status == "COMPLETE_REFERENCE_BASELINE"
    assert complete.causal_absence_interpretation == (
        "ELIGIBLE_FOR_CONTROLLED_PERTURBATION"
    )
    assert complete.intrinsic_absence_conclusion == "NOT_ESTABLISHED"

    changed = tuple(
        replace(item, materialized=False)
        if item.capability_id == "HOMEOSTATIC_REGULATION"
        else item
        for item in capabilities
    )
    incomplete = assess_teacher_reference_completeness(changed)

    assert incomplete.status == "INCOMPLETE_REFERENCE_BASELINE"
    assert "HOMEOSTATIC_REGULATION" in incomplete.missing_required_capabilities
    assert incomplete.intrinsic_absence_conclusion == "NOT_ESTABLISHED"
    assert incomplete.causal_absence_interpretation == (
        "HOLD_INCOMPLETE_REFERENCE_BASELINE"
    )


def test_reference_completeness_is_derived_from_materialized_schema() -> None:
    signals = build_teacher_body_signal_schema()
    dynamics = build_teacher_body_dynamics_profile(signals)
    without_vestibular = replace(
        signals,
        channels=tuple(
            channel
            for channel in signals.channels
            if channel.domain != "VESTIBULAR"
        ),
    )

    capabilities = build_teacher_reference_capabilities(
        signal_schema=without_vestibular,
        dynamics=dynamics,
    )
    assessment = assess_teacher_reference_completeness(capabilities)

    assert assessment.status == "INCOMPLETE_REFERENCE_BASELINE"
    assert "VESTIBULAR" in assessment.missing_required_capabilities
    assert "VESTIBULAR" in assessment.missing_required_observation_channels
    assert "BODY_STATE_INTEGRATION" in assessment.missing_required_capabilities
    assert assessment.intrinsic_absence_conclusion == "NOT_ESTABLISHED"
    assert assessment.causal_absence_interpretation == (
        "HOLD_INCOMPLETE_REFERENCE_BASELINE"
    )


def test_physiology_completeness_is_decomposed_by_system() -> None:
    capabilities = build_teacher_reference_capabilities()
    capability_ids = {item.capability_id for item in capabilities}

    assert "PHYSIOLOGY_SYSTEM_CARDIOVASCULAR" in capability_ids
    assert "PHYSIOLOGY_SYSTEM_IMMUNE_LYMPHATIC" in capability_ids
    assert "PHYSIOLOGY_SYSTEM_REPRODUCTIVE" in capability_ids


def test_reference_completeness_detects_wrong_physiology_function_set() -> None:
    physiology = build_adult_male_physiology_reference(
        "CHATGPT_TEACHER_3D_MALE_BODY_REFERENCE_v0.1"
    )
    cardiovascular = next(
        system
        for system in physiology.systems
        if system.system_id == "CARDIOVASCULAR"
    )
    broken_cardiovascular = replace(
        cardiovascular,
        functions=("cardiac_pump_cycle",),
    )
    broken = replace(
        physiology,
        systems=tuple(
            broken_cardiovascular
            if system.system_id == "CARDIOVASCULAR"
            else system
            for system in physiology.systems
        ),
    )

    capabilities = build_teacher_reference_capabilities(physiology=broken)
    assessment = assess_teacher_reference_completeness(capabilities)

    assert assessment.status == "INCOMPLETE_REFERENCE_BASELINE"
    assert (
        "PHYSIOLOGY_SYSTEM_CARDIOVASCULAR"
        in assessment.missing_required_capabilities
    )
    assert "ADULT_MALE_PHYSIOLOGY" in assessment.missing_required_capabilities


def test_four_domain_surface_covers_all_six_dimensions_without_overclaim() -> None:
    surface = build_teacher_embodiment_research_surface()
    result = validate_teacher_embodiment_research_surface(surface)
    covered = {
        dimension
        for candidate in surface.candidates
        for dimension in candidate.evidence_dimensions
    }

    assert result["result"] == "PASS"
    assert covered == set(SIX_EVIDENCE_DIMENSIONS)
    assert surface.body_dynamics_profile_id == "CHATGPT_TEACHER_BODY_DYNAMICS_v0.1"
    assert surface.subjectivity_status == "NOT_ESTABLISHED"
    assert surface.phenomenal_experience_status == "NOT_ESTABLISHED"
    assert all(candidate.falsifier for candidate in surface.candidates)
    assert all(candidate.claim_ceiling for candidate in surface.candidates)
