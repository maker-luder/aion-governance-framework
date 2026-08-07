from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import pytest

from aion_astra_governance.cli import main
from aion_astra_governance.enums import ApprovalStatus, CanonicalEffect, ForkStatus, QAStatus, VerificationResult
from aion_astra_governance.errors import ConflictError, ValidationError
from aion_astra_governance.forks import ResearchForkService
from aion_astra_governance.governance import WritebackRequest, evaluate_writeback, qa_gate_status
from aion_astra_governance.hashing import hash_file, hash_object, valid_sha256
from aion_astra_governance.lineage import StateLineageLedger
from aion_astra_governance.models import (
    AnalysisChannel,
    CapabilityArtifactRecord,
    LineageEvent,
    PerspectiveEventRecord,
    ProjectIdentityRecord,
    ResearchForkRecord,
    RuntimeManifest,
    SystemStateRecord,
)
from aion_astra_governance.perspectives import compare_channels
from aion_astra_governance.registry import CapabilityRegistry, ProjectIdentityRegistry
from aion_astra_governance.reports import write_json_report

H = "a" * 64


def state(state_id: str, sequence: int, parent_id: str | None, parent_hash: str) -> SystemStateRecord:
    return SystemStateRecord(
        state_id=state_id,
        project_id="AION-ASTRA-PROJECT-001",
        previous_state_id=parent_id,
        sequence_number=sequence,
        state_type="CANDIDATE",
        previous_state_hash=parent_hash,
        canonical_manifest_hash=H,
        governance_policy_hash=H,
        capability_manifest_hash=H,
        model_manifest_hash=H,
        runtime_manifest_hash=H,
    )


def channel(channel_id: str, interpretation: str) -> AnalysisChannel:
    return AnalysisChannel(channel_id, ("finding",), interpretation, "HIGH", ("E1",), (), "TEST", "METHOD")


def test_identity_is_decoupled_and_registered(tmp_path: Path) -> None:
    registry = ProjectIdentityRegistry(tmp_path)
    record = ProjectIdentityRecord("AION-ASTRA-PROJECT-001")
    registry.register(record)
    loaded = registry.load(record.project_id)
    assert loaded["canonical_name"] == "AION／Astra"
    assert loaded["subjectivity_status"] == "NOT_ESTABLISHED"


def test_upstream_model_cannot_be_canonical_name() -> None:
    with pytest.raises(ValidationError):
        ProjectIdentityRecord("P", canonical_name="Qwen")


def test_genesis_and_append_state(tmp_path: Path) -> None:
    ledger = StateLineageLedger(tmp_path)
    genesis = state("S0", 0, None, "GENESIS").sealed()
    ledger.append(genesis)
    ledger.append(state("S1", 1, "S0", genesis.state_hash))
    assert len(ledger.states()) == 2


def test_previous_hash_tamper_is_rejected(tmp_path: Path) -> None:
    ledger = StateLineageLedger(tmp_path)
    genesis = state("S0", 0, None, "GENESIS").sealed()
    ledger.append(genesis)
    with pytest.raises(ConflictError):
        ledger.append(state("S1", 1, "S0", "b" * 64))


def test_manifest_tamper_returns_invalid_hash(tmp_path: Path) -> None:
    ledger = StateLineageLedger(tmp_path)
    path = ledger.append(state("S0", 0, None, "GENESIS"))
    raw = json.loads(path.read_text(encoding="utf-8"))
    raw["runtime_manifest_hash"] = "b" * 64
    path.write_text(json.dumps(raw), encoding="utf-8")
    assert ledger.verify() is VerificationResult.INVALID_HASH


def test_sequence_jump_rejected(tmp_path: Path) -> None:
    ledger = StateLineageLedger(tmp_path)
    genesis = state("S0", 0, None, "GENESIS").sealed()
    ledger.append(genesis)
    with pytest.raises(ConflictError):
        ledger.append(state("S2", 2, "S0", genesis.state_hash))


def test_duplicate_state_id_rejected(tmp_path: Path) -> None:
    ledger = StateLineageLedger(tmp_path)
    ledger.append(state("S0", 0, None, "GENESIS"))
    with pytest.raises(ConflictError):
        ledger.append(state("S0", 0, None, "GENESIS"))


def test_unapproved_ledger_stays_qa_hold(tmp_path: Path) -> None:
    ledger = StateLineageLedger(tmp_path)
    ledger.append(state("S0", 0, None, "GENESIS"))
    assert ledger.verify() is VerificationResult.QA_HOLD


def test_unknown_artifact_blocks_approved_state(tmp_path: Path) -> None:
    ledger = StateLineageLedger(tmp_path)
    s0 = replace(
        state("S0", 0, None, "GENESIS"),
        artifact_ids=("UNKNOWN-1",),
        qa_status=QAStatus.APPROVED,
        approval_status=ApprovalStatus.APPROVED,
    )
    ledger.append(s0)
    assert ledger.verify(set()) is VerificationResult.UNKNOWN_ARTIFACT


