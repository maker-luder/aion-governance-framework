from __future__ import annotations

import io
import json

import pytest

from astra_language_core.errors import RuntimeFailure, ValidationError
from astra_language_core.metrics import (
    completion_success,
    constraint_scores,
    loop_detected,
    repeated_ngram_ratio,
    script_counts,
    terminology_scores,
    uncertainty_acknowledged,
)
from astra_language_core.models import GenerationSettings
from astra_language_core.runtime import MockRuntime, OllamaRuntime


class _Response:
    def __init__(self, payload: object) -> None:
        self.buffer = io.BytesIO(json.dumps(payload).encode())

    def __enter__(self) -> _Response:
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def read(self) -> bytes:
        return self.buffer.read()


def test_mock_runtime() -> None:
    runtime = MockRuntime({"p": "回答"})
    assert runtime.generate("m", "p", GenerationSettings()).text == "回答"
    assert runtime.generate("m", "other", GenerationSettings()).text == "MOCK_RESPONSE"


@pytest.mark.parametrize(
    "url", ["https://127.0.0.1:11434", "http://example.com", "http://user:x@localhost"]
)
def test_ollama_rejects_nonlocal_or_credentials(url: str) -> None:
    with pytest.raises(ValidationError):
        OllamaRuntime(url)


def test_ollama_success(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_open(_request: object, timeout: float) -> _Response:
        assert timeout == 2
        return _Response(
            {"response": "ok", "eval_count": 20, "eval_duration": 2_000_000_000, "done": True}
        )

    monkeypatch.setattr("urllib.request.urlopen", fake_open)
    result = OllamaRuntime(timeout_seconds=2).generate("local", "prompt", GenerationSettings())
    assert result.text == "ok"
    assert result.tokens_per_second == 10


def test_ollama_timeout_and_bad_response(monkeypatch: pytest.MonkeyPatch) -> None:
    def timeout(*_args: object, **_kwargs: object) -> _Response:
        raise TimeoutError("late")

    monkeypatch.setattr("urllib.request.urlopen", timeout)
    with pytest.raises(RuntimeFailure, match="failed"):
        OllamaRuntime().generate("m", "p", GenerationSettings())

    monkeypatch.setattr("urllib.request.urlopen", lambda *_a, **_k: _Response({"missing": True}))
    with pytest.raises(RuntimeFailure, match="missing"):
        OllamaRuntime().generate("m", "p", GenerationSettings())


def test_metrics() -> None:
    assert completion_success(" ok ") and not completion_success(" ")
    assert repeated_ngram_ratio("a b c a b c a b c") > 0
    assert loop_detected("同句。同句。同句。")
    assert script_counts("這个資訊") == {"simplified_markers": 1, "traditional_markers": 3}
    assert (
        terminology_scores("執行程式", ("執行", "程式"), ("运行",))["taiwan_terminology_hit_rate"]
        == 1
    )
    assert constraint_scores("status QA_HOLD", ("status", "QA_HOLD"))["constraint_hits"] == 2
    assert uncertainty_acknowledged("資訊不足，無法判定")


@pytest.mark.parametrize(
    "payload",
    [
        {"response": "ok", "eval_count": True, "eval_duration": 1_000_000_000},
        {"response": "ok", "eval_count": -1, "eval_duration": 1_000_000_000},
        {"response": "ok", "eval_count": 2, "eval_duration": False},
        {"response": "ok", "eval_count": 2, "eval_duration": 0},
        {"response": "ok", "eval_count": 2, "eval_duration": float("nan")},
        {"response": "ok", "eval_count": 2, "eval_duration": float("inf")},
        {"response": "ok", "eval_count": 2, "eval_duration": "1"},
        {"response": "ok", "eval_count": 10**1000, "eval_duration": 1},
    ],
)
def test_ollama_rejects_malformed_numeric_telemetry(
    monkeypatch: pytest.MonkeyPatch, payload: dict[str, object]
) -> None:
    monkeypatch.setattr("urllib.request.urlopen", lambda *_a, **_k: _Response(payload))
    with pytest.raises(RuntimeFailure, match="invalid telemetry"):
        OllamaRuntime().generate("m", "p", GenerationSettings())
