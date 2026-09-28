from __future__ import annotations

from dataclasses import replace

import pytest

from aion_human_ai_longitudinal import StudyError
from aion_human_ai_longitudinal.ccts_human_epistemic_agency import (
    HumanAgencyCondition,
    ccts_human_agency_condition_content_sha256,
    ccts_manifest_snapshot_sha256,
)
from aion_human_ai_longitudinal.learning_contrast_design import (
    AssessmentEvent,
    AssessmentTimepoint,
    ComparatorRole,
    ComponentInformation,
    ComponentTransform,
    FalsifierOutcome,
    LearningContrastArm,
    LearningContrastDesign,
    PresentationPlan,
    RelationSourceRole,
    RelationVisibility,
    RepresentationCondition,
    audit_learning_contrast_design,
    render_practice_protocol,
)

import test_ccts_human_epistemic_agency as agency_fixture
import test_task_selection_exposure_hardened as exposure_fixture


def design() -> LearningContrastDesign:
    exposure = exposure_fixture.audit()
    unit = exposure.units[0]
    paired_unit = next(
        item for item in exposure.units if item.pair_id == unit.pair_id and item.unit_id != unit.unit_id
    )
    identities = {item.unit_id: item for item in exposure.execution_identities}
    episode = unit.realized_exposure_trace[2]
    held_out = next(item for item in exposure.within_family_held_out_tasks if item.task_domain is episode.task_domain)
    task = exposure_fixture.artifact("task", "synthetic relation task")
    rubric = exposure_fixture.artifact("rubric", "synthetic relation rubric")
    provenance = exposure_fixture.artifact("provenance", "synthetic source roles")
    components = (
        ComponentInformation("component:a", exposure_fixture.artifact("component:a", "known component A")),
        ComponentInformation("component:b", exposure_fixture.artifact("component:b", "known component B")),
    )
    target_relation = exposure_fixture.artifact("target-relation", "synthetic target relation")
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

    component_ids = tuple(item.component_id for item in components)
    presentation_by_condition = {
        RepresentationCondition.DIRECT_ANSWER: PresentationPlan(
            component_ids,
            ComponentTransform.ORIGINAL,
            RelationVisibility.PRESENTED,
            RelationSourceRole.AI,
            False,
        ),
        RepresentationCondition.REPETITION: PresentationPlan(
            component_ids,
            ComponentTransform.VERBATIM_REPEAT,
            RelationVisibility.WITHHELD,
            RelationSourceRole.UNKNOWN,
            False,
        ),
        RepresentationCondition.RE_REPRESENTATION: PresentationPlan(
            component_ids,
            ComponentTransform.REORGANIZE_EXISTING,
            RelationVisibility.WITHHELD,
            RelationSourceRole.UNKNOWN,
            False,
        ),
        RepresentationCondition.RE_REPRESENTATION_PLUS_HUMAN_JUDGMENT: PresentationPlan(
            component_ids,
            ComponentTransform.REORGANIZE_EXISTING,
            RelationVisibility.WITHHELD,
            RelationSourceRole.UNKNOWN,
            True,
        ),
    }
    arms = []
    for condition in RepresentationCondition:
        arms.append(
            LearningContrastArm(
                arm_id=f"ccts:{condition.value}",
                condition=condition,
                comparator_role=ComparatorRole.CCTS,
                presentation=presentation_by_condition[condition],
                task_domain=episode.task_domain,
                task_family=episode.task_family_artifact,
                task_payload=task,
                exposure_content=episode.exposure_payload_artifact,
                exposure_intensity=unit.exposure_unit_definition,
                prior_knowledge=unit.prior_knowledge_control,
                evaluator=unit.evaluator_payload,
                rubric=rubric,
                provenance=provenance,
                execution_identity=identities[unit.unit_id],
                ccts_manifest_snapshot_sha256=snapshot,
            )
        )
    comparator_identity = identities[paired_unit.unit_id]
    comparator_presentation = presentation_by_condition[
        RepresentationCondition.RE_REPRESENTATION_PLUS_HUMAN_JUDGMENT
    ]
    practice = exposure_fixture.artifact(
        "practice",
        render_practice_protocol(comparator_presentation, comparator_identity),
    )
    arms.append(
        replace(
            arms[-1],
            arm_id="practice:matched",
            comparator_role=ComparatorRole.NON_CCTS_PRACTICE,
            ccts_manifest_snapshot_sha256=None,
            practice_protocol=practice,
            execution_identity=comparator_identity,
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
        component_information=components,
        target_relation_payload=target_relation,
        arms=tuple(arms),
        assessments=events,
        falsifier=exposure_fixture.artifact(
            "falsifier",
            "If re-representation does not outperform matched controls on independent explanation or delayed assessment, its incremental role is weakened.",
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


def test_human_judgment_is_not_relabelled_as_human_relation_origin() -> None:
    value = design()
    direct = value.arms[0].presentation
    judgment = value.arms[3].presentation
    assert direct.relation_visibility is RelationVisibility.PRESENTED
    assert direct.relation_source_role is RelationSourceRole.AI
    assert direct.human_judgment_required is False
    assert judgment.relation_visibility is RelationVisibility.WITHHELD
    assert judgment.relation_source_role is RelationSourceRole.UNKNOWN
    assert judgment.human_judgment_required is True

    with pytest.raises(StudyError, match="withheld relation"):
        replace(judgment, relation_source_role=RelationSourceRole.HUMAN)


def test_representation_conditions_require_distinct_typed_presentation_semantics() -> None:
    value = design()
    repeated = value.arms[1].presentation
    rerepresented = value.arms[2].presentation
    assert repeated.component_transform is ComponentTransform.VERBATIM_REPEAT
    assert rerepresented.component_transform is ComponentTransform.REORGANIZE_EXISTING

    bad = replace(rerepresented, component_transform=ComponentTransform.VERBATIM_REPEAT)
    with pytest.raises(StudyError, match="presentation plan"):
        replace(value.arms[2], presentation=bad)


def test_extra_or_missing_component_information_fails_closed() -> None:
    value = design()
    extra = replace(
        value.arms[2],
        presentation=replace(
            value.arms[2].presentation,
            component_ids=value.arms[2].presentation.component_ids + ("component:new",),
        ),
    )
    with pytest.raises(StudyError, match="declared component-information set"):
        audited(replace(value, arms=value.arms[:2] + (extra,) + value.arms[3:]))
    missing = replace(
        value.arms[1],
        presentation=replace(
            value.arms[1].presentation,
            component_ids=value.arms[1].presentation.component_ids[:-1],
        ),
    )
    with pytest.raises(StudyError, match="declared component-information set"):
        audited(replace(value, arms=(value.arms[0], missing) + value.arms[2:]))


def test_target_relation_payload_is_separate_from_component_information() -> None:
    value = design()
    with pytest.raises(StudyError, match="target relation payload"):
        replace(value, target_relation_payload=value.component_information[0].payload)


def test_missing_or_mismatched_comparator_holds() -> None:
    value = design()
    with pytest.raises(StudyError, match="matched non-CCTS practice comparator"):
        audited(replace(value, arms=value.arms[:-1]))
    bad = replace(value.arms[-1], exposure_content=exposure_fixture.artifact("drift", "drift"))
    with pytest.raises(StudyError, match="exposure content"):
        audited(replace(value, arms=value.arms[:-1] + (bad,)))


def test_comparator_requires_distinct_verified_execution_and_practice_protocol() -> None:
    value = design()
    reused_execution = replace(
        value.arms[-1],
        execution_identity=value.arms[0].execution_identity,
    )
    with pytest.raises(StudyError, match="distinct verified execution identity"):
        audited(replace(value, arms=value.arms[:-1] + (reused_execution,)))

    with pytest.raises(StudyError, match="practice protocol"):
        replace(value.arms[-1], practice_protocol=None)

    bad_protocol = replace(
        value.arms[-1],
        practice_protocol=value.component_information[0].payload,
    )
    with pytest.raises(StudyError, match="practice protocol"):
        audited(replace(value, arms=value.arms[:-1] + (bad_protocol,)))

    leaky_protocol = exposure_fixture.artifact(
        "practice:leaky",
        value.arms[-1].practice_protocol.content_utf8 + "\nNEW_COMPONENT_FACT=smuggled",
    )
    leaky = replace(value.arms[-1], practice_protocol=leaky_protocol)
    with pytest.raises(StudyError, match="canonically bind"):
        audited(replace(value, arms=value.arms[:-1] + (leaky,)))

    rebound_identity = value.arms[0].execution_identity
    rebound_protocol = exposure_fixture.artifact(
        "practice:rebound",
        render_practice_protocol(value.arms[-1].presentation, rebound_identity),
    )
    rebound = replace(
        value.arms[-1],
        execution_identity=rebound_identity,
        practice_protocol=rebound_protocol,
    )
    with pytest.raises(StudyError, match="distinct verified execution identity"):
        audited(replace(value, arms=value.arms[:-1] + (rebound,)))


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


def test_held_out_payload_cannot_equal_target_relation_payload() -> None:
    value = design()
    bad = replace(value, target_relation_payload=value.held_out_task.task_payload_artifact)
    with pytest.raises(StudyError, match="held-out"):
        audited(bad)


def test_required_artifact_must_be_content_addressed() -> None:
    with pytest.raises(StudyError, match="sha256_digest"):
        exposure_fixture.BoundArtifact("bad", "contents", "0" * 64)
    with pytest.raises(StudyError, match="component payload"):
        ComponentInformation("bad", "not an artifact")  # type: ignore[arg-type]


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
