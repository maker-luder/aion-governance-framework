from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]


def load_runner() -> ModuleType:
    path = ROOT / "scripts" / "run_component_tests.py"
    spec = importlib.util.spec_from_file_location("run_component_tests_for_test", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_empty_target_set_fails_closed_and_writes_empty_results(tmp_path: Path, monkeypatch) -> None:
    module = load_runner()
    monkeypatch.setattr(module, "ROOT", tmp_path)
    monkeypatch.setattr(module, "TARGETS", [])
    (tmp_path / "qa").mkdir()

    assert module.main() == 1
    assert (tmp_path / "qa/CURRENT_TEST_RESULTS.json").read_text(encoding="utf-8") == "[]\n"


def test_component_result_preserves_target_and_returncode(tmp_path: Path, monkeypatch) -> None:
    module = load_runner()
    target = tmp_path / "components" / "demo"
    (target / "src").mkdir(parents=True)
    (target / "tests").mkdir()
    monkeypatch.setattr(module, "ROOT", tmp_path)

    class Completed:
        returncode = 0
        stdout = "1 passed\n"

    monkeypatch.setattr(module.subprocess, "run", lambda *args, **kwargs: Completed())

    results = module.run_component_tests([target], tmp_path, [])

    assert results == [{"target": "components/demo", "returncode": 0, "output": "1 passed\n"}]
