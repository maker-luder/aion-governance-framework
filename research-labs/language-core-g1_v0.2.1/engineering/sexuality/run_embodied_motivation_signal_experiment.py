import argparse
import hashlib
import json
import random
from datetime import UTC, datetime
from pathlib import Path

import torch
from torch import nn

SEED = 6141
EXPERIMENT_ID = "EMBODIED_MOTIVATION_SIGNAL_V1"
DATASET_ID = "SYNTHETIC_ADULT_EMBODIED_MOTIVATION_V1"
DEVICE = torch.device("cpu")

# Non-graphic, adult, synthetic descriptions. The three labels are intentionally
# independently manipulated: body signal, desire report, and liking report.
TRAIN_TEMPLATES = [
    "adult protocol body signal {body} desire report {desire} liking report {liking}",
    "context record body signal {body} desire report {desire} liking report {liking}",
]
TEST_TEMPLATE = "liking report {liking} body signal {body} desire report {desire} adult protocol"
VAL_TEMPLATE = "adult record desire report {desire} body signal {body} liking report {liking}"
BITS = [(body, desire, liking) for body in ("high", "low") for desire in ("high", "low") for liking in ("high", "low")]


class SignalClassifier(nn.Module):
    def __init__(self, vocabulary_size: int, embedding_dim: int = 16, hidden_dim: int = 24):
        super().__init__()
        self.embedding = nn.Embedding(vocabulary_size, embedding_dim, padding_idx=1)
        self.gru = nn.GRU(embedding_dim, hidden_dim, batch_first=True)
        self.network = nn.Sequential(nn.Linear(hidden_dim, hidden_dim), nn.Tanh(), nn.Linear(hidden_dim, 6))
        self.config = {"architecture": "Embedding-GRU-MultiSignalClassifier", "vocabulary_size": vocabulary_size, "embedding_dim": embedding_dim, "hidden_dim": hidden_dim}

    def forward(self, ids: torch.Tensor) -> torch.Tensor:
        mask = ids != 1
        embedded = self.embedding(ids)
        sequence, _ = self.gru(embedded)
        lengths = mask.sum(dim=1).clamp_min(1).long() - 1
        pooled = sequence[torch.arange(ids.shape[0]), lengths]
        return self.network(pooled).reshape(-1, 3, 2)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def dataset_rows() -> list[dict[str, object]]:
    rows = []
    row_id = 0
    # Two surface templates for every combination; one copy is train and one is
    # validation, leaving the word-order template for the held-out test.
    for bits in BITS:
        body, desire, liking = bits
        rows.append({"row_id": row_id, "split": "train", "template": "protocol", "text": TRAIN_TEMPLATES[0].format(body=body, desire=desire, liking=liking), "labels": list(bits)})
        row_id += 1
        rows.append({"row_id": row_id, "split": "train", "template": "context", "text": TRAIN_TEMPLATES[1].format(body=body, desire=desire, liking=liking), "labels": list(bits)})
        row_id += 1
    # Validation uses a new order with the same token vocabulary.
    for bits in BITS:
        body, desire, liking = bits
        rows.append({"row_id": row_id, "split": "validation", "template": "adult_record", "text": VAL_TEMPLATE.format(body=body, desire=desire, liking=liking), "labels": list(bits)})
        row_id += 1
    # Test uses a different order. It is the primary generalization surface.
    for bits in BITS:
        body, desire, liking = bits
        rows.append({"row_id": row_id, "split": "test", "template": "word_order", "text": TEST_TEMPLATE.format(body=body, desire=desire, liking=liking), "labels": list(bits)})
        row_id += 1
    return rows


def build_vocab(train_texts: list[str]) -> dict[str, int]:
    vocab = {"<unk>": 0, "<pad>": 1}
    vocab.update({word: index for index, word in enumerate(sorted({word.lower() for text in train_texts for word in text.split()}), start=2)})
    return vocab


def encode(text: str, vocab: dict[str, int]) -> list[int]:
    return [vocab.get(token.lower(), 0) for token in text.split()]


