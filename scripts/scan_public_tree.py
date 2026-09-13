from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROHIBITED_SUFFIXES = {".zip", ".whl", ".sqlite3", ".db", ".pyc"}
GENERATED_PARTS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "build", "dist"}
EXTERNAL_EVIDENCE_PARTS = {"sources", "incident-originals"}
PATH_PATTERNS = [
    re.compile(r"[A-Za-z]:\\{1,2}Users\\{1,2}[A-Za-z0-9._-]+", re.I),
    re.compile(r"^/home/[A-Za-z0-9._-]+(?:/|$)"),
]
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
]

# Unicode format controls (category Cf) are machine-readable while commonly
# rendering invisibly. A few additional code points/ranges are visually blank or
# selector-only without being Cf. Project-owned tracked UTF-8 text fails closed on
# these classes. Retained external-source paths are reported as signals instead of
# being rewritten or promoted into project provenance evidence.
EXTRA_IMPERCEPTIBLE_CODEPOINTS = {
    0x034F,  # COMBINING GRAPHEME JOINER
    0x115F,  # HANGUL CHOSEONG FILLER
    0x1160,  # HANGUL JUNGSEONG FILLER
    0x17B4,  # KHMER VOWEL INHERENT AQ
    0x17B5,  # KHMER VOWEL INHERENT AA
    0x3164,  # HANGUL FILLER
    0xFFA0,  # HALFWIDTH HANGUL FILLER
}
EXTRA_IMPERCEPTIBLE_RANGES = (
    (0xE0100, 0xE01EF, "VARIATION SELECTOR SUPPLEMENT"),
)


def _is_generated(path: Path) -> bool:
    return (
        any(part in GENERATED_PARTS or part.endswith(".egg-info") for part in path.parts)
        or path.name == ".coverage"
    )


def _is_external_evidence(path: Path, root: Path) -> bool:
    return any(part in EXTERNAL_EVIDENCE_PARTS for part in path.relative_to(root).parts)


def _imperceptible_reason(char: str) -> str | None:
    codepoint = ord(char)
    if unicodedata.category(char) == "Cf":
        return unicodedata.name(char, "UNICODE FORMAT CONTROL")
    if codepoint in EXTRA_IMPERCEPTIBLE_CODEPOINTS:
        return unicodedata.name(char, "INVISIBLE UNICODE CHARACTER")
    for start, end, label in EXTRA_IMPERCEPTIBLE_RANGES:
        if start <= codepoint <= end:
            return f"{label} {codepoint - start + 1}"
    return None


def _find_imperceptible_markers(text: str) -> list[tuple[int, int, int, str]]:
    findings: list[tuple[int, int, int, str]] = []
    line = 1
    column = 0
    for char in text:
        column += 1
        reason = _imperceptible_reason(char)
        if reason is not None:
            findings.append((line, column, ord(char), reason))
        if char == "\n":
            line += 1
            column = 0
    return findings


def scan_root_detailed(root: Path = ROOT) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    external_marker_signals: list[str] = []
    for path in root.rglob("*"):
        if path.is_symlink() or not path.is_file() or ".git" in path.parts:
            continue
        if _is_generated(path):
            continue
        rel = path.relative_to(root).as_posix()
        if rel == "scripts/scan_public_tree.py":
            continue
        if path.suffix.lower() in PROHIBITED_SUFFIXES:
            errors.append(f"prohibited file: {rel}")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"non-UTF8 file: {rel}")
            continue
        for pattern in PATH_PATTERNS:
            if pattern.search(text):
                errors.append(f"private path pattern: {rel}")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"secret pattern: {rel}")
        for line, column, codepoint, reason in _find_imperceptible_markers(text):
            finding = f"{rel}:{line}:{column} U+{codepoint:04X} {reason}"
            if _is_external_evidence(path, root):
                external_marker_signals.append(f"external imperceptible marker signal: {finding}")
            else:
                errors.append(f"imperceptible marker: {finding}")
    return errors, external_marker_signals


def scan_root(root: Path = ROOT) -> list[str]:
    errors, _ = scan_root_detailed(root)
    return errors


def main() -> int:
    errors, external_marker_signals = scan_root_detailed()
    print(
        json.dumps(
            {
                "status": "PASS" if not errors else "FAIL",
                "errors": errors,
                "external_marker_signals": external_marker_signals,
                "watermark_detection_scope": (
                    "bounded to detectable high-risk invisible Unicode controls in UTF-8 text; "
                    "PASS does not prove absence of statistical, binary-media, metadata, "
                    "provider-side or other steganographic watermarking"
                ),
            },
            indent=2,
        )
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
