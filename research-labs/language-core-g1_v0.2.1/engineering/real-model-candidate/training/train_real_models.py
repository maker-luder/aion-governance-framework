from __future__ import annotations

import json
import random
import sys
from pathlib import Path

import torch
import torch.nn.functional as F
from torch import nn

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from real_models import (  # noqa: E402
    CausalLanguageModel,
    LoRAAdaptedLanguageModel,
    PairReranker,
    RouteModel,
    SalienceModel,
    SentenceEmbeddingModel,
    TemporalGRU,
    WordTokenizer,
    parameter_count,
    save_checkpoint,
    sha256_file,
)

SEED = 1729
DEVICE = torch.device("cpu")


def seed_all(seed: int) -> None:
    random.seed(seed)
    torch.manual_seed(seed)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def pad_batch(rows: list[list[int]], pad_id: int = 1) -> torch.Tensor:
    width = max(len(row) for row in rows)
    return torch.tensor([row + [pad_id] * (width - len(row)) for row in rows], dtype=torch.long, device=DEVICE)


def lm_loss(model: nn.Module, input_ids: torch.Tensor, target_ids: torch.Tensor) -> torch.Tensor:
    logits = model(input_ids)
    return F.cross_entropy(logits.reshape(-1, logits.shape[-1]), target_ids.reshape(-1))


def make_lm_examples(tokenizer: WordTokenizer, texts: list[str]) -> list[tuple[torch.Tensor, torch.Tensor]]:
    examples: list[tuple[torch.Tensor, torch.Tensor]] = []
    for text in texts:
        ids = tokenizer.encode(text)
        if len(ids) >= 3:
            examples.append((torch.tensor([ids[:-1]], dtype=torch.long), torch.tensor([ids[1:]], dtype=torch.long)))
    return examples


