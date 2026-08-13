import json
import subprocess
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError

from aion_iqc.inspector import CheckStatus, InspectionPolicy, inspect_repository


def make_root(
    tmp_path: Path,
    *,
    tests: int = 2,
    target_count: int = 1,
    public_scan: str = "PASS",
    deployment: bool = False,
    coverage_head: str = "UNSPECIFIED",
) -> Path:
    root = tmp_path / "repo"
    (root / "qa").mkdir(parents=True)
    (root / "docs").mkdir()
    for index in range(target_count):
        target_root = root / "components" / f"example_{index}"
        target_root.mkdir(parents=True)
        (target_root / "README.md").write_text("test fixture\n", encoding="utf-8")
        (target_root / "pyproject.toml").write_text("[project]\nname = 'fixture'\nversion = '0.0.0'\n", encoding="utf-8")
    results = [
        {
            "target": f"components/example_{index}",
            "returncode": 0,
            "output": f"{tests} passed in 0.01s\n",
        }
        for index in range(target_count)
    ]
    (root / "qa" / "CURRENT_TEST_RESULTS.json").write_text(json.dumps(results), encoding="utf-8")
    (root / "qa" / "CURRENT_RELEASE_STATUS_LOCK.json").write_text(
        json.dumps(
            {
                "current_tests": f"{tests * target_count} PASSED",
                "current_targets": target_count,
                "eligible_target_count": target_count,
                "tested_target_count": target_count,
                "non_applicable_target_count": 0,
                "whole_system_validation": "NOT_ESTABLISHED",
                "public_scan": public_scan,
                "canonical_effect": "NONE",
                "independent_ivv": "NOT_ACHIEVED",
                "deployment": deployment,
            }
        ),
        encoding="utf-8",
    )
    (root / "docs" / "C0_EXTERNAL_STANDARDS_CROSSWALK_2026-08-08.md").write_text(
        "ISO/IEC 25040\nISO/IEC 25041\nNASA SWE-034\nCERTIFICATION_CLAIM = FALSE\n",
        encoding="utf-8",
    )
    (root / "qa" / "NCR_CAPA_REGISTER.md").write_text("NCR\nCorrective action\n", encoding="utf-8")
    coverage_results = [
        {
            "target": f"components/example_{index}",
            "returncode": 0,
            "totals": {"percent_covered": 80.0, "percent_covered_display": "80"},
            "output": "coverage evidence\n",
        }
        for index in range(target_count)
    ]
    (root / "qa" / "CURRENT_COVERAGE_RESULTS.json").write_text(json.dumps(coverage_results), encoding="utf-8")
    (root / "qa" / "CURRENT_COVERAGE_EVIDENCE.json").write_text(
        json.dumps(
            {
                "target_head": coverage_head,
                "target_count": target_count,
                "branch_coverage": True,
                "whole_system_validation": "NOT_ESTABLISHED",
            }
        ),
        encoding="utf-8",
    )
    (root / "qa" / "CURRENT_EVIDENCE_TRACEABILITY.json").write_text(
        json.dumps(
            {
                "status": "PASS",
                "target_head": coverage_head,
                "criterion_count": 1,
                "records": [{"criterion": "AC-SCOPE-01"}],
                "acceptance_decision": "NOT_EVALUATED",
                "canonical_effect": "NONE",
                "deployment": False,
                "independent_ivv": "NOT_ACHIEVED",
                "mutation_performed": False,
                "diagnostics": {"malformed_criteria": [], "missing_local_refs": []},
            }
        ),
        encoding="utf-8",
    )
    return root


def test_iqc_passes_closed_boundaries_and_matching_test_evidence(tmp_path: Path) -> None:
    root = make_root(tmp_path, coverage_head="abc123")
    before = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))
    report = inspect_repository(
        root,
        target_head="abc123",
        policy=InspectionPolicy(required_test_target_count=1),
        generated_at="2026-08-12T00:00:00+00:00",
    )
    after = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))
    assert report.verdict is CheckStatus.PASS
    assert report.canonical_effect == "NONE"
    assert report.mutation_performed is False
    assert before == after
    assert all(check.status is CheckStatus.PASS for check in report.checks)