def test_capability_registry_and_language_core_adapter(tmp_path: Path) -> None:
    registry = CapabilityRegistry(tmp_path)
    record = registry.from_language_core_node({"model_id": "G1-BASE", "display_name": "G1", "read_only": True})
    registry.register(record)
    assert record.capability_type == "LANGUAGE_MODEL_BASELINE"
    assert registry.verify("G1-BASE")


def test_duplicate_capability_rejected(tmp_path: Path) -> None:
    registry = CapabilityRegistry(tmp_path)
    record = CapabilityArtifactRecord("A1", "LANGUAGE_MODEL", "Model", "1")
    registry.register(record)
    with pytest.raises(ConflictError):
        registry.register(record)


def test_path_traversal_rejected() -> None:
    with pytest.raises(ValidationError):
        CapabilityArtifactRecord("A1", "MODEL", "x", "1", local_path="../secret")


def test_runtime_rejects_non_loopback_endpoint() -> None:
    with pytest.raises(ValidationError):
        RuntimeManifest("R1", "OLLAMA", allowed_endpoints=("https://example.com",))


def test_runtime_accepts_localhost_as_runtime_not_identity() -> None:
    runtime = RuntimeManifest("R1", "OLLAMA", allowed_endpoints=("http://127.0.0.1:11434",))
    assert runtime.runtime_type == "OLLAMA"


def test_fork_denies_all_inheritance_and_preserves_parent(tmp_path: Path) -> None:
    parent = state("S0", 0, None, "GENESIS").sealed()
    service = ResearchForkService(tmp_path)
    fork = ResearchForkRecord(
        "RESEARCH-FORK-TW-LORA-002", "S0", parent.state_hash, "LORA_EXPERIMENT", "test", "h", ("language",)
    )
    service.create(fork, {"state_id": "S0", "state_hash": parent.state_hash}, set())
    assert service.inspect(fork.fork_id)["identity_inheritance"] == "DENIED"
    assert parent.state_hash == state("S0", 0, None, "GENESIS").sealed().state_hash


def test_duplicate_fork_id_rejected(tmp_path: Path) -> None:
    parent = state("S0", 0, None, "GENESIS").sealed()
    service = ResearchForkService(tmp_path)
    fork = ResearchForkRecord(
        "RESEARCH-FORK-TEST-001", "S0", parent.state_hash, "PROMPT_POLICY_EXPERIMENT", "test", "h", ("policy",)
    )
    parent_data = {"state_id": "S0", "state_hash": parent.state_hash}
    service.create(fork, parent_data, set())
    with pytest.raises(ConflictError):
        service.create(fork, parent_data, set())


def test_fork_cannot_inherit_privileges_or_identity() -> None:
    with pytest.raises(ValidationError):
        ResearchForkRecord(
            "RESEARCH-FORK-X-001", "S0", H, "MODEL_EDIT", "p", "h", ("x",), identity_inheritance="ALLOWED"
        )


def test_merge_candidate_is_not_merged() -> None:
    fork = ResearchForkRecord(
        "RESEARCH-FORK-X-001",
        "S0",
        H,
        "MODEL_EDIT",
        "p",
        "h",
        ("x",),
        status=ForkStatus.MERGE_CANDIDATE,
        disposition="MERGE_CANDIDATE",
    )
    assert fork.canonical_writeback == "DENIED"


def test_writeback_denied_without_human_approval() -> None:
    request = WritebackRequest(True, True, True, QAStatus.APPROVED, None, False, False, CanonicalEffect.APPROVED)
    decision = evaluate_writeback(request)
    assert decision.canonical_writeback == "DENIED"
    assert decision.qa_status is QAStatus.QA_HOLD


def test_writeback_allowed_only_when_every_gate_passes() -> None:
    request = WritebackRequest(
        True, True, True, QAStatus.APPROVED, "OWNER-APPROVAL-001", False, False, CanonicalEffect.APPROVED
    )
    assert evaluate_writeback(request).canonical_writeback == "ALLOWED_FOR_HUMAN_CONTROLLED_WRITEBACK"


def test_missing_threshold_or_gate_stays_hold() -> None:
    status, failed = qa_gate_status({"identity": True, "threshold": None})
    assert status is QAStatus.QA_HOLD
    assert failed == ("threshold",)


def test_perspective_channels_and_disagreement_preserved() -> None:
    record = PerspectiveEventRecord(
        "P1", ("E1",), H, (channel("A", "x"), channel("B", "y")), (), ("different interpretation",), ("open",)
    )
    result = compare_channels(record)
    assert result["channel_count"] == 2
    assert result["merge_status"] == "UNRESOLVED"
    assert result["original_channels_preserved"] is True


