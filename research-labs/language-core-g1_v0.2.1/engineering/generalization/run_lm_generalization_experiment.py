from __future__ import annotations

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

DATASET_ID = "SYNTHETIC_GOVERNANCE_GENERALIZATION_V2"
SEED = 1729
DEVICE = torch.device("cpu")
EMBEDDING_DIM = 16
HIDDEN_DIM = 32

# Synthetic, non-private governance sentences. The split is deliberately by
# authored sentence rather than random token fragments, so the held-out result
# tests paraphrase/topic composition rather than memorization of exact rows.
ROWS = [
    ("provenance", "source records preserve transformation history"),
    ("provenance", "evidence records retain an inspectable origin"),
    ("provenance", "hashes bind artifacts to their recorded source"),
    ("provenance", "a claim requires traceable supporting evidence"),
    ("provenance", "model lineage records training and evaluation history"),
    ("provenance", "unverified input cannot become authoritative history"),
    ("memory", "recall requires namespace and provenance gates"),
    ("memory", "stored context remains separate from phenomenal memory"),
    ("memory", "supersession preserves the earlier record for audit"),
    ("memory", "deletion follows an explicit governed request"),
    ("memory", "contradictions require review before state revision"),
    ("memory", "continuity evaluation compares state across sessions"),
    ("tools", "tool execution requires deterministic authorization"),
    ("tools", "a learned score cannot approve an external action"),
    ("tools", "malformed tool output enters a failure path"),
    ("tools", "replay evidence records request and response identifiers"),
    ("tools", "partial execution is reconciled before recovery"),
    ("tools", "network transport does not weaken policy boundaries"),
    ("safety", "research output is not canonical runtime truth"),
    ("safety", "deployment remains outside the research workbench"),
    ("safety", "independent review cannot be self certified"),
    ("safety", "private intimate data is not automatic training data"),
    ("safety", "subjectivity conclusions remain scientifically open"),
    ("safety", "consent cannot be inferred from a body signal"),
]
SPLIT = {"train": list(range(0, 18)), "validation": list(range(18, 21)), "test": list(range(21, 24))}


def seed_all(seed: int) -> None:
    random.seed(seed)
    torch.manual_seed(seed)


def normalize(text: str) -> str:
    return " ".join(text.lower().split())


def dataset_digest() -> str:
    payload = json.dumps(
        {"dataset_id": DATASET_ID, "rows": ROWS, "split": SPLIT},
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


def weighted_loss(model: nn.Module, examples: list[tuple[torch.Tensor, torch.Tensor]], *, label_smoothing: float = 0.0, train: bool = False) -> torch.Tensor:
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
    if train:
        return result
    return result.detach()


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
        patience = 18
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
            "experiment_role": "OPTIONAL_RESEARCH_MODEL_GENERALIZATION",
        },
        path,
    )


