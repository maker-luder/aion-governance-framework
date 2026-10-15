"""限制範圍的 C++／Python 一致性檢查；在 CI 缺少編譯器時明確失敗。"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_cpp_connectivity_probe_matches_python_reference() -> None:
    """編譯暫存 C++ 函式，對照既有 CCTS Python 連通性判定。"""
    root = Path(__file__).resolve().parents[1]
    runner = root / "experiments" / "ccts-cpp-connectivity-probe_v0.1.0" / "probe.py"
    result = subprocess.run(
        [sys.executable, str(runner), "--random-cases", "320", "--benchmark-iterations", "0"],
        check=True,
        capture_output=True,
        text=True,
        timeout=90,
    )
    report = json.loads(result.stdout)
    assert report["status"] == "LOCAL_SYNTHETIC_PARITY_PASS"
    assert report["case_count"] == 327
    assert report["invalid_input_checks"] == 4
    assert report["scope"] == "UNDIRECTED_GRAPH_CONNECTIVITY_ONLY"
    assert report["ccts_admission_unchanged"] is True
    assert report["scientific_validation"] == "NOT_ESTABLISHED"
