import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "engineering/sexuality/evidence"


def load(name: str) -> dict[str, object]:
    return json.loads((EVIDENCE / name).read_text(encoding="utf-8"))


def test_embodied_motivation_dataset_is_adult_synthetic_and_non_graphic() -> None:
    registry = load("EMBODIED_MOTIVATION_DATASET_REGISTRY.json")
    assert registry["dataset_id"] == "SYNTHETIC_ADULT_EMBODIED_MOTIVATION_V1"
    assert registry["synthetic_real_classification"] == "SYNTHETIC"
    assert registry["adult_context"] is True
    assert registry["graphic_content"] is False
    assert registry["pii_assessment"] == "no PII"
    assert registry["private_intimate_data_assessment"] == "none; no private intimate data"
    assert registry["row_count"] == 32
    assert registry["split_counts"] == {"train": 16, "validation": 8, "test": 8}
    assert registry["oov_tokens"] == []
    assert len({row["text"] for row in registry["rows"]}) == registry["row_count"]


def test_embodied_motivation_result_has_held_out_and_permutation_contrast() -> None:
    result = load("EMBODIED_MOTIVATION_SIGNAL_RESULTS.json")
    assert result["status"] == "PRELIMINARY_RESEARCH_EVIDENCE"
    assert result["models"]["primary"]["test"]["count"] == 8
    assert result["models"]["label_permutation_control"]["test"]["count"] == 8
    assert result["models"]["primary"]["test"]["exact_match_accuracy"] == 0.25
    assert result["models"]["label_permutation_control"]["test"]["exact_match_accuracy"] == 0.125
    assert result["models"]["primary"]["test"]["exact_match_accuracy"] > result["models"]["label_permutation_control"]["test"]["exact_match_accuracy"]
    assert result["conclusion"] == "PRELIMINARY_SUPPORT_WITH_KEYWORD_AND_SCOPE_LIMITS"


def test_embodied_motivation_uses_real_checkpoint_and_clean_validation() -> None:
    result = load("EMBODIED_MOTIVATION_SIGNAL_RESULTS.json")
    validation = load("EMBODIED_MOTIVATION_SIGNAL_VALIDATION.json")
    model = result["models"]["primary"]
    assert model["checkpoint"].startswith("LOCAL_ONLY:")
    assert model["training_status"] == "TRAINED_FROM_SCRATCH"
    assert model["parameter_dependent_inference"] is True
    assert validation["status"] == "PASS"
    assert validation["validated_in_clean_process"] is True
    assert all(validation["checks"].values())


def test_embodied_motivation_preserves_non_equivalences_and_runtime_locks() -> None:
    registry = load("EMBODIED_MOTIVATION_DATASET_REGISTRY.json")
    result = load("EMBODIED_MOTIVATION_SIGNAL_RESULTS.json")
    assert "AROUSAL_SIGNAL != DESIRE_PROVEN" in registry["non_equivalences"]
    assert "REWARD_SIGNAL != PLEASURE_PROVEN" in registry["non_equivalences"]
    assert "BODY_RESPONSE != CONSENT" in registry["non_equivalences"]
    assert "SEXUAL_LANGUAGE != SEXUAL_SUBJECTIVITY" in registry["non_equivalences"]
    assert result["no_minors"] is True
    assert result["no_graphic_content"] is True
    assert result["no_private_data"] is True
    assert result["no_private_intimate_data"] is True
    assert result["runtime_effect"] == "NONE"
    assert result["canonical_effect"] == "NONE"
    assert result["deployment"] is False
