import argparse
import hashlib
import json
from pathlib import Path

import torch

from run_embodied_motivation_signal_experiment import SignalClassifier, batch
from run_embodied_motivation_signal_v3_falsification import make_admitted_cases, make_rejected_oov_cases

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
    result = json.loads((args.evidence_dir / "EMBODIED_MOTIVATION_SIGNAL_V3_RESULTS.json").read_text(encoding="utf-8"))
    registry = json.loads((args.evidence_dir / "EMBODIED_MOTIVATION_V3_DATASET_REGISTRY.json").read_text(encoding="utf-8"))
    checkpoint_name = result["checkpoint"].split(":", 1)[1]
    checkpoint = args.models_dir / checkpoint_name
    payload = torch.load(checkpoint, map_location=DEVICE, weights_only=False)
    model = SignalClassifier(payload["config"]["vocabulary_size"], payload["config"]["embedding_dim"], payload["config"]["hidden_dim"])
    model.load_state_dict(payload["state_dict"])
    model.eval()
    vocab = payload["vocabulary"]
    admitted = make_admitted_cases()
    rejected = make_rejected_oov_cases()
    admitted_rows = [row for rows in admitted.values() for row in rows]
    encoded = [[vocab.get(token.lower(), 0) for token in row["text"].split()] for row in admitted_rows]
    max_len = max(len(row) for row in encoded)
    ids = torch.tensor([row + [1] * (max_len - len(row)) for row in encoded], dtype=torch.long)
    with torch.no_grad():
        logits = model(ids)
        original = {key: value.detach().clone() for key, value in model.state_dict().items()}
        learned = model(ids).clone()
        for parameter in model.parameters():
            parameter.zero_()
        zeroed = model(ids).clone()
        model.load_state_dict(original)
    rejected_oov_tokens = sorted({token.lower() for row in rejected for token in row["text"].split() if token.lower() not in vocab})
    checks = {
        "checkpoint_exists": checkpoint.is_file(),
        "checkpoint_hash_matches": sha256_file(checkpoint) == result["checkpoint_sha256"],
        "checkpoint_dataset_matches_v1": payload["dataset_id"] == "SYNTHETIC_ADULT_EMBODIED_MOTIVATION_V1",
        "admitted_case_counts": registry["scored_case_counts"] == {"slot_free": 8, "phrase_reordered": 8, "polarity_swapped": 8},
        "rejected_case_count": registry["rejected_case_count"] == 4,
        "adult_non_graphic_contract": registry["adult_context"] is True and registry["graphic_content"] is False and registry["no_minors"] is True,
        "no_private_data": result["no_private_data"] is True and result["no_private_intimate_data"] is True,
        "admitted_oov_free": registry["admitted_oov_tokens"] == [],
        "rejected_oov_present": registry["rejected_oov_tokens"] == rejected_oov_tokens and len(rejected_oov_tokens) >= 3,
        "admitted_exact_disjoint": registry["admitted_exact_disjoint_texts"] is True,
        "rejected_rows_not_scored": result["rejected_rows_not_scored"] is True and registry["rejected_rows_not_scored"] is True,
        "scored_case_total": registry["scored_case_total"] == 24 and tuple(logits.shape) == (24, 3, 2),
        "finite_logits": bool(torch.isfinite(logits).all()),
        "parameter_dependent_inference": not torch.allclose(learned, zeroed),
        "runtime_canonical_locks": result["runtime_effect"] == "NONE" and result["canonical_effect"] == "NONE" and result["deployment"] is False,
        "falsification_result_present": result["falsification_result"] == "LEXICAL_SUBSTITUTION_REJECTED_BEFORE_SCORE_AND_PARAPHRASE_ROBUSTNESS_INCONCLUSIVE",
    }
    output = {
        "schema_version": "1.0",
        "experiment_id": "EMBODIED_MOTIVATION_SIGNAL_V3",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "validated_in_clean_process": True,
        "checkpoint": result["checkpoint"],
        "checkpoint_sha256": sha256_file(checkpoint),
        "checks": checks,
        "scored_rows": 24,
        "rejected_rows": 4,
        "rejected_rows_not_scored": True,
        "non_claim": "V3 evaluates lexical-control robustness only; it cannot prove desire, consent, pleasure, subjectivity or phenomenal experience.",
    }
    (args.evidence_dir / "EMBODIED_MOTIVATION_SIGNAL_V3_VALIDATION.json").write_text(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"experiment_id": output["experiment_id"], "status": output["status"], "checks_passed": sum(checks.values()), "checks_total": len(checks), "scored_rows": output["scored_rows"], "rejected_rows": output["rejected_rows"]}, sort_keys=True))
    if output["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
