"""Fail-closed admission for reusing closed pull-request material.

This validator is an adapter into the existing Four-Domain / ResearchQualityChain
architecture. It does not create a new evidence ontology and has no merge authority.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = Path("docs/research/closed_pr_reentry_registry_v0.1.0.json")
EXPECTED_UNMERGED = frozenset({8, 12, 19, 25, 26, 33, 37, 38, 41, 80, 84, 103})
ALLOWED_ACTIONS = frozenset({"NO_ACTION", "PRESERVE_ONLY", "EXTRACT_REDESIGN_ONLY"})
FORBIDDEN_ACTIONS = frozenset({"MERGE_HISTORICAL_HEAD", "REOPEN_AND_MERGE", "PROMOTE_HISTORICAL_EVIDENCE"})
CORE_RELATIONS = frozenset({"NONE", "QUALITY_FEED", "SUBJECTIVITY_FEED", "DUAL_CORE_REFERENCE"})
QUALITY_CHECKPOINTS = frozenset(
    {
        "SOURCE_IQC",
        "DESIGN_ADMISSION",
        "PREREGISTRATION",
        "EXECUTION_INTEGRITY",
        "EVIDENCE_REVIEW",
        "COUNTEREVIDENCE_REVIEW",
        "CLAIM_CEILING_REVIEW",
        "FINAL_QA",
    }
)
SUBJECTIVITY_REENTRY_FIELDS = (
    "ontology_neutral_question",
    "theory_or_construct_link",
    "discriminating_prediction",
    "falsifier_or_support_reducing_condition",
    "competing_explanations",
    "mimicry_alternative",
    "internal_variant_alternative",
    "indicator_validation_status",
    "claim_ceiling",
)
SHA40 = re.compile(r"[0-9a-f]{40}")


class ReentryValidationError(ValueError):
    pass


def _nonempty(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ReentryValidationError(f"{label} must be a non-empty string")


def validate_registry(record: dict[str, Any]) -> dict[str, Any]:
    if record.get("schema_version") != "0.1.0" or record.get("record_type") != "CLOSED_PR_DUAL_CORE_REENTRY_REGISTRY":
        raise ReentryValidationError("unknown closed-PR re-entry registry schema")
    if record.get("repository") != "maker-luder/aion-governance-framework":
        raise ReentryValidationError("repository binding mismatch")
    if not SHA40.fullmatch(str(record.get("audited_main", ""))):
        raise ReentryValidationError("audited_main must be an exact commit SHA")

    closed_count = record.get("closed_pr_count")
    merged_count = record.get("merged_closed_pr_count")
    unmerged_count = record.get("closed_unmerged_pr_count")
    if type(closed_count) is not int or type(merged_count) is not int or type(unmerged_count) is not int:
        raise ReentryValidationError("closed PR counts must be exact integers")
    if closed_count != 110 or merged_count != 98 or unmerged_count != 12 or merged_count + unmerged_count != closed_count:
        raise ReentryValidationError("closed PR inventory count drift")

    core = record.get("core_contract")
    if not isinstance(core, dict):
        raise ReentryValidationError("missing dual-core contract")
    required_core = {
        "central_research_question": "AI_SUBJECTIVITY_POSSIBILITY",
        "quality_management_line": "END_TO_END_RESEARCH_QUALITY_AND_GOVERNANCE",
        "subjectivity": "NOT_ESTABLISHED",
        "consciousness": "NOT_ESTABLISHED",
        "phenomenal_experience": "NOT_ESTABLISHED",
        "canonical_effect": "NONE",
        "deployment": False,
    }
    for key, expected in required_core.items():
        if type(core.get(key)) is not type(expected) or core.get(key) != expected:
            raise ReentryValidationError(f"dual-core boundary changed: {key}")

    merged_policy = record.get("merged_closed_policy")
    if not isinstance(merged_policy, dict) or merged_policy.get("disposition") != "CANONICAL_ALREADY_ABSORBED":
        raise ReentryValidationError("merged closed PRs must be treated as current-main ancestry")
    if merged_policy.get("reimport_from_historical_pr") is not False:
        raise ReentryValidationError("merged closed PR bytes must not be re-imported")

    contract = record.get("future_reentry_contract")
    if not isinstance(contract, dict):
        raise ReentryValidationError("missing future re-entry contract")
    if contract.get("historical_head_is_authority") is not False or contract.get("historical_ci_is_current_evidence") is not False:
        raise ReentryValidationError("historical head or CI cannot become current authority")
    if contract.get("direct_reopen_and_merge") is not False:
        raise ReentryValidationError("direct reopen-and-merge must remain prohibited")
    if contract.get("evidence_reuse_requires_current_claim_rebinding") is not True:
        raise ReentryValidationError("evidence reuse must rebind the current exact claim")
    if contract.get("external_material_policy") != "DERIVATIVE_ONLY" or contract.get("raw_external_publication_in_repo_by_default") is not False:
        raise ReentryValidationError("external material must remain derivative-only by default")
    if tuple(contract.get("subjectivity_feed_requirements", ())) != tuple(x.upper() for x in SUBJECTIVITY_REENTRY_FIELDS):
        raise ReentryValidationError("subjectivity re-entry requirements drifted")

    entries = record.get("closed_unmerged")
    if not isinstance(entries, list) or len(entries) != 12:
        raise ReentryValidationError("closed-unmerged registry must contain exactly 12 entries")
    numbers = {entry.get("pr") for entry in entries if isinstance(entry, dict)}
    if numbers != EXPECTED_UNMERGED:
        raise ReentryValidationError("closed-unmerged PR set drifted")

    for entry in entries:
        if not isinstance(entry, dict):
            raise ReentryValidationError("entry must be an object")
        pr = entry.get("pr")
        _nonempty(entry.get("title"), f"PR {pr} title")
        if not SHA40.fullmatch(str(entry.get("historical_head", ""))):
            raise ReentryValidationError(f"PR {pr} lacks exact historical head")
        _nonempty(entry.get("disposition"), f"PR {pr} disposition")
        _nonempty(entry.get("current_main_crosscheck"), f"PR {pr} current-main crosscheck")
        _nonempty(entry.get("reason"), f"PR {pr} reason")
        relation = entry.get("core_relation")
        if relation not in CORE_RELATIONS:
            raise ReentryValidationError(f"PR {pr} has unknown core relation")
        action = entry.get("allowed_action")
        if action in FORBIDDEN_ACTIONS or action not in ALLOWED_ACTIONS:
            raise ReentryValidationError(f"PR {pr} has prohibited re-entry action")
        checkpoints = entry.get("quality_targets")
        if not isinstance(checkpoints, list) or len(checkpoints) != len(set(checkpoints)):
            raise ReentryValidationError(f"PR {pr} quality targets must be a unique list")
        if not set(checkpoints).issubset(QUALITY_CHECKPOINTS):
            raise ReentryValidationError(f"PR {pr} created a parallel quality checkpoint")
        if relation in {"QUALITY_FEED", "DUAL_CORE_REFERENCE"} and not checkpoints:
            raise ReentryValidationError(f"PR {pr} quality feed is not mapped to the existing quality chain")
        if action == "EXTRACT_REDESIGN_ONLY" and relation in {"QUALITY_FEED", "DUAL_CORE_REFERENCE"}:
            if entry.get("control_effectiveness_recheck") is not True:
                raise ReentryValidationError(f"PR {pr} redesign lacks control-effectiveness recheck")
        if action == "EXTRACT_REDESIGN_ONLY" and relation in {"SUBJECTIVITY_FEED", "DUAL_CORE_REFERENCE"}:
            detail = entry.get("subjectivity_reentry")
            if not isinstance(detail, dict):
                raise ReentryValidationError(f"PR {pr} subjectivity redesign lacks admission detail")
            for field in SUBJECTIVITY_REENTRY_FIELDS:
                value = detail.get(field)
                if field == "competing_explanations":
                    if not isinstance(value, list) or len(value) < 2 or len(value) != len(set(value)):
                        raise ReentryValidationError(f"PR {pr} needs distinct competing explanations")
                else:
                    _nonempty(value, f"PR {pr} {field}")

    by_pr = {entry["pr"]: entry for entry in entries}
    if by_pr[103]["disposition"] != "HISTORICAL_RESEARCH_VALIDITY_INCIDENT" or by_pr[103]["allowed_action"] != "PRESERVE_ONLY":
        raise ReentryValidationError("PR #103 incident containment weakened")
    if by_pr[84]["disposition"] != "SUPERSEDED_BY_MERGED_PR_85" or by_pr[84]["allowed_action"] != "NO_ACTION":
        raise ReentryValidationError("PR #84 supersession boundary weakened")
    for control_pr in (25, 26):
        if by_pr[control_pr]["disposition"] != "HISTORICAL_GOVERNANCE_TEST_CONTROL":
            raise ReentryValidationError("disposable authority control promoted as feature")
    if by_pr[33]["disposition"] != "OBSOLETE_BRANCH_TOPOLOGY_REMEDIATION":
        raise ReentryValidationError("historical branch topology remediation was revived")

    return {
        "status": "PASS",
        "audited_main": record["audited_main"],
        "closed_prs_covered": closed_count,
        "merged_closed_prs": merged_count,
        "closed_unmerged_prs": unmerged_count,
        "direct_historical_merge": False,
        "new_quality_ontology": False,
        "subjectivity": "NOT_ESTABLISHED",
        "canonical_effect": "NONE",
        "deployment": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("registry", nargs="?", type=Path, default=DEFAULT_REGISTRY)
    args = parser.parse_args(argv)
    try:
        path = args.registry if args.registry.is_absolute() else ROOT / args.registry
        record = json.loads(path.read_text(encoding="utf-8"))
        print(json.dumps(validate_registry(record), indent=2, sort_keys=True))
        return 0
    except (OSError, json.JSONDecodeError, ReentryValidationError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "HOLD", "error_type": type(exc).__name__, "message": str(exc)}, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
