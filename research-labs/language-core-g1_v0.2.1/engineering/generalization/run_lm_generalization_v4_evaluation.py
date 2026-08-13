import argparse
import hashlib
import json
import math
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

import torch
import torch.nn.functional as F

FORMAL_ROOT = Path(__file__).resolve().parents[4]
SRC = FORMAL_ROOT / "research-labs/language-core-g1_v0.2.1/engineering/real-model-candidate/src"
sys.path.insert(0, str(SRC))
from real_models import CausalLanguageModel, WordTokenizer, parameter_count, sha256_file  # noqa: E402

EXPERIMENT_ID = "LM_GENERALIZATION_V4"
DATASET_ID = "SYNTHETIC_GOVERNANCE_EXPANDED_PERTURBATION_V4"
DEVICE = torch.device("cpu")

# Authored only from the V3 train vocabulary. These rows are intentionally distinct
# from every V3 row and combine concepts across topics or perturb their order.
ROWS = [
    ("cross_topic_composition", "provenance_memory", "source records preserve context history across sessions"),
    ("cross_topic_composition", "provenance_safety", "traceable source records remain outside canonical deployment"),
    ("cross_topic_composition", "memory_tools", "governed recall requires deterministic tool authorization"),
    ("cross_topic_composition", "privacy_audit", "explicit authorization preserves deletion audit traces"),
    ("cross_topic_composition", "continuity_research", "continuity evaluation requires falsifiable research tests"),
    ("cross_topic_composition", "model_safety", "model lineage remains outside canonical runtime truth"),
    ("cross_topic_composition", "recovery_provenance", "partial execution requires recovery before source revision"),
    ("cross_topic_composition", "evidence_authority", "learned scores remain advisory outside research"),
    ("cross_topic_composition", "privacy_memory", "stored context remains separate from explicit privacy authorization"),
    ("cross_topic_composition", "audit_continuity", "replay evidence records current state across sessions"),
    ("word_order_perturbation", "provenance_memory", "history context preserve records source across sessions"),
    ("word_order_perturbation", "provenance_safety", "canonical deployment remains outside records traceable source"),
    ("word_order_perturbation", "memory_tools", "authorization deterministic requires recall governed tool"),
    ("word_order_perturbation", "privacy_audit", "audit traces preserve authorization explicit deletion"),
    ("word_order_perturbation", "continuity_research", "falsifiable tests require evaluation continuity research"),
    ("word_order_perturbation", "model_safety", "runtime truth remains outside lineage canonical model"),
    ("word_order_perturbation", "recovery_provenance", "source revision before recovery requires execution partial"),
    ("word_order_perturbation", "evidence_authority", "outside research advisory remain scores learned"),
    ("word_order_perturbation", "privacy_memory", "authorization privacy explicit separate remains context stored"),
    ("word_order_perturbation", "audit_continuity", "sessions across state current records evidence replay"),
]


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def load_model(path: Path) -> tuple[dict[str, object], WordTokenizer, CausalLanguageModel]:
    payload = torch.load(path, map_location=DEVICE, weights_only=False)
    tokenizer = WordTokenizer(payload["tokenizer"]["vocabulary"])
    config = payload["config"]
    model = CausalLanguageModel(config["vocabulary_size"], embedding_dim=config["embedding_dim"], hidden_dim=config["hidden_dim"]).to(DEVICE)
    model.load_state_dict(payload["state_dict"])
    model.eval()
    return payload, tokenizer, model


def parameter_dependent(model: CausalLanguageModel, tokenizer: WordTokenizer) -> bool:
    input_ids = torch.tensor([tokenizer.encode("source records preserve")], dtype=torch.long, device=DEVICE)
    with torch.no_grad():
        learned = model(input_ids).clone()
        original = {key: value.detach().clone() for key, value in model.state_dict().items()}
        for parameter in model.parameters():
            parameter.zero_()
        zeroed = model(input_ids).clone()
        model.load_state_dict(original)
    return not torch.allclose(learned, zeroed)


