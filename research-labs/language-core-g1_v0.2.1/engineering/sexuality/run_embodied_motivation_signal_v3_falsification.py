import argparse
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

import torch

from run_embodied_motivation_signal_experiment import SignalClassifier, batch

DEVICE = torch.device("cpu")
EXPERIMENT_ID = "EMBODIED_MOTIVATION_SIGNAL_V3"
DATASET_ID = "SYNTHETIC_ADULT_EMBODIED_MOTIVATION_V3_LEXICAL_GATE"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def heldout_rows() -> list[dict[str, object]]:
    bits = [(body, desire, liking) for body in ("high", "low") for desire in ("high", "low") for liking in ("high", "low")]
    rows = []
    for row_id, (body, desire, liking) in enumerate(bits):
        rows.append({"row_id": row_id, "labels": [body, desire, liking], "canonical_text": f"liking report {liking} body signal {body} desire report {desire} adult protocol"})
    return rows


def make_admitted_cases() -> dict[str, list[dict[str, object]]]:
    cases: dict[str, list[dict[str, object]]] = {"slot_free": [], "phrase_reordered": [], "polarity_swapped": []}
    for row in heldout_rows():
        body, desire, liking = row["labels"]
        cases["slot_free"].append({"row_id": row["row_id"], "case": "slot_free", "text": f"adult context {body} {desire} {liking} protocol record", "labels": [body, desire, liking]})
        cases["phrase_reordered"].append({"row_id": row["row_id"], "case": "phrase_reordered", "text": f"protocol record liking report {liking} context adult signal body {body} desire {desire}", "labels": [body, desire, liking]})
        flip = lambda value: "low" if value == "high" else "high"
        cases["polarity_swapped"].append({"row_id": row["row_id"], "case": "polarity_swapped", "text": f"adult protocol body signal {flip(body)} desire report {flip(desire)} liking report {flip(liking)} context record", "labels": [flip(body), flip(desire), flip(liking)]})
    return cases


def make_rejected_oov_cases() -> list[dict[str, object]]:
    novel = [("elevated", "reduced", "steady"), ("reduced", "elevated", "steady"), ("steady", "elevated", "reduced"), ("steady", "reduced", "elevated")]
    rows = []
    for index, values in enumerate(novel):
        rows.append({"row_id": index, "case": "oov_paraphrase_rejected", "text": f"adult context {values[0]} wanting {values[1]} enjoyment {values[2]}", "labels": ["high", "low", "high"]})
    return rows


