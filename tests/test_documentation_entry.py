from __future__ import annotations

from pathlib import Path

from scripts.validate_documentation_entry import validate


def test_documentation_entry_contract() -> None:
    root = Path(__file__).resolve().parents[1]
    assert validate(root) == []
