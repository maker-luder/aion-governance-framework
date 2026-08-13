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


def load_checkpoint(path: Path) -> tuple[dict[str, object], WordTokenizer, CausalLanguageModel]:
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
    return payload, tokenizer, model


def validate_model(path: Path, expected_checkpoint: str, expected_tokenizer_sha: str, expected_dataset_id: str) -> dict[str, object]:
    payload, tokenizer, model = load_checkpoint(path)
    prompt = torch.tensor([tokenizer.encode("governed recall checks")], dtype=torch.long, device=DEVICE)
    with torch.no_grad():
        logits = model(prompt)
        generated = model.generate(prompt, max_new_tokens=2)
        original = {key: value.detach().clone() for key, value in model.state_dict().items()}
        learned = logits.clone()
        for parameter in model.parameters():
            parameter.zero_()
        zeroed = model(prompt).clone()
        model.load_state_dict(original)
    return {
        "checkpoint": expected_checkpoint,
        "checkpoint_exists": path.is_file(),
        "dataset_id_matches": payload.get("dataset_id") == expected_dataset_id,
        "tokenizer_sha256_matches": tokenizer.sha256() == expected_tokenizer_sha,
        "training_status": payload.get("training_status"),
        "experiment_role": payload.get("experiment_role"),
        "actual_inference": bool(logits.shape[0] == 1 and logits.shape[2] == model.config["vocabulary_size"]),
        "generation_length": int(generated.shape[1]) == int(prompt.shape[1]) + 2,
        "finite_parameters": bool(all(torch.isfinite(parameter).all() for parameter in model.parameters())),
        "parameter_count": parameter_count(model),
        "parameter_dependent_inference": not torch.allclose(learned, zeroed),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models-dir", type=Path, required=True)
    parser.add_argument("--evidence-dir", type=Path, required=True)
    args = parser.parse_args()
    result = json.loads((args.evidence_dir / "MODEL_SWAP_CONTINUITY_RESULTS.json").read_text(encoding="utf-8"))
    registry = json.loads((args.evidence_dir / "MODEL_SWAP_GOVERNANCE_STATE_REGISTRY.json").read_text(encoding="utf-8"))
    model_checks = []
    for name in ("baseline", "regularized_primary"):
        metadata = result["models"][name]
        filename = metadata["checkpoint"].split(":", 1)[1]
        model_checks.append(validate_model(args.models_dir / filename, metadata["checkpoint"], metadata["tokenizer_sha256"], result["models"][name]["dataset_id"]))
    row_contracts = result["per_state_results"]
    checks = {
        "registry_dataset_matches": registry["dataset_id"] == result["dataset_id"],
        "registry_state_digest_matches": registry["state_digest"] == result["state_digest"],
        "constant_state_digest": result["state_digest_identical_across_model_runs"] is True and all(row["state_digest"] == result["state_digest"] for row in row_contracts),
        "gate_before_score": result["gate_before_score"] is True,
        "admitted_rows_scored": result["admitted_rows_scored"] == len(registry["admitted_rows"]),
        "rejected_rows_not_scored": result["rejected_rows_scored"] == 0 and result["rejected_score_fields_absent"] is True,
        "model_checks_pass": all(all(value for key, value in model.items() if key not in {"checkpoint", "training_status", "experiment_role", "parameter_count"}) for model in model_checks),
        "no_private_data": result["no_private_data"] is True and result["no_private_intimate_data"] is True,
        "no_external_paid_resource": result["no_external_paid_resource"] is True,
        "no_new_model_added": result["model_registry_status"].startswith("OPTIONAL_RESEARCH_MODEL_INPUTS"),
    }
    output = {
        "schema_version": "1.0",
        "experiment_id": "MODEL_SWAP_CONTINUITY_V1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "validated_in_clean_process": True,
        "device": str(DEVICE),
        "checks": checks,
        "models": model_checks,
        "non_claim": "A fixed-state model swap measurement does not establish identity, subjectivity, consciousness or phenomenal continuity.",
    }
    (args.evidence_dir / "MODEL_SWAP_CONTINUITY_VALIDATION.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"experiment_id": output["experiment_id"], "status": output["status"], "models": len(model_checks)}, sort_keys=True))
    if output["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
