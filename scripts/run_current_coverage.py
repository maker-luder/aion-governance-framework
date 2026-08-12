from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = sorted(
    [path for path in (ROOT / "components").iterdir() if (path / "tests").is_dir()]
    + [path for path in (ROOT / "examples").iterdir() if (path / "tests").is_dir()]
    + [path for path in (ROOT / "research-labs").iterdir() if (path / "tests").is_dir()]
)
SOURCE_ROOTS = [
    ROOT / "research-labs" / "language-core-g1_v0.2.1" / "src",
    ROOT / "components" / "governance_kernel_v0.4.0" / "src",
    ROOT / "components" / "astra_workbench_v1.0.0" / "src",
] + sorted(ROOT.glob("components/*/src")) + sorted(ROOT.glob("examples/*/src")) + sorted(ROOT.glob("research-labs/*/src"))


def _target_environment(target_src: Path) -> dict[str, str]:
    env = os.environ.copy()
    ordered = [target_src] + [path for path in SOURCE_ROOTS if path != target_src and path.is_dir()]
    env["PYTHONPATH"] = os.pathsep.join(str(path) for path in ordered)
    return env


def _sanitize_output(output: str) -> str:
    lines = []
    for line in output.splitlines():
        if "Coverage JSON written to file" in line:
            lines.append("Coverage JSON written to file <temporary-coverage-artifact>")
        else:
            lines.append(line)
    return "\n".join(lines) + ("\n" if output else "")


def collect_current_coverage() -> tuple[list[dict[str, object]], int]:
    records: list[dict[str, object]] = []
    failed = 0
    for target in TARGETS:
        target_src = target / "src"
        with tempfile.TemporaryDirectory(prefix="aion-coverage-") as temporary:
            report_path = Path(temporary) / "coverage.json"
            command = [
                sys.executable,
                "-m",
                "pytest",
                "-q",
                "-o",
                "addopts=",
                "--cov",
                str(target_src),
                "--cov-branch",
                "--cov-report",
                "term-missing",
                "--cov-report",
                f"json:{report_path}",
            ]
            environment = _target_environment(target_src)
            environment["COVERAGE_FILE"] = str(Path(temporary) / ".coverage")
            process = subprocess.run(
                command,
                cwd=target,
                env=environment,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
            )
            if process.returncode:
                failed += 1
            coverage = json.loads(report_path.read_text(encoding="utf-8")) if report_path.is_file() else {}
            records.append(
                {
                    "target": str(target.relative_to(ROOT)),
                    "returncode": process.returncode,
                    "totals": coverage.get("totals", {}),
                    "output": _sanitize_output(process.stdout),
                }
            )
    return records, failed


def write_coverage_evidence(records: list[dict[str, object]], target_head: str) -> None:
    results_path = ROOT / "qa" / "CURRENT_COVERAGE_RESULTS.json"
    results_path.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    envelope = {
        "schema_version": "0.1.0",
        "target_head": target_head,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "target_count": len(records),
        "results_ref": "qa/CURRENT_COVERAGE_RESULTS.json",
        "branch_coverage": True,
        "whole_system_validation": "NOT_ESTABLISHED",
        "independent_ivv": "NOT_ACHIEVED",
        "canonical_effect": "NONE",
        "deployment": False,
    }
    (ROOT / "qa" / "CURRENT_COVERAGE_EVIDENCE.json").write_text(json.dumps(envelope, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rows = [
        "# Current Reconstruction Coverage Report",
        "",
        f"Target head: `{target_head}`. Coverage was measured with branch coverage enabled for {len(records)} targets.",
        "",
        "| Target | Branch coverage | Return code |",
        "|---|---:|---:|",
    ]
    for record in records:
        totals = record.get("totals", {})
        display = totals.get("percent_covered_display", "NOT_RECORDED")
        rows.append(f"| `{record['target']}` | {display}% | {record['returncode']} |")
    rows.extend([
        "",
        "Coverage percentages describe executed public test suites; they are not whole-system validation, independent IV&V, deployment readiness or scientific evidence.",
        "",
    ])
    (ROOT / "qa" / "COVERAGE_REPORT.md").write_text("\n".join(rows), encoding="utf-8")


def main() -> int:
    records, failed = collect_current_coverage()
    try:
        target_head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        target_head = "UNSPECIFIED"
    write_coverage_evidence(records, target_head)
    print(f"coverage_targets={len(records)}")
    print(f"coverage_failed_targets={failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
