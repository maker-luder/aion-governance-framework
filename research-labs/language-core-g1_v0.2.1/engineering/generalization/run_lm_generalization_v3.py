import argparse
import copy
import hashlib
import json
import random
import sys
from datetime import UTC, datetime
from pathlib import Path

import torch
import torch.nn.functional as F
from torch import nn

FORMAL_ROOT = Path(__file__).resolve().parents[4]
SRC = FORMAL_ROOT / "research-labs/language-core-g1_v0.2.1/engineering/real-model-candidate/src"
sys.path.insert(0, str(SRC))
from real_models import CausalLanguageModel, WordTokenizer, parameter_count, sha256_file  # noqa: E402

DATASET_ID = "SYNTHETIC_GOVERNANCE_COMPOSITION_V3"
SEED = 2027
PAIRED_SEEDS = (SEED, SEED + 1, SEED + 2)
DEVICE = torch.device("cpu")
EMBEDDING_DIM = 16
HIDDEN_DIM = 32

# All rows are authored synthetic governance text. The test rows are compositions
# of concepts represented in train, while no exact test row is present in train.
TRAIN_ROWS = [
    ("provenance", "source records preserve transformation history"),
    ("provenance", "evidence records retain a traceable origin"),
    ("provenance", "hashes bind artifacts to their recorded source"),
    ("memory", "governed recall checks namespace boundaries"),
    ("memory", "stored context remains separate from memory"),
    ("memory", "supersession preserves earlier records for audit"),
    ("tools", "tool execution requires deterministic authorization"),
    ("tools", "learned scores cannot approve external actions"),
    ("tools", "malformed output enters a governed failure path"),
    ("safety", "canonical promotion requires an owner decision"),
    ("safety", "canonical runtime truth remains outside research workbench"),
    ("safety", "deployment remains outside the research workbench"),
    ("safety", "independent review cannot be self certified"),
    ("privacy", "private data requires explicit authorization"),
    ("privacy", "deletion requests preserve audit traces"),
    ("privacy", "consent cannot be inferred from a body signal"),
    ("privacy", "privacy boundaries require authorization"),
    ("audit", "replay evidence records request identifiers"),
    ("audit", "model lineage records training history"),
    ("audit", "current state remains inspectable"),
    ("continuity", "continuity evaluation compares state across sessions"),
    ("continuity", "contradictions require review before revision"),
    ("continuity", "recovery reconciles partial execution"),
    ("research", "research hypotheses require falsifiable tests"),
    ("research", "synthetic fixtures remain bounded evidence"),
    ("research", "scores remain advisory and cannot become authority"),
]
VALIDATION_ROWS = [
    ("provenance", "source records preserve a traceable history"),
    ("memory", "stored context remains separate from governed recall"),
    ("tools", "tool execution requires authorization"),
    ("safety", "research remains outside deployment workbench"),
    ("privacy", "deletion requests preserve explicit authorization"),
    ("audit", "replay evidence records model lineage"),
    ("continuity", "continuity compares state across sessions"),
    ("research", "bounded evidence remains synthetic"),
]
TEST_ROWS = [
    ("composition", "traceable evidence requires source records preserve namespace boundaries"),
    ("composition", "learned scores remain advisory and cannot become authority"),
    ("composition", "private data requires deletion requests preserve audit traces"),
    ("composition", "research evidence cannot become canonical runtime truth"),
    ("composition", "partial execution requires recovery before state revision"),
    ("composition", "consent evidence requires authorization and privacy boundaries"),
    ("composition", "replay evidence records current state identifiers"),
    ("composition", "synthetic fixtures remain advisory and falsifiable"),
]
ROWS = TRAIN_ROWS + VALIDATION_ROWS + TEST_ROWS
SPLIT = {
    "train": list(range(len(TRAIN_ROWS))),
    "validation": list(range(len(TRAIN_ROWS), len(TRAIN_ROWS) + len(VALIDATION_ROWS))),
    "test": list(range(len(TRAIN_ROWS) + len(VALIDATION_ROWS), len(ROWS))),
}


def seed_all(seed: int) -> None:
    random.seed(seed)
    torch.manual_seed(seed)


def normalize(text: str) -> str:
    return " ".join(text.lower().split())


