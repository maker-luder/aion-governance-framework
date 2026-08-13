from __future__ import annotations

import json
from pathlib import Path

import pytest

from astra_language_core.dataset import PromptPair
from astra_language_core.errors import ArtifactExistsError
from astra_language_core.evaluation import EvaluationRun, evaluate
from astra_language_core.models import GenerationSettings
from astra_language_core.reports import compare_runs, write_json_report, write_markdown_report
from astra_language_core.runtime import MockRuntime


def pair() -> PromptPair:
    return PromptPair("P1", "general", "繁中", "简中", ("答案",), ("程式",), ("程序",), None, None, "test")


def test_full_mock_evaluation_and_reports(tmp_path: Path) -> None:
    run = EvaluationRun("R1", "G1-BASE", "mock", GenerationSettings(seed=7))
    output = tmp_path / "run.json"
    evaluate(run, [pair()], MockRuntime({"繁中": "答案 程式", "简中": "答案"}), output)
    data = json.loads(output.read_text(encoding="utf-8"))
    assert len(data["records"]) == 2
    assert data["settings"]["seed"] == 7
    with pytest.raises(ArtifactExistsError):
        evaluate(run, [pair()], MockRuntime({}), output)
    comparison = compare_runs(output, output)
    assert comparison["baseline_record_count"] == 2
    json_path = write_json_report(comparison, tmp_path / "comparison.json")
    md_path = write_markdown_report(comparison, tmp_path / "comparison.md")
    assert json_path.exists() and "QA_HOLD" in md_path.read_text(encoding="utf-8")
    with pytest.raises(ArtifactExistsError):
        write_json_report(comparison, json_path)
