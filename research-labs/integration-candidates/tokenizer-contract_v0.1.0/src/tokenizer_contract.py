"""Deterministic tokenizer interface candidate with no model dependency."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import re


class TokenizerContractError(ValueError):
    pass


@dataclass(frozen=True)
class TokenizerMetadata:
    tokenizer_id: str
    vocabulary_size: int
    model_max_length: int
    special_tokens: tuple[str, ...] = ("<bos>", "<eos>")
    normalization: str = "unicode-codepoint-reference"
    canonical_effect: str = "NONE"
    deployment: bool = False
    independent_ivv: str = "NOT_ACHIEVED"

    def validate(self) -> None:
        if not self.tokenizer_id or self.vocabulary_size < 1 or self.model_max_length < 1:
            raise TokenizerContractError("invalid tokenizer metadata")
        if len(self.special_tokens) != len(set(self.special_tokens)):
            raise TokenizerContractError("special tokens must be unique")
        if self.canonical_effect != "NONE":
            raise TokenizerContractError("canonical_effect must remain NONE")
        if self.deployment:
            raise TokenizerContractError("deployment must remain false")
        if self.independent_ivv != "NOT_ACHIEVED":
            raise TokenizerContractError("independent_ivv must remain NOT_ACHIEVED")


@dataclass(frozen=True)
class TokenizationResult:
    text: str
    tokens: tuple[str, ...]
    token_ids: tuple[int, ...]
    offsets: tuple[tuple[int, int], ...]
    truncated: bool
    special_tokens_added: bool

    @property
    def token_count(self) -> int:
        return len(self.tokens)

    def to_dict(self) -> dict[str, object]:
        return asdict(self) | {"token_count": self.token_count}


class ReferenceTokenizer:
    """A test tokenizer, not a model tokenizer or a language claim."""

    _piece = re.compile(r"[A-Za-z0-9_]+|[\u4e00-\u9fff]|[^\w\s]", re.UNICODE)

    def __init__(self, metadata: TokenizerMetadata) -> None:
        metadata.validate()
        self.metadata = metadata
        self._special_ids = {
            token: self._stable_id(f"special:{token}") for token in metadata.special_tokens
        }

    @staticmethod
    def _stable_id(piece: str) -> int:
        return int.from_bytes(hashlib.sha256(piece.encode("utf-8")).digest()[:4], "big")

    def tokenize(self, text: str, *, add_special_tokens: bool = False) -> TokenizationResult:
        if not isinstance(text, str):
            raise TokenizerContractError("text must be a string")
        matches = tuple(self._piece.finditer(text))
        tokens = [match.group(0) for match in matches]
        offsets = [(match.start(), match.end()) for match in matches]
        special_added = False
        if add_special_tokens:
            tokens = [self.metadata.special_tokens[0], *tokens, self.metadata.special_tokens[-1]]
            offsets = [(0, 0), *offsets, (len(text), len(text))]
            special_added = True
        truncated = len(tokens) > self.metadata.model_max_length
        if truncated:
            tokens = tokens[: self.metadata.model_max_length]
            offsets = offsets[: self.metadata.model_max_length]
        token_ids = tuple(
            self._special_ids.get(token, self._stable_id(f"piece:{token}")) for token in tokens
        )
        return TokenizationResult(
            text=text,
            tokens=tuple(tokens),
            token_ids=token_ids,
            offsets=tuple(offsets),
            truncated=truncated,
            special_tokens_added=special_added,
        )

    def metadata_json(self) -> str:
        return json.dumps(asdict(self.metadata), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
