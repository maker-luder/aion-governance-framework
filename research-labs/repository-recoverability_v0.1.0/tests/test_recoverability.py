from __future__ import annotations

import json
from pathlib import Path
import subprocess

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
    assert backup["refs_captured"] == 3
    assert backup["contains_credentials"] is False
    assert restored["restore_verified"] is True
    assert restored["checksum_result"] == "PASS"
    assert restored["ref_comparison"] == "PASS"
    assert restored["required_file_check"] == "PASS"
    assert restored["restored_head_commit_sha"] == backup["source_head_commit_sha"]
    assert restored["restored_head_tree_sha"] == backup["source_head_tree_sha"]


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


def test_backup_destination_inside_source_is_rejected(
    source_repository: Path,
) -> None:
    with pytest.raises(RecoveryError, match="outside"):
        create_repository_backup(
            str(source_repository),
            source_repository / "backup",
            timestamp="2026-09-13T00:00:00Z",
        )


def test_required_files_reject_parent_traversal(source_repository: Path, tmp_path: Path) -> None:
    with pytest.raises(RecoveryError, match="safe repository-relative"):
        create_repository_backup(
            str(source_repository),
            tmp_path / "backup",
            timestamp="2026-09-13T00:00:00Z",
            required_files=("../secret",),
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