def score(model: CausalLanguageModel, tokenizer: WordTokenizer, text: str) -> dict[str, object]:
    ids = tokenizer.encode(text)
    if len(ids) < 3:
        raise ValueError(f"row too short: {text}")
    inputs = torch.tensor([ids[:-1]], dtype=torch.long, device=DEVICE)
    targets = torch.tensor([ids[1:]], dtype=torch.long, device=DEVICE)
    with torch.no_grad():
        logits = model(inputs)
        losses = F.cross_entropy(logits.reshape(-1, logits.shape[-1]), targets.reshape(-1), reduction="none")
        predictions = logits.argmax(dim=-1)
    token_accuracy = float((predictions == targets).float().mean())
    mean_loss = float(losses.mean())
    return {
        "loss": mean_loss,
        "perplexity": float(math.exp(min(mean_loss, 20.0))),
        "token_accuracy": token_accuracy,
        "token_count": len(ids),
        "all_logits_finite": bool(torch.isfinite(logits).all()),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models-dir", type=Path, required=True)
    parser.add_argument("--evidence-dir", type=Path, required=True)
    parser.add_argument("--v3-registry", type=Path, required=True)
    args = parser.parse_args()
    args.evidence_dir.mkdir(parents=True, exist_ok=True)
    v3_registry = json.loads(args.v3_registry.read_text(encoding="utf-8"))
    v3_rows = {row["text"].strip().lower() for row in v3_registry["rows"]}
    texts = [text for _, _, text in ROWS]
    if len(texts) != len(set(texts)):
        raise AssertionError("V4 rows must be exact-disjoint")
    if set(texts) & v3_rows:
        raise AssertionError("V4 rows must not duplicate V3 rows")

    baseline_path = args.models_dir / "lm_generalization_v3_baseline.pt"
    regularized_path = args.models_dir / "lm_generalization_v3_regularized_primary.pt"
    baseline_payload, baseline_tokenizer, baseline_model = load_model(baseline_path)
    regularized_payload, regularized_tokenizer, regularized_model = load_model(regularized_path)
    if baseline_tokenizer.sha256() != regularized_tokenizer.sha256():
        raise AssertionError("V4 comparison requires identical tokenizers")
    train_vocab = set(baseline_tokenizer.vocabulary)
    oov_tokens = sorted({token for text in texts for token in text.lower().split() if token not in train_vocab})
    if oov_tokens:
        raise AssertionError(f"V4 OOV tokens: {oov_tokens}")

    grouped = defaultdict(list)
    for condition, composition, text in ROWS:
        grouped[condition].append(text)
    registry = {
        "schema_version": "1.0",
        "dataset_id": DATASET_ID,
        "source": "authored synthetic V4 rows in run_lm_generalization_v4_evaluation.py",
        "license": "Apache-2.0-compatible synthetic research artifact",
        "synthetic_real_classification": "SYNTHETIC",
        "pii_assessment": "no PII",
        "private_intimate_data_assessment": "none; no private intimate data",
        "allowed_use": "local research evaluation only",
        "split_method": "fixed authored held-out rows, exact-disjoint from V3, train-only tokenizer vocabulary",
        "tokenizer_scope": "V3 train_only vocabulary",
        "tokenizer_sha256": baseline_tokenizer.sha256(),
        "v3_registry_sha256": sha256_text(args.v3_registry.read_text(encoding="utf-8")),
        "rows": [{"row_id": index, "condition": condition, "composition": composition, "text": text} for index, (condition, composition, text) in enumerate(ROWS)],
        "condition_counts": {key: len(value) for key, value in grouped.items()},
        "oov_tokens": oov_tokens,
        "no_external_data_ingestion": True,
    }
    registry["dataset_sha256"] = sha256_text(json.dumps(registry, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    (args.evidence_dir / "GENERALIZATION_PERTURBATION_V4_DATASET_REGISTRY.json").write_text(json.dumps(registry, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    models = {}
    for name, payload, tokenizer, model, path in (
        ("baseline", baseline_payload, baseline_tokenizer, baseline_model, baseline_path),
        ("regularized_primary", regularized_payload, regularized_tokenizer, regularized_model, regularized_path),
    ):
        rows = []
        for row_id, (condition, composition, text) in enumerate(ROWS):
            metrics = score(model, tokenizer, text)
            rows.append({"row_id": row_id, "condition": condition, "composition": composition, "text": text, **metrics})
        by_condition = {}
        for condition in sorted({row["condition"] for row in rows}):
            selected = [row for row in rows if row["condition"] == condition]
            by_condition[condition] = {
                "count": len(selected),
                "mean_loss": sum(row["loss"] for row in selected) / len(selected),
                "mean_perplexity": sum(row["perplexity"] for row in selected) / len(selected),
                "mean_token_accuracy": sum(row["token_accuracy"] for row in selected) / len(selected),
            }
        models[name] = {
            "checkpoint": f"LOCAL_ONLY:{path.name}",
            "checkpoint_sha256": sha256_file(path),
            "dataset_id": payload.get("dataset_id"),
            "tokenizer_sha256": tokenizer.sha256(),
            "parameter_count": parameter_count(model),
            "parameter_dependent_inference": parameter_dependent(model, tokenizer),
            "training_status": payload.get("training_status"),
            "rows": rows,
            "by_condition": by_condition,
            "mean_loss": sum(row["loss"] for row in rows) / len(rows),
            "mean_perplexity": sum(row["perplexity"] for row in rows) / len(rows),
            "mean_token_accuracy": sum(row["token_accuracy"] for row in rows) / len(rows),
        }
    baseline_improvements = []
    for row_id in range(len(ROWS)):
        baseline_improvements.append(models["baseline"]["rows"][row_id]["loss"] - models["regularized_primary"]["rows"][row_id]["loss"])
    result = {
        "schema_version": "1.0",
        "experiment_id": EXPERIMENT_ID,
        "generated_at": datetime.now(UTC).isoformat(),
        "status": "PRELIMINARY_RESEARCH_EVIDENCE",
        "research_question": "Do two V3 learned checkpoints retain the V3 regularization advantage across an expanded, exact-disjoint held-out corpus with cross-topic composition and word-order perturbation?",
        "epistemic_role": "MEASUREMENT",
        "dataset_id": DATASET_ID,
        "dataset_sha256": registry["dataset_sha256"],
        "v3_train_only_vocabulary": True,
        "v3_exact_disjoint": True,
        "row_count": len(ROWS),
        "condition_counts": registry["condition_counts"],
        "oov_count": len(oov_tokens),
        "models": models,
        "paired_loss_improvements_regularized_minus_baseline": baseline_improvements,
        "mean_loss_improvement_regularized_minus_baseline": sum(baseline_improvements) / len(baseline_improvements),
        "positive_paired_improvement_count": sum(value > 0 for value in baseline_improvements),
        "minimum_paired_improvement": min(baseline_improvements),
        "falsification_conditions": [
            "any V4 OOV token or duplicate against V3 invalidates the held-out contract",
            "failed checkpoint reload, non-finite inference or parameter-independent inference invalidates the model evidence",
            "negative or mixed paired improvements falsify a universal claim that regularization always improves this expanded evaluation",
            "this small synthetic evaluation cannot establish mature general-purpose language capability",
        ],
        "conclusion": "PRELIMINARY_SUPPORT" if all(value > 0 for value in baseline_improvements) else "MIXED_OR_FALSIFIED_REGULARIZATION_EFFECT",
        "authority_boundary": "descriptive held-out measurement only; scores cannot authorize actions, become canonical truth or establish subjectivity",
        "model_registry_status": "OPTIONAL_RESEARCH_MODEL_INPUTS; NO_NEW_MODEL_ADDED",
        "no_private_data": True,
        "no_private_intimate_data": True,
        "no_external_paid_resource": True,
        "checkpoint_policy": "local-only checkpoint binaries remain outside Git",
    }
    (args.evidence_dir / "LM_GENERALIZATION_V4_RESULTS.json").write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"experiment_id": EXPERIMENT_ID, "rows": len(ROWS), "oov_count": len(oov_tokens), "positive_paired_improvement_count": result["positive_paired_improvement_count"], "minimum_paired_improvement": result["minimum_paired_improvement"], "conclusion": result["conclusion"]}, sort_keys=True))


if __name__ == "__main__":
    main()
