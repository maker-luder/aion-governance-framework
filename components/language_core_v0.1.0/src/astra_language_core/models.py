from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import cast

from .enums import ModelStatus, QAStatus
from .errors import ValidationError
from .json_types import JsonValue


def _text(data: dict[str, JsonValue], key: str, default: str = "UNKNOWN") -> str:
    value = data.get(key, default)
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{key} must be a non-empty string")
    return value


def _optional_text(data: dict[str, JsonValue], key: str) -> str | None:
    value = data.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValidationError(f"{key} must be a string or null")
    return value


def _plain_text(data: dict[str, JsonValue], key: str, default: str = "") -> str:
    value = data.get(key, default)
    if not isinstance(value, str):
        raise ValidationError(f"{key} must be a string")
    return value


@dataclass(frozen=True, slots=True)
class ModelNode:
    model_id: str
    display_name: str
    family_generation: str
    parent_model_id: str | None
    upstream_model_name: str = "UNKNOWN"
    upstream_developer: str = "UNKNOWN"
    upstream_license: str = "NOT_VERIFIED"
    source_path: str | None = None
    source_format: str = "UNKNOWN"
    parameter_count: int | None = None
    quantization: str = "UNKNOWN"
    precision: str = "UNKNOWN"
    tokenizer_id: str = "UNKNOWN"
    chat_template_id: str = "UNKNOWN"
    context_length: int | None = None
    modification_type: str = "NONE"
    modification_description: str = ""
    adapter_path: str | None = None
    merged: bool = False
    runtime: str = "ollama"
    sha256: str | None = None
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    status: ModelStatus = ModelStatus.EXPERIMENTAL
    qa_status: QAStatus = QAStatus.QA_HOLD
    canonical_effect: str = "NONE"
    read_only: bool = False
    notes: str = ""

    def __post_init__(self) -> None:
        if self.canonical_effect != "NONE":
            raise ValidationError("candidate model canonical_effect must be NONE")
        if self.parameter_count is not None and self.parameter_count <= 0:
            raise ValidationError("parameter_count must be positive or null")
        if self.context_length is not None and self.context_length <= 0:
            raise ValidationError("context_length must be positive or null")
        if self.sha256 is not None and (
            len(self.sha256) != 64 or any(c not in "0123456789abcdef" for c in self.sha256.lower())
        ):
            raise ValidationError("sha256 must be a 64-character hexadecimal digest")
        if self.parent_model_id is None and not self.read_only:
            raise ValidationError("root baseline must be read_only")
        if self.parent_model_id is not None and self.read_only:
            raise ValidationError("derived experimental nodes cannot be marked read_only")

    def to_dict(self) -> dict[str, JsonValue]:
        raw = asdict(self)
        raw["status"] = self.status.value
        raw["qa_status"] = self.qa_status.value
        return cast(dict[str, JsonValue], raw)

    @classmethod
    def from_dict(cls, data: dict[str, JsonValue]) -> ModelNode:
        allowed = {field.name for field in cls.__dataclass_fields__.values()}
        unknown = set(data) - allowed
        if unknown:
            raise ValidationError(f"unknown model fields: {sorted(unknown)}")
        ints: dict[str, int | None] = {}
        for key in ("parameter_count", "context_length"):
            value = data.get(key)
            if value is not None and (not isinstance(value, int) or isinstance(value, bool)):
                raise ValidationError(f"{key} must be an integer or null")
            ints[key] = value
        merged = data.get("merged", False)
        read_only = data.get("read_only", False)
        if not isinstance(merged, bool) or not isinstance(read_only, bool):
            raise ValidationError("merged and read_only must be booleans")
        try:
            status = ModelStatus(_text(data, "status", ModelStatus.EXPERIMENTAL.value))
            qa_status = QAStatus(_text(data, "qa_status", QAStatus.QA_HOLD.value))
        except ValueError as exc:
            raise ValidationError(str(exc)) from exc
        return cls(
            model_id=_text(data, "model_id"),
            display_name=_text(data, "display_name"),
            family_generation=_text(data, "family_generation"),
            parent_model_id=_optional_text(data, "parent_model_id"),
            upstream_model_name=_text(data, "upstream_model_name"),
            upstream_developer=_text(data, "upstream_developer"),
            upstream_license=_text(data, "upstream_license", "NOT_VERIFIED"),
            source_path=_optional_text(data, "source_path"),
            source_format=_text(data, "source_format"),
            parameter_count=ints["parameter_count"],
            quantization=_text(data, "quantization"),
            precision=_text(data, "precision"),
            tokenizer_id=_text(data, "tokenizer_id"),
            chat_template_id=_text(data, "chat_template_id"),
            context_length=ints["context_length"],
            modification_type=_text(data, "modification_type", "NONE"),
            modification_description=_plain_text(data, "modification_description"),
            adapter_path=_optional_text(data, "adapter_path"),
            merged=merged,
            runtime=_text(data, "runtime", "ollama"),
            sha256=_optional_text(data, "sha256"),
            created_at=_text(data, "created_at", datetime.now(UTC).isoformat()),
            status=status,
            qa_status=qa_status,
            canonical_effect=_text(data, "canonical_effect", "NONE"),
            read_only=read_only,
            notes=_plain_text(data, "notes"),
        )


@dataclass(frozen=True, slots=True)
class GenerationSettings:
    seed: int = 0
    temperature: float = 0.0
    top_p: float = 1.0
    top_k: int = 40
    repeat_penalty: float = 1.0
    num_ctx: int = 2048
    max_output_tokens: int = 256
    system_prompt_hash: str = "UNKNOWN"
    chat_template_id: str = "UNKNOWN"

    def __post_init__(self) -> None:
        if not 0 <= self.temperature <= 2:
            raise ValidationError("temperature must be between 0 and 2")
        if not 0 < self.top_p <= 1:
            raise ValidationError("top_p must be in (0, 1]")
        if self.top_k < 0 or self.num_ctx <= 0 or self.max_output_tokens <= 0:
            raise ValidationError("top_k, num_ctx, and max_output_tokens are invalid")

    def to_dict(self) -> dict[str, JsonValue]:
        return cast(dict[str, JsonValue], asdict(self))


@dataclass(frozen=True, slots=True)
class CompletionResult:
    text: str
    total_latency_seconds: float
    time_to_first_token_seconds: float | None = None
    eval_tokens: int | None = None
    tokens_per_second: float | None = None
    runtime_metadata: dict[str, JsonValue] = field(default_factory=dict)
