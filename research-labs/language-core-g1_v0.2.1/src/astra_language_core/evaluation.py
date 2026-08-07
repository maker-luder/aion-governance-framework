from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .dataset import PromptPair
from .errors import ArtifactExistsError
from .json_types import JsonValue
from .metrics import (
    completion_success,
    constraint_scores,
    loop_detected,
    repeated_ngram_ratio,
    script_counts,
    terminology_scores,
)
from .models import GenerationSettings
from .runtime import Runtime


@dataclass(frozen=True, slots=True)
class EvaluationRun:
    run_id: str
    model_id: str
    model_name: str
    settings: GenerationSettings


def evaluate(run: EvaluationRun, pairs: list[PromptPair], runtime: Runtime, output: Path) -> Path:
    if output.exists():
        raise ArtifactExistsError(f"run artifact already exists: {output}")
    records: list[JsonValue] = []
    for pair in pairs:
        for script, prompt in (("zh_tw", pair.zh_tw_prompt), ("zh_cn", pair.zh_cn_prompt)):
            result = runtime.generate(run.model_name, prompt, run.settings)
            metrics: dict[str, JsonValue] = {
                "completion_success": completion_success(result.text),
                "total_latency_seconds": result.total_latency_seconds,
                "time_to_first_token_seconds": result.time_to_first_token_seconds,
                "eval_tokens": result.eval_tokens,
                "tokens_per_second": result.tokens_per_second,
                "repeated_trigram_ratio": repeated_ngram_ratio(result.text),
                "loop_detected": loop_detected(result.text),
                **script_counts(result.text),
                **terminology_scores(
                    result.text, pair.expected_keywords_tw, pair.forbidden_simplified_terms
                ),
                **constraint_scores(result.text, pair.expected_constraints),
            }
            records.append(
                {
                    "pair_id": pair.pair_id,
                    "category": pair.category,
                    "script": script,
                    "prompt": prompt,
                    "response": result.text,
                    "metrics": metrics,
                    "runtime_metadata": result.runtime_metadata,
                }
            )
    payload: dict[str, JsonValue] = {
        "run_id": run.run_id,
        "model_id": run.model_id,
        "model_name": run.model_name,
        "settings": run.settings.to_dict(),
        "records": records,
        "canonical_effect": "NONE",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return output
