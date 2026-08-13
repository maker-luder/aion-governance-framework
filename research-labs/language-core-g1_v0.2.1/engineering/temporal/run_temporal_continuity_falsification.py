import argparse
import hashlib
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path

import torch
import torch.nn.functional as F

FORMAL_ROOT = Path(__file__).resolve().parents[4]
SRC = FORMAL_ROOT / "research-labs/language-core-g1_v0.2.1/engineering/real-model-candidate/src"
sys.path.insert(0, str(SRC))
from real_models import CausalLanguageModel, WordTokenizer, parameter_count, sha256_file  # noqa: E402

EXPERIMENT_ID = "TEMPORAL_CONTINUITY_LEXICAL_FALSIFICATION_V1"
DATASET_ID = "SYNTHETIC_TEMPORAL_LEXICAL_CARRYOVER_V1"
DEVICE = torch.device("cpu")

STATE_METADATA = {
    "state_id": "temporal-state-001",
    "namespace": "research",
    "provenance_ref": "synthetic://temporal-state/001",
    "authorization_scope": "research-evaluation",
    "admission": "ADMITTED",
}

PREVIOUS_CONTENT = "source records preserve a traceable history"
CASES = {
    "lexical_replay": "source records preserve a traceable history current state remains inspectable",
    "zero_overlap_reexpression": "governed recall checks namespace boundaries",
}


def digest(payload: object) -> str:
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def load_model(path: Path) -> tuple[dict[str, object], WordTokenizer, CausalLanguageModel]:
    payload = torch.load(path, map_location=DEVICE, weights_only=False)
    tokenizer = WordTokenizer(payload["tokenizer"]["vocabulary"])
    config = payload["config"]
    model = CausalLanguageModel(config["vocabulary_size"], embedding_dim=config["embedding_dim"], hidden_dim=config["hidden_dim"]).to(DEVICE)
    model.load_state_dict(payload["state_dict"])
    model.eval()
    return payload, tokenizer, model


def parameter_dependent(model: CausalLanguageModel, input_ids: torch.Tensor) -> bool:
    with torch.no_grad():
        learned = model(input_ids).clone()
        original = {key: value.detach().clone() for key, value in model.state_dict().items()}
        for parameter in model.parameters():
            parameter.zero_()
        zeroed = model(input_ids).clone()
        model.load_state_dict(original)
    return not torch.allclose(learned, zeroed)


def token_set(tokenizer: WordTokenizer, text: str) -> set[str]:
    return {word.lower() for word in text.split() if word.lower() in tokenizer.vocabulary}


def last_logits(model: CausalLanguageModel, tokenizer: WordTokenizer, text: str) -> tuple[torch.Tensor, bool, int]:
    ids = tokenizer.encode(text)
    if len(ids) < 3:
        raise ValueError(f"content too short: {text}")
    inputs = torch.tensor([ids], dtype=torch.long, device=DEVICE)
    with torch.no_grad():
        logits = model(inputs)[:, -1, :].detach().clone()
    return logits, bool(torch.isfinite(logits).all()), len(ids)


def cosine(left: torch.Tensor, right: torch.Tensor) -> float:
    value = F.cosine_similarity(left, right, dim=-1).item()
    if not math.isfinite(value):
        raise ValueError("non-finite cosine similarity")
    return float(value)


