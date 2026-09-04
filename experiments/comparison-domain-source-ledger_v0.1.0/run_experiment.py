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

C1_SURFACES = REGISTERS + FETCH_MANIFESTS

LEGAL_RESULTS = ("SUPPORTED", "PARTIALLY_SUPPORTED", "NOT_SUPPORTED")
ENTRY_OUTCOMES = ("MATCH", "MISMATCH", "MISSING", "NOT_APPLICABLE")


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
    for relpath in C1_SURFACES:
        try:
            data = load_json(relpath)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            failures.append(f"{relpath}: {exc}")
            rows.append({"path": relpath, "kind": "register_or_manifest", "ok": False, "error": str(exc)})
            continue
        kind = "fetch_manifest" if relpath in FETCH_MANIFESTS else "register"
        rows.append({"path": relpath, "kind": kind, "ok": True, "source_count": len(data["sources"]), "ids": [source_id(item) if isinstance(item, dict) else "(invalid)" for item in data["sources"]]})
    return {"claim": "C1_REGISTER_AND_MANIFEST_FILES_PARSE_WITH_SOURCES_ARRAY", "result": "SUPPORTED" if not failures else "NOT_SUPPORTED", "surfaces_expected": list(C1_SURFACES), "surfaces_checked": len(rows), "failures": failures, "rows": rows}


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
    return {"claim": "C2_LICENSE_OR_USAGE_METADATA_PRESENT", "result": "SUPPORTED" if not failures else "NOT_SUPPORTED", "note": "Presence of a recorded string only. Legal validity of the license is NOT_ESTABLISHED.", "failures": failures, "rows": rows}


def check_local_hashes() -> dict[str, Any]:
    entries = []
    for relpath in FETCH_MANIFESTS:
        data = load_json(relpath)
        for item in data["sources"]:
            if not isinstance(item, dict):
                entries.append({"manifest": relpath, "source_id": "(invalid)", "outcome": "MISSING", "reason": "non_object_source"})
                continue
            sid = source_id(item)
            repo_path = item.get("repository_path")
            expected = item.get("repository_sha256")
            if not repo_path:
                entries.append({"manifest": relpath, "source_id": sid, "outcome": "NOT_APPLICABLE", "reason": "no_checked_in_path", "retention_policy": item.get("retention_policy")})
                continue
            path = ROOT / str(repo_path)
            row: dict[str, Any] = {"manifest": relpath, "source_id": sid, "path": repo_path, "expected_repository_sha256": expected}
            if not path.is_file():
                row.update({"outcome": "MISSING", "reason": "missing_file"})
                entries.append(row)
                continue
            actual = sha256_file(path)
            row["actual_sha256"] = actual
            row["bytes"] = path.stat().st_size
            if isinstance(expected, str) and actual == expected:
                row["outcome"] = "MATCH"
            else:
                row["outcome"] = "MISMATCH"
                row["reason"] = "hash_mismatch_or_missing_expected"
            entries.append(row)
    checked_in = [row for row in entries if row["outcome"] != "NOT_APPLICABLE"]
    coverage = {"checked_in_n": len(checked_in), "match": sum(1 for row in checked_in if row["outcome"] == "MATCH"), "mismatch": sum(1 for row in checked_in if row["outcome"] == "MISMATCH"), "missing": sum(1 for row in checked_in if row["outcome"] == "MISSING"), "not_applicable": sum(1 for row in entries if row["outcome"] == "NOT_APPLICABLE")}
    coverage["match_coverage"] = f"{coverage['match']}/{coverage['checked_in_n']}" if coverage["checked_in_n"] else "0/0"
    outcomes_reported = bool(entries) and all(row.get("outcome") in ENTRY_OUTCOMES for row in entries)
    all_checked_in_match = coverage["checked_in_n"] > 0 and coverage["match"] == coverage["checked_in_n"]
    child_claims = [{"claim": "C3A_PER_ENTRY_OUTCOMES_REPORTED", "result": "SUPPORTED" if outcomes_reported else "NOT_SUPPORTED"}, {"claim": "C3B_ALL_CHECKED_IN_HASHES_MATCH", "result": "SUPPORTED" if all_checked_in_match else "NOT_SUPPORTED"}]
    return {"claim": "C3_CHECKED_IN_HASH_COVERAGE", "result": aggregate_results([item["result"] for item in child_claims]), "note": "C3 is coverage, not a universal match claim. C3B is NOT_SUPPORTED unless every checked-in hash matches. HASH_ONLY payloads are NOT_APPLICABLE. External URL content is not fetched.", "coverage": coverage, "child_claims": child_claims, "entries": entries, "hashed": [row for row in entries if row["outcome"] in {"MATCH", "MISMATCH", "MISSING"} and "path" in row], "skipped_not_applicable": [row for row in entries if row["outcome"] == "NOT_APPLICABLE"]}


