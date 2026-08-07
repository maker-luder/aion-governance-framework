from __future__ import annotations

from .errors import ValidationError
from .models import ModelNode

REQUIRED_IDS = {
    "G1-BASE",
    "G1-TW-LORA",
    "G1-ABLATION-LOW",
    "G1-RANDOM-CONTROL",
    "G1-ABLATION-TW-LORA",
}


def validate_lineage(nodes: list[ModelNode]) -> None:
    by_id = {node.model_id: node for node in nodes}
    if len(by_id) != len(nodes):
        raise ValidationError("duplicate model_id in lineage")
    missing = REQUIRED_IDS - set(by_id)
    if missing:
        raise ValidationError(f"required lineage nodes missing: {sorted(missing)}")
    base = by_id["G1-BASE"]
    if base.parent_model_id is not None or not base.read_only or base.modification_type != "NONE":
        raise ValidationError("G1-BASE must be an immutable, unmodified root")
    for node in nodes:
        if node.model_id == "G1-BASE":
            continue
        if node.parent_model_id not in by_id:
            raise ValidationError(f"unknown parent for {node.model_id}")
        if node.status.value != "EXPERIMENTAL" or node.qa_status.value != "QA_HOLD":
            raise ValidationError(f"derived node must start EXPERIMENTAL/QA_HOLD: {node.model_id}")
    interaction = by_id["G1-ABLATION-TW-LORA"]
    if "A_B_C_D_REQUIRED" not in interaction.notes:
        raise ValidationError("interaction node must retain A/B/C/D prerequisite note")


def assert_baseline_unchanged(existing: ModelNode, replacement: ModelNode) -> None:
    if existing.model_id == "G1-BASE" and existing.to_dict() != replacement.to_dict():
        raise ValidationError("G1-BASE overwrite rejected")
