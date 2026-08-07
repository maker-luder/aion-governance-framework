"""Deterministic candidate packaging with manifest, SHA-256 and CRC32."""

from __future__ import annotations

import hashlib
import json
import zipfile
import zlib
from pathlib import Path

from .errors import PackagingError
from .file_index import index_workspace
from .models import PackageCandidate

CONTROL_EXCLUSIONS = {
    "__pycache__", ".pytest_cache", ".mypy_cache", "build", "dist", ".astra_meta"
}


def build_package(
    *,
    task_id: str,
    package_id: str,
    source_root: Path,
    destination: Path,
) -> PackageCandidate:
    if destination.exists():
        raise PackagingError("historical or existing package cannot be overwritten")
    records: list[dict[str, str | int]] = [
        {"path": path, "size": size, "sha256": digest}
        for path, size, digest in index_workspace(source_root)
        if not any(part in CONTROL_EXCLUSIONS for part in Path(path).parts)
    ]
    manifest_bytes = (
        json.dumps(records, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    manifest_hash = hashlib.sha256(manifest_bytes).hexdigest()
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "x", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("MANIFEST.json", manifest_bytes)
        archive.writestr(
            "SHA256SUMS.txt",
            "".join(f"{item['sha256']}  {item['path']}\n" for item in records),
        )
        archive.writestr(
            "CRC32SUMS.txt",
            "".join(
                f"{zlib.crc32((source_root / str(item['path'])).read_bytes()) & 0xffffffff:08x}  {item['path']}\n"
                for item in records
            ),
        )
        for item in records:
            archive.write(source_root / str(item["path"]), str(item["path"]))
    package_hash = hashlib.sha256(destination.read_bytes()).hexdigest()
    return PackageCandidate(
        package_id=package_id,
        task_id=task_id,
        path=str(destination),
        manifest_hash=manifest_hash,
        package_hash=package_hash,
    )


def verify_package(path: Path) -> dict[str, object]:
    with zipfile.ZipFile(path) as archive:
        bad = archive.testzip()
        manifest = json.loads(archive.read("MANIFEST.json"))
        mismatches: list[str] = []
        for item in manifest:
            actual = hashlib.sha256(archive.read(item["path"])).hexdigest()
            if actual != item["sha256"]:
                mismatches.append(item["path"])
        return {
            "zip": path.name,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "entry_count": len(archive.infolist()),
            "manifest_count": len(manifest),
            "crc_pass": bad is None,
            "hash_pass": not mismatches,
            "mismatches": mismatches,
        }
