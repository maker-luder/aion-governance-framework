from __future__ import annotations

import json
from pathlib import Path

from astra_language_core.cli import main

ROOT = Path(__file__).resolve().parents[1]


def test_cli_dataset_and_hash(tmp_path: Path, capsys: object) -> None:
    row = {
        "pair_id": "P",
        "category": "general",
        "zh_tw_prompt": "甲",
        "zh_cn_prompt": "甲",
        "expected_constraints": [],
        "expected_keywords_tw": [],
        "forbidden_simplified_terms": [],
        "reference_answer_optional": None,
        "executable_test_optional": None,
        "notes": "test",
    }
    dataset = tmp_path / "d.jsonl"
    dataset.write_text(json.dumps(row, ensure_ascii=False), encoding="utf-8")
    assert main(["validate-dataset", "--path", str(dataset)]) == 0
    assert main(["hash-model", "--path", str(dataset)]) == 0


def test_cli_error(tmp_path: Path) -> None:
    assert main(["validate-dataset", "--path", str(tmp_path / "missing")]) == 2


def test_cli_end_to_end_mock_workflow(tmp_path: Path) -> None:
    registry = tmp_path / "registry.json"
    models = ROOT / "configs" / "astra_language_core" / "models.example.yaml"
    dataset = ROOT / "data" / "astra_language_core" / "prompts" / "zh_tw_zh_cn_pairs.jsonl"
    evaluation = ROOT / "configs" / "astra_language_core" / "evaluation.example.yaml"
    run = tmp_path / "run.json"
    comparison = tmp_path / "comparison.json"
    markdown = tmp_path / "comparison.md"
    assert main(["init-lab", "--models", str(models), "--output", str(registry)]) == 0
    assert len(json.loads(registry.read_text(encoding="utf-8"))) == 5
    assert (
        main(
            [
                "run-eval",
                "--config",
                str(evaluation),
                "--dataset",
                str(dataset),
                "--output",
                str(run),
            ]
        )
        == 0
    )
    assert (
        main(
            [
                "compare-runs",
                "--baseline",
                str(run),
                "--candidate",
                str(run),
                "--output",
                str(comparison),
            ]
        )
        == 0
    )
    assert main(["build-report", "--input", str(comparison), "--output", str(markdown)]) == 0
    assert "QA_HOLD" in markdown.read_text(encoding="utf-8")
    assert main(["qa-status", "--model", str(models)]) == 2
    assert main(["hash-model", "--path", str(tmp_path)]) == 0
