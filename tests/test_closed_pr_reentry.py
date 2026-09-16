from __future__ import annotations

from copy import deepcopy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate_closed_pr_reentry.py"
REGISTRY_PATH = ROOT / "docs" / "research" / "closed_pr_reentry_registry_v0.2.0.json"

spec = importlib.util.spec_from_file_location("validate_closed_pr_reentry", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def registry() -> dict:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def entry(record: dict, pr: int) -> dict:
    return next(item for item in record["historical_reentry_cohort"] if item["pr"] == pr)


def test_registry_preserves_frozen_historical_cohort_and_two_cores() -> None:
    result = module.validate_registry(registry())
    assert result["status"] == "PASS"
    assert result["historical_cohort_size"] == 12
    assert result["future_global_pr_counts_are_reentry_guard"] is False
    assert result["retained_draft_pr"] == 122
    assert result["superseded_duplicate_drafts"] == [123, 124]
    assert result["full_qms_mapping"] is True
    assert result["direct_historical_merge"] is False
    assert result["historical_code_reuse"] is False
    assert result["new_quality_ontology"] is False
    assert result["subjectivity"] == "NOT_ESTABLISHED"


def test_audit_snapshot_is_provenance_not_future_global_guard() -> None:
    record = registry()
    assert record["audit_snapshot"]["scope"] == "HISTORICAL_CLOSED_UNMERGED_COHORT_AT_AUDIT"
    assert record["audit_snapshot"]["global_future_pr_counts_are_reentry_guard"] is False

    broken = deepcopy(record)
    broken["audit_snapshot"]["global_future_pr_counts_are_reentry_guard"] = True
    with pytest.raises(module.ReentryValidationError, match="future global PR counts"):
        module.validate_registry(broken)


def test_historical_snapshot_itself_is_immutable_provenance() -> None:
    record = registry()
    record["audit_snapshot"]["closed_pr_count"] = 117
    with pytest.raises(module.ReentryValidationError, match="historical audit snapshot changed"):
        module.validate_registry(record)


def test_registry_is_bound_to_current_main_and_full_qms() -> None:
    record = registry()
    record["audited_main"] = "0" * 40
    with pytest.raises(module.ReentryValidationError, match="current-main baseline"):
        module.validate_registry(record)

    record = registry()
    record["current_quality_envelope"]["parallel_qms_allowed"] = True
    with pytest.raises(module.ReentryValidationError, match="parallel QMS"):
        module.validate_registry(record)


def test_historical_head_ci_and_direct_merge_cannot_be_promoted() -> None:
    record = registry()
    record["future_reentry_contract"]["historical_ci_is_current_evidence"] = True
    with pytest.raises(module.ReentryValidationError, match="historical head or CI"):
        module.validate_registry(record)

    record = registry()
    record["future_reentry_contract"]["direct_reopen_and_merge"] = True
    with pytest.raises(module.ReentryValidationError, match="reopen-and-merge"):
        module.validate_registry(record)


def test_consolidation_keeps_one_research_draft_and_two_superseded_drafts() -> None:
    record = registry()
    plan = record["consolidation_plan"]
    assert plan["retained_draft_pr"] == 122
    assert plan["superseded_draft_prs"] == [123, 124]
    assert plan["current_main_method_anchor"] == "PR118_INTERPRETIVE_SPECIFICITY_AND_EVIDENCE_ADMISSION"
    assert plan["historical_code_reuse"] is False

    broken = deepcopy(record)
    broken["consolidation_plan"]["superseded_draft_prs"] = [124]
    with pytest.raises(module.ReentryValidationError, match="duplicate Draft disposition"):
        module.validate_registry(broken)


def test_pr103_incident_cannot_be_revived_as_merge_candidate() -> None:
    record = registry()
    entry(record, 103)["allowed_action"] = "REOPEN_AND_MERGE"
    with pytest.raises(module.ReentryValidationError, match="prohibited re-entry action"):
        module.validate_registry(record)


def test_pr84_sandbox_remains_superseded_and_method_is_localized() -> None:
    record = registry()
    pr84 = entry(record, 84)
    assert pr84["allowed_action"] == "NO_ACTION"
    assert pr84["derivative_method_source_only"] is True
    assert pr84["current_use"] == "LOCAL_DISCRIMINANT_VALIDITY_CHECKLIST_IN_REFINED_PR122"

    broken = deepcopy(record)
    entry(broken, 84)["current_use"] = "REVIVE_GENERIC_MATRIX"
    with pytest.raises(module.ReentryValidationError, match="not properly deduplicated"):
        module.validate_registry(broken)


def test_memory_continuity_sources_are_extract_and_reauthor_only() -> None:
    record = registry()
    for pr in (38, 41, 8):
        candidate = entry(record, pr)
        assert candidate["allowed_action"] == "EXTRACT_REDESIGN_ONLY"
        assert candidate["historical_code_reuse"] is False
        assert candidate["current_main_reauthoring_required"] is True
        assert candidate["subjectivity_reentry"]["indicator_validation_status"] == "NOT_ESTABLISHED"


def test_quality_feed_cannot_create_parallel_checkpoint_or_skip_full_qms() -> None:
    record = registry()
    entry(record, 41)["quality_targets"].append("HISTORICAL_PR_REVIEW")
    with pytest.raises(module.ReentryValidationError, match="parallel quality checkpoint"):
        module.validate_registry(record)

    record = registry()
    record["future_reentry_contract"]["quality_feed_requirements"].remove("MAP_TO_EXISTING_FULL_QMS_ENVELOPE")
    with pytest.raises(module.ReentryValidationError, match="quality re-entry requirements"):
        module.validate_registry(record)


def test_subjectivity_redesign_requires_mimicry_internal_variant_and_validation_controls() -> None:
    record = registry()
    broken = deepcopy(record)
    entry(broken, 38)["subjectivity_reentry"]["mimicry_alternative"] = ""
    with pytest.raises(module.ReentryValidationError, match="mimicry_alternative"):
        module.validate_registry(broken)

    broken = deepcopy(record)
    entry(broken, 8)["subjectivity_reentry"]["competing_explanations"] = ["only one"]
    with pytest.raises(module.ReentryValidationError, match="competing explanations"):
        module.validate_registry(broken)


def test_historical_controls_are_not_researchized() -> None:
    record = registry()
    entry(record, 25)["researchization"] = True
    with pytest.raises(module.ReentryValidationError, match="researchized"):
        module.validate_registry(record)


def test_external_material_policy_cannot_default_to_raw_publication_copying() -> None:
    record = registry()
    record["future_reentry_contract"]["raw_external_publication_in_repo_by_default"] = True
    with pytest.raises(module.ReentryValidationError, match="derivative-only"):
        module.validate_registry(record)
