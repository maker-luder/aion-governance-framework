from __future__ import annotations

from pathlib import Path

import pytest

from aion_evidence_interop.canonical import InteropError, validate_source_record


COMPONENT = Path(__file__).resolve().parents[1]
ROOT = COMPONENT.parents[1]


def test_source_record_must_be_repository_local(tmp_path: Path) -> None:
    external = tmp_path / "record.json"
    external.write_text("{}")
    with pytest.raises(InteropError, match="repository-local"):
        validate_source_record(
            ROOT,
            external,
            expected_head="a" * 40,
        )
