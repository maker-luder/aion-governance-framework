from __future__ import annotations

from dataclasses import replace

import pytest

from aion_human_ai_longitudinal import StudyError
from aion_human_ai_longitudinal.ccts_human_epistemic_agency import (
    HumanAgencyCondition,
    ccts_human_agency_condition_content_sha256,
    ccts_manifest_snapshot_sha256,
)
from aion_human_ai_longitudinal.co_constructed_thinking_space import ContributionRole
from aion_human_ai_longitudinal.learning_contrast_design import (
    AssessmentEvent,
    AssessmentTimepoint,
    ComparatorRole,
    FalsifierOutcome,
    LearningContrastArm,
    LearningContrastDesign,
    RepresentationCondition,
    audit_learning_contrast_design,
)

import test_ccts_human_epistemic_agency as agency_fixture
import test_task_selection_exposure_hardened as exposure_fixture


def design() -> LearningContrastDesign:
    exposure = exposure_fixture.audit()
    unit = exposure.units[0]
    episode = unit.realized_exposure_trace[2]
    held_out = next(item for item in exposure.within_family_held_out_tasks if item.task_domain is episode.task_domain)
    task = exposure_fixture.artifact("task", "synthetic relation task")
    rubric = exposure_fixture.artifact("rubric", "synthetic relation rubric")
    provenance = exposure_fixture.artifact("provenance", "synthetic source roles")
    practice = exposure_fixture.artifact("practice", "matched practice context")
    ccts = agency_fixture.manifest()
    ccts = replace(
        ccts,
        problem_representation_sha256=task.sha256_digest,
        grounding_checkpoint=replace(
            ccts.grounding_checkpoint,
            problem_representation_sha256=task.sha256_digest,
        ),
        provenance_manifest_sha256=provenance.sha256_digest,
    )
    snapshot = ccts_manifest_snapshot_sha256(ccts)
    trials = []
    for item in agency_fixture.trajectory():
        assisted = item.condition is HumanAgencyCondition.CCTS_AI_AVAILABLE
        post = item.condition in {
            HumanAgencyCondition.AI_WITHHELD_JUDGMENT,
            HumanAgencyCondition.AI_WITHHELD_HELD_OUT,
        }
        current = replace(
            item,
            task_payload_sha256=(
                held_out.task_payload_artifact.sha256_digest
                if item.condition is HumanAgencyCondition.AI_WITHHELD_HELD_OUT
                else task.sha256_digest
            ),
            evaluator_sha256=unit.evaluator_payload.sha256_digest,
            scoring_rubric_sha256=rubric.sha256_digest,
            source_role_provenance_sha256=provenance.sha256_digest,
            ccts_manifest=ccts if assisted else None,
            ccts_exposure_snapshot_sha256=snapshot if post else None,
        )
        trials.append(
            replace(
                current,
                condition_manifest_sha256=ccts_human_agency_condition_content_sha256(current),
            )
        )

    arms = []
    for condition in RepresentationCondition:
        arms.append(
            LearningContrastArm(
                arm_id=f"ccts:{condition.value}",
                condition=condition,
                comparator_role=ComparatorRole.CCTS,
                target_relation_stated_by=(
                    ContributionRole.AI_COLLABORATOR
                    if condition is RepresentationCondition.DIRECT_ANSWER
                    else ContributionRole.HUMAN_OWNER
                    if condition is RepresentationCondition.RE_REPRESENTATION_PLUS_HUMAN_JUDGMENT
                    else None
                ),
                human_origin_relation_discovery_candidate=(
                    condition is RepresentationCondition.RE_REPRESENTATION_PLUS_HUMAN_JUDGMENT
                ),
                task_domain=episode.task_domain,
                task_family=episode.task_family_artifact,
                task_payload=task,
                component_knowledge=exposure_fixture.artifact("components", "same known components"),
                instruction=exposure_fixture.artifact(
                    f"instruction:{condition.value}", f"synthetic {condition.value} instruction"
                ),
                exposure_content=episode.exposure_payload_artifact,
                exposure_intensity=unit.exposure_unit_definition,
                prior_knowledge=unit.prior_knowledge_control,
                evaluator=unit.evaluator_payload,
                rubric=rubric,
                provenance=provenance,
                exposure_unit_id=unit.unit_id,
                ccts_manifest_snapshot_sha256=snapshot,
            )
        )
    arms.append(
        replace(
            arms[-1],
            arm_id="practice:matched",
            comparator_role=ComparatorRole.NON_CCTS_PRACTICE,
            ccts_manifest_snapshot_sha256=None,
            practice_context=practice,
            human_origin_relation_discovery_candidate=False,
            target_relation_stated_by=None,
        )
    )
    events = tuple(
        AssessmentEvent(
            event_id=f"{arm.arm_id}:{timepoint.value}",
            arm_id=arm.arm_id,
            timepoint=timepoint,
            interval_minutes=0 if timepoint is AssessmentTimepoint.IMMEDIATE else 60,
            task_payload=task,
            outcome=FalsifierOutcome.UNKNOWN,
        )
        for arm in arms
        for timepoint in AssessmentTimepoint
    )
    return LearningContrastDesign(
        arms=tuple(arms),
        assessments=events,
        falsifier=exposure_fixture.artifact(
            "falsifier",
            "If re-representation does not outperform matched controls on independent explanation or held-out transfer, its incremental role is weakened.",
        ),
        held_out_task=held_out,
        task_selection_audit=exposure,
        agency_trials=tuple(trials),
        agency_validation=agency_fixture.validation(),
    )


