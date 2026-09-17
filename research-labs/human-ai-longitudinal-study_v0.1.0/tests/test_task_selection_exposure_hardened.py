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
)
from aion_human_ai_longitudinal.task_selection_exposure_hardened import (
    ChoiceAlternative,
    ChoiceOpportunity,
    ExecutionIdentityBinding,
    FreeChoiceOpportunityTrace,
    audit_task_selection_exposure_design_hardened,
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
    "task_difficulty_control": artifact("difficulty", "same-task-difficulty-control"),
    "resource_cost_information": artifact("cost", "same-resource-cost-information"),
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
    pair_id: str,
    domains: tuple[SelectionTaskDomain, ...],
) -> tuple[ExposureEvent, ...]:
    return tuple(
        ExposureEvent(
            event_index=index,
            task_domain=domain,
            task_family_artifact=FAMILY[domain],
            exposure_payload_artifact=artifact(
                f"payload:{pair_id}:{index}",
                f"payload:{pair_id}:{index}:{domain.value}",
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
    pair_id: str,
    regime: SelectionRegime,
    events: tuple[ExposureEvent, ...],
) -> TaskSelectionUnit:
    return TaskSelectionUnit(
        unit_id=f"{pair_id}:{regime.value}",
        pair_id=pair_id,
        selection_regime=regime,
        selection_protocol=(FREE_PROTOCOL if regime is SelectionRegime.FREE_SELECTION else YOKED_PROTOCOL),
        realized_choice_trace=(decisions(events) if regime is SelectionRegime.FREE_SELECTION else ()),
        assignment_schedule=(schedule(events) if regime is SelectionRegime.YOKED_ASSIGNED_EXPOSURE else ()),
        realized_exposure_trace=events,
        execution_record=artifact(
            f"execution-record:{pair_id}:{regime.value}",
            f"execution-record-content:{pair_id}:{regime.value}",
        ),
        exposure_unit_kind=ExposureUnitKind.TASK_EPISODE,
        **CONTROLS,
    )


def pair(
    pair_id: str,
    domains: tuple[SelectionTaskDomain, ...],
) -> tuple[TaskSelectionUnit, TaskSelectionUnit]:
    events = sequence(pair_id, domains)
    return (
        unit(pair_id, SelectionRegime.FREE_SELECTION, events),
        unit(pair_id, SelectionRegime.YOKED_ASSIGNED_EXPOSURE, events),
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
    return first + pair("PAIR_B", second_domains)


def alternative_for(
    unit_id: str,
    event_index: int,
    selected_domain: SelectionTaskDomain,
) -> ChoiceAlternative:
    domains = tuple(SelectionTaskDomain)
    selected_index = domains.index(selected_domain)
    domain = domains[(selected_index + 1) % len(domains)]
    return ChoiceAlternative(
        task_domain=domain,
        task_family_artifact=artifact(
            f"opportunity-family:{unit_id}:{event_index}:{domain.value}",
            f"opportunity-family-content:{unit_id}:{event_index}:{domain.value}",
        ),
        exposure_payload_artifact=artifact(
            f"opportunity-payload:{unit_id}:{event_index}:{domain.value}",
            f"opportunity-payload-content:{unit_id}:{event_index}:{domain.value}",
        ),
    )


def choice_traces(units: tuple[TaskSelectionUnit, ...]) -> tuple[FreeChoiceOpportunityTrace, ...]:
    traces: list[FreeChoiceOpportunityTrace] = []
    for item in units:
        if item.selection_regime is not SelectionRegime.FREE_SELECTION:
            continue
        opportunities: list[ChoiceOpportunity] = []
        for event in item.realized_exposure_trace:
            selected = ChoiceAlternative(
                task_domain=event.task_domain,
                task_family_artifact=event.task_family_artifact,
                exposure_payload_artifact=event.exposure_payload_artifact,
            )
            opportunities.append(
                ChoiceOpportunity(
                    event_index=event.event_index,
                    options=(
                        selected,
                        alternative_for(item.unit_id, event.event_index, event.task_domain),
                    ),
                    opportunity_record=artifact(
                        f"opportunity-record:{item.unit_id}:{event.event_index}",
                        f"opportunity-record-content:{item.unit_id}:{event.event_index}",
                    ),
                )
            )
        traces.append(
            FreeChoiceOpportunityTrace(
                unit_id=item.unit_id,
                opportunities=tuple(opportunities),
            )
        )
    return tuple(traces)


def execution_identities(
    units: tuple[TaskSelectionUnit, ...],
) -> tuple[ExecutionIdentityBinding, ...]:
    return tuple(
        ExecutionIdentityBinding(
            unit_id=item.unit_id,
            execution_id=f"execution:{item.unit_id}",
            execution_record_artifact_id=item.execution_record.artifact_id,
        )
        for item in units
    )


def within_family_tasks() -> tuple[HeldOutTransferTask, ...]:
    return tuple(
        HeldOutTransferTask(
            task_domain=domain,
            task_family_artifact=FAMILY[domain],
            task_payload_artifact=artifact(
                f"within-payload:{domain.value}",
                f"within-payload-content:{domain.value}",
            ),
            evaluator_payload=CONTROLS["evaluator_payload"],
        )
        for domain in SelectionTaskDomain
    )


def cross_family_tasks() -> tuple[HeldOutTransferTask, ...]:
    return tuple(
        HeldOutTransferTask(
            task_domain=domain,
            task_family_artifact=artifact(
                f"cross-family:{domain.value}",
                f"cross-family-content:{domain.value}",
            ),
            task_payload_artifact=artifact(
                f"cross-payload:{domain.value}",
                f"cross-payload-content:{domain.value}",
            ),
            evaluator_payload=CONTROLS["evaluator_payload"],
        )
        for domain in SelectionTaskDomain
    )


def audit(units: tuple[TaskSelectionUnit, ...] | None = None):
    actual_units = design() if units is None else units
    return audit_task_selection_exposure_design_hardened(
        actual_units,
        choice_traces(actual_units),
        execution_identities(actual_units),
        within_family_tasks(),
        cross_family_tasks(),
    )


def test_hardened_design_binds_choice_sets_execution_identity_and_two_holdout_levels() -> None:
    result = audit()
    assert result.complete_design is True
    assert result.pair_count == 2
    assert result.choice_opportunity_sets_bound is True
    assert result.chosen_option_membership_verified is True
    assert result.execution_identity_separated_from_content is True
    assert result.same_content_execution_records_permitted is True
    assert result.within_family_payload_holdout_bound is True
    assert result.cross_family_domain_generalization_bound is True
    assert result.choice_set_temporal_provenance_established is False
    assert result.family_level_human_transfer_established is False
    assert result.human_learning == "NOT_ESTABLISHED"
    assert result.causal_effect == "NOT_ESTABLISHED"
    assert result.scientific_disposition.value == "HOLD"
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"


def test_choice_opportunity_trace_is_required_for_every_free_unit() -> None:
    units = design()
    traces = choice_traces(units)
    with pytest.raises(StudyError, match="exactly the FREE_SELECTION units"):
        audit_task_selection_exposure_design_hardened(
            units,
            traces[:-1],
            execution_identities(units),
            within_family_tasks(),
            cross_family_tasks(),
        )


def test_free_choice_requires_at_least_two_distinct_available_alternatives() -> None:
    event = design()[0].realized_exposure_trace[0]
    selected = ChoiceAlternative(
        task_domain=event.task_domain,
        task_family_artifact=event.task_family_artifact,
        exposure_payload_artifact=event.exposure_payload_artifact,
    )
    with pytest.raises(StudyError, match="at least two"):
        ChoiceOpportunity(
            event_index=0,
            options=(selected,),
            opportunity_record=artifact("record", "record"),
        )
    with pytest.raises(StudyError, match="content-distinct"):
        ChoiceOpportunity(
            event_index=0,
            options=(selected, selected),
            opportunity_record=artifact("record2", "record2"),
        )


def test_realized_choice_must_belong_to_bound_opportunity_set() -> None:
    units = design()
    traces = list(choice_traces(units))
    trace = traces[0]
    original = trace.opportunities[0]
    first = alternative_for(trace.unit_id, 0, SelectionTaskDomain.IMAGE_VISUAL)
    second = alternative_for(trace.unit_id, 1, SelectionTaskDomain.IMAGE_VISUAL)
    changed = replace(original, options=(first, second))
    traces[0] = replace(trace, opportunities=(changed,) + trace.opportunities[1:])
    with pytest.raises(StudyError, match="member of the bound opportunity set"):
        audit_task_selection_exposure_design_hardened(
            units,
            tuple(traces),
            execution_identities(units),
            within_family_tasks(),
            cross_family_tasks(),
        )


def test_execution_identity_is_separate_from_record_content_digest() -> None:
    units = tuple(
        replace(
            item,
            execution_record=artifact(
                f"execution-record:{item.unit_id}",
                "identical-record-content-is-allowed",
            ),
        )
        for item in design()
    )
    result = audit_task_selection_exposure_design_hardened(
        units,
        choice_traces(units),
        execution_identities(units),
        within_family_tasks(),
        cross_family_tasks(),
    )
    assert result.execution_identity_separated_from_content is True


def test_duplicate_execution_identity_fails_closed() -> None:
    units = design()
    identities = list(execution_identities(units))
    identities[-1] = replace(identities[-1], execution_id=identities[0].execution_id)
    with pytest.raises(StudyError, match="execution_id values must be unique"):
        audit_task_selection_exposure_design_hardened(
            units,
            choice_traces(units),
            tuple(identities),
            within_family_tasks(),
            cross_family_tasks(),
        )


def test_within_family_holdout_must_match_exposed_family_when_domain_was_exposed() -> None:
    tasks = list(within_family_tasks())
    tasks[0] = replace(
        tasks[0],
        task_family_artifact=artifact("wrong-within-family", "wrong-within-family"),
    )
    units = design()
    with pytest.raises(StudyError, match="within-family held-out task"):
        audit_task_selection_exposure_design_hardened(
            units,
            choice_traces(units),
            execution_identities(units),
            tuple(tasks),
            cross_family_tasks(),
        )


def test_cross_family_holdout_must_use_family_absent_from_exposure() -> None:
    tasks = list(cross_family_tasks())
    tasks[0] = replace(tasks[0], task_family_artifact=FAMILY[SelectionTaskDomain.IMAGE_VISUAL])
    units = design()
    with pytest.raises(StudyError, match="family not seen in exposure"):
        audit_task_selection_exposure_design_hardened(
            units,
            choice_traces(units),
            execution_identities(units),
            within_family_tasks(),
            tuple(tasks),
        )


def test_zero_exposure_domain_still_requires_two_distinct_held_out_families() -> None:
    tasks = list(cross_family_tasks())
    creative_index = tuple(SelectionTaskDomain).index(SelectionTaskDomain.CREATIVE_TEXT)
    within = within_family_tasks()[creative_index]
    tasks[creative_index] = replace(
        tasks[creative_index],
        task_family_artifact=within.task_family_artifact,
    )
    units = design()
    with pytest.raises(StudyError, match="two distinct held-out families"):
        audit_task_selection_exposure_design_hardened(
            units,
            choice_traces(units),
            execution_identities(units),
            within_family_tasks(),
            tuple(tasks),
        )


def test_all_held_out_payloads_must_be_distinct_from_exposure_and_each_other() -> None:
    units = design()
    tasks = list(cross_family_tasks())
    tasks[0] = replace(
        tasks[0],
        task_payload_artifact=units[0].realized_exposure_trace[0].exposure_payload_artifact,
    )
    with pytest.raises(StudyError, match="distinct from exposure payloads"):
        audit_task_selection_exposure_design_hardened(
            units,
            choice_traces(units),
            execution_identities(units),
            within_family_tasks(),
            tuple(tasks),
        )


def test_free_selection_null_result_remains_valid_under_hardening() -> None:
    same = (
        SelectionTaskDomain.IMAGE_VISUAL,
        SelectionTaskDomain.IMAGE_VISUAL,
        SelectionTaskDomain.RESEARCH_PROVENANCE,
    )
    units = design(second_domains=same)
    result = audit_task_selection_exposure_design_hardened(
        units,
        choice_traces(units),
        execution_identities(units),
        within_family_tasks(),
        cross_family_tasks(),
    )
    assert result.free_selection_exposure_divergence_observed is False


def test_true_yoked_sequence_regression_still_fails_closed() -> None:
    units = list(design())
    yoked = units[1]
    events = list(yoked.realized_exposure_trace)
    events[0] = replace(
        events[0],
        exposure_payload_artifact=artifact("mismatch", "mismatch"),
    )
    changed_events = tuple(events)
    units[1] = replace(
        yoked,
        assignment_schedule=schedule(changed_events),
        realized_exposure_trace=changed_events,
    )
    changed_units = tuple(units)
    with pytest.raises(StudyError, match="same realized exposure sequence"):
        audit_task_selection_exposure_design_hardened(
            changed_units,
            choice_traces(changed_units),
            execution_identities(changed_units),
            within_family_tasks(),
            cross_family_tasks(),
        )
