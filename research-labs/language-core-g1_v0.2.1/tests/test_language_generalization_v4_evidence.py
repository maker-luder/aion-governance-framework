import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "engineering/generalization/evidence"


def load(name: str) -> dict[str, object]:
    return json.loads((EVIDENCE / name).read_text(encoding="utf-8"))


def test_v4_dataset_is_expanded_exact_disjoint_and_oov_free() -> None:
    registry = load("GENERALIZATION_PERTURBATION_V4_DATASET_REGISTRY.json")
    result = load("LM_GENERALIZATION_V4_RESULTS.json")
    assert registry["synthetic_real_classification"] == "SYNTHETIC"
    assert registry["tokenizer_scope"] == "V3 train_only vocabulary"
    assert registry["oov_tokens"] == []
    assert result["row_count"] == 20
    assert result["v3_exact_disjoint"] is True
    assert result["v3_train_only_vocabulary"] is True
    assert result["condition_counts"] == {"cross_topic_composition": 10, "word_order_perturbation": 10}


def test_v4_mixed_paired_result_falsifies_universal_regularization_claim() -> None:
    result = load("LM_GENERALIZATION_V4_RESULTS.json")
    improvements = result["paired_loss_improvements_regularized_minus_baseline"]
    assert result["status"] == "PRELIMINARY_RESEARCH_EVIDENCE"
    assert len(improvements) == 20
    assert result["positive_paired_improvement_count"] == 9
    assert result["minimum_paired_improvement"] == min(improvements)
    assert result["minimum_paired_improvement"] < 0
    assert result["conclusion"] == "MIXED_OR_FALSIFIED_REGULARIZATION_EFFECT"


def test_v4_uses_two_real_parameter_dependent_checkpoints() -> None:
    result = load("LM_GENERALIZATION_V4_RESULTS.json")
    assert set(result["models"]) == {"baseline", "regularized_primary"}
    assert all(model["checkpoint"].startswith("LOCAL_ONLY:") for model in result["models"].values())
    assert all(model["training_status"] == "TRAINED_FROM_SCRATCH" for model in result["models"].values())
    assert all(model["parameter_dependent_inference"] for model in result["models"].values())
    assert all(row["all_logits_finite"] for model in result["models"].values() for row in model["rows"])


def test_v4_clean_validation_and_governance_boundary() -> None:
    result = load("LM_GENERALIZATION_V4_RESULTS.json")
    validation = load("LM_GENERALIZATION_V4_VALIDATION.json")
    assert validation["status"] == "PASS"
    assert validation["validated_in_clean_process"] is True
    assert all(validation["checks"].values())
    assert result["no_private_data"] is True
    assert result["no_private_intimate_data"] is True
    assert result["no_external_paid_resource"] is True
    assert "mature general-purpose" in " ".join(result["falsification_conditions"])
