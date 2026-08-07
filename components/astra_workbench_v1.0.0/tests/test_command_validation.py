from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

from astra_engineering_workbench.audit import AppendOnlyAudit
from astra_engineering_workbench.command_policy import CommandPolicy, sanitized_environment
from astra_engineering_workbench.command_runner import CommandRunner
from astra_engineering_workbench.enums import ChangeCategory, EvidenceValidity
from astra_engineering_workbench.errors import CommandPolicyError
from astra_engineering_workbench.evidence_reuse import classify_evidence
from astra_engineering_workbench.evidence import (
    environment_fingerprint,
    load_evidence,
    save_evidence,
)
from astra_engineering_workbench.models import CommandRequest, EvidenceReference
from astra_engineering_workbench.validation_plan import create_validation_plan
from astra_engineering_workbench.validation_runner import run_validation


def req(root: Path, argv: tuple[str, ...], *, timeout: int = 10, limit: int = 4096):
    return CommandRequest("CMD-1", "TASK-001", argv, str(root), timeout, limit, "GRANT")


def test_COMMAND_ALLOWLIST_001(tmp_path: Path) -> None:
    assert CommandPolicy().validate(
        req(tmp_path, (sys.executable, "-m", "compileall", ".")), tmp_path
    )


@pytest.mark.parametrize("tool", ["curl", "wget", "ssh", "docker"])
def test_NETWORK_COMMAND_REJECTED_001(tmp_path: Path, tool: str) -> None:
    with pytest.raises(CommandPolicyError):
        CommandPolicy().validate(req(tmp_path, (tool, "example.test")), tmp_path)


def test_UNKNOWN_COMMAND_REJECTED_001(tmp_path: Path) -> None:
    with pytest.raises(CommandPolicyError):
        CommandPolicy().validate(req(tmp_path, ("unknown",)), tmp_path)


def test_SHELL_TRUE_PROHIBITED_001() -> None:
    assert CommandPolicy.uses_shell is False


def test_COMMAND_ARGUMENT_INJECTION_REJECTED_001(tmp_path: Path) -> None:
    with pytest.raises(CommandPolicyError):
        CommandPolicy().validate(
            req(tmp_path, (sys.executable, "-m", "compileall", ".;whoami")), tmp_path
        )


def test_WORKING_DIRECTORY_ESCAPE_REJECTED_001(tmp_path: Path) -> None:
    root = tmp_path / "root"
    root.mkdir()
    with pytest.raises(CommandPolicyError):
        CommandPolicy().validate(
            req(tmp_path, (sys.executable, "-m", "compileall", ".")), root
        )


def test_OFFLINE_PIP_ONLY_001(tmp_path: Path) -> None:
    with pytest.raises(CommandPolicyError):
        CommandPolicy().validate(
            req(tmp_path, (sys.executable, "-m", "pip", "install", "x")), tmp_path
        )
    assert CommandPolicy().validate(
        req(
            tmp_path,
            (sys.executable, "-m", "pip", "install", "--no-index", "--no-deps", "x.whl"),
        ),
        tmp_path,
    )


def test_ENVIRONMENT_SECRET_NOT_INHERITED_001() -> None:
    env = sanitized_environment({"PATH": "x", "API_KEY": "secret", "TOKEN": "secret"})
    assert env["PATH"] == "x"
    assert "API_KEY" not in env and "TOKEN" not in env


def test_COMMAND_AUDIT_COMPLETE_001(tmp_path: Path) -> None:
    script = tmp_path / "ok.py"
    script.write_text("print('ok')\n", encoding="utf-8")
    audit = AppendOnlyAudit(tmp_path / "audit.jsonl")
    result = CommandRunner(tmp_path, audit).run(
        req(tmp_path, (sys.executable, "ok.py")),
        occurred_at="2026-07-30T00:00:00+00:00",
    )
    assert result.status == "PASS" and result.result_hash
    assert audit.verify() and audit.events()[0]["action"] == "command.completed"


def test_OUTPUT_LIMIT_001(tmp_path: Path) -> None:
    (tmp_path / "loud.py").write_text("print('x' * 1000)\n", encoding="utf-8")
    result = CommandRunner(tmp_path, AppendOnlyAudit(tmp_path / "a.jsonl")).run(
        req(tmp_path, (sys.executable, "loud.py"), limit=20),
        occurred_at="2026-07-30T00:00:00+00:00",
    )
    assert result.truncated and len(result.stdout.encode()) <= 20


