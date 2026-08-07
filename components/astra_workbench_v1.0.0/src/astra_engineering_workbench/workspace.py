"""Programmatic baseline/candidate/output isolation and atomic file changes."""

from __future__ import annotations

import os
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePath, PureWindowsPath

from .approvals import validate_grant
from .diffs import unified_text_diff
from .enums import PermissionLevel
from .errors import ApprovalError, PatchError, WorkspaceBoundaryError
from .file_index import index_workspace, sha256_file, workspace_hash
from .models import (
    ApprovalGrant,
    ApprovalRequest,
    CandidateWorkspace,
    ChangeSet,
)


MAX_TEXT_BYTES = 4 * 1024 * 1024


def _is_link(path: Path) -> bool:
    junction_check = getattr(os.path, "isjunction", lambda _path: False)
    return path.is_symlink() or bool(junction_check(path))


def _validate_relative(relative_path: str) -> Path:
    if not relative_path or relative_path.startswith(("\\\\", "//")):
        raise WorkspaceBoundaryError("blank or UNC path is not authorized")
    pure = PurePath(relative_path)
    windows = PureWindowsPath(relative_path)
    if pure.is_absolute() or windows.is_absolute() or bool(windows.drive) or ".." in pure.parts:
        raise WorkspaceBoundaryError("absolute path or traversal is rejected")
    return Path(*pure.parts)


def _ensure_no_links(root: Path, path: Path) -> None:
    current = root
    if _is_link(current):
        raise WorkspaceBoundaryError("workspace root cannot be a link or junction")
    for part in path.relative_to(root).parts:
        current = current / part
        if current.exists() and _is_link(current):
            raise WorkspaceBoundaryError("symlink or junction escape is rejected")


def _resolve_inside(root: Path, relative_path: str, *, allow_missing: bool) -> Path:
    relative = _validate_relative(relative_path)
    candidate = root / relative
    parent = candidate.parent.resolve(strict=True)
    resolved_root = root.resolve(strict=True)
    try:
        parent.relative_to(resolved_root)
    except ValueError as exc:
        raise WorkspaceBoundaryError("path escapes configured root") from exc
    _ensure_no_links(resolved_root, parent)
    if candidate.exists():
        resolved = candidate.resolve(strict=True)
        try:
            resolved.relative_to(resolved_root)
        except ValueError as exc:
            raise WorkspaceBoundaryError("resolved path escapes configured root") from exc
        _ensure_no_links(resolved_root, resolved)
    elif not allow_missing:
        raise WorkspaceBoundaryError("requested path does not exist")
    return candidate


def _scan_source_links(root: Path) -> None:
    for path in root.rglob("*"):
        if _is_link(path):
            raise WorkspaceBoundaryError("baseline contains a symlink or junction")


def create_candidate_workspace(
    *,
    task_id: str,
    baseline_root: Path,
    sessions_root: Path,
    created_at: str,
) -> CandidateWorkspace:
    if not task_id or any(char in task_id for char in "\\/:*?\"<>|"):
        raise WorkspaceBoundaryError("task_id is unsafe for a workspace path")
    baseline = baseline_root.resolve(strict=True)
    sessions = sessions_root.resolve(strict=True)
    _scan_source_links(baseline)
    candidate = sessions / "candidate" / task_id
    output = sessions / "output" / task_id
    if candidate.exists() or output.exists():
        raise WorkspaceBoundaryError("stale candidate or output workspace exists")
    candidate.parent.mkdir(parents=True, exist_ok=True)
    output.mkdir(parents=True, exist_ok=False)
    shutil.copytree(
        baseline,
        candidate,
        copy_function=shutil.copy2,
        ignore=shutil.ignore_patterns(
            "__pycache__", ".pytest_cache", ".mypy_cache", "build", "*.pyc", "*.pyo"
        ),
    )
    baseline_hash = workspace_hash(baseline)
    if workspace_hash(candidate) != baseline_hash:
        raise WorkspaceBoundaryError("candidate copy does not match baseline hash tree")
    return CandidateWorkspace(
        task_id=task_id,
        baseline_root=str(baseline),
        candidate_root=str(candidate),
        output_root=str(output),
        baseline_hash=baseline_hash,
        created_at=created_at,
    )


