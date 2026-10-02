from __future__ import annotations

from dataclasses import replace

import pytest

from aion_human_ai_longitudinal.ccts_validity_study_design import (
    AssessmentSourceRole,
    CCTSValidityStudyDesign,
    DiscriminantPlan,
    HybridNegative,
    NeighborConstruct,
    OutcomeCondition,
    OutcomeMeasure,
    OutcomePlan,
    audit_ccts_validity_study_design,
)
from aion_human_ai_longitudinal.ccts_human_epistemic_agency import HumanAgencyCondition
from aion_human_ai_longitudinal.harness import AdmissionDisposition, StudyError


def digest(character: str) -> str:
    return character * 64


def design() -> CCTSValidityStudyDesign:
    return CCTSValidityStudyDesign(
        study_id="synthetic-validity-design-001",
        discriminant=DiscriminantPlan(
            candidate_unit_ids=("ccts-case",),
            hard_negative_cases=tuple((neighbor, f"{neighbor.value}-case") for neighbor in NeighborConstruct),
            hybrid_negative_cases=tuple((kind, f"{kind.value}-case") for kind in HybridNegative),
            coding_manual_sha256=digest("a"),
            falsification_rule_sha256=digest("b"),
            independent_coder_ids=("coder-a", "coder-b"),
            coders_blind_to_candidate_label=True,
            coders_blind_to_outcome=True,
        ),
        outcome=OutcomePlan(
            condition_unit_ids=(
                (OutcomeCondition.CCTS, "ccts-outcome"),
                (OutcomeCondition.MATCHED_NON_CCTS, "practice-outcome"),
                (OutcomeCondition.HUMAN_ALONE, "human-outcome"),
                (OutcomeCondition.AI_ALONE, "ai-outcome"),
            ),
            primary_measure=OutcomeMeasure.INDEPENDENT_HUMAN_JUDGMENT,
            scoring_rule_sha256=digest("c"),
            held_out_task_sha256=digest("d"),
            independent_rater_ids=("rater-a", "rater-b"),
            raters_blind_to_ccts_status=True,
            exposure_matching_plan_sha256=digest("e"),
            baseline_covariate_plan_sha256=digest("f"),
            ai_quality_record_plan_sha256=digest("0"),
            assessment_delay_minutes=None,
            primary_assessment_condition=HumanAgencyCondition.AI_WITHHELD_JUDGMENT,
            primary_response_source=AssessmentSourceRole.HUMAN_PARTICIPANT,
        ),
    )


def test_complete_synthetic_design_separates_primary_questions_without_claim_promotion() -> None:
    audit = audit_ccts_validity_study_design(design())
    assert audit.discriminant_plan_complete is True
    assert audit.outcome_plan_complete is True
    assert audit.empirical_observations_present is False
    assert audit.ccts_validation == "NOT_ESTABLISHED"
    assert audit.human_learning == "NOT_ESTABLISHED"
    assert audit.retention == "NOT_ESTABLISHED"
    assert audit.transfer == "NOT_ESTABLISHED"
    assert audit.ccts_specific_effect == "NOT_ESTABLISHED"
    assert audit.causality == "NOT_ESTABLISHED"
    assert audit.human_ai_synergy == "NOT_ESTABLISHED"
    assert audit.scientific_disposition is AdmissionDisposition.HOLD
    assert audit.canonical_effect == "NONE"
    assert audit.deployment is False


def test_hard_negative_and_candidate_cannot_share_units() -> None:
    item = design()
    with pytest.raises(StudyError, match="disjoint"):
        replace(item.discriminant, hard_negative_cases=((NeighborConstruct.ITERATIVE_PROMPTING, "ccts-case"),))


def test_neighbor_coverage_and_blinding_are_visible_without_reclassifying_negative() -> None:
    item = design()
    negative = replace(item.discriminant, hard_negative_cases=item.discriminant.hard_negative_cases[:-1])
    audit = audit_ccts_validity_study_design(replace(item, discriminant=negative))
    assert audit.discriminant_plan_complete is False
    assert audit.outcome_plan_complete is True
    assert audit.ccts_validation == "NOT_ESTABLISHED"
    unblinded = replace(item.discriminant, coders_blind_to_candidate_label=False)
    assert audit_ccts_validity_study_design(replace(item, discriminant=unblinded)).discriminant_plan_complete is False


def test_both_hybrid_hard_negatives_are_required_for_discriminant_coverage() -> None:
    item = design()
    for omitted in HybridNegative:
        remaining = tuple(case for case in item.discriminant.hybrid_negative_cases if case[0] is not omitted)
        audit = audit_ccts_validity_study_design(replace(item, discriminant=replace(item.discriminant, hybrid_negative_cases=remaining)))
        assert audit.discriminant_plan_complete is False
    with pytest.raises(StudyError, match="disjoint"):
        replace(item.discriminant, hybrid_negative_cases=((HybridNegative.PROVENANCE_AUTHORITY_WITHOUT_RECIPROCAL_REVISION, "ccts-case"),))


