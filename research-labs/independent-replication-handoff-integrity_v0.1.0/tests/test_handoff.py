from __future__ import annotations

from aion_replication_handoff import (
    AccessManifest,
    ArtifactManifest,
    ArtifactMode,
    EnvironmentManifest,
    HandoffStatus,
    IndependenceAttestation,
    ReplicationHandoff,
    Disposition,
    audit_handoff,
)


def handoff(**changes: object) -> ReplicationHandoff:
    artifact = ArtifactManifest(
        artifact_id="artifact-1",
        artifact_digest="sha256:artifact-1",
        source_commit="commit:source-1",
        source_url="https://example.org/artifact-1",
        entrypoint_ref="entry:run",
        input_manifest_ref="input:manifest",
        output_schema_ref="output:schema",
        license_ref="license:mit",
    )
    environment = EnvironmentManifest(
        runtime_ref="python:3.11",
        operating_system_ref="os:linux",
        dependency_lock_ref="deps:lock-1",
        hardware_assumption_ref="hardware:cpu",
        container_digest="sha256:container-1",
        seed_policy_ref="seed:fixed",
    )
    access = AccessManifest(True, True, True, True, "public synthetic fixture")
    independence = IndependenceAttestation(
        receiving_team_id="team-receiver",
        source_team_id="team-source",
        conflict_declaration="none declared",
        independent_execution_ref="run:receiver-1",
        blinding_status="artifact-review-blinded",
    )
    values: dict[str, object] = {
        "handoff_id": "handoff-1",
        "study_question_ref": "question:1",
        "estimand_ref": "estimand:1",
        "artifact": artifact,
        "environment": environment,
        "access": access,
        "independence": independence,
        "mode": ArtifactMode.SAME_ARTIFACT,
        "expected_output_ref": "expected:output",
        "deviation_log_ref": "deviation:none",
        "outcome_observation_ref": None,
    }
    values.update(changes)
    return ReplicationHandoff(**values)


def test_complete_same_artifact_handoff_is_admissible_only() -> None:
    result = audit_handoff(handoff())
    assert result.status is HandoffStatus.COMPLETE
    assert result.disposition is Disposition.ADMISSIBLE_FOR_REPLICATION_REVIEW
    assert result.reason == "HANDOFF_MANIFEST_COMPLETE"
    assert result.replication_result == "NOT_EVALUATED"


def test_complete_independent_recreation_requires_source_reference() -> None:
    result = audit_handoff(handoff(mode=ArtifactMode.INDEPENDENT_RECREATION))
    assert result.status is HandoffStatus.COMPLETE
    assert result.disposition is Disposition.ADMISSIBLE_FOR_REPLICATION_REVIEW


def test_missing_dependency_lock_holds() -> None:
    environment = EnvironmentManifest("python:3.11", "os:linux", None, "hardware:cpu", "sha256:container", "seed:fixed")
    result = audit_handoff(handoff(environment=environment))
    assert result.status is HandoffStatus.INDETERMINATE
    assert result.reason == "HANDOFF_MANIFEST_INCOMPLETE"
    assert "environment.dependency_lock_ref" in result.missing_fields


def test_missing_entrypoint_holds() -> None:
    artifact = ArtifactManifest("artifact-1", "sha256:a", "commit:s", "https://example.org/a", None, "input:m", "output:s", "license:mit")
    result = audit_handoff(handoff(artifact=artifact))
    assert result.status is HandoffStatus.INDETERMINATE
    assert "artifact.entrypoint_ref" in result.missing_fields


def test_access_incomplete_holds_and_names_flags() -> None:
    result = audit_handoff(handoff(access=AccessManifest(False, True, False, True, "restricted")))
    assert result.status is HandoffStatus.INDETERMINATE
    assert result.reason == "HANDOFF_ACCESS_INCOMPLETE"
    assert result.contradiction_fields == ("artifact_accessible", "dependency_accessible")


def test_license_incompatibility_is_invalid() -> None:
    result = audit_handoff(handoff(access=AccessManifest(True, True, True, False, "license unresolved")))
    assert result.status is HandoffStatus.INVALID
    assert result.reason == "LICENSE_COMPATIBILITY_UNRESOLVED"


def test_same_team_independence_attestation_is_invalid() -> None:
    independence = IndependenceAttestation("team-source", "team-source", "none", "run:1", "blinded")
    result = audit_handoff(handoff(independence=independence))
    assert result.status is HandoffStatus.INVALID
    assert result.reason == "INDEPENDENCE_ATTESTATION_CONTRADICTORY"


def test_same_artifact_execution_ref_collision_is_invalid() -> None:
    independence = IndependenceAttestation("team-receiver", "team-source", "none", "sha256:artifact-1", "blinded")
    result = audit_handoff(handoff(independence=independence))
    assert result.status is HandoffStatus.INVALID
    assert result.reason == "INDEPENDENT_EXECUTION_REF_COLLIDES_WITH_SOURCE_ARTIFACT"


def test_independent_recreation_without_source_url_holds() -> None:
    artifact = ArtifactManifest("artifact-1", "sha256:a", "commit:s", None, "entry:run", "input:m", "output:s", "license:mit")
    result = audit_handoff(handoff(artifact=artifact, mode=ArtifactMode.INDEPENDENT_RECREATION))
    assert result.status is HandoffStatus.INDETERMINATE
    assert result.reason == "INDEPENDENT_RECREATION_SOURCE_REFERENCE_MISSING"


def test_missing_study_question_holds() -> None:
    result = audit_handoff(handoff(study_question_ref=None))
    assert result.status is HandoffStatus.INDETERMINATE
    assert "study_question_ref" in result.missing_fields


def test_missing_blinding_status_holds() -> None:
    independence = IndependenceAttestation("team-receiver", "team-source", "none", "run:1", None)
    result = audit_handoff(handoff(independence=independence))
    assert result.status is HandoffStatus.INDETERMINATE
    assert "independence.blinding_status" in result.missing_fields


def test_access_notes_are_not_a_substitute_for_access_flags() -> None:
    result = audit_handoff(handoff(access=AccessManifest(False, False, False, True, "available on request")))
    assert result.status is HandoffStatus.INDETERMINATE
    assert result.reason == "HANDOFF_ACCESS_INCOMPLETE"


def test_serialization_uses_enum_values_and_boundary_invariants() -> None:
    payload = audit_handoff(handoff()).as_dict()
    assert payload["status"] == "COMPLETE"
    assert payload["disposition"] == "ADMISSIBLE_FOR_REPLICATION_REVIEW"
    assert payload["replication_result"] == "NOT_EVALUATED"
    assert payload["canonical_effect"] == "NONE"
    assert payload["deployment"] is False
    assert payload["subjectivity_conclusion"] == "NOT_ESTABLISHED"
    assert payload["identity_continuity_conclusion"] == "NOT_ESTABLISHED"