@dataclass
class WorkspaceController:
    workspace: CandidateWorkspace
    write_request: ApprovalRequest
    write_grant: ApprovalGrant
    now: str

    @property
    def baseline_root(self) -> Path:
        return Path(self.workspace.baseline_root)

    @property
    def candidate_root(self) -> Path:
        return Path(self.workspace.candidate_root)

    @property
    def output_root(self) -> Path:
        return Path(self.workspace.output_root)

    def _require_write(self) -> None:
        validate_grant(
            self.write_request,
            self.write_grant,
            task_id=self.workspace.task_id,
            required_permission=PermissionLevel.CANDIDATE_WRITE,
            now=self.now,
        )

    def _candidate(self, relative_path: str, *, allow_missing: bool = False) -> Path:
        return _resolve_inside(
            self.candidate_root, relative_path, allow_missing=allow_missing
        )

    def _baseline(self, relative_path: str) -> Path:
        return _resolve_inside(self.baseline_root, relative_path, allow_missing=False)

    def index_workspace(self) -> tuple[tuple[str, int, str], ...]:
        return index_workspace(self.candidate_root)

    def read_file(self, relative_path: str, *, maximum_bytes: int = MAX_TEXT_BYTES) -> bytes:
        path = self._candidate(relative_path)
        if path.stat().st_size > maximum_bytes:
            raise WorkspaceBoundaryError("file exceeds read size limit")
        return path.read_bytes()

    def read_text_range(
        self,
        relative_path: str,
        *,
        start_line: int,
        end_line: int,
    ) -> str:
        if start_line < 1 or end_line < start_line:
            raise WorkspaceBoundaryError("invalid text range")
        data = self.read_file(relative_path)
        if b"\x00" in data:
            raise WorkspaceBoundaryError("binary file cannot be read as text")
        try:
            lines = data.decode("utf-8").splitlines(keepends=True)
        except UnicodeDecodeError as exc:
            raise WorkspaceBoundaryError("unknown/non-UTF-8 encoding") from exc
        return "".join(lines[start_line - 1 : end_line])

    def find_text(self, needle: str) -> tuple[tuple[str, int], ...]:
        if not needle:
            raise WorkspaceBoundaryError("search text cannot be blank")
        matches: list[tuple[str, int]] = []
        for relative, size, _ in self.index_workspace():
            if size > MAX_TEXT_BYTES:
                continue
            data = (self.candidate_root / relative).read_bytes()
            if b"\x00" in data:
                continue
            try:
                lines = data.decode("utf-8").splitlines()
            except UnicodeDecodeError:
                continue
            matches.extend(
                (relative, index)
                for index, line in enumerate(lines, start=1)
                if needle in line
            )
        return tuple(matches)

    def _snapshot(self, relative_path: str, source: Path) -> Path:
        snapshot = self.candidate_root / ".astra_meta" / "snapshots" / relative_path
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        if snapshot.exists():
            raise PatchError("snapshot already exists for this change set")
        shutil.copy2(source, snapshot)
        return snapshot

    def _atomic_text_write(self, target: Path, text: str) -> None:
        target.parent.mkdir(parents=True, exist_ok=True)
        handle, temp_name = tempfile.mkstemp(prefix=".astra-", dir=target.parent)
        os.close(handle)
        temp = Path(temp_name)
        try:
            temp.write_text(text, encoding="utf-8", newline="\n")
            temp.replace(target)
        except OSError as exc:
            temp.unlink(missing_ok=True)
            raise PatchError("atomic candidate write failed") from exc

    def create_candidate_file(self, relative_path: str, content: str) -> str:
        self._require_write()
        target = self._candidate(relative_path, allow_missing=True)
        if target.exists():
            raise PatchError("candidate file already exists")
        self._atomic_text_write(target, content)
        return sha256_file(target)

    def update_candidate_file(
        self,
        relative_path: str,
        content: str,
        *,
        expected_hash: str,
    ) -> str:
        self._require_write()
        target = self._candidate(relative_path)
        if not target.is_file() or target.stat().st_size > MAX_TEXT_BYTES:
            raise PatchError("target is missing, non-file or too large")
        if target.stat().st_nlink > 1:
            raise WorkspaceBoundaryError("hard-linked target cannot be modified")
        data = target.read_bytes()
        if b"\x00" in data:
            raise PatchError("binary file cannot be rewritten as text")
        try:
            data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise PatchError("target encoding is not UTF-8") from exc
        if sha256_file(target) != expected_hash:
            raise PatchError("target hash changed before write")
        self._snapshot(relative_path, target)
        self._atomic_text_write(target, content)
        return sha256_file(target)

    def apply_patch(
        self,
        relative_path: str,
        *,
        old_text: str,
        new_text: str,
        expected_hash: str,
    ) -> str:
        target = self._candidate(relative_path)
        before = target.read_text(encoding="utf-8")
        if before.count(old_text) != 1:
            raise PatchError("patch context must match exactly once")
        return self.update_candidate_file(
            relative_path,
            before.replace(old_text, new_text, 1),
            expected_hash=expected_hash,
        )

    def delete_candidate_file(
        self,
        relative_path: str,
        *,
        request: ApprovalRequest,
        grant: ApprovalGrant,
    ) -> None:
        validate_grant(
            request,
            grant,
            task_id=self.workspace.task_id,
            required_permission=PermissionLevel.DESTRUCTIVE_CHANGE,
            now=self.now,
        )
        target = self._candidate(relative_path)
        if not target.is_file():
            raise PatchError("delete target must be a regular file")
        self._snapshot(relative_path, target)
        target.unlink()

    def restore_snapshot(self, relative_path: str) -> str:
        target = self._candidate(relative_path, allow_missing=True)
        snapshot_root = self.candidate_root / ".astra_meta" / "snapshots"
        if not snapshot_root.is_dir():
            raise PatchError("rollback snapshot is missing")
        snapshot = _resolve_inside(snapshot_root, relative_path, allow_missing=False)
        if not snapshot.is_file():
            raise PatchError("rollback snapshot is missing")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(snapshot, target)
        return sha256_file(target)

    def generate_diff(self, relative_path: str) -> str:
        baseline = self._baseline(relative_path)
        candidate = self._candidate(relative_path)
        return unified_text_diff(
            baseline.read_text(encoding="utf-8"),
            candidate.read_text(encoding="utf-8"),
            from_name=f"baseline/{relative_path}",
            to_name=f"candidate/{relative_path}",
        )

    def list_changes(self) -> ChangeSet:
        baseline = {item[0]: item[2] for item in index_workspace(self.baseline_root)}
        candidate = {item[0]: item[2] for item in index_workspace(self.candidate_root)}
        added = tuple(sorted(set(candidate) - set(baseline)))
        deleted = tuple(sorted(set(baseline) - set(candidate)))
        modified = tuple(
            sorted(
                path
                for path in set(baseline) & set(candidate)
                if baseline[path] != candidate[path]
            )
        )
        return ChangeSet(
            change_id=f"CHANGESET-{self.workspace.task_id}",
            requirement_ids=(),
            affected_files=tuple(sorted((*added, *modified, *deleted))),
            symbols=(),
            change_reason="candidate workspace delta",
            risk=self.write_request.risk_level,
            expected_behavior="baseline remains immutable",
            tests_required=(),
            rollback_method="restore pre-change snapshots",
            owner_approval_reference=self.write_grant.grant_id,
            files_added=added,
            files_modified=modified,
            files_deleted=deleted,
            baseline_hash=workspace_hash(self.baseline_root),
            candidate_hash=workspace_hash(self.candidate_root),
            diff_summary=f"added={len(added)} modified={len(modified)} deleted={len(deleted)}",
        )

    def baseline_unchanged(self) -> bool:
        return workspace_hash(self.baseline_root) == self.workspace.baseline_hash