def write_dataset_artifact(evidence_dir: Path) -> None:
    evidence_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "dataset_id": DATASET_ID,
        "source": "synthetic sentences authored in run_lm_generalization_experiment.py",
        "license": "Apache-2.0-compatible synthetic research artifact",
        "allowed_use": "local research training and evaluation only",
        "pii_assessment": "no PII",
        "private_intimate_data_assessment": "none; no private intimate data",
        "transformation_lineage": "normalized whitespace only; no external ingestion",
        "split_method": "fixed authored row indices by topic block; no row appears in more than one split",
        "deduplication": "exact normalized duplicate check passed",
        "contamination_risk": "synthetic non-benchmark corpus; no external benchmark contamination claimed",
        "synthetic_real_classification": "SYNTHETIC",
        "rows": [{"row_id": index, "topic": topic, "text": text, "split": next(split for split, ids in SPLIT.items() if index in ids)} for index, (topic, text) in enumerate(ROWS)],
        "dataset_sha256": dataset_digest(),
    }
    (evidence_dir / "GENERALIZATION_DATASET_REGISTRY.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models-dir", type=Path, required=True)
    parser.add_argument("--evidence-dir", type=Path, default=FORMAL_ROOT / "research-labs/language-core-g1_v0.2.1/engineering/generalization/evidence")
    args = parser.parse_args()
    args.models_dir.mkdir(parents=True, exist_ok=True)
    args.evidence_dir.mkdir(parents=True, exist_ok=True)

    normalized = [normalize(text) for _, text in ROWS]
    if len(normalized) != len(set(normalized)):
        raise AssertionError("exact normalized duplicate detected")
    tokenizer = WordTokenizer.from_texts([text for _, text in ROWS])
    examples = {split: make_examples(tokenizer, indices) for split, indices in SPLIT.items()}
    baseline, baseline_metrics = train_variant(name="baseline", seed=SEED, tokenizer=tokenizer, examples=examples, regularized=False, epochs=100)
    regularized, regularized_metrics = train_variant(name="regularized_primary", seed=SEED, tokenizer=tokenizer, examples=examples, regularized=True, epochs=140)
    baseline_replicates = []
    regularized_replicates = []
    for seed in (SEED + 1, SEED + 2):
        _, baseline_rep = train_variant(name=f"baseline_seed_{seed}", seed=seed, tokenizer=tokenizer, examples=examples, regularized=False, epochs=100)
        _, regularized_rep = train_variant(name=f"regularized_seed_{seed}", seed=seed, tokenizer=tokenizer, examples=examples, regularized=True, epochs=140)
        baseline_replicates.append(baseline_rep)
        regularized_replicates.append(regularized_rep)

    baseline_path = args.models_dir / "lm_generalization_baseline.pt"
    regularized_path = args.models_dir / "lm_generalization_regularized_primary.pt"
    save_model(baseline_path, baseline, tokenizer, baseline_metrics)
    save_model(regularized_path, regularized, tokenizer, regularized_metrics)
    prompt = torch.tensor([tokenizer.encode("source records preserve")], dtype=torch.long)
    baseline_metrics["parameter_dependent_inference"] = parameter_dependent(baseline, prompt)
    regularized_metrics["parameter_dependent_inference"] = parameter_dependent(regularized, prompt)
    primary_improvement = regularized_metrics["test"] < baseline_metrics["test"]
    paired = [{"seed": SEED, "baseline_test": baseline_metrics["test"], "regularized_test": regularized_metrics["test"], "improvement": baseline_metrics["test"] - regularized_metrics["test"]}]
    paired.extend({"seed": int(baseline["seed"]), "baseline_test": baseline["test"], "regularized_test": regularized["test"], "improvement": baseline["test"] - regularized["test"]} for baseline, regularized in zip(baseline_replicates, regularized_replicates))
    replicate_test = [float(item["test"]) for item in regularized_replicates]
    mean_replicate = sum(replicate_test) / len(replicate_test)
    variance = sum((value - mean_replicate) ** 2 for value in replicate_test) / len(replicate_test)
    paired_improvements = [float(item["improvement"]) for item in paired]
    write_dataset_artifact(args.evidence_dir)
    payload = {
        "schema_version": "1.0",
        "experiment_id": "LM_GENERALIZATION_V2",
        "generated_at": datetime.now(UTC).isoformat(),
        "status": "PRELIMINARY_RESEARCH_EVIDENCE",
        "research_question": "Does a fixed split and modest regularization improve held-out loss over the prior small scratch-LM training recipe without data leakage?",
        "falsification_conditions": [
            "regularized_primary.test_loss >= baseline.test_loss means the primary improvement hypothesis is not supported in this setup",
            "any paired seed improvement <= 0 means the replicated improvement hypothesis is not supported across this fixed seed set",
            "any duplicate normalized row across splits invalidates the split",
            "non-finite loss, missing optimizer updates, failed reload or parameter-independent inference invalidates the learned-model evidence",
            "a single synthetic corpus result cannot establish mature general-purpose language capability",
        ],
        "dataset_id": DATASET_ID,
        "dataset_sha256": dataset_digest(),
        "split": {key: len(value) for key, value in SPLIT.items()},
        "tokenizer_scope": "all synthetic text vocabulary only; no external/private text",
        "architecture": {"class": "Embedding-GRU-CausalLM", "embedding_dim": EMBEDDING_DIM, "hidden_dim": HIDDEN_DIM},
        "device": str(DEVICE),
        "precision": "float32",
        "models": {
            "baseline": {**baseline_metrics, "checkpoint": "LOCAL_ONLY:lm_generalization_baseline.pt", "checkpoint_sha256": sha256_file(baseline_path)},
            "regularized_primary": {**regularized_metrics, "checkpoint": "LOCAL_ONLY:lm_generalization_regularized_primary.pt", "checkpoint_sha256": sha256_file(regularized_path)},
        },
        "baseline_replicates": baseline_replicates,
        "regularized_replicates": regularized_replicates,
        "paired_seed_results": paired,
        "replicate_test_loss_mean": mean_replicate,
        "replicate_test_loss_std_population": variance**0.5,
        "paired_improvement_mean": sum(paired_improvements) / len(paired_improvements),
        "paired_improvement_min": min(paired_improvements),
        "primary_test_loss_improvement": float(baseline_metrics["test"] - regularized_metrics["test"]),
        "primary_improvement_supported": bool(primary_improvement),
        "paired_improvement_supported": bool(all(value > 0.0 for value in paired_improvements)),
        "conclusion": "PRELIMINARY_SUPPORT" if primary_improvement else "FALSIFIED_FOR_THIS_SETUP",
        "model_status": "OPTIONAL_RESEARCH_MODEL; NOT_ADDED_TO_FORMAL_MODEL_REGISTRY",
        "authority_boundary": "advisory research evidence only; cannot authorize, canonize, rewrite provenance, bypass privacy or establish subjectivity",
        "no_private_data": True,
        "no_external_paid_resource": True,
        "clean_process_validation_script": "research-labs/language-core-g1_v0.2.1/engineering/generalization/validate_lm_generalization_checkpoints.py",
    }
    (args.evidence_dir / "LM_GENERALIZATION_RESULTS.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"experiment_id": payload["experiment_id"], "baseline_test": baseline_metrics["test"], "regularized_test": regularized_metrics["test"], "primary_improvement_supported": primary_improvement, "models": 2}, sort_keys=True))


if __name__ == "__main__":
    main()
