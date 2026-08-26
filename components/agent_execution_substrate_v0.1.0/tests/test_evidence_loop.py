from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from aion_astra_agent_substrate import (
    EVENT_LOG_FILENAME,
    EXECUTION_EVIDENCE_FILENAME,
    AdapterRegistryError,
    SubstrateError,
    dispatch_native_execution,
    dsh_profile,
    verify_execution_event_log,
    verify_execution_evidence,
)


def runtime_context(agent_id: str) -> dict[str, str]:
    return {
        "agent_id": agent_id,
        "runtime_instance_id": f"{agent_id}-I-LOOP-001",
        "memory_stream_id": f"{agent_id}-MEMORY-LOOP-001",
        "event_lineage_id": f"{agent_id}-EVENT-LOOP-001",
        "canonical_state_reference": f"{agent_id}-CANONICAL",
        "genesis_root_id": "ROOT-LOOP-001",
    }


@pytest.mark.parametrize("agent_id", ["AION", "ASTRA"])
def test_shared_dispatch_closes_durable_execution_evidence_loop(tmp_path, agent_id: str) -> None:
    output_root = tmp_path / agent_id
    output_root.mkdir()
    audit_path = output_root / "runtime_audit.jsonl"
    audit_events = [
        {
            "action": "runtime.started",
            "details": {"canonical_effect": "NONE", "secret": "not-copied"},
        },
        {
            "action": "task.completed",
            "details": {"status": "PASS_PENDING_OWNER_REVIEW"},
        },
    ]
    audit_path.write_text(
        "".join(json.dumps(event, sort_keys=True) + "\n" for event in audit_events),
        encoding="utf-8",
    )

    outcome = dispatch_native_execution(
        context=runtime_context(agent_id),
        task_id="TASK-LOOP-001",
        owner_approved=True,
        authority_reference="OWNER-RUNTIME-APPROVAL-SECRET",
        network_access=False,
        execute=lambda: SimpleNamespace(
            task_id="TASK-LOOP-001",
            status=SimpleNamespace(value="PASS_PENDING_OWNER_REVIEW"),
            steps_executed=1,
            output_root=str(output_root),
            output_sha256="b" * 64,
            audit_path=str(audit_path),
            audit_chain_valid=True,
            baseline_unchanged=True,
            canonical_effect="NONE",
            deployment=False,
        ),
    )

    assert outcome.binding.agent_id.value == agent_id
    assert outcome.event_log_path.name == EVENT_LOG_FILENAME
    assert outcome.evidence_path.name == EXECUTION_EVIDENCE_FILENAME
    assert verify_execution_event_log(outcome.event_log_path).event_count == 5
    assert verify_execution_evidence(outcome.evidence_path) is True

    combined = (
        outcome.receipt_path.read_text(encoding="utf-8")
        + outcome.event_log_path.read_text(encoding="utf-8")
        + outcome.evidence_path.read_text(encoding="utf-8")
    )
    assert "OWNER-RUNTIME-APPROVAL-SECRET" not in combined
    assert "not-copied" not in combined

    evidence = json.loads(outcome.evidence_path.read_text(encoding="utf-8"))
    assert evidence["boundaries"]["canonical_effect"] == "NONE"
    assert evidence["boundaries"]["research_record"] is False
    assert evidence["boundaries"]["live_dsh_execution"] is False


def test_disabled_dsh_registry_entry_cannot_execute(tmp_path) -> None:
    called = False

    def execute() -> object:
        nonlocal called
        called = True
        return object()

    with pytest.raises(AdapterRegistryError):
        dispatch_native_execution(
            context=runtime_context("AION"),
            task_id="TASK-DSH-BLOCKED",
            owner_approved=True,
            authority_reference="OWNER-RUNTIME-APPROVAL",
            network_access=False,
            adapter_id=dsh_profile().adapter_id,
            execute=execute,
        )

    assert called is False


def test_tampered_durable_event_log_breaks_evidence_verification(tmp_path) -> None:
    output_root = tmp_path / "tamper"
    output_root.mkdir()
    audit_path = output_root / "runtime_audit.jsonl"
    audit_path.write_text(
        json.dumps(
            {
                "action": "runtime.started",
                "details": {"canonical_effect": "NONE"},
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    outcome = dispatch_native_execution(
        context=runtime_context("ASTRA"),
        task_id="TASK-TAMPER-001",
        owner_approved=True,
        authority_reference="OWNER-RUNTIME-APPROVAL",
        network_access=False,
        execute=lambda: SimpleNamespace(
            task_id="TASK-TAMPER-001",
            status=SimpleNamespace(value="PASS_PENDING_OWNER_REVIEW"),
            steps_executed=1,
            output_root=str(output_root),
            output_sha256="c" * 64,
            audit_path=str(audit_path),
            audit_chain_valid=True,
            baseline_unchanged=True,
            canonical_effect="NONE",
            deployment=False,
        ),
    )

    outcome.event_log_path.write_text(
        outcome.event_log_path.read_text(encoding="utf-8") + "{}\n",
        encoding="utf-8",
    )
    with pytest.raises(SubstrateError):
        verify_execution_evidence(outcome.evidence_path)
