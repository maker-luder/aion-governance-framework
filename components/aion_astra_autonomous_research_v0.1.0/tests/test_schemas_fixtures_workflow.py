from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


COMPONENT = Path(__file__).resolve().parents[1]
ROOT = COMPONENT.parents[1]


def test_all_schemas_are_valid_draft_2020_12() -> None:
    campaign_schemas = sorted((COMPONENT / "schemas").glob("*.schema.json"))
    triadic_schemas = sorted(
        (ROOT / "research-labs" / "triadic-state-dynamics_v0.1.0" / "schemas").glob("*.schema.json")
    )
    assert len(campaign_schemas) == 5
    assert len(triadic_schemas) >= 3
    schema_paths = [*campaign_schemas, *triadic_schemas]
    for path in schema_paths:
        Draft202012Validator.check_schema(json.loads(path.read_text(encoding="utf-8")))


def test_fourteen_public_fixtures_validate() -> None:
    schema = json.loads(
        (COMPONENT / "schemas" / "experiment_manifest_v0.1.0.schema.json").read_text(encoding="utf-8")
    )
    fixtures = sorted((COMPONENT / "fixtures").glob("*.json"))
    assert len(fixtures) == 14
    for path in fixtures:
        Draft202012Validator(schema).validate(json.loads(path.read_text(encoding="utf-8")))


def test_fixture_catalog_covers_required_conditions_and_controls() -> None:
    records = [json.loads(path.read_text(encoding="utf-8")) for path in sorted((COMPONENT / "fixtures").glob("*.json"))]
    conditions = {record["condition"] for record in records}
    assert {
        "NORM_STATE_ON",
        "NORM_STATE_OFF",
        "NORM_STATE_CONFLICTED",
        "NORM_STATE_ADVERSARIALLY_PERTURBED",
        "EXTERNAL_NORM_PROMPT_REMOVED",
        "MOTIVATIONAL_STATE_ABLATED",
        "SELF_WORLD_MODEL_ABLATED",
        "STATE_SWAPPED",
        "HISTORY_RESET",
        "REPLAY",
        "RANDOM_CONTROL",
    } <= conditions
    sequences = {item for record in records for item in record.get("sequence", [])}
    assert "HISTORY_RESTORED" in sequences
    assert "AION_PROPOSER_ASTRA_FALSIFIER" in sequences
    assert "ASTRA_PROPOSER_AION_FALSIFIER" in sequences
    assert any(record["expected_disposition"] == "REJECT" for record in records)
    assert all(record["canonical_effect"] == "NONE" for record in records)
    assert all(record["action_authority"] == "NONE" for record in records)


def test_workflow_is_manual_or_relevant_pr_only_and_fail_closed() -> None:
    workflow = (ROOT / ".github" / "workflows" / "aion-astra-autonomous-research.yml").read_text(encoding="utf-8")
    assert "workflow_dispatch:" in workflow
    assert "pull_request:" in workflow
    assert "schedule:" not in workflow
    assert "push:" not in workflow
    assert "contents: read" in workflow
    assert "persist-credentials: false" in workflow
    assert "external_web" in workflow
    assert "default: false" in workflow
    assert "runner.temp" in workflow
    assert "git status --porcelain --untracked-files=all" in workflow
    assert "Working tree changed during bounded campaign" in workflow
    assert "uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1" in workflow
    assert "uses: actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97" in workflow
    pythonpath = next(line.strip().removeprefix("PYTHONPATH: ") for line in workflow.splitlines() if line.strip().startswith("PYTHONPATH: "))
    assert " " not in pythonpath
    source_roots = pythonpath.split(":")
    assert len(source_roots) == 7
    assert "research-labs/subjectivity-pipeline_v0.1.0/src" in source_roots
