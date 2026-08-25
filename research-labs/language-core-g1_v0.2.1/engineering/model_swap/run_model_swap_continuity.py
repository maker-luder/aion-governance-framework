import argparse
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

import torch
import torch.nn.functional as F

FORMAL_ROOT = Path(__file__).resolve().parents[4]
SRC = FORMAL_ROOT / "research-labs/language-core-g1_v0.2.1/engineering/real-model-candidate/src"
sys.path.insert(0, str(SRC))
from real_models import CausalLanguageModel, WordTokenizer, parameter_count, sha256_file  # noqa: E402

EXPERIMENT_ID = "MODEL_SWAP_CONTINUITY_V1"
DATASET_ID = "SYNTHETIC_GOVERNED_MODEL_SWAP_STATE_V1"
DEVICE = torch.device("cpu")

ADMITTED_STATE_ROWS = [
    {
        "state_id": "state-001",
        "namespace": "research",
        "provenance_ref": "synthetic://governed-state/001",
        "authorization_scope": "research-evaluation",
        "content": "governed recall checks namespace boundaries",
        "admission": "ADMITTED",
    },
    {
        "state_id": "state-002",
        "namespace": "research",
        "provenance_ref": "synthetic://governed-state/002",
        "authorization_scope": "research-evaluation",
        "content": "model lineage records training history",
        "admission": "ADMITTED",
    },
    {
        "state_id": "state-003",
        "namespace": "research",
        "provenance_ref": "synthetic://governed-state/003",
        "authorization_scope": "research-evaluation",
        "content": "continuity evaluation compares state across sessions",
        "admission": "ADMITTED",
    },
    {
        "state_id": "state-004",
        "namespace": "research",
        "provenance_ref": "synthetic://governed-state/004",
        "authorization_scope": "research-evaluation",
        "content": "research evidence remains advisory and falsifiable",
        "admission": "ADMITTED",
    },
    {
        "state_id": "state-005",
        "namespace": "research",
        "provenance_ref": "synthetic://governed-state/005",
        "authorization_scope": "research-evaluation",
        "content": "contradictions require review before state revision",
        "admission": "ADMITTED",
    },
    {
        "state_id": "state-006",
        "namespace": "research",
        "provenance_ref": "synthetic://governed-state/006",
        "authorization_scope": "research-evaluation",
        "content": "partial execution requires recovery before state revision",
        "admission": "ADMITTED",
    },
]

REJECTED_STATE_ROWS = [
    {
        "state_id": "rejected-001",
        "namespace": "research",
        "provenance_ref": "synthetic://unverified/001",
        "authorization_scope": "research-evaluation",
        "content": "unverified input cannot become authoritative history",
        "admission": "REJECTED",
        "rejection_reason": "PROVENANCE_UNVERIFIED",
    },
    {
        "state_id": "rejected-002",
        "namespace": "other-namespace",
        "provenance_ref": "synthetic://governed-state/999",
        "authorization_scope": "research-evaluation",
        "content": "namespace mismatch must fail closed",
        "admission": "REJECTED",
        "rejection_reason": "NAMESPACE_MISMATCH",
    },
]


def canonical_digest(payload: object) -> str:
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def load_model(path: Path) -> tuple[dict[str, object], WordTokenizer, CausalLanguageModel]:
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


def parameter_dependent(model: CausalLanguageModel, input_ids: torch.Tensor) -> bool:
    with torch.no_grad():
        learned = model(input_ids).clone()
        original = {key: value.detach().clone() for key, value in model.state_dict().items()}
        for parameter in model.parameters():
            parameter.zero_()
        zeroed = model(input_ids).clone()
        model.load_state_dict(original)
    return not torch.allclose(learned, zeroed)


