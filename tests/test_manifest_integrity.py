from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import manifest_integrity as integrity  # noqa: E402


def make_manifest_root(tmp_path: Path) -> tuple[Path, Path]:
    root = tmp_path / "repo"
    root.mkdir()
    (root / "payload.txt").write_text("payload\n", encoding="utf-8")
    control_dir = root / "controls"
    integrity.write_manifest(root, control_dir)
    return root, control_dir


@pytest.mark.parametrize("boolean_size", [False, True])
def test_manifest_rejects_boolean_size_as_invalid_control_file(
    tmp_path: Path, boolean_size: bool
) -> None:
    root, control_dir = make_manifest_root(tmp_path)
    manifest_path = control_dir / "FILE_MANIFEST.json"
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    payload["files"][0]["size"] = boolean_size
    manifest_path.write_text(json.dumps(payload), encoding="utf-8")

    issues = integrity.verify_manifest(root, manifest_dir=control_dir)

    assert len(issues) == 1
    assert issues[0].code == "INVALID_CONTROL_FILE"
    assert "invalid or duplicate record" in issues[0].detail


def test_manifest_accepts_non_negative_integer_size(tmp_path: Path) -> None:
    root, control_dir = make_manifest_root(tmp_path)

    assert integrity.verify_manifest(root, manifest_dir=control_dir) == ()
