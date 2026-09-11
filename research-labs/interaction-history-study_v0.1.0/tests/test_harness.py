from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path

import pytest

from aion_interaction_history import (
    ArtifactAction,
    ArtifactEvent,
    CollaborationChannel,
    ConditionProfile,
    ContrastSpec,
    InteractionHistoryStudyHarness,
    MetricName,
    MetricObservation,
    Presence,
    RunBinding,
    SafetyEnvelope,
    ScientificDisposition,
    StudyError,
    TaskRegime,
    TrialRecord,
)


CONTENT_HASH = "a" * 64


def binding(run_id: str, participant_id: str) -> RunBinding:
    return RunBinding(
        run_id=run_id,
        study_id="history-study-001",
        participant_id=participant_id,
        provider_id="provider-under-study",
        model_id="model-under-study",
        model_version="version-pinned",
        runtime_ref="runtime:container-image@sha256",
        environment_ref="environment:synthetic-sandbox-v1",
        task_id="matched-task-001",
        task_version="v1",
        tool_manifest_ref="tools:manifest-v1",
        action_budget_ref="budget:100-steps",
        sampling_ref="sampling:seed-set-001",
        scorer_ref="scorer:v1",
        preregistration_ref="preregistration:history-001",
        repository_commit="b" * 40,
        source_refs=("source:synthetic-fixture",),
    )


def safety() -> SafetyEnvelope:
    return SafetyEnvelope(
        sandbox_ref="sandbox:isolated-001",
        allowed_target_refs=("target:synthetic-only",),
        egress_policy_ref="egress:deny-external",
        rate_limit_ref="rate-limit:fixed",
        human_review_ref="review:required",
    )


def event(event_id: str, participant: str, action: ArtifactAction, index: int) -> ArtifactEvent:
    return ArtifactEvent(
        event_id=event_id,
        artifact_id="artifact-001",
        participant_id=participant,
        action=action,
        sequence_index=index,
        content_sha256=CONTENT_HASH,
        provenance_ref=f"event-log:{event_id}",
    )


def metric(value: float) -> MetricObservation:
    return MetricObservation(
        MetricName.BRANCH_CHANGE_RATE,
        value,
        "ratio",
        (f"score:{value}",),
        held_out=True,
    )


def condition(*, artifacts: Presence, peer: Presence) -> ConditionProfile:
    return ConditionProfile(
        persistent_artifacts=artifacts,
        peer_artifacts=peer,
        collaboration_channel=CollaborationChannel.NONE,
        task_regime=TaskRegime.REPEATED_FAILURE,
        interaction_history=Presence.ABSENT,
        full_provenance=Presence.PRESENT,
    )


def trial(run_id: str, *, artifacts: Presence, peer: Presence, value: float) -> TrialRecord:
    events = ()
    if artifacts is Presence.PRESENT:
        events = (
            event("write", "peer-a", ArtifactAction.WRITE, 1),
            event("read", "participant-b", ArtifactAction.READ, 2),
        )
    return TrialRecord(
        binding=binding(run_id, "participant-b"),
        condition=condition(artifacts=artifacts, peer=peer),
        safety=safety(),
        trajectory_ref=f"trajectory:{run_id}",
        artifact_events=events,
        metrics=(metric(value),),
        evaluator_id="independent-scorer",
        evaluator_source_ref="evaluator:receipt",
    )


def contrast() -> ContrastSpec:
    return ContrastSpec(
        contrast_id="artifact-contrast",
        hypothesis_id="H3",
        baseline_run_id="absent",
        intervention_run_id="present",
        manipulated_fields=("persistent_artifacts", "peer_artifacts"),
        required_metrics=(MetricName.BRANCH_CHANGE_RATE,),
        falsifier="persistent peer artifacts do not change later branch selection",
        alternative_explanations=("immediate context", "independent rediscovery"),
    )


def test_artifact_contrast_is_structural_and_stays_on_hold() -> None:
    harness = InteractionHistoryStudyHarness()
    harness.add_trial(trial("absent", artifacts=Presence.ABSENT, peer=Presence.ABSENT, value=0.1))
    harness.add_trial(trial("present", artifacts=Presence.PRESENT, peer=Presence.PRESENT, value=0.4))

    audit = harness.audit_contrast(contrast())

    assert audit.structurally_admissible is True
    assert audit.observed_deltas[0][0] == "BRANCH_CHANGE_RATE"
    assert audit.observed_deltas[0][1] == pytest.approx(0.3)
    assert audit.scientific_disposition is ScientificDisposition.HOLD
    assert audit.canonical_effect == "NONE"
    assert audit.deployment is False
    assert "OBSERVED_DIFFERENCE_IS_NOT_CAUSAL_IDENTIFICATION" in audit.reasons


