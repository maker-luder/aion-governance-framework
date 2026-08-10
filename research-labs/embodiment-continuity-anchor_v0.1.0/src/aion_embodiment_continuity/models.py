from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class AnchorDecision(str, Enum):
    PASS = "PASS"
    HOLD = "HOLD"
    FAIL = "FAIL"


class DimensionStatus(str, Enum):
    PASS = "PASS"
    HOLD = "HOLD"
    FAIL = "FAIL"
    NOT_ASSESSED = "NOT_ASSESSED"


@dataclass(frozen=True, slots=True)
class LineageAnchor:
    agent_id: str
    genesis_root_id: str
    memory_stream_id: str
    event_lineage_id: str
    canonical_state_reference: str
    lifecycle_epoch: str

    def __post_init__(self) -> None:
        for name in (
            "agent_id",
            "genesis_root_id",
            "memory_stream_id",
            "event_lineage_id",
            "canonical_state_reference",
            "lifecycle_epoch",
        ):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must be non-empty")

    def stable_tuple(self) -> tuple[str, ...]:
        return (
            self.agent_id,
            self.genesis_root_id,
            self.memory_stream_id,
            self.event_lineage_id,
            self.canonical_state_reference,
            self.lifecycle_epoch,
        )


@dataclass(frozen=True, slots=True)
class EmbodimentBinding:
    embodiment_id: str
    runtime_instance_id: str
    environment_fingerprint: str
    bound_at: datetime
    model_artifact_id: str | None = None
    inference_backend_id: str | None = None
    hardware_fingerprint: str | None = None

    def __post_init__(self) -> None:
        for name in ("embodiment_id", "runtime_instance_id", "environment_fingerprint"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must be non-empty")
        for name in ("model_artifact_id", "inference_backend_id", "hardware_fingerprint"):
            value = getattr(self, name)
            if value is not None and not value.strip():
                raise ValueError(f"{name} must be non-empty when provided")
        if self.bound_at.tzinfo is None or self.bound_at.utcoffset() is None:
            raise ValueError("bound_at must be timezone-aware")


@dataclass(frozen=True, slots=True)
class MigrationObservation:
    before_anchor: LineageAnchor
    after_anchor: LineageAnchor
    before_binding: EmbodimentBinding
    after_binding: EmbodimentBinding
    provenance_refs: tuple[str, ...]
    state_drift_observed: bool = False
    memory_integrity_observed: bool | None = None
    interpretive_drift_observed: bool | None = None
    relationship_drift_observed: bool | None = None

    def __post_init__(self) -> None:
        if not self.provenance_refs:
            raise ValueError("migration observation requires provenance_refs")


@dataclass(frozen=True, slots=True)
class AnchorAssessment:
    decision: AnchorDecision
    lineage_preserved: bool
    implementation_changed: bool
    embodiment_changed: bool
    runtime_changed: bool
    environment_changed: bool
    model_changed: bool
    inference_backend_changed: bool
    hardware_changed: bool
    state_drift_observed: bool
    relationship_drift_observed: bool | None
    identity_continuity_conclusion: str
    reasons: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ContinuityDimensionAssessment:
    subject_lineage: DimensionStatus
    memory_lineage: DimensionStatus
    interpretive_continuity: DimensionStatus
    relational_continuity: DimensionStatus
    implementation_migration: DimensionStatus
    identity_continuity_conclusion: str
    reasons: tuple[str, ...]


def _changed(before: str | None, after: str | None) -> bool:
    return before != after


def assess_anchor_continuity(observation: MigrationObservation) -> AnchorAssessment:
    reasons: list[str] = []
    lineage_preserved = observation.before_anchor.stable_tuple() == observation.after_anchor.stable_tuple()
    runtime_changed = _changed(
        observation.before_binding.runtime_instance_id,
        observation.after_binding.runtime_instance_id,
    )
    embodiment_changed = _changed(
        observation.before_binding.embodiment_id,
        observation.after_binding.embodiment_id,
    )
    environment_changed = _changed(
        observation.before_binding.environment_fingerprint,
        observation.after_binding.environment_fingerprint,
    )
    model_changed = _changed(
        observation.before_binding.model_artifact_id,
        observation.after_binding.model_artifact_id,
    )
    inference_backend_changed = _changed(
        observation.before_binding.inference_backend_id,
        observation.after_binding.inference_backend_id,
    )
    hardware_changed = _changed(
        observation.before_binding.hardware_fingerprint,
        observation.after_binding.hardware_fingerprint,
    )
    implementation_changed = any(
        (
            runtime_changed,
            embodiment_changed,
            environment_changed,
            model_changed,
            inference_backend_changed,
            hardware_changed,
        )
    )

    if not lineage_preserved:
        reasons.append("STABLE_LINEAGE_ANCHOR_CHANGED")
        return AnchorAssessment(
            decision=AnchorDecision.FAIL,
            lineage_preserved=False,
            implementation_changed=implementation_changed,
            embodiment_changed=embodiment_changed,
            runtime_changed=runtime_changed,
            environment_changed=environment_changed,
            model_changed=model_changed,
            inference_backend_changed=inference_backend_changed,
            hardware_changed=hardware_changed,
            state_drift_observed=observation.state_drift_observed,
            relationship_drift_observed=observation.relationship_drift_observed,
            identity_continuity_conclusion="NOT_ESTABLISHED",
            reasons=tuple(reasons),
        )

    if not implementation_changed:
        reasons.append("NO_IMPLEMENTATION_MIGRATION_OBSERVED")
    if observation.relationship_drift_observed is True:
        reasons.append("RELATIONAL_CONTINUITY_REQUIRES_SEPARATE_REVIEW")
    if observation.interpretive_drift_observed is True:
        reasons.append("INTERPRETIVE_CONTINUITY_REQUIRES_SEPARATE_REVIEW")
    if observation.state_drift_observed:
        reasons.append("STATE_DRIFT_DOES_NOT_BY_ITSELF_BREAK_LINEAGE")

    decision = (
        AnchorDecision.HOLD
        if observation.relationship_drift_observed is True
        or observation.interpretive_drift_observed is True
        else AnchorDecision.PASS
    )
    return AnchorAssessment(
        decision=decision,
        lineage_preserved=True,
        implementation_changed=implementation_changed,
        embodiment_changed=embodiment_changed,
        runtime_changed=runtime_changed,
        environment_changed=environment_changed,
        model_changed=model_changed,
        inference_backend_changed=inference_backend_changed,
        hardware_changed=hardware_changed,
        state_drift_observed=observation.state_drift_observed,
        relationship_drift_observed=observation.relationship_drift_observed,
        identity_continuity_conclusion="NOT_ESTABLISHED",
        reasons=tuple(reasons),
    )


def assess_continuity_dimensions(
    observation: MigrationObservation,
) -> ContinuityDimensionAssessment:
    reasons: list[str] = []
    anchor_assessment = assess_anchor_continuity(observation)

    subject_lineage = (
        DimensionStatus.PASS if anchor_assessment.lineage_preserved else DimensionStatus.FAIL
    )

    memory_stream_preserved = (
        observation.before_anchor.memory_stream_id == observation.after_anchor.memory_stream_id
    )
    if not memory_stream_preserved:
        memory_lineage = DimensionStatus.FAIL
        reasons.append("MEMORY_STREAM_ID_CHANGED")
    elif observation.memory_integrity_observed is True:
        memory_lineage = DimensionStatus.PASS
    elif observation.memory_integrity_observed is False:
        memory_lineage = DimensionStatus.FAIL
        reasons.append("MEMORY_INTEGRITY_NOT_PRESERVED")
    else:
        memory_lineage = DimensionStatus.NOT_ASSESSED

    if observation.interpretive_drift_observed is True:
        interpretive_continuity = DimensionStatus.HOLD
        reasons.append("INTERPRETIVE_DRIFT_OBSERVED")
    elif observation.interpretive_drift_observed is False:
        interpretive_continuity = DimensionStatus.PASS
    else:
        interpretive_continuity = DimensionStatus.NOT_ASSESSED

    if observation.relationship_drift_observed is True:
        relational_continuity = DimensionStatus.HOLD
        reasons.append("RELATIONSHIP_DRIFT_OBSERVED")
    elif observation.relationship_drift_observed is False:
        relational_continuity = DimensionStatus.PASS
    else:
        relational_continuity = DimensionStatus.NOT_ASSESSED

    if not anchor_assessment.lineage_preserved:
        implementation_migration = DimensionStatus.HOLD
        reasons.append("IMPLEMENTATION_MIGRATION_CANNOT_ESTABLISH_LINEAGE_AFTER_ANCHOR_CHANGE")
    elif anchor_assessment.implementation_changed:
        implementation_migration = DimensionStatus.PASS
    else:
        implementation_migration = DimensionStatus.NOT_ASSESSED

    return ContinuityDimensionAssessment(
        subject_lineage=subject_lineage,
        memory_lineage=memory_lineage,
        interpretive_continuity=interpretive_continuity,
        relational_continuity=relational_continuity,
        implementation_migration=implementation_migration,
        identity_continuity_conclusion="NOT_ESTABLISHED",
        reasons=tuple(reasons),
    )
