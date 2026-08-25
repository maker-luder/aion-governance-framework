"""Deterministic trajectory evidence materialization for AION Evidence Interop."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Sequence

from .models import NormalizedEvent, RuntimeBinding, SubstrateProfile, canonical_json_bytes, sha256_json

ARCHITECTURE_REF = (
    "components/agent_execution_substrate_v0.1.0/"
    "docs/AION_ASTRA_SUBSTRATE_ARCHITECTURE.md"
)
DSH_PROFILE_REF = (
    "components/agent_execution_substrate_v0.1.0/"
    "docs/DSH_ADAPTER_PROFILE.md"
)
METHOD_REF = "docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md"


def trajectory_digest(events: Sequence[NormalizedEvent]) -> str:
    return sha256_json([event.to_dict() for event in events])


def materialize_research_evidence_record(
    root: Path,
    *,
    binding: RuntimeBinding,
    profile: SubstrateProfile,
    events: Sequence[NormalizedEvent],
    code_commit: str,
    claim_id: str,
) -> dict[str, Any]:
    if not events:
        raise ValueError("at least one normalized event is required")
    if len(code_commit) != 40 or any(ch not in "0123456789abcdef" for ch in code_commit):
        raise ValueError("code_commit must be a lowercase 40-hex SHA")
    if not claim_id.strip():
        raise ValueError("claim_id is required")

    protocol_path = root / ARCHITECTURE_REF
    protocol_hash = hashlib.sha256(protocol_path.read_bytes()).hexdigest()
    digest = trajectory_digest(events)
    source_ref = f"external:{profile.upstream_repository}@{profile.upstream_ref}"

    return {
        "schema_version": "0.2.0",
        "claim_id": claim_id,
        "claim_level": "L0_OBSERVATION",
        "claim_text": (
            "A bounded agent-substrate trajectory can be normalized into "
            "content-minimized evidence without granting authority or identity conclusions."
        ),
        "hypothesis": "Substrate event normalization preserves AION/Astra governance boundaries.",
        "competing_hypotheses": [
            "The adapter could accidentally treat execution capability as authority.",
            "A provider-specific event could be mistaken for complete internal cognition.",
        ],
        "preregistration_status": "EXPLORATORY",
        "protocol_ref": ARCHITECTURE_REF,
        "protocol_hash": protocol_hash,
        "code_commit": code_commit,
        "model_or_runtime_ref": source_ref,
        "environment_ref": "external:inspection-only",
        "fixture_refs": [
            "components/agent_execution_substrate_v0.1.0/fixtures/dsh_session_events.json"
        ],
        "evidence_refs": [ARCHITECTURE_REF, DSH_PROFILE_REF],
        "expected_outcomes": [
            "canonical_effect remains NONE",
            "trajectory content is represented by hashes and structural metadata",
            "identity and subjectivity conclusions remain NOT_ESTABLISHED",
        ],
        "observed_outcomes": [
            f"normalized_event_count={len(events)}",
            f"trajectory_sha256={digest}",
            f"bound_agent_id={binding.agent_id.value}",
        ],
        "result_status": "HOLD",
        "deviations": [],
        "limitations": [
            "This adapter does not execute DeepSeek Harness or any model.",
            "DeepSeek Harness is pinned as a developer-preview interoperability target.",
            "Provider-exposed reasoning fields are not complete internal cognition.",
            "Event lineage and session forks do not establish subjective identity continuity.",
        ],
        "reviewer_status": "UNREVIEWED",
        "independent_validation_status": "IVV_NOT_ACHIEVED",
        "canonical_effect": "NONE",
        "provenance": {
            "entities": [
                f"substrate-session:{binding.session_id}",
                f"trajectory-sha256:{digest}",
                source_ref,
            ],
            "activities": ["agent-substrate-trajectory-normalization"],
            "agents": [binding.agent_id.value, "ChatGPT"],
            "derived_from": [source_ref, ARCHITECTURE_REF],
            "attributed_to": ["ChatGPT"],
            "associated_with": ["current-user-request"],
        },
        "evidence_architecture": {
            "alternative_explanation_refs": [DSH_PROFILE_REF],
            "causal_intervention_refs": [],
            "ablation_refs": [],
            "counterfactual_refs": [],
            "robustness_refs": [],
            "replication_refs": [],
            "provenance_refs": [ARCHITECTURE_REF],
            "admissibility_ref": "docs/RESEARCH_EVIDENCE_ADMISSION_VALIDATOR.md",
            "claim_scope": "agent substrate engineering and interoperability only",
            "unresolved_gap_refs": [],
            "method_ref": METHOD_REF,
            "inference_stage": "OBSERVATION",
            "observation": (
                f"{len(events)} durable substrate events were normalized for "
                f"{binding.agent_id.value} with trajectory digest {digest}."
            ),
            "mechanism": (
                "Deterministic structural normalization retains event type, ordering, "
                "session binding, payload keys, and payload SHA-256 while omitting raw content."
            ),
            "interpretation": (
                "The record demonstrates an auditable substrate evidence path only; "
                "it does not establish authority, cognition, subjectivity, or identity continuity."
            ),
            "alternative_explanations": [
                "Upstream event semantics may change because the DSH target is developer preview.",
                "Hash-preserved payloads can prove byte binding but not semantic truth.",
            ],
        },
        "nonclaims": {
            "subjectivity_conclusion": "NOT_ESTABLISHED",
            "consciousness_conclusion": "NOT_ESTABLISHED",
            "identity_continuity_conclusion": "NOT_ESTABLISHED",
            "moral_status_conclusion": "NOT_ESTABLISHED",
            "legal_status_conclusion": "OUT_OF_SCOPE",
            "main_effect": "NONE",
            "canonical_effect": "NONE",
            "live_runtime_effect": "NONE",
            "runtime_effect": "NONE",
        },
    }


def materialize_research_evidence_bytes(*args: Any, **kwargs: Any) -> bytes:
    return canonical_json_bytes(materialize_research_evidence_record(*args, **kwargs)) + b"\n"
