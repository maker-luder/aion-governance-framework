from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from scripts.audit_repository_security import REQUIRED_SECURITY_DOCS, audit_repository


def git(root: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True)


def repository(tmp_path: Path) -> Path:
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.email", "fixture@example.invalid")
    git(tmp_path, "config", "user.name", "Synthetic Fixture")
    markers = "\n".join(
        ("READ_ONLY", "CANONICAL_EFFECT = NONE", "DEPLOYMENT = FALSE", "HUMAN_OWNER_REVIEW_REQUIRED")
    )
    for relative in REQUIRED_SECURITY_DOCS:
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(markers, encoding="utf-8")
    workflow = tmp_path / ".github/workflows/quality.yml"
    workflow.parent.mkdir(parents=True, exist_ok=True)
    workflow.write_text("permissions: read-all\nname: quality\n", encoding="utf-8")
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-qm", "fixture")
    return tmp_path


def test_clean_fixture_receipt_binds_commit_and_tree(tmp_path: Path) -> None:
    root = repository(tmp_path)
    receipt = audit_repository(root)
    assert receipt["mode"] == "READ_ONLY"
    assert receipt["high_or_critical_count"] == 0
    assert receipt["findings"] == []
    assert len(receipt["repository_commit_sha"]) == 40
    assert len(receipt["repository_tree_sha"]) == 40
    assert len(receipt["receipt_sha256"]) == 64


def test_unexpected_binary_and_high_confidence_secret_are_reported(tmp_path: Path) -> None:
    root = repository(tmp_path)
    (root / "payload.exe").write_bytes(b"MZ")
    secret = "gh" + "p_" + "A" * 24
    (root / "leak.txt").write_text(secret, encoding="utf-8")
    git(root, "add", ".")
    git(root, "commit", "-qm", "add synthetic findings")
    receipt = audit_repository(root)
    checks = {item["check"] for item in receipt["findings"]}
    assert "UNEXPECTED_BINARY" in checks
    assert "GITHUB_TOKEN" in checks
    assert receipt["high_or_critical_count"] == 2


def test_missing_security_doc_and_workflow_permission_are_reported(tmp_path: Path) -> None:
    root = repository(tmp_path)
    (root / REQUIRED_SECURITY_DOCS[0]).unlink()
    (root / ".github/workflows/quality.yml").write_text("name: quality\n", encoding="utf-8")
    git(root, "add", "-A")
    git(root, "commit", "-qm", "remove controls")
    receipt = audit_repository(root)
    checks = {item["check"] for item in receipt["findings"]}
    assert "REQUIRED_SECURITY_DOC" in checks
    assert "WORKFLOW_PERMISSION_REVIEW" in checks


def test_stale_relative_security_link_is_reported(tmp_path: Path) -> None:
    root = repository(tmp_path)
    security = root / "SECURITY.md"
    security.write_text(security.read_text(encoding="utf-8") + "\n[missing](docs/missing.md)\n", encoding="utf-8")
    git(root, "add", ".")
    git(root, "commit", "-qm", "stale link")
    assert any(item["check"] == "STALE_SECURITY_LINK" for item in audit_repository(root)["findings"])


def test_nested_directory_is_rejected_as_audit_root(tmp_path: Path) -> None:
    root = repository(tmp_path)
    nested = root / "nested"
    nested.mkdir()
    with pytest.raises(ValueError, match="exact git top-level"):
        audit_repository(nested)


def test_current_repository_merge_tree_has_no_high_or_critical_findings() -> None:
    root = Path(__file__).resolve().parents[1]
    receipt = audit_repository(root)
    assert receipt["tracked_file_count"] > 0
    assert receipt["high_or_critical_count"] == 0
