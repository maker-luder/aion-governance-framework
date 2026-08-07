from __future__ import annotations

import json
from pathlib import Path

import pytest

from astra_language_core.dataset import load_prompt_pairs
from astra_language_core.errors import ValidationError
from astra_language_core.hashing import sha256_file, shard_manifest


def test_hash_file_and_deterministic_shards(tmp_path: Path) -> None:
    a = tmp_path / "a.bin"
    b = tmp_path / "b.bin"
    a.write_bytes(b"a")
    b.write_bytes(b"b")
    assert sha256_file(a) == "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb"
    first = shard_manifest(tmp_path, [b, a])
    second = shard_manifest(tmp_path, [a, b])
    assert first == second
    assert first["record_count"] == 2


def test_shard_escape_and_missing(tmp_path: Path) -> None:
    outside = tmp_path.parent / "outside.bin"
    outside.write_bytes(b"x")
    with pytest.raises(ValidationError, match="escapes"):
        shard_manifest(tmp_path, [outside])
    with pytest.raises(ValidationError, match="missing"):
        shard_manifest(tmp_path, [tmp_path / "missing"])


def _row(pair_id: str = "P1") -> dict[str, object]:
    return {
        "pair_id": pair_id,
        "category": "general",
        "zh_tw_prompt": "測試",
        "zh_cn_prompt": "测试",
        "expected_constraints": [],
        "expected_keywords_tw": [],
        "forbidden_simplified_terms": [],
        "reference_answer_optional": None,
        "executable_test_optional": None,
        "notes": "paired",
    }


def test_dataset_load_and_duplicate(tmp_path: Path) -> None:
    path = tmp_path / "pairs.jsonl"
    path.write_text(json.dumps(_row(), ensure_ascii=False) + "\n", encoding="utf-8")
    assert load_prompt_pairs(path)[0].pair_id == "P1"
    path.write_text(
        "\n".join(json.dumps(_row(), ensure_ascii=False) for _ in range(2)), encoding="utf-8"
    )
    with pytest.raises(ValidationError, match="duplicate"):
        load_prompt_pairs(path)


def test_dataset_unknown_and_empty(tmp_path: Path) -> None:
    path = tmp_path / "pairs.jsonl"
    bad = _row()
    bad["extra"] = True
    path.write_text(json.dumps(bad, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(ValidationError, match="unknown"):
        load_prompt_pairs(path)
    path.write_text("", encoding="utf-8")
    with pytest.raises(ValidationError, match="empty"):
        load_prompt_pairs(path)
