from __future__ import annotations

from dataclasses import replace

import pytest

from aion_human_ai_longitudinal import StudyError
from aion_human_ai_longitudinal.task_selection_exposure import (
    DomainExposure,
    HeldOutTransferTask,
    SelectionRegime,
    SelectionTaskDomain,
    SyntheticTrack,
    TaskSelectionArm,
    audit_task_selection_exposure_design,
)


def digest(char: str) -> str:
    return char * 64


def patterned_digest(left: str, right: str) -> str:
    return (left + right) * 32


def exposure_vector(
    regime: SelectionRegime,
    track: SyntheticTrack,
) -> dict[SelectionTaskDomain, int]:
    if regime is SelectionRegime.MATCHED_ASSIGNED_EXPOSURE:
        return {
            SelectionTaskDomain.IMAGE_VISUAL: 2,
            SelectionTaskDomain.CREATIVE_TEXT: 3,
            SelectionTaskDomain.RESEARCH_PROVENANCE: 2,
            SelectionTaskDomain.GIT_ENGINEERING: 3,
        }
    if track is SyntheticTrack.TRACK_A:
        return {
            SelectionTaskDomain.IMAGE_VISUAL: 4,
            SelectionTaskDomain.CREATIVE_TEXT: 4,
            SelectionTaskDomain.RESEARCH_PROVENANCE: 1,
            SelectionTaskDomain.GIT_ENGINEERING: 1,
        }
    return {
        SelectionTaskDomain.IMAGE_VISUAL: 1,
        SelectionTaskDomain.CREATIVE_TEXT: 1,
        SelectionTaskDomain.RESEARCH_PROVENANCE: 4,
        SelectionTaskDomain.GIT_ENGINEERING: 4,
    }


def arm(regime: SelectionRegime, track: SyntheticTrack) -> TaskSelectionArm:
    family_chars = "0123"
    free_payload_chars = {
        (SyntheticTrack.TRACK_A, SelectionTaskDomain.IMAGE_VISUAL): "4",
        (SyntheticTrack.TRACK_A, SelectionTaskDomain.CREATIVE_TEXT): "5",
        (SyntheticTrack.TRACK_A, SelectionTaskDomain.RESEARCH_PROVENANCE): "6",
        (SyntheticTrack.TRACK_A, SelectionTaskDomain.GIT_ENGINEERING): "7",
        (SyntheticTrack.TRACK_B, SelectionTaskDomain.IMAGE_VISUAL): "8",
        (SyntheticTrack.TRACK_B, SelectionTaskDomain.CREATIVE_TEXT): "9",
        (SyntheticTrack.TRACK_B, SelectionTaskDomain.RESEARCH_PROVENANCE): "a",
        (SyntheticTrack.TRACK_B, SelectionTaskDomain.GIT_ENGINEERING): "b",
    }
    assigned_payload_chars = {
        SelectionTaskDomain.IMAGE_VISUAL: "c",
        SelectionTaskDomain.CREATIVE_TEXT: "d",
        SelectionTaskDomain.RESEARCH_PROVENANCE: "e",
        SelectionTaskDomain.GIT_ENGINEERING: "f",
    }
    units = exposure_vector(regime, track)
    exposures = []
    for index, domain in enumerate(SelectionTaskDomain):
        payload_char = (
            assigned_payload_chars[domain]
            if regime is SelectionRegime.MATCHED_ASSIGNED_EXPOSURE
            else free_payload_chars[(track, domain)]
        )
        exposures.append(
            DomainExposure(
                task_domain=domain,
                exposure_units=units[domain],
                task_family_sha256=digest(family_chars[index]),
                exposure_payload_sha256=digest(payload_char),
            )
        )
    return TaskSelectionArm(
        arm_id=f"{regime.value}:{track.value}",
        selection_regime=regime,
        synthetic_track=track,
        exposures=tuple(exposures),
        access_profile_sha256=digest("1"),
        model_configuration_sha256=digest("2"),
        tool_access_sha256=digest("3"),
        evaluator_payload_sha256=digest("4"),
        prior_knowledge_control_sha256=digest("5"),
        time_budget_sha256=digest("6"),
        task_difficulty_control_sha256=digest("7"),
        resource_cost_information_sha256=digest("8"),
    )


