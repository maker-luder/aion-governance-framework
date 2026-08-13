import argparse
import hashlib
import json
from pathlib import Path

import torch

from run_embodied_motivation_signal_experiment import SignalClassifier, batch
from run_embodied_motivation_signal_v2_falsification import make_cases

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
    result = json.loads((args.evidence_dir / "EMBODIED_MOTIVATION_SIGNAL_V2_RESULTS.json").read_text(encoding="utf-8"))
    registry = json.loads((args.evidence_dir / "EMBODIED_MOTIVATION_V2_DATASET_REGISTRY.json").read_text(encoding="utf-8"))
    checkpoint_name = result["checkpoint"].split(":", 1)[1]
    checkpoint = args.models_dir / checkpoint_name
    payload = torch.load(checkpoint, map_location=DEVICE, weights_only=False)
    model = SignalClassifier(payload["config"]["vocabulary_size"], payload["config"]["embedding_dim"], payload["config"]["hidden_dim"])
    model.load_state_dict(payload["state_dict"])
    model.eval()
    cases = make_cases()
    all_rows = [row for rows in cases.values() for row in rows]
    vocab = payload["vocabulary"]
    check_rows = []
    for row in all_rows:
        encoded = [vocab.get(token.lower(), 0) for token in row["text"].split()]
        check_rows.append(encoded)
    max_len = max(len(row) for row in check_rows)
    ids = torch.tensor([row + [1] * (max_len - len(row)) for row in check_rows], dtype=torch.long)
    with torch.no_grad():
        logits = model(ids)
        original = {key: value.detach().clone() for key, value in model.state_dict().items()}
        learned = model(ids).clone()
        for parameter in model.parameters():
            parameter.zero_()
        zeroed = model(ids).clone()
        model.load_state_dict(original)
    checks = {
        "checkpoint_exists": checkpoint.is_file(),
        "checkpoint_hash_matches": sha256_file(checkpoint) == result["checkpoint_sha256"],
        "checkpoint_dataset_matches_v1": payload["dataset_id"] == "SYNTHETIC_ADULT_EMBODIED_MOTIVATION_V1",
        "case_counts": registry["case_counts"] == {"canonical": 8, "keyword_scrubbed": 8, "label_permuted": 8},
        "adult_non_graphic_contract": registry["adult_context"] is True and registry["graphic_content"] is False and registry["no_minors"] is True,
        "no_private_data": result["no_private_data"] is True and result["no_private_intimate_data"] is True,
        "oov_free": registry["oov_tokens"] == [],
        "exact_disjoint_case_texts": registry["exact_disjoint_case_texts"] is True,
        "label_permutation_pairs_preserve_text": registry["label_permutation_pairs_preserve_text"] is True,
        "finite_logits": bool(torch.isfinite(logits).all()),
        "parameter_dependent_inference": not torch.allclose(learned, zeroed),
        "prediction_shape": tuple(logits.shape) == (24, 3, 2),
        "runtime_canonical_locks": result["runtime_effect"] == "NONE" and result["canonical_effect"] == "NONE" and result["deployment"] is False,
        "baseline_contrast_present": "deterministic_keyword_baseline_canonical" in result["cases"] and "deterministic_keyword_baseline_scrubbed" in result["cases"],
        "falsification_result_present": result["falsification_result"] in {"TEMPLATE_OR_KEYWORD_DEPENDENCE_SUPPORTED", "TEMPLATE_DEPENDENCE_NOT_SUPPORTED_IN_THIS_FIXTURE"},
    }
    output = {
        "schema_version": "1.0",
        "experiment_id": "EMBODIED_MOTIVATION_SIGNAL_V2",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "validated_in_clean_process": True,
        "checkpoint": result["checkpoint"],
        "checkpoint_sha256": sha256_file(checkpoint),
        "checks": checks,
        "non_claim": "V2 tests prompt/template dependence only; it cannot prove desire, consent, pleasure, subjectivity or phenomenal experience.",
    }
    (args.evidence_dir / "EMBODIED_MOTIVATION_SIGNAL_V2_VALIDATION.json").write_text(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"experiment_id": output["experiment_id"], "status": output["status"], "checks_passed": sum(checks.values()), "checks_total": len(checks)}, sort_keys=True))
    if output["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
