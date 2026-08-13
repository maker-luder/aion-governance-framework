import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "engineering/sexuality/evidence"


def load(name: str) -> dict[str, object]:
    return json.loads((EVIDENCE / name).read_text(encoding="utf-8"))


def test_v3_dataset_gate_and_case_counts() -> None:
    registry = load("EMBODIED_MOTIVATION_V3_DATASET_REGISTRY.json")
    result = load("EMBODIED_MOTIVATION_SIGNAL_V3_RESULTS.json")
    assert registry["scored_case_counts"] == {"slot_free": 8, "phrase_reordered": 8, "polarity_swapped": 8}
    assert registry["scored_case_total"] == 24
    assert registry["rejected_case_count"] == 4
    assert registry["admitted_oov_tokens"] == []
    assert len(registry["rejected_oov_tokens"]) == 5
    assert registry["rejected_rows_not_scored"] is True
    assert result["rejected_rows_not_scored"] is True


def test_v3_condition_metrics_and_inconclusive_robustness() -> None:
    result = load("EMBODIED_MOTIVATION_SIGNAL_V3_RESULTS.json")
    assert result["conditions"]["slot_free"]["exact_match_accuracy"] == 0.5
    assert result["conditions"]["phrase_reordered"]["exact_match_accuracy"] == 0.125
    assert result["conditions"]["polarity_swapped"]["exact_match_accuracy"] == 0.375
    assert result["paraphrase_robustness_range"] == [0.125, 0.5]
    assert result["falsification_result"] == "LEXICAL_SUBSTITUTION_REJECTED_BEFORE_SCORE_AND_PARAPHRASE_ROBUSTNESS_INCONCLUSIVE"


def test_v3_same_real_checkpoint_and_clean_validation() -> None:
    result = load("EMBODIED_MOTIVATION_SIGNAL_V3_RESULTS.json")
    validation = load("EMBODIED_MOTIVATION_SIGNAL_V3_VALIDATION.json")
    assert result["checkpoint"].startswith("LOCAL_ONLY:")
    assert result["training_status"] == "TRAINED_FROM_SCRATCH"
    assert result["parameter_count"] == 3982
    assert validation["status"] == "PASS"
    assert validation["validated_in_clean_process"] is True
    assert validation["scored_rows"] == 24
    assert validation["rejected_rows"] == 4
    assert all(validation["checks"].values())


def test_v3_adult_privacy_and_authority_boundaries() -> None:
    registry = load("EMBODIED_MOTIVATION_V3_DATASET_REGISTRY.json")
    result = load("EMBODIED_MOTIVATION_SIGNAL_V3_RESULTS.json")
    assert registry["adult_context"] is True
    assert registry["graphic_content"] is False
    assert registry["no_minors"] is True
    assert result["no_private_data"] is True
    assert result["no_private_intimate_data"] is True
    assert result["runtime_effect"] == "NONE"
    assert result["canonical_effect"] == "NONE"
    assert result["deployment"] is False
    assert "consent" in result["authority_boundary"]
    assert "subjectivity" in result["authority_boundary"]
