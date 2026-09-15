from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys


LAB_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB_ROOT / "src"))

from aion_repository_recoverability import verify_repository_restore  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify a Git mirror backup in isolation.")
    parser.add_argument("archive", type=Path)
    parser.add_argument("backup_receipt", type=Path)
    parser.add_argument("output_receipt", type=Path)
    args = parser.parse_args()
    receipt = verify_repository_restore(
        args.archive,
        args.backup_receipt,
        args.output_receipt,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