def aggregate_results(results: list[str]) -> str:
    unique = set(results)
    if not unique:
        return "NOT_SUPPORTED"
    if unique == {"SUPPORTED"}:
        return "SUPPORTED"
    if unique == {"NOT_SUPPORTED"}:
        return "NOT_SUPPORTED"
    if unique <= set(LEGAL_RESULTS):
        return "PARTIALLY_SUPPORTED"
    return "NOT_SUPPORTED"


def verdict(parts: list[dict[str, Any]]) -> str:
    results: list[str] = []
    for item in parts:
        results.append(item["result"])
        for child in item.get("child_claims") or []:
            results.append(child["result"])
    return aggregate_results(results)


def render_ledger(report: dict[str, Any]) -> str:
    c3 = next(item for item in report["claims"] if item["claim"] == "C3_CHECKED_IN_HASH_COVERAGE")
    coverage = c3["coverage"]
    lines = ["# Derived source ledger — EX-001", "", "```text", "AUTHORITY = NONE", "DERIVED_FROM = existing domain registers and fetch manifests", "SUBJECTIVITY_EVIDENCE_WEIGHT = 0", "```", "", "This file is generated from existing typed surfaces. Cite the original", "register or manifest, not this report.", "", f"Generated (UTC): {report['generated_utc']}", f"Head SHA recorded by runner: {report['head_sha_if_available']}", "", "## Claims", ""]
    for item in report["claims"]:
        lines.append(f"- `{item['claim']}` = `{item['result']}`")
        for child in item.get("child_claims") or []:
            lines.append(f"  - `{child['claim']}` = `{child['result']}`")
    lines.extend(["", "## C3 coverage", "", f"- checked_in_n = {coverage['checked_in_n']}", f"- MATCH = {coverage['match']}", f"- MISMATCH = {coverage['mismatch']}", f"- MISSING = {coverage['missing']}", f"- NOT_APPLICABLE = {coverage['not_applicable']}", f"- match_coverage = {coverage['match_coverage']}", "", "## Per-entry checked-in outcomes", ""])
    for row in c3["hashed"]:
        lines.append(f"- `{row.get('source_id')}` `{row.get('path')}` `{row.get('outcome')}`")
    lines.extend(["", "## Not applicable (no checked-in payload)", ""])
    for row in c3["skipped_not_applicable"]:
        lines.append(f"- `{row['source_id']}` retention=`{row.get('retention_policy')}` outcome=NOT_APPLICABLE")
    lines.extend(["", "## Limits", "", "- External URL current content: NOT_VERIFIED", "- Legal license effectiveness: NOT_ESTABLISHED", "- Subjectivity / causal validation of comparison domains: NOT_ESTABLISHED", ""])
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
    report = {"experiment": "comparison-domain-source-ledger_v0.1.0", "experiment_id": "EX-001", "kind": "PROVENANCE_REPOSITORY_INTEGRITY", "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "head_sha_if_available": current_head(), "network_used": False, "paid_api_used": False, "claims": claims, "aggregate_of_narrow_claims": verdict(claims), "SUBJECTIVITY_CONCLUSION": "NOT_ESTABLISHED", "SUBJECTIVITY_EVIDENCE_WEIGHT": 0, "CANONICAL_EFFECT": "NONE", "DEPLOYMENT": False, "LEDGER_AUTHORITY": "NONE_DERIVED_REPORT_ONLY", "PR_DIFF_INCLUDES_SANDBOX_RULES": True, "MAIN_TRANSITION_AUTHORITY_GATE": "UNCHANGED_NOT_BYPASSED", "non_claims": ["external URL current content not verified", "license legal effectiveness not established", "comparison-domain causal validity not established", "subjectivity not established"]}
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