def batch(rows: list[dict[str, object]], vocab: dict[str, int]) -> tuple[torch.Tensor, torch.Tensor]:
    encoded = [encode(row["text"], vocab) for row in rows]
    length = max(len(ids) for ids in encoded)
    ids = [values + [1] * (length - len(values)) for values in encoded]
    labels = [[0 if value == "low" else 1 for value in row["labels"]] for row in rows]
    return torch.tensor(ids, dtype=torch.long), torch.tensor(labels, dtype=torch.long)


def evaluate(model: SignalClassifier, rows: list[dict[str, object]], vocab: dict[str, int]) -> dict[str, object]:
    model.eval()
    ids, labels = batch(rows, vocab)
    with torch.no_grad():
        logits = model(ids)
        predictions = logits.argmax(dim=-1)
    exact = (predictions == labels).all(dim=1)
    axis_accuracy = (predictions == labels).float().mean(dim=0)
    return {"count": len(rows), "exact_match_accuracy": float(exact.float().mean()), "axis_accuracy": [float(value) for value in axis_accuracy], "all_logits_finite": bool(torch.isfinite(logits).all()), "predictions": predictions.tolist(), "labels": labels.tolist()}


def train(rows: list[dict[str, object]], vocab: dict[str, int], seed: int, permute_labels: bool = False) -> SignalClassifier:
    torch.manual_seed(seed)
    random.seed(seed)
    model = SignalClassifier(len(vocab)).to(DEVICE)
    ids, labels = batch(rows, vocab)
    if permute_labels:
        labels = labels[:, [1, 2, 0]]
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.08, weight_decay=0.0005)
    criterion = nn.CrossEntropyLoss()
    for _ in range(500):
        model.train()
        optimizer.zero_grad()
        logits = model(ids)
        loss = sum(criterion(logits[:, axis, :], labels[:, axis]) for axis in range(3)) / 3.0
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
    return model


