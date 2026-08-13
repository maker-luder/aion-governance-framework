from __future__ import annotations

from aion_replication_environment_drift import (
    ArtifactMode,
    ArtifactRecord,
    EnvironmentMatch,
    EnvironmentRecord,
    InterpretationState,
    ReplicationPacket,
    ResultState,
    ReviewStatus,
    audit_replication_packet,
)


def artifact(*, mode: ArtifactMode = ArtifactMode.SAME_ARTIFACT_REPLAY, source_team: str = "team:source", receiving_team: str = "team:receiver", accessible: bool = True, independent_ref: str | None = "artifact:independent", independent_digest: str | None = "sha256:independent") -> ArtifactRecord:
    return ArtifactRecord(
        artifact_id="artifact:source-001",
        artifact_digest="sha256:source-artifact",
        source_commit="commit:source-001",
        entrypoint_ref="entrypoint:run",
        input_manifest_ref="inputs:manifest",
        output_schema_ref="outputs:schema",
        license_ref="license:compatible",
        artifact_accessible=accessible,
        source_team_id=source_team,
        receiving_team_id=receiving_team,
        independent_artifact_ref=independent_ref,
        independent_artifact_digest=independent_digest,
        mode=mode,
    )


def environment(*, runtime: str = "runtime:python-3.11", os_ref: str = "os:linux", deps: str = "deps:lock-1", seed: str = "seed:declared", condition: str = "condition:exact", match: EnvironmentMatch = EnvironmentMatch.EXACT, deviation: str | None = None) -> EnvironmentRecord:
    return EnvironmentRecord(
        runtime_ref=runtime,
        operating_system_ref=os_ref,
        dependency_lock_ref=deps,
        hardware_assumption_ref="hardware:cpu",
        container_digest="container:sha256:1",
        seed_policy_ref=seed,
        condition_digest=condition,
        match=match,
        deviation_log_ref=deviation,
    )


def packet(**changes: object) -> ReplicationPacket:
    values: dict[str, object] = {
        "packet_id": "replication-packet-001",
        "study_question_ref": "question:study-001",
        "estimand_ref": "estimand:declared-001",
        "source_evidence_refs": (
            "repo:independent-replication-design@76de1eda",
            "literature:national-academies-25303",
        ),
        "preregistration_ref": "preregistration:replication-001",
        "method_ref": "method:locked-protocol",
        "source_artifact": artifact(),
        "receiving_environment": environment(),
        "source_environment": environment(),
        "expected_tolerance_ref": "tolerance:predeclared",
        "uncertainty_ref": "uncertainty:reported",
        "interpretation_ref": "interpretation:review-only",
        "result_state": ResultState.NOT_EVALUATED,
        "observed_result_ref": None,
        "interpretation_state": InterpretationState.REVIEW_ONLY,
        "scientific_conclusion": "NOT_ESTABLISHED",
        "canonical_effect": "NONE",
        "governance_effect": "NONE",
        "deployment": False,
    }
    values.update(changes)
    return ReplicationPacket(**values)


def test_same_artifact_readiness_is_admissible_for_review() -> None:
    result = audit_replication_packet(packet())
    assert result.status is ReviewStatus.COMPLETE
    assert result.reason == "REPLICATION_READINESS_COMPLETE"
    assert result.result_state is ResultState.NOT_EVALUATED


def test_independent_recreation_readiness_is_admissible() -> None:
    result = audit_replication_packet(packet(source_artifact=artifact(mode=ArtifactMode.INDEPENDENT_RECREATION)))
    assert result.status is ReviewStatus.COMPLETE
    assert result.reason == "REPLICATION_READINESS_COMPLETE"


def test_missing_source_evidence_is_indeterminate() -> None:
    result = audit_replication_packet(packet(source_evidence_refs=()))
    assert result.status is ReviewStatus.INDETERMINATE
    assert result.reason == "REPLICATION_PACKET_INCOMPLETE"
    assert "source_evidence_refs" in result.missing_fields


def test_source_and_receiving_team_collision_is_invalid() -> None:
    result = audit_replication_packet(packet(source_artifact=artifact(receiving_team="team:source")))
    assert result.status is ReviewStatus.INVALID
    assert result.reason == "INDEPENDENCE_TEAM_COLLISION"


def test_inaccessible_artifact_is_indeterminate() -> None:
    result = audit_replication_packet(packet(source_artifact=artifact(accessible=False)))
    assert result.status is ReviewStatus.INDETERMINATE
    assert result.reason == "SOURCE_ARTIFACT_INACCESSIBLE"


def test_independent_recreation_missing_artifact_metadata_is_indeterminate() -> None:
    result = audit_replication_packet(packet(source_artifact=artifact(mode=ArtifactMode.INDEPENDENT_RECREATION, independent_ref=None, independent_digest=None)))
    assert result.status is ReviewStatus.INDETERMINATE
    assert result.reason == "INDEPENDENT_RECREATION_METADATA_INCOMPLETE"


def test_independent_artifact_digest_collision_is_invalid() -> None:
    result = audit_replication_packet(packet(source_artifact=artifact(mode=ArtifactMode.INDEPENDENT_RECREATION, independent_digest="sha256:source-artifact")))
    assert result.status is ReviewStatus.INVALID
    assert result.reason == "INDEPENDENT_ARTIFACT_DIGEST_COLLISION"


