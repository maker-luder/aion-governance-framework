from __future__ import annotations

from pathlib import Path

import pytest

from astra_engineering_workbench.enums import AdoptionStatus, KernelDecision
from astra_engineering_workbench.episodic_adapter import EpisodicCoreAdapter
from astra_engineering_workbench.errors import (
    EpisodicAdapterError,
    KernelDeniedError,
    ValidationError,
)
from astra_engineering_workbench.governance_adapter import GovernanceKernelAdapter
from astra_engineering_workbench.packaging import build_package, verify_package
from astra_engineering_workbench.reasoning_provider import (
    DeterministicTestProvider,
    LocalhostModelProvider,
    OwnerSuppliedResponseProvider,
)
from astra_engineering_workbench.review_packet import (
    create_review_packet,
    record_external_response,
)


class Writer:
    def __init__(self, fail: bool = False) -> None:
        self.fail = fail
        self.calls: list[dict[str, str]] = []

    def append(self, **kwargs: str) -> str:
        if self.fail:
            raise RuntimeError("db down")
        self.calls.append(kwargs)
        return "EVENT-1"


def pipeline(payload: dict[str, object], db: str) -> dict[str, str]:
    return {"decision": str(payload["target"]), "reason": db}


def test_KERNEL_DENY_CANNOT_BE_OVERRIDDEN_001() -> None:
    adapter = GovernanceKernelAdapter(pipeline, "kernel.db")
    evaluation = adapter.evaluate(task_id="T", operation="write", target="STOP", approved=True)
    assert evaluation.decision is KernelDecision.DENY
    with pytest.raises(KernelDeniedError):
        adapter.enforce(evaluation)


def test_KERNEL_REQUIRES_OWNER_APPROVAL_001() -> None:
    adapter = GovernanceKernelAdapter(pipeline, "kernel.db")
    result = adapter.evaluate(
        task_id="T", operation="write", target="REQUIRE_HUMAN", approved=False
    )
    assert result.decision is KernelDecision.REQUIRE_OWNER_APPROVAL


def test_kernel_allow() -> None:
    adapter = GovernanceKernelAdapter(pipeline, "kernel.db")
    result = adapter.evaluate(task_id="T", operation="read", target="ALLOW", approved=True)
    adapter.enforce(result)


def test_ASTRA_WRITES_ONLY_ASTRA_STREAM_001() -> None:
    writer = Writer()
    adapter = EpisodicCoreAdapter(writer)
    assert adapter.record(
        task_id="T", event_kind="change", source_type="OWNER_STATEMENT", payload={"x": 1}
    ) == "EVENT-1"
    assert writer.calls[0]["agent_id"] == "AGENT_ASTRA"
    assert writer.calls[0]["memory_stream_id"].startswith("ASTRA_")


def test_AION_STREAM_WRITE_REJECTED_001() -> None:
    with pytest.raises(EpisodicAdapterError):
        EpisodicCoreAdapter.validate_stream("AION_MEMORY", "ASTRA_AUDIT")


def test_provenance_failure_stops() -> None:
    with pytest.raises(EpisodicAdapterError):
        EpisodicCoreAdapter(Writer(True)).record(
            task_id="T", event_kind="x", source_type="TEST", payload={}
        )


def test_BLOCKED_TASK_GENERATES_REVIEW_PACKET_001_and_minimum(tmp_path: Path) -> None:
    evidence = tmp_path / "evidence.txt"
    evidence.write_text("safe", encoding="utf-8")
    packet = create_review_packet(
        packet_id="PKT-1",
        task_id="T",
        blocking_issue="dependency",
        current_state="BLOCKED",
        expected_result="pass",
        actual_result="missing",
        attempts_made=("local check",),
        relevant_files=(evidence,),
        minimal_code_excerpt="token=secret",
        logs="OWNER_A@example.test at USER_HOME_TEST/x",
        environment={"python": "3.12"},
        questions_for_reviewer=("What is the intended interface?",),
    )
    assert packet.blocking_issue and packet.manifest == ("evidence.txt",)
    assert "[REDACTED" in packet.minimal_code_excerpt
    assert packet.owner_submission_status.startswith("NOT_SUBMITTED")


