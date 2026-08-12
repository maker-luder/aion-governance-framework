from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

import torch

FORMAL_ROOT = Path(__file__).resolve().parents[4]
SRC = FORMAL_ROOT / "research-labs/language-core-g1_v0.2.1/engineering/real-model-candidate/src"
sys.path.insert(0, str(SRC))
from real_models import CausalLanguageModel, WordTokenizer, sha256_file  # noqa: E402


def load_tokenizer(payload: dict[str, object]) -> WordTokenizer:
    return WordTokenizer(dict(payload["tokenizer"]["vocabulary"]))


def validate_checkpoint(path: Path, *, expected_hash: str, prompt: str) -> dict[str, object]:
    actual_hash = sha256_file(path)
    payload = torch.load(path, map_location="cpu")
    tokenizer = load_tokenizer(payload)
    config = dict(payload["config"])
    model = CausalLanguageModel(config["vocabulary_size"], embedding_dim=config["embedding_dim"], hidden_dim=config["hidden_dim"])
    model.load_state_dict(payload["state_dict"])
    model.eval()
    token_ids = tokenizer.encode(prompt)
    unknown_ids = tokenizer.encode("unseen governance symbol")
    if len(token_ids) < 2 or len(unknown_ids) < 2:
        raise AssertionError("validation prompts must produce at least two tokens")
    prompt_tensor = torch.tensor([token_ids], dtype=torch.long)
    unknown_tensor = torch.tensor([unknown_ids], dtype=torch.long)
    with torch.no_grad():
        learned_output = model(prompt_tensor)
        unknown_output = model(unknown_tensor)
        generated = model.generate(prompt_tensor, max_new_tokens=3)
        original = {key: value.detach().clone() for key, value in model.state_dict().items()}
        for parameter in model.parameters():
            parameter.zero_()
        zeroed_output = model(prompt_tensor)
        model.load_state_dict(original)
    return {
        "checkpoint": str(path.name),
        "checkpoint_sha256": actual_hash,
        "expected_hash_matches": actual_hash == expected_hash,
        "clean_reload": True,
        "actual_inference": bool(learned_output.shape[-1] == config["vocabulary_size"]),
        "unknown_input_failure_mode": bool(torch.isfinite(unknown_output).all()),
        "generated_token_count": int(generated.shape[-1] - prompt_tensor.shape[-1]),
        "parameter_dependent_inference": bool(not torch.allclose(learned_output, zeroed_output)),
        "all_parameters_finite": bool(all(torch.isfinite(value).all() for value in model.parameters())),
        "training_status": payload.get("training_status"),
        "dataset_id": payload.get("dataset_id"),
        "tokenizer_sha256": payload.get("tokenizer_sha256"),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models-dir", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    evidence = json.loads(args.evidence.read_text(encoding="utf-8"))
    results = []
    for key, filename in [("baseline", "lm_generalization_baseline.pt"), ("regularized_primary", "lm_generalization_regularized_primary.pt")]:
        expected = evidence["models"][key]["checkpoint_sha256"]
        results.append(validate_checkpoint(args.models_dir / filename, expected_hash=expected, prompt="source records preserve"))
    checks = [
        all(item["expected_hash_matches"] for item in results),
        all(item["clean_reload"] for item in results),
        all(item["actual_inference"] for item in results),
        all(item["parameter_dependent_inference"] for item in results),
        all(item["unknown_input_failure_mode"] for item in results),
        all(item["all_parameters_finite"] for item in results),
        all(item["generated_token_count"] == 3 for item in results),
    ]
    payload = {
        "schema_version": "1.0",
        "validation_id": "LM_GENERALIZATION_CLEAN_RELOAD_V1",
        "generated_at": datetime.now(UTC).isoformat(),
        "evidence_subject": "LM_GENERALIZATION_V2",
        "checks": {
            "hashes_match": checks[0],
            "clean_reload": checks[1],
            "actual_inference": checks[2],
            "parameter_dependent_inference": checks[3],
            "unknown_input_failure_mode": checks[4],
            "finite_parameters": checks[5],
            "generation_length": checks[6],
        },
        "models": results,
        "status": "PASS" if all(checks) else "FAIL",
        "non_claim": "This clean reload validates learned-checkpoint behavior only; it does not establish mature general-purpose language capability.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "models": len(results)}, sort_keys=True))
    if payload["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
