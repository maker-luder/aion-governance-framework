from __future__ import annotations

from pathlib import Path

import pytest

from aion_evidence_interop.opa_export import evaluate_boundaries


COMPONENT = Path(__file__).resolve().parents[1]


def _digest(character: str) -> str:
    return character * 64


def _input() -> dict[str, object]:
    return {
        "source": {"validation_status": "PASS"},
        "boundaries": {
            "canonical_effect": "NONE",
            "deployment": False,
            "research_execution": False,
            "model_execution": False,
            "network_access": False,
            "subjectivity_conclusion": "NOT_ESTABLISHED",
            "identity_continuity_conclusion": "NOT_ESTABLISHED",
            "independent_ivv": "NOT_ACHIEVED",
            "human_identity_inferred": False,
            "human_presence_inferred": False,
            "merge_authority_inferred": False,
        },
        "artifact_digests": {
            "attestation.intoto.json": _digest("a"),
            "prov.jsonld": _digest("b"),
            "ro-crate-metadata.json": _digest("c"),
            "inspect/task-manifest.json": _digest("d"),
            "inspect/dataset.jsonl": _digest("e"),
            "openssf/scorecard-crosswalk.json": _digest("f"),
        },
    }


def test_python_policy_mirror_allows_closed_boundaries() -> None:
    allow, reasons = evaluate_boundaries(_input())
    assert allow is True
    assert reasons == ()


def test_python_policy_mirror_denies_semantic_promotion() -> None:
    value = _input()
    value["boundaries"]["subjectivity_conclusion"] = "ESTABLISHED"  # type: ignore[index]
    allow, reasons = evaluate_boundaries(value)
    assert allow is False
    assert "SUBJECTIVITY_PROMOTION_DETECTED" in reasons


@pytest.mark.parametrize(
    ("field", "invalid", "reason"),
    [
        ("canonical_effect", "PROMOTE", "CANONICAL_EFFECT_OPEN"),
        ("deployment", True, "DEPLOYMENT_TRUE"),
        ("research_execution", True, "RESEARCH_EXECUTION_REQUESTED"),
        ("model_execution", True, "MODEL_EXECUTION_REQUESTED"),
        ("network_access", True, "NETWORK_ACCESS_REQUESTED"),
        ("subjectivity_conclusion", "ESTABLISHED", "SUBJECTIVITY_PROMOTION_DETECTED"),
        ("identity_continuity_conclusion", "ESTABLISHED", "IDENTITY_PROMOTION_DETECTED"),
        ("independent_ivv", "IVV_ACHIEVED", "IVV_PROMOTION_DETECTED"),
        ("human_identity_inferred", True, "HUMAN_IDENTITY_INFERENCE_DETECTED"),
        ("human_presence_inferred", True, "HUMAN_PRESENCE_INFERENCE_DETECTED"),
        ("merge_authority_inferred", True, "MERGE_AUTHORITY_INFERENCE_DETECTED"),
    ],
)
def test_python_policy_mirror_denies_every_critical_boundary(
    field: str, invalid: object, reason: str
) -> None:
    value = _input()
    value["boundaries"][field] = invalid  # type: ignore[index]
    allow, reasons = evaluate_boundaries(value)
    assert allow is False
    assert reason in reasons


@pytest.mark.parametrize("invalid", ["", "a" * 63, "A" * 64, "g" * 64, 123])
def test_python_policy_mirror_denies_missing_or_malformed_digest(invalid: object) -> None:
    value = _input()
    value["artifact_digests"]["prov.jsonld"] = invalid  # type: ignore[index]
    allow, reasons = evaluate_boundaries(value)
    assert allow is False
    assert "MISSING_DERIVATION_HASH" in reasons


def test_rego_policy_is_fail_closed_and_checks_execution_boundaries() -> None:
    policy = (COMPONENT / "policies" / "aion_interop.rego").read_text()
    assert "default allow := false" in policy
    assert "MODEL_EXECUTION_REQUESTED" in policy
    assert "NETWORK_ACCESS_REQUESTED" in policy
    assert "SUBJECTIVITY_PROMOTION_DETECTED" in policy
    assert "^[0-9a-f]{64}$" in policy
