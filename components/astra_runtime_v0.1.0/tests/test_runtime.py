from __future__ import annotations

import pytest

from aion_astra_runtime.models import IndividualRuntimeContext, TaskSpec
from astra_runtime import AstraRuntime, RuntimeIdentityMismatch


def astra_context(**changes: str) -> IndividualRuntimeContext:
    values = {
        "agent_id": "ASTRA",
        "runtime_instance_id": "ASTRA-I-001",
        "memory_stream_id": "ASTRA_RESEARCH_EPISODIC_MEMORY",
        "event_lineage_id": "ASTRA-EVENT-LINEAGE-001",
        "canonical_state_reference": "ASTRA_CANONICAL",
        "genesis_root_id": "ROOT-001",
    }
    values.update(changes)
    return IndividualRuntimeContext(**values)


def test_runtime_rejects_non_astra_context(tmp_path):
    with pytest.raises(RuntimeIdentityMismatch):
        AstraRuntime(
            memory_db=tmp_path / "memory.sqlite3",
            context=astra_context(agent_id="AION"),
        )


def test_memory_is_bound_to_astra_stream(tmp_path):
    runtime = AstraRuntime(memory_db=tmp_path / "memory.sqlite3", context=astra_context())
    stored = runtime.remember(
        memory_id="m1",
        user_id="u1",
        content="Astra research decision",
        provenance_source="owner-input",
        provenance_verified=True,
        writeback_approved=True,
        entities={"Astra"},
        topics={"runtime"},
        access_scope={"project"},
    )
    assert stored.agent_id == "ASTRA"
    assert stored.namespace == "ASTRA_RESEARCH_EPISODIC_MEMORY"

    recalled = runtime.recall(
        user_id="u1",
        requester_scopes={"project"},
        entity_cues={"Astra"},
        topic_cues={"runtime"},
    )
    assert [item.memory_id for item in recalled] == ["m1"]


def test_task_context_must_match_bound_astra_instance(tmp_path):
    runtime = AstraRuntime(memory_db=tmp_path / "memory.sqlite3", context=astra_context())
    task = TaskSpec.from_dict(
        {
            "task_id": "ASTRA-MISMATCH-001",
            "objective": "Inventory and summarize",
            "profile": "INVENTORY_SUMMARIZE",
            "input_paths": ["input.txt"],
            "output_path": "out.txt",
            "owner_approved": True,
            "approved_by": "OWNER",
            "runtime_context": astra_context(runtime_instance_id="ASTRA-I-OTHER").to_dict(),
        }
    )
    with pytest.raises(RuntimeIdentityMismatch):
        runtime.run_task(task, baseline_root=tmp_path, sessions_root=tmp_path)


def test_recall_applies_bound_namespace_before_limit(tmp_path):
    runtime = AstraRuntime(memory_db=tmp_path / "memory.sqlite3", context=astra_context())
    common = dict(
        user_id="u1",
        content="candidate",
        provenance_source="owner-input",
        provenance_verified=True,
        entities={"Astra"},
        topics={"runtime"},
        access_scope={"project"},
        writeback_approved=True,
    )
    runtime.memory.write(
        memory_id="a-foreign",
        namespace="AION_PRIVATE_EPISODIC_MEMORY",
        agent_id="ASTRA",
        **common,
    )
    runtime.remember(memory_id="z-bound", **common)

    recalled = runtime.recall(
        user_id="u1",
        requester_scopes={"project"},
        entity_cues={"Astra"},
        topic_cues={"runtime"},
        limit=1,
    )

    assert [item.memory_id for item in recalled] == ["z-bound"]
