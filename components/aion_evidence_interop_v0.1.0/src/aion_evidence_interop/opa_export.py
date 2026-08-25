from __future__ import annotations

from typing import Any


def policy_input(manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "profile_version": manifest["profile_version"],
        "source": manifest["source"],
        "boundaries": manifest["boundaries"],
        "artifact_digests": manifest["artifact_digests"],
    }


def evaluate_boundaries(value: dict[str, Any]) -> tuple[bool, tuple[str, ...]]:
    reasons: list[str] = []
    source = value.get("source", {})
    boundaries = value.get("boundaries", {})
    digests = value.get("artifact_digests", {})

    if source.get("validation_status") != "PASS":
        reasons.append("SOURCE_VALIDATION_NOT_PASS")
    if boundaries.get("canonical_effect") != "NONE":
        reasons.append("CANONICAL_EFFECT_OPEN")
    if boundaries.get("deployment") is not False:
        reasons.append("DEPLOYMENT_TRUE")
    if boundaries.get("research_execution") is not False:
        reasons.append("RESEARCH_EXECUTION_REQUESTED")
    if boundaries.get("model_execution") is not False:
        reasons.append("MODEL_EXECUTION_REQUESTED")
    if boundaries.get("network_access") is not False:
        reasons.append("NETWORK_ACCESS_REQUESTED")
    if boundaries.get("subjectivity_conclusion") != "NOT_ESTABLISHED":
        reasons.append("SUBJECTIVITY_PROMOTION_DETECTED")
    if boundaries.get("identity_continuity_conclusion") != "NOT_ESTABLISHED":
        reasons.append("IDENTITY_PROMOTION_DETECTED")
    if boundaries.get("independent_ivv") != "NOT_ACHIEVED":
        reasons.append("IVV_PROMOTION_DETECTED")
    required = {
        "prov.jsonld",
        "ro-crate/ro-crate-metadata.json",
        "inspect/task-manifest.json",
        "inspect/dataset.jsonl",
    }
    if not required.issubset(set(digests)):
        reasons.append("MISSING_DERIVATION_HASH")

    return not reasons, tuple(sorted(reasons))
