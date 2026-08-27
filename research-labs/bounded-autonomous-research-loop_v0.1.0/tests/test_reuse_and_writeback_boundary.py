from __future__ import annotations

import inspect
from pathlib import Path

import aion_bounded_research_loop.adapters as adapters
from aion_bounded_research_loop import BOUNDARY


def test_adapters_import_existing_capabilities_instead_of_reimplementing_them() -> None:
    source = inspect.getsource(adapters)
    assert "from aion_astra_inquiry.core import" in source
    assert "from aion_endogenous_goal_dynamics import" in source
    assert "BoundedInquiryLoop" in source
    assert "run_matched_experiment" in source
    assert "assess_causal_pattern" in source
    assert "FourDomainMapping" in source
    assert "endogenous_goal_dynamics_mapping" in source
    assert "class FourDomainMapping" not in source
    assert "class BoundedInquiryLoop" not in source


def test_runtime_source_has_no_repository_write_or_merge_surface() -> None:
    package_root = Path(__file__).resolve().parents[1] / "src" / "aion_bounded_research_loop"
    text = "\n".join(path.read_text(encoding="utf-8") for path in sorted(package_root.glob("*.py")))
    forbidden = (
        "merge_pull_request",
        "enable_auto_merge",
        "update_ref",
        "create_file(",
        "update_file(",
        "delete_file(",
        "subprocess",
        "os.system",
        "git push",
        "git commit",
        ".write_text(",
        ".write_bytes(",
    )
    for token in forbidden:
        assert token not in text


def test_boundary_contract_contains_every_required_lock() -> None:
    contract = set(BOUNDARY.as_contract())
    assert {
        "FULL_AUTOMATION != FULL_AUTHORITY",
        "NORMATIVE_STATE != AUTHORITY",
        "RUN_INTEGRITY_PASS != SCIENTIFIC_TRUTH",
        "ENGINEERING_ANALOGUE != HUMAN_PSYCHOLOGY",
        "SUBJECTIVITY = NOT_ESTABLISHED",
        "CONSCIOUSNESS = NOT_ESTABLISHED",
        "CANONICAL_EFFECT = NONE",
        "DEPLOYMENT = FALSE",
        "AUTONOMOUS_MERGE = NO",
        "AUTONOMOUS_REPOSITORY_WRITEBACK = NO",
    } <= contract
