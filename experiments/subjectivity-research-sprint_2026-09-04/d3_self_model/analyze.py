#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

D4_RESULT = Path(__file__).resolve().parents[1] / "d4_heldout" / "RESULT.json"


def analyze() -> dict:
    report = json.loads(D4_RESULT.read_text(encoding="utf-8"))
    rows = []
    for family in report["families"]:
        effects = dict(family.get("channel_ablation_effects") or [])
        rows.append(
            {
                "family_id": family["family_id"],
                "SELF_MODEL_ABLATED_changed": bool(effects.get("SELF_MODEL_ABLATED")),
                "AFFECT_ABLATED_changed": bool(effects.get("AFFECT_ABLATED")),
                "full_ablation_changed": family["ablation_changed"],
            }
        )
    self_model_specific = any(row["SELF_MODEL_ABLATED_changed"] for row in rows)
    return {
        "question": "Under matched external conditions, does ablating only SELF_MODEL change selection?",
        "claim_ceiling": "L3_SYNTHETIC_HARNESS",
        "SELF_WORLD_MODEL_FUNCTION != PHENOMENAL_SELF": True,
        "SELF_MODEL_CAUSAL_ROLE != SUBJECTIVITY_ESTABLISHED": True,
        "self_model_specific_effect_observed": self_model_specific,
        "result_status": "NOT_SUPPORTED" if not self_model_specific else "SUPPORTED",
        "families": rows,
        "SUBJECTIVITY_CONCLUSION": "NOT_ESTABLISHED",
    }


if __name__ == "__main__":
    text = json.dumps(analyze(), indent=2, sort_keys=True)
    Path(__file__).with_name("RESULT.json").write_text(text + "\n", encoding="utf-8")
    print(text)
