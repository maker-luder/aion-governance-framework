from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FROZEN_MANIFEST_DIR = ROOT / "manifest"
FROZEN_OUTPUTS = {
    (FROZEN_MANIFEST_DIR / "FILE_MANIFEST.json").resolve(),
    (FROZEN_MANIFEST_DIR / "SHA256SUMS.txt").resolve(),
}
GENERATED_PARTS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "build", "dist"}


def resolve_output_dir(value: str) -> Path:
    path = Path(value)
    return (path if path.is_absolute() else ROOT / path).resolve()


def validate_destination(output_dir: Path, *, force: bool) -> tuple[Path, Path]:
    manifest_path = (output_dir / "FILE_MANIFEST.json").resolve()
    sums_path = (output_dir / "SHA256SUMS.txt").resolve()
    if output_dir == ROOT.resolve() or output_dir == FROZEN_MANIFEST_DIR.resolve():
        raise ValueError("refusing repository-root or frozen historical manifest destination")
    if ROOT.resolve() / ".git" == output_dir or (ROOT.resolve() / ".git") in output_dir.parents:
        raise ValueError("refusing output inside .git")
    if manifest_path in FROZEN_OUTPUTS or sums_path in FROZEN_OUTPUTS:
        raise ValueError("refusing to overwrite frozen v0.1.0-rc.1 evidence")
    existing = [path for path in (manifest_path, sums_path) if path.exists()]
    if existing and not force:
        raise ValueError(
            "output already exists; choose a new versioned destination or pass --force: "
            + ", ".join(str(path) for path in existing)
        )
    return manifest_path, sums_path


def build_records(output_dir: Path) -> list[dict[str, object]]:
    excluded = {"manifest/FILE_MANIFEST.json", "manifest/SHA256SUMS.txt"}
    files: list[dict[str, object]] = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        if any(part in GENERATED_PARTS or part.endswith(".egg-info") for part in path.parts):
            continue
        if path.name == ".coverage" or path.suffix == ".pyc":
            continue
        if output_dir == path.parent or output_dir in path.parents:
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel in excluded:
            continue
        data = path.read_bytes()
        files.append({"path": rel, "size": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    return files


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a current-worktree manifest at an explicit non-frozen, "
            "versioned destination."
        )
    )
    parser.add_argument("--baseline", required=True, help="Explicit baseline/version label")
    parser.add_argument("--output-dir", required=True, help="Explicit non-frozen output directory")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace existing files at the explicit non-frozen destination",
    )
    args = parser.parse_args(argv)
    if not args.baseline.strip():
        parser.error("--baseline must not be empty")

    output_dir = resolve_output_dir(args.output_dir)
    try:
        manifest_path, sums_path = validate_destination(output_dir, force=args.force)
    except ValueError as exc:
        parser.error(str(exc))

    records = build_records(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(
            {
                "schema_version": "2.0",
                "baseline": args.baseline,
                "source_scope": "CURRENT_WORKTREE",
                "files": records,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    sums_path.write_text(
        "".join(f"{item['sha256']}  {item['path']}\n" for item in records),
        encoding="utf-8",
    )
    print(f"wrote {len(records)} records to {output_dir} for baseline {args.baseline}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
