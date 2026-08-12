from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


EXCLUDED_RELATIVE_PATHS = {"manifest/FILE_MANIFEST.json", "manifest/SHA256SUMS.txt"}
EXCLUDED_DIR_NAMES = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
EXCLUDED_DIR_SUFFIXES = (".egg-info",)
EXCLUDED_FILE_NAMES = {".coverage"}


class ManifestIntegrityError(ValueError):
    """Raised when a manifest does not describe the current tree."""


def _relative_exclusions(root: Path, manifest_dir: Path | None) -> set[str]:
    exclusions = set(EXCLUDED_RELATIVE_PATHS)
    if manifest_dir is not None:
        try:
            relative = manifest_dir.resolve().relative_to(root.resolve()).as_posix()
        except ValueError:
            return exclusions
        exclusions.update({f"{relative}/FILE_MANIFEST.json", f"{relative}/SHA256SUMS.txt"})
    return exclusions


def iter_manifest_files(root: Path, *, excluded_paths: set[str] | None = None) -> Iterable[Path]:
    root = root.resolve()
    excluded = excluded_paths or set(EXCLUDED_RELATIVE_PATHS)
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        parts = path.relative_to(root).parts
        if any(part in EXCLUDED_DIR_NAMES or part.endswith(EXCLUDED_DIR_SUFFIXES) for part in parts):
            continue
        if path.name in EXCLUDED_FILE_NAMES or path.suffix == ".pyc":
            continue
        relative = path.relative_to(root).as_posix()
        if relative in excluded:
            continue
        yield path


def build_entries(root: Path, *, excluded_paths: set[str] | None = None) -> list[dict[str, Any]]:
    root = root.resolve()
    return [
        {
            "path": path.relative_to(root).as_posix(),
            "size": len(path.read_bytes()),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
        for path in iter_manifest_files(root, excluded_paths=excluded_paths)
    ]


def write_manifest(root: Path, output_dir: Path | None = None) -> int:
    root = root.resolve()
    manifest_dir = (output_dir or (root / "manifest")).resolve()
    manifest_dir.mkdir(parents=True, exist_ok=True)
    entries = build_entries(root, excluded_paths=_relative_exclusions(root, manifest_dir))
    (manifest_dir / "FILE_MANIFEST.json").write_text(
        json.dumps({"schema_version": "1.0", "scope": "CURRENT_REVIEW_TREE", "files": entries}, indent=2) + "\n",
        encoding="utf-8",
    )
    (manifest_dir / "SHA256SUMS.txt").write_text(
        "".join(f"{item['sha256']} {item['path']}\n" for item in entries),
        encoding="utf-8",
    )
    return len(entries)


def _load_manifest(path: Path) -> list[dict[str, Any]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ManifestIntegrityError(f"cannot read manifest: {path}") from exc
    if payload.get("schema_version") != "1.0" or not isinstance(payload.get("files"), list):
        raise ManifestIntegrityError("unsupported manifest schema")
    return payload["files"]


def _load_checksums(path: Path) -> dict[str, str]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise ManifestIntegrityError(f"cannot read checksum file: {path}") from exc
    checksums: dict[str, str] = {}
    for line in lines:
        if not line.strip():
            continue
        parts = line.split(" ", 1)
        if len(parts) != 2 or len(parts[0]) != 64:
            raise ManifestIntegrityError(f"malformed checksum line: {line!r}")
        digest, relative = parts
        if relative in checksums:
            raise ManifestIntegrityError(f"duplicate checksum path: {relative}")
        checksums[relative] = digest
    return checksums


def verify_manifest(root: Path, manifest_dir: Path | None = None) -> dict[str, int | str]:
    root = root.resolve()
    directory = (manifest_dir or (root / "manifest")).resolve()
    manifest_path = directory / "FILE_MANIFEST.json"
    checksum_path = directory / "SHA256SUMS.txt"
    exclusions = _relative_exclusions(root, directory)
    records = _load_manifest(manifest_path)
    checksums = _load_checksums(checksum_path)
    record_map: dict[str, dict[str, Any]] = {}
    for record in records:
        relative = record.get("path")
        if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
            raise ManifestIntegrityError(f"invalid manifest path: {relative!r}")
        if relative in record_map:
            raise ManifestIntegrityError(f"duplicate manifest path: {relative}")
        if record.get("size", -1) < 0 or not isinstance(record.get("sha256"), str):
            raise ManifestIntegrityError(f"invalid manifest record: {relative}")
        record_map[relative] = record
    actual_paths = {path.relative_to(root).as_posix() for path in iter_manifest_files(root, excluded_paths=exclusions)}
    manifest_paths = set(record_map)
    if actual_paths != manifest_paths:
        raise ManifestIntegrityError(f"closed-set drift: missing={sorted(actual_paths - manifest_paths)!r} stale={sorted(manifest_paths - actual_paths)!r}")
    if set(checksums) != manifest_paths:
        raise ManifestIntegrityError(f"checksum closed-set drift: missing={sorted(manifest_paths - set(checksums))!r} stale={sorted(set(checksums) - manifest_paths)!r}")
    verified = 0
    for relative in sorted(manifest_paths):
        path = root / relative
        data = path.read_bytes()
        actual_sha = hashlib.sha256(data).hexdigest()
        record = record_map[relative]
        if record["size"] != len(data) or record["sha256"] != actual_sha or checksums[relative] != actual_sha:
            raise ManifestIntegrityError(f"content mismatch: {relative}")
        verified += 1
    return {"schema_version": "1.0", "files": verified, "status": "PASS", "manifest_dir": str(directory.relative_to(root)) if directory.is_relative_to(root) else str(directory)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify a versioned repository manifest closed-set and content integrity")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--manifest-dir", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--generate", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    directory = args.output_dir or args.manifest_dir
    if args.generate:
        print(f"generated={write_manifest(root, directory)}")
    result = verify_manifest(root, directory)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