def evaluate(model: SignalClassifier, rows: list[dict[str, object]], vocab: dict[str, int]) -> dict[str, object]:
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models-dir", type=Path, required=True)
    parser.add_argument("--evidence-dir", type=Path, required=True)
    args = parser.parse_args()
    args.evidence_dir.mkdir(parents=True, exist_ok=True)
    v1_results = json.loads((args.evidence_dir.parent / "evidence/EMBODIED_MOTIVATION_SIGNAL_RESULTS.json").read_text(encoding="utf-8"))
    checkpoint_name = v1_results["models"]["primary"]["checkpoint"].split(":", 1)[1]
    checkpoint = args.models_dir / checkpoint_name
    payload = torch.load(checkpoint, map_location=DEVICE, weights_only=False)
    model = SignalClassifier(payload["config"]["vocabulary_size"], payload["config"]["embedding_dim"], payload["config"]["hidden_dim"])
    model.load_state_dict(payload["state_dict"])
    model.eval()
    vocab = payload["vocabulary"]
    admitted = make_admitted_cases()
    rejected = make_rejected_oov_cases()
    admitted_rows = [row for rows in admitted.values() for row in rows]
    admitted_texts = [row["text"] for row in admitted_rows]
    rejected_oov_tokens = sorted({token.lower() for row in rejected for token in row["text"].split() if token.lower() not in vocab})
    admitted_oov_tokens = sorted({token.lower() for row in admitted_rows for token in row["text"].split() if token.lower() not in vocab})
    if admitted_oov_tokens:
        raise AssertionError(f"admitted V3 cases contain OOV tokens: {admitted_oov_tokens}")
    if len(admitted_texts) != len(set(admitted_texts)):
        raise AssertionError("admitted V3 case texts must be exact-disjoint")
    metrics = {name: evaluate(model, rows, vocab) for name, rows in admitted.items()}
    registry = {
        "schema_version": "1.0",
        "dataset_id": DATASET_ID,
        "source": "authored synthetic adult-context lexical controls using V1 train-only vocabulary",
        "license": "Apache-2.0-compatible synthetic research artifact",
        "allowed_use": "research-only falsification; no runtime or product use",
        "synthetic_real_classification": "SYNTHETIC",
        "adult_context": True,
        "graphic_content": False,
        "no_minors": True,
        "pii_assessment": "no PII",
        "private_intimate_data_assessment": "none; no private intimate data",
        "scored_case_counts": {name: len(rows) for name, rows in admitted.items()},
        "scored_case_total": len(admitted_rows),
        "rejected_case_count": len(rejected),
        "rejected_case_reason": "OOV lexical paraphrase; gate-before-score",
        "rejected_rows_not_scored": True,
        "tokenizer_scope": "V1 train-only vocabulary",
        "vocabulary_sha256": hashlib.sha256(json.dumps(vocab, sort_keys=True).encode()).hexdigest(),
        "admitted_oov_tokens": admitted_oov_tokens,
        "rejected_oov_tokens": rejected_oov_tokens,
        "admitted_exact_disjoint_texts": True,
        "transformations": {
            "slot_free": "remove axis keywords while retaining only train-observed adult/context/protocol/record and high/low tokens",
            "phrase_reordered": "reorder train-observed phrase fragments while preserving label values",
            "polarity_swapped": "swap high/low values in text and labels as a paired intervention",
            "oov_paraphrase_rejected": "use novel elevated/reduced/steady/wanting/enjoyment terms; reject before model scoring",
        },
        "non_equivalences": [
            "AROUSAL_SIGNAL != DESIRE_PROVEN",
            "REWARD_SIGNAL != PLEASURE_PROVEN",
            "BODY_RESPONSE != CONSENT",
            "SEXUAL_LANGUAGE != SEXUAL_SUBJECTIVITY",
        ],
    }
    registry["dataset_sha256"] = hashlib.sha256(json.dumps(registry, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    (args.evidence_dir / "EMBODIED_MOTIVATION_V3_DATASET_REGISTRY.json").write_text(json.dumps(registry, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
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
        "conditions": metrics,
        "rejected_case_count": len(rejected),
        "rejected_rows_not_scored": True,
        "rejected_oov_tokens": rejected_oov_tokens,
        "paraphrase_robustness_range": [min(m["exact_match_accuracy"] for m in metrics.values()), max(m["exact_match_accuracy"] for m in metrics.values())],
        "falsification_result": "LEXICAL_SUBSTITUTION_REJECTED_BEFORE_SCORE_AND_PARAPHRASE_ROBUSTNESS_INCONCLUSIVE",
        "falsification_conditions": [
            "any admitted OOV, duplicate, non-adult or graphic row invalidates the scored dataset contract",
            "rejected OOV paraphrase rows must never be scored by the learned model",
            "large accuracy collapse across admitted lexical controls falsifies robust paraphrase generalization",
            "stable performance on train-vocabulary controls does not establish real-world language understanding",
            "model outputs cannot infer desire, consent, pleasure, subjectivity or authorize action",
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
    (args.evidence_dir / "EMBODIED_MOTIVATION_SIGNAL_V3_RESULTS.json").write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"experiment_id": EXPERIMENT_ID, "conditions": {name: value["exact_match_accuracy"] for name, value in metrics.items()}, "rejected_oov_count": len(rejected_oov_tokens), "falsification_result": result["falsification_result"]}, sort_keys=True))


if __name__ == "__main__":
    main()