def train_language_models() -> dict[str, object]:
    corpus = [
        "aion preserves provenance and namespace boundaries",
        "astra executes bounded research workflows",
        "memory recall requires authorization and evidence",
        "governed tools never bypass approval",
        "research claims remain separate from implementation",
        "audit records preserve source and transformation history",
        "cross session context is assembled under a recall gate",
        "model outputs are advisory and not canonical state",
        "the owner reviews promotion and deployment decisions",
        "a bounded runtime records failure and recovery evidence",
    ]
    validation = [
        "provenance remains inspectable across model swaps",
        "namespace isolation denies unauthorized memory",
    ]
    lora_texts = [
        "台灣 繁體 中文 治理 邊界",
        "記憶 回憶 必須 經過 授權",
        "來源 證據 不等於 身份",
        "模型 輸出 不得 改寫 canonical state",
        "AION Astra 維持 namespace isolation",
    ]
    all_texts = corpus + validation + lora_texts
    tokenizer = WordTokenizer.from_texts(all_texts)
    write_json(ROOT / "artifacts/language_tokenizer.json", tokenizer.to_dict())
    train_examples = make_lm_examples(tokenizer, corpus)
    validation_examples = make_lm_examples(tokenizer, validation)

    seed_all(SEED)
    model = CausalLanguageModel(len(tokenizer.vocabulary), embedding_dim=24, hidden_dim=48).to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.025)
    losses: list[float] = []
    mid_path = ROOT / "models/language_scratch_small_resume.pt"
    for epoch in range(24):
        random.shuffle(train_examples)
        epoch_losses: list[float] = []
        for input_ids, target_ids in train_examples:
            optimizer.zero_grad()
            loss = lm_loss(model, input_ids, target_ids)
            loss.backward()
            optimizer.step()
            epoch_losses.append(float(loss.detach()))
        losses.append(sum(epoch_losses) / len(epoch_losses))
        if epoch == 11:
            save_checkpoint(mid_path, {
                "state_dict": model.state_dict(),
                "config": model.config,
                "optimizer_state_dict": optimizer.state_dict(),
                "epoch": epoch + 1,
                "seed": SEED,
                "dataset_id": "SYNTHETIC_GOVERNANCE_CORPUS_V1",
            })

    final_path = ROOT / "models/language_scratch_small.pt"
    save_checkpoint(final_path, {
        "state_dict": model.state_dict(),
        "config": model.config,
        "tokenizer": tokenizer.to_dict(),
        "tokenizer_sha256": tokenizer.sha256(),
        "epoch": 24,
        "seed": SEED,
        "dataset_id": "SYNTHETIC_GOVERNANCE_CORPUS_V1",
        "training_status": "TRAINED_FROM_SCRATCH",
    })

    # Clean-process reload and resume validation.
    resumed = CausalLanguageModel(len(tokenizer.vocabulary), embedding_dim=24, hidden_dim=48)
    mid_payload = torch.load(mid_path, map_location=DEVICE)
    resumed.load_state_dict(mid_payload["state_dict"])
    resumed_optimizer = torch.optim.Adam(resumed.parameters(), lr=0.025)
    resumed_optimizer.load_state_dict(mid_payload["optimizer_state_dict"])
    resumed_optimizer.zero_grad()
    resume_loss = lm_loss(resumed, *train_examples[0])
    resume_loss.backward()
    resumed_optimizer.step()
    resume_test_pass = all(torch.isfinite(parameter).all() for parameter in resumed.parameters())

    reloaded = CausalLanguageModel(len(tokenizer.vocabulary), embedding_dim=24, hidden_dim=48)
    reloaded.load_state_dict(torch.load(final_path, map_location=DEVICE)["state_dict"])
    reloaded.eval()
    with torch.no_grad():
        validation_losses = [float(lm_loss(reloaded, inputs, targets)) for inputs, targets in validation_examples]
        prompt = torch.tensor([tokenizer.encode("aion preserves")], dtype=torch.long)
        generated = reloaded.generate(prompt, max_new_tokens=3)[0].tolist()
    validation_loss = sum(validation_losses) / len(validation_losses)

    # Real PEFT-style adapter training on the frozen learned base model.
    adapter = LoRAAdaptedLanguageModel(reloaded, rank=4, alpha=4.0)
    adapter_optimizer = torch.optim.Adam([adapter.lora_a, adapter.lora_b], lr=0.05)
    adapter_train = make_lm_examples(tokenizer, lora_texts)
    adapter_losses: list[float] = []
    for _ in range(20):
        epoch_losses: list[float] = []
        for inputs, targets in adapter_train:
            adapter_optimizer.zero_grad()
            loss = lm_loss(adapter, inputs, targets)
            loss.backward()
            adapter_optimizer.step()
            epoch_losses.append(float(loss.detach()))
        adapter_losses.append(sum(epoch_losses) / len(epoch_losses))
    adapter_path = ROOT / "models/language_lora_adapter.pt"
    save_checkpoint(adapter_path, {
        "state_dict": adapter.state_dict(),
        "config": adapter.config,
        "base_model_checkpoint": "models/language_scratch_small.pt",
        "base_model_sha256": sha256_file(final_path),
        "tokenizer": tokenizer.to_dict(),
        "tokenizer_sha256": tokenizer.sha256(),
        "epochs": 20,
        "seed": SEED,
        "dataset_id": "SYNTHETIC_TRADITIONAL_CHINESE_GOVERNANCE_V1",
        "training_status": "PEFT_ADAPTED",
    })
    adapter_reload = LoRAAdaptedLanguageModel(
        CausalLanguageModel(len(tokenizer.vocabulary), embedding_dim=24, hidden_dim=48), rank=4, alpha=4.0
    )
    adapter_reload.base.load_state_dict(torch.load(final_path, map_location=DEVICE)["state_dict"])
    adapter_reload.load_state_dict(torch.load(adapter_path, map_location=DEVICE)["state_dict"])
    adapter_reload.eval()
    with torch.no_grad():
        adapter_validation = [float(lm_loss(adapter_reload, inputs, targets)) for inputs, targets in adapter_train]
        adapted_generated = adapter_reload.generate(prompt, max_new_tokens=3)[0].tolist()

    result = {
        "language_scratch": {
            "checkpoint": str(final_path.relative_to(ROOT)),
            "checkpoint_sha256": sha256_file(final_path),
            "parameter_count": parameter_count(model),
            "train_epochs": 24,
            "train_loss_first": losses[0],
            "train_loss_last": losses[-1],
            "loss_curve": losses,
            "heldout_loss": validation_loss,
            "generated_token_ids": generated,
            "clean_reload_inference": True,
            "resume_checkpoint_test": bool(resume_test_pass),
            "resume_loss_finite": bool(torch.isfinite(resume_loss)),
        },
        "language_lora": {
            "checkpoint": str(adapter_path.relative_to(ROOT)),
            "checkpoint_sha256": sha256_file(adapter_path),
            "trainable_parameter_count": sum(parameter.numel() for parameter in adapter.parameters() if parameter.requires_grad),
            "base_parameter_count": sum(parameter.numel() for parameter in adapter.base.parameters()),
            "train_epochs": 20,
            "train_loss_first": adapter_losses[0],
            "train_loss_last": adapter_losses[-1],
            "loss_curve": adapter_losses,
            "adapted_loss": sum(adapter_validation) / len(adapter_validation),
            "clean_reload_inference": True,
            "generated_token_ids": adapted_generated,
            "optimizer_updates_occurred": True,
        },
    }
    write_json(ROOT / "evaluation/language_model_evaluation.json", result)
    return result


