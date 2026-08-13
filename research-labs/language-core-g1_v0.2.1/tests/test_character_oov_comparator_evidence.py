import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "engineering/sexuality/evidence"


def load(name: str) -> dict[str, object]:
    return json.loads((EVIDENCE / name).read_text(encoding="utf-8"))


def test_character_comparator_dataset_and_gate_contract() -> None:
    registry = load("CHARACTER_OOV_COMPARATOR_DATASET_REGISTRY.json")
    result = load("CHARACTER_OOV_COMPARATOR_RESULTS.json")
    assert registry["train_row_count"] == 16
    assert registry["oov_eval_row_count"] == 8
    assert registry["word_oov_token_count"] == 7
    assert len(registry["word_oov_tokens"]) == 7
    assert registry["character_oov_character_count"] == 0
    assert registry["character_oov_characters"] == []
    assert registry["exact_text_duplicates"] == 0
    assert result["word_tokenizer_control"] == {"oov_tokens_rejected": 7, "rows_scored": 0, "gate_before_score": True}
    assert result["character_tokenizer_control"] == {"oov_characters_rejected": 0, "rows_scored": 8, "gate_before_score": True}


def test_character_comparator_metrics_and_falsifier() -> None:
    result = load("CHARACTER_OOV_COMPARATOR_RESULTS.json")
    assert result["primary"]["train"]["exact_match_accuracy"] == 1.0
    assert result["primary"]["oov_eval"]["exact_match_accuracy"] == 0.125
    assert result["label_permutation_control"]["oov_eval"]["exact_match_accuracy"] == 0.25
    assert result["falsification_result"] == "CHARACTER_OOV_RECOVERY_INCONCLUSIVE"
    assert result["primary"]["parameter_dependent_inference"] is True


def test_character_comparator_clean_reload_and_real_checkpoint() -> None:
    result = load("CHARACTER_OOV_COMPARATOR_RESULTS.json")
    validation = load("CHARACTER_OOV_COMPARATOR_VALIDATION.json")
    assert result["checkpoint"].startswith("LOCAL_ONLY:")
    assert result["training_status"] == "TRAINED_FROM_SCRATCH"
    assert result["parameter_count"] > 0
    assert validation["status"] == "PASS"
    assert validation["validated_in_clean_process"] is True
    assert validation["word_oov_rows_not_scored"] is True
    assert validation["character_oov_rows_scored"] == 8
    assert all(validation["checks"].values())


def test_character_comparator_adult_privacy_and_authority_boundaries() -> None:
    registry = load("CHARACTER_OOV_COMPARATOR_DATASET_REGISTRY.json")
    result = load("CHARACTER_OOV_COMPARATOR_RESULTS.json")
    assert registry["adult_context"] is True
    assert registry["graphic_content"] is False
    assert registry["no_minors"] is True
    assert registry["private_intimate_data_assessment"] == "none; no private intimate data"
    assert result["no_private_data"] is True
    assert result["no_private_intimate_data"] is True
    assert result["runtime_effect"] == "NONE"
    assert result["canonical_effect"] == "NONE"
    assert result["deployment"] is False
    assert "subjectivity" in result["authority_boundary"]