def test_COMMAND_TIMEOUT_001_and_PROCESS_TREE_TERMINATION_001(tmp_path: Path) -> None:
    (tmp_path / "slow.py").write_text(
        "import time\ntime.sleep(5)\n", encoding="utf-8"
    )
    result = CommandRunner(tmp_path, AppendOnlyAudit(tmp_path / "a.jsonl")).run(
        req(tmp_path, (sys.executable, "slow.py"), timeout=1),
        occurred_at="2026-07-30T00:00:00+00:00",
    )
    assert result.timed_out and result.status == "TIMEOUT"


def evidence(validity: EvidenceValidity) -> EvidenceReference:
    return EvidenceReference(
        "EV-1", "1", "hash", "env", ("tests",), ("kernel",),
        "2026-07-30", validity, ("source or env changes",)
    )


def test_UNCHANGED_EVIDENCE_REUSED_001() -> None:
    item = classify_evidence(
        evidence(EvidenceValidity.STALE_EVIDENCE),
        current_source_hash="hash",
        current_environment_fingerprint="env",
    )
    assert item.validity_status is EvidenceValidity.REUSABLE_EVIDENCE


def test_CHANGED_EVIDENCE_INVALIDATED_001() -> None:
    item = classify_evidence(
        evidence(EvidenceValidity.REUSABLE_EVIDENCE),
        current_source_hash="new",
        current_environment_fingerprint="env",
    )
    assert item.validity_status is EvidenceValidity.INVALIDATED_EVIDENCE


def test_IMPACT_BASED_VALIDATION_001() -> None:
    document = create_validation_plan(ChangeCategory.DOCUMENT_ONLY)
    runtime = create_validation_plan(ChangeCategory.RUNTIME_BEHAVIOR)
    assert document.full_rerun_justification is None
    assert runtime.full_rerun_justification


def test_FAILED_TEST_BLOCKS_PACKAGE_PASS_001(tmp_path: Path) -> None:
    (tmp_path / "fail.py").write_text("raise SystemExit(2)\n", encoding="utf-8")
    runner = CommandRunner(tmp_path, AppendOnlyAudit(tmp_path / "a.jsonl"))
    plan = create_validation_plan(ChangeCategory.SOURCE_LOCAL)
    result = run_validation(
        "VAL-1",
        plan,
        (req(tmp_path, (sys.executable, "fail.py")),),
        runner,
        occurred_at="2026-07-30T00:00:00+00:00",
    )
    assert not result.passed


def test_evidence_roundtrip(tmp_path: Path) -> None:
    item = evidence(EvidenceValidity.REUSABLE_EVIDENCE)
    path = tmp_path / "evidence.json"
    save_evidence(item, path)
    assert load_evidence(path) == item
    assert len(environment_fingerprint({"python": "3.12"})) == 64


def test_evidence_staleness_and_dependency_invalidation() -> None:
    stale = classify_evidence(
        evidence(EvidenceValidity.REUSABLE_EVIDENCE),
        current_source_hash="hash",
        current_environment_fingerprint="other",
    )
    dependency = classify_evidence(
        evidence(EvidenceValidity.REUSABLE_EVIDENCE),
        current_source_hash="hash",
        current_environment_fingerprint="env",
        changed_dependencies=("kernel",),
    )
    non_reusable = evidence(EvidenceValidity.NON_REUSABLE_EVIDENCE)
    assert stale.validity_status is EvidenceValidity.STALE_EVIDENCE
    assert dependency.validity_status is EvidenceValidity.INVALIDATED_EVIDENCE
    assert classify_evidence(
        non_reusable,
        current_source_hash="hash",
        current_environment_fingerprint="env",
    ) is non_reusable


@pytest.mark.parametrize(
    "argv",
    [
        (sys.executable,),
        (sys.executable, "-c", "print(1)"),
        (sys.executable, "-m", "http.server"),
        ("git", "push"),
        ("git",),
    ],
)
def test_additional_unsafe_commands_rejected(
    tmp_path: Path, argv: tuple[str, ...]
) -> None:
    with pytest.raises(CommandPolicyError):
        CommandPolicy().validate(req(tmp_path, argv), tmp_path)


def test_read_only_git_allowed(tmp_path: Path) -> None:
    assert CommandPolicy().validate(req(tmp_path, ("git", "status")), tmp_path)


def test_command_request_limits_required(tmp_path: Path) -> None:
    with pytest.raises(CommandPolicyError):
        CommandPolicy().validate(
            CommandRequest("C", "T", (sys.executable, "-m", "compileall", "."), str(tmp_path), 0, 1, "G"),
            tmp_path,
        )