def test_REVIEW_PACKET_NO_AUTO_UPLOAD_001_and_NO_AUTO_API_CALL_001(tmp_path: Path) -> None:
    packet = create_review_packet(
        packet_id="PKT", task_id="T", blocking_issue="x", current_state="BLOCKED",
        expected_result="y", actual_result="z", attempts_made=(), relevant_files=(),
        minimal_code_excerpt="", logs="", environment={}, questions_for_reviewer=("q",),
    )
    assert packet.owner_submission_status == "NOT_SUBMITTED_MANUAL_OWNER_ACTION_REQUIRED"


def test_EXTERNAL_TEACHER_INPUT_ATTRIBUTION_001_and_no_auto_apply() -> None:
    item = record_external_response(
        task_id="T", source_actor_id="EXTERNAL_REVIEWER",
        response="advice", received_at="2026-07-30",
    )
    assert item.source_actor_id == "EXTERNAL_REVIEWER"
    assert item.adoption_status is AdoptionStatus.PENDING_OWNER_REVIEW


def test_CLOUD_PROVIDER_DISABLED_001() -> None:
    with pytest.raises(ValidationError):
        LocalhostModelProvider("https://api.example.test", False)
    with pytest.raises(ValidationError):
        LocalhostModelProvider().reason("x")


def test_reasoning_is_advisory_only() -> None:
    assert DeterministicTestProvider("candidate").reason("x") == "candidate"
    assert OwnerSuppliedResponseProvider("owner text").reason("x") == "owner text"


def test_PACKAGE_MANIFEST_COMPLETE_001(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "a.txt").write_text("a", encoding="utf-8")
    package = build_package(
        task_id="T", package_id="P", source_root=source, destination=tmp_path / "p.zip"
    )
    result = verify_package(Path(package.path))
    assert result["crc_pass"] and result["hash_pass"]
    assert package.canonical_effect == "NONE_PENDING_OWNER_REVIEW"
    assert not package.deployed


def test_AUTOMATIC_DEPLOYMENT_BLOCKED_001(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "a").write_text("a", encoding="utf-8")
    package = build_package(
        task_id="T", package_id="P", source_root=source, destination=tmp_path / "p.zip"
    )
    assert not package.deployed


def test_historical_package_not_overwritten(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "a").write_text("a", encoding="utf-8")
    destination = tmp_path / "p.zip"
    destination.write_bytes(b"history")
    with pytest.raises(Exception):
        build_package(task_id="T", package_id="P", source_root=source, destination=destination)


def test_unknown_kernel_response_fails_closed() -> None:
    adapter = GovernanceKernelAdapter(pipeline, "kernel.db")
    result = adapter.evaluate(task_id="T", operation="x", target="UNKNOWN", approved=False)
    assert result.decision is KernelDecision.REQUIRE_ADDITIONAL_EVIDENCE
    with pytest.raises(KernelDeniedError):
        adapter.enforce(result)


def test_external_input_hash_is_deterministic() -> None:
    first = record_external_response(
        task_id="T", source_actor_id="EXTERNAL_REVIEWER",
        response="same", received_at="2026-07-30",
    )
    second = record_external_response(
        task_id="T", source_actor_id="EXTERNAL_REVIEWER",
        response="same", received_at="2026-07-30",
    )
    assert first.content_hash == second.content_hash


def test_cli_status_and_inspect(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    import sys
    from astra_engineering_workbench.cli import main

    (tmp_path / "a").write_text("a", encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["astra-workbench", "status", str(tmp_path)])
    assert main() == 0
    assert '"deployment": false' in capsys.readouterr().out
    monkeypatch.setattr(sys, "argv", ["astra-workbench", "inspect", str(tmp_path)])
    assert main() == 0


def test_owner_response_empty_rejected() -> None:
    with pytest.raises(ValidationError):
        OwnerSuppliedResponseProvider("").reason("x")
