import json
from pathlib import Path

import scripts.check_research_consolidation_consistency as consistency


ROOT = Path(__file__).resolve().parents[2]
CONSOLIDATION = ROOT / "docs" / "research-consolidation"


def test_machine_consistency_checker_passes():
    assert consistency.main() == 0


def test_named_artifacts_have_markdown_and_json_companions():
    pairs = (
        "RESEARCH_INDEX_V0.1.0",
        "CLAIM_DEPENDENCY_GRAPH_V0.1.0",
        "SOURCE_OF_TRUTH_MAP_V0.1.0",
        "EXTERNAL_LITERATURE_CROSSWALK_V0.1.0",
        "SUPERSESSION_MAP_V0.1.0",
        "PROMOTION_READINESS_MATRIX_V0.1.0",
    )
    for stem in pairs:
        assert (CONSOLIDATION / f"{stem}.md").is_file()
        assert (CONSOLIDATION / f"{stem}.json").is_file()


def test_first_batch_excludes_runtime_and_unverified_claims():
    matrix = json.loads(
        (CONSOLIDATION / "PROMOTION_READINESS_MATRIX_V0.1.0.json").read_text(
            encoding="utf-8"
        )
    )
    first_batch = set(matrix["recommended_first_batch"])
    assert {"PR-001", "PR-002", "PR-003", "PR-004", "PR-005", "PR-006", "PR-007", "PR-008"} <= first_batch
    assert not first_batch.intersection({"PR-014", "PR-015", "PR-017", "PR-020", "PR-025", "PR-026", "PR-027"})


