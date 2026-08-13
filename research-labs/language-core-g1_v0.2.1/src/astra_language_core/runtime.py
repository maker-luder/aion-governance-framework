from __future__ import annotations

import json
import math
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Protocol

from .errors import RuntimeFailure, ValidationError
from .json_types import JsonValue
from .models import CompletionResult, GenerationSettings


class Runtime(Protocol):
    def generate(self, model_name: str, prompt: str, settings: GenerationSettings) -> CompletionResult:
        """Generate one completion without modifying model state."""


@dataclass(slots=True)
class MockRuntime:
    responses: dict[str, str]
    default_response: str = "MOCK_RESPONSE"

    def generate(self, model_name: str, prompt: str, settings: GenerationSettings) -> CompletionResult:
        del model_name, settings
        text = self.responses.get(prompt, self.default_response)
        return CompletionResult(text=text, total_latency_seconds=0.001, eval_tokens=len(text.split()))


class OllamaRuntime:
    def __init__(self, base_url: str = "http://127.0.0.1:11434", timeout_seconds: float = 30.0) -> None:
        parsed = urllib.parse.urlparse(base_url)
        if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
            raise ValidationError("OllamaRuntime permits only local HTTP loopback URLs")
        if parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise ValidationError("Ollama base URL must not contain credentials, query, or fragment")
        if timeout_seconds <= 0:
            raise ValidationError("timeout_seconds must be positive")
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def generate(self, model_name: str, prompt: str, settings: GenerationSettings) -> CompletionResult:
        payload: dict[str, JsonValue] = {
            "model": model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "seed": settings.seed,
                "temperature": settings.temperature,
                "top_p": settings.top_p,
                "top_k": settings.top_k,
                "repeat_penalty": settings.repeat_penalty,
                "num_ctx": settings.num_ctx,
                "num_predict": settings.max_output_tokens,
            },
        }
        request = urllib.request.Request(
            f"{self.base_url}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        started = time.perf_counter()
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:  # noqa: S310
                body = response.read()
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise RuntimeFailure(f"local Ollama request failed: {exc}") from exc
        latency = time.perf_counter() - started
        try:
            decoded: JsonValue = json.loads(body)
        except json.JSONDecodeError as exc:
            raise RuntimeFailure("Ollama returned invalid JSON") from exc
        if not isinstance(decoded, dict):
            raise RuntimeFailure("Ollama response must be an object")
        response_text = decoded.get("response")
        if not isinstance(response_text, str):
            raise RuntimeFailure("Ollama response missing text")
        eval_count = decoded.get("eval_count")
        eval_duration = decoded.get("eval_duration")
        tokens: int | None = None
        if eval_count is not None:
            if isinstance(eval_count, bool) or not isinstance(eval_count, int) or eval_count < 0:
                raise RuntimeFailure("Ollama response has invalid telemetry")
            tokens = eval_count

        rate: float | None = None
        if eval_duration is not None:
            if isinstance(eval_duration, bool) or not isinstance(eval_duration, int | float):
                raise RuntimeFailure("Ollama response has invalid telemetry")
            try:
                duration_seconds = float(eval_duration) / 1_000_000_000
            except (OverflowError, ValueError) as exc:
                raise RuntimeFailure("Ollama response has invalid telemetry") from exc
            if not math.isfinite(duration_seconds) or duration_seconds <= 0:
                raise RuntimeFailure("Ollama response has invalid telemetry")
            if tokens is not None:
                try:
                    rate = tokens / duration_seconds
                except (OverflowError, ZeroDivisionError) as exc:
                    raise RuntimeFailure("Ollama response has invalid telemetry") from exc
                if not math.isfinite(rate):
                    raise RuntimeFailure("Ollama response has invalid telemetry")
        return CompletionResult(
            text=response_text,
            total_latency_seconds=latency,
            eval_tokens=tokens,
            tokens_per_second=rate,
            runtime_metadata={"done": decoded.get("done"), "eval_duration": eval_duration},
        )
