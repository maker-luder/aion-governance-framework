from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any


class ReviewStatus(StrEnum):
    COMPLETE = "COMPLETE"
    INDETERMINATE = "INDETERMINATE"
    INVALID = "INVALID"


class Disposition(StrEnum):
    ADMISSIBLE_FOR_REVIEW = "ADMISSIBLE_FOR_REVIEW"
    HOLD = "HOLD"


class ArtifactMode(StrEnum):
    SAME_ARTIFACT_REPLAY = "SAME_ARTIFACT_REPLAY"
    INDEPENDENT_RECREATION = "INDEPENDENT_RECREATION"


class EnvironmentMatch(StrEnum):
    EXACT = "EXACT"
    DRIFT_DECLARED = "DRIFT_DECLARED"
    DRIFT_UNDECLARED = "DRIFT_UNDECLARED"
    UNKNOWN = "UNKNOWN"


class ResultState(StrEnum):
    NOT_EVALUATED = "NOT_EVALUATED"
    CONSISTENT = "CONSISTENT"
    DIVERGENT = "DIVERGENT"
    INDETERMINATE = "INDETERMINATE"


class InterpretationState(StrEnum):
    NOT_ESTABLISHED = "NOT_ESTABLISHED"
    REVIEW_ONLY = "REVIEW_ONLY"
    OVERREACHING = "OVERREACHING"


@dataclass(frozen=True, slots=True)
class ArtifactRecord:
    artifact_id: str
    artifact_digest: str | None
    source_commit: str | None
    entrypoint_ref: str | None
    input_manifest_ref: str | None
    output_schema_ref: str | None
    license_ref: str | None
    artifact_accessible: bool
    source_team_id: str | None
    receiving_team_id: str | None
    independent_artifact_ref: str | None
    independent_artifact_digest: str | None
    mode: ArtifactMode


@dataclass(frozen=True, slots=True)
class EnvironmentRecord:
    runtime_ref: str | None
    operating_system_ref: str | None
    dependency_lock_ref: str | None
    hardware_assumption_ref: str | None
    container_digest: str | None
    seed_policy_ref: str | None
    condition_digest: str | None
    match: EnvironmentMatch
    deviation_log_ref: str | None


@dataclass(frozen=True, slots=True)
class ReplicationPacket:
    packet_id: str
    study_question_ref: str | None
    estimand_ref: str | None
    source_evidence_refs: tuple[str, ...]
    preregistration_ref: str | None
    method_ref: str | None
    source_artifact: ArtifactRecord
    receiving_environment: EnvironmentRecord
    source_environment: EnvironmentRecord
    expected_tolerance_ref: str | None
    uncertainty_ref: str | None
    interpretation_ref: str | None
    result_state: ResultState
    observed_result_ref: str | None
    interpretation_state: InterpretationState = InterpretationState.NOT_ESTABLISHED
    scientific_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    governance_effect: str = "NONE"
    deployment: bool = False


@dataclass(frozen=True, slots=True)
class ReplicationDecision:
    status: ReviewStatus
    disposition: Disposition
    reason: str
    packet_id: str
    missing_fields: tuple[str, ...] = ()
    contradiction_fields: tuple[str, ...] = ()
    artifact_mode: ArtifactMode | None = None
    environment_match: EnvironmentMatch | None = None
    result_state: ResultState = ResultState.NOT_EVALUATED
    interpretation_state: InterpretationState = InterpretationState.NOT_ESTABLISHED
    scientific_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    governance_effect: str = "NONE"
    deployment: bool = False

    def as_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["status"] = self.status.value
        payload["disposition"] = self.disposition.value
        if self.artifact_mode is not None:
            payload["artifact_mode"] = self.artifact_mode.value
        if self.environment_match is not None:
            payload["environment_match"] = self.environment_match.value
        payload["result_state"] = self.result_state.value
        payload["interpretation_state"] = self.interpretation_state.value
        return payload


def _missing(values: dict[str, object]) -> tuple[str, ...]:
    return tuple(key for key, value in values.items() if value is None or value == "" or value == ())