def test_cross_participant_artifact_reuse_requires_ordered_matching_hash() -> None:
    events = (
        event("write", "peer-a", ArtifactAction.WRITE, 1),
        event("read", "participant-b", ArtifactAction.READ, 2),
    )
    audit = InteractionHistoryStudyHarness.audit_artifact_trajectory(events)

    assert audit.cross_participant_reuse_observed is True
    assert audit.matched_artifact_ids == ("artifact-001",)
    assert "ARTIFACT_READ_DOES_NOT_ESTABLISH_INTERNAL_REPRESENTATION" in audit.reasons


def test_read_before_write_and_same_participant_do_not_establish_reuse() -> None:
    read_first = (
        event("read", "participant-b", ArtifactAction.READ, 1),
        event("write", "peer-a", ArtifactAction.WRITE, 2),
    )
    same_participant = (
        event("write", "participant-b", ArtifactAction.WRITE, 1),
        event("read", "participant-b", ArtifactAction.READ, 2),
    )

    assert InteractionHistoryStudyHarness.audit_artifact_trajectory(read_first).cross_participant_reuse_observed is False
    assert InteractionHistoryStudyHarness.audit_artifact_trajectory(same_participant).cross_participant_reuse_observed is False


def test_peer_artifact_condition_without_read_log_fails_closed() -> None:
    with pytest.raises(StudyError, match="cross-participant"):
        TrialRecord(
            binding=binding("missing-read", "participant-b"),
            condition=condition(artifacts=Presence.PRESENT, peer=Presence.PRESENT),
            safety=safety(),
            trajectory_ref="trajectory:missing-read",
            artifact_events=(event("write", "peer-a", ArtifactAction.WRITE, 1),),
            metrics=(metric(0.2),),
            evaluator_id="scorer",
            evaluator_source_ref="scorer:receipt",
        )

    with pytest.raises(StudyError, match="peer artifacts require persistent artifacts"):
        TrialRecord(
            binding=binding("incoherent-condition", "participant-b"),
            condition=condition(artifacts=Presence.ABSENT, peer=Presence.PRESENT),
            safety=safety(),
            trajectory_ref="trajectory:incoherent-condition",
            artifact_events=(event("read", "participant-b", ArtifactAction.READ, 1),),
            metrics=(metric(0.2),),
            evaluator_id="scorer",
            evaluator_source_ref="scorer:receipt",
        )


def test_safety_or_runtime_drift_fails_closed() -> None:
    harness = InteractionHistoryStudyHarness()
    harness.add_trial(trial("absent", artifacts=Presence.ABSENT, peer=Presence.ABSENT, value=0.1))
    changed = trial("present", artifacts=Presence.PRESENT, peer=Presence.PRESENT, value=0.4)
    changed = replace(changed, binding=replace(changed.binding, runtime_ref="runtime:different"))
    harness.add_trial(changed)
    with pytest.raises(StudyError, match="runtime_ref"):
        harness.audit_contrast(contrast())

    participant_harness = InteractionHistoryStudyHarness()
    participant_harness.add_trial(trial("absent", artifacts=Presence.ABSENT, peer=Presence.ABSENT, value=0.1))
    participant_changed = trial("present", artifacts=Presence.PRESENT, peer=Presence.PRESENT, value=0.4)
    participant_changed = replace(
        participant_changed,
        binding=replace(participant_changed.binding, participant_id="different-participant"),
        artifact_events=(
            participant_changed.artifact_events[0],
            replace(
                participant_changed.artifact_events[1],
                participant_id="different-participant",
            ),
        ),
    )
    participant_harness.add_trial(participant_changed)
    with pytest.raises(StudyError, match="participant_id"):
        participant_harness.audit_contrast(contrast())


def test_undeclared_condition_change_fails_closed() -> None:
    harness = InteractionHistoryStudyHarness()
    harness.add_trial(trial("absent", artifacts=Presence.ABSENT, peer=Presence.ABSENT, value=0.1))
    changed = trial("present", artifacts=Presence.PRESENT, peer=Presence.PRESENT, value=0.4)
    changed = replace(changed, condition=replace(changed.condition, interaction_history=Presence.PRESENT))
    harness.add_trial(changed)
    with pytest.raises(StudyError, match="condition change mismatch"):
        harness.audit_contrast(contrast())


