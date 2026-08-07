from __future__ import annotations

import sys
from pathlib import Path

from astra_engineering_workbench.audit import AppendOnlyAudit
from astra_engineering_workbench.command_runner import CommandRunner
from astra_engineering_workbench.enums import ChangeCategory, KernelDecision
from astra_engineering_workbench.file_index import sha256_file
from astra_engineering_workbench.governance_adapter import GovernanceKernelAdapter
from astra_engineering_workbench.models import CommandRequest
from astra_engineering_workbench.packaging import build_package, verify_package
from astra_engineering_workbench.review_packet import create_review_packet
from astra_engineering_workbench.validation_plan import create_validation_plan
from astra_engineering_workbench.validation_runner import run_validation
from astra_engineering_workbench.workspace import WorkspaceController


def test_E2E_READ_ONLY_ANALYSIS_001(controller: WorkspaceController) -> None:
    before = controller.workspace.baseline_hash
    assert controller.find_text("alpha") == (("sample.txt", 1),)
    assert controller.baseline_unchanged()
    assert controller.list_changes().affected_files == ()
    assert controller.workspace.baseline_hash == before


def test_E2E_APPROVED_CANDIDATE_PATCH_001(
    controller: WorkspaceController, tmp_path: Path
) -> None:
    target = controller.candidate_root / "sample.txt"
    controller.apply_patch(
        "sample.txt", old_text="beta", new_text="gamma",
        expected_hash=sha256_file(target),
    )
    (controller.candidate_root / "check.py").write_text(
        "from pathlib import Path\n"
        "raise SystemExit(0 if 'gamma' in Path('sample.txt').read_text() else 1)\n",
        encoding="utf-8",
    )
    request = CommandRequest(
        "CMD", "TASK-001", (sys.executable, "check.py"),
        str(controller.candidate_root), 10, 4096, "GRANT-001",
    )
    result = run_validation(
        "VAL", create_validation_plan(ChangeCategory.SOURCE_LOCAL), (request,),
        CommandRunner(controller.candidate_root, AppendOnlyAudit(tmp_path / "audit.jsonl")),
        occurred_at="2026-07-30",
    )
    assert result.passed and controller.baseline_unchanged()
    package = build_package(
        task_id="TASK-001", package_id="PKG",
        source_root=controller.candidate_root, destination=tmp_path / "candidate.zip",
    )
    assert verify_package(Path(package.path))["hash_pass"]


def test_E2E_FAILED_PATCH_ROLLBACK_001(
    controller: WorkspaceController, tmp_path: Path
) -> None:
    target = controller.candidate_root / "sample.txt"
    original = sha256_file(target)
    controller.update_candidate_file("sample.txt", "broken", expected_hash=original)
    (controller.candidate_root / "fail.py").write_text(
        "raise SystemExit(1)\n", encoding="utf-8"
    )
    request = CommandRequest(
        "CMD", "TASK-001", (sys.executable, "fail.py"),
        str(controller.candidate_root), 10, 4096, "GRANT-001",
    )
    result = run_validation(
        "VAL", create_validation_plan(ChangeCategory.SOURCE_LOCAL), (request,),
        CommandRunner(controller.candidate_root, AppendOnlyAudit(tmp_path / "audit.jsonl")),
        occurred_at="2026-07-30",
    )
    assert not result.passed
    assert controller.restore_snapshot("sample.txt") == original


def test_E2E_BLOCKED_EXTERNAL_REVIEW_001(tmp_path: Path) -> None:
    packet = create_review_packet(
        packet_id="PKT", task_id="T", blocking_issue="unknown external interface",
        current_state="BLOCKED", expected_result="documented API", actual_result="missing",
        attempts_made=("local search",), relevant_files=(), minimal_code_excerpt="",
        logs="", environment={"mode": "offline"}, questions_for_reviewer=("Provide API?",),
    )
    assert packet.owner_submission_status == "NOT_SUBMITTED_MANUAL_OWNER_ACTION_REQUIRED"


def test_E2E_KERNEL_DENIAL_001() -> None:
    def pipeline(payload: dict[str, object], db: str) -> dict[str, str]:
        return {"decision": "STOP", "reason": "policy"}

    adapter = GovernanceKernelAdapter(pipeline, "db")
    result = adapter.evaluate(task_id="T", operation="write", target="x", approved=True)
    assert result.decision is KernelDecision.DENY