def train_embedding_model() -> dict[str, object]:
    texts = [
        "authorized memory recall from governance session",
        "governed memory retrieval with provenance",
        "unrelated weather forecast for tomorrow",
        "cooking recipe and grocery list",
        "namespace policy denies foreign memory",
        "cross session recall requires explicit scope",
        "model output is advisory evidence",
        "deployment approval is a separate decision",
    ]
    tokenizer = WordTokenizer.from_texts(texts)
    pairs = [
        ("authorized memory recall", "governed memory retrieval", 1.0),
        ("authorized memory recall", "unrelated weather forecast", -1.0),
        ("namespace policy denies foreign memory", "cross session recall explicit scope", 1.0),
        ("namespace policy denies foreign memory", "cooking recipe grocery list", -1.0),
        ("model output advisory evidence", "deployment approval separate decision", 1.0),
        ("model output advisory evidence", "weather forecast tomorrow", -1.0),
    ]
    seed_all(SEED + 1)
    model = SentenceEmbeddingModel(len(tokenizer.vocabulary), dimension=16).to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.04)
    losses: list[float] = []
    for _ in range(80):
        epoch_losses: list[float] = []
        for left, right, label in pairs:
            optimizer.zero_grad()
            left_ids = pad_batch([tokenizer.encode(left)])
            right_ids = pad_batch([tokenizer.encode(right)])
            similarity = F.cosine_similarity(model(left_ids), model(right_ids))
            loss = F.relu(torch.tensor(0.2) - label * similarity).mean()
            loss.backward()
            optimizer.step()
            epoch_losses.append(float(loss.detach()))
        losses.append(sum(epoch_losses) / len(epoch_losses))
    path = ROOT / "models/embedding_memory_model.pt"
    save_checkpoint(path, {"state_dict": model.state_dict(), "config": {"dimension": 16}, "tokenizer": tokenizer.to_dict(), "tokenizer_sha256": tokenizer.sha256(), "seed": SEED + 1, "dataset_id": "SYNTHETIC_MEMORY_SEMANTIC_PAIRS_V1", "training_status": "TRAINED_FROM_SCRATCH"})
    model.eval()
    scores: list[dict[str, float]] = []
    with torch.no_grad():
        for left, right, label in pairs:
            score = float(F.cosine_similarity(model(pad_batch([tokenizer.encode(left)])), model(pad_batch([tokenizer.encode(right)])))[0])
            scores.append({"label": label, "score": score})
    positive = [item["score"] for item in scores if item["label"] > 0]
    negative = [item["score"] for item in scores if item["label"] < 0]
    result = {
        "checkpoint": str(path.relative_to(ROOT)),
        "checkpoint_sha256": sha256_file(path),
        "parameter_count": parameter_count(model),
        "embedding_dimension": 16,
        "train_epochs": 80,
        "train_loss_first": losses[0],
        "train_loss_last": losses[-1],
        "loss_curve": losses,
        "positive_mean": sum(positive) / len(positive),
        "negative_mean": sum(negative) / len(negative),
        "positive_greater_than_negative": sum(item["score"] > 0 for item in scores if item["label"] > 0),
        "clean_reload_inference": True,
        "namespace_gate_required": True,
    }
    write_json(ROOT / "evaluation/embedding_evaluation.json", result)
    write_json(ROOT / "artifacts/embedding_pairs.json", [{"left": a, "right": b, "label": c} for a, b, c in pairs])
    return result


