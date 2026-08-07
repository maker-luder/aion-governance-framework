"""Rollback and interrupted-workspace recovery helpers."""

from __future__ import annotations

from .workspace import WorkspaceController


def restore_snapshot(controller: WorkspaceController, relative_path: str) -> str:
    return controller.restore_snapshot(relative_path)


def recover_interrupted_change(
    controller: WorkspaceController,
    affected_paths: tuple[str, ...],
) -> tuple[str, ...]:
    restored: list[str] = []
    for path in affected_paths:
        controller.restore_snapshot(path)
        restored.append(path)
    return tuple(restored)