def test_exact_neighbor_and_independent_coder_types_are_required() -> None:
    item = design()
    with pytest.raises(StudyError, match="NeighborConstruct"):
        replace(item.discriminant, hard_negative_cases=(("ITERATIVE_PROMPTING", "case"),))  # type: ignore[arg-type]
    with pytest.raises(StudyError, match="independent coders"):
        replace(item.discriminant, independent_coder_ids=("coder-a",))


def test_outcome_conditions_have_independent_units_and_all_comparators() -> None:
    item = design()
    with pytest.raises(StudyError, match="distinct unit"):
        replace(item.outcome, condition_unit_ids=((OutcomeCondition.CCTS, "same"), (OutcomeCondition.HUMAN_ALONE, "same")))
    incomplete = replace(item.outcome, condition_unit_ids=item.outcome.condition_unit_ids[:-1])
    audit = audit_ccts_validity_study_design(replace(item, outcome=incomplete))
    assert audit.outcome_plan_complete is False


def test_structural_status_is_not_an_independent_outcome() -> None:
    item = design()
    with pytest.raises(StudyError, match="OutcomeMeasure"):
        replace(item.outcome, primary_measure="CCTS_STATUS")  # type: ignore[arg-type]


def test_missing_confound_plan_and_blinding_leave_outcome_design_incomplete() -> None:
    item = design()
    incomplete = replace(
        item.outcome,
        ai_quality_record_plan_sha256=None,
        raters_blind_to_ccts_status=False,
    )
    audit = audit_ccts_validity_study_design(replace(item, outcome=incomplete))
    assert audit.discriminant_plan_complete is True
    assert audit.outcome_plan_complete is False


def test_delayed_retention_requires_declared_positive_interval() -> None:
    item = design()
    delayed = replace(item.outcome, primary_measure=OutcomeMeasure.DELAYED_RETENTION)
    assert audit_ccts_validity_study_design(replace(item, outcome=delayed)).outcome_plan_complete is False
    with pytest.raises(StudyError, match="positive"):
        replace(delayed, assessment_delay_minutes=0)
    assert audit_ccts_validity_study_design(
        replace(item, outcome=replace(delayed, assessment_delay_minutes=1440))
    ).outcome_plan_complete is True


def test_independent_human_outcome_requires_ai_withheld_human_response() -> None:
    item = design()
    assisted = replace(item.outcome, primary_assessment_condition=HumanAgencyCondition.CCTS_AI_AVAILABLE)
    assert audit_ccts_validity_study_design(replace(item, outcome=assisted)).outcome_plan_complete is False
    ai_sourced = replace(item.outcome, primary_response_source=AssessmentSourceRole.AI)
    assert audit_ccts_validity_study_design(replace(item, outcome=ai_sourced)).outcome_plan_complete is False
    held_out = replace(item.outcome, primary_measure=OutcomeMeasure.HELD_OUT_TRANSFER)
    assert audit_ccts_validity_study_design(replace(item, outcome=held_out)).outcome_plan_complete is False
    actual_held_out = replace(held_out, primary_assessment_condition=HumanAgencyCondition.AI_WITHHELD_HELD_OUT)
    assert audit_ccts_validity_study_design(replace(item, outcome=actual_held_out)).outcome_plan_complete is True


def test_coders_and_outcome_raters_must_be_distinct_people() -> None:
    item = design()
    with pytest.raises(StudyError, match="disjoint"):
        replace(item, outcome=replace(item.outcome, independent_rater_ids=("coder-a", "rater-b")))


def test_direct_audit_construction_cannot_promote_scientific_or_authority_claims() -> None:
    audit = audit_ccts_validity_study_design(design())
    for override in (
        {"ccts_validation": "ESTABLISHED"},
        {"human_learning": "ESTABLISHED"},
        {"empirical_observations_present": True},
        {"canonical_effect": "APPROVED"},
        {"deployment": True},
        {"scientific_disposition": "ADMIT"},
    ):
        with pytest.raises(StudyError, match="fixed scientific boundary"):
            replace(audit, **override)


def test_raw_strings_and_claims_cannot_be_smuggled_through_the_design() -> None:
    item = design()
    with pytest.raises(StudyError, match="OutcomeCondition"):
        replace(item.outcome, condition_unit_ids=(("CCTS", "unit"),))  # type: ignore[arg-type]
    with pytest.raises(StudyError, match="scientific claims"):
        replace(item, claims_human_learning=True)
    with pytest.raises(StudyError, match="exact bool"):
        replace(item.discriminant, coders_blind_to_outcome=1)  # type: ignore[arg-type]