def _decision(
    packet: ReplicationPacket,
    status: ReviewStatus,
    disposition: Disposition,
    reason: str,
    *,
    missing: tuple[str, ...] = (),
    contradictions: tuple[str, ...] = (),
) -> ReplicationDecision:
    return ReplicationDecision(
        status=status,
        disposition=disposition,
        reason=reason,
        packet_id=packet.packet_id,
        missing_fields=missing,
        contradiction_fields=contradictions,
        artifact_mode=packet.source_artifact.mode,
        environment_match=packet.receiving_environment.match,
        result_state=packet.result_state,
        interpretation_state=packet.interpretation_state,
        scientific_conclusion=packet.scientific_conclusion,
        canonical_effect=packet.canonical_effect,
        governance_effect=packet.governance_effect,
        deployment=packet.deployment,
    )


def audit_replication_packet(packet: ReplicationPacket) -> ReplicationDecision:
    """Audit replication metadata only; never executes or interprets a result."""
    if packet.canonical_effect != "NONE" or packet.governance_effect != "NONE" or packet.deployment:
        return _decision(packet, ReviewStatus.INVALID, Disposition.HOLD, "BOUNDARY_EFFECT_REQUESTED")
    if packet.scientific_conclusion != "NOT_ESTABLISHED":
        return _decision(packet, ReviewStatus.INVALID, Disposition.HOLD, "SCIENTIFIC_CONCLUSION_OVERREACH")
    if packet.interpretation_state is InterpretationState.OVERREACHING:
        return _decision(packet, ReviewStatus.INVALID, Disposition.HOLD, "INTERPRETATION_OVERREACH")
    if packet.result_state is ResultState.NOT_EVALUATED and packet.observed_result_ref is not None:
        return _decision(packet, ReviewStatus.INVALID, Disposition.HOLD, "OBSERVED_RESULT_WITH_NOT_EVALUATED_STATE", contradictions=("result_state", "observed_result_ref"))
    if packet.result_state is not ResultState.NOT_EVALUATED and packet.observed_result_ref is None:
        return _decision(packet, ReviewStatus.INVALID, Disposition.HOLD, "RESULT_STATE_WITHOUT_OBSERVED_RESULT_REF", contradictions=("result_state", "observed_result_ref"))

    required = {
        "packet_id": packet.packet_id,
        "study_question_ref": packet.study_question_ref,
        "estimand_ref": packet.estimand_ref,
        "source_evidence_refs": packet.source_evidence_refs,
        "preregistration_ref": packet.preregistration_ref,
        "method_ref": packet.method_ref,
        "artifact.artifact_id": packet.source_artifact.artifact_id,
        "artifact.artifact_digest": packet.source_artifact.artifact_digest,
        "artifact.source_commit": packet.source_artifact.source_commit,
        "artifact.entrypoint_ref": packet.source_artifact.entrypoint_ref,
        "artifact.input_manifest_ref": packet.source_artifact.input_manifest_ref,
        "artifact.output_schema_ref": packet.source_artifact.output_schema_ref,
        "artifact.license_ref": packet.source_artifact.license_ref,
        "artifact.source_team_id": packet.source_artifact.source_team_id,
        "artifact.receiving_team_id": packet.source_artifact.receiving_team_id,
        "source_env.runtime_ref": packet.source_environment.runtime_ref,
        "source_env.operating_system_ref": packet.source_environment.operating_system_ref,
        "source_env.dependency_lock_ref": packet.source_environment.dependency_lock_ref,
        "source_env.seed_policy_ref": packet.source_environment.seed_policy_ref,
        "source_env.condition_digest": packet.source_environment.condition_digest,
        "receiving_env.runtime_ref": packet.receiving_environment.runtime_ref,
        "receiving_env.operating_system_ref": packet.receiving_environment.operating_system_ref,
        "receiving_env.dependency_lock_ref": packet.receiving_environment.dependency_lock_ref,
        "receiving_env.seed_policy_ref": packet.receiving_environment.seed_policy_ref,
        "receiving_env.condition_digest": packet.receiving_environment.condition_digest,
        "expected_tolerance_ref": packet.expected_tolerance_ref,
        "uncertainty_ref": packet.uncertainty_ref,
        "interpretation_ref": packet.interpretation_ref,
    }
    missing = _missing(required)
    if missing:
        return _decision(packet, ReviewStatus.INDETERMINATE, Disposition.HOLD, "REPLICATION_PACKET_INCOMPLETE", missing=missing)
    if packet.source_artifact.source_team_id == packet.source_artifact.receiving_team_id:
        return _decision(packet, ReviewStatus.INVALID, Disposition.HOLD, "INDEPENDENCE_TEAM_COLLISION", contradictions=("source_team_id", "receiving_team_id"))
    if not packet.source_artifact.artifact_accessible:
        return _decision(packet, ReviewStatus.INDETERMINATE, Disposition.HOLD, "SOURCE_ARTIFACT_INACCESSIBLE")
    if not packet.source_artifact.license_ref:
        return _decision(packet, ReviewStatus.INDETERMINATE, Disposition.HOLD, "LICENSE_REFERENCE_MISSING")
    if packet.source_artifact.mode is ArtifactMode.INDEPENDENT_RECREATION:
        if packet.source_artifact.independent_artifact_ref is None or packet.source_artifact.independent_artifact_digest is None:
            return _decision(packet, ReviewStatus.INDETERMINATE, Disposition.HOLD, "INDEPENDENT_RECREATION_METADATA_INCOMPLETE", missing=("independent_artifact_ref", "independent_artifact_digest"))
        if packet.source_artifact.independent_artifact_digest == packet.source_artifact.artifact_digest:
            return _decision(packet, ReviewStatus.INVALID, Disposition.HOLD, "INDEPENDENT_ARTIFACT_DIGEST_COLLISION", contradictions=("artifact_digest", "independent_artifact_digest"))
    environment_fields = ("runtime_ref", "operating_system_ref", "dependency_lock_ref", "seed_policy_ref", "condition_digest")
    environment_mismatch = tuple(
        field
        for field in environment_fields
        if getattr(packet.source_environment, field) != getattr(packet.receiving_environment, field)
    )
    if packet.receiving_environment.match is EnvironmentMatch.EXACT and environment_mismatch:
        return _decision(packet, ReviewStatus.INVALID, Disposition.HOLD, "EXACT_ENVIRONMENT_DECLARATION_CONTRADICTED", contradictions=environment_mismatch)
    if packet.receiving_environment.match is EnvironmentMatch.DRIFT_UNDECLARED:
        return _decision(packet, ReviewStatus.INVALID, Disposition.HOLD, "UNDECLARED_ENVIRONMENT_DRIFT")
    if packet.receiving_environment.match is EnvironmentMatch.UNKNOWN:
        return _decision(packet, ReviewStatus.INDETERMINATE, Disposition.HOLD, "ENVIRONMENT_COMPARABILITY_UNKNOWN")
    if packet.receiving_environment.match is EnvironmentMatch.DRIFT_DECLARED and packet.receiving_environment.deviation_log_ref is None:
        return _decision(packet, ReviewStatus.INDETERMINATE, Disposition.HOLD, "DECLARED_DRIFT_WITHOUT_DEVIATION_LOG")
    if packet.interpretation_state is InterpretationState.NOT_ESTABLISHED and packet.result_state is not ResultState.NOT_EVALUATED:
        return _decision(packet, ReviewStatus.INDETERMINATE, Disposition.HOLD, "RESULT_REPORTED_WITHOUT_REVIEW_INTERPRETATION")
    if packet.interpretation_state is InterpretationState.REVIEW_ONLY and packet.result_state is ResultState.NOT_EVALUATED:
        return _decision(packet, ReviewStatus.COMPLETE, Disposition.ADMISSIBLE_FOR_REVIEW, "REPLICATION_READINESS_COMPLETE")
    return _decision(packet, ReviewStatus.COMPLETE, Disposition.ADMISSIBLE_FOR_REVIEW, "REPLICATION_RESULT_ADMISSIBLE_FOR_REVIEW")