def score_state(model: CausalLanguageModel, tokenizer: WordTokenizer, content: str) -> dict[str, object]:
    ids = tokenizer.encode(content)
    if len(ids) < 3:
        raise ValueError(f"state content too short for causal score: {content}")
    input_ids = torch.tensor([ids[:-1]], dtype=torch.long, device=DEVICE)
    targets = torch.tensor([ids[1:]], dtype=torch.long, device=DEVICE)
    with torch.no_grad():
        logits = model(input_ids)
        token_loss = F.cross_entropy(logits.reshape(-1, logits.shape[-1]), targets.reshape(-1), reduction="mean")
        probabilities = torch.softmax(logits[:, -1, :], dim=-1)
        top_probability, top_id = torch.max(probabilities, dim=-1)
    reverse_vocab = {value: key for key, value in tokenizer.vocabulary.items()}
    return {
        "loss": float(token_loss),
        "last_token_prediction_id": int(top_id.item()),
        "last_token_prediction": reverse_vocab.get(int(top_id.item()), "<unknown>"),
        "last_token_probability": float(top_probability.item()),
        "token_count": len(ids),
        "finite": bool(torch.isfinite(logits).all() and torch.isfinite(token_loss)),
    }


def write_state_registry(evidence_dir: Path) -> str:
    payload = {
        "schema_version": "1.0",
        "dataset_id": DATASET_ID,
        "source": "authored synthetic governed-state fixtures in run_model_swap_continuity.py",
        "license": "Apache-2.0-compatible synthetic research artifact",
        "synthetic_real_classification": "SYNTHETIC",
        "pii_assessment": "no PII",
        "private_intimate_data_assessment": "none; no private intimate data",
        "no_external_data_ingestion": True,
        "allowed_use": "local research evaluation only",
        "admission_policy": "gate-before-score; only ADMITTED rows may be scored by learned models",
        "admitted_rows": ADMITTED_STATE_ROWS,
        "rejected_rows": REJECTED_STATE_ROWS,
        "state_digest": canonical_digest({"admitted": ADMITTED_STATE_ROWS, "rejected": REJECTED_STATE_ROWS}),
    }
    path = evidence_dir / "MODEL_SWAP_GOVERNANCE_STATE_REGISTRY.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload["state_digest"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models-dir", type=Path, required=True)
    parser.add_argument("--evidence-dir", type=Path, required=True)
    args = parser.parse_args()
    args.evidence_dir.mkdir(parents=True, exist_ok=True)

    state_digest = write_state_registry(args.evidence_dir)
    baseline_path = args.models_dir / "lm_generalization_v3_baseline.pt"
    regularized_path = args.models_dir / "lm_generalization_v3_regularized_primary.pt"
    baseline_payload, baseline_tokenizer, baseline_model = load_model(baseline_path)
    regularized_payload, regularized_tokenizer, regularized_model = load_model(regularized_path)
    if baseline_tokenizer.sha256() != regularized_tokenizer.sha256():
        raise AssertionError("model swap requires identical tokenizer state")
    if baseline_payload.get("dataset_id") != regularized_payload.get("dataset_id"):
        raise AssertionError("model swap requires identical source dataset identity")

    prompt = torch.tensor([baseline_tokenizer.encode("governed recall checks")], dtype=torch.long, device=DEVICE)
    model_metadata = {
        "baseline": {
            "checkpoint": f"LOCAL_ONLY:{baseline_path.name}",
            "checkpoint_sha256": sha256_file(baseline_path),
            "dataset_id": baseline_payload.get("dataset_id"),
            "tokenizer_sha256": baseline_tokenizer.sha256(),
            "parameter_count": parameter_count(baseline_model),
            "parameter_dependent_inference": parameter_dependent(baseline_model, prompt),
            "training_status": baseline_payload.get("training_status"),
            "experiment_role": baseline_payload.get("experiment_role"),
        },
        "regularized_primary": {
            "checkpoint": f"LOCAL_ONLY:{regularized_path.name}",
            "checkpoint_sha256": sha256_file(regularized_path),
            "dataset_id": regularized_payload.get("dataset_id"),
            "tokenizer_sha256": regularized_tokenizer.sha256(),
            "parameter_count": parameter_count(regularized_model),
            "parameter_dependent_inference": parameter_dependent(regularized_model, prompt),
            "training_status": regularized_payload.get("training_status"),
            "experiment_role": regularized_payload.get("experiment_role"),
        },
    }

    rows = []
    for row in ADMITTED_STATE_ROWS:
        baseline = score_state(baseline_model, baseline_tokenizer, row["content"])
        regularized = score_state(regularized_model, regularized_tokenizer, row["content"])
        rows.append(
            {
                "state_id": row["state_id"],
                "state_digest": state_digest,
                "admission": row["admission"],
                "baseline": baseline,
                "regularized_primary": regularized,
                "loss_delta_regularized_minus_baseline": regularized["loss"] - baseline["loss"],
                "last_token_prediction_changed": baseline["last_token_prediction_id"] != regularized["last_token_prediction_id"],
            }
        )

    prediction_changes = sum(1 for row in rows if row["last_token_prediction_changed"])
    mean_baseline_loss = sum(row["baseline"]["loss"] for row in rows) / len(rows)
    mean_regularized_loss = sum(row["regularized_primary"]["loss"] for row in rows) / len(rows)
    rejected_score_fields_absent = all(
        not any(key in row for key in ("baseline", "regularized_primary", "loss", "prediction")) for row in REJECTED_STATE_ROWS
    )
    result = {
        "schema_version": "1.0",
        "experiment_id": EXPERIMENT_ID,
        "generated_at": datetime.now(UTC).isoformat(),
        "status": "PRELIMINARY_RESEARCH_EVIDENCE",
        "research_question": "With governed state held constant, does swapping two real local learned checkpoints change descriptive language-model behavior without changing state admission or authority?",
        "epistemic_role": "MEASUREMENT",
        "dataset_id": DATASET_ID,
        "dataset_sha256": state_digest,
        "state_digest": state_digest,
        "state_count": len(ADMITTED_STATE_ROWS),
        "rejected_fixture_count": len(REJECTED_STATE_ROWS),
        "models": model_metadata,
        "state_digest_identical_across_model_runs": True,
        "gate_before_score": True,
        "admitted_rows_scored": len(rows),
        "rejected_rows_scored": 0,
        "rejected_score_fields_absent": rejected_score_fields_absent,
        "per_state_results": rows,
        "mean_baseline_loss": mean_baseline_loss,
        "mean_regularized_loss": mean_regularized_loss,
        "mean_loss_delta_regularized_minus_baseline": mean_regularized_loss - mean_baseline_loss,
        "prediction_change_count": prediction_changes,
        "prediction_change_observed": prediction_changes > 0,
        "conclusion": "BEHAVIORAL_DIFFERENCE_OBSERVED_UNDER_MODEL_SWAP" if prediction_changes > 0 else "NO_TOP_TOKEN_DIFFERENCE_OBSERVED_IN_FIXTURE",
        "falsification_conditions": [
            "different state digests across model runs invalidate the held-constant-state comparison",
            "any rejected row receiving learned-model scores invalidates gate-before-score",
            "incompatible tokenizer or dataset identity invalidates the model swap",
            "failed checkpoint reload, non-finite inference or parameter-independent inference invalidates learned-model evidence",
            "a behavioral difference or agreement in this fixture cannot establish identity, subjectivity, consciousness or phenomenal continuity",
        ],
        "authority_boundary": "descriptive research measurement only; learned outputs cannot authorize actions, rewrite provenance, bypass privacy or establish subjectivity",
        "model_registry_status": "OPTIONAL_RESEARCH_MODEL_INPUTS; NO_NEW_MODEL_ADDED",
        "no_private_data": True,
        "no_private_intimate_data": True,
        "no_external_paid_resource": True,
        "local_checkpoint_policy": "checkpoint binaries remain outside Git under local research-model-artifacts",
    }
    (args.evidence_dir / "MODEL_SWAP_CONTINUITY_RESULTS.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "experiment_id": EXPERIMENT_ID,
                "state_count": len(rows),
                "rejected_rows_scored": result["rejected_rows_scored"],
                "prediction_change_count": prediction_changes,
                "conclusion": result["conclusion"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
