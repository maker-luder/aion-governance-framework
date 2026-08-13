import argparse
import hashlib
import json
from pathlib import Path

import torch

from run_character_oov_comparator import CharSignalClassifier, batch, make_oov_rows, make_train_rows

DEVICE = torch.device("cpu")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models-dir", type=Path, required=True)
    parser.add_argument("--evidence-dir", type=Path, required=True)
    args = parser.parse_args()
    result = json.loads((args.evidence_dir / "CHARACTER_OOV_COMPARATOR_RESULTS.json").read_text(encoding="utf-8"))
    registry = json.loads((args.evidence_dir / "CHARACTER_OOV_COMPARATOR_DATASET_REGISTRY.json").read_text(encoding="utf-8"))
    checkpoint_name = result["checkpoint"].split(":", 1)[1]
    checkpoint = args.models_dir / checkpoint_name
    payload = torch.load(checkpoint, map_location=DEVICE, weights_only=False)
    model = CharSignalClassifier(payload["config"]["vocabulary_size"], payload["config"]["embedding_dim"], payload["config"]["hidden_dim"])
    model.load_state_dict(payload["state_dict"])
    model.eval()
    train_rows = make_train_rows()
    oov_rows = make_oov_rows()
    vocab = payload["vocabulary"]
    ids, labels = batch(oov_rows, vocab)
    with torch.no_grad():
        logits = model(ids)
        original = {key: value.detach().clone() for key, value in model.state_dict().items()}
        learned = model(ids).clone()
        for parameter in model.parameters():
            parameter.zero_()
        zeroed = model(ids).clone()
        model.load_state_dict(original)
    word_train_vocab = {word.lower() for row in train_rows for word in row["text"].split()}
    word_oov_tokens = sorted({word.lower() for row in oov_rows for word in row["text"].split() if word.lower() not in word_train_vocab})
    char_oov_characters = sorted({char for row in oov_rows for char in row["text"] if char not in vocab})
    checks = {
        "checkpoint_exists": checkpoint.is_file(),
        "checkpoint_hash_matches": sha256_file(checkpoint) == result["checkpoint_sha256"],
        "dataset_id_matches": payload["dataset_id"] == registry["dataset_id"] == result["dataset_id"],
        "model_role_optional_research": registry["model_role"] == "OPTIONAL_RESEARCH_MODEL",
        "train_count": registry["train_row_count"] == 16,
        "oov_eval_count": registry["oov_eval_row_count"] == 8,
        "word_oov_present": registry["word_oov_tokens"] == word_oov_tokens and len(word_oov_tokens) >= 5,
        "word_rows_not_scored": result["word_tokenizer_control"]["rows_scored"] == 0 and result["word_tokenizer_control"]["gate_before_score"] is True,
        "character_oov_absent": registry["character_oov_characters"] == char_oov_characters == [],
        "character_rows_scored": result["character_tokenizer_control"]["rows_scored"] == 8 and result["character_tokenizer_control"]["gate_before_score"] is True,
        "adult_non_graphic_contract": registry["adult_context"] is True and registry["graphic_content"] is False and registry["no_minors"] is True,
        "no_private_data": result["no_private_data"] is True and result["no_private_intimate_data"] is True,
        "exact_disjoint_texts": registry["exact_text_duplicates"] == 0,
        "finite_logits": bool(torch.isfinite(logits).all()),
        "parameter_dependent_inference": not torch.allclose(learned, zeroed),
        "prediction_shape": tuple(logits.shape) == (8, 3, 2),
        "runtime_canonical_locks": result["runtime_effect"] == "NONE" and result["canonical_effect"] == "NONE" and result["deployment"] is False,
        "falsification_result_present": result["falsification_result"] in {"CHARACTER_OOV_RECOVERY_INCONCLUSIVE", "CHARACTER_OOV_RECOVERY_PRELIMINARY_SUPPORT"},
    }
    output = {
        "schema_version": "1.0",
        "experiment_id": "CHARACTER_OOV_COMPARATOR_V1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "validated_in_clean_process": True,
        "checkpoint": result["checkpoint"],
        "checkpoint_sha256": sha256_file(checkpoint),
        "checks": checks,
        "word_oov_rows_not_scored": True,
        "character_oov_rows_scored": 8,
        "non_claim": "Character-tokenized OOV evaluation is a tokenizer comparator only; it cannot prove desire, consent, pleasure, subjectivity or phenomenal experience.",
    }
    (args.evidence_dir / "CHARACTER_OOV_COMPARATOR_VALIDATION.json").write_text(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"experiment_id": output["experiment_id"], "status": output["status"], "checks_passed": sum(checks.values()), "checks_total": len(checks)}, sort_keys=True))
    if output["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
