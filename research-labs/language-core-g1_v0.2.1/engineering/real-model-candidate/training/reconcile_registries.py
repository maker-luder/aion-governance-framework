from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    registry_path = ROOT / "models/MODEL_REGISTRY.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    dataset_registry = {row["dataset_id"]: row for row in json.loads((ROOT / "qa/DATASET_MATERIALIZATION.json").read_text(encoding="utf-8"))}
    evaluation_paths = {
        "language_scratch_small": "evaluation/language_model_evaluation.json",
        "language_lora_adapter": "evaluation/language_model_evaluation.json",
        "embedding_memory_model": "evaluation/embedding_evaluation.json",
        "reranker_cross_encoder_model": "evaluation/reranker_evaluation.json",
        "router_planner_model_a": "evaluation/router_evaluation.json",
        "router_planner_model_b": "evaluation/router_evaluation.json",
        "memory_salience_model": "evaluation/salience_evaluation.json",
        "temporal_continuity_gru": "evaluation/temporal_evaluation.json",
    }
    for row in registry:
        dataset_artifacts = [dataset_registry[item] for item in row.get("dataset_ids", []) if item in dataset_registry]
        row["dataset_artifacts"] = dataset_artifacts
        checkpoint = row.get("checkpoint_path")
        if checkpoint:
            path = ROOT / checkpoint
            row["checkpoint_sha256"] = sha256(path)
            row["checkpoint_bytes"] = path.stat().st_size
        if row["model_id"] in evaluation_paths:
            row["evaluation_artifact"] = evaluation_paths[row["model_id"]]
        if row["model_id"] == "language_lora_adapter":
            base_path = ROOT / "models/language_scratch_small.pt"
            row["base_model_checkpoint_sha256"] = sha256(base_path)
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    dataset_rows = []
    for dataset_id, row in dataset_registry.items():
        artifact = ROOT / row["artifact_path"]
        dataset_rows.append({
            "dataset_id": dataset_id,
            "source": row["source"],
            "license": row["license"],
            "download_or_source_digest": row["artifact_sha256"],
            "allowed_use": row["allowed_use"],
            "pii_assessment": row["pii_assessment"],
            "private_material_assessment": row["private_material_assessment"],
            "transformation_lineage": row["transformation_lineage"],
            "split_method": "explicit payload in artifact",
            "artifact_path": row["artifact_path"],
            "artifact_sha256": row["artifact_sha256"],
            "dedup_status": "source-controlled synthetic artifact",
            "contamination_considerations": "not an external benchmark; no private or unknown-license data",
            "status": row["status"]
        })
    (ROOT / "datasets/DATASET_REGISTRY.json").write_text(json.dumps(sorted(dataset_rows, key=lambda item: item["dataset_id"]), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"registry_models": len(registry), "dataset_artifact_links": sum(len(row.get("dataset_artifacts", [])) for row in registry), "dataset_registry_rows": len(dataset_rows)}, sort_keys=True))


if __name__ == "__main__":
    main()
