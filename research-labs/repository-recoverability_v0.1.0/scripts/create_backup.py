from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys


LAB_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB_ROOT / "src"))

from aion_repository_recoverability import create_repository_backup  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a bounded Git mirror backup.")
    parser.add_argument("source")
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--required-file", action="append", default=[])
    args = parser.parse_args()
    receipt = create_repository_backup(
        args.source,
        args.output_dir,
        timestamp=datetime.now(timezone.utc).isoformat(),
        required_files=tuple(args.required_file),
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
