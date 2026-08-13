from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HISTORICAL_RC_REF = "refs/tags/v0.1.0-rc.1"
HISTORICAL_RC_NAME = "v0.1.0-rc.1"
EXPECTED_TAG_OBJECT = "abc2f4f4c08e1e696e576da6d6907d745471c184"
EXPECTED_PEELED_COMMIT = "7f4647fe365c7c010f6ebd16924dd8990b0dbafe"
MANIFEST_PATH = "manifest/FILE_MANIFEST.json"
SUMS_PATH = "manifest/SHA256SUMS.txt"

PROHIBITED_SUFFIXES = {".zip", ".whl", ".sqlite3", ".db", ".pyc"}
PATH_PATTERNS = [
    re.compile(r"[A-Za-z]:\\{1,2}Users\\{1,2}[A-Za-z0-9._-]+", re.I),
    re.compile(r"/home/[A-Za-z0-9._-]+/"),
    re.compile("hs" + "upo", re.I),
]
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
]


def git_bytes(*args: str) -> bytes:
    completed = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed.stdout


def git_text(*args: str) -> str:
    return git_bytes(*args).decode("utf-8").strip()


def tree_entries(ref: str) -> dict[str, tuple[str, str]]:
    entries: dict[str, tuple[str, str]] = {}
    for record in git_bytes("ls-tree", "-rz", ref).split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        mode, object_type, object_id = metadata.decode("ascii").split()
        if object_type == "blob":
            entries[raw_path.decode("utf-8")] = (mode, object_id)
    return entries


def index_entries() -> dict[str, tuple[str, str]]:
    entries: dict[str, tuple[str, str]] = {}
    for record in git_bytes("ls-files", "--stage", "-z").split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        mode, object_id, stage = metadata.decode("ascii").split()
        path = raw_path.decode("utf-8")
        if stage != "0":
            raise ValueError(f"unmerged index entry: {path} (stage {stage})")
        entries[path] = (mode, object_id)
    return entries


