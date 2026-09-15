#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path


UNEXPECTED_BINARY_SUFFIXES = frozenset(
    {".exe", ".dll", ".msi", ".jar", ".class", ".so", ".dylib", ".bin", ".apk", ".ipa"}
)
REQUIRED_SECURITY_DOCS = (
    "SECURITY.md",
    "PUBLIC_RELEASE_SECURITY_SCAN.md",
    "qa/SECRET_SCAN_REPORT.md",
    "docs/security/READ_ONLY_REPOSITORY_SECURITY_AUDIT.md",
)
BOUNDARY_MARKERS = (
    "READ_ONLY",
    "CANONICAL_EFFECT = NONE",
    "DEPLOYMENT = FALSE",
    "HUMAN_OWNER_REVIEW_REQUIRED",
)
SECRET_PATTERNS = (
    ("PRIVATE_KEY_MATERIAL", re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("GITHUB_TOKEN", re.compile(rb"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("AWS_ACCESS_KEY", re.compile(rb"\bAKIA[0-9A-Z]{16}\b")),
)
DOWNLOAD_PATTERN = re.compile(
    r"(?i)(?:curl|wget|invoke-webrequest|download|pip\s+install|npm\s+install).{0,160}https?://"
)
MARKDOWN_LINK = re.compile(r"\[[^]]+\]\(([^)]+)\)")
URI_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


@dataclass(frozen=True, slots=True)
class Finding:
    check: str
    severity: str
    path: str
    detail: str


@dataclass(frozen=True, slots=True)
class TreeEntry:
    mode: str
    object_type: str
    object_id: str
    path: str


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        raise ValueError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def _head_tree_entries(root: Path) -> dict[str, TreeEntry]:
    result = subprocess.run(
        ["git", "-C", str(root), "ls-tree", "-r", "-z", "HEAD"],
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        raise ValueError(f"git ls-tree failed: {result.stderr.decode('utf-8', errors='replace').strip()}")
    entries: dict[str, TreeEntry] = {}
    for record in result.stdout.split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        mode, object_type, object_id = metadata.decode("ascii").split(" ", 2)
        path = raw_path.decode("utf-8")
        if path in entries:
            raise ValueError(f"duplicate HEAD tree path: {path}")
        entries[path] = TreeEntry(mode, object_type, object_id, path)
    return entries


def _blob_bytes(root: Path, entry: TreeEntry) -> bytes:
    if entry.object_type != "blob":
        raise ValueError(f"HEAD tree path is not a blob: {entry.path}")
    result = subprocess.run(
        ["git", "-C", str(root), "cat-file", "blob", entry.object_id],
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        raise ValueError(
            f"git cat-file failed for {entry.path}: "
            + result.stderr.decode("utf-8", errors="replace").strip()
        )
    return result.stdout


def _line_number(data: bytes, offset: int) -> int:
    return data.count(b"\n", 0, offset) + 1


def _relative_link_exists(entries: dict[str, TreeEntry], source_relative: str, target: str) -> bool:
    clean = target.split("#", 1)[0].split("?", 1)[0].strip().replace("\\", "/")
    if not clean or clean.startswith("#") or URI_SCHEME.match(clean):
        return True
    if clean.startswith("/"):
        return False
    normalized = posixpath.normpath(posixpath.join(posixpath.dirname(source_relative), clean))
    if normalized == ".." or normalized.startswith("../"):
        return False
    if normalized in entries:
        return True
    prefix = normalized.rstrip("/") + "/"
    return any(path.startswith(prefix) for path in entries)


def _has_bounded_top_level_permissions(text: str) -> bool:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if not line.startswith("permissions:"):
            continue
        value = line.split(":", 1)[1].strip()
        if value in {"read-all", "{}"}:
            return True
        if value:
            return False

        mapping_seen = False
        for following in lines[index + 1 :]:
            if not following.strip() or following.lstrip().startswith("#"):
                continue
            if not following.startswith((" ", "\t")):
                break
            item = following.strip()
            match = re.fullmatch(r"[A-Za-z0-9_-]+:\s*(read|none)", item)
            if not match:
                return False
            mapping_seen = True
        return mapping_seen
    return False


def audit_repository(root: Path) -> dict[str, object]:
    root = root.resolve()
    git_root = Path(_git(root, "rev-parse", "--show-toplevel")).resolve()
    if git_root != root:
        raise ValueError("audit root must be the exact git top-level")
    commit_sha = _git(root, "rev-parse", "HEAD")
    tree_sha = _git(root, "rev-parse", "HEAD^{tree}")
    entries = _head_tree_entries(root)
    findings: list[Finding] = []
    external_download_refs: list[str] = []
    blob_cache: dict[str, bytes] = {}

    def blob(relative: str) -> bytes:
        if relative not in blob_cache:
            blob_cache[relative] = _blob_bytes(root, entries[relative])
        return blob_cache[relative]

    for relative, entry in entries.items():
        suffix = Path(relative).suffix.lower()
        if suffix in UNEXPECTED_BINARY_SUFFIXES:
            findings.append(Finding("UNEXPECTED_BINARY", "HIGH", relative, suffix))
        if entry.object_type != "blob":
            continue
        data = blob(relative)
        for label, pattern in SECRET_PATTERNS:
            for match in pattern.finditer(data):
                findings.append(
                    Finding(label, "CRITICAL", relative, f"line={_line_number(data, match.start())}")
                )
        if b"\x00" in data or len(data) > 2_000_000:
            continue
        text = data.decode("utf-8", errors="replace")
        if DOWNLOAD_PATTERN.search(text):
            external_download_refs.append(relative)

    for relative in REQUIRED_SECURITY_DOCS:
        entry = entries.get(relative)
        if entry is None or entry.object_type != "blob":
            findings.append(Finding("REQUIRED_SECURITY_DOC", "HIGH", relative, "missing from HEAD tree"))

    boundary_text = "\n".join(
        blob(path).decode("utf-8", errors="replace")
        for path in REQUIRED_SECURITY_DOCS
        if path in entries and entries[path].object_type == "blob"
    )
    for marker in BOUNDARY_MARKERS:
        if marker not in boundary_text:
            findings.append(Finding("AUTHORITY_BOUNDARY", "HIGH", "<security-docs>", f"missing {marker}"))

    for relative in REQUIRED_SECURITY_DOCS:
        entry = entries.get(relative)
        if entry is None or entry.object_type != "blob" or not relative.endswith(".md"):
            continue
        text = blob(relative).decode("utf-8", errors="replace")
        for target in MARKDOWN_LINK.findall(text):
            if not _relative_link_exists(entries, relative, target):
                findings.append(Finding("STALE_SECURITY_LINK", "MEDIUM", relative, target))

    workflows = tuple(
        path
        for path, entry in entries.items()
        if entry.object_type == "blob"
        and path.startswith(".github/workflows/")
        and path.endswith((".yml", ".yaml"))
    )
    for relative in workflows:
        text = blob(relative).decode("utf-8", errors="replace")
        if not _has_bounded_top_level_permissions(text):
            findings.append(
                Finding(
                    "WORKFLOW_PERMISSION_REVIEW",
                    "MEDIUM",
                    relative,
                    "top-level permissions are absent or include non-read capability",
                )
            )

    ordered = sorted(findings, key=lambda item: (item.severity, item.check, item.path, item.detail))
    receipt = {
        "schema_version": "aion.repository-security-audit.v0.1.0",
        "mode": "READ_ONLY",
        "scan_source": "HEAD_GIT_OBJECTS",
        "working_tree_content_used": False,
        "repository_commit_sha": commit_sha,
        "repository_tree_sha": tree_sha,
        "tracked_file_count": len(entries),
        "blob_count": sum(entry.object_type == "blob" for entry in entries.values()),
        "checks": {
            "unexpected_binary_suffixes": sorted(UNEXPECTED_BINARY_SUFFIXES),
            "high_confidence_secret_patterns": [name for name, _ in SECRET_PATTERNS],
            "required_security_docs": list(REQUIRED_SECURITY_DOCS),
            "authority_boundary_markers": list(BOUNDARY_MARKERS),
            "workflow_top_level_permissions": True,
            "security_doc_relative_links": True,
            "external_download_instruction_inventory": True,
            "exact_head_object_scan": True,
        },
        "external_download_reference_paths": sorted(set(external_download_refs)),
        "findings": [asdict(item) for item in ordered],
        "high_or_critical_count": sum(item.severity in {"HIGH", "CRITICAL"} for item in ordered),
        "scientific_claim": "NOT_APPLICABLE",
        "canonical_effect": "NONE",
        "deployment": False,
        "human_owner_review": "REQUIRED",
    }
    canonical = json.dumps(receipt, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    receipt["receipt_sha256"] = hashlib.sha256(canonical).hexdigest()
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only exact-HEAD repository security audit")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    receipt = audit_repository(args.root)
    rendered = json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 1 if receipt["high_or_critical_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