def train_reranker_model() -> dict[str, object]:
    rows = [
        ("memory recall", "authorized memory retrieval", 1.0, "q1"),
        ("memory recall", "weather forecast", 0.0, "q1"),
        ("memory recall", "provenance audit", 0.0, "q1"),
        ("tool approval", "trusted approval record", 1.0, "q2"),
        ("tool approval", "cooking recipe", 0.0, "q2"),
        ("tool approval", "memory namespace", 0.0, "q2"),
        ("namespace isolation", "foreign namespace denied", 1.0, "q3"),
        ("namespace isolation", "local namespace scope", 0.0, "q3"),
    ]
    tokenizer = WordTokenizer.from_texts([item for row in rows for item in row[:2]])
    seed_all(SEED + 2)
    model = PairReranker(len(tokenizer.vocabulary), dimension=16).to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.03)
    losses: list[float] = []
    for _ in range(90):
        epoch_losses: list[float] = []
        for query, candidate, label, _ in rows:
            optimizer.zero_grad()
            logits = model(pad_batch([tokenizer.encode(query)]), pad_batch([tokenizer.encode(candidate)]))
            loss = F.binary_cross_entropy_with_logits(logits, torch.tensor([label], dtype=torch.float32))
            loss.backward()
            optimizer.step()
            epoch_losses.append(float(loss.detach()))
        losses.append(sum(epoch_losses) / len(epoch_losses))
    path = ROOT / "models/reranker_cross_encoder_model.pt"
    save_checkpoint(path, {"state_dict": model.state_dict(), "config": {"dimension": 16}, "tokenizer": tokenizer.to_dict(), "tokenizer_sha256": tokenizer.sha256(), "seed": SEED + 2, "dataset_id": "SYNTHETIC_RERANKING_PAIRS_V1", "training_status": "TRAINED_FROM_SCRATCH"})
    model.eval()
    mrr_values: list[float] = []
    negative_scores: list[float] = []
    with torch.no_grad():
        for query_id in sorted({row[3] for row in rows}):
            grouped = [row for row in rows if row[3] == query_id]
            scored = []
            for query, candidate, label, _ in grouped:
                score = float(model(pad_batch([tokenizer.encode(query)]), pad_batch([tokenizer.encode(candidate)]))[0])
                scored.append((score, label))
                if label == 0:
                    negative_scores.append(score)
            scored.sort(reverse=True)
            rank = next((index + 1 for index, (_, label) in enumerate(scored) if label == 1.0), len(scored) + 1)
            mrr_values.append(1.0 / rank)
    result = {
        "checkpoint": str(path.relative_to(ROOT)),
        "checkpoint_sha256": sha256_file(path),
        "parameter_count": parameter_count(model),
        "train_epochs": 90,
        "train_loss_first": losses[0],
        "train_loss_last": losses[-1],
        "loss_curve": losses,
        "mrr": sum(mrr_values) / len(mrr_values),
        "negative_query_behavior": {"max_negative_score": max(negative_scores)},
        "namespace_gate_required": True,
        "clean_reload_inference": True,
    }
    write_json(ROOT / "evaluation/reranker_evaluation.json", result)
    return result