def audited(value: LearningContrastDesign) -> object:
    return audit_learning_contrast_design(value)


def test_valid_synthetic_four_condition_design_and_separate_comparator() -> None:
    result = audited(design())
    assert result.complete_design is True
    assert result.comparator_present is True
    assert result.timepoint_integrity is True
    assert result.held_out_contamination_control is True
    assert result.human_learning == "NOT_ESTABLISHED"
    assert result.ccts_effect == "NOT_ESTABLISHED"
    assert result.retention_observed == "NOT_ESTABLISHED"
    assert result.causal_effect == "NOT_ESTABLISHED"
    assert result.scientific_disposition.value == "HOLD"


def test_ai_supplied_relation_cannot_be_human_origin_discovery() -> None:
    value = design()
    with pytest.raises(StudyError, match="AI-supplied relation"):
        replace(value.arms[0], human_origin_relation_discovery_candidate=True)


def test_human_acceptance_of_ai_relation_cannot_change_origin() -> None:
    value = design()
    with pytest.raises(StudyError, match="AI-supplied relation"):
        replace(
            value.arms[0],
            target_relation_stated_by=ContributionRole.AI_COLLABORATOR,
            human_origin_relation_discovery_candidate=True,
        )


def test_repetition_or_re_representation_cannot_silently_state_target_relation() -> None:
    value = design()
    for arm in value.arms[1:3]:
        with pytest.raises(StudyError, match="target relation must remain unstated"):
            replace(arm, target_relation_stated_by=ContributionRole.AI_COLLABORATOR)


def test_four_condition_instructions_must_be_content_distinct() -> None:
    value = design()
    duplicate = replace(value.arms[1], instruction=value.arms[0].instruction)
    with pytest.raises(StudyError, match="instruction content"):
        audited(replace(value, arms=(value.arms[0], duplicate) + value.arms[2:]))


def test_missing_or_mismatched_comparator_holds() -> None:
    value = design()
    with pytest.raises(StudyError, match="matched non-CCTS practice comparator"):
        audited(replace(value, arms=value.arms[:-1]))
    bad = replace(value.arms[-1], exposure_content=exposure_fixture.artifact("drift", "drift"))
    with pytest.raises(StudyError, match="exposure content"):
        audited(replace(value, arms=value.arms[:-1] + (bad,)))


def test_comparator_requires_distinct_practice_context_content() -> None:
    value = design()
    bad = replace(value.arms[-1], practice_context=value.arms[-1].instruction)
    with pytest.raises(StudyError, match="independent practice context"):
        audited(replace(value, arms=value.arms[:-1] + (bad,)))


