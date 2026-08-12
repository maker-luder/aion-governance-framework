import argparse
import hashlib
import json
import sys
from pathlib import Path

import torch

FORMAL_ROOT = Path(__file__).resolve().parents[4]
SRC = FORMAL_ROOT / "research-labs/language-core-g1_v0.2.1/engineering/real-model-candidate/src"
sys.path.insert(0, str(SRC))
from real_models import CausalLanguageModel, WordTokenizer, parameter_count  # noqa: E402

DEVICE = torch.device("cpu")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_checkpoint(path: Path, expected_sha: str, dataset_id: str, prompt: str) -> dict[str, object]:
    payload = torch.load(path, map_location=DEVICE, weights_only=False)
    tokenizer = WordTokenizer(payload["tokenizer"]["vocabulary"])
    config = payload["config"]
    model = CausalLanguageModel(
        config["vocabulary_size"],
        embedding_dim=config["embedding_dim"],
        hidden_dim=config["hidden_dim"],
    ).to(DEVICE)
    model.load_state_dict(payload["state_dict"])
    model.eval()
    encoded = tokenizer.encode(prompt)
    if not encoded:
        raise AssertionError("prompt encoded to an empty sequence")
    input_ids = torch.tensor([encoded], dtype=torch.long)
    with torch.no_grad():
        logits = model(input_ids)
        generated = model.generate(input_ids, max_new_tokens=3)
        learned = logits.clone()
        original = {key: value.detach().clone() for key, value in model.state_dict().items()}
        for parameter in model.parameters():
            parameter.zero_()
        zeroed = model(input_ids).clone()
        model.load_state_dict(original)
    finite = all(bool(torch.isfinite(parameter).all()) for parameter in model.parameters())
    return {
        "checkpoint": f"LOCAL_ONLY:{path.name}",
        "sha256_matches": sha256_file(path) == expected_sha,
        "dataset_id_matches": payload.get("dataset_id") == dataset_id,
        "training_status": payload.get("training_status"),
        "experiment_role": payload.get("experiment_role"),
        "tokenizer_training_scope": payload.get("tokenizer_training_scope"),
        "actual_inference": tuple(logits.shape) == (1, len(encoded), config["vocabulary_size"]),
        "generation_length": int(generated.shape[1]) == len(encoded) + 3,
        "finite_parameters": finite,
        "parameter_count_matches": parameter_count(model) == sum(parameter.numel() for parameter in model.parameters()),
        "parameter_dependent_inference": not torch.allclose(learned, zeroed),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models-dir", type=Path, required=True)
    parser.add_argument("--evidence-dir", type=Path, required=True)
    args = parser.parse_args()
    result_evidence = json.loads((args.evidence_dir / "LM_GENERALIZATION_V3_RESULTS.json").read_text(encoding="utf-8"))
    dataset = json.loads((args.evidence_dir / "GENERALIZATION_COMPOSITION_V3_DATASET_REGISTRY.json").read_text(encoding="utf-8"))
    models = []
    for name, prompt in (("baseline", "traceable recall requires"), ("regularized_primary", "traceable recall requires")):
        model_meta = result_evidence["models"][name]
        filename = model_meta["checkpoint"].split(":", 1)[1]
        models.append(validate_checkpoint(args.models_dir / filename, model_meta["checkpoint_sha256"], result_evidence["dataset_id"], prompt))
    checks = {
        "dataset_status": dataset["synthetic_real_classification"] == "SYNTHETIC",
        "dataset_sha256_matches": dataset["dataset_sha256"] == result_evidence["dataset_sha256"],
        "train_only_tokenizer": dataset["tokenizer_scope"] == "train_only",
        "zero_unknown_validation_and_test": result_evidence["composition_test_contract"]["unknown_tokens_in_validation"] == 0 and result_evidence["composition_test_contract"]["unknown_tokens_in_test"] == 0,
        "all_models_valid": all(all(value for key, value in model.items() if key not in {"path", "training_status", "experiment_role", "tokenizer_training_scope"}) for model in models),
        "no_private_data": result_evidence["no_private_data"] is True,
        "no_external_paid_resource": result_evidence["no_external_paid_resource"] is True,
    }
    output = {
        "schema_version": "1.0",
        "experiment_id": "LM_GENERALIZATION_V3",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "validated_in_clean_process": True,
        "device": str(DEVICE),
        "checks": checks,
        "models": models,
        "non_claim": "Clean reload validates an optional local research checkpoint, not mature general-purpose capability or authority.",
    }
    (args.evidence_dir / "LM_GENERALIZATION_V3_VALIDATION.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"experiment_id": output["experiment_id"], "status": output["status"], "models": len(models)}, sort_keys=True))
    if output["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
