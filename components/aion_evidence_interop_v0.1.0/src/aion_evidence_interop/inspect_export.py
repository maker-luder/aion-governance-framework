from __future__ import annotations

from typing import Any


def export_inspect(record: dict[str, Any], source_ref: str) -> tuple[dict[str, Any], dict[str, Any]]:
    architecture = record.get("evidence_architecture", {})
    expected = [str(v) for v in record.get("expected_outcomes", [])]
    sample = {
        "id": str(record.get("claim_id", "")),
        "input": str(record.get("claim_text", "")),
        "target": expected,
        "metadata": {
            "aion_source_ref": source_ref,
            "claim_level": str(record.get("claim_level", "")),
            "hypothesis": str(record.get("hypothesis", "")),
            "competing_hypotheses": [
                str(v) for v in record.get("competing_hypotheses", [])
            ],
            "protocol_ref": str(record.get("protocol_ref", "")),
            "observation": str(architecture.get("observation", "")),
            "mechanism": str(architecture.get("mechanism", "")),
            "interpretation": str(architecture.get("interpretation", "")),
            "alternative_explanations": [
                str(v) for v in architecture.get("alternative_explanations", [])
            ],
            "limitations": [str(v) for v in record.get("limitations", [])],
            "preregistration_status": str(record.get("preregistration_status", "")),
            "execution_authorized": False,
        },
    }
    task_manifest = {
        "profile": "AION_INSPECT_EXPORT_V0.1.0",
        "dataset_format": "Inspect Sample-compatible JSON Lines",
        "dataset_ref": "inspect/dataset.jsonl",
        "source_ref": source_ref,
        "execution": {
            "model_execution": False,
            "network_access": False,
            "sandbox_setup": False,
            "solver_defined": False,
            "scorer_defined": False,
        },
        "nonclaims": {
            "subjectivity_conclusion": "NOT_ESTABLISHED",
            "identity_continuity_conclusion": "NOT_ESTABLISHED",
            "scientific_validation": "NOT_ESTABLISHED",
        },
    }
    return task_manifest, sample
