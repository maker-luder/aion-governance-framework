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
from aion_astra_twin_embodiment.teacher_body_model import (
    build_teacher_body_model_profile,
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

    assert complete.status == "COMPLETE_DECLARED_REFERENCE_BASELINE"
    assert complete.causal_absence_interpretation == (
        "ELIGIBLE_FOR_CONTROLLED_PERTURBATION"
    )
    assert complete.completeness_scope == "DECLARED_REFERENCE_CONTRACT_ONLY"
    assert complete.global_human_body_completeness_status == "NOT_ESTABLISHED"
    assert complete.intrinsic_absence_conclusion == "NOT_ESTABLISHED"

    changed = tuple(
        replace(item, materialized=False)
        if item.capability_id == "HOMEOSTATIC_REGULATION"
        else item
        for item in capabilities
    )
    incomplete = assess_teacher_reference_completeness(changed)

    assert incomplete.status == "INCOMPLETE_DECLARED_REFERENCE_BASELINE"
    assert "HOMEOSTATIC_REGULATION" in incomplete.missing_required_capabilities
    assert incomplete.intrinsic_absence_conclusion == "NOT_ESTABLISHED"
    assert incomplete.causal_absence_interpretation == (
        "HOLD_INCOMPLETE_DECLARED_REFERENCE_BASELINE"
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

    assert assessment.status == "INCOMPLETE_DECLARED_REFERENCE_BASELINE"
    assert "VESTIBULAR" in assessment.missing_required_capabilities
    assert "VESTIBULAR" in assessment.missing_required_observation_channels
    assert "BODY_STATE_INTEGRATION" in assessment.missing_required_capabilities
    assert assessment.intrinsic_absence_conclusion == "NOT_ESTABLISHED"
    assert assessment.causal_absence_interpretation == (
        "HOLD_INCOMPLETE_DECLARED_REFERENCE_BASELINE"
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

    assert assessment.status == "INCOMPLETE_DECLARED_REFERENCE_BASELINE"
    assert (
        "PHYSIOLOGY_SYSTEM_CARDIOVASCULAR"
        in assessment.missing_required_capabilities
    )
    assert "ADULT_MALE_PHYSIOLOGY" in assessment.missing_required_capabilities


def test_new_reference_channel_groups_are_machine_verifiable() -> None:
    capabilities = build_teacher_reference_capabilities()
    capability_ids = {item.capability_id for item in capabilities}

    expected = {
        "PRURICEPTION",
        "VESTIBULAR_DYNAMICS",
        "MUSCULOSKELETAL_INTEROCEPTION",
        "OSMOTIC_ELECTROLYTE_REGULATION",
        "RESPIRATORY_WORKLOAD_REGULATION",
        "AUTONOMIC_STATE",
        "IMMUNE_INFLAMMATORY_STATE",
        "TISSUE_INJURY_REPAIR",
        "VISCERAL_DISTURBANCE",
        "FEEDING_HOMEOSTASIS",
        "ENDOCRINE_DYNAMICS",
    }
    assert expected.issubset(capability_ids)

    signals = build_teacher_body_signal_schema()
    dynamics = build_teacher_body_dynamics_profile(signals)
    without_pruriception = replace(
        signals,
        channels=tuple(
            channel
            for channel in signals.channels
            if channel.channel_id != "PRURICEPTIVE_REFERENCE"
        ),
    )
    assessment = assess_teacher_reference_completeness(
        build_teacher_reference_capabilities(
            signal_schema=without_pruriception,
            dynamics=dynamics,
        )
    )

    assert assessment.status == "INCOMPLETE_DECLARED_REFERENCE_BASELINE"
    assert "PRURICEPTION" in assessment.missing_required_capabilities
    assert "PRURICEPTION" in assessment.missing_required_observation_channels
    assert assessment.global_human_body_completeness_status == "NOT_ESTABLISHED"


def test_body_model_capabilities_are_part_of_declared_completeness() -> None:
    capabilities = build_teacher_reference_capabilities()
    capability_ids = {item.capability_id for item in capabilities}

    assert {
        "BODY_SCHEMA_MODEL",
        "PERIPERSONAL_SPACE",
        "MULTISENSORY_INTEGRATION",
        "ALLOSTATIC_REGULATION",
        "BODY_MODEL_PLASTICITY",
    }.issubset(capability_ids)

    body_model = build_teacher_body_model_profile()
    broken = replace(
        body_model,
        peripersonal_zones=(),
    )
    assessment = assess_teacher_reference_completeness(
        build_teacher_reference_capabilities(body_model=broken)
    )

    assert assessment.status == "INCOMPLETE_DECLARED_REFERENCE_BASELINE"
    assert "PERIPERSONAL_SPACE" in assessment.missing_required_capabilities


def test_feeding_and_endocrine_groups_fail_declared_completeness_when_missing() -> None:
    signals = build_teacher_body_signal_schema()
    dynamics = build_teacher_body_dynamics_profile(signals)
    broken = replace(
        signals,
        channels=tuple(
            channel
            for channel in signals.channels
            if channel.channel_id != "SATIATION_SIGNAL_REFERENCE"
        ),
    )
    assessment = assess_teacher_reference_completeness(
        build_teacher_reference_capabilities(
            signal_schema=broken,
            dynamics=dynamics,
        )
    )

    assert assessment.status == "INCOMPLETE_DECLARED_REFERENCE_BASELINE"
    assert "FEEDING_HOMEOSTASIS" in assessment.missing_required_capabilities
    assert "FEEDING_HOMEOSTASIS" in assessment.missing_required_observation_channels


def test_invalid_body_model_structure_fails_declared_completeness() -> None:
    body_model = build_teacher_body_model_profile()
    broken_zone = replace(
        body_model.peripersonal_zones[0],
        anchor_id="UNKNOWN_ANCHOR",
    )
    broken = replace(
        body_model,
        peripersonal_zones=(broken_zone,) + body_model.peripersonal_zones[1:],
    )
    assessment = assess_teacher_reference_completeness(
        build_teacher_reference_capabilities(body_model=broken)
    )

    assert assessment.status == "INCOMPLETE_DECLARED_REFERENCE_BASELINE"
    assert "PERIPERSONAL_SPACE" in assessment.missing_required_capabilities


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
    assert surface.body_model_profile_id == "CHATGPT_TEACHER_BODY_MODEL_v0.1"
    assert surface.subjectivity_status == "NOT_ESTABLISHED"
    assert surface.phenomenal_experience_status == "NOT_ESTABLISHED"
    assert all(candidate.falsifier for candidate in surface.candidates)
    assert all(candidate.claim_ceiling for candidate in surface.candidates)