def dataset_digest() -> str:
    payload = json.dumps(
        {"dataset_id": DATASET_ID, "rows": ROWS, "split": SPLIT, "tokenizer_scope": "train_only"},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def make_examples(tokenizer: WordTokenizer, indices: list[int]) -> list[tuple[torch.Tensor, torch.Tensor]]:
    examples = []
    for index in indices:
        ids = tokenizer.encode(ROWS[index][1])
        if len(ids) < 3:
            raise ValueError(f"row {index} is too short for causal evaluation")
        examples.append((torch.tensor([ids[:-1]], dtype=torch.long), torch.tensor([ids[1:]], dtype=torch.long)))
    return examples


def weighted_loss(
    model: nn.Module,
    examples: list[tuple[torch.Tensor, torch.Tensor]],
    *,
    label_smoothing: float = 0.0,
    train: bool = False,
) -> torch.Tensor:
    total = torch.tensor(0.0, device=DEVICE)
    tokens = 0
    for inputs, targets in examples:
        logits = model(inputs)
        loss = F.cross_entropy(
            logits.reshape(-1, logits.shape[-1]),
            targets.reshape(-1),
            reduction="sum",
            label_smoothing=label_smoothing,
        )
        total = total + loss
        tokens += int(targets.numel())
    result = total / max(tokens, 1)
    return result if train else result.detach()


def evaluate(model: CausalLanguageModel, examples: dict[str, list[tuple[torch.Tensor, torch.Tensor]]]) -> dict[str, float]:
    model.eval()
    with torch.no_grad():
        return {split: float(weighted_loss(model, rows)) for split, rows in examples.items()}


def train_variant(
    *,
    name: str,
    seed: int,
    tokenizer: WordTokenizer,
    examples: dict[str, list[tuple[torch.Tensor, torch.Tensor]]],
    regularized: bool,
    epochs: int,
) -> tuple[CausalLanguageModel, dict[str, object]]:
    seed_all(seed)
    model = CausalLanguageModel(len(tokenizer.vocabulary), embedding_dim=EMBEDDING_DIM, hidden_dim=HIDDEN_DIM).to(DEVICE)
    if regularized:
        optimizer = torch.optim.AdamW(model.parameters(), lr=0.005, weight_decay=0.02)
        smoothing = 0.05
        patience = 24
        clip_norm = 1.0
    else:
        optimizer = torch.optim.Adam(model.parameters(), lr=0.02)
        smoothing = 0.0
        patience = epochs
        clip_norm = None
    losses: list[float] = []
    best_validation = float("inf")
    best_state = copy.deepcopy(model.state_dict())
    best_epoch = 0
    stale = 0
    for epoch in range(epochs):
        model.train()
        order = list(range(len(examples["train"])))
        random.shuffle(order)
        ordered = [examples["train"][index] for index in order]
        optimizer.zero_grad()
        loss = weighted_loss(model, ordered, label_smoothing=smoothing, train=True)
        loss.backward()
        if clip_norm is not None:
            torch.nn.utils.clip_grad_norm_(model.parameters(), clip_norm)
        optimizer.step()
        losses.append(float(loss.detach()))
        validation = float(weighted_loss(model, examples["validation"]))
        if validation < best_validation - 1e-8:
            best_validation = validation
            best_state = copy.deepcopy(model.state_dict())
            best_epoch = epoch + 1
            stale = 0
        else:
            stale += 1
        if stale >= patience:
            break
    model.load_state_dict(best_state)
    metrics = evaluate(model, examples)
    metrics.update(
        {
            "name": name,
            "seed": seed,
            "regularized": regularized,
            "epochs_requested": epochs,
            "epochs_completed": len(losses),
            "best_epoch": best_epoch,
            "train_loss_first": losses[0],
            "train_loss_last": losses[-1],
            "loss_curve": losses,
            "parameter_count": parameter_count(model),
            "optimizer_updates_occurred": len(losses) > 0,
            "clean_reload_required": True,
        }
    )
    return model, metrics


def parameter_dependent(model: CausalLanguageModel, prompt: torch.Tensor) -> bool:
    model.eval()
    with torch.no_grad():
        learned = model(prompt).clone()
        original = {key: value.detach().clone() for key, value in model.state_dict().items()}
        for parameter in model.parameters():
            parameter.zero_()
        zeroed = model(prompt).clone()
        model.load_state_dict(original)
    return not torch.allclose(learned, zeroed)


def save_model(path: Path, model: CausalLanguageModel, tokenizer: WordTokenizer, metrics: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "state_dict": model.state_dict(),
            "config": model.config,
            "tokenizer": tokenizer.to_dict(),
            "tokenizer_sha256": tokenizer.sha256(),
            "seed": metrics["seed"],
            "dataset_id": DATASET_ID,
            "training_status": "TRAINED_FROM_SCRATCH",
            "experiment_role": "OPTIONAL_RESEARCH_MODEL_GENERALIZATION_V3",
            "tokenizer_training_scope": "train_only",
        },
        path,
    )


