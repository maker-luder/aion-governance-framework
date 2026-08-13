import pytest

from aion_artifact_lineage_adversarial import (
    ArtifactRef,
    AuditStatus,
    EventState,
    LineageEvent,
    audit_transformation_lineage,
    digest_bytes,
    redact_environment,
)


def artifact(path: str = "out.txt", data: bytes = b"output", source: str | None = "repo:source") -> ArtifactRef:
    return ArtifactRef(path, digest_bytes(data), source)


def event(
    event_id: str,
    state: EventState,
    index: int,
    *,
    run_id: str = "run:1",
    source: str | None = "source:commit",
    approval: str | None = "approval:research",
    products: tuple[ArtifactRef, ...] = (),
    materials: tuple[ArtifactRef, ...] = (),
    environment: dict[str, object] | None = None,
    parent: str | None = None,
    namespace: str = "research",
    name: str = "transform",
) -> LineageEvent:
    return LineageEvent(
        event_id=event_id,
        run_id=run_id,
        state=state,
        sequence_index=index,
        event_time=f"2026-08-13T00:0{index}:00Z",
        job_namespace=namespace,
        job_name=name,
        source_ref=source,
        approval_ref=approval,
        materials=materials,
        products=products,
        environment=environment or {"workdir": "/tmp", "API_KEY": "[REDACTED]"},
        parent_run_id=parent,
    )


def valid_events() -> tuple[LineageEvent, LineageEvent]:
    return (
        event("event:1", EventState.START, 1, materials=(artifact("in.txt", b"input"),)),
        event("event:2", EventState.COMPLETE, 2, products=(artifact(),)),
    )


def assert_no_effect(audit) -> None:
    assert audit.canonical_effect == "NONE"
    assert audit.governance_effect == "NONE"
    assert audit.deployment is False
    assert audit.scientific_conclusion == "NOT_ESTABLISHED"
    assert audit.observed_result == "NOT_EVALUATED"


def test_valid_lineage_and_digest_verification() -> None:
    result = audit_transformation_lineage(valid_events(), expected_run_id="run:1", payloads={"out.txt": b"output"})
    assert result.status is AuditStatus.VALID
    assert result.reason == "LINEAGE_COMPLETE_AND_OUTPUTS_VERIFIED"
    assert result.output_verified is True
    assert_no_effect(result)


def test_empty_lineage_holds() -> None:
    result = audit_transformation_lineage((), expected_run_id="run:1")
    assert result.status is AuditStatus.HOLD
    assert result.reason == "LINEAGE_EMPTY"
    assert_no_effect(result)


def test_expected_run_scope_is_required() -> None:
    result = audit_transformation_lineage(valid_events(), expected_run_id="")
    assert result.status is AuditStatus.INVALID
    assert result.reason == "EXPECTED_RUN_ID_MISSING"
    assert_no_effect(result)


def test_run_scope_mismatch_is_invalid() -> None:
    result = audit_transformation_lineage(valid_events(), expected_run_id="run:other")
    assert result.reason == "RUN_ID_SCOPE_MISMATCH"
    assert_no_effect(result)


def test_duplicate_event_id_is_invalid() -> None:
    first, second = valid_events()
    duplicate = event("event:1", EventState.COMPLETE, 2, products=second.products)
    result = audit_transformation_lineage((first, duplicate), expected_run_id="run:1", payloads={"out.txt": b"output"})
    assert result.reason == "DUPLICATE_EVENT_ID"
    assert_no_effect(result)


def test_noncontiguous_sequence_is_invalid() -> None:
    first, second = valid_events()
    result = audit_transformation_lineage((first, event("event:2", EventState.COMPLETE, 3, products=second.products)), expected_run_id="run:1", payloads={"out.txt": b"output"})
    assert result.reason == "SEQUENCE_INDEX_NOT_CONTIGUOUS"
    assert_no_effect(result)


def test_state_order_is_invalid() -> None:
    first, second = valid_events()
    result = audit_transformation_lineage((event("event:bad", EventState.COMPLETE, 1, products=second.products), event("event:2", EventState.START, 2, materials=first.materials)), expected_run_id="run:1", payloads={"out.txt": b"output"})
    assert result.reason == "RUN_STATE_ORDER_INVALID"
    assert_no_effect(result)


