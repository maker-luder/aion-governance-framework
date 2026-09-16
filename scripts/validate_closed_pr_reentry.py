"""Fail-closed admission for reusing the frozen historical closed-PR cohort.

The gate is intentionally scoped to the 2026-09-16 historical re-entry cohort.
Future PR creation/closure must not mutate this cohort or force a global-count refresh.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = Path("docs/research/closed_pr_reentry_registry_v0.2.0.json")
EXPECTED_MAIN = "fd54fd8cb920328282b78f24e31c01c1010f6189"
EXPECTED_TREE = "e7e0c61cce02e1d79b2b78b7fbd175631fb5e08c"
EXPECTED_AUDIT_SNAPSHOT = (115, 103, 12, 1)
EXPECTED_COHORT = frozenset({8, 12, 19, 25, 26, 33, 37, 38, 41, 80, 84, 103})
ALLOWED_ACTIONS = frozenset({"NO_ACTION", "PRESERVE_ONLY", "EXTRACT_REDESIGN_ONLY"})
FORBIDDEN_ACTIONS = frozenset({"MERGE_HISTORICAL_HEAD", "REOPEN_AND_MERGE", "PROMOTE_HISTORICAL_EVIDENCE"})
CORE_RELATIONS = frozenset({"NONE", "QUALITY_FEED", "SUBJECTIVITY_FEED", "DUAL_CORE_REFERENCE"})
QUALITY_CHECKPOINTS = frozenset({
    "SOURCE_IQC", "DESIGN_ADMISSION", "PREREGISTRATION", "EXECUTION_INTEGRITY",
    "EVIDENCE_REVIEW", "COUNTEREVIDENCE_REVIEW", "CLAIM_CEILING_REVIEW", "FINAL_QA",
})
SUBJECTIVITY_REENTRY_FIELDS = (
    "ontology_neutral_question", "theory_or_construct_link", "discriminating_prediction",
    "falsifier_or_support_reducing_condition", "competing_explanations", "mimicry_alternative",
    "internal_variant_alternative", "indicator_validation_status", "claim_ceiling",
)
QUALITY_FEED_REQUIREMENTS = (
    "MAP_TO_EXISTING_RESEARCH_QUALITY_CHAIN",
    "MAP_TO_EXISTING_FULL_QMS_ENVELOPE",
    "CURRENT_MAIN_DEDUP_CHECK",
    "CONTROL_EFFECTIVENESS_RECHECK",
    "FAIL_CLOSED_ON_STALE_OR_AMBIGUOUS_PROVENANCE",
)
SHA40 = re.compile(r"[0-9a-f]{40}")


class ReentryValidationError(ValueError):
    pass


def _nonempty(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ReentryValidationError(f"{label} must be a non-empty string")


def validate_registry(record: dict[str, Any]) -> dict[str, Any]:
    if record.get("schema_version") != "0.2.0" or record.get("record_type") != "CLOSED_PR_DUAL_CORE_REENTRY_REGISTRY":
        raise ReentryValidationError("unknown closed-PR re-entry registry schema")
    if record.get("repository") != "maker-luder/aion-governance-framework":
        raise ReentryValidationError("repository binding mismatch")
    if record.get("audited_main") != EXPECTED_MAIN or record.get("audited_tree") != EXPECTED_TREE:
        raise ReentryValidationError("registry is not bound to the recalibrated current-main baseline")

    snapshot = record.get("audit_snapshot")
    if not isinstance(snapshot, dict):
        raise ReentryValidationError("missing immutable audit snapshot")
    observed_snapshot = (
        snapshot.get("closed_pr_count"), snapshot.get("merged_closed_pr_count"),
        snapshot.get("closed_unmerged_pr_count"), snapshot.get("open_pr_count"),
    )
    if any(type(value) is not int for value in observed_snapshot):
        raise ReentryValidationError("audit snapshot values must be exact integers")
    if observed_snapshot != EXPECTED_AUDIT_SNAPSHOT:
        raise ReentryValidationError("historical audit snapshot changed")
    if snapshot.get("scope") != "HISTORICAL_CLOSED_UNMERGED_COHORT_AT_AUDIT":
        raise ReentryValidationError("historical cohort scope changed")
    if snapshot.get("global_future_pr_counts_are_reentry_guard") is not False:
        raise ReentryValidationError("future global PR counts must not become re-entry guards")

    core = record.get("core_contract")
    required_core = {
        "central_research_question": "AI_SUBJECTIVITY_POSSIBILITY",
        "quality_management_line": "END_TO_END_RESEARCH_QUALITY_AND_GOVERNANCE",
        "subjectivity": "NOT_ESTABLISHED",
        "consciousness": "NOT_ESTABLISHED",
        "phenomenal_experience": "NOT_ESTABLISHED",
        "canonical_effect": "NONE",
        "deployment": False,
    }
    if not isinstance(core, dict):
        raise ReentryValidationError("missing dual-core contract")
    for key, expected in required_core.items():
        if type(core.get(key)) is not type(expected) or core.get(key) != expected:
            raise ReentryValidationError(f"dual-core boundary changed: {key}")

    qms = record.get("current_quality_envelope")
    if not isinstance(qms, dict):
        raise ReentryValidationError("missing current quality envelope")
    if qms.get("research_quality_chain") != "EXISTING_EIGHT_CHECKPOINT_CHAIN" or qms.get("full_qms") != "EXISTING_FULL_QUALITY_SYSTEM_ENGINE":
        raise ReentryValidationError("historical re-entry is not mapped to current canonical quality controls")
    if qms.get("parallel_qms_allowed") is not False:
        raise ReentryValidationError("parallel QMS is prohibited")
    if qms.get("quality_system_pass_is_scientific_validation") is not False or qms.get("measurement_system_qualified_is_target_construct_established") is not False:
        raise ReentryValidationError("quality controls were promoted into scientific validation")

    contract = record.get("future_reentry_contract")
    if not isinstance(contract, dict):
        raise ReentryValidationError("missing future re-entry contract")
    if contract.get("historical_head_is_authority") is not False or contract.get("historical_ci_is_current_evidence") is not False:
        raise ReentryValidationError("historical head or CI cannot become current authority")
    if contract.get("direct_reopen_and_merge") is not False:
        raise ReentryValidationError("direct reopen-and-merge must remain prohibited")
    if contract.get("evidence_reuse_requires_current_claim_rebinding") is not True or contract.get("new_current_main_reauthoring_required") is not True:
        raise ReentryValidationError("historical reuse must rebind and re-author against current main")
    if contract.get("external_material_policy") != "DERIVATIVE_ONLY" or contract.get("raw_external_publication_in_repo_by_default") is not False:
        raise ReentryValidationError("external material must remain derivative-only by default")
    if tuple(contract.get("quality_feed_requirements", ())) != QUALITY_FEED_REQUIREMENTS:
        raise ReentryValidationError("quality re-entry requirements drifted")
    if tuple(contract.get("subjectivity_feed_requirements", ())) != tuple(x.upper() for x in SUBJECTIVITY_REENTRY_FIELDS):
        raise ReentryValidationError("subjectivity re-entry requirements drifted")

    consolidation = record.get("consolidation_plan")
    if not isinstance(consolidation, dict):
        raise ReentryValidationError("missing deduplicated consolidation plan")
    if consolidation.get("retained_draft_pr") != 122 or consolidation.get("retained_design") != "MEMORY_LOCUS_CONTINUITY_DEPENDENCY_DISCRIMINATION":
        raise ReentryValidationError("retained research design drifted")
    if tuple(consolidation.get("historical_source_prs", ())) != (38, 41, 8):
        raise ReentryValidationError("historical source provenance drifted")
    if tuple(consolidation.get("method_source_prs", ())) != (84,):
        raise ReentryValidationError("method-source provenance drifted")
    if tuple(consolidation.get("superseded_draft_prs", ())) != (123, 124):
        raise ReentryValidationError("duplicate Draft disposition drifted")
    if consolidation.get("current_main_method_anchor") != "PR118_INTERPRETIVE_SPECIFICITY_AND_EVIDENCE_ADMISSION":
        raise ReentryValidationError("current-main method anchor drifted")
    if consolidation.get("historical_code_reuse") is not False or consolidation.get("current_main_reauthoring_required") is not True:
        raise ReentryValidationError("consolidation attempted historical code reuse or skipped current-main re-authoring")
    _nonempty(consolidation.get("claim_ceiling"), "consolidated claim ceiling")

    entries = record.get("historical_reentry_cohort")
    if not isinstance(entries, list) or len(entries) != 12:
        raise ReentryValidationError("historical re-entry cohort must contain exactly 12 entries")
    numbers = {entry.get("pr") for entry in entries if isinstance(entry, dict)}
    if numbers != EXPECTED_COHORT:
        raise ReentryValidationError("historical re-entry cohort changed")

    for entry in entries:
        if not isinstance(entry, dict):
            raise ReentryValidationError("cohort entry must be an object")
        pr = entry.get("pr")
        _nonempty(entry.get("title"), f"PR {pr} title")
        if not SHA40.fullmatch(str(entry.get("historical_head", ""))):
            raise ReentryValidationError(f"PR {pr} lacks exact historical head")
        _nonempty(entry.get("disposition"), f"PR {pr} disposition")
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
        if action == "EXTRACT_REDESIGN_ONLY" and relation in {"QUALITY_FEED", "DUAL_CORE_REFERENCE"} and entry.get("control_effectiveness_recheck") is not True:
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
        if action == "EXTRACT_REDESIGN_ONLY" and pr != 37:
            if entry.get("historical_code_reuse") is not False or entry.get("current_main_reauthoring_required") is not True:
                raise ReentryValidationError(f"PR {pr} extraction must be newly authored from current main")

    by_pr = {entry["pr"]: entry for entry in entries}
    if by_pr[103]["disposition"] != "HISTORICAL_RESEARCH_VALIDITY_INCIDENT" or by_pr[103]["allowed_action"] != "PRESERVE_ONLY":
        raise ReentryValidationError("PR #103 incident containment weakened")
    if by_pr[84]["disposition"] != "SUPERSEDED_BY_MERGED_PR_85" or by_pr[84]["allowed_action"] != "NO_ACTION":
        raise ReentryValidationError("PR #84 supersession boundary weakened")
    if by_pr[84].get("derivative_method_source_only") is not True or by_pr[84].get("current_use") != "LOCAL_DISCRIMINANT_VALIDITY_CHECKLIST_IN_REFINED_PR122":
        raise ReentryValidationError("PR #84 method source was not properly deduplicated")
    for pr in (38, 41, 8):
        if by_pr[pr]["disposition"] != "EXTRACT_REDESIGN_CANDIDATE" or by_pr[pr]["allowed_action"] != "EXTRACT_REDESIGN_ONLY":
            raise ReentryValidationError(f"PR #{pr} must remain extract-and-reauthor only")
    for control_pr in (25, 26, 33):
        if by_pr[control_pr].get("researchization") is not False:
            raise ReentryValidationError("historical governance/topology control was researchized")
    for control_pr in (25, 26):
        if by_pr[control_pr]["disposition"] != "HISTORICAL_GOVERNANCE_TEST_CONTROL":
            raise ReentryValidationError("disposable authority control promoted as feature")
    if by_pr[33]["disposition"] != "OBSOLETE_BRANCH_TOPOLOGY_REMEDIATION":
        raise ReentryValidationError("historical branch topology remediation was revived")

    return {
        "status": "PASS",
        "audited_main": record["audited_main"],
        "audited_tree": record["audited_tree"],
        "historical_cohort_size": len(entries),
        "future_global_pr_counts_are_reentry_guard": False,
        "retained_draft_pr": 122,
        "superseded_duplicate_drafts": [123, 124],
        "full_qms_mapping": True,
        "direct_historical_merge": False,
        "historical_code_reuse": False,
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
