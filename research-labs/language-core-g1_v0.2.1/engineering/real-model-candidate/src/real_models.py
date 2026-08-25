from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Iterable

import torch
from torch import nn


class WordTokenizer:
    def __init__(self, vocabulary: dict[str, int]):
        self.vocabulary = dict(vocabulary)
        self.unk_id = self.vocabulary.get("<unk>", 0)

    @classmethod
    def from_texts(cls, texts: Iterable[str]) -> "WordTokenizer":
        words = {word.lower() for text in texts for word in text.split()}
        vocab = {"<unk>": 0, "<pad>": 1}
        vocab.update({word: index for index, word in enumerate(sorted(words), start=2)})
        return cls(vocab)

    def encode(self, text: str) -> list[int]:
        return [self.vocabulary.get(word.lower(), self.unk_id) for word in text.split()]

    def to_dict(self) -> dict[str, object]:
        return {"vocabulary": dict(sorted(self.vocabulary.items(), key=lambda item: item[1]))}

    def sha256(self) -> str:
        payload = json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":")).encode()
        return hashlib.sha256(payload).hexdigest()


class CharTokenizer:
    def __init__(self, vocabulary: list[str]):
        self.vocabulary = list(vocabulary)
        self.to_id = {token: index for index, token in enumerate(self.vocabulary)}

    @classmethod
    def from_text(cls, text: str) -> "CharTokenizer":
        return cls(sorted(set(text)))

    def encode(self, text: str) -> list[int]:
        return [self.to_id[char] for char in text]

    def decode(self, ids: Iterable[int]) -> str:
        return "".join(self.vocabulary[int(index)] for index in ids)

    def to_dict(self) -> dict[str, object]:
        return {"vocabulary": self.vocabulary}

    def sha256(self) -> str:
        payload = json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
        return hashlib.sha256(payload).hexdigest()


class CausalLanguageModel(nn.Module):
    def __init__(self, vocabulary_size: int, embedding_dim: int = 24, hidden_dim: int = 48):
        super().__init__()
        self.embedding = nn.Embedding(vocabulary_size, embedding_dim)
        self.gru = nn.GRU(embedding_dim, hidden_dim, batch_first=True)
        self.lm_head = nn.Linear(hidden_dim, vocabulary_size)
        self.config = {
            "vocabulary_size": vocabulary_size,
            "embedding_dim": embedding_dim,
            "hidden_dim": hidden_dim,
            "architecture": "Embedding-GRU-CausalLM",
        }

    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:
        hidden = self.embedding(input_ids)
        hidden, _ = self.gru(hidden)
        return self.lm_head(hidden)

    @torch.no_grad()
    def generate(self, input_ids: torch.Tensor, max_new_tokens: int) -> torch.Tensor:
        output = input_ids.clone()
        for _ in range(max_new_tokens):
            logits = self.forward(output[:, -64:])[:, -1, :]
            next_token = torch.argmax(logits, dim=-1, keepdim=True)
            output = torch.cat([output, next_token], dim=1)
        return output


class LoRAAdaptedLanguageModel(nn.Module):
    def __init__(self, base: CausalLanguageModel, rank: int = 4, alpha: float = 4.0):
        super().__init__()
        self.base = base
        for parameter in self.base.parameters():
            parameter.requires_grad = False
        hidden_dim = base.lm_head.in_features
        vocabulary_size = base.lm_head.out_features
        self.lora_a = nn.Parameter(torch.zeros(rank, hidden_dim))
        self.lora_b = nn.Parameter(torch.zeros(vocabulary_size, rank))
        nn.init.normal_(self.lora_a, mean=0.0, std=0.02)
        nn.init.zeros_(self.lora_b)
        self.rank = rank
        self.alpha = alpha
        self.config = {"architecture": "Frozen-CausalLM-plus-LoRA-output-head", "rank": rank, "alpha": alpha}

    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:
        hidden = self.base.embedding(input_ids)
        hidden, _ = self.base.gru(hidden)
        base_logits = self.base.lm_head(hidden)
        delta = torch.matmul(torch.matmul(hidden, self.lora_a.t()), self.lora_b.t()) * (self.alpha / self.rank)
        return base_logits + delta

    @torch.no_grad()
    def generate(self, input_ids: torch.Tensor, max_new_tokens: int) -> torch.Tensor:
        output = input_ids.clone()
        for _ in range(max_new_tokens):
            logits = self.forward(output[:, -64:])[:, -1, :]
            next_token = torch.argmax(logits, dim=-1, keepdim=True)
            output = torch.cat([output, next_token], dim=1)
        return output


class SentenceEmbeddingModel(nn.Module):
    def __init__(self, vocabulary_size: int, dimension: int = 16):
        super().__init__()
        self.embedding = nn.Embedding(vocabulary_size, dimension, padding_idx=1)
        self.dimension = dimension

    def forward(self, token_ids: torch.Tensor) -> torch.Tensor:
        mask = (token_ids != 1).float().unsqueeze(-1)
        values = self.embedding(token_ids) * mask
        return values.sum(dim=1) / mask.sum(dim=1).clamp_min(1.0)


class PairReranker(nn.Module):
    def __init__(self, vocabulary_size: int, dimension: int = 16):
        super().__init__()
        self.embedding = nn.Embedding(vocabulary_size, dimension, padding_idx=1)
        self.network = nn.Sequential(
            nn.Linear(dimension * 4, 24),
            nn.ReLU(),
            nn.Linear(24, 1),
        )
        self.dimension = dimension

    def encode(self, token_ids: torch.Tensor) -> torch.Tensor:
        mask = (token_ids != 1).float().unsqueeze(-1)
        values = self.embedding(token_ids) * mask
        return values.sum(dim=1) / mask.sum(dim=1).clamp_min(1.0)

    def forward(self, left: torch.Tensor, right: torch.Tensor) -> torch.Tensor:
        left_vector = self.encode(left)
        right_vector = self.encode(right)
        features = torch.cat([left_vector, right_vector, torch.abs(left_vector - right_vector), left_vector * right_vector], dim=1)
        return self.network(features).squeeze(-1)


class RouteModel(nn.Module):
    def __init__(self, vocabulary_size: int, class_count: int, dimension: int = 12):
        super().__init__()
        self.embedding = nn.Embedding(vocabulary_size, dimension, padding_idx=1)
        self.head = nn.Linear(dimension, class_count)

    def forward(self, token_ids: torch.Tensor) -> torch.Tensor:
        mask = (token_ids != 1).float().unsqueeze(-1)
        vector = (self.embedding(token_ids) * mask).sum(dim=1) / mask.sum(dim=1).clamp_min(1.0)
        return self.head(vector)


class SalienceModel(nn.Module):
    def __init__(self, feature_count: int = 4):
        super().__init__()
        self.network = nn.Sequential(nn.Linear(feature_count, 12), nn.Tanh(), nn.Linear(12, 1))

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        return self.network(features).squeeze(-1)


class TemporalGRU(nn.Module):
    def __init__(self, input_dim: int = 3, hidden_dim: int = 12):
        super().__init__()
        self.gru = nn.GRU(input_dim, hidden_dim, batch_first=True)
        self.head = nn.Linear(hidden_dim, 1)

    def forward(self, sequence: torch.Tensor) -> torch.Tensor:
        hidden, _ = self.gru(sequence)
        return self.head(hidden[:, -1, :]).squeeze(-1)


def parameter_count(model: nn.Module) -> int:
    return sum(parameter.numel() for parameter in model.parameters())


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def save_checkpoint(path: Path, payload: dict[str, object]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(payload, path)
    return sha256_file(path)