def test_synthetic_fixture_has_no_live_target_or_identity() -> None:
    fixture_path = Path(__file__).parents[1] / "fixtures" / "minimal_artifact_contrast.json"
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))

    assert fixture["live_external_execution"] is False
    assert fixture["contains_real_identity"] is False
    assert fixture["scientific_disposition"] == "HOLD"
    assert fixture["canonical_effect"] == "NONE"


@pytest.mark.parametrize(
    ("field_name", "raw_value"),
    (
        ("persistent_artifacts", "PRESENT"),
        ("peer_artifacts", "ABSENT"),
        ("collaboration_channel", "NONE"),
        ("task_regime", "REPEATED_FAILURE"),
        ("interaction_history", "ABSENT"),
        ("full_provenance", "PRESENT"),
        ("persistent_artifacts", "INVALID"),
    ),
)
def test_condition_profile_rejects_raw_or_invalid_enum_values(
    field_name: str,
    raw_value: str,
) -> None:
    values = {
        "persistent_artifacts": Presence.ABSENT,
        "peer_artifacts": Presence.ABSENT,
        "collaboration_channel": CollaborationChannel.NONE,
        "task_regime": TaskRegime.REPEATED_FAILURE,
        "interaction_history": Presence.ABSENT,
        "full_provenance": Presence.PRESENT,
    }
    values[field_name] = raw_value

    with pytest.raises(StudyError, match=field_name):
        ConditionProfile(**values)


def test_artifact_action_rejects_raw_string() -> None:
    with pytest.raises(StudyError, match="action"):
        event("raw-action", "peer-a", "WRITE", 1)


@pytest.mark.parametrize(
    "events",
    (
        (event("read-only", "participant-b", ArtifactAction.READ, 2),),
        (
            event("write", "peer-a", ArtifactAction.WRITE, 1),
            replace(event("read", "participant-b", ArtifactAction.READ, 2), content_sha256="b" * 64),
        ),
        (
            event("write", "participant-b", ArtifactAction.WRITE, 1),
            event("read", "participant-b", ArtifactAction.READ, 2),
        ),
        (
            event("read", "participant-b", ArtifactAction.READ, 1),
            event("write", "peer-a", ArtifactAction.WRITE, 2),
        ),
    ),
)
def test_peer_artifact_label_without_linked_peer_write_read_fails_closed(
    events: tuple[ArtifactEvent, ...],
) -> None:
    harness = InteractionHistoryStudyHarness()
    harness.add_trial(trial("absent", artifacts=Presence.ABSENT, peer=Presence.ABSENT, value=0.1))

    with pytest.raises(StudyError, match="cross-participant"):
        invalid = TrialRecord(
            binding=binding("present", "participant-b"),
            condition=condition(artifacts=Presence.PRESENT, peer=Presence.PRESENT),
            safety=safety(),
            trajectory_ref="trajectory:invalid-peer-label",
            artifact_events=events,
            metrics=(metric(0.4),),
            evaluator_id="independent-scorer",
            evaluator_source_ref="evaluator:receipt",
        )
        harness.add_trial(invalid)
        harness.audit_contrast(contrast())


def test_tied_or_non_monotonic_sequence_indexes_fail_closed() -> None:
    tied = (
        event("write", "peer-a", ArtifactAction.WRITE, 1),
        event("read", "participant-b", ArtifactAction.READ, 1),
    )
    reversed_order = (
        event("read", "participant-b", ArtifactAction.READ, 2),
        event("write", "peer-a", ArtifactAction.WRITE, 1),
    )

    with pytest.raises(StudyError, match="strictly increasing"):
        InteractionHistoryStudyHarness.audit_artifact_trajectory(tied)
    with pytest.raises(StudyError, match="strictly increasing"):
        InteractionHistoryStudyHarness.audit_artifact_trajectory(reversed_order)


