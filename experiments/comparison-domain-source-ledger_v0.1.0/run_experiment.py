#!/usr/bin/env python3
"""Offline provenance check over existing comparison-domain registers."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent

REGISTERS = (
    "examples/bazi-capability_v0.1.1/docs/BAZI_RULE_SOURCE_REGISTER.json",
    "examples/bazi-capability_v0.1.1/docs/CALENDAR_ENGINE_SOURCE_REGISTER.json",
    "examples/classical-western-astrology_v0.1.0/docs/SOURCE_REGISTER.json",
    "examples/zi-wei-dou-shu_v0.1.0/docs/SOURCE_REGISTER.json",
)

FETCH_MANIFESTS = (
    "examples/bazi-capability_v0.1.1/sources/SOURCE_FETCH_MANIFEST.json",
    "examples/classical-western-astrology_v0.1.0/sources/SOURCE_FETCH_MANIFEST.json",
    "examples/zi-wei-dou-shu_v0.1.0/sources/SOURCE_FETCH_MANIFEST.json",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(relpath: str) -> dict[str, Any]:
    path = ROOT / relpath
    if not path.is_file():
        raise FileNotFoundError(relpath)
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{relpath} is not a JSON object")
    if "sources" not in data or not isinstance(data["sources"], list):
        raise ValueError(f"{relpath} has no sources array")
    return data


def source_id(entry: dict[str, Any]) -> str:
    for key in ("source_id", "id"):
        value = entry.get(key)
        if isinstance(value, str) and value:
            return value
    return "(unnamed)"


def check_registers() -> dict[str, Any]:
    rows = []
    failures = []
    for relpath in REGISTERS:
        try:
            data = load_json(relpath)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            failures.append(f"{relpath}: {exc}")
            rows.append({"path": relpath, "ok": False, "error": str(exc)})
            continue
        rows.append(
            {
                "path": relpath,
                "ok": True,
                "source_count": len(data["sources"]),
                "ids": [source_id(item) if isinstance(item, dict) else "(invalid)" for item in data["sources"]],
            }
        )
    return {
        "claim": "C1_REGISTER_FILES_PARSE_WITH_SOURCES_ARRAY",
        "result": "SUPPORTED" if not failures else "NOT_SUPPORTED",
        "failures": failures,
        "rows": rows,
    }


def check_license_metadata() -> dict[str, Any]:
    failures = []
    rows = []
    for relpath in FETCH_MANIFESTS:
        data = load_json(relpath)
        for item in data["sources"]:
            if not isinstance(item, dict):
                failures.append(f"{relpath}: non-object source")
                continue
            sid = source_id(item)
            present = isinstance(item.get("license_or_terms"), str) and bool(item.get("license_or_terms"))
            rows.append({"manifest": relpath, "source_id": sid, "license_or_terms_present": present})
            if not present:
                failures.append(f"{relpath}:{sid} missing license_or_terms")
    calendar = load_json("examples/bazi-capability_v0.1.1/docs/CALENDAR_ENGINE_SOURCE_REGISTER.json")
    for item in calendar["sources"]:
        if not isinstance(item, dict):
            failures.append("calendar register: non-object source")
            continue
        sid = source_id(item)
        present = isinstance(item.get("license"), str) and bool(item.get("license"))
        rows.append({"manifest": "CALENDAR_ENGINE_SOURCE_REGISTER.json", "source_id": sid, "license_present": present})
        if not present:
            failures.append(f"calendar register:{sid} missing license")
    return {
        "claim": "C2_LICENSE_OR_USAGE_METADATA_PRESENT",
        "result": "SUPPORTED" if not failures else "NOT_SUPPORTED",
        "note": "Presence of a recorded string only. Legal validity of the license is NOT_ESTABLISHED.",
        "failures": failures,
        "rows": rows,
    }


def check_local_hashes() -> dict[str, Any]:
    failures = []
    hashed = []
    skipped = []
    for relpath in FETCH_MANIFESTS:
        data = load_json(relpath)
        for item in data["sources"]:
            if not isinstance(item, dict):
                failures.append(f"{relpath}: non-object source")
                continue
            sid = source_id(item)
            repo_path = item.get("repository_path")
            expected = item.get("repository_sha256")
            if not repo_path:
                skipped.append(
                    {
                        "manifest": relpath,
                        "source_id": sid,
                        "reason": "no_checked_in_path",
                        "retention_policy": item.get("retention_policy"),
                        "local_hash": "NOT_APPLICABLE",
                    }
                )
                continue
            path = ROOT / str(repo_path)
            if not path.is_file():
                failures.append(f"{sid}: missing file {repo_path}")
                hashed.append({"source_id": sid, "path": repo_path, "ok": False, "error": "missing_file"})
                continue
            actual = sha256_file(path)
            match = isinstance(expected, str) and actual == expected
            hashed.append(
                {
                    "source_id": sid,
                    "path": repo_path,
                    "expected_repository_sha256": expected,
                    "actual_sha256": actual,
                    "ok": match,
                }
            )
            if not match:
                failures.append(f"{sid}: hash mismatch or missing repository_sha256")
    if not hashed and not failures:
        result = "NOT_SUPPORTED"
    elif failures and hashed and any(row.get("ok") for row in hashed):
        result = "PARTIALLY_SUPPORTED"
    elif failures:
        result = "NOT_SUPPORTED"
    else:
        result = "SUPPORTED"
    return {
        "claim": "C3_CHECKED_IN_CONTENT_HASH_RECOMPUTES",
        "result": result,
        "note": "HASH_ONLY / discarded payloads are NOT_APPLICABLE. External URL content is not fetched. Working-tree SHA-256 is compared to repository_sha256 recorded in the existing fetch manifest.",
        "failures": failures,
        "hashed": hashed,
        "skipped_not_applicable": skipped,
    }


def verdict(parts: list[dict[str, Any]]) -> str:
    results = {item["result"] for item in parts}
    if results == {"SUPPORTED"}:
        return "SUPPORTED"
    if "NOT_SUPPORTED" in results and "SUPPORTED" in results:
        return "PARTIALLY_SUPPORTED"
    if results == {"NOT_SUPPORTED"}:
        return "NOT_SUPPORTED"
    return "PARTIALLY_SUPPORTED"


def render_ledger(report: dict[str, Any]) -> str:
    lines = [
        "# Derived source ledger — EX-001",
        "",
        "```text",
        "AUTHORITY = NONE",
        "DERIVED_FROM = existing domain registers and fetch manifests",
        "SUBJECTIVITY_EVIDENCE_WEIGHT = 0",
        "```",
        "",
        "This file is generated from existing typed surfaces. Cite the original",
        "register or manifest, not this report.",
        "",
        f"Generated (UTC): {report['generated_utc']}",
        f"Head SHA recorded by runner: {report['head_sha_if_available']}",
        "",
        "## Claims",
        "",
    ]
    for item in report["claims"]:
        lines.append(f"- `{item['claim']}` = `{item['result']}`")
    lines.extend(["", "## Checked-in files whose SHA-256 was recomputed", ""])
    for row in report["claims"][2]["hashed"]:
        mark = "MATCH" if row.get("ok") else "FAIL"
        lines.append(f"- `{row.get('source_id')}` `{row.get('path')}` `{mark}`")
    lines.extend(["", "## Not applicable (no checked-in payload)", ""])
    for row in report["claims"][2]["skipped_not_applicable"]:
        lines.append(
            f"- `{row['source_id']}` retention=`{row.get('retention_policy')}` local_hash=NOT_APPLICABLE"
        )
    lines.extend(
        [
            "",
            "## Limits",
            "",
            "- External URL current content: NOT_VERIFIED",
            "- Legal license effectiveness: NOT_ESTABLISHED",
            "- Subjectivity / causal validation of comparison domains: NOT_ESTABLISHED",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def current_head() -> str:
    git_head = ROOT / ".git" / "HEAD"
    if not git_head.is_file():
        return "UNKNOWN"
    text = git_head.read_text(encoding="utf-8").strip()
    if text.startswith("ref:"):
        ref = ROOT / ".git" / text.split(" ", 1)[1]
        if ref.is_file():
            return ref.read_text(encoding="utf-8").strip()
        return text
    return text


def run(write_derived: bool = False) -> dict[str, Any]:
    claims = [check_registers(), check_license_metadata(), check_local_hashes()]
    report = {
        "experiment": "comparison-domain-source-ledger_v0.1.0",
        "experiment_id": "EX-001",
        "kind": "PROVENANCE_REPOSITORY_INTEGRITY",
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "head_sha_if_available": current_head(),
        "network_used": False,
        "paid_api_used": False,
        "claims": claims,
        "aggregate_of_narrow_claims": verdict(claims),
        "SUBJECTIVITY_CONCLUSION": "NOT_ESTABLISHED",
        "SUBJECTIVITY_EVIDENCE_WEIGHT": 0,
        "CANONICAL_EFFECT": "NONE",
        "DEPLOYMENT": False,
        "LEDGER_AUTHORITY": "NONE_DERIVED_REPORT_ONLY",
        "non_claims": [
            "external URL current content not verified",
            "license legal effectiveness not established",
            "comparison-domain causal validity not established",
            "subjectivity not established",
        ],
    }
    if write_derived:
        (HERE / "RESULT.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (HERE / "LEDGER.md").write_text(render_ledger(report), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-derived", action="store_true")
    args = parser.parse_args()
    report = run(write_derived=args.write_derived)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["aggregate_of_narrow_claims"] != "NOT_SUPPORTED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