def test_declared_exact_environment_is_admissible() -> None:
    result = audit_replication_packet(packet())
    assert result.status is ReviewStatus.COMPLETE
    assert result.environment_match is EnvironmentMatch.EXACT


def test_declared_environment_drift_with_log_is_admissible_for_review() -> None:
    receiving = environment(runtime="runtime:python-3.12", match=EnvironmentMatch.DRIFT_DECLARED, deviation="deviation:runtime")
    result = audit_replication_packet(packet(receiving_environment=receiving))
    assert result.status is ReviewStatus.COMPLETE
    assert result.reason == "REPLICATION_READINESS_COMPLETE"


def test_declared_environment_drift_without_log_is_indeterminate() -> None:
    receiving = environment(runtime="runtime:python-3.12", match=EnvironmentMatch.DRIFT_DECLARED)
    result = audit_replication_packet(packet(receiving_environment=receiving))
    assert result.status is ReviewStatus.INDETERMINATE
    assert result.reason == "DECLARED_DRIFT_WITHOUT_DEVIATION_LOG"


def test_undeclared_environment_drift_is_invalid() -> None:
    receiving = environment(runtime="runtime:python-3.12", match=EnvironmentMatch.DRIFT_UNDECLARED)
    result = audit_replication_packet(packet(receiving_environment=receiving))
    assert result.status is ReviewStatus.INVALID
    assert result.reason == "UNDECLARED_ENVIRONMENT_DRIFT"


def test_unknown_environment_comparability_is_indeterminate() -> None:
    receiving = environment(match=EnvironmentMatch.UNKNOWN)
    result = audit_replication_packet(packet(receiving_environment=receiving))
    assert result.status is ReviewStatus.INDETERMINATE
    assert result.reason == "ENVIRONMENT_COMPARABILITY_UNKNOWN"


def test_exact_environment_claim_with_drift_is_contradictory() -> None:
    receiving = environment(runtime="runtime:python-3.12", match=EnvironmentMatch.EXACT)
    result = audit_replication_packet(packet(receiving_environment=receiving))
    assert result.status is ReviewStatus.INVALID
    assert result.reason == "EXACT_ENVIRONMENT_DECLARATION_CONTRADICTED"


def test_reported_consistent_result_requires_observed_reference_and_review_scope() -> None:
    result = audit_replication_packet(
        packet(result_state=ResultState.CONSISTENT, observed_result_ref="result:consistent", interpretation_state=InterpretationState.REVIEW_ONLY)
    )
    assert result.status is ReviewStatus.COMPLETE
    assert result.reason == "REPLICATION_RESULT_ADMISSIBLE_FOR_REVIEW"
    assert result.scientific_conclusion == "NOT_ESTABLISHED"


def test_reported_divergence_without_review_interpretation_is_indeterminate() -> None:
    result = audit_replication_packet(
        packet(result_state=ResultState.DIVERGENT, observed_result_ref="result:divergent", interpretation_state=InterpretationState.NOT_ESTABLISHED)
    )
    assert result.status is ReviewStatus.INDETERMINATE
    assert result.reason == "RESULT_REPORTED_WITHOUT_REVIEW_INTERPRETATION"


def test_result_state_without_observed_reference_is_invalid() -> None:
    result = audit_replication_packet(packet(result_state=ResultState.CONSISTENT))
    assert result.status is ReviewStatus.INVALID
    assert result.reason == "RESULT_STATE_WITHOUT_OBSERVED_RESULT_REF"


def test_observed_reference_with_not_evaluated_state_is_invalid() -> None:
    result = audit_replication_packet(packet(observed_result_ref="result:unexpected"))
    assert result.status is ReviewStatus.INVALID
    assert result.reason == "OBSERVED_RESULT_WITH_NOT_EVALUATED_STATE"


def test_interpretation_overreach_is_invalid() -> None:
    result = audit_replication_packet(
        packet(result_state=ResultState.CONSISTENT, observed_result_ref="result:consistent", interpretation_state=InterpretationState.OVERREACHING)
    )
    assert result.status is ReviewStatus.INVALID
    assert result.reason == "INTERPRETATION_OVERREACH"


def test_scientific_conclusion_overreach_is_invalid() -> None:
    result = audit_replication_packet(packet(scientific_conclusion="CONFIRMED"))
    assert result.status is ReviewStatus.INVALID
    assert result.reason == "SCIENTIFIC_CONCLUSION_OVERREACH"


def test_boundary_effect_request_is_invalid() -> None:
    for changes in ({"canonical_effect": "WRITE"}, {"governance_effect": "PROMOTE"}, {"deployment": True}):
        result = audit_replication_packet(packet(**changes))
        assert result.status is ReviewStatus.INVALID
        assert result.reason == "BOUNDARY_EFFECT_REQUESTED"


def test_decision_serializes_nonpromotion_fields() -> None:
    payload = audit_replication_packet(packet()).as_dict()
    assert payload["result_state"] == "NOT_EVALUATED"
    assert payload["environment_match"] == "EXACT"
    assert payload["scientific_conclusion"] == "NOT_ESTABLISHED"
    assert payload["canonical_effect"] == "NONE"
    assert payload["governance_effect"] == "NONE"
    assert payload["deployment"] is False
