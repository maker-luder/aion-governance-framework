from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_BASE_BRANCH = "review/four-domain-research-materialization"
LOCAL_EXECUTION_BRANCHES = {
    EXPECTED_BASE_BRANCH,
    "convergence/two-branch-finalization-20260818",
}
SCHEMA = ROOT / "schemas/aion_research_consolidation_artifact_v0.1.0.schema.json"
CROSS_BRANCH_SCHEMA = ROOT / "schemas/aion_cross_branch_index_v0.1.0.schema.json"
TAXONOMY_SCHEMA = ROOT / "schemas/aion_public_discoverability_taxonomy_v0.1.0.schema.json"
CHANGE_PROV_SCHEMA = ROOT / "schemas/aion_change_level_provenance_v0.1.0.schema.json"
CROSS_BRANCH_INDEX = ROOT / "docs/research-consolidation/CROSS_BRANCH_INDEX_V0.1.0.json"
TAXONOMY = ROOT / "docs/research-consolidation/PUBLIC_DISCOVERABILITY_TAXONOMY_V0.1.0.json"
CHANGE_PROV = ROOT / "docs/research-consolidation/CHANGE_LEVEL_PROVENANCE_V0.1.0.json"
EVIDENCE_RECORD = ROOT / "research-workbench/four-domain-materialization/2026-08-14/P2_PACKET_C_EVIDENCE_ADMISSION_RECORD.json"
P2_PACKET = ROOT / "research-labs/four-domain-p2-materialization_v0.1.0/docs/P2_MATERIALIZATION_PACKET_C.md"
P2_TEST = ROOT / "research-labs/four-domain-p2-materialization_v0.1.0/tests/test_p2_compact.py"
P2_FIXTURE = ROOT / "research-labs/four-domain-p2-materialization_v0.1.0/fixtures/p2_synthetic_fixture_a.json"

