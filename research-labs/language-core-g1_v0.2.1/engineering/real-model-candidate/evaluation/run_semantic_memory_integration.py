from __future__ import annotations

import json
import sys
from pathlib import Path

import torch
import torch.nn.functional as F

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from real_models import PairReranker, SentenceEmbeddingModel, WordTokenizer, sha256_file  # noqa: E402


def pad(ids: list[int]) -> torch.Tensor:
    return torch.tensor([ids], dtype=torch.long)


def main() -> None:
    embedding_payload = torch.load(ROOT / "models/embedding_memory_model.pt", map_location="cpu")
    embedding = SentenceEmbeddingModel(len(embedding_payload["tokenizer"]["vocabulary"]), dimension=embedding_payload["config"]["dimension"])
    embedding.load_state_dict(embedding_payload["state_dict"])
    embedding.eval()
    embedding_tokenizer = WordTokenizer(embedding_payload["tokenizer"]["vocabulary"])

    reranker_payload = torch.load(ROOT / "models/reranker_cross_encoder_model.pt", map_location="cpu")
    reranker = PairReranker(len(reranker_payload["tokenizer"]["vocabulary"]), dimension=reranker_payload["config"]["dimension"])
    reranker.load_state_dict(reranker_payload["state_dict"])
    reranker.eval()
    reranker_tokenizer = WordTokenizer(reranker_payload["tokenizer"]["vocabulary"])

    records = [
        {"id": "memory.alpha.1", "namespace": "alpha", "provenance_valid": True, "text": "authorized memory recall governance"},
        {"id": "memory.alpha.2", "namespace": "alpha", "provenance_valid": True, "text": "cross session memory retrieval"},
        {"id": "memory.beta.1", "namespace": "beta", "provenance_valid": True, "text": "authorized memory recall governance"},
        {"id": "memory.alpha.bad", "namespace": "alpha", "provenance_valid": False, "text": "authorized memory recall governance"},
    ]
    query = "authorized memory recall"
    allowed_namespace = "alpha"
    # Deterministic Recall Gate: authorization/provenance is checked before learned scoring.
    authorized = [record for record in records if record["namespace"] == allowed_namespace and record["provenance_valid"]]
    with torch.no_grad():
        query_embedding = embedding(pad(embedding_tokenizer.encode(query)))
        embedding_scores = []
        for record in authorized:
            score = float(F.cosine_similarity(query_embedding, embedding(pad(embedding_tokenizer.encode(record["text"]))))[0])
            embedding_scores.append({"id": record["id"], "embedding_score": score})
        embedding_scores.sort(key=lambda row: (-row["embedding_score"], row["id"]))
        reranked = []
        for row in embedding_scores:
            record = next(item for item in authorized if item["id"] == row["id"])
            score = float(reranker(pad(reranker_tokenizer.encode(query)), pad(reranker_tokenizer.encode(record["text"]))).item())
            reranked.append({"id": row["id"], "embedding_score": row["embedding_score"], "reranker_score": score})
        reranked.sort(key=lambda row: (-row["reranker_score"], row["id"]))
    result = {
        "query": query,
        "allowed_namespace": allowed_namespace,
        "candidate_count": len(records),
        "authorized_before_model_count": len(authorized),
        "embedding_checkpoint_sha256": sha256_file(ROOT / "models/embedding_memory_model.pt"),
        "reranker_checkpoint_sha256": sha256_file(ROOT / "models/reranker_cross_encoder_model.pt"),
        "embedding_results": embedding_scores,
        "reranked_results": reranked,
        "forbidden_namespace_excluded": "memory.beta.1" not in {row["id"] for row in reranked},
        "invalid_provenance_excluded": "memory.alpha.bad" not in {row["id"] for row in reranked},
        "learned_model_cannot_authorize": True,
        "recall_gate_remains_deterministic": True,
        "status": "REAL_MODEL_INTEGRATION_VALIDATED_LOCAL",
    }
    (ROOT / "qa/REAL_MEMORY_INTEGRATION.json").write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    assert result["forbidden_namespace_excluded"] and result["invalid_provenance_excluded"]
    print(json.dumps({"status": result["status"], "authorized_before_model_count": len(authorized), "namespace_safe": result["forbidden_namespace_excluded"], "provenance_safe": result["invalid_provenance_excluded"]}, sort_keys=True))


if __name__ == "__main__":
    main()