def test_iqc_holds_when_status_count_is_stale(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    lock = json.loads((root / "qa" / "CURRENT_RELEASE_STATUS_LOCK.json").read_text(encoding="utf-8"))
    lock["current_tests"] = "999 PASSED"
    (root / "qa" / "CURRENT_RELEASE_STATUS_LOCK.json").write_text(json.dumps(lock), encoding="utf-8")
    report = inspect_repository(root, policy=InspectionPolicy(required_test_target_count=1))
    assert report.verdict is CheckStatus.HOLD
    assert any(check.check_id == "IQC-TEST-001" and check.status is CheckStatus.HOLD for check in report.checks)


def test_iqc_holds_when_scoped_target_counts_are_stale(tmp_path: Path) -> None:
    root = make_root(tmp_path, target_count=2)
    lock = json.loads((root / "qa" / "CURRENT_RELEASE_STATUS_LOCK.json").read_text(encoding="utf-8"))
    lock["tested_target_count"] = 1
    lock["non_applicable_target_count"] = 1
    (root / "qa" / "CURRENT_RELEASE_STATUS_LOCK.json").write_text(json.dumps(lock), encoding="utf-8")
    report = inspect_repository(root)
    assert report.verdict is CheckStatus.HOLD
    test_gate = next(check for check in report.checks if check.check_id == "IQC-TEST-001")
    assert test_gate.status is CheckStatus.HOLD
    assert "tested_target_count" in test_gate.detail


def test_iqc_holds_when_whole_system_semantics_conflict(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    evidence = json.loads((root / "qa" / "CURRENT_COVERAGE_EVIDENCE.json").read_text(encoding="utf-8"))
    evidence["whole_system_validation"] = "PASS"
    (root / "qa" / "CURRENT_COVERAGE_EVIDENCE.json").write_text(json.dumps(evidence), encoding="utf-8")
    report = inspect_repository(root)
    assert report.verdict is CheckStatus.HOLD
    semantic = next(check for check in report.checks if check.check_id == "IQC-SEM-001")
    assert semantic.status is CheckStatus.HOLD
    assert "conflict" in semantic.detail


def test_iqc_holds_when_coverage_target_set_is_stale(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    coverage = json.loads((root / "qa" / "CURRENT_COVERAGE_RESULTS.json").read_text(encoding="utf-8"))
    coverage.append({"target": "components/stale", "returncode": 0, "totals": {"percent_covered": 80.0}, "output": ""})
    (root / "qa" / "CURRENT_COVERAGE_RESULTS.json").write_text(json.dumps(coverage), encoding="utf-8")
    report = inspect_repository(root)
    assert report.verdict is CheckStatus.HOLD
    measurement = next(check for check in report.checks if check.check_id == "IQC-MEAS-001")
    assert measurement.status is CheckStatus.HOLD


def test_iqc_holds_when_coverage_head_is_stale(tmp_path: Path) -> None:
    root = make_root(tmp_path, coverage_head="old-head")
    report = inspect_repository(root, target_head="new-head")
    assert report.verdict is CheckStatus.HOLD
    measurement = next(check for check in report.checks if check.check_id == "IQC-MEAS-001")
    assert measurement.status is CheckStatus.HOLD


def test_iqc_passes_traceability_and_component_contract_checks(tmp_path: Path) -> None:
    root = make_root(tmp_path, coverage_head="abc123")
    report = inspect_repository(
        root,
        target_head="abc123",
        policy=InspectionPolicy(require_traceability=True, require_component_contracts=True),
    )
    assert report.verdict is CheckStatus.PASS
    assert next(check for check in report.checks if check.check_id == "IQC-TRACE-001").status is CheckStatus.PASS
    assert next(check for check in report.checks if check.check_id == "IQC-PKG-001").status is CheckStatus.PASS


def test_iqc_holds_when_traceability_artifact_is_missing(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    (root / "qa" / "CURRENT_EVIDENCE_TRACEABILITY.json").unlink()
    report = inspect_repository(root, policy=InspectionPolicy(require_traceability=True))
    assert report.verdict is CheckStatus.HOLD
    assert next(check for check in report.checks if check.check_id == "IQC-TRACE-001").status is CheckStatus.HOLD


def test_iqc_holds_when_component_contract_is_incomplete(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    (root / "components" / "example_0" / "pyproject.toml").unlink()
    report = inspect_repository(root, policy=InspectionPolicy(require_component_contracts=True))
    assert report.verdict is CheckStatus.HOLD
    assert next(check for check in report.checks if check.check_id == "IQC-PKG-001").status is CheckStatus.HOLD


def test_iqc_fails_open_boundary(tmp_path: Path) -> None:
    root = make_root(tmp_path, deployment=True)
    report = inspect_repository(root)
    assert report.verdict is CheckStatus.FAIL
    boundary = next(check for check in report.checks if check.check_id == "IQC-GOV-001")
    assert boundary.status is CheckStatus.FAIL


def test_iqc_holds_when_public_scan_is_not_pass(tmp_path: Path) -> None:
    root = make_root(tmp_path, public_scan="HOLD")
    report = inspect_repository(root)
    assert report.verdict is CheckStatus.HOLD
    public_release = next(check for check in report.checks if check.check_id == "IQC-REL-001")
    assert public_release.status is CheckStatus.HOLD


def test_iqc_report_shape_preserves_inspection_only_boundary(tmp_path: Path) -> None:
    report = inspect_repository(make_root(tmp_path))
    payload = report.as_dict()
    assert payload["schema_version"] == "0.1.0"
    assert payload["evaluator_role"] == "REPOSITORY_IQC_INSPECTION_ONLY"
    assert payload["canonical_effect"] == "NONE"
    assert payload["independent_ivv_status"] == "NOT_ACHIEVED"
    assert payload["mutation_performed"] is False


def test_iqc_report_schema_accepts_valid_report_and_rejects_promotion(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    report = inspect_repository(root, generated_at="2026-08-12T00:00:00+00:00")
    schema = json.loads((Path(__file__).resolve().parents[1] / "qa" / "iqc_report.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    validator.validate(report.as_dict())
    promoted = report.as_dict()
    promoted["canonical_effect"] = "WRITE"
    with pytest.raises(ValidationError):
        validator.validate(promoted)


def _init_git(root: Path) -> str:
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.email", "iqc-test@example.invalid"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "IQC Test"], cwd=root, check=True)
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "commit", "-qm", "fixture"], cwd=root, check=True)
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()


def test_iqc_source_state_binding_passes_exact_clean_head(tmp_path: Path) -> None:
    root = make_root(tmp_path, coverage_head="placeholder")
    head = _init_git(root)
    report = inspect_repository(
        root,
        target_head=head,
        policy=InspectionPolicy(require_source_state_binding=True),
    )
    source = next(check for check in report.checks if check.check_id == "IQC-SRC-001")
    assert source.status is CheckStatus.PASS


def test_iqc_source_state_binding_holds_non_qa_drift(tmp_path: Path) -> None:
    root = make_root(tmp_path, coverage_head="placeholder")
    head = _init_git(root)
    (root / "components" / "example_0" / "README.md").write_text("drift\n", encoding="utf-8")
    report = inspect_repository(
        root,
        target_head=head,
        policy=InspectionPolicy(require_source_state_binding=True),
    )
    source = next(check for check in report.checks if check.check_id == "IQC-SRC-001")
    assert source.status is CheckStatus.HOLD
