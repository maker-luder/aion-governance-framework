from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys


LAB_ROOT = Path(__file__).resolve().parents[1]
SRC = LAB_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from aion_subjectivity_pipeline import (  # noqa: E402
    ContinuityCase,
    ContinuityChannel,
    ContinuityDissociationHarness,
    ContinuityIntervention,
    ContinuityRunBinding,
)


BASE_COMMIT_SHA = "d95bc2625e71f1c85a725aaba78cb0feccfc0668"
BASE_TREE_SHA = "77470062979df1db2f17c3a2a396891d1e910f98"
SPECIFICATION_PR = 101
SPECIFICATION_HEAD_SHA = "b6d81743c6e8b879be31074bb9d98acc9b4be13a"


def execute() -> dict[str, object]:
    fixture_path = LAB_ROOT / "fixtures" / "continuity_dissociation_synthetic.json"
    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    if data["contains_private_transcript"] or data["human_psychometric_classification"]:
        raise ValueError("synthetic fixture privacy or psychometric boundary changed")
    binding = ContinuityRunBinding(**data["binding"])
    cases = tuple(
        ContinuityCase(
            case_id=row["case_id"],
            intervention=ContinuityIntervention(row["intervention"]),
            target_channels=tuple(ContinuityChannel(item) for item in row["target_channels"]),
            retained_channels=tuple(ContinuityChannel(item) for item in row["retained_channels"]),
            strategy_signature=row["strategy_signature"],
            self_prediction_state=row["self_prediction_state"],
            evidence_refs=tuple(row["evidence_refs"]),
            binding=binding,
        )
        for row in data["cases"]
    )
    audit = ContinuityDissociationHarness().audit(cases)
    return {
        "schema_version": "0.1.0",
        "experiment_id": "AION-CONTINUITY-DISSOCIATION-SYNTHETIC-001",
        "mode": "DETERMINISTIC_SYNTHETIC_FIXTURE",
        "specification_dependency": {
            "pull_request": SPECIFICATION_PR,
            "head_commit_sha": SPECIFICATION_HEAD_SHA,
            "unmerged": True,
            "used_as_implementation_base": False,
        },
        "implementation_base": {
            "commit_sha": BASE_COMMIT_SHA,
            "tree_sha": BASE_TREE_SHA,
        },
        "fixture_sha256": hashlib.sha256(fixture_path.read_bytes()).hexdigest(),
        "case_fingerprints": {case.intervention.value: case.fingerprint for case in cases},
        "structurally_admissible": audit.structurally_admissible,
        "case_count": audit.case_count,
        "distinct_failure_profiles": audit.distinct_failure_profiles,
        "changed_strategy_conditions": list(audit.changed_strategy_conditions),
        "changed_self_prediction_conditions": list(audit.changed_self_prediction_conditions),
        "reasons": list(audit.reasons),
        "model_invoked": False,
        "private_transcript_collected": False,
        "human_psychometric_classification": False,
        "empirical_result": audit.empirical_result,
        "identity_continuity_conclusion": audit.identity_continuity_conclusion,
        "subjectivity_conclusion": audit.subjectivity_conclusion,
        "consciousness_conclusion": audit.consciousness_conclusion,
        "phenomenal_experience_conclusion": audit.phenomenal_experience_conclusion,
        "moral_status_conclusion": audit.moral_status_conclusion,
        "scientific_disposition": audit.scientific_disposition,
        "canonical_effect": audit.canonical_effect,
        "deployment": audit.deployment,
        "merge_authorization": "NONE",
        "main_write": "NO",
    }


def main() -> int:
    output = LAB_ROOT / "results" / "continuity_dissociation_synthetic_receipt.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    result = execute()
    output.write_bytes((json.dumps(result, indent=2, sort_keys=True) + "\n").encode())
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
