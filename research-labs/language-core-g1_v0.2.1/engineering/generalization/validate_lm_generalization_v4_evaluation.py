import argparse
import json
import sys
from pathlib import Path

import torch

FORMAL_ROOT = Path(__file__).resolve().parents[4]
SRC = FORMAL_ROOT / "research-labs/language-core-g1_v0.2.1/engineering/real-model-candidate/src"
sys.path.insert(0, str(SRC))
from real_models import CausalLanguageModel, WordTokenizer, parameter_count  # noqa: E402

DEVICE = torch.device("cpu")


def load_model(path: Path) -> tuple[dict[str, object], WordTokenizer, CausalLanguageModel]:
    payload = torch.load(path, map_location=DEVICE, weights_only=False)
    tokenizer = WordTokenizer(payload["tokenizer"]["vocabulary"])
    config = payload["config"]
    model = CausalLanguageModel(config["vocabulary_size"], embedding_dim=config["embedding_dim"], hidden_dim=config["hidden_dim"]).to(DEVICE)
    model.load_state_dict(payload["state_dict"])
    model.eval()
    return payload, tokenizer, model


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models-dir", type=Path, required=True)
    parser.add_argument("--evidence-dir", type=Path, required=True)
    args = parser.parse_args()
    result = json.loads((args.evidence_dir / "LM_GENERALIZATION_V4_RESULTS.json").read_text(encoding="utf-8"))
    registry = json.loads((args.evidence_dir / "GENERALIZATION_PERTURBATION_V4_DATASET_REGISTRY.json").read_text(encoding="utf-8"))
    v3_registry = json.loads((args.evidence_dir.parent.parent / "generalization/evidence/GENERALIZATION_COMPOSITION_V3_DATASET_REGISTRY.json").read_text(encoding="utf-8"))
    v3_texts = {row["text"].strip().lower() for row in v3_registry["rows"]}
    v4_texts = [row["text"].strip().lower() for row in registry["rows"]]
    models = []
    for name in ("baseline", "regularized_primary"):
        metadata = result["models"][name]
        filename = metadata["checkpoint"].split(":", 1)[1]
        payload, tokenizer, model = load_model(args.models_dir / filename)
        prompt = torch.tensor([tokenizer.encode("source records preserve")], dtype=torch.long)
        with torch.no_grad():
            logits = model(prompt)
            original = {key: value.detach().clone() for key, value in model.state_dict().items()}
            learned = logits.clone()
            for parameter in model.parameters():
                parameter.zero_()
            zeroed = model(prompt).clone()
            model.load_state_dict(original)
        models.append(
            {
                "name": name,
                "checkpoint": metadata["checkpoint"],
                "checkpoint_exists": (args.models_dir / filename).is_file(),
                "dataset_id_matches": payload.get("dataset_id") == metadata["dataset_id"],
                "tokenizer_sha256_matches": tokenizer.sha256() == metadata["tokenizer_sha256"],
                "actual_inference": bool(logits.shape[0] == 1 and logits.shape[2] == model.config["vocabulary_size"]),
                "finite_parameters": bool(all(torch.isfinite(parameter).all() for parameter in model.parameters())),
                "parameter_count_matches": parameter_count(model) == metadata["parameter_count"],
                "parameter_dependent_inference": not torch.allclose(learned, zeroed),
            }
        )
    checks = {
        "row_count_matches": result["row_count"] == 20 and len(registry["rows"]) == 20,
        "exact_disjoint_rows": len(v4_texts) == len(set(v4_texts)) and not (set(v4_texts) & v3_texts),
        "v3_train_only_vocabulary": result["v3_train_only_vocabulary"] is True and result["oov_count"] == 0 and registry["oov_tokens"] == [],
        "condition_counts_match": result["condition_counts"] == {"cross_topic_composition": 10, "word_order_perturbation": 10},
        "model_checks_pass": all(all(value for key, value in model.items() if key not in {"name", "checkpoint"}) for model in models),
        "paired_improvement_contract": len(result["paired_loss_improvements_regularized_minus_baseline"]) == 20 and result["minimum_paired_improvement"] == min(result["paired_loss_improvements_regularized_minus_baseline"]),
        "no_private_data": result["no_private_data"] is True and result["no_private_intimate_data"] is True,
        "no_external_paid_resource": result["no_external_paid_resource"] is True,
        "no_new_model_added": result["model_registry_status"].startswith("OPTIONAL_RESEARCH_MODEL_INPUTS"),
    }
    output = {
        "schema_version": "1.0",
        "experiment_id": "LM_GENERALIZATION_V4",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "validated_in_clean_process": True,
        "device": str(DEVICE),
        "checks": checks,
        "models": models,
        "non_claim": "V4 held-out evaluation does not establish mature general-purpose language capability, identity, subjectivity or consciousness.",
    }
    (args.evidence_dir / "LM_GENERALIZATION_V4_VALIDATION.json").write_text(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"experiment_id": output["experiment_id"], "status": output["status"], "models": len(models)}, sort_keys=True))
    if output["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
