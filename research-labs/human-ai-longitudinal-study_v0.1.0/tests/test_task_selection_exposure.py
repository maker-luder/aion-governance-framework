from __future__ import annotations

from dataclasses import replace
import hashlib

import pytest

from aion_human_ai_longitudinal import StudyError
from aion_human_ai_longitudinal.task_selection_exposure import (
    AssignmentStep,
    BoundArtifact,
    ExposureEvent,
    ExposureUnitKind,
    HeldOutTransferTask,
    SelectionDecision,
    SelectionRegime,
    SelectionTaskDomain,
    TaskSelectionUnit,
    audit_task_selection_exposure_design,
)


def artifact(name: str, content: str) -> BoundArtifact:
    return BoundArtifact(
        artifact_id=name,
        content_utf8=content,
        sha256_digest=hashlib.sha256(content.encode("utf-8")).hexdigest(),
    )


FAMILY = {
    domain: artifact(f"family:{domain.value}", f"family-definition:{domain.value}")
    for domain in SelectionTaskDomain
}

CONTROLS = {
    "exposure_unit_definition": artifact(
        "exposure-unit",
        "One exposure unit is one bounded synthetic task episode. Counts do not imply equal duration, difficulty, or semantic intensity.",
    ),
    "access_profile": artifact("access", "same-access-profile"),
    "model_configuration": artifact("model", "same-model-configuration"),
    "tool_access": artifact("tools", "same-tool-access"),
    "evaluator_payload": artifact("evaluator", "same-evaluator"),
    "prior_knowledge_control": artifact("prior", "same-prior-knowledge-control"),
    "time_budget_control": artifact("time", "same-time-budget"),
    "task_difficulty_control": artifact(
        "difficulty", "same-task-difficulty-control"
    ),
    "resource_cost_information": artifact(
        "cost", "same-resource-cost-information"
    ),
}

FREE_PROTOCOL = artifact(
    "protocol:free",
    "At each episode the synthetic free-selection unit selects one available task episode.",
)
YOKED_PROTOCOL = artifact(
    "protocol:yoked",
    "The yoked unit receives the exact episode sequence realized by its paired free-selection unit and makes no task-selection choice.",
)


def sequence(
    pair: str,
    domains: tuple[SelectionTaskDomain, ...],
) -> tuple[ExposureEvent, ...]:
    return tuple(
        ExposureEvent(
            event_index=index,
            task_domain=domain,
            task_family_artifact=FAMILY[domain],
            exposure_payload_artifact=artifact(
                f"payload:{pair}:{index}",
                f"payload:{pair}:{index}:{domain.value}",
            ),
        )
        for index, domain in enumerate(domains)
    )


def decisions(events: tuple[ExposureEvent, ...]) -> tuple[SelectionDecision, ...]:
    return tuple(
        SelectionDecision(
            event_index=event.event_index,
            task_domain=event.task_domain,
            task_family_sha256=event.task_family_artifact.sha256_digest,
            exposure_payload_sha256=event.exposure_payload_artifact.sha256_digest,
        )
        for event in events
    )


def schedule(events: tuple[ExposureEvent, ...]) -> tuple[AssignmentStep, ...]:
    return tuple(
        AssignmentStep(
            event_index=event.event_index,
            task_domain=event.task_domain,
            task_family_sha256=event.task_family_artifact.sha256_digest,
            exposure_payload_sha256=event.exposure_payload_artifact.sha256_digest,
        )
        for event in events
    )


