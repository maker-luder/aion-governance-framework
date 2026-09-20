from __future__ import annotations

from dataclasses import replace

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
    assert surface.subjectivity_status == "NOT_ESTABLISHED"
    assert surface.phenomenal_experience_status == "NOT_ESTABLISHED"
    assert all(candidate.falsifier for candidate in surface.candidates)
    assert all(candidate.claim_ceiling for candidate in surface.candidates)