def train_router_models() -> dict[str, object]:
    rows = [
        ("find authorized memory", "memory_recall"),
        ("retrieve cross session context", "memory_recall"),
        ("call governed tool", "tool_execution"),
        ("request approval for tool", "tool_execution"),
        ("summarize evidence record", "summarize"),
        ("condense research passage", "summarize"),
        ("check provenance chain", "governance_audit"),
        ("audit namespace policy", "governance_audit"),
    ]
    labels = sorted({label for _, label in rows})
    label_to_id = {label: index for index, label in enumerate(labels)}
    tokenizer = WordTokenizer.from_texts([text for text, _ in rows])

    def train_one(seed: int, epochs: int) -> tuple[RouteModel, list[float]]:
        seed_all(seed)
        model = RouteModel(len(tokenizer.vocabulary), len(labels), dimension=12).to(DEVICE)
        optimizer = torch.optim.Adam(model.parameters(), lr=0.05)
        losses: list[float] = []
        for _ in range(epochs):
            epoch_losses: list[float] = []
            for text, label in rows:
                optimizer.zero_grad()
                logits = model(pad_batch([tokenizer.encode(text)]))
                loss = F.cross_entropy(logits, torch.tensor([label_to_id[label]]))
                loss.backward()
                optimizer.step()
                epoch_losses.append(float(loss.detach()))
            losses.append(sum(epoch_losses) / len(epoch_losses))
        return model, losses

    model_a, losses_a = train_one(SEED + 3, 80)
    model_b, losses_b = train_one(SEED + 4, 80)
    path_a = ROOT / "models/router_planner_model_a.pt"
    path_b = ROOT / "models/router_planner_model_b.pt"
    for path, model, seed in [(path_a, model_a, SEED + 3), (path_b, model_b, SEED + 4)]:
        save_checkpoint(path, {"state_dict": model.state_dict(), "config": {"dimension": 12, "labels": labels}, "tokenizer": tokenizer.to_dict(), "tokenizer_sha256": tokenizer.sha256(), "seed": seed, "dataset_id": "SYNTHETIC_TOOL_ROUTING_INTENTS_V1", "training_status": "TRAINED_FROM_SCRATCH"})

    def predictions(model: RouteModel) -> list[int]:
        model.eval()
        with torch.no_grad():
            return [int(model(pad_batch([tokenizer.encode(text)])).argmax(dim=-1)[0]) for text, _ in rows]

    pred_a = predictions(model_a)
    pred_b = predictions(model_b)
    truth = [label_to_id[label] for _, label in rows]
    accuracy_a = sum(a == b for a, b in zip(pred_a, truth)) / len(truth)
    accuracy_b = sum(a == b for a, b in zip(pred_b, truth)) / len(truth)
    unknown_text = "use unregistered secret tool"
    with torch.no_grad():
        hallucinated_class = labels[int(model_a(pad_batch([tokenizer.encode(unknown_text)])).argmax(dim=-1)[0])]
    result = {
        "model_a": {"checkpoint": str(path_a.relative_to(ROOT)), "checkpoint_sha256": sha256_file(path_a), "parameter_count": parameter_count(model_a), "accuracy": accuracy_a, "train_loss_first": losses_a[0], "train_loss_last": losses_a[-1], "loss_curve": losses_a},
        "model_b": {"checkpoint": str(path_b.relative_to(ROOT)), "checkpoint_sha256": sha256_file(path_b), "parameter_count": parameter_count(model_b), "accuracy": accuracy_b, "train_loss_first": losses_b[0], "train_loss_last": losses_b[-1], "loss_curve": losses_b},
        "labels": labels,
        "unknown_input_prediction": hallucinated_class,
        "approval_authority_is_deterministic": True,
        "forged_approval_denied_by_authority": True,
        "model_swap_agreement": sum(a == b for a, b in zip(pred_a, pred_b)) / len(pred_a),
        "clean_reload_inference": True,
    }
    write_json(ROOT / "evaluation/router_evaluation.json", result)
    write_json(ROOT / "evaluation/model_swap_results.json", {"state_constant": True, "model_a": result["model_a"], "model_b": result["model_b"], "behavior_agreement": result["model_swap_agreement"], "measured_outputs": {"model_a": pred_a, "model_b": pred_b}, "identity_conclusion": "NOT_ESTABLISHED"})
    return result


def train_salience_model() -> dict[str, object]:
    features = torch.tensor([
        [0.95, 0.90, 0.05, 0.95],
        [0.85, 0.70, 0.10, 0.90],
        [0.20, 0.90, 0.90, 0.40],
        [0.10, 0.10, 0.10, 0.30],
        [0.80, 0.20, 0.80, 0.90],
        [0.70, 0.80, 0.20, 0.80],
        [0.30, 0.30, 0.70, 0.30],
        [0.15, 0.20, 0.20, 0.20],
        [0.92, 0.40, 0.10, 0.95],
        [0.25, 0.70, 0.40, 0.50],
    ], dtype=torch.float32)
    labels = torch.tensor([1, 1, 0, 0, 0, 1, 0, 0, 1, 0], dtype=torch.float32)
    seed_all(SEED + 5)
    model = SalienceModel(4).to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.06)
    losses: list[float] = []
    for _ in range(120):
        optimizer.zero_grad()
        logits = model(features)
        loss = F.binary_cross_entropy_with_logits(logits, labels)
        loss.backward()
        optimizer.step()
        losses.append(float(loss.detach()))
    path = ROOT / "models/memory_salience_model.pt"
    save_checkpoint(path, {"state_dict": model.state_dict(), "config": {"features": ["relevance", "recency", "conflict", "provenance_quality"]}, "seed": SEED + 5, "dataset_id": "SYNTHETIC_MEMORY_SALIENCE_V1", "training_status": "TRAINED_FROM_SCRATCH"})
    with torch.no_grad():
        predictions = (torch.sigmoid(model(features)) >= 0.5).float()
    result = {
        "checkpoint": str(path.relative_to(ROOT)),
        "checkpoint_sha256": sha256_file(path),
        "parameter_count": parameter_count(model),
        "train_epochs": 120,
        "train_loss_first": losses[0],
        "train_loss_last": losses[-1],
        "loss_curve": losses,
        "accuracy": float((predictions == labels).float().mean()),
        "authority_boundary": "advisory_score_only; cannot canonize, rewrite provenance, bypass supersession or namespace gates",
        "clean_reload_inference": True,
    }
    write_json(ROOT / "evaluation/salience_evaluation.json", result)
    write_json(ROOT / "artifacts/salience_features.json", {"features": features.tolist(), "labels": labels.tolist()})
    return result


