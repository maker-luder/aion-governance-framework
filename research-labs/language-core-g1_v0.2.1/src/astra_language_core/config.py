from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .errors import ValidationError
from .json_types import JsonValue, require_object
from .models import GenerationSettings


def load_json_compatible_yaml(path: Path) -> dict[str, JsonValue]:
    """Load JSON-compatible YAML without adding a runtime YAML dependency."""
    try:
        value: JsonValue = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationError(f"invalid JSON-compatible YAML: {path}: {exc}") from exc
    return require_object(value, "configuration")


@dataclass(frozen=True, slots=True)
class LabConfig:
    project_identity: str
    subsystem: str
    model_family_status: str
    artifact_root: Path
    registry_path: Path
    dataset_path: Path

    @classmethod
    def from_dict(cls, data: dict[str, JsonValue], base: Path) -> LabConfig:
        expected = {
            "project_identity",
            "subsystem",
            "model_family_status",
            "artifact_root",
            "registry_path",
            "dataset_path",
        }
        unknown = set(data) - expected
        missing = expected - set(data)
        if unknown or missing:
            raise ValidationError(f"config missing={sorted(missing)} unknown={sorted(unknown)}")
        texts: dict[str, str] = {}
        for key in expected:
            value = data[key]
            if not isinstance(value, str) or not value:
                raise ValidationError(f"{key} must be a non-empty string")
            texts[key] = value
        return cls(
            project_identity=texts["project_identity"],
            subsystem=texts["subsystem"],
            model_family_status=texts["model_family_status"],
            artifact_root=(base / texts["artifact_root"]).resolve(),
            registry_path=(base / texts["registry_path"]).resolve(),
            dataset_path=(base / texts["dataset_path"]).resolve(),
        )


def generation_settings(data: dict[str, JsonValue]) -> GenerationSettings:
    expected = {
        "seed",
        "temperature",
        "top_p",
        "top_k",
        "repeat_penalty",
        "num_ctx",
        "max_output_tokens",
        "system_prompt_hash",
        "chat_template_id",
    }
    unknown = set(data) - expected
    if unknown:
        raise ValidationError(f"unknown generation settings: {sorted(unknown)}")
    try:
        return GenerationSettings(**data)  # type: ignore[arg-type]
    except TypeError as exc:
        raise ValidationError(str(exc)) from exc
