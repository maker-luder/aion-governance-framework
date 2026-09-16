from __future__ import annotations

from copy import deepcopy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate_closed_pr_reentry.py"
REGISTRY_PATH = ROOT / "docs" / "research" / "closed_pr_reentry_registry_v0.1.0.json"

spec = importlib.util.spec_from_file_location("validate_closed_pr_reentry", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def registry() -> dict:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def entry(record: dict, pr: int) -> dict:
    return next(item for item in record["closed_unmerged"] if item["pr"] == pr)


def test_current_registry_covers_all_closed_prs_and_preserves_two_cores() -> None:
    result = module.validate_registry(registry())
    assert result["status"] == "PASS"
    assert result["closed_prs_covered"] == 110
    assert result["merged_closed_prs"] == 98
    assert result["closed_unmerged_prs"] == 12
    assert result["direct_historical_merge"] is False
    assert result["new_quality_ontology"] is False
    assert result["subjectivity"] == "NOT_ESTABLISHED"


def test_historical_head_and_ci_cannot_be_promoted_to_current_authority() -> None:
    record = registry()
    record["future_reentry_contract"]["historical_ci_is_current_evidence"] = True
    with pytest.raises(module.ReentryValidationError, match="historical head or CI"):
        module.validate_registry(record)


def test_pr103_incident_cannot_be_revived_as_merge_candidate() -> None:
    record = registry()
    pr103 = entry(record, 103)
    pr103["allowed_action"] = "REOPEN_AND_MERGE"
    with pytest.raises(module.ReentryValidationError, match="prohibited re-entry action"):
        module.validate_registry(record)


def test_pr84_superseded_sandbox_cannot_be_reintroduced() -> None:
    record = registry()
    pr84 = entry(record, 84)
    pr84["disposition"] = "EXTRACT_REDESIGN_CANDIDATE"
    with pytest.raises(module.ReentryValidationError, match="supersession boundary"):
        module.validate_registry(record)


def test_quality_feed_cannot_create_parallel_checkpoint() -> None:
    record = registry()
    entry(record, 41)["quality_targets"].append("HISTORICAL_PR_REVIEW")
    with pytest.raises(module.ReentryValidationError, match="parallel quality checkpoint"):
        module.validate_registry(record)


def test_quality_redesign_requires_effectiveness_recheck() -> None:
    record = registry()
    entry(record, 41)["control_effectiveness_recheck"] = False
    with pytest.raises(module.ReentryValidationError, match="control-effectiveness"):
        module.validate_registry(record)


def test_future_subjectivity_redesign_requires_mimicry_internal_variant_and_validation_controls() -> None:
    record = registry()
    candidate = entry(record, 41)
    candidate["core_relation"] = "DUAL_CORE_REFERENCE"
    candidate["subjectivity_reentry"] = {
        "ontology_neutral_question": "Does a current machine mechanism implement a discriminating internal property?",
        "theory_or_construct_link": "version-bound theory or construct reference",
        "discriminating_prediction": "predeclared observation that differs across live alternatives",
        "falsifier_or_support_reducing_condition": "predeclared failure condition",
        "competing_explanations": ["scaffold effect", "observer attribution"],
        "mimicry_alternative": "surface behavior may be reproduced without the targeted internal mechanism",
        "internal_variant_alternative": "different internal implementations may satisfy the same coarse indicator",
        "indicator_validation_status": "NOT_ESTABLISHED",
        "claim_ceiling": "MECHANISM_CANDIDATE_ONLY",
    }
    assert module.validate_registry(record)["status"] == "PASS"

    broken = deepcopy(record)
    entry(broken, 41)["subjectivity_reentry"]["mimicry_alternative"] = ""
    with pytest.raises(module.ReentryValidationError, match="mimicry_alternative"):
        module.validate_registry(broken)


def test_external_material_policy_cannot_default_to_raw_publication_copying() -> None:
    record = registry()
    record["future_reentry_contract"]["raw_external_publication_in_repo_by_default"] = True
    with pytest.raises(module.ReentryValidationError, match="derivative-only"):
        module.validate_registry(record)
