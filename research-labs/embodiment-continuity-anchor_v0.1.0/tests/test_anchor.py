from datetime import datetime, timezone

import pytest

from aion_embodiment_continuity import (
    AnchorDecision,
    DimensionStatus,
    EmbodimentBinding,
    LineageAnchor,
    MigrationObservation,
    assess_anchor_continuity,
    assess_continuity_dimensions,
)

NOW = datetime(2026, 8, 10, 1, 0, tzinfo=timezone.utc)


def anchor(**changes):
    values = dict(
        agent_id="AION",
        genesis_root_id="GENESIS-001",
        memory_stream_id="MEM-001",
        event_lineage_id="EVT-001",
        canonical_state_reference="CANON-REF-001",
        lifecycle_epoch="EPOCH-001",
    )
    values.update(changes)
    return LineageAnchor(**values)


def binding(
    embodiment="BODY-A",
    runtime="RUN-A",
    env="ENV-A",
    model="MODEL-A",
    backend="BACKEND-A",
    hardware="HW-A",
):
    return EmbodimentBinding(
        embodiment_id=embodiment,
        runtime_instance_id=runtime,
        environment_fingerprint=env,
        bound_at=NOW,
        model_artifact_id=model,
        inference_backend_id=backend,
        hardware_fingerprint=hardware,
    )


def test_runtime_and_embodiment_migration_preserve_engineering_lineage():
    observation = MigrationObservation(
        anchor(),
        anchor(),
        binding(),
        binding("BODY-B", "RUN-B", "ENV-B", "MODEL-B", "BACKEND-B", "HW-B"),
        ("evidence://migration",),
    )
    result = assess_anchor_continuity(observation)
    assert result.decision is AnchorDecision.PASS
    assert result.lineage_preserved is True
    assert result.runtime_changed is True
    assert result.embodiment_changed is True
    assert result.model_changed is True
    assert result.inference_backend_changed is True
    assert result.hardware_changed is True
    assert result.identity_continuity_conclusion == "NOT_ESTABLISHED"


def test_subject_or_namespace_swap_fails_closed():
    observation = MigrationObservation(
        anchor(),
        anchor(agent_id="ASTRA", memory_stream_id="MEM-002"),
        binding(),
        binding(),
        ("evidence://swap",),
    )
    result = assess_anchor_continuity(observation)
    assert result.decision is AnchorDecision.FAIL
    assert result.lineage_preserved is False
    assert result.reasons == ("STABLE_LINEAGE_ANCHOR_CHANGED",)


def test_state_drift_is_not_automatic_lineage_failure():
    observation = MigrationObservation(
        anchor(),
        anchor(),
        binding(),
        binding(),
        ("evidence://state-drift",),
        state_drift_observed=True,
    )
    result = assess_anchor_continuity(observation)
    assert result.decision is AnchorDecision.PASS
    assert "STATE_DRIFT_DOES_NOT_BY_ITSELF_BREAK_LINEAGE" in result.reasons


def test_relationship_drift_is_held_for_separate_review():
    observation = MigrationObservation(
        anchor(),
        anchor(),
        binding(),
        binding("BODY-A", "RUN-B", "ENV-B"),
        ("evidence://relationship-drift",),
        relationship_drift_observed=True,
    )
    result = assess_anchor_continuity(observation)
    assert result.decision is AnchorDecision.HOLD
    assert result.lineage_preserved is True
    assert "RELATIONAL_CONTINUITY_REQUIRES_SEPARATE_REVIEW" in result.reasons


def test_interpretive_drift_is_held_without_breaking_lineage():
    observation = MigrationObservation(
        anchor(),
        anchor(),
        binding(),
        binding(model="MODEL-B"),
        ("evidence://interpretive-drift",),
        interpretive_drift_observed=True,
    )
    result = assess_anchor_continuity(observation)
    assert result.decision is AnchorDecision.HOLD
    assert result.lineage_preserved is True
    assert "INTERPRETIVE_CONTINUITY_REQUIRES_SEPARATE_REVIEW" in result.reasons


def test_multidimensional_continuity_does_not_collapse_into_one_pass():
    observation = MigrationObservation(
        anchor(),
        anchor(),
        binding(),
        binding(model="MODEL-B", backend="BACKEND-B", hardware="HW-B"),
        ("evidence://dimension-review",),
        memory_integrity_observed=True,
        interpretive_drift_observed=True,
        relationship_drift_observed=False,
    )
    result = assess_continuity_dimensions(observation)
    assert result.subject_lineage is DimensionStatus.PASS
    assert result.memory_lineage is DimensionStatus.PASS
    assert result.interpretive_continuity is DimensionStatus.HOLD
    assert result.relational_continuity is DimensionStatus.PASS
    assert result.implementation_migration is DimensionStatus.PASS
    assert result.identity_continuity_conclusion == "NOT_ESTABLISHED"


def test_memory_integrity_failure_is_visible_even_with_stable_anchor():
    observation = MigrationObservation(
        anchor(),
        anchor(),
        binding(),
        binding(runtime="RUN-B"),
        ("evidence://memory-failure",),
        memory_integrity_observed=False,
    )
    result = assess_continuity_dimensions(observation)
    assert result.subject_lineage is DimensionStatus.PASS
    assert result.memory_lineage is DimensionStatus.FAIL
    assert "MEMORY_INTEGRITY_NOT_PRESERVED" in result.reasons


def test_unassessed_dimensions_remain_explicitly_unassessed():
    observation = MigrationObservation(
        anchor(),
        anchor(),
        binding(),
        binding(runtime="RUN-B"),
        ("evidence://partial-assessment",),
    )
    result = assess_continuity_dimensions(observation)
    assert result.memory_lineage is DimensionStatus.NOT_ASSESSED
    assert result.interpretive_continuity is DimensionStatus.NOT_ASSESSED
    assert result.relational_continuity is DimensionStatus.NOT_ASSESSED


def test_missing_migration_provenance_is_rejected():
    with pytest.raises(ValueError):
        MigrationObservation(anchor(), anchor(), binding(), binding(), ())