def unit(
    pair: str,
    regime: SelectionRegime,
    events: tuple[ExposureEvent, ...],
) -> TaskSelectionUnit:
    return TaskSelectionUnit(
        unit_id=f"{pair}:{regime.value}",
        pair_id=pair,
        selection_regime=regime,
        selection_protocol=(
            FREE_PROTOCOL
            if regime is SelectionRegime.FREE_SELECTION
            else YOKED_PROTOCOL
        ),
        realized_choice_trace=(
            decisions(events) if regime is SelectionRegime.FREE_SELECTION else ()
        ),
        assignment_schedule=(
            schedule(events)
            if regime is SelectionRegime.YOKED_ASSIGNED_EXPOSURE
            else ()
        ),
        realized_exposure_trace=events,
        execution_record=artifact(
            f"execution:{pair}:{regime.value}",
            f"execution-record:{pair}:{regime.value}",
        ),
        exposure_unit_kind=ExposureUnitKind.TASK_EPISODE,
        **CONTROLS,
    )


def pair(
    pair_id: str,
    domains: tuple[SelectionTaskDomain, ...],
) -> tuple[TaskSelectionUnit, TaskSelectionUnit]:
    free_events = sequence(pair_id, domains)
    return (
        unit(pair_id, SelectionRegime.FREE_SELECTION, free_events),
        unit(pair_id, SelectionRegime.YOKED_ASSIGNED_EXPOSURE, free_events),
    )


def design(
    second_domains: tuple[SelectionTaskDomain, ...] = (
        SelectionTaskDomain.RESEARCH_PROVENANCE,
        SelectionTaskDomain.GIT_ENGINEERING,
        SelectionTaskDomain.GIT_ENGINEERING,
    ),
) -> tuple[TaskSelectionUnit, ...]:
    first = pair(
        "PAIR_A",
        (
            SelectionTaskDomain.IMAGE_VISUAL,
            SelectionTaskDomain.IMAGE_VISUAL,
            SelectionTaskDomain.RESEARCH_PROVENANCE,
        ),
    )
    second = pair("PAIR_B", second_domains)
    return first + second


def held_out_tasks() -> tuple[HeldOutTransferTask, ...]:
    return tuple(
        HeldOutTransferTask(
            task_domain=domain,
            task_family_artifact=FAMILY[domain],
            task_payload_artifact=artifact(
                f"heldout:{domain.value}",
                f"heldout-payload:{domain.value}",
            ),
            evaluator_payload=CONTROLS["evaluator_payload"],
        )
        for domain in SelectionTaskDomain
    )


def test_complete_design_uses_true_yoked_pairs_and_real_hash_bindings() -> None:
    result = audit_task_selection_exposure_design(design(), held_out_tasks())
    assert result.complete_design is True
    assert result.pair_count == 2
    assert result.true_yoked_pairing is True
    assert result.free_selection_null_permitted is True
    assert result.protocol_schedule_choice_exposure_separated is True
    assert result.zero_domain_exposure_permitted is True
    assert result.exposure_unit_definition_bound is True
    assert result.content_hash_verified is True
    assert result.separate_execution_records is True
    assert result.design_unit == "BETWEEN_UNIT_YOKED_PAIR"
    assert result.exposure_unit == "TASK_EPISODE_EVENT_COUNT"
    assert result.cross_domain_commensurability == "EVENT_COUNT_ONLY_NOT_INTENSITY"
    assert (
        result.temporal_provenance_status
        == "SPECIFICATION_BOUND_NOT_EMPIRICALLY_POPULATED"
    )
    assert result.free_selection_exposure_divergence_observed is True
    assert result.h_ts1_status == "NOT_ESTABLISHED"
    assert result.h_dl1_status == "NOT_ESTABLISHED"
    assert result.h_ra1_status == "NOT_TESTED_BY_THIS_HARNESS"
    assert result.human_learning == "NOT_ESTABLISHED"
    assert result.causal_effect == "NOT_ESTABLISHED"
    assert result.scientific_disposition.value == "HOLD"
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert result.consciousness_conclusion == "NOT_ESTABLISHED"
    assert result.phenomenal_experience_conclusion == "NOT_ESTABLISHED"


