from __future__ import annotations

import json

import pytest

from aion_astra_agent_substrate import SubstratePolicyHold
from aion_astra_runtime.models import (
    IndividualRuntimeContext,
    RunResult,
    RunStatus,
    TaskSpec,
)
from aion_runtime import AIONRuntime


class FakeExecution:
    def __init__(self) -> None:
        self.called = False

    def run(self, task: TaskSpec, *, baseline_root, sessions_root, kill_switch=None) -> RunResult:
        self.called = True
        output_root = sessions_root / f"{task.task_id}-output"
        output_root.mkdir(parents=True, exist_ok=True)
        audit_path = output_root / "runtime_audit.jsonl"
        audit_path.write_text(
            "\n".join(
                (
                    json.dumps(
                        {
                            "action": "runtime.started",
                            "details": {
                                "profile": task.profile,
                                "canonical_effect": "NONE",
                            },
                        },
                        sort_keys=True,
                    ),
                    json.dumps(
                        {
                            "action": "tool.completed",
                            "details": {"tool": "complete", "status": "PASS"},
                        },
                        sort_keys=True,
                    ),
                )
            )
            + "\n",
            encoding="utf-8",
        )
        return RunResult(
            task_id=task.task_id,
            runtime_context=task.runtime_context,
            status=RunStatus.PASS_PENDING_OWNER_REVIEW,
            steps_executed=1,
            candidate_root=str(output_root / "candidate"),
            output_root=str(output_root),
            output_relative_path=task.output_path,
            output_sha256="b" * 64,
            audit_path=str(audit_path),
            audit_chain_valid=True,
            baseline_unchanged=True,
        )


def context() -> IndividualRuntimeContext:
    return IndividualRuntimeContext(
        agent_id="AION",
        runtime_instance_id="AION-I-SUBSTRATE",
        memory_stream_id="AION-MEMORY-SUBSTRATE",
        event_lineage_id="AION-EVENT-SUBSTRATE",
        canonical_state_reference="AION-CANONICAL",
        genesis_root_id="ROOT-001",
    )


def task(*, network_policy: str = "OFFLINE") -> TaskSpec:
    return TaskSpec.from_dict(
        {
            "task_id": "AION-SUBSTRATE-001",
            "objective": "Inventory and summarize",
            "profile": "INVENTORY_SUMMARIZE",
            "input_paths": ["input.txt"],
            "output_path": "out.txt",
            "owner_approved": True,
            "approved_by": "OWNER-RUNTIME-APPROVAL",
            "network_policy": network_policy,
            "runtime_context": context().to_dict(),
        }
    )


def test_aion_run_task_flows_through_native_substrate(tmp_path) -> None:
    execution = FakeExecution()
    runtime = AIONRuntime(
        memory_db=tmp_path / "memory.sqlite3",
        context=context(),
        execution=execution,
    )

    result = runtime.run_task(
        task(),
        baseline_root=tmp_path,
        sessions_root=tmp_path,
    )

    assert execution.called is True
    assert result.status is RunStatus.PASS_PENDING_OWNER_REVIEW
    receipt_path = tmp_path / "AION-SUBSTRATE-001-output" / "substrate_execution_receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert receipt["binding"]["agent_id"] == "AION"
    assert receipt["policy_decision"]["decision"] == "ALLOW"
    assert runtime.status().shared_execution_substrate == "ENABLED_NATIVE_BOUNDED"
    assert runtime.status().substrate_policy_gate == "ENFORCED"


def test_aion_substrate_gate_blocks_network_before_engine(tmp_path) -> None:
    execution = FakeExecution()
    runtime = AIONRuntime(
        memory_db=tmp_path / "memory.sqlite3",
        context=context(),
        execution=execution,
    )

    with pytest.raises(SubstratePolicyHold):
        runtime.run_task(
            task(network_policy="LOOPBACK_ONLY"),
            baseline_root=tmp_path,
            sessions_root=tmp_path,
        )

    assert execution.called is False
