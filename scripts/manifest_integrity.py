from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re

SHA256 = re.compile(r"^[0-9a-f]{64}$")
GENERATED_PARTS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "build", "dist"}


def is_generated_path(path: Path) -> bool:
    return (
        any(part in GENERATED_PARTS or part.endswith(".egg-info") for part in path.parts)
        or path.name == ".coverage"
        or path.suffix == ".pyc"
    )


@dataclass(frozen=True, slots=True)
class ManifestIssue:
    code: str
    path: str
    detail: str

    def render(self) -> str:
        return f"{self.code}: {self.path}: {self.detail}"


def _inside(path: Path, directory: Path) -> bool:
    try:
        path.relative_to(directory)
        return True
    except ValueError:
        return False


def public_files(root: Path, *, control_dir: Path | None = None) -> tuple[Path, ...]:
    """Return the public file surface used for a candidate manifest.

    `control_dir` is excluded because the generator writes the manifest and checksum
    sidecar there after measuring the source surface. Excluding the actual control
    directory prevents a self-reference loop without excluding any source directory.
    """

    root = root.resolve()
    control_dir = control_dir.resolve() if control_dir is not None else None
    result: list[Path] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        resolved = path.resolve()
        if control_dir is not None and _inside(resolved, control_dir):
            continue
        if is_generated_path(path):
            continue
        result.append(path)
    return tuple(result)


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_manifest(path: Path) -> tuple[dict[str, object], ...]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read manifest: {path}") from exc
    records = payload.get("files") if isinstance(payload, dict) else None
    if not isinstance(records, list):
        raise ValueError("manifest must contain a files array")
    normalized: list[dict[str, object]] = []
    seen: set[str] = set()
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError(f"manifest record {index} must be an object")
        if set(record) != {"path", "size", "sha256"}:
            raise ValueError(f"manifest record {index} fields drift")
        relative = record.get("path")
        digest = record.get("sha256")
        size = record.get("size")
        if (
            not isinstance(relative, str)
            or not relative
            or Path(relative).is_absolute()
            or ".." in Path(relative).parts
        ):
            raise ValueError(f"manifest record {index} has unsafe path")
        if relative in seen:
            raise ValueError(f"manifest contains duplicate path: {relative}")
        if not isinstance(size, int) or size < 0:
            raise ValueError(f"manifest record {index} has invalid size")
        if not isinstance(digest, str) or SHA256.fullmatch(digest) is None:
            raise ValueError(f"manifest record {index} has invalid sha256")
        seen.add(relative)
        normalized.append({"path": relative, "size": size, "sha256": digest})
    return tuple(normalized)


def _load_sums(path: Path) -> dict[str, str]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise ValueError(f"cannot read checksum file: {path}") from exc
    result: dict[str, str] = {}
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        parts = line.split("  ", 1)
        if len(parts) != 2 or SHA256.fullmatch(parts[0]) is None or not parts[1]:
            raise ValueError(f"invalid checksum line {line_number}")
        digest, relative = parts
        if relative in result:
            raise ValueError(f"checksum file contains duplicate path: {relative}")
        result[relative] = digest
    return result


def verify_manifest(
    root: Path,
    manifest_path: Path | None = None,
    sums_path: Path | None = None,
) -> tuple[ManifestIssue, ...]:
    """Verify a candidate manifest, checksum sidecar and measured file set as one closed set."""

    root = root.resolve()
    manifest_path = (manifest_path or root / "manifest/FILE_MANIFEST.json").resolve()
    sums_path = (sums_path or root / "manifest/SHA256SUMS.txt").resolve()
    issues: list[ManifestIssue] = []
    try:
        records = _load_manifest(manifest_path)
        sums = _load_sums(sums_path)
    except ValueError as exc:
        try:
            ref = manifest_path.relative_to(root).as_posix()
        except ValueError:
            ref = str(manifest_path)
        return (ManifestIssue("INVALID_CONTROL_FILE", ref, str(exc)),)

    control_dir = manifest_path.parent if manifest_path.parent == sums_path.parent else None
    manifest_map = {str(record["path"]): record for record in records}
    current_map = {
        path.relative_to(root).as_posix(): path
        for path in public_files(root, control_dir=control_dir)
    }

    for relative in sorted(set(manifest_map) - set(current_map)):
        issues.append(ManifestIssue("MISSING_FROM_TREE", relative, "manifest record has no current file"))
    for relative in sorted(set(current_map) - set(manifest_map)):
        issues.append(ManifestIssue("UNTRACKED_IN_MANIFEST", relative, "current public file is absent from manifest"))
    for relative in sorted(set(manifest_map) & set(current_map)):
        record = manifest_map[relative]
        path = current_map[relative]
        actual_size = path.stat().st_size
        actual_digest = _digest(path)
        if record["size"] != actual_size:
            issues.append(
                ManifestIssue(
                    "SIZE_MISMATCH",
                    relative,
                    f"manifest={record['size']} actual={actual_size}",
                )
            )
        if record["sha256"] != actual_digest:
            issues.append(
                ManifestIssue(
                    "HASH_MISMATCH",
                    relative,
                    f"manifest={record['sha256']} actual={actual_digest}",
                )
            )

    if set(sums) != set(manifest_map):
        for relative in sorted(set(manifest_map) - set(sums)):
            issues.append(ManifestIssue("CHECKSUM_MISSING", relative, "manifest record has no SHA256SUMS entry"))
        for relative in sorted(set(sums) - set(manifest_map)):
            issues.append(ManifestIssue("CHECKSUM_EXTRA", relative, "SHA256SUMS entry has no manifest record"))
    for relative in sorted(set(sums) & set(manifest_map)):
        if sums[relative] != manifest_map[relative]["sha256"]:
            issues.append(
                ManifestIssue(
                    "CHECKSUM_HASH_MISMATCH",
                    relative,
                    "SHA256SUMS differs from FILE_MANIFEST",
                )
            )

    return tuple(issues)


__all__ = ["ManifestIssue", "is_generated_path", "public_files", "verify_manifest"]