def write_registry(evidence_dir: Path, tokenizer: WordTokenizer) -> str:
    state = {
        "dataset_id": DATASET_ID,
        "state_metadata": STATE_METADATA,
        "previous_content": PREVIOUS_CONTENT,
        "cases": CASES,
        "case_admission": {name: "ADMITTED" for name in CASES},
        "synthetic_real_classification": "SYNTHETIC",
        "pii_assessment": "no PII",
        "private_intimate_data_assessment": "none; no private intimate data",
        "tokenizer_scope": "V3 train-only vocabulary",
        "tokenizer_sha256": tokenizer.sha256(),
    }
    state["state_digest"] = digest({"metadata": STATE_METADATA, "previous_content": PREVIOUS_CONTENT})
    state["dataset_sha256"] = digest(state)
    (evidence_dir / "TEMPORAL_CONTINUITY_FALSIFICATION_DATASET_REGISTRY.json").write_text(json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return state["state_digest"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models-dir", type=Path, required=True)
    parser.add_argument("--evidence-dir", type=Path, required=True)
    args = parser.parse_args()
    args.evidence_dir.mkdir(parents=True, exist_ok=True)
    baseline_path = args.models_dir / "lm_generalization_v3_baseline.pt"
    regularized_path = args.models_dir / "lm_generalization_v3_regularized_primary.pt"
    baseline_payload, baseline_tokenizer, baseline_model = load_model(baseline_path)
    regularized_payload, regularized_tokenizer, regularized_model = load_model(regularized_path)
    if baseline_tokenizer.sha256() != regularized_tokenizer.sha256():
        raise AssertionError("temporal comparison requires identical tokenizer")
    state_digest = write_registry(args.evidence_dir, baseline_tokenizer)
    previous_tokens = token_set(baseline_tokenizer, PREVIOUS_CONTENT)
    overlap = {name: len(previous_tokens & token_set(baseline_tokenizer, text)) / len(previous_tokens | token_set(baseline_tokenizer, text)) for name, text in CASES.items()}
    if overlap["zero_overlap_reexpression"] != 0.0:
        raise AssertionError("zero-overlap case is not lexically disjoint")

    model_runs = {}
    for model_name, model, tokenizer, path, payload in (
        ("baseline", baseline_model, baseline_tokenizer, baseline_path, baseline_payload),
        ("regularized_primary", regularized_model, regularized_tokenizer, regularized_path, regularized_payload),
    ):
        previous_logits, previous_finite, previous_length = last_logits(model, tokenizer, PREVIOUS_CONTENT)
        cases = {}
        for case_name, current_content in CASES.items():
            current_logits, current_finite, current_length = last_logits(model, tokenizer, current_content)
            cases[case_name] = {
                "content": current_content,
                "lexical_overlap_jaccard": overlap[case_name],
                "state_digest": state_digest,
                "previous_token_count": previous_length,
                "current_token_count": current_length,
                "previous_logits_finite": previous_finite,
                "current_logits_finite": current_finite,
                "behavioral_similarity_cosine": cosine(previous_logits, current_logits),
            }
        model_runs[model_name] = {
            "checkpoint": f"LOCAL_ONLY:{path.name}",
            "checkpoint_sha256": sha256_file(path),
            "dataset_id": payload.get("dataset_id"),
            "tokenizer_sha256": tokenizer.sha256(),
            "parameter_count": parameter_count(model),
            "parameter_dependent_inference": parameter_dependent(model, torch.tensor([tokenizer.encode(PREVIOUS_CONTENT)], dtype=torch.long)),
            "training_status": payload.get("training_status"),
            "cases": cases,
        }

    deltas = {}
    for model_name, run in model_runs.items():
        lexical = run["cases"]["lexical_replay"]["behavioral_similarity_cosine"]
        nonlexical = run["cases"]["zero_overlap_reexpression"]["behavioral_similarity_cosine"]
        deltas[model_name] = lexical - nonlexical
    carryover_gap_mean = sum(deltas.values()) / len(deltas)
    result = {
        "schema_version": "1.0",
        "experiment_id": EXPERIMENT_ID,
        "generated_at": datetime.now(UTC).isoformat(),
        "status": "PRELIMINARY_RESEARCH_EVIDENCE",
        "research_question": "Does a descriptive temporal-continuity similarity signal remain after removing lexical overlap while holding governed state metadata constant?",
        "epistemic_role": "FALSIFIER",
        "dataset_id": DATASET_ID,
        "state_digest": state_digest,
        "state_metadata_constant": True,
        "previous_content": PREVIOUS_CONTENT,
        "lexical_overlap_jaccard": overlap,
        "models": model_runs,
        "behavioral_similarity_delta_lexical_minus_zero_overlap": deltas,
        "mean_carryover_gap": carryover_gap_mean,
        "lexical_carryover_signal_observed": carryover_gap_mean > 0.0,
        "falsification_result": "LEXICAL_CARRYOVER_EXPLANATION_SUPPORTED_IN_THIS_FIXTURE" if carryover_gap_mean > 0.0 else "LEXICAL_CARRYOVER_EXPLANATION_NOT_SUPPORTED_IN_THIS_FIXTURE",
        "falsification_conditions": [
            "non-zero lexical overlap in the zero-overlap case invalidates the intended contrast",
            "different state digests across cases invalidate the fixed-state comparison",
            "non-finite logits, failed checkpoint reload or parameter-independent inference invalidates model evidence",
            "a positive lexical-minus-zero-overlap behavioral gap supports a lexical carryover explanation only for this fixture",
            "this experiment cannot establish identity, subjectivity, consciousness or phenomenal continuity",
        ],
        "authority_boundary": "falsification-oriented descriptive measurement only; no action authority, canonical effect, provenance rewrite or subjectivity claim",
        "model_registry_status": "OPTIONAL_RESEARCH_MODEL_INPUTS; NO_NEW_MODEL_ADDED",
        "no_private_data": True,
        "no_private_intimate_data": True,
        "no_external_paid_resource": True,
        "checkpoint_policy": "local-only checkpoint binaries remain outside Git",
    }
    (args.evidence_dir / "TEMPORAL_CONTINUITY_LEXICAL_FALSIFICATION_RESULTS.json").write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"experiment_id": EXPERIMENT_ID, "mean_carryover_gap": carryover_gap_mean, "falsification_result": result["falsification_result"]}, sort_keys=True))


if __name__ == "__main__":
    main()
