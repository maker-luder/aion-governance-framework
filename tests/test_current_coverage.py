from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]


def load_coverage_module() -> ModuleType:
    path = ROOT / "scripts" / "run_current_coverage.py"
    spec = importlib.util.spec_from_file_location("run_current_coverage_for_test", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_malformed_coverage_json_fails_closed_with_record(tmp_path: Path, monkeypatch) -> None:
    module = load_coverage_module()
    target = tmp_path / "components" / "example"
    (target / "src").mkdir(parents=True)
    (target / "tests").mkdir()
    monkeypatch.setattr(module, "ROOT", tmp_path)
    monkeypatch.setattr(module, "TARGETS", (target,))
    monkeypatch.setattr(module, "SOURCE_ROOTS", [])

    class Completed:
        returncode = 0
        stdout = "pytest output\n"

    def fake_run(command, **kwargs):
        report_path = Path(next(value[5:] for value in command if value.startswith("json:")))
        report_path.write_text("{malformed", encoding="utf-8")
        return Completed()

    monkeypatch.setattr(module.subprocess, "run", fake_run)

    records, failed = module.collect_current_coverage()

    assert failed == 1
    assert records[0]["returncode"] == 0
    assert records[0]["totals"] == {}
    assert "coverage_error" in records[0]
