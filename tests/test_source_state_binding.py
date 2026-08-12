from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path


def _load_checker():
    script = Path(__file__).resolve().parents[1] / "scripts" / "check_source_state_binding.py"
    spec = importlib.util.spec_from_file_location("check_source_state_binding", script)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


checker = _load_checker()


def _git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


def _repo(tmp_path: Path) -> tuple[Path, str]:
    root = tmp_path / "repo"
    root.mkdir()
    (root / "components" / "example").mkdir(parents=True)
    (root / "components" / "example" / "README.md").write_text("source\n", encoding="utf-8")
    (root / "qa").mkdir()
    (root / "qa" / "CURRENT_TEST_RESULTS.json").write_text("[]\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.email", "iqc-test@example.invalid"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "IQC Test"], cwd=root, check=True)
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "commit", "-qm", "fixture"], cwd=root, check=True)
    return root, _git(root, "rev-parse", "HEAD")


def test_exact_committed_head_passes(tmp_path: Path) -> None:
    root, head = _repo(tmp_path)
    result = checker.inspect_source_state(root, head)
    assert result["status"] == "PASS"
    assert result["actual_head"] == head
    assert result["source_dirty_paths"] == []


def test_declared_head_mismatch_holds(tmp_path: Path) -> None:
    root, _ = _repo(tmp_path)
    result = checker.inspect_source_state(root, "0" * 40)
    assert result["status"] == "HOLD"
    assert "differs from actual Git HEAD" in result["reason"]


def test_non_qa_worktree_drift_holds(tmp_path: Path) -> None:
    root, head = _repo(tmp_path)
    (root / "components" / "example" / "README.md").write_text("mutated\n", encoding="utf-8")
    result = checker.inspect_source_state(root, head)
    assert result["status"] == "HOLD"
    assert result["source_dirty_paths"] == ["components/example/README.md"]


def test_governed_qa_output_is_allowed(tmp_path: Path) -> None:
    root, head = _repo(tmp_path)
    (root / "qa" / "CURRENT_TEST_RESULTS.json").write_text("[{}]\n", encoding="utf-8")
    result = checker.inspect_source_state(root, head)
    assert result["status"] == "PASS"
    assert result["governed_qa_mutation_paths"] == ["qa/CURRENT_TEST_RESULTS.json"]


def test_staged_change_holds_even_when_qa_path(tmp_path: Path) -> None:
    root, head = _repo(tmp_path)
    (root / "qa" / "CURRENT_TEST_RESULTS.json").write_text("[{}]\n", encoding="utf-8")
    subprocess.run(["git", "add", "qa/CURRENT_TEST_RESULTS.json"], cwd=root, check=True)
    result = checker.inspect_source_state(root, head)
    assert result["status"] == "HOLD"
    assert result["staged_paths"] == ["qa/CURRENT_TEST_RESULTS.json"]
