from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path
from typing import Any

import pytest

from astra_language_core.errors import RuntimeFailure
from astra_language_core.models import GenerationSettings
from astra_language_core.runtime import OllamaRuntime

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "data/language_core_g1/PAIRED_ZH_DATASET_V1.jsonl"
FIXTURE = ROOT / "evaluation/OFFLINE_TOKENIZER_TELEMETRY_FIXTURE.json"


class _Response:
    def __init__(self, payload: object) -> None:
        self.buffer = io.BytesIO(json.dumps(payload).encode())

    def __enter__(self) -> _Response:
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def read(self) -> bytes:
        return self.buffer.read()


def _fixture() -> dict[str, Any]:
    value = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_offline_fixture_is_pinned_and_does_not_produce_token_counts() -> None:
    fixture = _fixture()
    assert fixture["schema_version"] == "g1.offline-tokenizer-telemetry.v1"
    assert fixture["fixture_status"] == "OFFLINE_CONTRACT_ONLY"
    assert fixture["model_execution_required"] is False
    assert fixture["tokenizer_execution_status"] == "NOT_EXECUTED"
    assert fixture["dataset_sha256"] == hashlib.sha256(DATASET.read_bytes()).hexdigest()

    rows = [json.loads(line) for line in DATASET.read_text(encoding="utf-8").splitlines() if line.strip()]
    rows_by_id = {row["pair_id"]: row for row in rows}
    samples = fixture["tokenizer_samples"]
    assert len(samples) == 4
    for sample in samples:
        row = rows_by_id[sample["pair_id"]]
        text = row[f"{sample['side']}_prompt"]
        assert sample["text_sha256"] == hashlib.sha256(text.encode("utf-8")).hexdigest()
        assert sample["char_count"] == len(text)
        assert sample["token_count"] is None

    non_claims = fixture["non_claims"]
    assert non_claims["model_scores"] == "NOT_PRODUCED"
    assert non_claims["benchmark_execution"] == "NOT_EXECUTED"
    assert non_claims["streaming_parity"] == "NOT_VALIDATED"


def test_offline_fixture_telemetry_cases_match_runtime_parser(monkeypatch: pytest.MonkeyPatch) -> None:
    fixture = _fixture()
    settings = GenerationSettings()
    for case in fixture["telemetry_cases"]:
        payload = case["payload"]
        expected = case["expected"]
        monkeypatch.setattr("urllib.request.urlopen", lambda *_args, _payload=payload, **_kwargs: _Response(_payload))
        if expected["accepted"]:
            result = OllamaRuntime().generate("fixture", "prompt", settings)
            assert result.eval_tokens == expected["eval_tokens"]
            assert result.tokens_per_second == expected["tokens_per_second"]
            assert result.runtime_metadata["eval_duration"] == payload["eval_duration"]
        else:
            with pytest.raises(RuntimeFailure, match=expected["error"]):
                OllamaRuntime().generate("fixture", "prompt", settings)
