from __future__ import annotations

from pathlib import Path

import pytest

from astra_engineering_workbench.approvals import create_approval_request, grant_approval
from astra_engineering_workbench.enums import ApprovalDecision, PermissionLevel, RiskLevel
from astra_engineering_workbench.errors import PatchError, WorkspaceBoundaryError
from astra_engineering_workbench.file_index import sha256_file
from astra_engineering_workbench.workspace import WorkspaceController


def destructive(controller: WorkspaceController):
    request = create_approval_request(
        approval_request_id="REQ-DEL",
        task_id="TASK-001",
        operation_type=PermissionLevel.DESTRUCTIVE_CHANGE,
        reason="delete candidate",
        affected_paths=("sample.txt",),
        proposed_commands=(),
        expected_effect="delete",
        risk_level=RiskLevel.HIGH,
        data_exposure="NONE",
        rollback_plan="snapshot",
        requested_at="2026-07-30T00:00:00+00:00",
        expires_at="2026-07-31T00:00:00+00:00",
    )
    grant = grant_approval(
        request,
        grant_id="GRANT-DEL",
        decision=ApprovalDecision.APPROVED,
        approved_by="OWNER_A",
        approved_at="2026-07-30T00:01:00+00:00",
    )
    return request, grant


def test_CANDIDATE_WRITE_ALLOWED_WITH_APPROVAL_001(controller: WorkspaceController) -> None:
    digest = controller.create_candidate_file("new.txt", "new\n")
    assert len(digest) == 64


def test_WRITE_REQUIRES_APPROVAL_001(controller: WorkspaceController) -> None:
    controller.now = "2026-08-02T00:00:00+00:00"
    with pytest.raises(Exception):
        controller.create_candidate_file("new.txt", "new\n")


def test_BASELINE_WRITE_REJECTED_001(controller: WorkspaceController) -> None:
    baseline = Path(controller.workspace.baseline_root) / "sample.txt"
    before = baseline.read_text(encoding="utf-8")
    controller.create_candidate_file("new.txt", "new\n")
    assert baseline.read_text(encoding="utf-8") == before


@pytest.mark.parametrize("path", ["../escape.txt", "a/../../escape.txt"])
def test_PATH_TRAVERSAL_REJECTED_001(
    controller: WorkspaceController, path: str
) -> None:
    with pytest.raises(WorkspaceBoundaryError):
        controller.create_candidate_file(path, "x")


def test_ABSOLUTE_PATH_ESCAPE_REJECTED_001(controller: WorkspaceController) -> None:
    with pytest.raises(WorkspaceBoundaryError):
        controller.create_candidate_file("C:\\escape.txt", "x")


def test_OUTSIDE_ROOT_WRITE_REJECTED_001(controller: WorkspaceController) -> None:
    with pytest.raises(WorkspaceBoundaryError):
        controller.create_candidate_file("\\\\server\\share\\x.txt", "x")


def test_SYMLINK_ESCAPE_REJECTED_001(
    controller: WorkspaceController, monkeypatch: pytest.MonkeyPatch
) -> None:
    link = controller.candidate_root / "link"
    link.mkdir()
    import astra_engineering_workbench.workspace as module

    original = module._is_link
    monkeypatch.setattr(module, "_is_link", lambda path: path == link or original(path))
    with pytest.raises(WorkspaceBoundaryError):
        controller.create_candidate_file("link/x.txt", "x")


def test_PATCH_CONTEXT_MISMATCH_REJECTED_001(controller: WorkspaceController) -> None:
    path = controller.candidate_root / "sample.txt"
    with pytest.raises(PatchError):
        controller.apply_patch(
            "sample.txt", old_text="missing", new_text="x", expected_hash=sha256_file(path)
        )


def test_atomic_update_and_diff(controller: WorkspaceController) -> None:
    path = controller.candidate_root / "sample.txt"
    controller.update_candidate_file(
        "sample.txt", "alpha\ngamma\n", expected_hash=sha256_file(path)
    )
    assert "-beta" in controller.generate_diff("sample.txt")
    changes = controller.list_changes()
    assert changes.files_modified == ("sample.txt",)
    assert controller.baseline_unchanged()


def test_ATOMIC_WRITE_ROLLBACK_001(controller: WorkspaceController) -> None:
    path = controller.candidate_root / "sample.txt"
    original = sha256_file(path)
    controller.update_candidate_file(
        "sample.txt", "changed\n", expected_hash=original
    )
    assert controller.restore_snapshot("sample.txt") == original


