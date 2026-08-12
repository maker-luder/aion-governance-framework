from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "engineering/generalization/evidence"


def load(name: str) -> dict[str, object]:
    return json.loads((EVIDENCE / name).read_text(encoding="utf-8"))


def test_generalization_dataset_has_disjoint_fixed_splits() -> None:
    dataset = load("GENERALIZATION_DATASET_REGISTRY.json")
    rows = dataset["rows"]
    by_split = {}
    for row in rows:
        by_split.setdefault(row["split"], []).append(row["text"])
    assert set(by_split) == {"train", "validation", "test"}
    assert len({" ".join(text.lower().split()) for text in sum(by_split.values(), [])}) == len(rows)
    assert sum(len(values) for values in by_split.values()) == 24


def test_paired_generalization_result_is_replicated_but_preliminary() -> None:
    evidence = load("LM_GENERALIZATION_RESULTS.json")
    assert evidence["status"] == "PRELIMINARY_RESEARCH_EVIDENCE"
    assert evidence["paired_improvement_supported"] is True
    assert evidence["paired_improvement_min"] > 0.0
    assert len(evidence["paired_seed_results"]) == 3
    assert evidence["model_status"].startswith("OPTIONAL_RESEARCH_MODEL")
    assert "MATURE_GENERAL_PURPOSE" not in evidence["conclusion"]


def test_generalization_checkpoints_clean_reload_and_parameter_dependence() -> None:
    validation = load("LM_GENERALIZATION_VALIDATION.json")
    assert validation["status"] == "PASS"
    assert all(validation["checks"].values())
    assert len(validation["models"]) == 2
    assert all(item["parameter_dependent_inference"] for item in validation["models"])


def test_generalization_has_explicit_falsifiers_and_no_private_data() -> None:
    evidence = load("LM_GENERALIZATION_RESULTS.json")
    assert len(evidence["falsification_conditions"]) >= 4
    assert evidence["no_private_data"] is True
    assert evidence["no_external_paid_resource"] is True
    assert "general-purpose" in " ".join(evidence["falsification_conditions"])