def test_free_selection_null_outcome_is_valid_not_rejected() -> None:
    same = (
        SelectionTaskDomain.IMAGE_VISUAL,
        SelectionTaskDomain.IMAGE_VISUAL,
        SelectionTaskDomain.RESEARCH_PROVENANCE,
    )
    result = audit_task_selection_exposure_design(
        design(second_domains=same), held_out_tasks()
    )
    assert result.complete_design is True
    assert result.free_selection_exposure_divergence_observed is False


def test_zero_domain_exposure_is_preserved_in_derived_counts() -> None:
    result = audit_task_selection_exposure_design(design(), held_out_tasks())
    assert (2, 0, 1, 0) in result.free_domain_exposure_counts
    assert (0, 0, 1, 2) in result.free_domain_exposure_counts


def test_yoked_pair_must_copy_free_realized_exposure_sequence() -> None:
    units = list(design())
    yoked_index = next(
        index
        for index, item in enumerate(units)
        if item.pair_id == "PAIR_A"
        and item.selection_regime is SelectionRegime.YOKED_ASSIGNED_EXPOSURE
    )
    original = units[yoked_index]
    changed_events = list(original.realized_exposure_trace)
    changed_events[0] = replace(
        changed_events[0],
        exposure_payload_artifact=artifact(
            "payload:mismatch", "mismatched-payload"
        ),
    )
    changed_events_tuple = tuple(changed_events)
    units[yoked_index] = replace(
        original,
        assignment_schedule=schedule(changed_events_tuple),
        realized_exposure_trace=changed_events_tuple,
    )
    with pytest.raises(StudyError, match="same realized exposure sequence"):
        audit_task_selection_exposure_design(tuple(units), held_out_tasks())


def test_assigned_schedule_binds_its_realized_exposure() -> None:
    item = design()[1]
    bad_schedule = list(item.assignment_schedule)
    bad_schedule[0] = replace(
        bad_schedule[0],
        exposure_payload_sha256=artifact(
            "different", "different-payload"
        ).sha256_digest,
    )
    with pytest.raises(StudyError, match="assigned schedule must bind"):
        replace(item, assignment_schedule=tuple(bad_schedule))


def test_free_choice_trace_binds_its_realized_exposure() -> None:
    item = design()[0]
    bad_trace = list(item.realized_choice_trace)
    bad_trace[0] = replace(
        bad_trace[0],
        task_domain=SelectionTaskDomain.CREATIVE_TEXT,
    )
    with pytest.raises(StudyError, match="realized choices must bind"):
        replace(item, realized_choice_trace=tuple(bad_trace))


def test_same_free_choice_trace_across_pairs_is_allowed() -> None:
    same = (
        SelectionTaskDomain.IMAGE_VISUAL,
        SelectionTaskDomain.IMAGE_VISUAL,
        SelectionTaskDomain.RESEARCH_PROVENANCE,
    )
    units = list(design(second_domains=same))
    free_a = next(
        item
        for item in units
        if item.pair_id == "PAIR_A"
        and item.selection_regime is SelectionRegime.FREE_SELECTION
    )
    free_b_index = next(
        index
        for index, item in enumerate(units)
        if item.pair_id == "PAIR_B"
        and item.selection_regime is SelectionRegime.FREE_SELECTION
    )
    free_b = units[free_b_index]
    pair_b_events = tuple(
        replace(
            event,
            task_family_artifact=free_a.realized_exposure_trace[
                index
            ].task_family_artifact,
            exposure_payload_artifact=free_a.realized_exposure_trace[
                index
            ].exposure_payload_artifact,
        )
        for index, event in enumerate(free_b.realized_exposure_trace)
    )
    units[free_b_index] = replace(
        free_b,
        realized_choice_trace=free_a.realized_choice_trace,
        realized_exposure_trace=pair_b_events,
    )
    yoked_b_index = next(
        index
        for index, item in enumerate(units)
        if item.pair_id == "PAIR_B"
        and item.selection_regime is SelectionRegime.YOKED_ASSIGNED_EXPOSURE
    )
    yoked_b = units[yoked_b_index]
    units[yoked_b_index] = replace(
        yoked_b,
        assignment_schedule=schedule(pair_b_events),
        realized_exposure_trace=pair_b_events,
    )
    result = audit_task_selection_exposure_design(tuple(units), held_out_tasks())
    assert result.free_selection_exposure_divergence_observed is False