def test_unresolved_perspective_cannot_be_marked_resolved() -> None:
    with pytest.raises(ValidationError):
        PerspectiveEventRecord(
            "P1", ("E1",), H, (channel("A", "x"), channel("B", "y")), (), ("d",), (), merge_status="RESOLVED"
        )


def test_subjectivity_claim_remains_not_established() -> None:
    assert ProjectIdentityRecord("P").subjectivity_status.value == "NOT_ESTABLISHED"


def test_canonical_event_requires_human_approval() -> None:
    with pytest.raises(ValidationError):
        LineageEvent("E1", "CANONICAL_UPDATED", "GENESIS", "P", "S", None, H, "AGENT")


def test_hash_serialization_is_reproducible() -> None:
    assert hash_object({"b": 2, "a": 1}) == hash_object({"a": 1, "b": 2})


def test_report_redacts_workspace_absolute_path(tmp_path: Path) -> None:
    output = tmp_path / "out" / "report.json"
    write_json_report(output, {"path": str(tmp_path / "private")}, workspace=tmp_path)
    text = output.read_text(encoding="utf-8")
    assert "<WORKSPACE>" in text
    assert str(tmp_path.resolve()) not in text


def test_cli_identity_and_capability(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = tmp_path / "artifacts"
    ProjectIdentityRegistry(root / "identity").register(ProjectIdentityRecord("AION-ASTRA-PROJECT-001"))
    CapabilityRegistry(root / "capabilities").register(
        CapabilityArtifactRecord("G1-BASE", "LANGUAGE_MODEL_BASELINE", "G1", "1")
    )
    assert main(["--workspace", str(root), "identity", "validate"]) == 0
    assert main(["--workspace", str(root), "capability", "verify", "--artifact-id", "G1-BASE"]) == 0
    assert '"valid": true' in capsys.readouterr().out


def test_cli_report_is_new_file_only(tmp_path: Path) -> None:
    output = tmp_path / "identity.md"
    assert main(["--workspace", str(tmp_path), "report", "identity", "--output", str(output)]) == 0
    with pytest.raises(ConflictError):
        main(["--workspace", str(tmp_path), "report", "identity", "--output", str(output)])


def test_file_hash_and_digest_validation(tmp_path: Path) -> None:
    path = tmp_path / "sample.bin"
    path.write_bytes(b"abc")
    assert hash_file(path) == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    assert valid_sha256(hash_file(path))
    assert not valid_sha256("invalid")


def test_registry_empty_ids_and_unknown_export(tmp_path: Path) -> None:
    registry = CapabilityRegistry(tmp_path)
    assert registry.ids() == set()
    with pytest.raises(ConflictError):
        registry.export("missing")


def test_fork_rejects_parent_and_unknown_artifact(tmp_path: Path) -> None:
    service = ResearchForkService(tmp_path)
    fork = ResearchForkRecord("RESEARCH-FORK-X-001", "S0", H, "MODEL_EDIT", "p", "h", ("x",), artifact_ids=("A",))
    with pytest.raises(ConflictError, match="parent"):
        service.create(fork, {"state_id": "OTHER", "state_hash": H}, {"A"})
    with pytest.raises(ConflictError, match="unknown artifact"):
        service.create(fork, {"state_id": "S0", "state_hash": H}, set())


def test_ledger_missing_and_broken_parent_results(tmp_path: Path) -> None:
    ledger = StateLineageLedger(tmp_path)
    assert ledger.verify() is VerificationResult.MISSING_PARENT
    path = ledger.append(state("S0", 0, None, "GENESIS"))
    raw = json.loads(path.read_text(encoding="utf-8"))
    raw["sequence_number"] = 1
    raw["previous_state_id"] = "MISSING"
    raw["previous_state_hash"] = H
    raw["state_hash"] = ""
    raw["state_hash"] = SystemStateRecord(**raw).expected_hash()
    path.write_text(json.dumps(raw), encoding="utf-8")
    assert ledger.verify() is VerificationResult.BROKEN_CHAIN


def test_cli_lineage_paths_and_capability_list(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = tmp_path / "artifacts"
    ledger = StateLineageLedger(root / "lineage")
    ledger.append(state("S0", 0, None, "GENESIS"))
    CapabilityRegistry(root / "capabilities").register(CapabilityArtifactRecord("A1", "FORMAT_VALIDATOR", "A", "1"))
    assert main(["--workspace", str(root), "lineage", "verify"]) == 0
    assert main(["--workspace", str(root), "lineage", "show", "--state-id", "S0"]) == 0
    assert main(["--workspace", str(root), "capability", "list"]) == 0
    output = capsys.readouterr().out
    assert "QA_HOLD" in output and "S0" in output and "A1" in output


def test_cli_missing_capability_and_state_return_two(tmp_path: Path) -> None:
    root = tmp_path / "artifacts"
    assert main(["--workspace", str(root), "capability", "verify", "--artifact-id", "missing"]) == 2
    assert main(["--workspace", str(root), "lineage", "show", "--state-id", "missing"]) == 2