def write_dataset_artifact(evidence_dir: Path, tokenizer: WordTokenizer) -> None:
    evidence_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "dataset_id": DATASET_ID,
        "source": "synthetic sentences authored in run_lm_generalization_v3.py",
        "license": "Apache-2.0-compatible synthetic research artifact",
        "allowed_use": "local research training and evaluation only",
        "pii_assessment": "no PII",
        "private_intimate_data_assessment": "none; no private intimate data",
        "transformation_lineage": "normalized whitespace only; no external ingestion",
        "split_method": "fixed authored rows; train/validation/test rows are disjoint and test rows are cross-topic compositions",
        "tokenizer_scope": "train_only",
        "unknown_token_policy": "test and validation tokens must already occur in the train vocabulary; assertion enforced",
        "deduplication": "exact normalized duplicate check passed",
        "contamination_risk": "synthetic non-benchmark corpus; no external benchmark contamination claimed",
        "synthetic_real_classification": "SYNTHETIC",
        "rows": [
            {"row_id": index, "topic": topic, "text": text, "split": next(split for split, ids in SPLIT.items() if index in ids)}
            for index, (topic, text) in enumerate(ROWS)
        ],
        "train_vocabulary_size": len(tokenizer.vocabulary),
        "tokenizer_sha256": tokenizer.sha256(),
        "dataset_sha256": dataset_digest(),
    }
    (evidence_dir / "GENERALIZATION_COMPOSITION_V3_DATASET_REGISTRY.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models-dir", type=Path, required=True)
    parser.add_argument(
        "--evidence-dir",
        type=Path,
        default=FORMAL_ROOT / "research-labs/language-core-g1_v0.2.1/engineering/generalization/evidence",
    )
    args = parser.parse_args()
    args.models_dir.mkdir(parents=True, exist_ok=True)
    args.evidence_dir.mkdir(parents=True, exist_ok=True)

    normalized = [normalize(text) for _, text in ROWS]
    if len(normalized) != len(set(normalized)):
        raise AssertionError("exact normalized duplicate detected")
    train_texts = [text for _, text in TRAIN_ROWS]
    tokenizer = WordTokenizer.from_texts(train_texts)
    train_words = set(word for text in train_texts for word in normalize(text).split())
    for split_name in ("validation", "test"):
        unknown = sorted(set(word for index in SPLIT[split_name] for word in normalize(ROWS[index][1]).split()) - train_words)
        if unknown:
            raise AssertionError(f"{split_name} contains out-of-vocabulary words: {unknown}")
    examples = {split: make_examples(tokenizer, indices) for split, indices in SPLIT.items()}

    primary_baseline, primary_baseline_metrics = train_variant(
        name="baseline", seed=SEED, tokenizer=tokenizer, examples=examples, regularized=False, epochs=140
    )
    primary_regularized, primary_regularized_metrics = train_variant(
        name="regularized_primary", seed=SEED, tokenizer=tokenizer, examples=examples, regularized=True, epochs=180
    )
    baseline_replicates = []
    regularized_replicates = []
    for seed in PAIRED_SEEDS[1:]:
        _, baseline_rep = train_variant(
            name=f"baseline_seed_{seed}", seed=seed, tokenizer=tokenizer, examples=examples, regularized=False, epochs=140
        )
        _, regularized_rep = train_variant(
            name=f"regularized_seed_{seed}", seed=seed, tokenizer=tokenizer, examples=examples, regularized=True, epochs=180
        )
        baseline_replicates.append(baseline_rep)
        regularized_replicates.append(regularized_rep)

    baseline_path = args.models_dir / "lm_generalization_v3_baseline.pt"
    regularized_path = args.models_dir / "lm_generalization_v3_regularized_primary.pt"
    save_model(baseline_path, primary_baseline, tokenizer, primary_baseline_metrics)
    save_model(regularized_path, primary_regularized, tokenizer, primary_regularized_metrics)
    prompt = torch.tensor([tokenizer.encode("traceable recall requires")], dtype=torch.long)
    primary_baseline_metrics["parameter_dependent_inference"] = parameter_dependent(primary_baseline, prompt)
    primary_regularized_metrics["parameter_dependent_inference"] = parameter_dependent(primary_regularized, prompt)

    paired = [
        {
            "seed": SEED,
            "baseline_test": primary_baseline_metrics["test"],
            "regularized_test": primary_regularized_metrics["test"],
            "improvement": primary_baseline_metrics["test"] - primary_regularized_metrics["test"],
        }
    ]
    paired.extend(
        {
            "seed": int(baseline["seed"]),
            "baseline_test": baseline["test"],
            "regularized_test": regularized["test"],
            "improvement": baseline["test"] - regularized["test"],
        }
        for baseline, regularized in zip(baseline_replicates, regularized_replicates)
    )
    paired_improvements = [float(item["improvement"]) for item in paired]
    test_delta = float(primary_baseline_metrics["test"] - primary_regularized_metrics["test"])
    write_dataset_artifact(args.evidence_dir, tokenizer)
    payload = {
        "schema_version": "1.0",
        "experiment_id": "LM_GENERALIZATION_V3",
        "generated_at": datetime.now(UTC).isoformat(),
        "status": "PRELIMINARY_RESEARCH_EVIDENCE",
        "research_question": "Under a train-only vocabulary and fixed synthetic corpus, does modest regularization improve cross-topic compositional held-out loss over the prior scratch-LM recipe across paired seeds?",
        "falsification_conditions": [
            "regularized_primary.test_loss >= baseline.test_loss means the primary improvement hypothesis is not supported in this setup",
            "any paired seed improvement <= 0 means the replicated improvement hypothesis is not supported across this fixed seed set",
            "any validation or test token absent from the train-only vocabulary invalidates the intended no-lexical-leakage contract",
            "any duplicate normalized row across splits invalidates the split",
            "non-finite loss, missing optimizer updates, failed reload or parameter-independent inference invalidates learned-model evidence",
            "a synthetic compositional result cannot establish mature general-purpose language capability",
        ],
        "dataset_id": DATASET_ID,
        "dataset_sha256": dataset_digest(),
        "split": {key: len(value) for key, value in SPLIT.items()},
        "tokenizer_scope": "train_only; validation and test rows use only tokens observed in training rows",
        "architecture": {"class": "Embedding-GRU-CausalLM", "embedding_dim": EMBEDDING_DIM, "hidden_dim": HIDDEN_DIM},
        "device": str(DEVICE),
        "precision": "float32",
        "models": {
            "baseline": {**primary_baseline_metrics, "checkpoint": "LOCAL_ONLY:lm_generalization_v3_baseline.pt", "checkpoint_sha256": sha256_file(baseline_path)},
            "regularized_primary": {**primary_regularized_metrics, "checkpoint": "LOCAL_ONLY:lm_generalization_v3_regularized_primary.pt", "checkpoint_sha256": sha256_file(regularized_path)},
        },
        "baseline_replicates": baseline_replicates,
        "regularized_replicates": regularized_replicates,
        "paired_seed_results": paired,
        "paired_improvement_mean": sum(paired_improvements) / len(paired_improvements),
        "paired_improvement_min": min(paired_improvements),
        "primary_test_loss_improvement": test_delta,
        "primary_improvement_supported": bool(test_delta > 0.0),
        "paired_improvement_supported": bool(all(value > 0.0 for value in paired_improvements)),
        "composition_test_contract": {
            "test_rows_are_cross_topic": True,
            "exact_test_row_in_train": False,
            "train_only_vocabulary": True,
            "unknown_tokens_in_validation": 0,
            "unknown_tokens_in_test": 0,
        },
        "conclusion": "PRELIMINARY_SUPPORT" if test_delta > 0.0 and all(value > 0.0 for value in paired_improvements) else "FALSIFIED_FOR_THIS_SETUP",
        "model_status": "OPTIONAL_RESEARCH_MODEL; NOT_ADDED_TO_FORMAL_MODEL_REGISTRY",
        "authority_boundary": "advisory research evidence only; cannot authorize, canonize, rewrite provenance, bypass privacy or establish subjectivity",
        "no_private_data": True,
        "no_external_paid_resource": True,
        "clean_process_validation_script": "research-labs/language-core-g1_v0.2.1/engineering/generalization/validate_lm_generalization_v3_checkpoints.py",
    }
    (args.evidence_dir / "LM_GENERALIZATION_V3_RESULTS.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "experiment_id": payload["experiment_id"],
                "baseline_test": primary_baseline_metrics["test"],
                "regularized_test": primary_regularized_metrics["test"],
                "primary_test_loss_improvement": test_delta,
                "paired_improvement_min": min(paired_improvements),
                "conclusion": payload["conclusion"],
                "models": 2,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
