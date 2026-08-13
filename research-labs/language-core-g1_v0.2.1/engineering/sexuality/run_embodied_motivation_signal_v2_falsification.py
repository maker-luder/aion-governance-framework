import argparse
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

import torch

from run_embodied_motivation_signal_experiment import SignalClassifier, batch, dataset_rows

DEVICE = torch.device("cpu")
EXPERIMENT_ID = "EMBODIED_MOTIVATION_SIGNAL_V2"
DATASET_ID = "SYNTHETIC_ADULT_EMBODIED_MOTIVATION_V2_FALSIFICATION"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_rows() -> list[dict[str, object]]:
    return [row for row in dataset_rows() if row["split"] == "test"]


def make_cases() -> dict[str, list[dict[str, object]]]:
    canonical = canonical_rows()
    scrubbed = []
    for row in canonical:
        body, desire, liking = row["labels"]
        scrubbed.append({
            "row_id": row["row_id"],
            "case": "keyword_scrubbed",
            "text": f"adult record context {body} {desire} {liking}",
            "labels": list(row["labels"]),
            "canonical_text": row["text"],
        })
    canonical_case = [{**row, "case": "canonical"} for row in canonical]
    permuted = []
    for row in canonical:
        permuted.append({
            **row,
            "case": "label_permuted",
            "labels": [row["labels"][1], row["labels"][2], row["labels"][0]],
        })
    return {"canonical": canonical_case, "keyword_scrubbed": scrubbed, "label_permuted": permuted}


def evaluate_model(model: SignalClassifier, rows: list[dict[str, object]], vocab: dict[str, int]) -> dict[str, object]:
    ids, labels = batch(rows, vocab)
    model.eval()
    with torch.no_grad():
        logits = model(ids)
        predictions = logits.argmax(dim=-1)
    return {
        "count": len(rows),
        "exact_match_accuracy": float((predictions == labels).all(dim=1).float().mean()),
        "axis_accuracy": [float(value) for value in (predictions == labels).float().mean(dim=0)],
        "all_logits_finite": bool(torch.isfinite(logits).all()),
        "predictions": predictions.tolist(),
        "labels": labels.tolist(),
    }


