#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
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


@dataclass(frozen=True, slots=True)
class Finding:
    check: str
    severity: str
    path: str
    detail: str


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        raise ValueError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def _tracked_files(root: Path) -> tuple[str, ...]:
    output = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z"],
        check=True,
        capture_output=True,
    ).stdout
    return tuple(item.decode("utf-8") for item in output.split(b"\0") if item)


def _line_number(data: bytes, offset: int) -> int:
    return data.count(b"\n", 0, offset) + 1


def _relative_link_exists(root: Path, source: Path, target: str) -> bool:
    clean = target.split("#", 1)[0].split("?", 1)[0]
    if not clean or clean.startswith(("http://", "https://", "mailto:", "#")):
        return True
    resolved = (source.parent / clean).resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        return False
    return resolved.exists()


def audit_repository(root: Path) -> dict[str, object]:
    root = root.resolve()
    git_root = Path(_git(root, "rev-parse", "--show-toplevel")).resolve()
    if git_root != root:
        raise ValueError("audit root must be the exact git top-level")
    commit_sha = _git(root, "rev-parse", "HEAD")
    tree_sha = _git(root, "rev-parse", "HEAD^{tree}")
    tracked = _tracked_files(root)
    findings: list[Finding] = []
    external_download_refs: list[str] = []

    for relative in tracked:
        path = root / relative
        suffix = path.suffix.lower()
        if suffix in UNEXPECTED_BINARY_SUFFIXES:
            findings.append(Finding("UNEXPECTED_BINARY", "HIGH", relative, suffix))
        if not path.is_file():
            continue
        data = path.read_bytes()
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
        if relative not in tracked:
            findings.append(Finding("REQUIRED_SECURITY_DOC", "HIGH", relative, "missing from tracked files"))

    boundary_text = "\n".join(
        (root / path).read_text(encoding="utf-8", errors="replace")
        for path in REQUIRED_SECURITY_DOCS
        if (root / path).is_file()
    )
    for marker in BOUNDARY_MARKERS:
        if marker not in boundary_text:
            findings.append(Finding("AUTHORITY_BOUNDARY", "HIGH", "<security-docs>", f"missing {marker}"))

    for relative in REQUIRED_SECURITY_DOCS:
        source = root / relative
        if not source.is_file() or source.suffix.lower() != ".md":
            continue
        for target in MARKDOWN_LINK.findall(source.read_text(encoding="utf-8", errors="replace")):
            if not _relative_link_exists(root, source, target):
                findings.append(Finding("STALE_SECURITY_LINK", "MEDIUM", relative, target))

    workflows = tuple(path for path in tracked if path.startswith(".github/workflows/") and path.endswith((".yml", ".yaml")))
    for relative in workflows:
        text = (root / relative).read_text(encoding="utf-8", errors="replace")
        if not re.search(r"(?m)^permissions:\s*(?:$|read-all\s*$|{})", text):
            findings.append(
                Finding("WORKFLOW_PERMISSION_REVIEW", "MEDIUM", relative, "no explicit top-level permissions baseline")
            )

    ordered = sorted(findings, key=lambda item: (item.severity, item.check, item.path, item.detail))
    receipt = {
        "schema_version": "aion.repository-security-audit.v0.1.0",
        "mode": "READ_ONLY",
        "repository_commit_sha": commit_sha,
        "repository_tree_sha": tree_sha,
        "tracked_file_count": len(tracked),
        "checks": {
            "unexpected_binary_suffixes": sorted(UNEXPECTED_BINARY_SUFFIXES),
            "high_confidence_secret_patterns": [name for name, _ in SECRET_PATTERNS],
            "required_security_docs": list(REQUIRED_SECURITY_DOCS),
            "authority_boundary_markers": list(BOUNDARY_MARKERS),
            "workflow_top_level_permissions": True,
            "security_doc_relative_links": True,
            "external_download_instruction_inventory": True,
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
    parser = argparse.ArgumentParser(description="Read-only tracked-file repository security audit")
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
