from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


EXCLUDED_RELATIVE_PATHS = {
    "manifest/FILE_MANIFEST.json",
    "manifest/SHA256SUMS.txt",
}
EXCLUDED_DIR_NAMES = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
EXCLUDED_DIR_SUFFIXES = (".egg-info",)
EXCLUDED_FILE_NAMES = {".coverage"}


class ManifestIntegrityError(ValueError):
    """Raised when the repository manifest does not describe the current tree."""


def iter_manifest_files(root: Path) -> Iterable[Path]:
    root = root.resolve()
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        parts = path.relative_to(root).parts
        if any(part in EXCLUDED_DIR_NAMES or part.endswith(EXCLUDED_DIR_SUFFIXES) for part in parts):
            continue
        if path.name in EXCLUDED_FILE_NAMES or path.suffix == ".pyc":
            continue
        relative = path.relative_to(root).as_posix()
        if relative in EXCLUDED_RELATIVE_PATHS:
            continue
        yield path


def build_entries(root: Path) -> list[dict[str, Any]]:
    root = root.resolve()
    entries: list[dict[str, Any]] = []
    for path in iter_manifest_files(root):
        data = path.read_bytes()
        entries.append(
            {
                "path": path.relative_to(root).as_posix(),
                "size": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    return entries


def write_manifest(root: Path) -> int:
    root = root.resolve()
    manifest_dir = root / "manifest"
    manifest_dir.mkdir(exist_ok=True)
    entries = build_entries(root)
    (manifest_dir / "FILE_MANIFEST.json").write_text(
        json.dumps({"schema_version": "1.0", "files": entries}, indent=2) + "\n",
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


def verify_manifest(root: Path) -> dict[str, int | str]:
    root = root.resolve()
    manifest_path = root / "manifest/FILE_MANIFEST.json"
    checksum_path = root / "manifest/SHA256SUMS.txt"
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

    actual_paths = {path.relative_to(root).as_posix() for path in iter_manifest_files(root)}
    manifest_paths = set(record_map)
    if actual_paths != manifest_paths:
        missing = sorted(actual_paths - manifest_paths)
        stale = sorted(manifest_paths - actual_paths)
        raise ManifestIntegrityError(f"closed-set drift: missing={missing!r} stale={stale!r}")
    if set(checksums) != manifest_paths:
        missing = sorted(manifest_paths - set(checksums))
        stale = sorted(set(checksums) - manifest_paths)
        raise ManifestIntegrityError(f"checksum closed-set drift: missing={missing!r} stale={stale!r}")

    verified = 0
    for relative in sorted(manifest_paths):
        path = root / relative
        data = path.read_bytes()
        actual_size = len(data)
        actual_sha = hashlib.sha256(data).hexdigest()
        record = record_map[relative]
        if record["size"] != actual_size:
            raise ManifestIntegrityError(f"size mismatch: {relative}")
        if record["sha256"] != actual_sha:
            raise ManifestIntegrityError(f"manifest hash mismatch: {relative}")
        if checksums[relative] != actual_sha:
            raise ManifestIntegrityError(f"checksum mismatch: {relative}")
        verified += 1
    return {"schema_version": "1.0", "files": verified, "status": "PASS"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify repository manifest closed-set and content integrity")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--generate", action="store_true", help="write current manifest before verification")
    args = parser.parse_args()
    if args.generate:
        print(f"generated={write_manifest(args.root)}")
    result = verify_manifest(args.root)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
