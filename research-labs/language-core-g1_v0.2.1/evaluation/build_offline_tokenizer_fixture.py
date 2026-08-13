from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

FIXTURE_SCHEMA = "g1.offline-tokenizer-telemetry.v1"
SAMPLE_LIMIT = 2

TELEMETRY_CASES: tuple[dict[str, object], ...] = (
    {
        "case_id": "valid_non_streaming_nanoseconds",
        "payload": {
            "response": "fixture response",
            "eval_count": 20,
            "eval_duration": 2_000_000_000,
            "done": True,
        },
        "expected": {
            "accepted": True,
            "eval_tokens": 20,
            "duration_seconds": 2.0,
            "tokens_per_second": 10.0,
            "duration_unit": "nanoseconds",
        },
    },
    {
        "case_id": "malformed_boolean_eval_count",
        "payload": {
            "response": "fixture response",
            "eval_count": True,
            "eval_duration": 1_000_000_000,
        },
        "expected": {"accepted": False, "error": "invalid telemetry"},
    },
    {
        "case_id": "malformed_zero_eval_duration",
        "payload": {
            "response": "fixture response",
            "eval_count": 2,
            "eval_duration": 0,
        },
        "expected": {"accepted": False, "error": "invalid telemetry"},
    },
    {
        "case_id": "malformed_string_eval_duration",
        "payload": {
            "response": "fixture response",
            "eval_count": 2,
            "eval_duration": "1",
        },
        "expected": {"accepted": False, "error": "invalid telemetry"},
    },
)


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_text(value: str) -> str:
    return _sha256_bytes(value.encode("utf-8"))


def _load_rows(dataset_path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for line_number, line in enumerate(dataset_path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"dataset line {line_number} must be an object")
        rows.append(value)
    if len(rows) < SAMPLE_LIMIT:
        raise ValueError(f"dataset must contain at least {SAMPLE_LIMIT} non-empty rows")
    return rows


def build_fixture(dataset_path: Path) -> dict[str, object]:
    rows = _load_rows(dataset_path)
    samples: list[dict[str, object]] = []
    for row in rows[:SAMPLE_LIMIT]:
        pair_id = row.get("pair_id")
        zh_tw_prompt = row.get("zh_tw_prompt")
        zh_cn_prompt = row.get("zh_cn_prompt")
        if not isinstance(pair_id, str) or not isinstance(zh_tw_prompt, str) or not isinstance(zh_cn_prompt, str):
            raise ValueError("sample rows must contain string pair_id and paired prompts")
        samples.extend(
            (
                {
                    "pair_id": pair_id,
                    "side": "zh_tw",
                    "text_sha256": _sha256_text(zh_tw_prompt),
                    "char_count": len(zh_tw_prompt),
                    "token_count": None,
                },
                {
                    "pair_id": pair_id,
                    "side": "zh_cn",
                    "text_sha256": _sha256_text(zh_cn_prompt),
                    "char_count": len(zh_cn_prompt),
                    "token_count": None,
                },
            )
        )
    return {
        "schema_version": FIXTURE_SCHEMA,
        "fixture_status": "OFFLINE_CONTRACT_ONLY",
        "model_execution_required": False,
        "tokenizer_execution_status": "NOT_EXECUTED",
        "dataset_sha256": _sha256_bytes(dataset_path.read_bytes()),
        "sample_selection": "first_two_nonblank_dataset_rows",
        "tokenizer_samples": samples,
        "telemetry_transport": {
            "endpoint": "/api/generate",
            "stream": False,
            "duration_unit": "nanoseconds",
        },
        "telemetry_cases": list(TELEMETRY_CASES),
        "non_claims": {
            "token_counts": "NOT_PRODUCED",
            "model_scores": "NOT_PRODUCED",
            "benchmark_execution": "NOT_EXECUTED",
            "scientific_conclusion": "NOT_ESTABLISHED",
            "streaming_parity": "NOT_VALIDATED",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a model-free G1 tokenizer/telemetry contract fixture")
    parser.add_argument(
        "--dataset",
        type=Path,
        default=Path("data/language_core_g1/PAIRED_ZH_DATASET_V1.jsonl"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("evaluation/OFFLINE_TOKENIZER_TELEMETRY_FIXTURE.json"),
    )
    args = parser.parse_args()
    fixture = build_fixture(args.dataset)
    args.output.write_text(json.dumps(fixture, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