@pytest.mark.parametrize("changed_field", ("evaluator_id", "evaluator_source_ref"))
def test_evaluator_drift_fails_closed(changed_field: str) -> None:
    harness = InteractionHistoryStudyHarness()
    harness.add_trial(trial("absent", artifacts=Presence.ABSENT, peer=Presence.ABSENT, value=0.1))
    changed = trial("present", artifacts=Presence.PRESENT, peer=Presence.PRESENT, value=0.4)
    changed = replace(changed, **{changed_field: "different-evaluator"})
    harness.add_trial(changed)

    with pytest.raises(StudyError, match=changed_field):
        harness.audit_contrast(contrast())


def test_channel_ref_drift_unrelated_to_channel_manipulation_fails_closed() -> None:
    harness = InteractionHistoryStudyHarness()
    baseline = trial("absent", artifacts=Presence.ABSENT, peer=Presence.ABSENT, value=0.1)
    intervention = trial("present", artifacts=Presence.PRESENT, peer=Presence.PRESENT, value=0.4)
    baseline = replace(
        baseline,
        condition=replace(baseline.condition, collaboration_channel=CollaborationChannel.AUTHORIZED),
        channel_ref="channel:baseline",
    )
    intervention = replace(
        intervention,
        condition=replace(intervention.condition, collaboration_channel=CollaborationChannel.AUTHORIZED),
        channel_ref="channel:intervention",
    )
    harness.add_trial(baseline)
    harness.add_trial(intervention)

    with pytest.raises(StudyError, match="channel_ref"):
        harness.audit_contrast(contrast())


def test_full_provenance_cannot_be_declaratively_manipulated() -> None:
    with pytest.raises(StudyError, match="unsupported manipulated_fields"):
        replace(contrast(), manipulated_fields=("full_provenance",))


def test_peer_artifacts_absent_rejects_observed_cross_participant_reuse() -> None:
    with pytest.raises(StudyError, match="peer_artifacts=ABSENT"):
        TrialRecord(
            binding=binding("peer-absence-conflict", "participant-b"),
            condition=condition(artifacts=Presence.PRESENT, peer=Presence.ABSENT),
            safety=safety(),
            trajectory_ref="trajectory:peer-absence-conflict",
            artifact_events=(
                event("write", "peer-a", ArtifactAction.WRITE, 1),
                event("read", "participant-b", ArtifactAction.READ, 2),
            ),
            metrics=(metric(0.2),),
            evaluator_id="scorer",
            evaluator_source_ref="scorer:receipt",
        )


@pytest.mark.parametrize(
    "events",
    (
        (event("unexpected-write", "participant-b", ArtifactAction.WRITE, 1),),
        (event("unexpected-read", "participant-b", ArtifactAction.READ, 1),),
    ),
)
def test_persistent_artifacts_absent_rejects_artifact_evidence(
    events: tuple[ArtifactEvent, ...],
) -> None:
    with pytest.raises(StudyError, match="persistent_artifacts=ABSENT"):
        TrialRecord(
            binding=binding("artifact-absence-conflict", "participant-b"),
            condition=condition(artifacts=Presence.ABSENT, peer=Presence.ABSENT),
            safety=safety(),
            trajectory_ref="trajectory:artifact-absence-conflict",
            artifact_events=events,
            metrics=(metric(0.2),),
            evaluator_id="scorer",
            evaluator_source_ref="scorer:receipt",
        )


@pytest.mark.parametrize("unsupported_field", ("task_regime", "interaction_history"))
def test_unbound_task_or_history_conditions_cannot_be_manipulated(
    unsupported_field: str,
) -> None:
    with pytest.raises(StudyError, match="unsupported manipulated_fields"):
        replace(contrast(), manipulated_fields=(unsupported_field,))


def test_required_metric_held_out_status_drift_fails_closed() -> None:
    harness = InteractionHistoryStudyHarness()
    harness.add_trial(trial("absent", artifacts=Presence.ABSENT, peer=Presence.ABSENT, value=0.1))
    changed = trial("present", artifacts=Presence.PRESENT, peer=Presence.PRESENT, value=0.4)
    changed = replace(changed, metrics=(replace(changed.metrics[0], held_out=False),))
    harness.add_trial(changed)

    with pytest.raises(StudyError, match="held_out"):
        harness.audit_contrast(contrast())


@pytest.mark.parametrize("raw_value", ("True", "False", 1, 0))
def test_metric_held_out_requires_exact_bool(raw_value: object) -> None:
    with pytest.raises(StudyError, match="held_out"):
        MetricObservation(
            MetricName.BRANCH_CHANGE_RATE,
            0.5,
            "ratio",
            ("score:raw-held-out",),
            held_out=raw_value,
        )
