from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from aion_evidence_interop.canonical import InteropError
from aion_evidence_interop.scorecard_export import (
    STATUS_VOCABULARY,
    export_scorecard_crosswalk,
)


COMPONENT = Path(__file__).resolve().parents[1]
ROOT = COMPONENT.parents[1]


def _head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()


def _by_name(report: dict[str, object]) -> dict[str, dict[str, object]]:
    return {item["check"]: item for item in report["checks"]}  # type: ignore[index,misc]


def _write(root: Path, relative: str, text: str = "") -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def test_scorecard_crosswalk_is_explicitly_non_authoritative() -> None:
    report = export_scorecard_crosswalk(ROOT, _head())
    assert report["profile"] == "OPENSSF_SCORECARD_CROSSWALK_ONLY"
    assert report["openssf_scorecard_executed"] is False
    assert report["score"] is None
    assert report["status_vocabulary"] == list(STATUS_VOCABULARY)
    assert report["boundaries"]["security_certification"] == "NOT_ESTABLISHED"  # type: ignore[index]
    assert report["boundaries"]["canonical_effect"] == "NONE"  # type: ignore[index]


def test_exact_tree_integration_separates_local_and_external_checks() -> None:
    checks = _by_name(export_scorecard_crosswalk(ROOT, _head()))
    assert checks["Security-Policy"]["status"] == "LOCAL_EVIDENCE_PRESENT"
    assert checks["CI-Tests"]["status"] == "LOCAL_EVIDENCE_PRESENT"
    assert checks["SAST"]["status"] == "LOCAL_EVIDENCE_PRESENT"
    assert checks["Branch-Protection"]["status"] == "EXTERNAL_VERIFICATION_REQUIRED"
    assert checks["Code-Review"]["status"] == "EXTERNAL_VERIFICATION_REQUIRED"


@pytest.mark.parametrize("suffix", ["yml", "yaml"])
def test_all_full_sha_external_actions_are_local_evidence_present(
    tmp_path: Path, suffix: str
) -> None:
    sha = "a" * 40
    _write(
        tmp_path,
        f".github/workflows/z.{suffix}",
        f"steps:\n  - uses: owner/action@{sha} # pinned rationale\n  - uses: ./local-action\n",
    )
    _write(tmp_path, ".github/workflows/a.yml", f"steps:\n  - uses: other/action@{sha}\n")
    report = export_scorecard_crosswalk(tmp_path, "b" * 40)
    pinning = report["pinning_summary"]
    assert pinning["workflow_count"] == 2  # type: ignore[index]
    assert pinning["external_action_uses"] == 2  # type: ignore[index]
    assert pinning["sha_pinned_external_action_uses"] == 2  # type: ignore[index]
    assert pinning["mutable_external_action_uses"] == []  # type: ignore[index]
    assert _by_name(report)["Pinned-Dependencies"]["status"] == "LOCAL_EVIDENCE_PRESENT"


@pytest.mark.parametrize("ref", ["main", "v4", "v4.1.0", ""])
def test_mutable_or_missing_external_action_ref_is_missing(tmp_path: Path, ref: str) -> None:
    target = "owner/action" + (f"@{ref}" if ref else "")
    _write(tmp_path, ".github/workflows/quality.yml", f"steps:\n  - uses: {target}\n")
    report = export_scorecard_crosswalk(tmp_path, "b" * 40)
    assert _by_name(report)["Pinned-Dependencies"]["status"] == "LOCAL_EVIDENCE_MISSING"
    mutable = report["pinning_summary"]["mutable_external_action_uses"]  # type: ignore[index]
    assert [item["uses"] for item in mutable] == [target]