def git_blob_id(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()  # Git object format for this repository.


def scan_bytes(path: str, data: bytes, errors: list[str]) -> None:
    if path == "scripts/verify_release.py":
        return
    if Path(path).suffix.lower() in PROHIBITED_SUFFIXES:
        errors.append(f"prohibited file: {path}")
        return
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        errors.append(f"non-UTF8 file: {path}")
        return
    for pattern in PATH_PATTERNS:
        if pattern.search(text):
            errors.append(f"private path pattern: {path}")
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            errors.append(f"secret pattern: {path}")


def verify_historical_rc() -> dict[str, object]:
    errors: list[str] = []
    tag_object = git_text("rev-parse", "--verify", HISTORICAL_RC_REF)
    commit = git_text("rev-parse", "--verify", f"{HISTORICAL_RC_REF}^{{commit}}")
    if tag_object != EXPECTED_TAG_OBJECT:
        errors.append(
            "historical tag-object mismatch: "
            f"expected {EXPECTED_TAG_OBJECT}, got {tag_object}"
        )
    if commit != EXPECTED_PEELED_COMMIT:
        errors.append(
            "historical peeled-commit mismatch: "
            f"expected {EXPECTED_PEELED_COMMIT}, got {commit}"
        )
    if errors:
        return {
            "verification_scope": "HISTORICAL_RC_VERIFICATION",
            "baseline": HISTORICAL_RC_NAME,
            "expected_tag_object": EXPECTED_TAG_OBJECT,
            "actual_tag_object": tag_object,
            "expected_peeled_commit": EXPECTED_PEELED_COMMIT,
            "actual_peeled_commit": commit,
            "historical_reference_drift": True,
            "status": "FAIL",
            "errors": errors,
            "files": 0,
        }

    # Use the pinned commit after validating the ref so a concurrent ref move cannot
    # change the historical subject between the trust-anchor check and blob reads.
    entries = tree_entries(EXPECTED_PEELED_COMMIT)
    manifest = json.loads(git_bytes("show", f"{EXPECTED_PEELED_COMMIT}:{MANIFEST_PATH}"))
    records = manifest["files"]
    sums_text = git_bytes("show", f"{EXPECTED_PEELED_COMMIT}:{SUMS_PATH}").decode("utf-8")
    sums = {
        line.split("  ", 1)[1]: line.split("  ", 1)[0]
        for line in sums_text.splitlines()
        if "  " in line
    }
    manifest_digests = {record["path"]: record["sha256"] for record in records}

    if sums != manifest_digests:
        errors.append("SHA256SUMS content differs from FILE_MANIFEST.json")

    expected_paths = set(manifest_digests) | {MANIFEST_PATH, SUMS_PATH}
    if missing := expected_paths - set(entries):
        errors.extend(f"missing from historical Git tree: {path}" for path in sorted(missing))
    if extra := set(entries) - expected_paths:
        errors.extend(f"unmanifested historical Git path: {path}" for path in sorted(extra))

    for record in records:
        path = record["path"]
        entry = entries.get(path)
        if entry is None:
            continue
        data = git_bytes("cat-file", "blob", entry[1])
        if len(data) != record["size"]:
            errors.append(f"size mismatch: {path}")
        if hashlib.sha256(data).hexdigest() != record["sha256"]:
            errors.append(f"hash mismatch: {path}")
        scan_bytes(path, data, errors)

    return {
        "verification_scope": "HISTORICAL_RC_VERIFICATION",
        "baseline": HISTORICAL_RC_NAME,
        "baseline_commit": commit,
        "expected_tag_object": EXPECTED_TAG_OBJECT,
        "actual_tag_object": tag_object,
        "expected_peeled_commit": EXPECTED_PEELED_COMMIT,
        "actual_peeled_commit": commit,
        "historical_reference_drift": False,
        "manifest": f"{EXPECTED_PEELED_COMMIT}:{MANIFEST_PATH}",
        "checksums": f"{EXPECTED_PEELED_COMMIT}:{SUMS_PATH}",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "files": len(records),
    }


def verify_current_snapshot(baseline: str) -> dict[str, object]:
    errors: list[str] = []
    if baseline == "current-head":
        commit = git_text("rev-parse", "HEAD^{commit}")
        tree = git_text("rev-parse", "HEAD^{tree}")
        entries = tree_entries("HEAD")
        baseline_name = f"HEAD@{commit}"
        manifest_name = f"git-tree:{tree}"
        verification_scope = "CURRENT_HEAD_VERIFICATION"
    else:
        commit = None
        entries = index_entries()
        baseline_name = "CURRENT_INDEX"
        manifest_name = "git-index"
        verification_scope = "CURRENT_INDEX_PRECOMMIT_VERIFICATION"

    for path, (mode, expected_object_id) in entries.items():
        worktree_path = ROOT / path
        if mode == "120000":
            errors.append(f"symlink verification unsupported on this platform: {path}")
            continue
        if not worktree_path.is_file():
            errors.append(f"missing tracked file: {path}")
            continue
        data = worktree_path.read_bytes()
        if git_blob_id(data) != expected_object_id:
            errors.append(f"Git blob mismatch: {path}")
        scan_bytes(path, data, errors)
    result: dict[str, object] = {
        "verification_scope": verification_scope,
        "baseline": baseline_name,
        "manifest": manifest_name,
        "subject": "tracked worktree files",
        "expected_reference": "HEAD Git tree" if commit is not None else "Git index",
        "untracked_files": "NOT_EVALUATED_USE_SCAN_PUBLIC_TREE",
        "independent_release_reproducibility": False,
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "files": len(entries),
    }
    if commit is not None:
        result["baseline_commit"] = commit
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify an explicitly selected historical release or current Git snapshot."
    )
    parser.add_argument(
        "--baseline",
        choices=("historical-rc", "current-head", "current-index"),
        required=True,
        help=(
            "historical-rc verifies the frozen v0.1.0-rc.1 manifest from Git objects; "
            "current-head verifies tracked worktree files against HEAD's Git tree; "
            "current-index verifies tracked pre-commit content against the Git index; "
            "current modes do not evaluate untracked files (run scan_public_tree.py)"
        ),
    )
    args = parser.parse_args()
    try:
        result = (
            verify_historical_rc()
            if args.baseline == "historical-rc"
            else verify_current_snapshot(args.baseline)
        )
    except (OSError, subprocess.CalledProcessError, ValueError, json.JSONDecodeError) as exc:
        result = {
            "verification_scope": args.baseline.upper().replace("-", "_"),
            "baseline": args.baseline,
            "status": "FAIL",
            "errors": [f"verification setup failed: {exc}"],
            "files": 0,
        }
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
