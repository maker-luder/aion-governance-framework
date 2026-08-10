from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class AnchorDecision(str, Enum):
    PASS = "PASS"
    HOLD = "HOLD"
    FAIL = "FAIL"


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

    def __post_init__(self) -> None:
        for name in ("embodiment_id", "runtime_instance_id", "environment_fingerprint"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must be non-empty")
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
    relationship_drift_observed: bool = False

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
    state_drift_observed: bool
    relationship_drift_observed: bool
    identity_continuity_conclusion: str
    reasons: tuple[str, ...]


def assess_anchor_continuity(observation: MigrationObservation) -> AnchorAssessment:
    reasons: list[str] = []
    lineage_preserved = observation.before_anchor.stable_tuple() == observation.after_anchor.stable_tuple()
    runtime_changed = (
        observation.before_binding.runtime_instance_id
        != observation.after_binding.runtime_instance_id
    )
    embodiment_changed = observation.before_binding.embodiment_id != observation.after_binding.embodiment_id
    environment_changed = (
        observation.before_binding.environment_fingerprint
        != observation.after_binding.environment_fingerprint
    )
    implementation_changed = runtime_changed or embodiment_changed or environment_changed

    if not lineage_preserved:
        reasons.append("STABLE_LINEAGE_ANCHOR_CHANGED")
        return AnchorAssessment(
            AnchorDecision.FAIL,
            False,
            implementation_changed,
            embodiment_changed,
            runtime_changed,
            observation.state_drift_observed,
            observation.relationship_drift_observed,
            "NOT_ESTABLISHED",
            tuple(reasons),
        )

    if not implementation_changed:
        reasons.append("NO_IMPLEMENTATION_MIGRATION_OBSERVED")

    if observation.relationship_drift_observed:
        reasons.append("RELATIONAL_CONTINUITY_REQUIRES_SEPARATE_REVIEW")
    if observation.state_drift_observed:
        reasons.append("STATE_DRIFT_DOES_NOT_BY_ITSELF_BREAK_LINEAGE")

    decision = AnchorDecision.HOLD if observation.relationship_drift_observed else AnchorDecision.PASS
    return AnchorAssessment(
        decision,
        True,
        implementation_changed,
        embodiment_changed,
        runtime_changed,
        observation.state_drift_observed,
        observation.relationship_drift_observed,
        "NOT_ESTABLISHED",
        tuple(reasons),
    )
