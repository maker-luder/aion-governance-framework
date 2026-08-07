from __future__ import annotations

from astra_language_core.enums import ModelStatus, QAStatus
from astra_language_core.models import ModelNode


def base_node() -> ModelNode:
    return ModelNode(
        model_id="G1-BASE",
        display_name="Base",
        family_generation="G1",
        parent_model_id=None,
        modification_type="NONE",
        read_only=True,
        status=ModelStatus.BASELINE_PENDING,
        qa_status=QAStatus.QA_HOLD,
    )


def derived(model_id: str, parent: str = "G1-BASE", notes: str = "test") -> ModelNode:
    return ModelNode(
        model_id=model_id,
        display_name=model_id,
        family_generation="G1",
        parent_model_id=parent,
        modification_type="PLANNED",
        notes=notes,
    )


def lineage_nodes() -> list[ModelNode]:
    return [
        base_node(),
        derived("G1-TW-LORA"),
        derived("G1-ABLATION-LOW"),
        derived("G1-RANDOM-CONTROL"),
        derived("G1-ABLATION-TW-LORA", "G1-ABLATION-LOW", "A_B_C_D_REQUIRED"),
    ]
