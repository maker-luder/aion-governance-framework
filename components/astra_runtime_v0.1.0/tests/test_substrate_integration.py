from __future__ import annotations

import json

from aion_astra_runtime.models import (
    IndividualRuntimeContext,
    RunResult,
    RunStatus,
    TaskSpec,
)
from astra_runtime import AstraRuntime


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
            output_sha256="c" * 64,
            audit_path=str(audit_path),
            audit_chain_valid=True,
            baseline_unchanged=True,
        )


def context() -> IndividualRuntimeContext:
    return IndividualRuntimeContext(
        agent_id="ASTRA",
        runtime_instance_id="ASTRA-I-SUBSTRATE",
        memory_stream_id="ASTRA-MEMORY-SUBSTRATE",
        event_lineage_id="ASTRA-EVENT-SUBSTRATE",
        canonical_state_reference="ASTRA-CANONICAL",
        genesis_root_id="ROOT-001",
    )


def task() -> TaskSpec:
    return TaskSpec.from_dict(
        {
            "task_id": "ASTRA-SUBSTRATE-001",
            "objective": "Inventory and summarize",
            "profile": "INVENTORY_SUMMARIZE",
            "input_paths": ["input.txt"],
            "output_path": "out.txt",
            "owner_approved": True,
            "approved_by": "OWNER-RUNTIME-APPROVAL",
            "runtime_context": context().to_dict(),
        }
    )


def test_astra_run_task_flows_through_native_substrate(tmp_path) -> None:
    execution = FakeExecution()
    runtime = AstraRuntime(
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
    receipt_path = tmp_path / "ASTRA-SUBSTRATE-001-output" / "substrate_execution_receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert receipt["binding"]["agent_id"] == "ASTRA"
    assert receipt["policy_decision"]["decision"] == "ALLOW"
    assert runtime.status().shared_execution_substrate == "ENABLED_NATIVE_BOUNDED"
    assert runtime.status().substrate_policy_gate == "ENFORCED"
