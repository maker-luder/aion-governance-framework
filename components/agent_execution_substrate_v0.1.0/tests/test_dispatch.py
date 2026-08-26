from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from aion_astra_agent_substrate import (
    RECEIPT_FILENAME,
    Decision,
    SubstratePolicyHold,
    dispatch_native_execution,
)


def runtime_context(agent_id: str = "AION") -> dict[str, str]:
    return {
        "agent_id": agent_id,
        "runtime_instance_id": f"{agent_id}-I-001",
        "memory_stream_id": f"{agent_id}-MEMORY-001",
        "event_lineage_id": f"{agent_id}-EVENT-001",
        "canonical_state_reference": f"{agent_id}-CANONICAL",
        "genesis_root_id": "ROOT-001",
    }


def test_dispatch_policy_hold_prevents_execution() -> None:
    called = False

    def execute() -> object:
        nonlocal called
        called = True
        return object()

    with pytest.raises(SubstratePolicyHold) as caught:
        dispatch_native_execution(
            context=runtime_context(),
            task_id="TASK-001",
            owner_approved=False,
            authority_reference=None,
            network_access=False,
            execute=execute,
        )

    assert called is False
    assert caught.value.decision.decision is Decision.HOLD
    assert "explicit Owner approval" in " ".join(caught.value.decision.reasons)


def test_network_request_holds_before_native_execution() -> None:
    called = False

    def execute() -> object:
        nonlocal called
        called = True
        return object()

    with pytest.raises(SubstratePolicyHold) as caught:
        dispatch_native_execution(
            context=runtime_context("ASTRA"),
            task_id="TASK-002",
            owner_approved=True,
            authority_reference="OWNER-RUNTIME-APPROVAL",
            network_access=True,
            execute=execute,
        )

    assert called is False
    assert "network access" in " ".join(caught.value.decision.reasons)


def test_dispatch_persists_content_minimized_native_receipt(tmp_path) -> None:
    output_root = tmp_path / "output"
    output_root.mkdir()
    audit_path = output_root / "runtime_audit.jsonl"
    events = [
        {
            "action": "runtime.started",
            "details": {
                "profile": "INVENTORY_SUMMARIZE",
                "canonical_effect": "NONE",
            },
        },
        {
            "action": "tool.completed",
            "details": {
                "tool": "write_summary",
                "status": "PASS",
                "payload": "sensitive-value-not-copied",
            },
        },
    ]
    audit_path.write_text(
        "".join(json.dumps(event, sort_keys=True) + "\n" for event in events),
        encoding="utf-8",
    )

    def execute() -> SimpleNamespace:
        return SimpleNamespace(
            task_id="TASK-003",
            status=SimpleNamespace(value="PASS_PENDING_OWNER_REVIEW"),
            steps_executed=2,
            output_root=str(output_root),
            output_sha256="a" * 64,
            audit_path=str(audit_path),
            audit_chain_valid=True,
            baseline_unchanged=True,
            canonical_effect="NONE",
            deployment=False,
        )

    outcome = dispatch_native_execution(
        context=runtime_context(),
        task_id="TASK-003",
        owner_approved=True,
        authority_reference="OWNER-RUNTIME-APPROVAL",
        network_access=False,
        execute=execute,
    )

    assert outcome.policy_decision.decision is Decision.ALLOW
    assert outcome.binding.agent_id.value == "AION"
    assert outcome.receipt_path.name == RECEIPT_FILENAME
    receipt_text = outcome.receipt_path.read_text(encoding="utf-8")
    receipt = json.loads(receipt_text)
    assert receipt["record_type"] == "AION_ASTRA_SUBSTRATE_EXECUTION_RECEIPT"
    assert receipt["binding"]["session_id"] == "AION-I-001:TASK-003"
    assert receipt["policy_decision"]["decision"] == "ALLOW"
    assert receipt["boundaries"]["canonical_effect"] == "NONE"
    assert receipt["boundaries"]["deployment"] is False
    assert receipt["boundaries"]["live_dsh_execution"] is False
    assert len(receipt["normalized_events"]) == 2
    assert "OWNER-RUNTIME-APPROVAL" not in receipt_text
    assert "sensitive-value-not-copied" not in receipt_text