def test_cross_branch_index_and_public_taxonomy_contract():
    cross_branch = json.loads(
        (CONSOLIDATION / "CROSS_BRANCH_INDEX_V0.1.0.json").read_text(encoding="utf-8")
    )
    branches = {row["name"]: row for row in cross_branch["branches"]}
    assert branches["main"]["head"] == "e079fb7dfe7a04be7dcb94b8a059951a003caa94"
    assert branches["review/four-domain-research-materialization"]["head"] == "858442a3ec2439398d188779f4309397bd4926b2"
    assert branches["engineering/aion-research-consolidation-literature-grounding-readiness-20260814"]["head"] == "cab09a210709a01ee9ed55b1b2a6494a2628bdfb"
    assert branches["main"]["promotion_disposition"] == "ALREADY_CANONICAL_BASELINE"
    assert cross_branch["repository_settings_modified"] is False
    assert cross_branch["topics_applied"] is False
    assert cross_branch["main_modified"] is False
    assert cross_branch["research_source_modified"] is False

    taxonomy = json.loads(
        (CONSOLIDATION / "PUBLIC_DISCOVERABILITY_TAXONOMY_V0.1.0.json").read_text(encoding="utf-8")
    )
    slugs = [item["slug"] for item in taxonomy["candidate_topics"]]
    assert 10 <= len(slugs) <= 16
    assert len(slugs) == len(set(slugs))
    recommended = set(taxonomy["recommended_initial_set"])
    owner_review = set(taxonomy["owner_review_set"])
    by_slug = {item["slug"]: item for item in taxonomy["candidate_topics"]}
    assert recommended.issubset(slugs)
    assert recommended.isdisjoint(owner_review)
    assert "governance-kernel" in owner_review
    assert "governance-kernel" not in recommended
    assert all(by_slug[slug]["readiness"] == "READY_CANDIDATE" and by_slug[slug]["owner_review"] == "REQUIRED_BEFORE_SETTINGS_CHANGE" for slug in recommended)
    assert all(by_slug[slug]["readiness"] == "OWNER_REVIEW_REQUIRED" and by_slug[slug]["owner_review"] == "REQUIRED" for slug in owner_review)
    assert taxonomy["topics_applied"] is False
    assert taxonomy["application_boundary"]["settings_operation"] == "NOT_PERFORMED"
    assert taxonomy["owner_positioning_review"] == [{"slug": "artificial-consciousness", "status": "OWNER_PUBLIC_POSITIONING_REVIEW", "reason": taxonomy["owner_positioning_review"][0]["reason"]}]
    assert "artificial-consciousness" not in {item["slug"] for item in taxonomy["rejected_topics"]}
    assert taxonomy["positioning_invariants"]["machine_rule"] == "RESEARCH_TOPIC != CAPABILITY_CLAIM != SCIENTIFIC_CONCLUSION"
    assert all(taxonomy["positioning_invariants"][key] is True for key in ("research_topic_is_not_capability_claim", "research_topic_is_not_scientific_conclusion", "capability_claim_is_not_scientific_conclusion"))
    provenance = json.loads((CONSOLIDATION / "CHANGE_LEVEL_PROVENANCE_V0.1.0.json").read_text(encoding="utf-8"))
    assert provenance["roles"]["human_owner_proposal_and_authority"]["actor"] == "HUMAN_OWNER"
    assert provenance["roles"]["human_owner_proposal_and_authority"]["role"] == "TASK_AUTHORIZATION_AND_FINAL_AUTHORITY"
    assert provenance["roles"]["chatgpt_architecture_and_review"]["actor"] == "CHATGPT"
    assert provenance["roles"]["chatgpt_architecture_and_review"]["role"] == "FINAL_REVIEW_FINDINGS_AND_ARCHITECTURE_REVIEW"
    assert provenance["roles"]["manus_implementation"]["actor"] == "MANUS"
    assert provenance["roles"]["owner_approval"]["status"] == "PENDING"
    assert provenance["historical_source_preservation"]["historical_p2_authorship_rewritten"] is False
    assert {"consciousness", "self-aware-ai", "sentient-ai", "first-of-its-kind", "production-ai"} <= {
        item["slug"] for item in taxonomy["rejected_topics"]
    }
    crosswalk = json.loads((CONSOLIDATION / "EXTERNAL_LITERATURE_CROSSWALK_V0.1.0.json").read_text(encoding="utf-8"))
    literature = {item["id"]: item for item in crosswalk["papers_and_standards"]}
    required = {"LIT-BUTLIN-INDICATORS-2025", "LIT-AGENT-TRACE-TRUST-SURVEY-2026", "LIT-GRAPHECTORY-2026", "LIT-ADPROV-2025", "LIT-PROV-AGENT-2025", "LIT-AGENT-SENTRY-2026", "LIT-FIDES-2025", "LIT-NEUROTAINT-2026", "LIT-AI-AUTHORSHIP-2026"}
    assert required <= set(literature)
    assert all(literature[item]["label"] == "VERIFIED" for item in required)
    assert set(literature["LIT-AGENT-TRACE-TRUST-SURVEY-2026"]["survey_mapping"]["mapped_primary_source_ids"]) == {"LIT-GRAPHECTORY-2026", "LIT-ADPROV-2025", "LIT-PROV-AGENT-2025", "LIT-AGENT-SENTRY-2026", "LIT-FIDES-2025", "LIT-NEUROTAINT-2026"}
    assert all(token in literature["LIT-AI-AUTHORSHIP-2026"]["source_claim"] for token in ("AI-AUTHorship", "TraceAuth", "AIEIS", "P/S/G"))


def test_convergence_workflow_is_read_only_and_branch_scoped():
    workflow = (ROOT / ".github/workflows/research-convergence-consistency.yml").read_text(
        encoding="utf-8"
    )
    assert "engineering/aion-research-consolidation-literature-grounding-readiness-20260814" in workflow
    assert "pull_request_target" not in workflow
    assert "contents: read" in workflow
    assert "persist-credentials: false" in workflow
    assert "uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1" in workflow
    assert "uses: actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97" in workflow
    assert "review/four-domain-research-materialization" not in workflow
    assert "python -m pip install -e ." in workflow


def test_p2_evidence_record_is_hold_and_noncanonical():
    record = json.loads(
        (
            ROOT
            / "research-workbench/four-domain-materialization/2026-08-14/P2_PACKET_C_EVIDENCE_ADMISSION_RECORD.json"
        ).read_text(encoding="utf-8")
    )
    assert record["result_status"] == "HOLD"
    assert record["canonical_effect"] == "NONE"
    assert record["independent_validation_status"] == "IVV_NOT_ACHIEVED"
    assert record["nonclaims"]["identity_continuity_conclusion"] == "NOT_ESTABLISHED"
