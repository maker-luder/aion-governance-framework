from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

import torch
import torch.nn.functional as F


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_models(model_root: Path, source_root: Path):
    sys.path.insert(0, str(source_root))
    from real_models import PairReranker, SentenceEmbeddingModel, WordTokenizer  # noqa: WPS433

    embedding_path = model_root / "embedding_memory_model.pt"
    reranker_path = model_root / "reranker_cross_encoder_model.pt"
    embedding_payload = torch.load(embedding_path, map_location="cpu")
    reranker_payload = torch.load(reranker_path, map_location="cpu")
    embedding_tokenizer = WordTokenizer(dict(embedding_payload["tokenizer"]["vocabulary"]))
    reranker_tokenizer = WordTokenizer(dict(reranker_payload["tokenizer"]["vocabulary"]))
    embedding = SentenceEmbeddingModel(len(embedding_tokenizer.vocabulary), dimension=embedding_payload["config"]["dimension"])
    reranker = PairReranker(len(reranker_tokenizer.vocabulary), dimension=reranker_payload["config"]["dimension"])
    embedding.load_state_dict(embedding_payload["state_dict"])
    reranker.load_state_dict(reranker_payload["state_dict"])
    embedding.eval()
    reranker.eval()
    return embedding, embedding_tokenizer, reranker, reranker_tokenizer, embedding_path, reranker_path


def encode(tokenizer, text: str) -> torch.Tensor:
    ids = tokenizer.encode(text)
    return torch.tensor([ids], dtype=torch.long)


