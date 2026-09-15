from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

import pytest

from aion_repository_recoverability import (
    RecoveryError,
    create_repository_backup,
    verify_repository_restore,
)


def git(repo: Path, *args: str) -> str:
    process = subprocess.run(
        ("git", "-C", str(repo), *args),
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=True,
    )
    return process.stdout.strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.fixture
def source_repository(tmp_path: Path) -> Path:
    repo = tmp_path / "source"
    repo.mkdir()
    git(repo, "init", "-b", "main")
    git(repo, "config", "user.name", "Synthetic Fixture")
    git(repo, "config", "user.email", "fixture@example.invalid")
    (repo / "README.md").write_text("synthetic recovery fixture\n", encoding="utf-8")
    (repo / "required.txt").write_text("required\n", encoding="utf-8")
    git(repo, "add", "README.md", "required.txt")
    git(repo, "commit", "-m", "fixture")
    git(repo, "tag", "v0.1.0")
    git(repo, "branch", "research-fixture")
    return repo


def test_backup_then_isolated_restore_verifies_refs_head_tree_and_required_file(
    source_repository: Path, tmp_path: Path
) -> None:
    output = tmp_path / "outside-source" / "backup"
    backup = create_repository_backup(
        str(source_repository),
        output,
        timestamp="2026-09-13T00:00:00Z",
        required_files=("README.md", "required.txt"),
    )
    restored = verify_repository_restore(
        output / "repository-mirror.zip",
        output / "backup-receipt.json",
        output / "restore-receipt.json",
        timestamp="2026-09-13T00:01:00Z",
    )
    assert backup["source_head_commit_sha"] == git(source_repository, "rev-parse", "HEAD")
    assert backup["source_head_tree_sha"] == git(source_repository, "rev-parse", "HEAD^{tree}")
    assert backup["source_head_symbolic_ref"] == "refs/heads/main"
    assert backup["refs_captured"] == 3
    assert backup["lfs_policy"] == "FAIL_CLOSED_ON_REACHABLE_POINTER"
    assert backup["lfs_applicable"] is False
    assert backup["lfs_pointer_object_count"] == 0
    assert backup["contains_credentials"] is False
    assert restored["restore_verified"] is True
    assert restored["checksum_result"] == "PASS"
    assert restored["ref_comparison"] == "PASS"
    assert restored["head_symbolic_ref_comparison"] == "PASS"
    assert restored["required_file_check"] == "PASS"
    assert restored["unresolved_warnings"] == []
    assert restored["restored_head_commit_sha"] == backup["source_head_commit_sha"]
    assert restored["restored_head_tree_sha"] == backup["source_head_tree_sha"]
    assert restored["restored_head_symbolic_ref"] == backup["source_head_symbolic_ref"]


def test_checksum_tamper_fails_before_restore(source_repository: Path, tmp_path: Path) -> None:
    output = tmp_path / "backup"
    create_repository_backup(str(source_repository), output, timestamp="2026-09-13T00:00:00Z")
    archive = output / "repository-mirror.zip"
    archive.write_bytes(archive.read_bytes() + b"tampered")
    with pytest.raises(RecoveryError, match="checksum mismatch"):
        verify_repository_restore(
            archive,
            output / "backup-receipt.json",
            output / "restore-receipt.json",
            timestamp="2026-09-13T00:01:00Z",
        )


def test_symbolic_head_drift_fails_even_when_commit_tree_and_refs_still_match(
    source_repository: Path, tmp_path: Path
) -> None:
    output = tmp_path / "backup"
    create_repository_backup(str(source_repository), output, timestamp="2026-09-13T00:00:00Z")
    archive = output / "repository-mirror.zip"
    rewritten = output / "rewritten.zip"
    with zipfile.ZipFile(archive, "r") as source_zip, zipfile.ZipFile(rewritten, "w") as target_zip:
        for info in source_zip.infolist():
            data = source_zip.read(info.filename)
            if info.filename == "repository.git/HEAD":
                data = b"ref: refs/heads/research-fixture\n"
            target_zip.writestr(info, data)
    rewritten.replace(archive)

    receipt_path = output / "backup-receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["archive_sha256"] = sha256(archive)
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    with pytest.raises(RecoveryError, match="symbolic HEAD mismatch"):
        verify_repository_restore(
            archive,
            receipt_path,
            output / "restore-receipt.json",
            timestamp="2026-09-13T00:01:00Z",
        )


def test_reachable_git_lfs_pointer_fails_closed(source_repository: Path, tmp_path: Path) -> None:
    (source_repository / "large.dat").write_text(
        "version https://git-lfs.github.com/spec/v1\n"
        f"oid sha256:{'0' * 64}\n"
        "size 123456\n",
        encoding="utf-8",
    )
    git(source_repository, "add", "large.dat")
    git(source_repository, "commit", "-m", "add synthetic lfs pointer")
    with pytest.raises(RecoveryError, match="Git LFS pointer"):
        create_repository_backup(
            str(source_repository),
            tmp_path / "backup",
            timestamp="2026-09-13T00:00:00Z",
        )


def test_backup_destination_inside_source_is_rejected(
    source_repository: Path,
) -> None:
    with pytest.raises(RecoveryError, match="outside"):
        create_repository_backup(
            str(source_repository),
            source_repository / "backup",
            timestamp="2026-09-13T00:00:00Z",
        )


def test_required_files_reject_parent_traversal_and_duplicates(
    source_repository: Path, tmp_path: Path
) -> None:
    with pytest.raises(RecoveryError, match="safe repository-relative"):
        create_repository_backup(
            str(source_repository),
            tmp_path / "backup",
            timestamp="2026-09-13T00:00:00Z",
            required_files=("../secret",),
        )
    with pytest.raises(RecoveryError, match="must be unique"):
        create_repository_backup(
            str(source_repository),
            tmp_path / "backup-2",
            timestamp="2026-09-13T00:00:00Z",
            required_files=("README.md", "README.md"),
        )


def test_receipts_are_non_secret_and_keep_claim_boundaries(
    source_repository: Path, tmp_path: Path
) -> None:
    output = tmp_path / "backup"
    receipt = create_repository_backup(str(source_repository), output, timestamp="fixed")
    persisted = json.loads((output / "backup-receipt.json").read_text())
    assert receipt == persisted
    assert receipt["repository_id"] == "source"
    assert "token" not in json.dumps(receipt).lower()
    assert receipt["canonical_effect"] == "NONE"
    assert receipt["deployment"] is False
    assert receipt["human_review_status"] == "PENDING"
