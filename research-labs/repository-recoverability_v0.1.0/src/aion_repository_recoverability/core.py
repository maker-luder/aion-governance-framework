from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from urllib.parse import urlsplit, urlunsplit
import zipfile


class RecoveryError(RuntimeError):
    pass


def _run(*args: str, cwd: Path | None = None) -> str:
    process = subprocess.run(
        args,
        cwd=cwd,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if process.returncode:
        raise RecoveryError(f"command failed ({args[0]} {args[1]}): {process.stdout.strip()}")
    return process.stdout.strip()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _safe_repository_id(source: str) -> str:
    parsed = urlsplit(source)
    if parsed.scheme and parsed.netloc:
        clean = urlunsplit((parsed.scheme, parsed.hostname or "", parsed.path, "", ""))
        return clean.removesuffix(".git").rstrip("/")
    return Path(source).resolve().name.removesuffix(".git")


def _refs(git_dir: Path) -> dict[str, str]:
    output = _run(
        "git",
        f"--git-dir={git_dir}",
        "for-each-ref",
        "--format=%(refname) %(objectname)",
        "refs/heads",
        "refs/tags",
    )
    return dict(line.split(" ", 1) for line in output.splitlines() if line)


def _write_zip(source: Path, target: Path) -> None:
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(item for item in source.rglob("*") if item.is_dir()):
            relative = (Path(source.name) / path.relative_to(source)).as_posix() + "/"
            info = zipfile.ZipInfo(relative, (1980, 1, 1, 0, 0, 0))
            info.external_attr = (0o40755 << 16) | 0x10
            archive.writestr(info, b"")
        for path in sorted(item for item in source.rglob("*") if item.is_file()):
            relative = Path(source.name) / path.relative_to(source)
            info = zipfile.ZipInfo(relative.as_posix(), (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())


def create_repository_backup(
    source: str,
    output_dir: Path,
    *,
    timestamp: str,
    required_files: tuple[str, ...] = (),
) -> dict[str, object]:
    """Create a non-secret archive and receipt from a fresh Git mirror clone."""
    if not timestamp.strip():
        raise RecoveryError("timestamp is required")
    if any(not item.strip() or Path(item).is_absolute() or ".." in Path(item).parts for item in required_files):
        raise RecoveryError("required_files must be safe repository-relative paths")
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    if Path(source).exists() and output_dir.is_relative_to(Path(source).resolve()):
        raise RecoveryError("backup output must be outside the source repository")

    with tempfile.TemporaryDirectory(prefix="aion-mirror-") as temporary:
        mirror = Path(temporary) / "repository.git"
        _run("git", "clone", "--mirror", source, str(mirror))
        integrity_output = _run("git", f"--git-dir={mirror}", "fsck", "--full")
        head_commit = _run("git", f"--git-dir={mirror}", "rev-parse", "HEAD")
        head_tree = _run("git", f"--git-dir={mirror}", "rev-parse", "HEAD^{tree}")
        refs = _refs(mirror)
        for item in required_files:
            _run("git", f"--git-dir={mirror}", "cat-file", "-e", f"HEAD:{item}")
        archive_path = output_dir / "repository-mirror.zip"
        _write_zip(mirror, archive_path)

    receipt = {
        "schema_version": "0.1.0",
        "repository_id": _safe_repository_id(source),
        "backup_timestamp": timestamp,
        "backup_method": "FRESH_GIT_MIRROR_ZIP",
        "source_head_commit_sha": head_commit,
        "source_head_tree_sha": head_tree,
        "refs": refs,
        "refs_captured": len(refs),
        "lfs_applicable": "NOT_ASSESSED",
        "lfs_objects_fetched": False,
        "archive_file": archive_path.name,
        "archive_sha256": _sha256(archive_path),
        "git_integrity": "PASS",
        "git_fsck_output": integrity_output,
        "required_files": list(required_files),
        "contains_credentials": False,
        "operator_role": "HUMAN_OWNER_AUTHORIZED_CODEX_EXECUTION",
        "human_review_status": "PENDING",
        "canonical_effect": "NONE",
        "deployment": False,
    }
    receipt_path = output_dir / "backup-receipt.json"
    receipt_path.write_bytes((json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode())
    checksum_path = output_dir / "backup-checksum.json"
    checksum_path.write_bytes(
        (
            json.dumps(
                {"algorithm": "SHA-256", "file": archive_path.name, "sha256": receipt["archive_sha256"]},
                indent=2,
                sort_keys=True,
            )
            + "\n"
        ).encode()
    )
    return receipt


def _safe_extract(archive: zipfile.ZipFile, destination: Path) -> None:
    root = destination.resolve()
    for member in archive.infolist():
        target = (destination / member.filename).resolve()
        if not target.is_relative_to(root):
            raise RecoveryError("archive contains an unsafe path")
    archive.extractall(destination)


def verify_repository_restore(
    archive_path: Path,
    backup_receipt_path: Path,
    output_receipt_path: Path,
    *,
    timestamp: str,
) -> dict[str, object]:
    """Verify checksum, isolated extraction, Git integrity, refs, HEAD and required files."""
    receipt = json.loads(backup_receipt_path.read_text(encoding="utf-8"))
    actual_sha = _sha256(archive_path)
    if actual_sha != receipt["archive_sha256"]:
        raise RecoveryError("backup archive checksum mismatch")

    with tempfile.TemporaryDirectory(prefix="aion-restore-") as temporary:
        restore_root = Path(temporary)
        with zipfile.ZipFile(archive_path) as archive:
            _safe_extract(archive, restore_root)
        git_dir = restore_root / "repository.git"
        integrity_output = _run("git", f"--git-dir={git_dir}", "fsck", "--full")
        restored_commit = _run("git", f"--git-dir={git_dir}", "rev-parse", "HEAD")
        restored_tree = _run("git", f"--git-dir={git_dir}", "rev-parse", "HEAD^{tree}")
        restored_refs = _refs(git_dir)
        if restored_commit != receipt["source_head_commit_sha"]:
            raise RecoveryError("restored HEAD commit SHA mismatch")
        if restored_tree != receipt["source_head_tree_sha"]:
            raise RecoveryError("restored HEAD tree SHA mismatch")
        if restored_refs != receipt["refs"]:
            raise RecoveryError("restored refs mismatch")
        for item in receipt["required_files"]:
            _run("git", f"--git-dir={git_dir}", "cat-file", "-e", f"HEAD:{item}")

    result = {
        "schema_version": "0.1.0",
        "restore_test_timestamp": timestamp,
        "repository_id": receipt["repository_id"],
        "archive_file": archive_path.name,
        "archive_sha256": actual_sha,
        "checksum_result": "PASS",
        "git_integrity": "PASS",
        "git_fsck_output": integrity_output,
        "restored_head_commit_sha": restored_commit,
        "restored_head_tree_sha": restored_tree,
        "ref_comparison": "PASS",
        "required_file_check": "PASS",
        "optional_test_suite": "NOT_REQUESTED",
        "unresolved_warnings": ["LFS_APPLICABILITY_NOT_ASSESSED"],
        "human_review_status": "PENDING",
        "restore_verified": True,
        "canonical_effect": "NONE",
        "deployment": False,
    }
    output_receipt_path.parent.mkdir(parents=True, exist_ok=True)
    output_receipt_path.write_bytes((json.dumps(result, indent=2, sort_keys=True) + "\n").encode())
    return result