def arms() -> tuple[TaskSelectionArm, ...]:
    return tuple(
        arm(regime, track)
        for regime in SelectionRegime
        for track in SyntheticTrack
    )


def held_out_tasks() -> tuple[HeldOutTransferTask, ...]:
    family_chars = "0123"
    payload_pairs = (("0", "f"), ("1", "e"), ("2", "d"), ("3", "c"))
    return tuple(
        HeldOutTransferTask(
            task_domain=domain,
            task_family_sha256=digest(family_chars[index]),
            task_payload_sha256=patterned_digest(*payload_pairs[index]),
            evaluator_payload_sha256=digest("4"),
        )
        for index, domain in enumerate(SelectionTaskDomain)
    )


def replace_exposure(
    item: TaskSelectionArm,
    domain: SelectionTaskDomain,
    **changes: object,
) -> TaskSelectionArm:
    exposures = tuple(
        replace(exposure, **changes) if exposure.task_domain is domain else exposure
        for exposure in item.exposures
    )
    return replace(item, exposures=exposures)


def test_complete_design_is_structural_qa_only() -> None:
    result = audit_task_selection_exposure_design(arms(), held_out_tasks())
    assert result.complete_design is True
    assert result.same_access_controls is True
    assert result.matched_assigned_exposure is True
    assert result.free_selection_exposure_divergence is True
    assert result.matched_total_exposure is True
    assert result.task_family_controls is True
    assert result.held_out_payload_separation is True
    assert result.resource_cost_information_controlled is True
    assert result.mode == "DETERMINISTIC_SYNTHETIC_FIXTURE"
    assert result.model_invoked is False
    assert result.human_participant_observed is False
    assert result.empirical_data_collected is False
    assert result.evidence_admissibility == "STRUCTURAL_QA_ONLY"
    assert result.h_ts1_status == "NOT_ESTABLISHED"
    assert result.h_dl1_status == "NOT_ESTABLISHED"
    assert result.h_ra1_status == "NOT_TESTED_BY_THIS_HARNESS"
    assert result.human_learning == "NOT_ESTABLISHED"
    assert result.causal_effect == "NOT_ESTABLISHED"
    assert result.scientific_disposition.value == "HOLD"
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert result.consciousness_conclusion == "NOT_ESTABLISHED"
    assert result.phenomenal_experience_conclusion == "NOT_ESTABLISHED"


def test_missing_or_duplicate_arm_fails_closed() -> None:
    with pytest.raises(StudyError, match="exactly one arm"):
        audit_task_selection_exposure_design(arms()[:-1], held_out_tasks())
    with pytest.raises(StudyError, match="unique|exactly one arm"):
        audit_task_selection_exposure_design(arms() + (arms()[0],), held_out_tasks())


def test_access_and_resource_cost_control_drift_fail_closed() -> None:
    items = list(arms())
    items[-1] = replace(items[-1], access_profile_sha256=digest("9"))
    with pytest.raises(StudyError, match="access_profile_sha256 drift"):
        audit_task_selection_exposure_design(tuple(items), held_out_tasks())

    items = list(arms())
    items[-1] = replace(items[-1], resource_cost_information_sha256=digest("9"))
    with pytest.raises(StudyError, match="resource_cost_information_sha256 drift"):
        audit_task_selection_exposure_design(tuple(items), held_out_tasks())


def test_task_family_drift_fails_closed() -> None:
    items = list(arms())
    items[-1] = replace_exposure(
        items[-1],
        SelectionTaskDomain.GIT_ENGINEERING,
        task_family_sha256=digest("9"),
    )
    with pytest.raises(StudyError, match="task-family binding drift"):
        audit_task_selection_exposure_design(tuple(items), held_out_tasks())


def test_total_exposure_must_be_matched() -> None:
    items = list(arms())
    items[-1] = replace_exposure(
        items[-1],
        SelectionTaskDomain.GIT_ENGINEERING,
        exposure_units=5,
    )
    with pytest.raises(StudyError, match="total exposure must be matched"):
        audit_task_selection_exposure_design(tuple(items), held_out_tasks())