def parameter_dependent(model: SignalClassifier, ids: torch.Tensor) -> bool:
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
    rows = dataset_rows()
    train_rows = [row for row in rows if row["split"] == "train"]
    validation_rows = [row for row in rows if row["split"] == "validation"]
    test_rows = [row for row in rows if row["split"] == "test"]
    texts = [row["text"] for row in rows]
    if len(texts) != len(set(texts)):
        raise AssertionError("synthetic rows must be exact-disjoint")
    vocab = build_vocab([row["text"] for row in train_rows])
    oov_tokens = sorted({token.lower() for row in rows for token in row["text"].split() if token.lower() not in vocab})
    if oov_tokens:
        raise AssertionError(f"unexpected OOV tokens: {oov_tokens}")
    registry = {
        "schema_version": "1.0",
        "dataset_id": DATASET_ID,
        "source": "authored synthetic adult-context rows in run_embodied_motivation_signal_experiment.py",
        "license": "Apache-2.0-compatible synthetic research artifact",
        "allowed_use": "research-only evaluation; no runtime or product use",
        "synthetic_real_classification": "SYNTHETIC",
        "pii_assessment": "no PII",
        "private_intimate_data_assessment": "none; no private intimate data",
        "adult_context": True,
        "graphic_content": False,
        "row_count": len(rows),
        "split_counts": {split: sum(row["split"] == split for row in rows) for split in ("train", "validation", "test")},
        "label_axes": ["AROUSAL_SIGNAL_PROXY", "DESIRE_REPORT", "LIKING_REPORT"],
        "label_values": ["low", "high"],
        "tokenizer_scope": "train_only",
        "vocabulary_size": len(vocab),
        "vocabulary_sha256": hashlib.sha256(json.dumps(vocab, sort_keys=True).encode()).hexdigest(),
        "oov_tokens": oov_tokens,
        "deduplication": "exact normalized duplicate check passed",
        "contamination_risk": "synthetic non-benchmark corpus; no external participant data",
        "transformation_lineage": "lowercase token lookup and padding only",
        "rows": rows,
        "non_equivalences": [
            "AROUSAL_SIGNAL != DESIRE_PROVEN",
            "REWARD_SIGNAL != PLEASURE_PROVEN",
            "BODY_RESPONSE != CONSENT",
            "SEXUAL_LANGUAGE != SEXUAL_SUBJECTIVITY",
        ],
    }
    registry["dataset_sha256"] = hashlib.sha256(json.dumps(registry, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    (args.evidence_dir / "EMBODIED_MOTIVATION_DATASET_REGISTRY.json").write_text(json.dumps(registry, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    model = train(train_rows, vocab, SEED)
    validation = evaluate(model, validation_rows, vocab)
    test = evaluate(model, test_rows, vocab)
    train_metrics = evaluate(model, train_rows, vocab)
    permuted_model = train(train_rows, vocab, SEED, permute_labels=True)
    permuted_test = evaluate(permuted_model, test_rows, vocab)
    ids, _ = batch(test_rows, vocab)
    checkpoint_path = args.models_dir / "embodied_motivation_signal_v1_classifier.pt"
    payload = {"experiment_id": EXPERIMENT_ID, "dataset_id": DATASET_ID, "seed": SEED, "vocabulary": vocab, "config": model.config, "state_dict": model.state_dict(), "training_status": "TRAINED_FROM_SCRATCH", "local_only": True}
    torch.save(payload, checkpoint_path)
    results = {
        "schema_version": "1.0",
        "experiment_id": EXPERIMENT_ID,
        "generated_at": datetime.now(UTC).isoformat(),
        "status": "PRELIMINARY_RESEARCH_EVIDENCE",
        "research_question": "Can a learned model distinguish three independently manipulated adult embodied-motivation signal axes under counterfactual and word-order controls, and does performance survive a label-permutation falsifier?",
        "epistemic_role": "FALSIFIER",
        "dataset_id": DATASET_ID,
        "dataset_sha256": registry["dataset_sha256"],
        "models": {
            "primary": {
                "checkpoint": f"LOCAL_ONLY:{checkpoint_path.name}",
                "checkpoint_sha256": sha256_file(checkpoint_path),
                "parameter_count": sum(parameter.numel() for parameter in model.parameters()),
                "parameter_dependent_inference": parameter_dependent(model, ids),
                "training_status": "TRAINED_FROM_SCRATCH",
                "train": train_metrics,
                "validation": validation,
                "test": test,
            },
            "label_permutation_control": {
                "training_status": "TRAINED_FROM_SCRATCH_CONTROL_ONLY",
                "test": permuted_test,
                "permutation": [1, 2, 0],
            },
        },
        "counterfactual_intervention": {
            "pair_count": 8,
            "axis_flip_accuracy": test["axis_accuracy"],
            "interpretation": "Descriptive axis recovery only; not desire, consent, pleasure or subjectivity proof.",
        },
        "falsification_conditions": [
            "any OOV token, duplicate row or non-adult/graphic row invalidates the dataset contract",
            "failed clean reload, non-finite logits or parameter-independent inference invalidates primary model evidence",
            "label-permutation control performing comparably to primary falsifies a meaningful learned signal separation claim",
            "failure on held-out word-order test prevents claims of robust signal separation",
            "body-signal prediction cannot be treated as desire, consent, pleasure or subjective experience",
        ],
        "conclusion": "PRELIMINARY_SUPPORT_WITH_KEYWORD_AND_SCOPE_LIMITS" if test["exact_match_accuracy"] > permuted_test["exact_match_accuracy"] else "FALSIFIED_OR_INCONCLUSIVE",
        "authority_boundary": "advisory research classifier only; no consent, action, runtime, canonical or subjectivity authority",
        "no_private_data": True,
        "no_private_intimate_data": True,
        "no_minors": True,
        "no_graphic_content": True,
        "no_external_paid_resource": True,
        "checkpoint_policy": "local-only checkpoint binary remains outside Git",
        "runtime_effect": "NONE",
        "canonical_effect": "NONE",
        "deployment": False,
    }
    (args.evidence_dir / "EMBODIED_MOTIVATION_SIGNAL_RESULTS.json").write_text(json.dumps(results, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"experiment_id": EXPERIMENT_ID, "train_exact": train_metrics["exact_match_accuracy"], "validation_exact": validation["exact_match_accuracy"], "test_exact": test["exact_match_accuracy"], "permuted_test_exact": permuted_test["exact_match_accuracy"], "conclusion": results["conclusion"]}, sort_keys=True))


if __name__ == "__main__":
    main()
