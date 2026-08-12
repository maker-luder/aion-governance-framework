from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "datasets"

DATASETS: dict[str, object] = {
    "SYNTHETIC_GOVERNANCE_CORPUS_V1": {
        "train": [
            "aion preserves provenance and namespace boundaries",
            "astra executes bounded research workflows",
            "memory recall requires authorization and evidence",
            "governed tools never bypass approval",
            "research claims remain separate from implementation",
            "audit records preserve source and transformation history",
            "cross session context is assembled under a recall gate",
            "model outputs are advisory and not canonical state",
            "the owner reviews promotion and deployment decisions",
            "a bounded runtime records failure and recovery evidence",
        ],
        "test": [
            "provenance remains inspectable across model swaps",
            "namespace isolation denies unauthorized memory",
        ],
    },
    "SYNTHETIC_TRADITIONAL_CHINESE_GOVERNANCE_V1": {
        "train": [
            "台灣 繁體 中文 治理 邊界",
            "記憶 回憶 必須 經過 授權",
            "來源 證據 不等於 身份",
            "模型 輸出 不得 改寫 canonical state",
            "AION Astra 維持 namespace isolation",
        ],
        "test": [],
    },
    "SYNTHETIC_MEMORY_SEMANTIC_PAIRS_V1": {
        "pairs": [
            ["authorized memory recall", "governed memory retrieval", 1.0],
            ["authorized memory recall", "unrelated weather forecast", -1.0],
            ["namespace policy denies foreign memory", "cross session recall explicit scope", 1.0],
            ["namespace policy denies foreign memory", "cooking recipe grocery list", -1.0],
            ["model output advisory evidence", "deployment approval separate decision", 1.0],
            ["model output advisory evidence", "weather forecast tomorrow", -1.0],
        ]
    },
    "SYNTHETIC_RERANKING_PAIRS_V1": {
        "rows": [
            ["memory recall", "authorized memory retrieval", 1.0, "q1"],
            ["memory recall", "weather forecast", 0.0, "q1"],
            ["memory recall", "provenance audit", 0.0, "q1"],
            ["tool approval", "trusted approval record", 1.0, "q2"],
            ["tool approval", "cooking recipe", 0.0, "q2"],
            ["tool approval", "memory namespace", 0.0, "q2"],
            ["namespace isolation", "foreign namespace denied", 1.0, "q3"],
            ["namespace isolation", "local namespace scope", 0.0, "q3"],
        ]
    },
    "SYNTHETIC_TOOL_ROUTING_INTENTS_V1": {
        "rows": [
            ["find authorized memory", "memory_recall"],
            ["retrieve cross session context", "memory_recall"],
            ["call governed tool", "tool_execution"],
            ["request approval for tool", "tool_execution"],
            ["summarize evidence record", "summarize"],
            ["condense research passage", "summarize"],
            ["check provenance chain", "governance_audit"],
            ["audit namespace policy", "governance_audit"],
        ]
    },
    "SYNTHETIC_MEMORY_SALIENCE_V1": {
        "features": [
            [0.95, 0.90, 0.05, 0.95, 1], [0.85, 0.70, 0.10, 0.90, 1],
            [0.20, 0.90, 0.90, 0.40, 0], [0.10, 0.10, 0.10, 0.30, 0],
            [0.80, 0.20, 0.80, 0.90, 0], [0.70, 0.80, 0.20, 0.80, 1],
            [0.30, 0.30, 0.70, 0.30, 0], [0.15, 0.20, 0.20, 0.20, 0],
            [0.92, 0.40, 0.10, 0.95, 1], [0.25, 0.70, 0.40, 0.50, 0],
        ]
    },
    "SYNTHETIC_TEMPORAL_CONTINUITY_V1": {
        "generation_rule": "trend=(index mod 7)*0.04 + step*0.08; context=((index*3+step) mod 5)*0.05; reset=1 at step 0; target=0.8*last trend + 0.3*last context - 0.1*first reset",
        "train_size": 64,
        "test_size": 16,
        "sequence_length": 8,
        "feature_names": ["trend", "context", "reset"],
    },
}


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    registry = []
    for dataset_id, payload in DATASETS.items():
        path = DATA / f"{dataset_id}.json"
        path.write_text(json.dumps({"dataset_id": dataset_id, "status": "SYNTHETIC", "payload": payload}, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        registry.append({"dataset_id": dataset_id, "artifact_path": str(path.relative_to(ROOT)), "artifact_sha256": digest, "source": "training/materialize_datasets.py", "license": "Apache-2.0-compatible synthetic artifact", "allowed_use": "local research candidate training/evaluation only", "pii_assessment": "NO_PII_SYNTHETIC", "private_material_assessment": "NO_PRIVATE_MATERIAL", "transformation_lineage": "generated from source script with seed 1729 where applicable", "status": "APPROVED_LOCAL_SYNTHETIC"})
    (ROOT / "qa/DATASET_MATERIALIZATION.json").write_text(json.dumps(registry, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"dataset_count": len(registry), "all_synthetic": True}, sort_keys=True))


if __name__ == "__main__":
    main()
