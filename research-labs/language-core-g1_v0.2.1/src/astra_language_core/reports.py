from __future__ import annotations

import json
from pathlib import Path

from .errors import ArtifactExistsError, ValidationError
from .json_types import JsonValue


def _load_run(path: Path) -> dict[str, JsonValue]:
    value: JsonValue = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not isinstance(value.get("records"), list):
        raise ValidationError(f"invalid run report: {path}")
    return value


def compare_runs(baseline_path: Path, candidate_path: Path) -> dict[str, JsonValue]:
    baseline = _load_run(baseline_path)
    candidate = _load_run(candidate_path)
    baseline_records = baseline["records"]
    candidate_records = candidate["records"]
    if not isinstance(baseline_records, list) or not isinstance(candidate_records, list):
        raise ValidationError("run records must be arrays")
    return {
        "baseline_run_id": baseline.get("run_id"),
        "candidate_run_id": candidate.get("run_id"),
        "baseline_record_count": len(baseline_records),
        "candidate_record_count": len(candidate_records),
        "side_effect_score": "NOT_COMPUTED_WITHOUT_OWNER_THRESHOLDS",
        "dimension_preservation": "REQUIRED",
        "canonical_effect": "NONE",
    }


def write_json_report(report: dict[str, JsonValue], output: Path) -> Path:
    if output.exists():
        raise ArtifactExistsError(f"report exists: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return output


def write_markdown_report(report: dict[str, JsonValue], output: Path) -> Path:
    if output.exists():
        raise ArtifactExistsError(f"report exists: {output}")
    lines = ["# Astra Language Core Comparison", "", "Status: `QA_HOLD`", ""]
    lines.extend(f"- **{key}**: `{value}`" for key, value in report.items())
    lines.extend(["", "This report has no canonical effect.", ""])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    return output