def test_pinning_traversal_is_deterministic_and_local_actions_are_excluded(
    tmp_path: Path,
) -> None:
    sha = "c" * 40
    _write(tmp_path, ".github/workflows/z.yaml", f"- uses: z/action@{sha}\n")
    _write(tmp_path, ".github/workflows/a.yml", f"- uses: a/action@{sha}\n- uses: ./local\n")
    first = export_scorecard_crosswalk(tmp_path, "d" * 40)
    second = export_scorecard_crosswalk(tmp_path, "d" * 40)
    assert first == second
    assert first["pinning_summary"]["external_action_uses"] == 2  # type: ignore[index]


def test_isolated_missing_local_files_and_hosted_checks(tmp_path: Path) -> None:
    checks = _by_name(export_scorecard_crosswalk(tmp_path, "e" * 40))
    assert checks["Security-Policy"]["status"] == "LOCAL_EVIDENCE_MISSING"
    assert checks["CI-Tests"]["status"] == "LOCAL_EVIDENCE_MISSING"
    assert checks["SAST"]["status"] == "LOCAL_EVIDENCE_MISSING"
    for name in (
        "Token-Permissions",
        "Branch-Protection",
        "Code-Review",
        "Dangerous-Workflow",
        "Vulnerabilities",
    ):
        assert checks[name]["status"] == "EXTERNAL_VERIFICATION_REQUIRED"


def test_frozen_project_markers_preserve_intentional_states(tmp_path: Path) -> None:
    _write(
        tmp_path,
        "README.md",
        "PROJECT_WORK_LOOP = TERMINATED\nACTIVE_ENGINEERING = NO\nNEW_UPSTREAM_TRACKING = NO\n",
    )
    checks = _by_name(export_scorecard_crosswalk(tmp_path, "f" * 40))
    assert checks["Dependency-Update-Tool"]["status"] == "INTENTIONALLY_DISABLED"
    assert checks["Maintained"]["status"] == "OUT_OF_SCOPE_FROZEN"


def test_partial_frozen_markers_do_not_create_frozen_status(tmp_path: Path) -> None:
    _write(tmp_path, "README.md", "PROJECT_WORK_LOOP = TERMINATED\nNEW_UPSTREAM_TRACKING = NO\n")
    checks = _by_name(export_scorecard_crosswalk(tmp_path, "f" * 40))
    assert checks["Dependency-Update-Tool"]["status"] == "LOCAL_EVIDENCE_MISSING"
    assert checks["Maintained"]["status"] == "EXTERNAL_VERIFICATION_REQUIRED"


def test_dependabot_present_overrides_frozen_absence_state(tmp_path: Path) -> None:
    _write(tmp_path, ".github/dependabot.yaml", "version: 2\nupdates: []\n")
    checks = _by_name(export_scorecard_crosswalk(tmp_path, "0" * 40))
    assert checks["Dependency-Update-Tool"]["status"] == "LOCAL_EVIDENCE_PRESENT"
    assert checks["Dependency-Update-Tool"]["evidence_refs"] == [".github/dependabot.yaml"]


def test_quality_and_codeql_yaml_extensions_are_detected(tmp_path: Path) -> None:
    _write(tmp_path, ".github/workflows/quality.yaml", "name: Quality\n")
    _write(tmp_path, ".github/workflows/codeql.yaml", "name: CodeQL\n")
    checks = _by_name(export_scorecard_crosswalk(tmp_path, "1" * 40))
    assert checks["CI-Tests"]["status"] == "LOCAL_EVIDENCE_PRESENT"
    assert checks["SAST"]["status"] == "LOCAL_EVIDENCE_PRESENT"


def test_workflow_symlink_escape_fails_closed(tmp_path: Path) -> None:
    external = tmp_path.parent / "external-workflow.yml"
    external.write_text("steps:\n  - uses: owner/action@main\n")
    workflows = tmp_path / ".github/workflows"
    workflows.mkdir(parents=True)
    (workflows / "escape.yml").symlink_to(external)
    try:
        with pytest.raises(InteropError) as caught:
            export_scorecard_crosswalk(tmp_path, "2" * 40)
        assert caught.value.category == "path_confinement_failure"
    finally:
        external.unlink(missing_ok=True)