def test_artifact_digest_must_match_real_content() -> None:
    with pytest.raises(StudyError, match="must match content_utf8"):
        BoundArtifact(
            artifact_id="bad",
            content_utf8="actual-content",
            sha256_digest="0" * 64,
        )


def test_design_requires_two_complete_yoked_pairs() -> None:
    with pytest.raises(StudyError, match="at least two"):
        audit_task_selection_exposure_design(
            pair("PAIR_A", (SelectionTaskDomain.IMAGE_VISUAL,)), held_out_tasks()
        )

    units = list(design())
    with pytest.raises(StudyError, match="exactly two"):
        audit_task_selection_exposure_design(tuple(units[:-1]), held_out_tasks())


def test_execution_records_are_per_unit_not_shared() -> None:
    units = list(design())
    units[-1] = replace(units[-1], execution_record=units[0].execution_record)
    with pytest.raises(StudyError, match="distinct execution record"):
        audit_task_selection_exposure_design(tuple(units), held_out_tasks())


def test_control_drift_fails_closed() -> None:
    units = list(design())
    units[-1] = replace(
        units[-1],
        resource_cost_information=artifact(
            "cost:drift", "different-cost-information"
        ),
    )
    with pytest.raises(StudyError, match="resource_cost_information drift"):
        audit_task_selection_exposure_design(tuple(units), held_out_tasks())


def test_protocol_drift_and_protocol_collapse_fail_closed() -> None:
    units = list(design())
    units[-2] = replace(
        units[-2],
        selection_protocol=artifact("free:drift", "different-free-protocol"),
    )
    with pytest.raises(StudyError, match="one exact protocol binding"):
        audit_task_selection_exposure_design(tuple(units), held_out_tasks())

    units = list(design())
    units = [
        replace(item, selection_protocol=FREE_PROTOCOL)
        if item.selection_regime is SelectionRegime.YOKED_ASSIGNED_EXPOSURE
        else item
        for item in units
    ]
    with pytest.raises(StudyError, match="content-distinct protocol"):
        audit_task_selection_exposure_design(tuple(units), held_out_tasks())


def test_held_out_family_and_payload_separation_fail_closed() -> None:
    tasks = list(held_out_tasks())
    tasks[0] = replace(
        tasks[0],
        task_family_artifact=artifact("wrong-family", "wrong-family"),
    )
    with pytest.raises(StudyError, match="task-family binding"):
        audit_task_selection_exposure_design(design(), tuple(tasks))

    tasks = list(held_out_tasks())
    reused = design()[0].realized_exposure_trace[0].exposure_payload_artifact
    tasks[0] = replace(tasks[0], task_payload_artifact=reused)
    with pytest.raises(StudyError, match="distinct from exposure payloads"):
        audit_task_selection_exposure_design(design(), tuple(tasks))


def test_privacy_empirical_and_raw_enum_boundaries_fail_closed() -> None:
    with pytest.raises(StudyError, match="structural QA only"):
        replace(design()[0], model_invoked=True)
    with pytest.raises(StudyError, match="private material"):
        replace(design()[0], contains_private_material=True)
    with pytest.raises(StudyError, match="human identity"):
        replace(held_out_tasks()[0], contains_human_identity=True)
    with pytest.raises(StudyError, match="exact SelectionRegime"):
        replace(design()[0], selection_regime="FREE_SELECTION")
    with pytest.raises(StudyError, match="exact SelectionTaskDomain"):
        replace(
            design()[0].realized_exposure_trace[0], task_domain="IMAGE_VISUAL"
        )
