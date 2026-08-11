import pytest

from aion_artifact_lineage import (
    ArtifactRef,
    RunState,
    TransformationJob,
    TransformationPlan,
    TransformationRunEvent,
    TransformationLedger,
    hash_bytes,
    sanitize_environment,
    verify_artifact_bytes,
)


def art(path: str, data: bytes = b"x") -> ArtifactRef:
    return ArtifactRef(path, hash_bytes(data), source_ref="source")


def job() -> TransformationJob:
    return TransformationJob("external-intake", "clean-room-convert", "git:abc")


def start(run_id: str = "r1", j: TransformationJob | None = None) -> TransformationRunEvent:
    return TransformationRunEvent(
        run_id,
        j or job(),
        RunState.START,
        "2026-08-11T00:00:00Z",
        materials=(art("input.txt"),),
        command=("convert",),
        environment={"TOKEN": "secret", "workdir": "/tmp"},
        source_ref="src",
        approval_ref="apr",
    )


def complete(run_id: str = "r1", j: TransformationJob | None = None, data: bytes = b"out") -> TransformationRunEvent:
    return TransformationRunEvent(
        run_id,
        j or job(),
        RunState.COMPLETE,
        "2026-08-11T00:01:00Z",
        products=(art("output.txt", data),),
        byproducts={"return-value": 0},
        source_ref="src",
        approval_ref="apr",
    )


def test_hash_is_deterministic() -> None:
    assert hash_bytes(b"abc") == hash_bytes(b"abc")


def test_artifact_verification() -> None:
    ref = art("a", b"abc")
    assert verify_artifact_bytes(ref, b"abc") is True
    assert verify_artifact_bytes(ref, b"abd") is False


def test_invalid_digest_rejected() -> None:
    with pytest.raises(ValueError):
        ArtifactRef("a", "bad")


def test_plan_separates_design_time_from_run() -> None:
    plan = TransformationPlan(job(), (art("input"),), ("output",), "method", "approval")
    assert plan.declared_outputs == ("output",)


def test_environment_redacts_secret_like_keys() -> None:
    env = sanitize_environment({"API_KEY": "x", "workdir": "/tmp"})
    assert env["API_KEY"] == "[REDACTED]"
    assert env["workdir"] == "/tmp"


def test_start_cannot_claim_products() -> None:
    with pytest.raises(ValueError):
        TransformationRunEvent("r", job(), RunState.START, "t", products=(art("x"),), source_ref="s", approval_ref="a")


def test_fail_cannot_claim_products() -> None:
    with pytest.raises(ValueError):
        TransformationRunEvent("r", job(), RunState.FAIL, "t", products=(art("x"),), source_ref="s", approval_ref="a")


def test_terminal_requires_start() -> None:
    ledger = TransformationLedger()
    with pytest.raises(ValueError):
        ledger.append(complete())


def test_job_cannot_change_within_run() -> None:
    ledger = TransformationLedger()
    ledger.append(start())
    with pytest.raises(ValueError):
        ledger.append(complete(j=TransformationJob("other", "job")))


def test_complete_product_hashes_verify() -> None:
    ledger = TransformationLedger()
    ledger.append(start())
    ledger.append(complete(data=b"artifact"))
    assert ledger.verify_products("r1", {"output.txt": b"artifact"}) is True
    assert ledger.verify_products("r1", {"output.txt": b"tampered"}) is False


def test_product_set_must_match() -> None:
    ledger = TransformationLedger()
    ledger.append(start())
    ledger.append(complete())
    assert ledger.verify_products("r1", {"other.txt": b"out"}) is False


def test_canonical_write_is_rejected() -> None:
    with pytest.raises(ValueError):
        TransformationRunEvent("r", job(), RunState.START, "t", source_ref="s", approval_ref="a", canonical_effect="WRITE")


def test_command_is_record_only() -> None:
    event = start()
    assert event.command == ("convert",)
    assert event.state is RunState.START


def test_lineage_preserves_event_order() -> None:
    ledger = TransformationLedger()
    ledger.append(start())
    ledger.append(complete())
    assert [event.state for event in ledger.lineage_for("r1")] == [RunState.START, RunState.COMPLETE]
