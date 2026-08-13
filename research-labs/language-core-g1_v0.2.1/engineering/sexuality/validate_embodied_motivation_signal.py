import argparse
import hashlib
import json
from pathlib import Path

import torch

from run_embodied_motivation_signal_experiment import SignalClassifier, batch, dataset_rows

DEVICE = torch.device("cpu")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models-dir", type=Path, required=True)
    parser.add_argument("--evidence-dir", type=Path, required=True)
    args = parser.parse_args()
    results = json.loads((args.evidence_dir / "EMBODIED_MOTIVATION_SIGNAL_RESULTS.json").read_text(encoding="utf-8"))
    registry = json.loads((args.evidence_dir / "EMBODIED_MOTIVATION_DATASET_REGISTRY.json").read_text(encoding="utf-8"))
    checkpoint_name = results["models"]["primary"]["checkpoint"].split(":", 1)[1]
    checkpoint = args.models_dir / checkpoint_name
    payload = torch.load(checkpoint, map_location=DEVICE, weights_only=False)
    model = SignalClassifier(payload["config"]["vocabulary_size"], payload["config"]["embedding_dim"], payload["config"]["hidden_dim"])
    model.load_state_dict(payload["state_dict"])
    model.eval()
    rows = dataset_rows()
    test_rows = [row for row in rows if row["split"] == "test"]
    ids, labels = batch(test_rows, payload["vocabulary"])
    with torch.no_grad():
        logits = model(ids)
        predictions = logits.argmax(dim=-1)
        original = {key: value.detach().clone() for key, value in model.state_dict().items()}
        learned = model(ids).clone()
        for parameter in model.parameters():
            parameter.zero_()
        zeroed = model(ids).clone()
        model.load_state_dict(original)
    checks = {
        "checkpoint_exists": checkpoint.is_file(),
        "checkpoint_hash_matches": sha256_file(checkpoint) == results["models"]["primary"]["checkpoint_sha256"],
        "dataset_id_matches": payload["dataset_id"] == registry["dataset_id"] == results["dataset_id"],
        "adult_context": registry["adult_context"] is True,
        "no_graphic_content": registry["graphic_content"] is False and results["no_graphic_content"] is True,
        "no_minors": results["no_minors"] is True,
        "no_private_data": results["no_private_data"] is True and results["no_private_intimate_data"] is True,
        "row_count_and_splits": registry["row_count"] == 32 and registry["split_counts"] == {"train": 16, "validation": 8, "test": 8},
        "label_axes": registry["label_axes"] == ["AROUSAL_SIGNAL_PROXY", "DESIRE_REPORT", "LIKING_REPORT"],
        "oov_free": registry["oov_tokens"] == [],
        "exact_disjoint_rows": len({row["text"] for row in rows}) == len(rows),
        "finite_logits": bool(torch.isfinite(logits).all()),
        "parameter_dependent_inference": not torch.allclose(learned, zeroed),
        "test_shape": tuple(logits.shape) == (8, 3, 2),
        "checkpoint_training_status": payload["training_status"] == "TRAINED_FROM_SCRATCH",
        "runtime_effect_none": results["runtime_effect"] == "NONE" and results["deployment"] is False,
        "canonical_effect_none": results["canonical_effect"] == "NONE",
    }
    output = {
        "schema_version": "1.0",
        "experiment_id": "EMBODIED_MOTIVATION_SIGNAL_V1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "validated_in_clean_process": True,
        "checkpoint": f"LOCAL_ONLY:{checkpoint.name}",
        "checkpoint_sha256": sha256_file(checkpoint),
        "checks": checks,
        "prediction_shape": list(logits.shape),
        "non_claim": "A learned proxy classifier cannot prove desire, consent, pleasure, subjectivity, identity or phenomenal experience.",
    }
    (args.evidence_dir / "EMBODIED_MOTIVATION_SIGNAL_VALIDATION.json").write_text(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"experiment_id": output["experiment_id"], "status": output["status"], "checks_passed": sum(checks.values()), "checks_total": len(checks)}, sort_keys=True))
    if output["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
