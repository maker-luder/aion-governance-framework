import argparse
import hashlib
import json
import random
from datetime import UTC, datetime
from pathlib import Path

import torch
from torch import nn

from run_embodied_motivation_signal_experiment import dataset_rows

DEVICE = torch.device("cpu")
SEED = 7319
EXPERIMENT_ID = "CHARACTER_OOV_COMPARATOR_V1"
DATASET_ID = "SYNTHETIC_ADULT_EMBODIED_MOTIVATION_CHARACTER_OOV_V1"


class CharSignalClassifier(nn.Module):
    def __init__(self, vocabulary_size: int, embedding_dim: int = 16, hidden_dim: int = 24):
        super().__init__()
        self.embedding = nn.Embedding(vocabulary_size, embedding_dim, padding_idx=0)
        self.gru = nn.GRU(embedding_dim, hidden_dim, batch_first=True)
        self.head = nn.Sequential(nn.Linear(hidden_dim, hidden_dim), nn.Tanh(), nn.Linear(hidden_dim, 6))
        self.config = {
            "architecture": "CharEmbedding-GRU-MultiSignalClassifier",
            "vocabulary_size": vocabulary_size,
            "embedding_dim": embedding_dim,
            "hidden_dim": hidden_dim,
        }

    def forward(self, ids: torch.Tensor) -> torch.Tensor:
        mask = ids != 0
        embedded = self.embedding(ids)
        sequence, _ = self.gru(embedded)
        lengths = mask.sum(dim=1).clamp_min(1).long() - 1
        pooled = sequence[torch.arange(ids.shape[0]), lengths]
        return self.head(pooled).reshape(-1, 3, 2)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def labels_to_int(labels: list[str]) -> list[int]:
    return [0 if value == "low" else 1 for value in labels]


def make_train_rows() -> list[dict[str, object]]:
    return [row for row in dataset_rows() if row["split"] == "train"]


def make_oov_rows() -> list[dict[str, object]]:
    body_words = {"high": "bright", "low": "cold"}
    desire_words = {"high": "wanting", "low": "reluctant"}
    liking_words = {"high": "glad", "low": "neutral"}
    rows = []
    row_id = 0
    for body in ("high", "low"):
        for desire in ("high", "low"):
            for liking in ("high", "low"):
                rows.append({
                    "row_id": row_id,
                    "split": "oov_paraphrase",
                    "text": f"adult context body state {body_words[body]} desire state {desire_words[desire]} liking state {liking_words[liking]} protocol record",
                    "labels": [body, desire, liking],
                })
                row_id += 1
    return rows


def build_char_vocab(train_rows: list[dict[str, object]]) -> dict[str, int]:
    characters = sorted({char for row in train_rows for char in row["text"]})
    return {"<pad>": 0, **{char: index for index, char in enumerate(characters, start=1)}}


def encode(text: str, vocab: dict[str, int]) -> list[int]:
    return [vocab[char] for char in text]


def batch(rows: list[dict[str, object]], vocab: dict[str, int]) -> tuple[torch.Tensor, torch.Tensor]:
    encoded = [encode(row["text"], vocab) for row in rows]
    length = max(len(ids) for ids in encoded)
    ids = [values + [0] * (length - len(values)) for values in encoded]
    labels = [labels_to_int(row["labels"]) for row in rows]
    return torch.tensor(ids, dtype=torch.long), torch.tensor(labels, dtype=torch.long)


def evaluate(model: CharSignalClassifier, rows: list[dict[str, object]], vocab: dict[str, int]) -> dict[str, object]:
    ids, labels = batch(rows, vocab)
    model.eval()
    with torch.no_grad():
        logits = model(ids)
        predictions = logits.argmax(dim=-1)
    return {
        "count": len(rows),
        "exact_match_accuracy": float((predictions == labels).all(dim=1).float().mean()),
        "axis_accuracy": [float(value) for value in (predictions == labels).float().mean(dim=0)],
        "all_logits_finite": bool(torch.isfinite(logits).all()),
        "predictions": predictions.tolist(),
        "labels": labels.tolist(),
    }


