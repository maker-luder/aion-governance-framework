"""Independent replication handoff artifact-integrity contract."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any


class HandoffStatus(StrEnum):
    COMPLETE = "COMPLETE"
    INDETERMINATE = "INDETERMINATE"
    INVALID = "INVALID"


class Disposition(StrEnum):
    ADMISSIBLE_FOR_REPLICATION_REVIEW = "ADMISSIBLE_FOR_REPLICATION_REVIEW"
    HOLD = "HOLD"


class ArtifactMode(StrEnum):
    SAME_ARTIFACT = "SAME_ARTIFACT"
    INDEPENDENT_RECREATION = "INDEPENDENT_RECREATION"


@dataclass(frozen=True, slots=True)
class ArtifactManifest:
    artifact_id: str
    artifact_digest: str | None
    source_commit: str | None
    source_url: str | None
    entrypoint_ref: str | None
    input_manifest_ref: str | None
    output_schema_ref: str | None
    license_ref: str | None


@dataclass(frozen=True, slots=True)
class EnvironmentManifest:
    runtime_ref: str | None
    operating_system_ref: str | None
    dependency_lock_ref: str | None
    hardware_assumption_ref: str | None
    container_digest: str | None
    seed_policy_ref: str | None


@dataclass(frozen=True, slots=True)
class AccessManifest:
    artifact_accessible: bool
    input_accessible: bool
    dependency_accessible: bool
    license_compatible: bool
    access_notes: str | None


@dataclass(frozen=True, slots=True)
class IndependenceAttestation:
    receiving_team_id: str | None
    source_team_id: str | None
    conflict_declaration: str | None
    independent_execution_ref: str | None
    blinding_status: str | None


@dataclass(frozen=True, slots=True)
class ReplicationHandoff:
    handoff_id: str
    study_question_ref: str | None
    estimand_ref: str | None
    artifact: ArtifactManifest
    environment: EnvironmentManifest
    access: AccessManifest
    independence: IndependenceAttestation
    mode: ArtifactMode
    expected_output_ref: str | None
    deviation_log_ref: str | None
    outcome_observation_ref: str | None


@dataclass(frozen=True, slots=True)
class HandoffDecision:
    status: HandoffStatus
    disposition: Disposition
    reason: str
    handoff_id: str
    missing_fields: tuple[str, ...] = ()
    contradiction_fields: tuple[str, ...] = ()
    artifact_mode: ArtifactMode | None = None
    replication_result: str = "NOT_EVALUATED"
    scientific_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    deployment: bool = False
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    identity_continuity_conclusion: str = "NOT_ESTABLISHED"

    def as_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["status"] = self.status.value
        payload["disposition"] = self.disposition.value
        if self.artifact_mode is not None:
            payload["artifact_mode"] = self.artifact_mode.value
        return payload


def _missing(values: dict[str, object]) -> tuple[str, ...]:
    return tuple(key for key, value in values.items() if value is None or value == "")


def audit_handoff(handoff: ReplicationHandoff) -> HandoffDecision:
    """Audit a handoff manifest only; never runs the replication."""

    if not handoff.handoff_id:
        return HandoffDecision(HandoffStatus.INVALID, Disposition.HOLD, "MISSING_HANDOFF_ID", handoff.handoff_id)

    required = {
        "study_question_ref": handoff.study_question_ref,
        "estimand_ref": handoff.estimand_ref,
        "artifact.artifact_id": handoff.artifact.artifact_id,
        "artifact.artifact_digest": handoff.artifact.artifact_digest,
        "artifact.source_commit": handoff.artifact.source_commit,
        "artifact.entrypoint_ref": handoff.artifact.entrypoint_ref,
        "artifact.input_manifest_ref": handoff.artifact.input_manifest_ref,
        "artifact.output_schema_ref": handoff.artifact.output_schema_ref,
        "environment.runtime_ref": handoff.environment.runtime_ref,
        "environment.operating_system_ref": handoff.environment.operating_system_ref,
        "environment.dependency_lock_ref": handoff.environment.dependency_lock_ref,
        "environment.seed_policy_ref": handoff.environment.seed_policy_ref,
        "independence.receiving_team_id": handoff.independence.receiving_team_id,
        "independence.source_team_id": handoff.independence.source_team_id,
        "independence.conflict_declaration": handoff.independence.conflict_declaration,
        "independence.independent_execution_ref": handoff.independence.independent_execution_ref,
        "independence.blinding_status": handoff.independence.blinding_status,
        "expected_output_ref": handoff.expected_output_ref,
    }
    missing = _missing(required)
    if missing:
        return HandoffDecision(
            HandoffStatus.INDETERMINATE,
            Disposition.HOLD,
            "HANDOFF_MANIFEST_INCOMPLETE",
            handoff.handoff_id,
            missing_fields=missing,
            artifact_mode=handoff.mode,
        )

    if handoff.independence.receiving_team_id == handoff.independence.source_team_id:
        return HandoffDecision(
            HandoffStatus.INVALID,
            Disposition.HOLD,
            "INDEPENDENCE_ATTESTATION_CONTRADICTORY",
            handoff.handoff_id,
            contradiction_fields=("receiving_team_id", "source_team_id"),
            artifact_mode=handoff.mode,
        )
    if not handoff.access.artifact_accessible or not handoff.access.input_accessible or not handoff.access.dependency_accessible:
        return HandoffDecision(
            HandoffStatus.INDETERMINATE,
            Disposition.HOLD,
            "HANDOFF_ACCESS_INCOMPLETE",
            handoff.handoff_id,
            contradiction_fields=tuple(
                key
                for key, value in {
                    "artifact_accessible": handoff.access.artifact_accessible,
                    "input_accessible": handoff.access.input_accessible,
                    "dependency_accessible": handoff.access.dependency_accessible,
                }.items()
                if not value
            ),
            artifact_mode=handoff.mode,
        )
    if not handoff.access.license_compatible:
        return HandoffDecision(
            HandoffStatus.INVALID,
            Disposition.HOLD,
            "LICENSE_COMPATIBILITY_UNRESOLVED",
            handoff.handoff_id,
            artifact_mode=handoff.mode,
        )
    if handoff.mode is ArtifactMode.SAME_ARTIFACT and handoff.independence.independent_execution_ref == handoff.artifact.artifact_digest:
        return HandoffDecision(
            HandoffStatus.INVALID,
            Disposition.HOLD,
            "INDEPENDENT_EXECUTION_REF_COLLIDES_WITH_SOURCE_ARTIFACT",
            handoff.handoff_id,
            contradiction_fields=("independent_execution_ref", "artifact_digest"),
            artifact_mode=handoff.mode,
        )
    if handoff.mode is ArtifactMode.INDEPENDENT_RECREATION and handoff.artifact.source_url is None:
        return HandoffDecision(
            HandoffStatus.INDETERMINATE,
            Disposition.HOLD,
            "INDEPENDENT_RECREATION_SOURCE_REFERENCE_MISSING",
            handoff.handoff_id,
            missing_fields=("artifact.source_url",),
            artifact_mode=handoff.mode,
        )

    return HandoffDecision(
        HandoffStatus.COMPLETE,
        Disposition.ADMISSIBLE_FOR_REPLICATION_REVIEW,
        "HANDOFF_MANIFEST_COMPLETE",
        handoff.handoff_id,
        artifact_mode=handoff.mode,
    )