def test_matched_assigned_exposure_requires_same_distribution_and_payloads() -> None:
    items = list(arms())
    index = next(
        i
        for i, item in enumerate(items)
        if item.selection_regime is SelectionRegime.MATCHED_ASSIGNED_EXPOSURE
        and item.synthetic_track is SyntheticTrack.TRACK_B
    )
    item = replace_exposure(
        items[index],
        SelectionTaskDomain.IMAGE_VISUAL,
        exposure_units=3,
    )
    item = replace_exposure(
        item,
        SelectionTaskDomain.CREATIVE_TEXT,
        exposure_units=2,
    )
    items[index] = item
    with pytest.raises(StudyError, match="identical exposure distributions"):
        audit_task_selection_exposure_design(tuple(items), held_out_tasks())

    items = list(arms())
    items[index] = replace_exposure(
        items[index],
        SelectionTaskDomain.IMAGE_VISUAL,
        exposure_payload_sha256=digest("9"),
    )
    with pytest.raises(StudyError, match="identical exposure payloads"):
        audit_task_selection_exposure_design(tuple(items), held_out_tasks())


def test_free_selection_tracks_must_encode_different_effective_exposure() -> None:
    items = list(arms())
    track_a = next(
        item
        for item in items
        if item.selection_regime is SelectionRegime.FREE_SELECTION
        and item.synthetic_track is SyntheticTrack.TRACK_A
    )
    track_b_index = next(
        i
        for i, item in enumerate(items)
        if item.selection_regime is SelectionRegime.FREE_SELECTION
        and item.synthetic_track is SyntheticTrack.TRACK_B
    )
    replacement_units = {
        exposure.task_domain: exposure.exposure_units for exposure in track_a.exposures
    }
    track_b = items[track_b_index]
    track_b = replace(
        track_b,
        exposures=tuple(
            replace(exposure, exposure_units=replacement_units[exposure.task_domain])
            for exposure in track_b.exposures
        ),
    )
    items[track_b_index] = track_b
    with pytest.raises(StudyError, match="different effective exposure distributions"):
        audit_task_selection_exposure_design(tuple(items), held_out_tasks())


def test_held_out_tasks_require_family_match_and_payload_separation() -> None:
    tasks = list(held_out_tasks())
    tasks[-1] = replace(tasks[-1], task_family_sha256=digest("9"))
    with pytest.raises(StudyError, match="task-family binding"):
        audit_task_selection_exposure_design(arms(), tuple(tasks))

    tasks = list(held_out_tasks())
    reused_payload = arms()[0].exposures[0].exposure_payload_sha256
    tasks[0] = replace(tasks[0], task_payload_sha256=reused_payload)
    with pytest.raises(StudyError, match="distinct from exposure payloads"):
        audit_task_selection_exposure_design(arms(), tuple(tasks))


def test_privacy_empirical_and_digest_boundaries_fail_closed() -> None:
    with pytest.raises(StudyError, match="structural QA only"):
        replace(arms()[0], model_invoked=True)
    with pytest.raises(StudyError, match="structural QA only"):
        replace(held_out_tasks()[0], human_participant_observed=True)
    with pytest.raises(StudyError, match="private material"):
        replace(arms()[0], contains_private_material=True)
    with pytest.raises(StudyError, match="human identity"):
        replace(held_out_tasks()[0], contains_human_identity=True)
    with pytest.raises(StudyError, match="SHA-256"):
        replace(arms()[0], access_profile_sha256="not-a-digest")


def test_raw_enums_and_duplicate_domains_are_rejected() -> None:
    with pytest.raises(StudyError, match="exact SelectionRegime"):
        replace(arms()[0], selection_regime="FREE_SELECTION")
    with pytest.raises(StudyError, match="exact SelectionTaskDomain"):
        replace(arms()[0].exposures[0], task_domain="IMAGE_VISUAL")

    duplicate = replace(
        arms()[0],
        exposures=arms()[0].exposures[:-1] + (arms()[0].exposures[0],),
    )
    items = list(arms())
    items[0] = duplicate
    with pytest.raises(StudyError, match="exactly one exposure record per task domain"):
        audit_task_selection_exposure_design(tuple(items), held_out_tasks())
