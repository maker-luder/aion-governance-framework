"""Small local-only inspection CLI."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .file_index import index_workspace, workspace_hash


def main() -> int:
    parser = argparse.ArgumentParser(prog="astra-workbench")
    sub = parser.add_subparsers(dest="command", required=True)
    status = sub.add_parser("status")
    status.add_argument("root", type=Path)
    inspect = sub.add_parser("inspect")
    inspect.add_argument("root", type=Path)
    args = parser.parse_args()
    root: Path = args.root.resolve(strict=True)
    payload = {
        "command": args.command,
        "root": str(root),
        "file_count": len(index_workspace(root)),
        "workspace_hash": workspace_hash(root),
        "canonical_effect": "NONE_PENDING_OWNER_REVIEW",
        "deployment": False,
    }
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return 0
