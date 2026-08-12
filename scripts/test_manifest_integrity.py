from __future__ import annotations

import hashlib
import json
from pathlib import Path

from manifest_integrity import verify_manifest


def _write_controls(
    root: Path,
    *,
    output_dir: Path | None = None,
    checksum_override: str | None = None,
) -> tuple[Path, Path]:
    output_dir = output_dir or root / "manifest"
    files = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        if output_dir in path.parents or path.parent == output_dir:
            continue
        if any(
            part in {"build", "dist", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
            or part.endswith(".egg-info")
            for part in path.parts
        ):
            continue
        if path.name == ".coverage" or path.suffix == ".pyc":
            continue
        relative = path.relative_to(root).as_posix()
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        files.append({"path": relative, "size": path.stat().st_size, "sha256": digest})
    manifest = output_dir / "FILE_MANIFEST.json"
    sums = output_dir / "SHA256SUMS.txt"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        json.dumps({"schema_version": "2.0", "files": files}) + "\n",
        encoding="utf-8",
    )
    sums.write_text(
        "".join(
            f"{(checksum_override if index == 0 and checksum_override else item['sha256'])}  {item['path']}\n"
            for index, item in enumerate(files)
        ),
        encoding="utf-8",
    )
    return manifest, sums


def test_manifest_verification_requires_a_closed_current_file_set(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("a", encoding="utf-8")
    (tmp_path / "b.txt").write_text("b", encoding="utf-8")
    _write_controls(tmp_path)
    assert verify_manifest(tmp_path) == ()

    (tmp_path / "a.txt").unlink()
    (tmp_path / "c.txt").write_text("c", encoding="utf-8")
    codes = {issue.code for issue in verify_manifest(tmp_path)}
    assert codes == {"MISSING_FROM_TREE", "UNTRACKED_IN_MANIFEST"}


def test_manifest_verification_detects_file_hash_and_size_drift(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("a", encoding="utf-8")
    _write_controls(tmp_path)
    (tmp_path / "a.txt").write_text("changed", encoding="utf-8")
    codes = {issue.code for issue in verify_manifest(tmp_path)}
    assert {"SIZE_MISMATCH", "HASH_MISMATCH"}.issubset(codes)


def test_manifest_verification_detects_checksum_sidecar_drift(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("a", encoding="utf-8")
    _write_controls(tmp_path, checksum_override="0" * 64)
    codes = {issue.code for issue in verify_manifest(tmp_path)}
    assert "CHECKSUM_HASH_MISMATCH" in codes


def test_manifest_verification_ignores_generated_metadata(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("a", encoding="utf-8")
    generated = [
        tmp_path / "aion_example.egg-info/METADATA",
        tmp_path / "build/a/artifact.txt",
        tmp_path / "dist/artifact.whl",
        tmp_path / ".coverage",
    ]
    for path in generated:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("generated metadata", encoding="utf-8")
    _write_controls(tmp_path)
    assert verify_manifest(tmp_path) == ()


def test_explicit_non_frozen_control_dir_does_not_self_reference(tmp_path: Path) -> None:
    (tmp_path / "src.txt").write_text("source", encoding="utf-8")
    output = tmp_path / "candidate-manifest-v2"
    manifest, sums = _write_controls(tmp_path, output_dir=output)
    assert verify_manifest(tmp_path, manifest, sums) == ()
