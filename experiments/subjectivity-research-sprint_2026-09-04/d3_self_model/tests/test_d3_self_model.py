from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

from analyze import analyze  # noqa: E402


def test_self_model_specific_effect_not_smuggled_as_subjectivity() -> None:
    report = analyze()
    assert report["SUBJECTIVITY_CONCLUSION"] == "NOT_ESTABLISHED"
    assert report["self_model_specific_effect_observed"] is False
    assert report["result_status"] == "NOT_SUPPORTED"