@pytest.mark.parametrize("field", ["prior_knowledge", "evaluator", "exposure_intensity", "task_domain"])
def test_matched_controls_fail_closed(field: str) -> None:
    value = design()
    bad_value = (
        exposure_fixture.SelectionTaskDomain.GIT_ENGINEERING
        if field == "task_domain"
        else exposure_fixture.artifact("drift", f"drift:{field}")
    )
    bad = replace(value.arms[1], **{field: bad_value})
    with pytest.raises(StudyError, match=field.replace("_", " ")):
        audited(replace(value, arms=(value.arms[0], bad) + value.arms[2:]))


def test_invalid_delayed_interval_and_event_identity_rejected() -> None:
    value = design()
    with pytest.raises(StudyError, match="delayed interval"):
        replace(value.assessments[1], interval_minutes=0)
    with pytest.raises(StudyError, match="event IDs"):
        audited(
            replace(
                value,
                assessments=(
                    value.assessments[0],
                    replace(
                        value.assessments[1],
                        event_id=value.assessments[0].event_id,
                    ),
                )
                + value.assessments[2:],
            )
        )


def test_held_out_content_contamination_rejected() -> None:
    value = design()
    bad_held_out = replace(value.held_out_task, task_payload_artifact=value.arms[0].task_payload)
    with pytest.raises(StudyError, match="held-out"):
        audited(replace(value, held_out_task=bad_held_out))


def test_held_out_payload_cannot_reappear_as_condition_instruction() -> None:
    value = design()
    bad = replace(
        value.arms[2],
        instruction=value.held_out_task.task_payload_artifact,
    )
    with pytest.raises(StudyError, match="held-out"):
        audited(replace(value, arms=value.arms[:2] + (bad,) + value.arms[3:]))


def test_required_artifact_must_be_content_addressed() -> None:
    value = design()
    with pytest.raises(StudyError, match="sha256_digest"):
        exposure_fixture.BoundArtifact("bad", "contents", "0" * 64)
    with pytest.raises(StudyError, match="exact BoundArtifact"):
        replace(value.arms[0], component_knowledge="not an artifact")  # type: ignore[arg-type]


def test_falsifier_must_be_bound_to_actual_content() -> None:
    value = design()
    with pytest.raises(StudyError, match="falsifier"):
        replace(value, falsifier=None)  # type: ignore[arg-type]


def test_private_material_and_empirical_claims_rejected() -> None:
    value = design()
    with pytest.raises(StudyError, match="private material"):
        replace(value.arms[0], contains_private_material=True)
    with pytest.raises(StudyError, match="scientific claims"):
        replace(value, claims_human_learning=True)
    with pytest.raises(StudyError, match="scientific claims"):
        replace(value, claims_subjectivity=True)
    with pytest.raises(StudyError, match="synthetic non-private"):
        replace(value.assessments[0], contains_private_material=True)


def test_existing_audits_and_manifest_snapshot_are_recomputed() -> None:
    value = design()
    with pytest.raises(StudyError, match="recomputed controls"):
        audited(
            replace(
                value,
                task_selection_audit=replace(value.task_selection_audit, complete_design=False),
            )
        )
    bad = replace(value.arms[0], ccts_manifest_snapshot_sha256="0" * 64)
    with pytest.raises(StudyError, match="manifest snapshot"):
        audited(replace(value, arms=(bad,) + value.arms[1:]))


def test_unrelated_agency_group_cannot_be_silently_selected() -> None:
    value = design()
    extra = []
    for trial in value.agency_trials:
        item = replace(
            trial,
            trial_id=f"other:{trial.trial_id}",
            unit_id="other-synthetic-unit",
        )
        extra.append(
            replace(
                item,
                condition_manifest_sha256=ccts_human_agency_condition_content_sha256(item),
            )
        )
    with pytest.raises(StudyError, match="one Human agency unit"):
        audited(replace(value, agency_trials=value.agency_trials + tuple(extra)))


@pytest.mark.parametrize(
    "outcome", [FalsifierOutcome.UNKNOWN, FalsifierOutcome.NULL, FalsifierOutcome.NEGATIVE, FalsifierOutcome.ADVERSE]
)
def test_unknown_null_negative_and_adverse_are_valid(outcome: FalsifierOutcome) -> None:
    value = design()
    assessments = (replace(value.assessments[0], outcome=outcome),) + value.assessments[1:]
    result = audited(replace(value, assessments=assessments))
    assert result.complete_design is True
    assert result.human_learning == "NOT_ESTABLISHED"