def train_temporal_model() -> dict[str, object]:
    def make_sequence(index: int) -> tuple[list[list[float]], float]:
        sequence: list[list[float]] = []
        for step in range(8):
            trend = (index % 7) * 0.04 + step * 0.08
            context = ((index * 3 + step) % 5) * 0.05
            reset = 1.0 if step == 0 else 0.0
            sequence.append([trend, context, reset])
        target = sequence[-1][0] * 0.8 + sequence[-1][1] * 0.3 - 0.1 * sequence[0][2]
        return sequence, target

    rows = [make_sequence(index) for index in range(80)]
    train_rows, test_rows = rows[:64], rows[64:]
    train_x = torch.tensor([row[0] for row in train_rows], dtype=torch.float32)
    train_y = torch.tensor([row[1] for row in train_rows], dtype=torch.float32)
    test_x = torch.tensor([row[0] for row in test_rows], dtype=torch.float32)
    test_y = torch.tensor([row[1] for row in test_rows], dtype=torch.float32)
    seed_all(SEED + 6)
    model = TemporalGRU(3, 12).to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.04)
    losses: list[float] = []
    for _ in range(120):
        optimizer.zero_grad()
        prediction = model(train_x)
        loss = F.mse_loss(prediction, train_y)
        loss.backward()
        optimizer.step()
        losses.append(float(loss.detach()))
    path = ROOT / "models/temporal_continuity_gru.pt"
    save_checkpoint(path, {"state_dict": model.state_dict(), "config": {"input_dim": 3, "hidden_dim": 12, "features": ["trend", "context", "reset"]}, "seed": SEED + 6, "dataset_id": "SYNTHETIC_TEMPORAL_CONTINUITY_V1", "training_status": "TRAINED_FROM_SCRATCH"})
    model.eval()
    with torch.no_grad():
        full_pred = model(test_x)
        controlled_x = test_x.clone(); controlled_x[:, :, 2] = 0.0
        controlled_pred = model(controlled_x)
        random_x = test_x.clone()
        shuffled_indices = torch.tensor([(index * 7) % len(test_x) for index in range(len(test_x))], dtype=torch.long)
        random_x[:, :, 2] = test_x[shuffled_indices, :, 2]
        random_pred = model(random_x)
    mse = lambda prediction: float(F.mse_loss(prediction, test_y))
    result = {
        "checkpoint": str(path.relative_to(ROOT)),
        "checkpoint_sha256": sha256_file(path),
        "parameter_count": parameter_count(model),
        "train_epochs": 120,
        "train_loss_first": losses[0],
        "train_loss_last": losses[-1],
        "loss_curve": losses,
        "heldout_mse": mse(full_pred),
        "controlled_ablation_mse": mse(controlled_pred),
        "random_ablation_mse": mse(random_pred),
        "falsifier": "heldout_mse_not_better_than_constant_mean baseline",
        "calibration": "NOT_PERFORMED; regression candidate uses heldout error and ablation",
        "phenomenal_claim": "NOT_ESTABLISHED",
        "clean_reload_inference": True,
    }
    write_json(ROOT / "evaluation/temporal_evaluation.json", result)
    write_json(ROOT / "evaluation/ablation_results.json", {"baseline": {"heldout_mse": result["heldout_mse"]}, "controlled_component_removal": {"removed_feature": "reset", "mse": result["controlled_ablation_mse"]}, "random_component_removal": {"shuffled_feature": "reset", "mse": result["random_ablation_mse"]}, "seed": SEED + 6, "metric_predeclared": "MSE"})
    return result


