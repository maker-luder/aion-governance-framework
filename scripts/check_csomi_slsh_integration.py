from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
LAB_SRC = ROOT / "research-labs" / "csomi-slsh-integration_v0.1.0" / "src"
if str(LAB_SRC) not in sys.path:
    sys.path.insert(0, str(LAB_SRC))

from aion_csomi_slsh_integration.validate import validate_file  # noqa: E402


if __name__ == "__main__":
    validate_file(ROOT)
