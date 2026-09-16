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
    return next(item for item in record["closed_unmerged"] if item["pr"] == pr)


def test_recalibrated_registry_covers_closed_inventory_and_preserves_two_cores() -> None:
    result = module.validate_registry(registry())
    assert result["status"] == "PASS"
    assert result["closed_prs_covered"] == 115
    assert result["merged_closed_prs"] == 103
    assert result["closed_unmerged_prs"] == 12
    assert result["open_prs_at_recalibration_snapshot"] == 1
    assert result["open_pr_count_is_reentry_guard"] is False
    assert result["full_qms_mapping"] is True
    assert result["direct_historical_merge"] is False
    assert result["historical_code_reuse"] is False
    assert result["new_quality_ontology"] is False
    assert result["subjectivity"] == "NOT_ESTABLISHED"


def test_open_pr_snapshot_is_not_a_closed_reentry_guard() -> None:
    record = registry()
    record["open_pr_count"] = 4
    result = module.validate_registry(record)
    assert result["status"] == "PASS"
    assert result["open_prs_at_recalibration_snapshot"] == 4
    assert result["open_pr_count_is_reentry_guard"] is False


def test_closed_inventory_still_fails_closed() -> None:
    record = registry()
    record["closed_pr_count"] = 116
    with pytest.raises(module.ReentryValidationError, match="closed PR inventory count drift"):
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


def test_human_owner_confirmed_priority_order_is_fail_closed() -> None:
    record = registry()
    record["redesign_priority_plan"][0], record["redesign_priority_plan"][1] = record["redesign_priority_plan"][1], record["redesign_priority_plan"][0]
    with pytest.raises(module.ReentryValidationError, match="priority plan drifted"):
        module.validate_registry(record)


def test_priority_designs_forbid_historical_code_reuse() -> None:
    record = registry()
    record["redesign_priority_plan"][0]["historical_code_reuse"] = True
    with pytest.raises(module.ReentryValidationError, match="historical code reuse"):
        module.validate_registry(record)


def test_pr103_incident_cannot_be_revived_as_merge_candidate() -> None:
    record = registry()
    entry(record, 103)["allowed_action"] = "REOPEN_AND_MERGE"
    with pytest.raises(module.ReentryValidationError, match="prohibited re-entry action"):
        module.validate_registry(record)


def test_pr84_sandbox_remains_superseded_while_method_question_may_be_extracted() -> None:
    record = registry()
    pr84 = entry(record, 84)
    assert pr84["allowed_action"] == "NO_ACTION"
    assert pr84["derivative_method_source_only"] is True
    assert pr84["new_current_main_question"] == "SUBJECTIVITY_INDICATOR_DISCRIMINANT_VALIDITY_MATRIX"

    broken = deepcopy(record)
    entry(broken, 84)["historical_code_reuse"] = True
    with pytest.raises(module.ReentryValidationError, match="sandbox was reintroduced"):
        module.validate_registry(broken)


def test_memory_locus_sources_are_extract_and_reauthor_only() -> None:
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