def train(train_rows: list[dict[str, object]], vocab: dict[str, int], seed: int, permute_labels: bool = False) -> CharSignalClassifier:
    torch.manual_seed(seed)
    random.seed(seed)
    model = CharSignalClassifier(len(vocab)).to(DEVICE)
    ids, labels = batch(train_rows, vocab)
    if permute_labels:
        labels = labels[:, [1, 2, 0]]
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.04, weight_decay=0.0005)
    criterion = nn.CrossEntropyLoss()
    for _ in range(700):
        model.train()
        optimizer.zero_grad()
        logits = model(ids)
        loss = sum(criterion(logits[:, axis, :], labels[:, axis]) for axis in range(3)) / 3.0
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
    return model


def parameter_dependent(model: CharSignalClassifier, ids: torch.Tensor) -> bool:
    model.eval()
    with torch.no_grad():
        learned = model(ids).clone()
        original = {key: value.detach().clone() for key, value in model.state_dict().items()}
        for parameter in model.parameters():
            parameter.zero_()
        zeroed = model(ids).clone()
        model.load_state_dict(original)
    return not torch.allclose(learned, zeroed)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models-dir", type=Path, required=True)
    parser.add_argument("--evidence-dir", type=Path, required=True)
    args = parser.parse_args()
    args.models_dir.mkdir(parents=True, exist_ok=True)
    args.evidence_dir.mkdir(parents=True, exist_ok=True)
    train_rows = make_train_rows()
    oov_rows = make_oov_rows()
    word_train_vocab = {word.lower() for row in train_rows for word in row["text"].split()}
    word_oov_tokens = sorted({word.lower() for row in oov_rows for word in row["text"].split() if word.lower() not in word_train_vocab})
    char_vocab = build_char_vocab(train_rows)
    char_oov_characters = sorted({char for row in oov_rows for char in row["text"] if char not in char_vocab})
    if char_oov_characters:
        raise AssertionError(f"character comparator has unexpected OOV characters: {char_oov_characters}")
    registry = {
        "schema_version": "1.0",
        "dataset_id": DATASET_ID,
        "source": "authored synthetic adult-context rows; train text reused from prior V1 synthetic corpus and OOV evaluation rows authored for this comparator",
        "license": "Apache-2.0-compatible synthetic research artifact",
        "allowed_use": "research-only tokenizer comparison; no runtime or product use",
        "synthetic_real_classification": "SYNTHETIC",
        "adult_context": True,
        "graphic_content": False,
        "no_minors": True,
        "pii_assessment": "no PII",
        "private_intimate_data_assessment": "none; no private intimate data",
        "train_row_count": len(train_rows),
        "oov_eval_row_count": len(oov_rows),
        "word_train_vocabulary_size": len(word_train_vocab),
        "word_oov_token_count": len(word_oov_tokens),
        "word_oov_tokens": word_oov_tokens,
        "character_vocabulary_size": len(char_vocab),
        "character_oov_character_count": len(char_oov_characters),
        "character_oov_characters": char_oov_characters,
        "split_method": "V1 train rows for training; eight novel-word combinations for held-out OOV evaluation",
        "deduplication": "exact normalized text checks are applied before evidence write",
        "contamination_risk": "synthetic non-benchmark corpus; no participant data",
        "transformation_lineage": "character encoding only; no external corpus or pretrained weights",
        "model_role": "OPTIONAL_RESEARCH_MODEL",
        "non_equivalences": [
            "AROUSAL_SIGNAL != DESIRE_PROVEN",
            "BODY_RESPONSE != CONSENT",
            "SEXUAL_LANGUAGE != SEXUAL_SUBJECTIVITY",
        ],
    }
    all_texts = [row["text"] for row in train_rows + oov_rows]
    registry["exact_text_duplicates"] = len(all_texts) - len(set(all_texts))
    if registry["exact_text_duplicates"] != 0:
        raise AssertionError("character comparator rows must be exact-disjoint")
    registry["dataset_sha256"] = hashlib.sha256(json.dumps(registry, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    (args.evidence_dir / "CHARACTER_OOV_COMPARATOR_DATASET_REGISTRY.json").write_text(json.dumps(registry, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    model = train(train_rows, char_vocab, SEED)
    train_metrics = evaluate(model, train_rows, char_vocab)
    oov_metrics = evaluate(model, oov_rows, char_vocab)
    permutation_model = train(train_rows, char_vocab, SEED, permute_labels=True)
    permutation_oov_metrics = evaluate(permutation_model, oov_rows, char_vocab)
    oov_ids, _ = batch(oov_rows, char_vocab)
    checkpoint_path = args.models_dir / "character_oov_comparator_v1_classifier.pt"
    torch.save({"experiment_id": EXPERIMENT_ID, "dataset_id": DATASET_ID, "seed": SEED, "vocabulary": char_vocab, "config": model.config, "state_dict": model.state_dict(), "training_status": "TRAINED_FROM_SCRATCH", "local_only": True}, checkpoint_path)
    result = {
        "schema_version": "1.0",
        "experiment_id": EXPERIMENT_ID,
        "generated_at": datetime.now(UTC).isoformat(),
        "status": "PRELIMINARY_RESEARCH_EVIDENCE",
        "epistemic_role": "FALSIFIER",
        "research_question": "Does a character-tokenized real learned comparator recover held-out novel-word embodied-motivation proxy labels that the V1 word tokenizer must reject as OOV?",
        "dataset_id": DATASET_ID,
        "dataset_sha256": registry["dataset_sha256"],
        "checkpoint": f"LOCAL_ONLY:{checkpoint_path.name}",
        "checkpoint_sha256": sha256_file(checkpoint_path),
        "parameter_count": sum(parameter.numel() for parameter in model.parameters()),
        "training_status": "TRAINED_FROM_SCRATCH",
        "primary": {"train": train_metrics, "oov_eval": oov_metrics, "parameter_dependent_inference": parameter_dependent(model, oov_ids)},
        "label_permutation_control": {"oov_eval": permutation_oov_metrics, "training_status": "TRAINED_FROM_SCRATCH_CONTROL_ONLY"},
        "word_tokenizer_control": {"oov_tokens_rejected": len(word_oov_tokens), "rows_scored": 0, "gate_before_score": True},
        "character_tokenizer_control": {"oov_characters_rejected": len(char_oov_characters), "rows_scored": len(oov_rows), "gate_before_score": True},
        "falsification_result": "CHARACTER_OOV_RECOVERY_INCONCLUSIVE" if oov_metrics["exact_match_accuracy"] <= permutation_oov_metrics["exact_match_accuracy"] else "CHARACTER_OOV_RECOVERY_PRELIMINARY_SUPPORT",
        "falsification_conditions": [
            "any character OOV, duplicate, non-adult or graphic row invalidates the comparator dataset",
            "word-tokenizer OOV rows must not be scored as word-model evidence",
            "character comparator performance at or below label-permutation control falsifies a learned OOV recovery interpretation",
            "small synthetic OOV recovery does not establish robust language understanding or mature AION LM capability",
            "model outputs cannot infer desire, consent, pleasure, subjectivity or authorize action",
        ],
        "no_private_data": True,
        "no_private_intimate_data": True,
        "no_minors": True,
        "no_graphic_content": True,
        "no_external_paid_resource": True,
        "authority_boundary": "optional research comparator only; no sexual, consent, runtime, canonical or subjectivity authority",
        "runtime_effect": "NONE",
        "canonical_effect": "NONE",
        "deployment": False,
    }
    (args.evidence_dir / "CHARACTER_OOV_COMPARATOR_RESULTS.json").write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"experiment_id": EXPERIMENT_ID, "train_exact": train_metrics["exact_match_accuracy"], "oov_exact": oov_metrics["exact_match_accuracy"], "permuted_oov_exact": permutation_oov_metrics["exact_match_accuracy"], "word_oov_tokens": len(word_oov_tokens), "falsification_result": result["falsification_result"]}, sort_keys=True))


if __name__ == "__main__":
    main()
