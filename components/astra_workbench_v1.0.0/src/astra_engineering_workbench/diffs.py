"""Unified text diff generation."""

from __future__ import annotations

import difflib


def unified_text_diff(
    before: str,
    after: str,
    *,
    from_name: str,
    to_name: str,
) -> str:
    return "".join(
        difflib.unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile=from_name,
            tofile=to_name,
        )
    )