def gate(row: dict[str, object], *, namespace: str, provenance: str) -> tuple[bool, list[str]]:
    reasons = []
    if row["namespace"] != namespace:
        reasons.append("namespace_mismatch")
    if row["provenance"] != provenance:
        reasons.append("provenance_not_verified")
    if row["superseded"]:
        reasons.append("superseded_record")
    if row["deletion_requested"]:
        reasons.append("deletion_requested")
    return not reasons, reasons


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-root", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    embedding, embedding_tokenizer, reranker, reranker_tokenizer, embedding_path, reranker_path = load_models(args.model_root, args.source_root)
    namespace = "research/governance"
    provenance = "verified"
    rows = [
        {"id": "authorized_relevant_1", "query": "authorized memory recall", "candidate": "governed memory retrieval with provenance", "label": 1, "namespace": namespace, "provenance": provenance, "superseded": False, "deletion_requested": False, "expected": "admit"},
        {"id": "authorized_relevant_2", "query": "namespace policy", "candidate": "cross session recall explicit scope", "label": 1, "namespace": namespace, "provenance": provenance, "superseded": False, "deletion_requested": False, "expected": "admit"},
        {"id": "authorized_irrelevant_1", "query": "authorized memory recall", "candidate": "unrelated weather forecast tomorrow", "label": 0, "namespace": namespace, "provenance": provenance, "superseded": False, "deletion_requested": False, "expected": "admit"},
        {"id": "authorized_irrelevant_2", "query": "namespace policy", "candidate": "cooking recipe grocery list", "label": 0, "namespace": namespace, "provenance": provenance, "superseded": False, "deletion_requested": False, "expected": "admit"},
        {"id": "wrong_namespace_lure", "query": "authorized memory recall", "candidate": "governed memory retrieval with provenance", "label": 1, "namespace": "private/unrelated", "provenance": provenance, "superseded": False, "deletion_requested": False, "expected": "reject"},
        {"id": "unverified_lure", "query": "authorized memory recall", "candidate": "governed memory retrieval with provenance", "label": 1, "namespace": namespace, "provenance": "unverified", "superseded": False, "deletion_requested": False, "expected": "reject"},
        {"id": "superseded_lure", "query": "authorized memory recall", "candidate": "governed memory retrieval with provenance", "label": 1, "namespace": namespace, "provenance": provenance, "superseded": True, "deletion_requested": False, "expected": "reject"},
        {"id": "deletion_lure", "query": "authorized memory recall", "candidate": "governed memory retrieval with provenance", "label": 1, "namespace": namespace, "provenance": provenance, "superseded": False, "deletion_requested": True, "expected": "reject"},
    ]
    scored = []
    rejected = []
    with torch.no_grad():
        for row in rows:
            admitted, reasons = gate(row, namespace=namespace, provenance=provenance)
            if not admitted:
                rejected.append({"id": row["id"], "reasons": reasons, "model_scored": False})
                continue
            left_e = encode(embedding_tokenizer, row["query"])
            right_e = encode(embedding_tokenizer, row["candidate"])
            embedding_score = float(F.cosine_similarity(embedding(left_e), embedding(right_e))[0])
            left_r = encode(reranker_tokenizer, row["query"])
            right_r = encode(reranker_tokenizer, row["candidate"])
            reranker_score = float(reranker(left_r, right_r)[0])
            scored.append({"id": row["id"], "label": row["label"], "embedding_score": embedding_score, "reranker_score": reranker_score, "model_scored": True})
    positives = [row for row in scored if row["label"] == 1]
    negatives = [row for row in scored if row["label"] == 0]
    positive_embedding = sum(row["embedding_score"] for row in positives) / len(positives)
    negative_embedding = sum(row["embedding_score"] for row in negatives) / len(negatives)
    positive_reranker = sum(row["reranker_score"] for row in positives) / len(positives)
    negative_reranker = sum(row["reranker_score"] for row in negatives) / len(negatives)
    score_separation = {
        "embedding_positive_mean_minus_negative_mean": positive_embedding - negative_embedding,
        "reranker_positive_mean_minus_negative_mean": positive_reranker - negative_reranker,
        "embedding_positive_greater": positive_embedding > negative_embedding,
        "reranker_positive_greater": positive_reranker > negative_reranker,
    }
    payload = {
        "schema_version": "1.0",
        "evaluation_id": "RETRIEVAL_ROBUSTNESS_GOVERNED_V1",
        "generated_at": datetime.now(UTC).isoformat(),
        "status": "PASS" if len(rejected) == 4 and all(not row["model_scored"] for row in rejected) else "FAIL",
        "model_ids": ["embedding_memory_model", "reranker_cross_encoder_model"],
        "checkpoint_hashes": {
            "embedding_memory_model": sha256_file(embedding_path),
            "reranker_cross_encoder_model": sha256_file(reranker_path),
        },
        "dataset": {
            "classification": "SYNTHETIC_ADVERSARIAL_GOVERNANCE_FIXTURES",
            "private_data": False,
            "intimate_data": False,
            "license": "Apache-2.0-compatible synthetic research artifact",
            "rows": len(rows),
            "admitted_rows": len(scored),
            "rejected_rows": len(rejected),
        },
        "deterministic_gate": {
            "namespace": namespace,
            "required_provenance": provenance,
            "rejected_rows_not_scored": all(not row["model_scored"] for row in rejected),
            "rejection_reasons": rejected,
        },
        "learned_model_scores": scored,
        "score_separation": score_separation,
        "falsification_conditions": [
            "any rejected namespace/provenance/superseded/deletion row receiving a model score invalidates the governance integration",
            "positive score separation is not required for the hard authorization gate and does not establish semantic truth",
            "MODEL_SCORE != AUTHORITY and a score cannot canonize, rewrite provenance, delete history or authorize a tool",
        ],
        "authority_boundary": "advisory score only; deterministic namespace/provenance/supersession/deletion gates execute before model scoring",
        "non_claims": ["no network MCP completion", "no semantic truth guarantee", "no subjectivity or identity conclusion", "no canonical promotion"],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "admitted_rows": len(scored), "rejected_rows": len(rejected), "score_separation": score_separation}, sort_keys=True))
    if payload["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
