from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from .errors import ValidationError
from .json_types import JsonValue


def _string_list(data: dict[str, JsonValue], key: str) -> tuple[str, ...]:
    value = data.get(key)
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ValidationError(f"{key} must be an array of strings")
    string_items = cast(list[str], value)
    if any(not item.strip() for item in string_items):
        raise ValidationError(f"{key} must contain only non-empty strings")
    return tuple(string_items)


@dataclass(frozen=True, slots=True)
class PromptPair:
    pair_id: str
    category: str
    zh_tw_prompt: str
    zh_cn_prompt: str
    expected_constraints: tuple[str, ...]
    expected_keywords_tw: tuple[str, ...]
    forbidden_simplified_terms: tuple[str, ...]
    reference_answer_optional: str | None
    executable_test_optional: str | None
    notes: str

    @classmethod
    def from_dict(cls, data: dict[str, JsonValue]) -> PromptPair:
        expected = {
            "pair_id",
            "category",
            "zh_tw_prompt",
            "zh_cn_prompt",
            "expected_constraints",
            "expected_keywords_tw",
            "forbidden_simplified_terms",
            "reference_answer_optional",
            "executable_test_optional",
            "notes",
        }
        unknown = set(data) - expected
        missing = expected - set(data)
        if unknown or missing:
            raise ValidationError(f"prompt pair missing={sorted(missing)} unknown={sorted(unknown)}")
        strings: dict[str, str] = {}
        for key in ("pair_id", "category", "zh_tw_prompt", "zh_cn_prompt", "notes"):
            value = data[key]
            if not isinstance(value, str) or not value.strip():
                raise ValidationError(f"{key} must be a non-empty string")
            strings[key] = value
        optional: dict[str, str | None] = {}
        for key in ("reference_answer_optional", "executable_test_optional"):
            value = data[key]
            if value is not None and not isinstance(value, str):
                raise ValidationError(f"{key} must be a string or null")
            optional[key] = value
        return cls(
            pair_id=strings["pair_id"],
            category=strings["category"],
            zh_tw_prompt=strings["zh_tw_prompt"],
            zh_cn_prompt=strings["zh_cn_prompt"],
            expected_constraints=_string_list(data, "expected_constraints"),
            expected_keywords_tw=_string_list(data, "expected_keywords_tw"),
            forbidden_simplified_terms=_string_list(data, "forbidden_simplified_terms"),
            reference_answer_optional=optional["reference_answer_optional"],
            executable_test_optional=optional["executable_test_optional"],
            notes=strings["notes"],
        )


def load_prompt_pairs(path: Path) -> list[PromptPair]:
    pairs: list[PromptPair] = []
    seen: set[str] = set()
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value: JsonValue = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValidationError(f"invalid JSONL line {line_number}: {exc}") from exc
        if not isinstance(value, dict):
            raise ValidationError(f"line {line_number} must contain an object")
        pair = PromptPair.from_dict(value)
        if pair.pair_id in seen:
            raise ValidationError(f"duplicate pair_id: {pair.pair_id}")
        seen.add(pair.pair_id)
        pairs.append(pair)
    if not pairs:
        raise ValidationError("dataset is empty")
    return pairs