ARTIFACTS = {
    "index": ROOT / "docs/research-consolidation/RESEARCH_INDEX_V0.1.0.json",
    "graph": ROOT / "docs/research-consolidation/CLAIM_DEPENDENCY_GRAPH_V0.1.0.json",
    "source_map": ROOT / "docs/research-consolidation/SOURCE_OF_TRUTH_MAP_V0.1.0.json",
    "crosswalk": ROOT / "docs/research-consolidation/EXTERNAL_LITERATURE_CROSSWALK_V0.1.0.json",
    "supersession": ROOT / "docs/research-consolidation/SUPERSESSION_MAP_V0.1.0.json",
    "matrix": ROOT / "docs/research-consolidation/PROMOTION_READINESS_MATRIX_V0.1.0.json",
    "falsifier": ROOT / "docs/research-consolidation/P2_PACKET_C_FALSIFIER_MATRIX_V0.1.0.json",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_execution_context(errors: list[str]) -> None:
    event_name = os.environ.get("GITHUB_EVENT_NAME", "").strip()
    if event_name == "pull_request":
        base_ref = os.environ.get("GITHUB_BASE_REF", "").strip()
        if base_ref != EXPECTED_BASE_BRANCH:
            fail(
                errors,
                f"unexpected pull_request base {base_ref!r}; expected {EXPECTED_BASE_BRANCH!r}",
            )
        return
    if event_name == "push":
        ref_name = os.environ.get("GITHUB_REF_NAME", "").strip()
        if ref_name != EXPECTED_BASE_BRANCH:
            fail(
                errors,
                f"unexpected push ref {ref_name!r}; expected {EXPECTED_BASE_BRANCH!r}",
            )
        return

    branch = git("branch", "--show-current")
    if branch not in LOCAL_EXECUTION_BRANCHES:
        fail(
            errors,
            f"unexpected local branch {branch!r}; expected one of {sorted(LOCAL_EXECUTION_BRANCHES)!r}",
        )


def validate_json_schema(
    errors: list[str], value: dict[str, Any], path: Path, schema_path: Path = SCHEMA
) -> None:
    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:
        fail(errors, f"jsonschema unavailable: {exc}")
        return
    try:
        schema = load(schema_path)
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        for error in sorted(validator.iter_errors(value), key=lambda item: list(item.absolute_path)):
            fail(errors, f"{path.relative_to(ROOT)} schema: {error.message}")
    except Exception as exc:  # pragma: no cover - diagnostic guard
        fail(errors, f"{path.relative_to(ROOT)} schema check error: {exc}")


def main() -> int:
    errors: list[str] = []

    try:
        validate_execution_context(errors)
    except subprocess.CalledProcessError as exc:
        fail(errors, f"cannot read execution branch context: {exc}")

    required_paths = (
        ROOT / "docs/research-consolidation/RESEARCH_INDEX_V0.1.0.md",
        ROOT / "docs/research-consolidation/CLAIM_DEPENDENCY_GRAPH_V0.1.0.md",
        ROOT / "docs/research-consolidation/SOURCE_OF_TRUTH_MAP_V0.1.0.md",
        ROOT / "docs/research-consolidation/EXTERNAL_LITERATURE_CROSSWALK_V0.1.0.md",
        ROOT / "docs/research-consolidation/SUPERSESSION_MAP_V0.1.0.md",
        ROOT / "docs/research-consolidation/PROMOTION_READINESS_MATRIX_V0.1.0.md",
        ROOT / "docs/research-consolidation/REVIEWER_FACING_VERTICAL_SLICE_P2_PACKET_C_V0.1.0.md",
        ROOT / "docs/research-consolidation/P2_PACKET_C_FALSIFIER_MATRIX_V0.1.0.md",
        ROOT / "docs/research-consolidation/CONVERGENCE_GAP_REGISTER_V0.1.0.md",
        ROOT / "docs/research-consolidation/CONVERGENCE_STATUS_V0.1.0.md",
        ROOT / "RESEARCH_BRANCH_STATUS.md",
        ROOT / "README.md",
        ROOT / "research-workbench/four-domain-materialization/2026-08-12/WHITEPAPER_WEB_BRANCH_RECONCILIATION_2026-08-12.md",
        ROOT / "research-labs/language-core-g1_v0.2.1/README.md",
        ROOT / "research-labs/language-core-g1_v0.2.1/docs/GOVERNANCE.md",
        ROOT / "research-labs/language-core-g1_v0.2.1/docs/IMPLEMENTATION_TRACEABILITY_MATRIX.csv",
        ROOT / "components/aion_runtime_v0.2.0/README.md",
        ROOT / "scripts/check_research_scope_lock.py",
        ROOT / "scripts/validate_research_evidence.py",
        ROOT / "schemas/research_evidence_record_v0.2.0.schema.json",
        ROOT / ".github/workflows/research-convergence-consistency.yml",
        ROOT / "docs/research-consolidation/CROSS_BRANCH_INDEX_V0.1.0.md",
        ROOT / "docs/research-consolidation/PUBLIC_DISCOVERABILITY_TAXONOMY_V0.1.0.md",
        ROOT / "schemas/aion_cross_branch_index_v0.1.0.schema.json",
        ROOT / "schemas/aion_public_discoverability_taxonomy_v0.1.0.schema.json",
        ROOT / "docs/research-consolidation/CHANGE_LEVEL_PROVENANCE_V0.1.0.md",
        ROOT / "schemas/aion_change_level_provenance_v0.1.0.schema.json",
    )
    for path in required_paths:
        if not path.exists():
            fail(errors, f"required inventory path missing: {path.relative_to(ROOT)}")

    for schema_path in (SCHEMA, CROSS_BRANCH_SCHEMA, TAXONOMY_SCHEMA, CHANGE_PROV_SCHEMA):
        if not schema_path.is_file():
            fail(errors, f"missing schema: {schema_path.relative_to(ROOT)}")

    for path in (ROOT / "README.md", ROOT / "RESEARCH_BRANCH_STATUS.md"):
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            for phrase in ("CANONICAL_EFFECT = NONE", "SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED"):
                if phrase not in text:
                    fail(errors, f"{path.relative_to(ROOT)} missing parity phrase: {phrase}")

    data: dict[str, Any] = {}
    for name, path in ARTIFACTS.items():
        if not path.is_file():
            fail(errors, f"missing artifact {name}: {path.relative_to(ROOT)}")
            continue
        try:
            value = load(path)
        except Exception as exc:
            fail(errors, f"invalid JSON {path.relative_to(ROOT)}: {exc}")
            continue
        if not isinstance(value, dict):
            fail(errors, f"artifact {name} is not an object")
            continue
        data[name] = value
        validate_json_schema(errors, value, path)
        if value.get("canonical_effect") != "NONE":
            fail(errors, f"{name} canonical_effect is not NONE")
        if value.get("deployment") is True:
            fail(errors, f"{name} deployment is true")

    special_data: dict[str, Any] = {}
    for name, path, schema_path in (
        ("cross_branch", CROSS_BRANCH_INDEX, CROSS_BRANCH_SCHEMA),
        ("taxonomy", TAXONOMY, TAXONOMY_SCHEMA),
        ("change_provenance", CHANGE_PROV, CHANGE_PROV_SCHEMA),
    ):
        if not path.is_file():
            fail(errors, f"missing artifact {name}: {path.relative_to(ROOT)}")
            continue
        try:
            value = load(path)
        except Exception as exc:
            fail(errors, f"invalid JSON {path.relative_to(ROOT)}: {exc}")
            continue
        if not isinstance(value, dict):
            fail(errors, f"artifact {name} is not an object")
            continue
        special_data[name] = value
        validate_json_schema(errors, value, path, schema_path)
        if value.get("canonical_effect") != "NONE":
            fail(errors, f"{name} canonical_effect is not NONE")

    index = data.get("index", {})
    graph = data.get("graph", {})
    source_map = data.get("source_map", {})
    crosswalk = data.get("crosswalk", {})
    supersession = data.get("supersession", {})
    matrix = data.get("matrix", {})
    falsifier = data.get("falsifier", {})

    expected_statuses = {"CURRENT", "SUPERSEDED", "HISTORICAL", "HOLD", "REJECT"}
    expected_dispositions = {"PROMOTE", "KEEP_RESEARCH_ONLY", "HOLD"}
    for name, value in (("index", index), ("matrix", matrix), ("falsifier", falsifier)):
        for row in value.get("entries", []) + value.get("rows", []):
            if row.get("status") not in expected_statuses:
                fail(errors, f"{name} has invalid status {row.get('status')!r}")
            if row.get("disposition") not in expected_dispositions:
                fail(errors, f"{name} has invalid disposition {row.get('disposition')!r}")

    for relation in supersession.get("relations", []):
        if relation.get("earlier_status") not in expected_statuses or relation.get("later_status") not in expected_statuses:
            fail(errors, f"supersession relation has invalid status: {relation.get('id')}")
        if relation.get("disposition") not in expected_dispositions:
            fail(errors, f"supersession relation has invalid disposition: {relation.get('id')}")

    index_text = (ROOT / "docs/research-consolidation/RESEARCH_INDEX_V0.1.0.md").read_text(encoding="utf-8")
    if "Four-Domain is the **research-method and evidence-question layer**" not in index_text:
        fail(errors, "index does not state Four-Domain method role")
    if "G1 is a **parallel enabling substrate**" not in index_text:
        fail(errors, "index does not state G1 parallel-substrate role")
    if index.get("four_domain_g1_relation", {}).get("authorized_runtime_integration") is not False:
        fail(errors, "Four-Domain/G1 authorized runtime integration must be false")
    if index.get("selected_vertical_slice", {}).get("id") != "VERT-P2-PACKET-C":
        fail(errors, "selected vertical slice is not VERT-P2-PACKET-C")

    edge_pairs = {(edge.get("from"), edge.get("to"), edge.get("kind")) for edge in graph.get("edges", [])}
    if ("P2", "FX", "IMPLEMENTATION_TO_FIXTURE") not in edge_pairs:
        fail(errors, "graph missing P2 to fixture edge")
    if ("P2", "T2", "IMPLEMENTATION_TO_TEST") not in edge_pairs:
        fail(errors, "graph missing P2 to test edge")
    if ("P2", "RT", "EXPLICIT_NON_INTEGRATION_BOUNDARY") not in edge_pairs:
        fail(errors, "graph missing P2 runtime non-integration edge")
    if ("G1", "FD", "SUBJECTIVITY_AUTHORITY") in edge_pairs or ("RT", "FD", "SUBJECTIVITY_AUTHORITY") in edge_pairs:
        fail(errors, "graph contains forbidden subjectivity authority edge")

    source_cases = {item.get("question"): item for item in source_map.get("entries", [])}
    if "branch standing" not in source_cases:
        fail(errors, "source map missing branch standing authority")
    else:
        if source_cases["branch standing"].get("authoritative") != ["RESEARCH_BRANCH_STATUS.md"]:
            fail(errors, "source map branch standing authority drifted")
    if "README_vs_status" not in {item.get("case") for item in source_map.get("duplicate_drift_resolutions", [])}:
        fail(errors, "source map missing README/status drift resolution")

    if supersession.get("policy", {}).get("historical_records") != "PRESERVE":
        fail(errors, "supersession policy does not preserve historical records")
    if supersession.get("policy", {}).get("date_erasure") is not False:
        fail(errors, "supersession policy permits date erasure")
    forbidden = set(supersession.get("forbidden_relations", []))
    for required in {
        "G1!=SUPERSESSION_OF_FOUR_DOMAIN_METHOD",
        "AION_RUNTIME_V0_2!=SUPERSESSION_OF_WHITEPAPER_METHOD",
        "KIMI_REVIEW!=SUPERSESSION_OF_PRIMARY_SOURCES",
    }:
        if required not in forbidden:
            fail(errors, f"supersession missing forbidden relation {required}")

    labels = {item.get("label") for item in crosswalk.get("papers_and_standards", []) + crosswalk.get("external_projects", [])}
    required_labels = {"VERIFIED", "PARTIAL", "ANALOGY", "AION_INTERPRETATION", "NOVELTY_HYPOTHESIS", "CORRECTION_REQUIRED"}
    declared_labels = set(crosswalk.get("claim_labels", []))
    if not required_labels.issubset(declared_labels):
        fail(errors, f"crosswalk missing declared labels {sorted(required_labels - declared_labels)}")
    if not labels.issubset(declared_labels):
        fail(errors, f"crosswalk row uses undeclared labels {sorted(labels - declared_labels)}")
    required_literature_ids = {
        "LIT-BUTLIN-AI-CONSCIOUSNESS-2023",
        "LIT-BUTLIN-INDICATORS-2025",
        "LIT-AGENT-TRACE-TRUST-SURVEY-2026",
        "LIT-GRAPHECTORY-2026",
        "LIT-ADPROV-2025",
        "LIT-MPCAB-2025",
        "LIT-PROV-AGENT-2025",
        "LIT-AGENT-SENTRY-2026",
        "LIT-FIDES-2025",
        "LIT-NEUROTAINT-2026",
        "LIT-AI-IDENTITY-2026",
        "LIT-AI-AUTHORSHIP-2026",
        "LIT-FAI2R-2026",
        "STD-COPE-AI-AUTHORSHIP-2023",
    }
    literature_rows = {item.get("id"): item for item in crosswalk.get("papers_and_standards", [])}
    if not required_literature_ids.issubset(literature_rows):
        fail(errors, f"crosswalk missing final-review literature rows: {sorted(required_literature_ids - set(literature_rows))}")
    for literature_id in required_literature_ids:
        if literature_rows.get(literature_id, {}).get("label") != "VERIFIED":
            fail(errors, f"final-review literature row is not VERIFIED: {literature_id}")
    survey = literature_rows.get("LIT-AGENT-TRACE-TRUST-SURVEY-2026", {})
    expected_supporting_ids = {"LIT-GRAPHECTORY-2026", "LIT-ADPROV-2025", "LIT-PROV-AGENT-2025", "LIT-AGENT-SENTRY-2026", "LIT-FIDES-2025", "LIT-NEUROTAINT-2026"}
    mapping = survey.get("survey_mapping", {})
    if mapping.get("role") != "MAIN_AGENT_PROVENANCE_SURVEY_ROW" or set(mapping.get("mapped_primary_source_ids", [])) != expected_supporting_ids:
        fail(errors, "agent-provenance survey main row does not map the required six primary sources")
    for supporting_id in expected_supporting_ids:
        supporting = literature_rows.get(supporting_id, {})
        if supporting.get("survey_mapping", {}).get("survey_id") != "LIT-AGENT-TRACE-TRUST-SURVEY-2026":
            fail(errors, f"supporting provenance row is not mapped to the survey: {supporting_id}")
    ai_authorship = literature_rows.get("LIT-AI-AUTHORSHIP-2026", {})
    if not all(token in str(ai_authorship.get("source_claim", "")) for token in ("AI-AUTHorship", "TraceAuth", "AIEIS", "P/S/G")):
        fail(errors, "AI-AUTHorship primary row is missing AI-AUTHorship/TraceAuth/AIEIS/P-S-G claims")
    for item in crosswalk.get("papers_and_standards", []) + crosswalk.get("external_projects", []):
        text = " ".join(str(item.get(key, "")) for key in ("claim", "aion_engineering", "aion_integration", "novelty" )).lower()
        novelty_patterns = (
            r"\b(?:aion|our|this)\s+(?:first|only|unprecedented)\b",
            r"\b(?:first|only|unprecedented)\s+(?:aion|contribution|result|system|architecture|method|claim)\b",
        )
        if any(re.search(pattern, text) for pattern in novelty_patterns) and item.get("label") not in {"CORRECTION_REQUIRED"}:
            fail(errors, f"crosswalk repeats forbidden novelty wording in {item.get('id')}")
    for item in crosswalk.get("external_projects", []):
        if item.get("id") in {"EXT-AISYSTESTING", "EXT-AIWARE", "EXT-MRIVAS", "EXT-ATOM"} and item.get("disposition") != "HOLD":
            fail(errors, f"unverified external project not HOLD: {item.get('id')}")

    cross_branch = special_data.get("cross_branch", {})
    expected_branch_heads = {
        "main": "e079fb7dfe7a04be7dcb94b8a059951a003caa94",
        "review/four-domain-research-materialization": "858442a3ec2439398d188779f4309397bd4926b2",
        "engineering/aion-research-consolidation-literature-grounding-readiness-20260814": "cab09a210709a01ee9ed55b1b2a6494a2628bdfb",
        "engineering/aion-native-language-feasibility-20260814": "3dfc21463502e1c32189ae167d92f163ca1a55e8",
        "engineering/aion-language-agnostic-runtime-integration-20260814": "6b81133dc351f5226fa95801254276e421b3e4fe",
        "cleanup/manus-output-consolidation-20260813": "c43430f9b39a86d11093f3286e9503145fcf0d70",
    }
    branch_rows = {row.get("name"): row for row in cross_branch.get("branches", [])}
    for branch_name, expected_head in expected_branch_heads.items():
        row = branch_rows.get(branch_name)
        if row is None:
            fail(errors, f"cross-branch index missing branch {branch_name}")
        elif row.get("head") != expected_head:
            fail(errors, f"cross-branch head drift for {branch_name}: {row.get('head')}")
    if branch_rows.get("main", {}).get("promotion_disposition") != "ALREADY_CANONICAL_BASELINE":
        fail(errors, "main branch disposition must be ALREADY_CANONICAL_BASELINE")
    if not any(item.get("id") == "CB-001" and item.get("promotion_disposition") == "ALREADY_CANONICAL_BASELINE" for item in cross_branch.get("artifacts", [])):
        fail(errors, "main README disposition must be ALREADY_CANONICAL_BASELINE")
    if cross_branch.get("repository_settings_modified") is not False:
        fail(errors, "cross-branch index says repository settings were modified")
    if cross_branch.get("topics_applied") is not False:
        fail(errors, "cross-branch index says topics were applied")
    if cross_branch.get("main_modified") is not False or cross_branch.get("research_source_modified") is not False:
        fail(errors, "cross-branch index reports protected source modification")
    required_cross_branch_artifacts = {"CB-001", "CB-002", "CB-003", "CB-004", "CB-005", "CB-006", "CB-007", "CB-008", "CB-009", "CB-010", "CB-011", "CB-012"}
    actual_cross_branch_artifacts = {item.get("id") for item in cross_branch.get("artifacts", [])}
    if not required_cross_branch_artifacts.issubset(actual_cross_branch_artifacts):
        fail(errors, f"cross-branch index missing artifact IDs: {sorted(required_cross_branch_artifacts - actual_cross_branch_artifacts)}")
    if not any(item.get("id") == "CB-009" and item.get("convergence") == "PRESENT" for item in cross_branch.get("artifacts", [])):
        fail(errors, "cross-branch index does not mark consolidation artifacts present")
    if any(item.get("id") == "CB-010" and item.get("convergence") != "ABSENT" for item in cross_branch.get("artifacts", [])):
        fail(errors, "Native Language artifacts are not explicitly absent from convergence branch")

    change_provenance = special_data.get("change_provenance", {})
    roles = change_provenance.get("roles", {})
    if roles.get("human_owner_proposal_and_authority", {}).get("actor") != "HUMAN_OWNER":
        fail(errors, "change provenance missing Human Owner proposal/authority role")
    if roles.get("chatgpt_architecture_and_review", {}).get("actor") != "CHATGPT":
        fail(errors, "change provenance missing ChatGPT architecture/review role")
    if roles.get("manus_implementation", {}).get("actor") != "MANUS":
        fail(errors, "change provenance missing Manus implementation role")
    if roles.get("owner_approval", {}).get("status") != "PENDING":
        fail(errors, "change provenance owner approval is not PENDING")
    preservation = change_provenance.get("historical_source_preservation", {})
    if preservation.get("historical_p2_provenance_edited") is not False or preservation.get("historical_p2_authorship_rewritten") is not False:
        fail(errors, "historical P2 provenance/authorship was marked rewritten")
    if preservation.get("current_convergence_provenance_is_distinct") is not True:
        fail(errors, "current convergence provenance is not distinct from historical P2 provenance")

    index_change_provenance = index.get("change_level_provenance", {})
    if index_change_provenance.get("implementation") != "MANUS" or index_change_provenance.get("approval") != "PENDING":
        fail(errors, "Research Index change-level provenance is not Manus/PENDING separated")
    taxonomy = special_data.get("taxonomy", {})
    candidates = taxonomy.get("candidate_topics", [])
    slugs = [item.get("slug") for item in candidates]
    ranks = [item.get("rank") for item in candidates]
    if len(candidates) < 10 or len(candidates) > 16:
        fail(errors, f"taxonomy candidate count outside 10-16: {len(candidates)}")
    if len(slugs) != len(set(slugs)):
        fail(errors, "taxonomy candidate slugs are not unique")
    if ranks != list(range(1, len(candidates) + 1)):
        fail(errors, "taxonomy ranks are not contiguous from 1")
    forbidden_topic_fragments = ("conscious", "sentient", "self-aware", "identity", "first", "only", "unprecedented", "agi", "production")
    for slug in slugs:
        if any(fragment in str(slug) for fragment in forbidden_topic_fragments):
            fail(errors, f"taxonomy contains forbidden public positioning term: {slug}")
    recommended = set(taxonomy.get("recommended_initial_set", []))
    owner_review = set(taxonomy.get("owner_review_set", []))
    candidate_by_slug = {item.get("slug"): item for item in candidates}
    if not recommended.issubset(set(slugs)):
        fail(errors, "recommended taxonomy set contains a slug not in candidates")
    if not owner_review.issubset(set(slugs)):
        fail(errors, "owner-review taxonomy set contains a slug not in candidates")
    if recommended.intersection(owner_review):
        fail(errors, f"recommended and owner-review taxonomy sets overlap: {sorted(recommended.intersection(owner_review))}")
    for slug in recommended:
        row = candidate_by_slug.get(slug, {})
        if row.get("readiness") != "READY_CANDIDATE" or row.get("owner_review") != "REQUIRED_BEFORE_SETTINGS_CHANGE":
            fail(errors, f"recommended Topic readiness mismatch: {slug}")
    for slug in owner_review:
        row = candidate_by_slug.get(slug, {})
        if row.get("readiness") != "OWNER_REVIEW_REQUIRED" or row.get("owner_review") != "REQUIRED":
            fail(errors, f"owner-review Topic readiness mismatch: {slug}")
    required_owner_review_topics = {"provenance-aware-ai", "long-term-memory", "metacognition", "ai-safety-evaluation", "governance-kernel"}
    if not required_owner_review_topics.issubset(owner_review):
        fail(errors, f"required owner-review Topics missing: {sorted(required_owner_review_topics - owner_review)}")
    if "governance-kernel" in recommended:
        fail(errors, "governance-kernel must remain Owner review only")
    required_rejected_topics = {"consciousness", "self-aware-ai", "sentient-ai", "identity-continuity", "first-of-its-kind", "agi", "production-ai"}
    rejected_slugs = {item.get("slug") for item in taxonomy.get("rejected_topics", [])}
    if not required_rejected_topics.issubset(rejected_slugs):
        fail(errors, f"taxonomy missing rejected terms: {sorted(required_rejected_topics - rejected_slugs)}")
    if "artificial-consciousness" in rejected_slugs:
        fail(errors, "artificial-consciousness must not remain permanently rejected")
    public_positioning = taxonomy.get("owner_positioning_review", [])
    if len(public_positioning) != 1 or public_positioning[0].get("slug") != "artificial-consciousness":
        fail(errors, "artificial-consciousness public positioning review record is malformed")
    if public_positioning and public_positioning[0].get("status") != "OWNER_PUBLIC_POSITIONING_REVIEW":
        fail(errors, "artificial-consciousness is not OWNER_PUBLIC_POSITIONING_REVIEW")
    positioning_invariants = taxonomy.get("positioning_invariants", {})
    if positioning_invariants.get("machine_rule") != "RESEARCH_TOPIC != CAPABILITY_CLAIM != SCIENTIFIC_CONCLUSION":
        fail(errors, "taxonomy missing machine-enforced positioning separation rule")
    for invariant in ("research_topic_is_not_capability_claim", "research_topic_is_not_scientific_conclusion", "capability_claim_is_not_scientific_conclusion"):
        if positioning_invariants.get(invariant) is not True:
            fail(errors, f"taxonomy positioning invariant is not true: {invariant}")
    if taxonomy.get("topics_applied") is not False or taxonomy.get("repository_settings_modified") is not False:
        fail(errors, "taxonomy claims that topics/settings were applied")
    if taxonomy.get("application_boundary", {}).get("settings_operation") != "NOT_PERFORMED":
        fail(errors, "taxonomy application boundary is not NOT_PERFORMED")

    first_batch = set(matrix.get("recommended_first_batch", []))
    if not first_batch:
        fail(errors, "promotion matrix has empty recommended first batch")
    for row in matrix.get("rows", []):
        if row.get("id") in first_batch and row.get("disposition") != "PROMOTE":
            fail(errors, f"first-batch row is not PROMOTE: {row.get('id')}")
    for row in matrix.get("rows", []):
        if row.get("id") in {"PR-009", "PR-010", "PR-011", "PR-014", "PR-015", "PR-017", "PR-020", "PR-025", "PR-026", "PR-027"} and row.get("disposition") == "PROMOTE":
            fail(errors, f"excluded runtime/claim row is PROMOTE: {row.get('id')}")

    for path in (P2_PACKET, P2_TEST, P2_FIXTURE, EVIDENCE_RECORD):
        if not path.is_file():
            fail(errors, f"missing vertical-slice path: {path.relative_to(ROOT)}")
    if P2_PACKET.is_file():
        packet = P2_PACKET.read_text(encoding="utf-8")
        for phrase in ("HISTORICAL_REPORTED_TEST_COUNT = 13", "CURRENT_TEST_FUNCTION_COUNT = 5", "CURRENT_EXPECTED_RESULT = 5 passed", "RUNTIME_EFFECT = NONE"):
            if phrase not in packet:
                fail(errors, f"P2 Packet C missing reconciliation phrase: {phrase}")
    if P2_TEST.is_file():
        test_count = len(re.findall(r"^def test_", P2_TEST.read_text(encoding="utf-8"), flags=re.MULTILINE))
        if test_count != 5:
            fail(errors, f"P2 current test function count is {test_count}, expected 5")
    if P2_FIXTURE.is_file():
        fixture = load(P2_FIXTURE)
        if fixture.get("canonical_effect") != "NONE":
            fail(errors, "P2 fixture canonical effect drifted")
        if fixture.get("expected", {}).get("selected_record_ids") != ["fact-new"]:
            fail(errors, "P2 fixture selected record expectation drifted")
        if fixture.get("expected", {}).get("identity_continuity_conclusion") != "NOT_ESTABLISHED":
            fail(errors, "P2 fixture identity boundary drifted")

    if EVIDENCE_RECORD.is_file():
        sys.path.insert(0, str(ROOT / "scripts"))
        try:
            from validate_research_evidence import validate_record

            result = validate_record(ROOT, EVIDENCE_RECORD)
            if result.status != "PASS":
                fail(errors, f"P2 evidence admission validation did not PASS: {result.diagnostics}")
            record = load(EVIDENCE_RECORD)
            if record.get("result_status") != "HOLD":
                fail(errors, "P2 evidence record must remain HOLD")
            if record.get("canonical_effect") != "NONE":
                fail(errors, "P2 evidence record canonical effect drifted")
            change_record = record.get("change_level_provenance", {})
            if change_record.get("implementation", {}).get("actor") != "MANUS":
                fail(errors, "P2 evidence record missing Manus implementation provenance")
            if change_record.get("proposal_and_authority", {}).get("actor") != "HUMAN_OWNER" or change_record.get("proposal_and_authority", {}).get("role") != "TASK_AUTHORIZATION_AND_FINAL_AUTHORITY":
                fail(errors, "P2 evidence record missing Human Owner task authorization/final authority provenance")
            if change_record.get("architecture_and_review", {}).get("actor") != "CHATGPT" or change_record.get("architecture_and_review", {}).get("role") != "FINAL_REVIEW_FINDINGS_AND_ARCHITECTURE_REVIEW":
                fail(errors, "P2 evidence record missing ChatGPT final-review findings provenance")
            if change_record.get("approval", {}).get("status") != "PENDING":
                fail(errors, "P2 evidence record owner approval must remain PENDING")
            if change_record.get("historical_p2_provenance_preserved") is not True:
                fail(errors, "P2 evidence record does not preserve historical provenance")
        except Exception as exc:  # pragma: no cover - diagnostic guard
            fail(errors, f"P2 evidence admission check error: {exc}")

    forbidden_source_patterns = (
        r"^\s*import\s+(requests|urllib|socket|subprocess)\b",
        r"^\s*from\s+(requests|urllib|socket|subprocess)\b",
        r"\bsubprocess\.",
        r"\beval\(",
        r"\bexec\(",
        r"\bimport\s+mcp\b",
        r"\bfrom\s+mcp\b",
    )
    p2_src = ROOT / "research-labs/four-domain-p2-materialization_v0.1.0/src"
    if p2_src.is_dir():
        for source in p2_src.rglob("*.py"):
            text = source.read_text(encoding="utf-8")
            for pattern in forbidden_source_patterns:
                if re.search(pattern, text, flags=re.MULTILINE | re.IGNORECASE):
                    fail(errors, f"P2 source contains forbidden runtime/transport pattern {pattern}: {source.relative_to(ROOT)}")

    if errors:
        print("research consolidation consistency: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("research consolidation consistency: PASS")
    print(f"validated artifacts={len(data)}; p2_tests=5; canonical_effect=NONE; deployment=FALSE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
