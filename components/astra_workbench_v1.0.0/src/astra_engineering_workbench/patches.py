"""Patch façade kept separate for traceable capability mapping."""

from __future__ import annotations

from .workspace import WorkspaceController


def apply_patch(
    controller: WorkspaceController,
    relative_path: str,
    *,
    old_text: str,
    new_text: str,
    expected_hash: str,
) -> str:
    return controller.apply_patch(
        relative_path,
        old_text=old_text,
        new_text=new_text,
        expected_hash=expected_hash,
    )