def test_DELETE_REQUIRES_OPERATION_APPROVAL_001(controller: WorkspaceController) -> None:
    with pytest.raises(Exception):
        controller.delete_candidate_file(
            "sample.txt",
            request=controller.write_request,
            grant=controller.write_grant,
        )


def test_delete_and_rollback(controller: WorkspaceController) -> None:
    request, grant = destructive(controller)
    controller.delete_candidate_file("sample.txt", request=request, grant=grant)
    assert not (controller.candidate_root / "sample.txt").exists()
    controller.restore_snapshot("sample.txt")
    assert (controller.candidate_root / "sample.txt").exists()


def test_BASELINE_HASH_UNCHANGED_001(controller: WorkspaceController) -> None:
    controller.create_candidate_file("new.txt", "new")
    assert controller.baseline_unchanged()


def test_read_index_range_find(controller: WorkspaceController) -> None:
    assert controller.read_file("sample.txt").startswith(b"alpha")
    assert controller.read_text_range("sample.txt", start_line=2, end_line=2).strip() == "beta"
    assert controller.find_text("beta") == (("sample.txt", 2),)
    assert controller.index_workspace()[0][0] == "sample.txt"


def test_invalid_range_and_blank_search(controller: WorkspaceController) -> None:
    with pytest.raises(WorkspaceBoundaryError):
        controller.read_text_range("sample.txt", start_line=0, end_line=1)
    with pytest.raises(WorkspaceBoundaryError):
        controller.find_text("")


def test_binary_and_encoding_rejected(controller: WorkspaceController) -> None:
    binary = controller.candidate_root / "binary.bin"
    binary.write_bytes(b"a\x00b")
    with pytest.raises(WorkspaceBoundaryError):
        controller.read_text_range("binary.bin", start_line=1, end_line=1)
    invalid = controller.candidate_root / "invalid.txt"
    invalid.write_bytes(b"\xff\xfe")
    with pytest.raises(WorkspaceBoundaryError):
        controller.read_text_range("invalid.txt", start_line=1, end_line=1)


def test_read_size_limit(controller: WorkspaceController) -> None:
    with pytest.raises(WorkspaceBoundaryError):
        controller.read_file("sample.txt", maximum_bytes=1)


def test_apply_patch_success_and_facade(controller: WorkspaceController) -> None:
    from astra_engineering_workbench.patches import apply_patch

    path = controller.candidate_root / "sample.txt"
    digest = apply_patch(
        controller,
        "sample.txt",
        old_text="beta",
        new_text="gamma",
        expected_hash=sha256_file(path),
    )
    assert digest == sha256_file(path)


def test_rollback_facades(controller: WorkspaceController) -> None:
    from astra_engineering_workbench.rollback import (
        recover_interrupted_change,
        restore_snapshot,
    )

    path = controller.candidate_root / "sample.txt"
    original = sha256_file(path)
    controller.update_candidate_file("sample.txt", "changed", expected_hash=original)
    assert restore_snapshot(controller, "sample.txt") == original

    other = controller.candidate_root / "other.txt"
    other.write_text("before", encoding="utf-8")
    controller.update_candidate_file(
        "other.txt", "after", expected_hash=sha256_file(other)
    )
    assert recover_interrupted_change(controller, ("other.txt",)) == ("other.txt",)


def test_create_existing_and_update_hash_mismatch(controller: WorkspaceController) -> None:
    with pytest.raises(PatchError):
        controller.create_candidate_file("sample.txt", "x")
    with pytest.raises(PatchError):
        controller.update_candidate_file("sample.txt", "x", expected_hash="0" * 64)


def test_restore_missing_snapshot(controller: WorkspaceController) -> None:
    with pytest.raises((PatchError, WorkspaceBoundaryError)):
        controller.restore_snapshot("missing.txt")


def test_hardlink_write_rejected(controller: WorkspaceController) -> None:
    target = controller.candidate_root / "sample.txt"
    link = controller.candidate_root / "hard.txt"
    try:
        link.hardlink_to(target)
    except OSError:
        pytest.skip("hard links unavailable")
    with pytest.raises(WorkspaceBoundaryError):
        controller.update_candidate_file(
            "sample.txt", "x", expected_hash=sha256_file(target)
        )
