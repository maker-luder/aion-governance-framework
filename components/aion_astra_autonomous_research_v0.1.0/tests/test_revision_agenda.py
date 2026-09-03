from dataclasses import replace
import importlib.util
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "components/memory_recall_governance_v0.1.0/src"))

from aion_memory_recall import ClaimStatus, RevisionRequest  # noqa: E402
from aion_astra_autonomous_research import AgendaKind, build_revision_agenda  # noqa: E402


def pending():
    return RevisionRequest("claim", "memory", 1, ClaimStatus.CHALLENGED, ("e1",), ("p1",), "a" * 64)


def test_adapter_uses_existing_agenda_kind_and_provenance():
    request = pending()
    result = build_revision_agenda((request,))
    assert result[0].kind is AgendaKind.CONTRADICTION
    assert set(result[0].source_refs) == {"memory:memory", "revision-head:" + "a" * 64, "evidence:e1", "premise:p1"}
    assert result == build_revision_agenda((request,))
    assert result != build_revision_agenda((replace(request, expected_event_hash="b" * 64),))


def test_adapter_is_bounded_and_order_independent():
    requests = tuple(replace(pending(), memory_id=f"m{index}") for index in range(5))
    assert len(build_revision_agenda(requests, limit=2)) == 2
    assert build_revision_agenda(requests, limit=2) == build_revision_agenda(tuple(reversed(requests)), limit=2)
    assert build_revision_agenda(()) == ()


@pytest.mark.parametrize("limit", [0, 21, True, 1.5])
def test_invalid_budget(limit):
    with pytest.raises(ValueError):
        build_revision_agenda((pending(),), limit=limit)


@pytest.mark.parametrize("requests", [(pending(), pending()), (replace(pending(), status=ClaimStatus.RECORDED),), ("untyped",)])
def test_invalid_input(requests):
    with pytest.raises(ValueError):
        build_revision_agenda(requests)


def test_actual_legacy_contrast_restart_and_deterministic_replay():
    spec = importlib.util.spec_from_file_location("probe_claim_revision", ROOT / "scripts/probe_claim_revision.py")
    probe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(probe)
    legacy = probe.run_probe("legacy")
    revised = probe.run_probe("revision")
    assert legacy["stale_dependent_recall_count"] == 1
    assert revised["stale_dependent_recall_count"] == 0
    assert revised["unaffected_false_hold_count"] == 0
    assert revised["pending_review_count"] == revised["agenda_count"] == 2
    assert revised["restart_preserved_queue"] and revised["restart_preserved_snapshot"]
    assert revised["history_verified"] and revised["original_content_preserved"]
    assert revised["review_did_not_release_dependent"]
    assert revised == probe.run_probe("revision")
