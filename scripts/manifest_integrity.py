from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
from typing import Any

SHA256 = re.compile(r"^[0-9a-f]{64}$")
GENERATED_PARTS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "build", "dist"}
EXCLUDED_RELATIVE_PATHS = {"manifest/FILE_MANIFEST.json", "manifest/SHA256SUMS.txt"}


@dataclass(frozen=True, slots=True)
class ManifestIssue:
    code: str
    path: str
    detail: str

    def render(self) -> str:
        return f"{self.code}: {self.path}: {self.detail}"


def is_generated_path(path: Path) -> bool:
    return (
        any(part in GENERATED_PARTS or part.endswith(".egg-info") for part in path.parts)
        or path.name == ".coverage"
        or path.suffix == ".pyc"
    )


def _inside(path: Path, directory: Path) -> bool:
    try:
        path.relative_to(directory)
        return True
    except ValueError:
        return False


def _relative_control_paths(root: Path, control_dir: Path) -> set[str]:
    excluded = set(EXCLUDED_RELATIVE_PATHS)
    try:
        rel = control_dir.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return excluded
    excluded.update({f"{rel}/FILE_MANIFEST.json", f"{rel}/SHA256SUMS.txt"})
    return excluded


def public_files(root: Path, *, control_dir: Path | None = None) -> tuple[Path, ...]:
    root = root.resolve()
    control_dir = control_dir.resolve() if control_dir is not None else None
    result: list[Path] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        if control_dir is not None and _inside(path.resolve(), control_dir):
            continue
        relative = path.relative_to(root).as_posix()
        if relative in _relative_control_paths(root, control_dir) if control_dir is not None else relative in EXCLUDED_RELATIVE_PATHS:
            continue
        if is_generated_path(path):
            continue
        result.append(path)
    return tuple(result)


def build_entries(root: Path, *, control_dir: Path | None = None) -> list[dict[str, Any]]:
    return [
        {"path": path.relative_to(root.resolve()).as_posix(), "size": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        for path in public_files(root, control_dir=control_dir)
    ]


def write_manifest(root: Path, output_dir: Path | None = None) -> int:
    root = root.resolve()
    control_dir = (output_dir or root / "manifest").resolve()
    control_dir.mkdir(parents=True, exist_ok=True)
    entries = build_entries(root, control_dir=control_dir)
    (control_dir / "FILE_MANIFEST.json").write_text(json.dumps({"schema_version": "1.0", "scope": "CURRENT_REVIEW_TREE", "files": entries}, indent=2) + "\n", encoding="utf-8")
    (control_dir / "SHA256SUMS.txt").write_text("".join(f"{item['sha256']}  {item['path']}\n" for item in entries), encoding="utf-8")
    return len(entries)


def _load_manifest(path: Path) -> tuple[dict[str, object], ...]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read manifest: {path}") from exc
    if not isinstance(payload, dict) or payload.get("schema_version") not in {"1.0", "2.0"} or not isinstance(payload.get("files"), list):
        raise ValueError("manifest must contain schema_version 1.0/2.0 and a files array")
    normalized: list[dict[str, object]] = []
    seen: set[str] = set()
    for index, record in enumerate(payload["files"]):
        if not isinstance(record, dict) or set(record) != {"path", "size", "sha256"}:
            raise ValueError(f"manifest record {index} fields drift")
        relative, size, digest = record.get("path"), record.get("size"), record.get("sha256")
        if not isinstance(relative, str) or not relative or Path(relative).is_absolute() or ".." in Path(relative).parts:
            raise ValueError(f"manifest record {index} has unsafe path")
        if (
            relative in seen
            or isinstance(size, bool)
            or not isinstance(size, int)
            or size < 0
            or not isinstance(digest, str)
            or SHA256.fullmatch(digest) is None
        ):
            raise ValueError(f"manifest record {index} has invalid or duplicate record")
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
        parts = line.split(maxsplit=1)
        if len(parts) != 2 or SHA256.fullmatch(parts[0]) is None or not parts[1] or parts[1] in result:
            raise ValueError(f"invalid checksum line {line_number}")
        result[parts[1]] = parts[0]
    return result


def verify_manifest(root: Path, manifest_path: Path | None = None, sums_path: Path | None = None, manifest_dir: Path | None = None) -> tuple[ManifestIssue, ...]:
    root = root.resolve()
    if manifest_dir is not None:
        manifest_path = manifest_dir / "FILE_MANIFEST.json"
        sums_path = manifest_dir / "SHA256SUMS.txt"
    manifest_path = (manifest_path or root / "manifest/FILE_MANIFEST.json").resolve()
    sums_path = (sums_path or root / "manifest/SHA256SUMS.txt").resolve()
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
    current_map = {path.relative_to(root).as_posix(): path for path in public_files(root, control_dir=control_dir)}
    issues: list[ManifestIssue] = []
    for relative in sorted(set(manifest_map) - set(current_map)):
        issues.append(ManifestIssue("MISSING_FROM_TREE", relative, "manifest record has no current file"))
    for relative in sorted(set(current_map) - set(manifest_map)):
        issues.append(ManifestIssue("UNTRACKED_IN_MANIFEST", relative, "current public file is absent from manifest"))
    for relative in sorted(set(manifest_map) & set(current_map)):
        record, path = manifest_map[relative], current_map[relative]
        actual_size, actual_digest = path.stat().st_size, hashlib.sha256(path.read_bytes()).hexdigest()
        if record["size"] != actual_size:
            issues.append(ManifestIssue("SIZE_MISMATCH", relative, f"manifest={record['size']} actual={actual_size}"))
        if record["sha256"] != actual_digest:
            issues.append(ManifestIssue("HASH_MISMATCH", relative, f"manifest={record['sha256']} actual={actual_digest}"))
    if set(sums) != set(manifest_map):
        for relative in sorted(set(manifest_map) - set(sums)):
            issues.append(ManifestIssue("CHECKSUM_MISSING", relative, "manifest record has no SHA256SUMS entry"))
        for relative in sorted(set(sums) - set(manifest_map)):
            issues.append(ManifestIssue("CHECKSUM_EXTRA", relative, "SHA256SUMS entry has no manifest record"))
    for relative in sorted(set(sums) & set(manifest_map)):
        if sums[relative] != manifest_map[relative]["sha256"]:
            issues.append(ManifestIssue("CHECKSUM_HASH_MISMATCH", relative, "SHA256SUMS differs from FILE_MANIFEST"))
    return tuple(issues)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify or generate a closed-set repository manifest")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--manifest-dir", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--generate", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    directory = args.output_dir or args.manifest_dir
    if args.generate:
        print(f"generated={write_manifest(root, directory)}")
    issues = verify_manifest(root, manifest_dir=directory) if directory else verify_manifest(root)
    if issues:
        for issue in issues:
            print(issue.render())
        return 1
    print(json.dumps({"files": len(public_files(root, control_dir=(directory or root / "manifest"))), "status": "PASS", "manifest_dir": str((directory or root / "manifest").resolve().relative_to(root))}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
