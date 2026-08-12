import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "engineering/generalization/evidence"


def load(name: str) -> dict[str, object]:
    return json.loads((EVIDENCE / name).read_text(encoding="utf-8"))


def test_v3_dataset_is_fixed_disjoint_and_train_vocabulary_scoped() -> None:
    dataset = load("GENERALIZATION_COMPOSITION_V3_DATASET_REGISTRY.json")
    rows = dataset["rows"]
    by_split = {}
    for row in rows:
        by_split.setdefault(row["split"], []).append(row["text"])
    assert set(by_split) == {"train", "validation", "test"}
    assert len(rows) == 42
    assert len(by_split["train"]) == 26
    assert len(by_split["validation"]) == 8
    assert len(by_split["test"]) == 8
    assert len({" ".join(text.lower().split()) for text in sum(by_split.values(), [])}) == len(rows)
    assert dataset["tokenizer_scope"] == "train_only"
    assert dataset["synthetic_real_classification"] == "SYNTHETIC"


def test_v3_compositional_generalization_is_replicated_but_preliminary() -> None:
    evidence = load("LM_GENERALIZATION_V3_RESULTS.json")
    assert evidence["status"] == "PRELIMINARY_RESEARCH_EVIDENCE"
    assert evidence["composition_test_contract"]["test_rows_are_cross_topic"] is True
    assert evidence["composition_test_contract"]["train_only_vocabulary"] is True
    assert evidence["composition_test_contract"]["unknown_tokens_in_test"] == 0
    assert evidence["paired_improvement_supported"] is True
    assert evidence["paired_improvement_min"] > 0.0
    assert len(evidence["paired_seed_results"]) == 3
    assert evidence["model_status"].startswith("OPTIONAL_RESEARCH_MODEL")
    assert "MATURE_GENERAL_PURPOSE" not in evidence["conclusion"]


def test_v3_checkpoints_clean_reload_and_parameter_dependence() -> None:
    validation = load("LM_GENERALIZATION_V3_VALIDATION.json")
    assert validation["status"] == "PASS"
    assert validation["validated_in_clean_process"] is True
    assert all(validation["checks"].values())
    assert len(validation["models"]) == 2
    assert all(item["parameter_dependent_inference"] for item in validation["models"])
    assert all(item["tokenizer_training_scope"] == "train_only" for item in validation["models"])


def test_v3_has_explicit_falsifiers_and_no_private_or_paid_resources() -> None:
    evidence = load("LM_GENERALIZATION_V3_RESULTS.json")
    assert len(evidence["falsification_conditions"]) >= 5
    assert evidence["no_private_data"] is True
    assert evidence["no_external_paid_resource"] is True
    assert "general-purpose" in " ".join(evidence["falsification_conditions"])