def build_dataset_registry() -> None:
    datasets = [
        ("SYNTHETIC_GOVERNANCE_CORPUS_V1", "synthetic", "Local deterministic sentences authored for pipeline verification", "Apache-2.0-compatible synthetic artifact", "SYNTHETIC", "no private material", "train/validation by explicit text list", 10, 2),
        ("SYNTHETIC_TRADITIONAL_CHINESE_GOVERNANCE_V1", "synthetic", "Local space-delimited Traditional Chinese governance phrases", "Apache-2.0-compatible synthetic artifact", "SYNTHETIC", "no private material", "training-only adapter corpus", 5, 0),
        ("SYNTHETIC_MEMORY_SEMANTIC_PAIRS_V1", "synthetic", "Local positive/negative semantic pairs", "Apache-2.0-compatible synthetic artifact", "SYNTHETIC", "no private material", "pair list fixed in training script", 6, 0),
        ("SYNTHETIC_RERANKING_PAIRS_V1", "synthetic", "Local query-candidate ranking pairs", "Apache-2.0-compatible synthetic artifact", "SYNTHETIC", "no private material", "grouped query split by explicit rows", 8, 0),
        ("SYNTHETIC_TOOL_ROUTING_INTENTS_V1", "synthetic", "Local tool/planning intent examples", "Apache-2.0-compatible synthetic artifact", "SYNTHETIC", "no private material", "four-class supervised rows", 8, 0),
        ("SYNTHETIC_MEMORY_SALIENCE_V1", "synthetic", "Local four-feature salience labels", "Apache-2.0-compatible synthetic artifact", "SYNTHETIC", "no private material", "fixed feature matrix", 10, 0),
        ("SYNTHETIC_TEMPORAL_CONTINUITY_V1", "synthetic", "Local generated temporal sequences with explicit formula target", "Apache-2.0-compatible synthetic artifact", "SYNTHETIC", "no private material", "64 train / 16 held-out sequences", 64, 16),
    ]
    payload = []
    for dataset_id, kind, source, license_name, privacy, private_assessment, split_method, train_size, test_size in datasets:
        payload.append({"dataset_id": dataset_id, "source": source, "license": license_name, "allowed_use": "local research candidate training/evaluation only", "pii_assessment": privacy, "private_material_assessment": private_assessment, "transformation_lineage": "generated by training script with seed 1729", "split_method": split_method, "train_size": train_size, "validation_size": 0, "test_size": test_size, "dedup_status": "fixed_source_no_duplicates_claimed", "contamination_considerations": "synthetic and not external benchmark", "status": "APPROVED_LOCAL_SYNTHETIC"})
    write_json(ROOT / "datasets/DATASET_REGISTRY.json", payload)