def test_unredacted_secret_is_invalid() -> None:
    first, second = valid_events()
    exposed = event("event:1", EventState.START, 1, materials=first.materials, environment={"TOKEN": "raw-secret"})
    result = audit_transformation_lineage((exposed, second), expected_run_id="run:1", payloads={"out.txt": b"output"})
    assert result.reason == "SECRETS_UNREDACTED"
    assert_no_effect(result)


def test_job_identity_drift_is_invalid() -> None:
    first, second = valid_events()
    drifted = event("event:2", EventState.COMPLETE, 2, products=second.products, namespace="other")
    result = audit_transformation_lineage((first, drifted), expected_run_id="run:1", payloads={"out.txt": b"output"})
    assert result.reason == "JOB_IDENTITY_DRIFT"
    assert_no_effect(result)


def test_provenance_drift_holds() -> None:
    first, second = valid_events()
    drifted = event("event:2", EventState.COMPLETE, 2, products=second.products, source="source:other")
    result = audit_transformation_lineage((first, drifted), expected_run_id="run:1", payloads={"out.txt": b"output"})
    assert result.status is AuditStatus.HOLD
    assert result.reason == "PROVENANCE_REFERENCE_DRIFT"
    assert_no_effect(result)


def test_missing_approval_holds() -> None:
    first, second = valid_events()
    missing = event("event:2", EventState.COMPLETE, 2, products=second.products, approval=None)
    result = audit_transformation_lineage((first, missing), expected_run_id="run:1", payloads={"out.txt": b"output"})
    assert result.reason == "PROVENANCE_REFERENCE_DRIFT"
    assert_no_effect(result)


def test_missing_artifact_provenance_holds() -> None:
    first, second = valid_events()
    missing = event("event:2", EventState.COMPLETE, 2, products=(artifact(source=None),))
    result = audit_transformation_lineage((first, missing), expected_run_id="run:1", payloads={"out.txt": b"output"})
    assert result.reason == "ARTIFACT_PROVENANCE_INCOMPLETE"
    assert_no_effect(result)


def test_duplicate_artifact_path_is_invalid() -> None:
    first, second = valid_events()
    duplicated = event("event:2", EventState.COMPLETE, 2, products=(artifact(), artifact("out.txt", b"other")))
    result = audit_transformation_lineage((first, duplicated), expected_run_id="run:1", payloads={"out.txt": b"output"})
    assert result.reason == "DUPLICATE_ARTIFACT_PATH"
    assert_no_effect(result)


def test_output_bytes_missing_holds() -> None:
    result = audit_transformation_lineage(valid_events(), expected_run_id="run:1")
    assert result.reason == "OUTPUT_BYTES_NOT_SUPPLIED"
    assert_no_effect(result)


def test_output_path_mismatch_is_invalid() -> None:
    result = audit_transformation_lineage(valid_events(), expected_run_id="run:1", payloads={"wrong.txt": b"output"})
    assert result.reason == "OUTPUT_PATH_SET_MISMATCH"
    assert_no_effect(result)


def test_output_digest_mismatch_holds() -> None:
    result = audit_transformation_lineage(valid_events(), expected_run_id="run:1", payloads={"out.txt": b"tampered"})
    assert result.status is AuditStatus.HOLD
    assert result.reason == "OUTPUT_DIGEST_MISMATCH"
    assert_no_effect(result)


def test_failed_run_is_recorded_without_promotion() -> None:
    first, _ = valid_events()
    failed = event("event:2", EventState.FAIL, 2)
    result = audit_transformation_lineage((first, failed), expected_run_id="run:1")
    assert result.status is AuditStatus.VALID
    assert result.reason == "FAILED_RUN_RECORDED"
    assert_no_effect(result)


def test_self_parent_lineage_is_invalid() -> None:
    first, second = valid_events()
    parented = event("event:2", EventState.COMPLETE, 2, products=second.products, parent="run:1")
    result = audit_transformation_lineage((first, parented), expected_run_id="run:1", payloads={"out.txt": b"output"})
    assert result.reason == "SELF_PARENT_LINEAGE"
    assert_no_effect(result)


def test_artifact_path_and_digest_contract() -> None:
    with pytest.raises(ValueError):
        ArtifactRef("../secret", digest_bytes(b"x"), "source")
    with pytest.raises(ValueError):
        ArtifactRef("x", "not-a-digest", "source")


def test_redaction_helper_is_deterministic() -> None:
    result = redact_environment({"authorization": "bearer", "workdir": "/tmp"})
    assert result == {"authorization": "[REDACTED]", "workdir": "/tmp"}
