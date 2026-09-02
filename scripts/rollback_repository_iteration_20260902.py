"""Verify by default; --apply creates a local revert commit, never pushes or force-updates main."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = "8ca9f5fe47a38726c64928b164c0f41f84e69dc7"
CORE = "73d4ffb6e9155208d0587b62e69a19b1d10066f9"
PATCH = ROOT / "qa/repository-iteration-20260902/REPOSITORY_ITERATION.patch"
EXPECTED = "c550115ca4da0af1632ec88beafab2088257f7ff08b7749dbcb2a4cf74e53f4f"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if hashlib.sha256(PATCH.read_bytes()).hexdigest() != EXPECTED:
        raise ValueError("patch digest mismatch")
    git("cat-file", "-e", BASE + "^{commit}")
    git("cat-file", "-e", CORE + "^{commit}")
    git("merge-base", "--is-ancestor", CORE, "HEAD")
    git("apply", "--cached", "--reverse", "--check", "--unidiff-zero", str(PATCH))
    print("ROLLBACK_VERIFY=PASS")
    print("BASE=" + BASE)
    print("CORE=" + CORE)
    print("PATCH_SHA256=" + EXPECTED)
    if args.apply:
        if git("status", "--porcelain"):
            raise ValueError("apply requires a clean worktree")
        git("revert", "--no-edit", CORE)
        print("ROLLBACK_MODE=LOCAL_REVERT")
        print("ROLLBACK_HEAD=" + git("rev-parse", "HEAD"))
    else:
        print("ROLLBACK_MODE=DRY_RUN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