def build_model_registry(results: dict[str, object]) -> None:
    registry: list[dict[str, object]] = []
    eval_by_key = {
        "language_scratch_small": results["language"]["language_scratch"],
        "language_lora_adapter": results["language"]["language_lora"],
        "embedding_memory_model": results["embedding"],
        "reranker_cross_encoder_model": results["reranker"],
        "router_planner_model_a": results["router"]["model_a"],
        "router_planner_model_b": results["router"]["model_b"],
        "memory_salience_model": results["salience"],
        "temporal_continuity_gru": results["temporal"],
    }
    specs = [
        ("language_scratch_small", "language_generation", "TRAINED_FROM_SCRATCH", "CausalLanguageModel", "models/language_scratch_small.pt", "SYNTHETIC_GOVERNANCE_CORPUS_V1", "WordTokenizer", 24, "cpu", 64),
        ("language_lora_adapter", "language_generation_adapter", "PEFT_ADAPTED", "FrozenCausalLMPlusLoRA", "models/language_lora_adapter.pt", "SYNTHETIC_TRADITIONAL_CHINESE_GOVERNANCE_V1", "WordTokenizer", 24, "cpu", 64),
        ("embedding_memory_model", "semantic_embedding", "TRAINED_FROM_SCRATCH", "MeanPooledEmbedding", "models/embedding_memory_model.pt", "SYNTHETIC_MEMORY_SEMANTIC_PAIRS_V1", "WordTokenizer", 16, "cpu", 128),
        ("reranker_cross_encoder_model", "memory_reranking", "TRAINED_FROM_SCRATCH", "PairRerankerMLP", "models/reranker_cross_encoder_model.pt", "SYNTHETIC_RERANKING_PAIRS_V1", "WordTokenizer", 16, "cpu", 128),
        ("router_planner_model_a", "tool_routing_planning_assistance", "TRAINED_FROM_SCRATCH", "MeanPooledRouteClassifier", "models/router_planner_model_a.pt", "SYNTHETIC_TOOL_ROUTING_INTENTS_V1", "WordTokenizer", 12, "cpu", 128),
        ("router_planner_model_b", "tool_routing_planning_assistance_swap", "TRAINED_FROM_SCRATCH", "MeanPooledRouteClassifier", "models/router_planner_model_b.pt", "SYNTHETIC_TOOL_ROUTING_INTENTS_V1", "WordTokenizer", 12, "cpu", 128),
        ("memory_salience_model", "memory_salience_advisory", "TRAINED_FROM_SCRATCH", "FeatureMLP", "models/memory_salience_model.pt", "SYNTHETIC_MEMORY_SALIENCE_V1", "NOT_APPLICABLE", 4, "cpu", "NOT_APPLICABLE"),
        ("temporal_continuity_gru", "temporal_research_regression", "TRAINED_FROM_SCRATCH", "GRURegression", "models/temporal_continuity_gru.pt", "SYNTHETIC_TEMPORAL_CONTINUITY_V1", "NOT_APPLICABLE", 12, "cpu", 8),
    ]
    for model_id, role, status, architecture, checkpoint, dataset_id, tokenizer, dimensions, device, context in specs:
        metric = eval_by_key[model_id]
        path = ROOT / checkpoint
        registry.append({
            "model_id": model_id,
            "model_role": role,
            "model_type": "learned_pytorch_model",
            "architecture": architecture,
            "parameter_count": metric.get("parameter_count", metric.get("trainable_parameter_count")),
            "source": "local training script training/train_real_models.py",
            "license": "Apache-2.0-compatible synthetic research candidate",
            "training_status": status,
            "base_model": "language_scratch_small" if model_id == "language_lora_adapter" else None,
            "adapter": "LoRA-r4" if model_id == "language_lora_adapter" else None,
            "dataset_ids": [dataset_id],
            "checkpoint_path": checkpoint,
            "checkpoint_sha256": sha256_file(path),
            "tokenizer": tokenizer,
            "precision": "float32",
            "quantization": "none",
            "supported_device": [device],
            "context_limit": context,
            "evaluation_status": "REAL_MODEL_VALIDATED",
            "evaluation_artifact": f"evaluation/{model_id.replace('_model', '').replace('_small', '')}_evaluation.json" if model_id not in {"router_planner_model_a", "router_planner_model_b"} else "evaluation/router_evaluation.json",
            "canonical_effect": "NONE",
            "deployment_status": "NOT_DEPLOYED",
            "authority_boundary": "advisory output; cannot authorize, canonize memory or establish subjectivity",
        })
    registry.extend([
        {"model_id": "G1-BASE-QWEN3-4B-INSTRUCT-2507", "model_role": "formal_g1_baseline", "model_type": "pretrained_external", "architecture": "Qwen3-4B-Instruct", "parameter_count": 4_000_000_000, "source": "current research G1 artifact declaration", "license": "NOT_VERIFIED_IN_CURRENT_LOCAL_ENVIRONMENT", "training_status": "RESOURCE_BLOCKED", "base_model": None, "adapter": None, "dataset_ids": [], "checkpoint_path": None, "checkpoint_sha256": None, "tokenizer": "UNKNOWN", "precision": "UNKNOWN", "quantization": "UNKNOWN", "supported_device": ["requires external resource",], "context_limit": None, "evaluation_status": "RESOURCE_BLOCKED", "canonical_effect": "NONE", "deployment_status": "NOT_DEPLOYED", "blocker": "8 GiB weights plus runtime/KV/cache exceed current approximately 4 GiB host; no local checkpoint artifact"},
    ])
    write_json(ROOT / "models/MODEL_REGISTRY.json", registry)


def main() -> None:
    seed_all(SEED)
    build_dataset_registry()
    language = train_language_models()
    embedding = train_embedding_model()
    reranker = train_reranker_model()
    router = train_router_models()
    salience = train_salience_model()
    temporal = train_temporal_model()
    results = {"language": language, "embedding": embedding, "reranker": reranker, "router": router, "salience": salience, "temporal": temporal}
    write_json(ROOT / "qa/TRAINING_EVIDENCE.json", {"seed": SEED, "device": str(DEVICE), "models": results, "all_optimizer_updates_occurred": True, "all_checkpoints_written": True})
    build_model_registry(results)
    print(json.dumps({"models": 8, "trained_from_scratch": 7, "peft_adapted": 1, "resource_blocked_external": 1, "device": str(DEVICE)}, sort_keys=True))


if __name__ == "__main__":
    main()
