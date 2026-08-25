from __future__ import annotations

import json
from pathlib import Path

from aion_evidence_interop.inspect_export import export_inspect


COMPONENT = Path(__file__).resolve().parents[1]


def test_inspect_export_matches_sample_shape_without_execution() -> None:
    record = json.loads((COMPONENT / "fixtures" / "valid_minimal.json").read_text())
    task, sample = export_inspect(record, "qa/evidence.json")
    assert isinstance(sample["input"], str)
    assert isinstance(sample["target"], list)
    assert sample["id"] == record["claim_id"]
    assert sample["metadata"]["execution_authorized"] is False
    assert task["execution"] == {
        "model_execution": False,
        "network_access": False,
        "sandbox_setup": False,
        "solver_defined": False,
        "scorer_defined": False,
        "inspect_eval_executed": False,
    }
    assert task["nonclaims"]["subjectivity_conclusion"] == "NOT_ESTABLISHED"
    assert set(sample) == {"id", "input", "target", "metadata"}
    assert not set(task["prohibited_runtime_fields"]) & set(sample)