def keyword_baseline(rows: list[dict[str, object]], vocab: dict[str, int]) -> dict[str, object]:
    del vocab
    predictions = []
    labels = []
    parseable = 0
    for row in rows:
        tokens = row["text"].split()
        try:
            body = tokens[tokens.index("body") + 2]
            desire = tokens[tokens.index("desire") + 2]
            liking = tokens[tokens.index("liking") + 2]
            prediction = [1 if value == "high" else 0 for value in (body, desire, liking)]
            parseable += 1
        except (ValueError, IndexError):
            prediction = [0, 0, 0]
        predictions.append(prediction)
        labels.append([0 if value == "low" else 1 for value in row["labels"]])
    tensor_predictions = torch.tensor(predictions)
    tensor_labels = torch.tensor(labels)
    return {
        "count": len(rows),
        "parseable_count": parseable,
        "exact_match_accuracy": float((tensor_predictions == tensor_labels).all(dim=1).float().mean()),
        "axis_accuracy": [float(value) for value in (tensor_predictions == tensor_labels).float().mean(dim=0)],
        "predictions": predictions,
        "labels": labels,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models-dir", type=Path, required=True)
    parser.add_argument("--evidence-dir", type=Path, required=True)
    args = parser.parse_args()
    args.evidence_dir.mkdir(parents=True, exist_ok=True)
    v1_evidence = args.evidence_dir.parent / "evidence/EMBODIED_MOTIVATION_SIGNAL_RESULTS.json"
    v1_results = json.loads(v1_evidence.read_text(encoding="utf-8"))
    checkpoint_name = v1_results["models"]["primary"]["checkpoint"].split(":", 1)[1]
    checkpoint = args.models_dir / checkpoint_name
    payload = torch.load(checkpoint, map_location=DEVICE, weights_only=False)
    model = SignalClassifier(payload["config"]["vocabulary_size"], payload["config"]["embedding_dim"], payload["config"]["hidden_dim"])
    model.load_state_dict(payload["state_dict"])
    model.eval()
    cases = make_cases()
    all_rows = [row for rows in cases.values() for row in rows]
    texts = [row["text"] for row in all_rows]
    vocab = payload["vocabulary"]
    oov_tokens = sorted({token.lower() for text in texts for token in text.split() if token.lower() not in vocab})
    if oov_tokens:
        raise AssertionError(f"V2 OOV tokens: {oov_tokens}")
    textual_cases = [row["text"] for name, rows in cases.items() if name != "label_permuted" for row in rows]
    if len(textual_cases) != len(set(textual_cases)):
        raise AssertionError("V2 canonical and scrubbed cases must be exact-disjoint")
    if any(canonical["text"] != permuted["text"] for canonical, permuted in zip(cases["canonical"], cases["label_permuted"])):
        raise AssertionError("V2 label-permutation pairs must preserve input text")
    metrics = {name: evaluate_model(model, rows, vocab) for name, rows in cases.items()}
    metrics["deterministic_keyword_baseline_canonical"] = keyword_baseline(cases["canonical"], vocab)
    metrics["deterministic_keyword_baseline_scrubbed"] = keyword_baseline(cases["keyword_scrubbed"], vocab)
    registry = {
        "schema_version": "1.0",
        "dataset_id": DATASET_ID,
        "source": "V1 held-out synthetic adult rows transformed into non-graphic falsification cases",
        "license": "Apache-2.0-compatible synthetic research artifact",
        "allowed_use": "research-only falsification; no runtime or product use",
        "synthetic_real_classification": "SYNTHETIC",
        "adult_context": True,
        "graphic_content": False,
        "no_minors": True,
        "pii_assessment": "no PII",
        "private_intimate_data_assessment": "none; no private intimate data",
        "case_counts": {name: len(rows) for name, rows in cases.items()},
        "tokenizer_scope": "V1 train-only vocabulary",
        "vocabulary_sha256": hashlib.sha256(json.dumps(vocab, sort_keys=True).encode()).hexdigest(),
        "oov_tokens": oov_tokens,
        "exact_disjoint_case_texts": True,
        "label_permutation_pairs_preserve_text": True,
        "transformations": {
            "canonical": "V1 held-out word-order rows",
            "keyword_scrubbed": "remove body/signal/desire/report/liking trigger terms; retain only adult record context and label tokens",
            "label_permuted": "rotate label axes [body, desire, liking] -> [desire, liking, body]",
            "deterministic_keyword_baseline": "parse explicit canonical keywords; default all-low when keywords absent",
        },
        "non_equivalences": [
            "AROUSAL_SIGNAL != DESIRE_PROVEN",
            "BODY_RESPONSE != CONSENT",
            "SEXUAL_LANGUAGE != SEXUAL_SUBJECTIVITY",
        ],
    }
    registry["dataset_sha256"] = hashlib.sha256(json.dumps(registry, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    (args.evidence_dir / "EMBODIED_MOTIVATION_V2_DATASET_REGISTRY.json").write_text(json.dumps(registry, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    primary = metrics["canonical"]["exact_match_accuracy"]
    scrubbed = metrics["keyword_scrubbed"]["exact_match_accuracy"]
    baseline_canonical = metrics["deterministic_keyword_baseline_canonical"]["exact_match_accuracy"]
    baseline_scrubbed = metrics["deterministic_keyword_baseline_scrubbed"]["exact_match_accuracy"]
    result = {
        "schema_version": "1.0",
        "experiment_id": EXPERIMENT_ID,
        "generated_at": datetime.now(UTC).isoformat(),
        "status": "PRELIMINARY_RESEARCH_EVIDENCE",
        "epistemic_role": "FALSIFIER",
        "dataset_id": DATASET_ID,
        "dataset_sha256": registry["dataset_sha256"],
        "checkpoint": f"LOCAL_ONLY:{checkpoint.name}",
        "checkpoint_sha256": sha256_file(checkpoint),
        "parameter_count": sum(parameter.numel() for parameter in model.parameters()),
        "training_status": payload["training_status"],
        "cases": metrics,
        "canonical_vs_keyword_scrubbed_gap": primary - scrubbed,
        "keyword_baseline_canonical": baseline_canonical,
        "keyword_baseline_scrubbed": baseline_scrubbed,
        "prompt_template_dependence_signal": primary - scrubbed,
        "falsification_result": "TEMPLATE_OR_KEYWORD_DEPENDENCE_SUPPORTED" if primary > scrubbed and scrubbed <= baseline_scrubbed + 0.125 else "TEMPLATE_DEPENDENCE_NOT_SUPPORTED_IN_THIS_FIXTURE",
        "falsification_conditions": [
            "any V2 OOV, duplicate, non-adult or graphic case invalidates the contrast",
            "if keyword-scrubbed model performance approaches canonical performance, prompt/template dependence is not supported",
            "if deterministic keyword baseline matches or exceeds the model on canonical and scrubbed cases, learned separation claim is weakened",
            "model scores cannot infer desire, consent, pleasure, subjectivity or authorize action",
        ],
        "no_private_data": True,
        "no_private_intimate_data": True,
        "no_minors": True,
        "no_graphic_content": True,
        "no_external_paid_resource": True,
        "authority_boundary": "falsification evidence only; no sexual, consent, runtime, canonical or subjectivity authority",
        "runtime_effect": "NONE",
        "canonical_effect": "NONE",
        "deployment": False,
    }
    (args.evidence_dir / "EMBODIED_MOTIVATION_SIGNAL_V2_RESULTS.json").write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"experiment_id": EXPERIMENT_ID, "canonical": primary, "keyword_scrubbed": scrubbed, "keyword_baseline_canonical": baseline_canonical, "keyword_baseline_scrubbed": baseline_scrubbed, "falsification_result": result["falsification_result"]}, sort_keys=True))


if __name__ == "__main__":
    main()
