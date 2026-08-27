from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_required_schemas_are_machine_readable() -> None:
    for name in ("triadic_state_snapshot_v0.1.0.schema.json", "triadic_transition_v0.1.0.schema.json", "experiment_manifest_v0.1.0.schema.json"):
        value = json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8")); assert value["$schema"].endswith("2020-12/schema") and value["type"] == "object" and value["required"]


def test_fixture_covers_preregistered_conditions() -> None:
    value = json.loads((ROOT / "fixtures" / "triadic-baseline.json").read_text(encoding="utf-8")); required = {"NORM_STATE_ON", "NORM_STATE_OFF", "NORM_STATE_CONFLICTED", "NORM_STATE_ADVERSARIALLY_PERTURBED", "EXTERNAL_NORM_PROMPT_REMOVED", "MOTIVATIONAL_STATE_ABLATED", "SELF_WORLD_MODEL_ABLATED", "STATE_SWAPPED", "HISTORY_RESET", "HISTORY_RESTORED", "REPLAY", "RANDOM_CONTROL"}; assert required <= set(value["conditions"]); assert value["canonical_effect"] == value["action_authority"] == "NONE"
